#!/usr/bin/env python
import os
import pandas as pd
from flask import Flask
from flask import request
from flask_pymongo import PyMongo
from bson.json_util import dumps

from datetime import datetime

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://root:root@host.docker.internal:27017/clusterScopus?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false'
mongo = PyMongo(app)

@app.route('/')
def todo():
    filter={
    '$text': {
            '$search': 'andr'
        }
    }
    project={
        'author-profile.preferred-name': 1
    }
    try:
        return f'{list(mongo.db.collectionAuthors.find(filter=filter,projection=project,limit=5))}'
    except:
        return 'Server not available'
    return 'Hello from the MongoDB client!\n'

# Presi gli autori con h-index > X, come varia il numero medio di coautori dopo Y di anni di carriera?
@app.route('/api/avg_coauthors_career')
def avg_coauthors_career():

    h_index_threshold = request.args.get('h-index', default=0, type=int)

    filter={
        '$expr': {
            '$gte': [
                {
                    '$toInt': '$h-index'
                }, h_index_threshold
            ]
        }
    }
    project={
        '_id': 0, 
        'articles': -1, 
        'author-profile.publication-range.@start': -1
    }

    df_filtered = mongo.db.collectionAuthorsAggregate.find(filter=filter,projection=project)
    df_filtered = pd.DataFrame(list(df_filtered))

    def extract_data(row):
        yearStart = int(row['author-profile']['publication-range']['@start'])
        df_counter = pd.DataFrame(columns=['years_since_creation', 'coauthors_count'])

        for type in ['main_author', 'coauthor']:
            if row.articles[type] is not None:
                df_counter_temp = pd.DataFrame(columns=['years_since_creation', 'coauthors_count'])
                df = pd.DataFrame(row.articles[type])
                df_counter_temp['coauthors_count'] = df['author_count'].astype(int)
                df['coverDate'] = pd.to_datetime(df['coverDate'])
                df_counter_temp['years_since_creation'] = df['coverDate'].dt.year - yearStart
                df_counter = pd.concat([df_counter, df_counter_temp], ignore_index=True)

        return df_counter

    df_filtered = df_filtered.apply(lambda row : extract_data(row), axis=1)
    df_filtered = pd.concat(df_filtered.tolist(), ignore_index=True)
    df_filtered = df_filtered.groupby(by='years_since_creation', as_index=False).mean()

    return df_filtered.to_json(orient='records')

# Vi è una relazione (e quindi un effetto sul h-index) tra il numero di coautori di un articolo e il numero di citazioni? Avere più coautori influisce sul numero di citazioni?
@app.route('/api/corr_citation_coauthors')
def corr_citation_coauthors():
    project={
        '_id': 0, 
        'articles': -1, 
    }
    df_filtered = mongo.db.collectionAuthorsAggregate.find(projection=project)
    df_filtered = pd.DataFrame(list(df_filtered))

    def extract_data(row):
        df_counter = pd.DataFrame(columns=['citedby_count', 'coauthors_count'])

        for type in ['main_author', 'coauthor']:
            if row.articles[type] is not None:
                df_counter_temp = pd.DataFrame(columns=['citedby_count', 'coauthors_count'])
                df = pd.DataFrame(row.articles[type])
                df_counter_temp['coauthors_count'] = df['author_count'].astype(int)
                df_counter_temp['citedby_count'] = df['citedby_count'].astype(int)
                df_counter = pd.concat([df_counter, df_counter_temp], ignore_index=True)

        return df_counter

    df_filtered = df_filtered.apply(lambda row : extract_data(row), axis=1)
    df_filtered = pd.concat(df_filtered.tolist(), ignore_index=True)

    return dumps(
        {
            'correlation': df_filtered['coauthors_count'].corr(df_filtered['citedby_count'])
        }
    )

# Presi gli autori con h-index > X, quando sono stati realizzati gli articoli che influiscono sull’h-index? In quale momento della carriera?
@app.route('/api/h_index_career')
def h_index_career():

    h_index_threshold = request.args.get('h-index', default=0, type=int)

    filter={
        '$expr': {
            '$gte': [
                {
                    '$toInt': '$h-index'
                }, h_index_threshold
            ]
        }
    }

    project={
        '_id': 0, 
        'articles': -1,
        'h-index': -1 ,
        'author-profile.publication-range': -1
    }
    df_filtered = mongo.db.collectionAuthorsAggregate.find(filter=filter,projection=project)
    df_filtered = pd.DataFrame(list(df_filtered))

    def extract_data(row):
        h_index = int(row['h-index'])
        career_start_year = int(row['author-profile']['publication-range']['@start'])
        career_end_year = int(row['author-profile']['publication-range']['@end'])
        df_abstracts = pd.DataFrame()

        for type in ['main_author', 'coauthor']:
            if row.articles[type] is not None:
                df_abstracts = pd.concat([df_abstracts, pd.DataFrame(row.articles[type])], ignore_index=True)

        if not df_abstracts.empty:
            df_abstracts = df_abstracts.sort_values('citedby_count', ascending=False).head(h_index)

            df_abstracts['coverYear'] = pd.to_datetime(df_abstracts['coverDate'])
            df_abstracts['years_since_creation'] = df_abstracts['coverYear'].dt.year - career_start_year
            max_difference = career_end_year - career_start_year
            df_abstracts['coefficient'] = df_abstracts['years_since_creation'] / max_difference
            return df_abstracts['coefficient'].mean()

        return None

    df_filtered = df_filtered.apply(lambda row : extract_data(row), axis=1)
    df_filtered = df_filtered.dropna()

    return dumps(
        {
            'weight_career': df_filtered.mean()
        }
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('FLASK_SERVER_PORT', 9091), debug=True)
