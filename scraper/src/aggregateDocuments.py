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
    FILENAME_CONFERENCE_RATING = '/Users/andrearota/Documents/GitHub/bachelorThesis/scraper/data/GII-GRIN-SCIE-Conference-Rating-24-ott-2021.csv'

    def __init__(self, mongodb_uri):
        self.mongodb_uri = mongodb_uri

    def download_author_by_id(self, id_author):
        return AuthorRetrieval(author_id=id_author, refresh=True)
    
    def get_abstracts_from_abstracts_collection(self, spark):
        return spark.read.format('mongodb').option('database', 'clusterScopus').option('collection', self.COLLECTION_ABSTRACTS).load()
    
    def get_authors_from_authors_collection(self, spark):
        return spark.read.format('mongodb').option('database', 'clusterScopus').option('collection', self.COLLECTION_AUTHORS).load()

    def convert_string_column_to_int(self, spark_collection, column_name):
        return spark_collection.withColumn(column_name, spark_collection[column_name].cast('int'))

    def split_author_ids(self, spark_collection):
        return spark_collection.withColumn('author_ids_array', split(col('author_ids'), ';'))

    def join_conference_rating(self, spark, spark_abstracts):
        df_conference_rating = spark.read.options(delimiter=';', header=True).csv(self.FILENAME_CONFERENCE_RATING)
        df_conference_rating = df_conference_rating.filter(df_conference_rating['GGS Rating'] != 'Work in Progress')
        df_conference_rating = df_conference_rating.withColumnRenamed('GGS Rating','GGS_Rating')

        return spark_abstracts.alias('base').join(df_conference_rating.alias('external'), lower(col('publicationName')).contains(lower(df_conference_rating['Title'])), 'left') \
            .selectExpr('base.*', 'external.GGS_Rating')

    def aggregate_main_authors(self, spark_authors, spark_abstracts):
        spark_main_authors = spark_abstracts. \
            where(col('author_ids_array') != array()). \
            withColumn('main_author', spark_abstracts['author_ids_array'].getItem(0)). \
            groupBy(col('main_author').alias('main_author_ref')). \
            agg(collect_list(struct(spark_abstracts.columns)).alias('main_author'))
        
        spark_authors = spark_authors.join(spark_main_authors, split(spark_authors.coredata['dc:identifier'], ':')[1] == spark_main_authors.main_author_ref, 'left') \
            .drop('main_author_ref')
        
        return spark_authors

    def aggregate_coauthors(self, spark_authors, spark_abstracts):
        spark_coauthors = spark_abstracts. \
            where(col('author_ids_array') != array()). \
            withColumn('author_ids_array', slice('author_ids_array', 2, size('author_ids_array'))). \
            withColumn('author_ids_array', explode('author_ids_array')). \
            groupBy(col('author_ids_array').alias('coauthor_ref')). \
            agg(collect_list(struct(spark_abstracts.columns)).alias('coauthor'))
        
        spark_authors = spark_authors.join(spark_coauthors, split(spark_authors.coredata['dc:identifier'], ':')[1] == spark_coauthors.coauthor_ref, 'left') \
            .drop('coauthor_ref')
        
        spark_authors = spark_authors.select('*', struct('main_author', 'coauthor').alias('articles')). \
            drop('main_author'). \
            drop('coauthor'). \
            drop('author_ids_array')
        
        return spark_authors

    def aggregate(self):
        spark = SparkSession.builder \
            .config('spark.driver.memory', '30g') \
            .config('spark.mongodb.read.connection.uri', self.mongodb_uri) \
            .config('spark.mongodb.write.connection.uri', self.mongodb_uri) \
            .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:10.2.0') \
            .getOrCreate()

        print('Get all authors from authors')
        spark_authors = self.get_authors_from_authors_collection(spark)

        """ if spark_authors.isEmpty():
            print('there are zero authors')
            return """

        print('Get all abstracts from abstracts')
        spark_abstracts = self.get_abstracts_from_abstracts_collection(spark)

        """ if spark_abstracts.isEmpty():
            print('there are zero abstracts')
            return """

        print('Convert some string fields to int')
        spark_authors = self.convert_string_column_to_int(spark_authors, 'h-index')
        spark_authors = self.convert_string_column_to_int(spark_authors, 'coauthor-count')
        spark_abstracts = self.convert_string_column_to_int(spark_abstracts, 'author_count')

        print('Search GGS rating conference')
        spark_abstracts = self.join_conference_rating(spark, spark_abstracts)

        spark_abstracts_split_ids = self.split_author_ids(spark_abstracts)
        spark_authors = self.aggregate_main_authors(spark_authors, spark_abstracts_split_ids)
        spark_authors = self.aggregate_coauthors(spark_authors, spark_abstracts_split_ids)

        spark_authors.write \
            .format('mongodb') \
            .option('database', 'clusterScopus').option('collection', self.COLLECTION_AGGREGATE) \
            .mode('overwrite') \
            .save()
        
        print('Abstracts aggregated')