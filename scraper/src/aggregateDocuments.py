import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pymongo import MongoClient
from multiprocessing.pool import Pool
from pybliometrics.scopus import AuthorRetrieval
from pybliometrics.scopus import exception

class AggregateDocuments:

    COLLECTION_AUTHORS = 'collectionAuthors'
    COLLECTION_ABSTRACTS = 'collectionAbstracts'
    COLLECTION_AGGREGATE = 'collectionAuthorsAggregate'

    def __init__(self, mongodb_uri):
        self.mongodb_uri = mongodb_uri

    def download_author_by_id(self, id_author):
        return AuthorRetrieval(author_id=id_author, refresh=True)
    
    def get_abstracts_from_abstracts_collection(self, spark):
        return spark.read.format('mongodb').option('database', 'clusterScopus').option('collection', self.COLLECTION_ABSTRACTS).load()
    
    def get_authors_from_authors_collection(self, spark):
        return spark.read.format('mongodb').option('database', 'clusterScopus').option('collection', self.COLLECTION_AUTHORS).load()

    def split_author_ids(self, df):
        return df.withColumn('author_ids_array', split(col('author_ids'), ';'))

    def aggregate_main_authors(self, df_authors, df_abstracts):
        df_main_authors = df_abstracts. \
            where(col('author_ids_array') != array()). \
            withColumn('main_author', df_abstracts['author_ids_array'].getItem(0)). \
            groupBy(col('main_author').alias('main_author_ref')). \
            agg(collect_list(struct(df_abstracts.columns)).alias('main_author'))
        
        df_authors = df_authors.join(df_main_authors, split(df_authors.coredata['dc:identifier'], ':')[1] == df_main_authors.main_author_ref, 'left') \
            .drop('main_author_ref')
        
        return df_authors

    def aggregate_coauthors(self, df_authors, df_abstracts):
        df_coauthors = df_abstracts. \
            where(col('author_ids_array') != array()). \
            withColumn('author_ids_array', slice('author_ids_array', 2, size('author_ids_array'))). \
            withColumn('author_ids_array', explode('author_ids_array')). \
            groupBy(col('author_ids_array').alias('coauthor_ref')). \
            agg(collect_list(struct(df_abstracts.columns)).alias('coauthor'))
        
        df_authors = df_authors.join(df_coauthors, split(df_authors.coredata['dc:identifier'], ':')[1] == df_coauthors.coauthor_ref, 'left') \
            .drop('coauthor_ref')
        
        df_authors = df_authors.select('*', struct('main_author', 'coauthor').alias('articles')). \
            drop('main_author'). \
            drop('coauthor'). \
            drop('author_ids_array')
        
        return df_authors

    def aggregate(self):
        spark = SparkSession.builder \
            .config('spark.driver.memory', '30g') \
            .config('spark.mongodb.read.connection.uri', self.mongodb_uri) \
            .config('spark.mongodb.write.connection.uri', self.mongodb_uri) \
            .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:10.2.0') \
            .getOrCreate()

        print('Get all authors from authors')
        df_authors = self.get_authors_from_authors_collection(spark)

        if df_authors.isEmpty():
            print('there are zero authors')
            return

        print('Get all abstracts from abstracts')
        df_abstracts = self.get_abstracts_from_abstracts_collection(spark)

        if df_abstracts.isEmpty():
            print('there are zero abstracts')
            return

        df_abstracts_split_ids = self.split_author_ids(df_abstracts)
        df_authors = self.aggregate_main_authors(df_authors, df_abstracts_split_ids)
        df_authors = self.aggregate_coauthors(df_authors, df_abstracts_split_ids)

        df_authors.write \
            .format('mongodb') \
            .option('database', 'clusterScopus').option('collection', self.COLLECTION_AGGREGATE) \
            .mode('overwrite') \
            .save()
        
        print('Abstracts aggregated')