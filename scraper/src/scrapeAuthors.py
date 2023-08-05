import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pymongo import MongoClient
from multiprocessing.pool import Pool
from pybliometrics.scopus import AuthorRetrieval

class AuthorDownloader:

    def __init__(self, mongodb_uri):
        self.mongodb_uri = mongodb_uri

    def download_author_by_id(self, id_author):
        return AuthorRetrieval(author_id=id_author, refresh=True)

    def get_authors_from_abstracts(self, spark, client):
        filter_query = {'author_ids': {'$ne': ''}}
        projection = {'_id': 0, 'author_ids': 1}
        result_query = client['clusterScopus']['collectionAbstracts'].find(filter=filter_query, projection=projection)
        df_authors_from_abstracts = pd.DataFrame(list(result_query))

        spark_authors_from_abstracts = spark.createDataFrame(df_authors_from_abstracts)
        spark_authors_from_abstracts_distinct = spark_authors_from_abstracts.select(explode(split(col('author_ids'), ';')).alias('author_id')).dropDuplicates()

        return spark_authors_from_abstracts_distinct

    def get_authors_from_authors_collection(self, spark, client):
        filter_query = {}
        projection = {'_id': 0, 'coredata.dc:identifier': 1}
        result_query = client['clusterScopus']['collectionAuthors'].find(filter=filter_query, projection=projection)
        df_authors_from_authors = pd.DataFrame(list(result_query))

        spark_authors_from_authors = spark.createDataFrame(df_authors_from_authors)
        spark_authors_from_authors = spark_authors_from_authors.select(element_at(split(col('coredata.dc:identifier'), ':'), -1).alias('author_id')).dropDuplicates()

        return spark_authors_from_authors

    def download_authors_from_abstracts(self):
        spark = SparkSession.builder \
            .config("spark.driver.memory", "15g") \
            .config("spark.mongodb.read.connection.uri", self.mongodb_uri) \
            .config("spark.mongodb.write.connection.uri", self.mongodb_uri) \
            .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.2.0") \
            .getOrCreate()

        client = MongoClient(self.mongodb_uri)

        print("Get all authors from abstracts")
        spark_authors_from_abstracts_distinct = self.get_authors_from_abstracts(spark, client)

        print("Get all authors from authors")
        spark_authors_from_authors = self.get_authors_from_authors_collection(spark, client)

        if not spark_authors_from_authors.isEmpty():
            spark_authors_from_abstracts_distinct = spark_authors_from_abstracts_distinct.join(
                spark_authors_from_authors,
                'author_id',
                'leftanti')

        df_authors_to_search = spark_authors_from_abstracts_distinct.toPandas()
        count = df_authors_to_search.shape[0]

        # Download data for each author
        for index, row in df_authors_to_search.iterrows():
            author_id = row['author_id']
            print(f"Get author > {author_id} | {index + 1}/{count}")
            client['clusterScopus']['collectionAuthors'].insert_one(self.download_author_by_id(author_id)._json)
