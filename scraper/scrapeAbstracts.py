import pandas as pd
import os
from pymongo import MongoClient
from multiprocessing import Pool
from pybliometrics.scopus import ScopusSearch
from itertools import repeat

class AbstractDownloader:
    def __init__(self, start_year, end_year, subj_area):
        self.start_year = start_year
        self.end_year = end_year
        self.subj_area = subj_area
    
    def run(self):
        years_range = list(range(self.start_year, self.end_year + 1))
        
        print("Get all coverDate")
        with Pool(5) as pool:
            list_counts = pool.starmap(self.download_abstracts_by_year, zip(years_range, repeat(self.subj_area)))

        print(f"Abstracts scraped: {sum(list_counts)}")


    def is_downloaded(self, year):
        client = MongoClient(os.environ['MONGOBD_READ_URI'])
        filter_query = {'coverDate': {'$regex': f'{year}-.*'}}
        projection = {'_id': 1}
        result_query = client['clusterScopus']['collectionAbstracts'].find(filter=filter_query, projection=projection, limit=1)
        return len(list(result_query)) > 0

    def download_abstracts_by_year(self, year, subj_area):
        if not self.is_downloaded(year):
            scopus_search = ScopusSearch(query=f'subjarea({subj_area})', verbose=True, refresh=True, date=year)
            df_scopus = pd.DataFrame(scopus_search.results).fillna('')
            
            client = MongoClient(os.environ['MONGOBD_READ_URI'])
            client['clusterScopus']['collectionAbstracts'].insert_many(df_scopus.to_dict('records'))

            count = df_scopus.shape[0]
            print(f"Get and save {df_scopus.shape[0]} abstracts from {year}")
        
        else:
            print(f"Abstracts from {year} are already downloaded")
            count = 0

        return count