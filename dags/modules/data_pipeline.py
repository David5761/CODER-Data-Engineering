from .db import Database
from dotenv import load_dotenv
import os

load_dotenv()

class DataPipeline():
    def __init__(self) -> None:
        self.config = {
            "REDSHIFT_USER" : os.getenv('REDSHIFT_USER'),
            "REDSHIFT_PASSWORD" : os.getenv('REDSHIFT_PASSWORD'),
            "REDSHIFT_HOST" : os.getenv('REDSHIFT_HOST'),
            "REDSHIFT_PORT" : os.getenv('REDSHIFT_PORT'),
            "REDSHIFT_DB" : os.getenv('REDSHIFT_DB'),
        }
        self.db = Database(config=self.config)

    def get_connection(self) -> None:
                self.db.get_connection()

    def create_sql_objects(self) -> None:
                self.db.cargar_datos_redshift()
                
    def etl_process(self) -> None:
                """
                Extract, Transform, Load
                """
                self.db.insert_data_table()

    def close_connection(self) -> None:
                self.db.close_conn()

if __name__ == "__main__":
    etl = DataPipeline()
    etl.get_connection()
    etl.create_sql_objects()
    etl.etl_process()
    etl.close_connection()