from datetime import datetime, timedelta
from email import message
from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator

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

def cargar_datos_redshift(conn, table_name, dataframe):
    with conn.cursor() as cur:
        cur.execute(f"""
        DROP TABLE {table_name};
        CREATE TABLE IF NOT EXISTS {table_name}
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
        [tuple(row) for row in dataframe.values],
        page_size=len(dataframe)
    )
    conn.commit()
    print('Datos insertados!')


cargar_datos_redshift(conn=conn,table_name='u202112462_coderhouse.news',dataframe=df)
conn.close()

## TAREAS

default_args={
    'owner': 'JeseSalazar',
    'retries': 5,
    'retry_delay': timedelta(minutes=2) # 2 min de espera antes de cualquier re intento
}

api_dag = DAG(
        dag_id="proyecto-final_pipeline",
        default_args= default_args,
        description="DAG para consumir API y vaciar datos en Redshift",
        start_date=datetime(2023,5,11,2),
        schedule_interval='@daily' 
    )

task1 = BashOperator(task_id='primera_tarea',
    bash_command='echo Iniciando...'
)


task3 = BashOperator(
    task_id= 'tercera_tarea',
    bash_command='echo Proceso completado...'
)
task1 >> task3