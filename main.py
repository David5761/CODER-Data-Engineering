import requests
import json
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import os
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

load_dotenv()

REDSHIFT_USER = os.getenv('REDSHIFT_USER')
REDSHIFT_PASSWORD = os.getenv('REDSHIFT_PASSWORD')
REDSHIFT_HOST = os.getenv('REDSHIFT_HOST')
REDSHIFT_PORT = os.getenv('REDSHIFT_PORT')
REDSHIFT_DB = os.getenv('REDSHIFT_DB')

print ( REDSHIFT_USER)
try:
    conn = psycopg2.connect(
        host= REDSHIFT_HOST,
        dbname= REDSHIFT_DB,
        user= REDSHIFT_USER,
        password= REDSHIFT_PASSWORD,
        port= REDSHIFT_PORT
    )
    print("Conectado a Redshift con éxito!")
    
except Exception as e:
    print("No es posible conectar a Redshift")
    print(e)

with conn.cursor() as cur:
    cur.execute("""
        DROP TABLE u202112462_coderhouse.news;
        CREATE TABLE IF NOT EXISTS u202112462_coderhouse.news
        (
	    id VARCHAR(100) primary key  
	    ,title VARCHAR(255)   
	    ,description VARCHAR(355)  
	    ,url VARCHAR(255)   
	    ,author VARCHAR(100)   
	    ,image VARCHAR(255) 
	    ,language VARCHAR(10) 
	    ,category VARCHAR(25)  
	    ,published VARCHAR(255)   	    
        )
    """)
    conn.commit()    



with conn.cursor() as cur:
    execute_values(
        cur,
        '''
        INSERT INTO news (id, title, description, url, author, image, language, category,published)
        VALUES %s
        ''',
        [tuple(row) for row in df.values],
        page_size=len(df)
    )
    conn.commit()
    print('Datos insertados!')
