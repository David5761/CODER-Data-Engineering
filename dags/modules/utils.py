from .data_pipeline import DataPipeline

pipeline = DataPipeline()

def create_sql_objects() -> None:
    pipeline.get_connection()
    pipeline.create_sql_objects()
    pipeline.close_connection()

def run_etl() -> None:
    pipeline.get_connection()
    pipeline.etl_process()
    pipeline.close_connection()

