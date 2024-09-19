import psycopg2


class DatabaseConnection():
    def __init__(self, config: dict) -> None:
        self.config = config

    def get_connection(self):
        username = self.config.get('REDSHIFT_USER')
        password = self.config.get('REDSHIFT_PASSWORD')
        host = self.config.get('REDSHIFT_HOST')
        port = self.config.get('REDSHIFT_PORT', '5439')
        dbname = self.config.get('REDSHIFT_DB')
        try:
            with psycopg2.connect(host= host,dbname= dbname,user= username,password= password,port= port) as self.conn:
                print("Conectado a Redshift con éxito!")
                return self.conn
        except Exception as e:
            print("No es posible conectar a Redshift")
            print(e)

    def close_conn(self) -> None:
            """ Close connection """
            try:
                self.conn.close()
                print('Connection closed...')
            except Exception as e:
                print("No es posible cerrar la conexion a Redshift")
                print(e)
                exit()