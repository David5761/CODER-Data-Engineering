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
