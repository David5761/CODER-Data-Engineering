# Proyecto Final Data Engineering

### Requisitos
Para completar las variables que usa el archivo docker-compose.yaml se debe utilizar el archivo .env

NOTA: Para ejecutar el proyecto se debe tener los servicios de docker activos y ejecutar el siguiente comando:
  ```bash
    docker-comnpose up
  ```
## Descripción del proyecto 

Este es un proyecto de Data Engineering en la cual se desarrollo todo el flujo ETL acerca de registros e información de noticias actuales. Se usó una base de datos de Amazon Redshift y la herramienta AirFlow para la ingesta y transformación de los datos. Asimismo, se utilizó librerias de Python como Psycog2 y Pandas principalmente.

### Flujo de datos del proyecto

1. **Extracción de datos**: Los registros de las noticias actuales más relevantes se obtiene a través de una API de Currents API. Esta API nos brinda información acerca del título de la noticia, descripción, imagen asociada, categoria de la noticia, idioma, autor, dia y fecha de la publicación. Esta información se podría modificar en base a las preferencias o requerimientos del consumidor de esta API como buscar por palabra de interés, por idioma, hora, categoria, etc.
   
2. **Transformación de datos**: Los registros son transformados usando Dataframes para darle el formato y los valores adecuados para su manejo y posterior ingesta a la base de datos. Además, esta información es facilmente manejable según los datos o campos que se requiera guardar.
   
3. **Carga de datos**: Los registros transformados se cargan en una base de datos Redshift. Se valida que exista la tabla, en caso contrario se crea y posteriormente se inserta los registros nuevos.
   
4. **Orquestación de Apache Airflow**:
   - **Configuración**: Este proceso ETL esta configurado para ejecutarse diariamente y de manera secuencial. Es decir, si hay un error en uno de las tareas, las tareas posteriores no se van a ejecutar.
   - **Ejecución manual**: En caso se requiera ejecutar de forma manual e inmmediata se necesita ingresar las credenciales de Apache Airflow y ejecutar manualmente el DAG llamado "proyecto-final_pipeline"

### Resumen de las principales funciones
- **get_connection()**: Esta función abre la conexión con la base de datos Redshift con las credenciales registradas en el archivo .env
- **create_sql_objects**: Esta función se encarga de crear la tabla en caso no exista con los atributos predefinidos en base a los registros que va a almacenar.
- **etl_process**: Esta función se encarga de hacer todo el proceso de extración, transformación y carga a la base de datos. Existen algunos parámetros que se podrían cambiar como el schema, entre otros.
- **close_connection**: Por último, esta función se encarga de cerrar la conexión creada inicialmente.

## Variables .env
Se debe llenar en un archivo .env las credenciales o parámetros correctos para la conexión a Amazon Redshift y para el servicio SMTP de Airflow.

Variables Amazon Redshift
```
REDSHIFT_USER = 
REDSHIFT_PASSWORD = 
REDSHIFT_HOST = 
REDSHIFT_PORT = 
REDSHIFT_DB = 
```

Variables Airflow - SMTP
```
AIRFLOW__SMTP__SMTP_HOST= 
AIRFLOW__SMTP__SMTP_STARTTLS=
AIRFLOW__SMTP__SMTP_SSL=
AIRFLOW__SMTP__SMTP_USER=
AIRFLOW__SMTP__SMTP_PASSWORD=
AIRFLOW__SMTP__SMTP_PORT=
AIRFLOW_VAR_SUBJECT_MAIL= 
TO_EMAIL=
```
