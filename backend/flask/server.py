#!/usr/bin/env python
import os
import pandas as pd
from flask import Flask
from flask import request
from flask_pymongo import PyMongo
from bson.json_util import dumps, loads
from datetime import datetime
import numpy as np
from analyses import analyses

ANALYSES = [
    'average_coauthors_variation_after_years',
    'coauthors_impact_on_citations_and_hindex',
    'analyze_hindex_influential_articles_timing',
    'correlation_between_hindex_and_excluded_articles',
    'correlation_between_hindex_and_career_duration',
    'citation_count_based_on_conference_ranking'
]

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://root:root@host.docker.internal:27017/clusterScopus?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false'
mongo = PyMongo(app)

@app.route('/api/saved_analyses')
def saved_analysis():
    return dumps(list(mongo.db.cacheAnalysis.find(filter={})))


@app.route('/api/all_analyses')
def all_analyses():
        
    h_index_threshold = request.args.get('h-index', default=0, type=int)
    title_analyses = request.args.get('title', default=f'analysis-{h_index_threshold}-hindex', type=str)
    analyses_obj = analyses(mongo, h_index_threshold)
    result_analyses = {}

    for name_analysis in ANALYSES:
        result_analyses[name_analysis] = loads(
            getattr(analyses_obj, name_analysis)())

    mongo.db.cacheAnalysis.insert_one({
        'h-index': h_index_threshold,
        'datetime': datetime.now(),
        'name': title_analyses,
        'data': result_analyses
    })

    return result_analyses


# Given authors with an h-index > X, how does the average number of co-authors change after Y years of their career?
@app.route('/api/average_coauthors_variation_after_years')
def average_coauthors_variation_after_years_api():
    h_index_threshold = request.args.get('h-index', default=0, type=int)
    analyses_obj = analyses(mongo, h_index_threshold)

    return analyses_obj.average_coauthors_variation_after_years()


# Is there a relationship (and therefore an effect on the h-index) between the number of co-authors on an article and the number of citations?
# Does having more co-authors influence the number of citations?
@app.route('/api/coauthors_impact_on_citations_and_hindex')
def coauthors_impact_on_citations_and_hindex_api():
    analyses_obj = analyses(mongo)

    return analyses_obj.coauthors_impact_on_citations_and_hindex()


# Among authors with an h-index > X, when were the articles that influence the h-index published? At what point in their careers?
@app.route('/api/analyze_hindex_influential_articles_timing')
def analyze_hindex_influential_articles_timing_api():
    h_index_threshold = request.args.get('h-index', default=0, type=int)
    analyses_obj = analyses(mongo, h_index_threshold)

    return analyses_obj.analyze_hindex_influential_articles_timing()
    

# Given a set of authors with an h-index > X, is there a correlation between the h-index variation
# and the number of articles not considered for the index calculation?
@app.route('/api/correlation_between_hindex_and_excluded_articles')
def correlation_between_hindex_and_excluded_articles_api():
    h_index_threshold = request.args.get('h-index', default=0, type=int)
    analyses_obj = analyses(mongo, h_index_threshold)

    return analyses_obj.correlation_between_hindex_and_excluded_articles()


# Is there a relationship between h-index and the number of years in one's career?
@app.route('/api/correlation_between_hindex_and_career_duration')
def correlation_between_hindex_and_career_duration_api():
    analyses_obj = analyses(mongo)

    return analyses_obj.correlation_between_hindex_and_career_duration()


# Given a set of authors with an h-index > X, is there a correlation between the number of citations 
# of an abstract and the conference ranking?
@app.route('/api/citation_count_based_on_conference_ranking')
def citation_count_based_on_conference_ranking_api():
    h_index_threshold = request.args.get('h-index', default=0, type=int)
    analyses_obj = analyses(mongo, h_index_threshold)

    return analyses_obj.citation_count_based_on_conference_ranking()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('FLASK_SERVER_PORT', 9091), debug=True)

