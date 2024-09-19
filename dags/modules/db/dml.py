import psycopg2
from .create_table import CreateTables
from psycopg2.extras import execute_values
import requests
import json
import pandas as pd

class DataManipulation(CreateTables):
    def __init__(self, config: dict) -> None:
        super().__init__(config)

    def preprocessing_data(self) -> pd.DataFrame:
        url_api = ('https://api.currentsapi.services/v1/latest-news?'
            'language=es&'
            'apiKey=CMJE0UO4CVU8WKiGkEOvrQMCHlYGQvv0zsOAGXAJ_Oiuxqcf')
        response = requests.get(url_api)


        data = []
        data_json = json.loads(response.text)

        for i in range(len(data_json['news'])):
            data.append(data_json['news'][i])


        df = pd.json_normalize(data, sep='_')

        for i in range (len(data_json['news'])):
            df.loc[i, "category"]= df['category'][i][0]
        
        return df
    


    def insert_data_table(self) -> None:
        try:
            df = self.preprocessing_data()
            with self.conn.cursor() as cur:
                execute_values(
                cur,
                '''
                INSERT INTO news (id, title, description, url, author, image, language, category,published)
                VALUES %s
                ''',
                [tuple(row) for row in df.values],
                page_size=len(df)) 
            self.conn.commit()
            print('Datos insertados!')            
        except Exception as e:
            print(e)
            self.conn.rollback()
            exit()
