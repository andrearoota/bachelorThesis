import pandas as pd
import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pymongo import MongoClient
from multiprocessing.pool import Pool
from pybliometrics.scopus import AuthorRetrieval
from pybliometrics.scopus import exception

class AuthorDownloader:

    COLLECTION_AUTHORS = 'collectionAuthors'
    COLLECTION_ABSTRACTS = 'collectionAbstracts'
    COLLECTION_AGGREGATE = 'collectionAuthorsAggregate'

    def __init__(self, mongodb_uri):
        self.mongodb_uri = mongodb_uri

    def download_author_by_id(self, id_author):
        return AuthorRetrieval(author_id=id_author, refresh=True)

    def get_authors_from_abstracts(self, spark):
        spark_authors_from_abstracts = spark.read.format('mongodb').option('database', 'clusterScopus').option('collection', self.COLLECTION_ABSTRACTS).load()
        spark_authors_from_abstracts = spark_authors_from_abstracts.filter("author_ids != ''")
        return spark_authors_from_abstracts.select(explode(split(col('author_ids'), ';')).alias('author_id')).dropDuplicates()

    def get_authors_from_authors_collection(self, spark):
        spark_authors_from_authors = spark.read.format('mongodb').option('database', 'clusterScopus').option('collection', self.COLLECTION_AUTHORS).load()
        return spark_authors_from_authors.select(element_at(split(col('coredata.dc:identifier'), ':'), -1).alias('author_id')).dropDuplicates()

    def download_authors_from_abstracts(self):
        spark = SparkSession.builder \
            .config("spark.driver.memory", "30g") \
            .config("spark.mongodb.read.connection.uri", self.mongodb_uri) \
            .config("spark.mongodb.write.connection.uri", self.mongodb_uri) \
            .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.2.0") \
            .getOrCreate()

        client = MongoClient(self.mongodb_uri)

        print("Get all authors from abstracts")
        spark_authors_from_abstracts_distinct = self.get_authors_from_abstracts(spark)

        print("Get all authors from authors")
        spark_authors_from_authors = self.get_authors_from_authors_collection(spark)

        if not spark_authors_from_authors.isEmpty():
            spark_authors_from_abstracts_distinct = spark_authors_from_abstracts_distinct.join(
                spark_authors_from_authors,
                'author_id',
                'leftanti')

        df_authors_to_search = spark_authors_from_abstracts_distinct.toPandas()
        count = df_authors_to_search.shape[0]

        # Download data for each author
        for index, row in df_authors_to_search.iterrows():
            time.sleep(0.34) # Sometimes pybliometrics sleep doesn't work. 
            author_id = row['author_id']
            print(f"Get author > {author_id} | {index + 1}/{count}")
            try:
                client['clusterScopus']['collectionAuthors'].insert_one(self.download_author_by_id(author_id)._json)
            except exception.Scopus404Error:
                print(f"author {row['author_id']} not found")

