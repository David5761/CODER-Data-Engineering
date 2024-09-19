import psycopg2
from .connection import DatabaseConnection

class CreateTables(DatabaseConnection):
    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.table_name = 'u202112462_coderhouse.news'

    def cargar_datos_redshift(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name}
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
            self.conn.commit()
            print("Tabla creada correctamente")
            
        except Exception as e:
            print(e)
            self.conn.rollback()
            exit()    