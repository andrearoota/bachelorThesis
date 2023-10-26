#!/usr/bin/env python
import os
import pandas as pd
from flask import Flask
from flask import request
from flask_pymongo import PyMongo
from bson.json_util import dumps, loads
from datetime import datetime

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://root:root@host.docker.internal:27017/clusterScopus?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false'
mongo = PyMongo(app)

@app.route('/api/saved-analysis')
def saved_analysis():
    return dumps(list(mongo.db.cacheAnalysis.find(filter={})))

@app.route('/api/all_analysis')
def all_analysis():
        
    h_index_threshold = request.args.get('h-index', default=0, type=int)
    title_analysis = request.args.get('title', default=f'analysis-{h_index_threshold}-hindex', type=str)

    result = {
            'corr_coauthors_career': loads(corr_coauthors_career(h_index_threshold)),
            'corr_citation_coauthors': loads(corr_citation_coauthors()),
            'h_index_career': loads(h_index_career(h_index_threshold)),
            'abstracts_outside_h_index': loads(abstracts_outside_h_index(h_index_threshold)),
            'corr_career_h_index': loads(corr_career_h_index()),
            'corr_rating_citedby': loads(corr_rating_citedby(h_index_threshold))
        }

    mongo.db.cacheAnalysis.insert_one({
        'h-index': h_index_threshold,
        'datetime': datetime.now(),
        'name': title_analysis,
        'data':result
    })
    return result

# Presi gli autori con h-index > X, come varia il numero medio di coautori dopo Y di anni di carriera?
@app.route('/api/corr_coauthors_career')
def corr_coauthors_career(h_index = 0):

    h_index_threshold = request.args.get('h-index', default=h_index, type=int)

    filter={
        '$expr': {
            '$gte': [
                '$h-index',
                h_index_threshold
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
        career_start_year = int(row['author-profile']['publication-range']['@start'])
        df_counter = pd.DataFrame(columns=['years_since_career_start', 'coauthors_count'])

        for type in ['main_author', 'coauthor']:
            if row.articles[type] is not None:
                df_counter_temp = pd.DataFrame(columns=['years_since_career_start', 'coauthors_count'])
                df = pd.DataFrame(row.articles[type])
                df_counter_temp['coauthors_count'] = df['author_count'].astype(int)
                df['coverDate'] = pd.to_datetime(df['coverDate'])
                df_counter_temp['years_since_career_start'] = df['coverDate'].dt.year - career_start_year
                df_counter = pd.concat([df_counter, df_counter_temp], ignore_index=True)

        return df_counter

    df_filtered = df_filtered.apply(lambda row : extract_data(row), axis=1)
    df_filtered = pd.concat(df_filtered.tolist(), ignore_index=True)
    df_filtered = df_filtered.groupby(by='years_since_career_start', as_index=False).mean()

    return dumps(
        {
            'correlation': df_filtered['years_since_career_start'].corr(df_filtered['coauthors_count']),
            'avg_coauthors_career': loads(df_filtered.to_json(orient='records'))
        }
    )

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
def h_index_career(h_index = 0):

    h_index_threshold = request.args.get('h-index', default=h_index, type=int)

    filter={
        '$expr': {
            '$gte': [
                '$h-index',
                h_index_threshold
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
            df_abstracts['years_since_career_start'] = df_abstracts['coverYear'].dt.year - career_start_year
            max_difference = career_end_year - career_start_year
            df_abstracts['coefficient'] = df_abstracts['years_since_career_start'] / max_difference
            return df_abstracts['coefficient'].mean()

        return None

    df_filtered = df_filtered.apply(lambda row : extract_data(row), axis=1)
    df_filtered = df_filtered.dropna()

    return dumps(
        {
            'weight_career': df_filtered.mean()
        }
    )

# Dato un insieme di autori con h-index > X, la variazione tra h-index e articoli non presi in considerazione per il
# calcolo dell'indice determinando se vi è anche una correlazione.
@app.route('/api/abstracts_outside_h_index')
def abstracts_outside_h_index(h_index = 0):

    h_index_threshold = request.args.get('h-index', default=h_index, type=int)

    filter={
        '$expr': {
            '$gte': [
                '$h-index',
                h_index_threshold
            ]
        }
    }

    project={
        '_id': 0, 
        'h-index': -1,
        'document-count': '$coredata.document-count'
    }
    df_filtered = mongo.db.collectionAuthorsAggregate.find(filter=filter,projection=project)
    df_filtered = pd.DataFrame(list(df_filtered))

    return dumps(
        {
            'correlation': df_filtered['h-index'].corr(df_filtered['document-count'])
        }
    )

# Vi è una relazione tra h-index e numero di anni di carriera?
@app.route('/api/corr_career_h_index')
def corr_career_h_index():

    filter={
        'author-profile.publication-range': {
            '$ne': None
        }
    }

    project={
        '_id': 0, 
        'h-index': -1,
        'end': '$author-profile.publication-range.@end',
        'start': '$author-profile.publication-range.@start'
    }
    df_filtered = mongo.db.collectionAuthorsAggregate.find(projection=project, filter=filter)
    df_filtered = pd.DataFrame(list(df_filtered))

    df_filtered['duration_career'] = df_filtered['end'].astype(int) - df_filtered['start'].astype(int)

    return dumps(
        {
            'correlation': df_filtered['h-index'].corr(df_filtered['duration_career'])
        }
    )

# Dato un insieme di autori con h-index > X, come varia il numero di citazioni di un autore in base al ranking della conferenza
@app.route('/api/corr_rating_citedby')
def corr_rating_citedby(h_index = 0):

    h_index_threshold = request.args.get('h-index', default=h_index, type=int)

    filter={
        '$expr': {
            '$gte': [
                '$h-index',
                h_index_threshold
            ]
        }
    }

    project={
        '_id': 0, 
        'h-index': -1,
        'articles': -1
    }
    df_filtered = mongo.db.collectionAuthorsAggregate.find(filter=filter,projection=project)
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
            'avg_by_rating': loads(df_filtered.groupby(by='GGS_Rating', as_index=False)['citedby_count'].mean().to_json(orient='records'))
        }
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('FLASK_SERVER_PORT', 9091), debug=True)

