from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
import os
from modules import create_sql_objects, run_etl



## TAREAS

default_args={
    'owner': 'DavidToledo',
    'retries': 5,
    'retry_delay': timedelta(minutes=2), # 2 min de espera antes de cualquier re intento
    'depends_on_past': True,
    'email_on_retry': True
}

with DAG(
    dag_id="proyecto-final_pipeline",
        default_args= default_args,
        description="DAG para consumir API News",
        start_date=datetime(2024, 1, 31),
        schedule_interval='@daily',
        catchup=False
    ) as dag:

    task1 = PythonOperator(
        task_id='primera_tarea',
        python_callable=create_sql_objects
    )

    task2 = PythonOperator(
        task_id='segunda_tarea',
        python_callable=run_etl
    )

    
    t_email_notification_success = EmailOperator(
        task_id='email_notification',
        to=os.getenv('TO_EMAIL'),
        subject=os.getenv('AIRFLOW_VAR_SUBJECT_MAIL'),
        html_content="Hola Usuario! El DAG en Airflow, {{ dag.dag_id }}, finalizó correctamente."
    )

    # Email on failure
    
    t_email_notification_failure = EmailOperator(
        task_id='email_notification_failure',
        to=os.getenv('TO_EMAIL'),
        subject='Fallo en el DAG {{ dag.dag_id }}',
        html_content="El DAG {{ dag.dag_id }} ha fallado.",
        trigger_rule='one_failed'  # Se ejecuta si alguna tarea falla
    )

    task1 >> task2 >>t_email_notification_success
    [task1, task2] >> t_email_notification_failure


