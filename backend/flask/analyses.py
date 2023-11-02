import pandas as pd
from numpy import nan
from flask_pymongo import PyMongo
from bson.json_util import dumps, loads
from datetime import datetime

class analyses:
    def __init__(self, mongo, h_index = 0):
        self.mongo = mongo
        self.h_index = h_index

    def average_coauthors_variation_after_years(self):
        filter={
            'author-profile.publication-range.@start': {
                '$exists': True
            }, 
            'h-index': {
                '$gte': self.h_index
            }
        }
        project={
            '_id': 0, 
            'articles': 1, 
            'author-profile.publication-range.@start': 1
        }

        df_filtered = self.mongo.db.collectionAuthorsAggregate.find(filter=filter,projection=project)
        df_filtered = pd.DataFrame(list(df_filtered))

        def extract_data(row):
            career_start_year = int(row['author-profile']['publication-range']['@start'])
            df_counter = pd.DataFrame(columns=['years_since_career_start', 'coauthors_count'])

            for type in ['main_author', 'coauthor']:
                if row.articles[type] is not None:
                    df_counter_temp = pd.DataFrame(columns=['years_since_career_start', 'coauthors_count'])
                    df = pd.DataFrame(row.articles[type])
                    df_counter_temp['coauthors_count'] = df['author_count']
                    df['coverDate'] = [x[:4] for x in df['coverDate']]
                    df_counter_temp['years_since_career_start'] = df['coverDate'].astype(int) - career_start_year
                    df_counter = pd.concat([df_counter, df_counter_temp], ignore_index=True)

            return df_counter

        df_filtered = df_filtered.apply(lambda row : extract_data(row), axis=1)
        df_filtered = pd.concat(df_filtered.tolist(), ignore_index=True)
        df_filtered = df_filtered.groupby(by='years_since_career_start', as_index=False).mean()

        return dumps(
            {
                'correlation': df_filtered['years_since_career_start'].corr(df_filtered['coauthors_count']),
                'data': loads(df_filtered.to_json(orient='records'))
            }
        )

    def coauthors_impact_on_citations_and_hindex(self):
        project={
        '_id': 0, 
        'author_count': 1,
        'citedby_count': 1
        }
        df_filtered =self.mongo.db.collectionAbstracts.find(projection=project)
        df_filtered = pd.DataFrame(list(df_filtered))

        df_filtered['author_count'].replace('', nan, inplace=True)
        df_filtered['citedby_count'].replace('', nan, inplace=True)
        df_filtered.dropna(subset=['author_count', 'citedby_count'], inplace=True)
        
        df_filtered = df_filtered.astype({'author_count': 'int', 'citedby_count': 'int'})

        return dumps(
            {
                'correlation': df_filtered['author_count'].corr(df_filtered['citedby_count']),
                'data': loads(df_filtered.drop_duplicates(subset=['author_count', 'citedby_count']).to_json(orient='records'))
            }
        )

    def analyze_hindex_influential_articles_timing(self):
        filter={
            'author-profile.publication-range.@start': {
                '$exists': True
            },
            'author-profile.publication-range.@end': {
                '$exists': True
            },
            'h-index': {
                '$gte': self.h_index
            }
        }

        project={
            '_id': 0, 
            'articles': 1,
            'h-index': 1 ,
            'author-profile.publication-range': 1
        }
        df_filtered =self.mongo.db.collectionAuthorsAggregate.find(filter=filter,projection=project)
        df_filtered = pd.DataFrame(list(df_filtered))

        def extract_data(row):
            h_index = int(row['h-index'])
            career_start_year = int(row['author-profile']['publication-range']['@start'])
            career_end_year = int(row['author-profile']['publication-range']['@end'])
            df_abstracts = pd.DataFrame()

            for type in ['main_author', 'coauthor']:
                if row.articles[type] is not None:
                    df_abstracts = pd.concat([df_abstracts, pd.DataFrame(row.articles[type])[['coverDate', 'citedby_count']]], ignore_index=True)

            if not df_abstracts.empty:
                df_abstracts = df_abstracts.sort_values('citedby_count', ascending=False).head(h_index)

                df_abstracts['coverYear'] = pd.to_datetime(df_abstracts['coverDate'])
                df_abstracts['years_since_career_start'] = df_abstracts['coverYear'].dt.year - career_start_year
                max_difference = career_end_year - career_start_year
                df_abstracts['coefficient'] = df_abstracts['years_since_career_start'] / max_difference
                return df_abstracts['coefficient'].mean()

            return None

        df_filtered = df_filtered.apply(lambda row : extract_data(row), axis=1)
        df_filtered = df_filtered.dropna()

        return dumps(
            {
                'weight_career_avg': df_filtered.mean(),
                'data': loads(df_filtered.to_json(orient='records'))
            }
        )

    def correlation_between_hindex_and_excluded_articles(self):
        filter={
            'h-index': {
                '$gte': self.h_index
            }
        }

        project={
            '_id': 0, 
            'h-index': 1,
            'document-count': '$coredata.document-count'
        }
        df_filtered =self.mongo.db.collectionAuthorsAggregate.find(filter=filter,projection=project)
        df_filtered = pd.DataFrame(list(df_filtered))
        df_filtered['document-count'] = df_filtered['document-count'].astype(int) - df_filtered['h-index']

        return dumps(
            {
                'correlation': df_filtered['h-index'].corr(df_filtered['document-count']),
                'data': loads(df_filtered.drop_duplicates(subset=['h-index', 'document-count']).to_json(orient='records'))
            }
        )

    def correlation_between_hindex_and_career_duration(self):
        filter={
            'author-profile.publication-range': {
                '$ne': None
            }
        }

        project={
            '_id': 0, 
            'h-index': 1,
            'end': '$author-profile.publication-range.@end',
            'start': '$author-profile.publication-range.@start'
        }
        df_filtered =self.mongo.db.collectionAuthorsAggregate.find(projection=project, filter=filter)
        df_filtered = pd.DataFrame(list(df_filtered))

        df_filtered['duration_career'] = df_filtered['end'].astype(int) - df_filtered['start'].astype(int)

        return dumps(
            {
                'correlation': df_filtered['h-index'].corr(df_filtered['duration_career']),
                'data': loads(df_filtered.drop_duplicates(subset=['duration_career', 'h-index'])[['duration_career', 'h-index']].to_json(orient='records'))
            }
        )

    def citation_count_based_on_conference_ranking(self):
        filter={
            'h-index': {
                '$gte': self.h_index
            }
        }

        project={
            '_id': 0, 
            'h-index': 1,
            'articles': 1
        }
        df_filtered =self.mongo.db.collectionAuthorsAggregate.find(filter=filter,projection=project)
        df_filtered = pd.DataFrame(list(df_filtered))

        def extract_data(row):
            df_abstracts = pd.DataFrame()

            for type in ['main_author', 'coauthor']:
                if row.articles[type] is not None:
                    df = pd.DataFrame(row.articles[type])
                    df = df[df['GGS_Rating'].notna()]
                    df_abstracts = pd.concat([df_abstracts, df], ignore_index=True)

            return df_abstracts

        df_filtered = df_filtered.apply(lambda row : extract_data(row), axis=1)
        df_filtered = pd.concat(df_filtered.tolist(), ignore_index=True)

        return dumps(
            {
                'correlation': df_filtered['GGS_Rating'].astype('category').cat.codes.corr(df_filtered['citedby_count']),
                'data': loads(df_filtered.groupby(by='GGS_Rating', as_index=False)['citedby_count'].mean().to_json(orient='records'))
            }
        )
