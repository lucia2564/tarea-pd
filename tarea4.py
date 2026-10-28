#Importamos librerías necesarias
from pyspark.sql import SparkSession, functions as F

from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DateType
)

# Inicializa la sesión de Spark
spark = SparkSession.builder.appName('Tarea-PD').getOrCreate()

# Definir el esquema de los datos
esquema_datos = StructType([
    StructField("DEPARTAMENTO", StringType(), True),
    StructField("MUNICIPIO", StringType(), True),
    StructField("CODIGO DANE", StringType(), True),
    StructField("ARMAS MEDIOS", StringType(), True),
    StructField("FECHA HECHO", DateType(), True),
    StructField("GENERO", StringType(), True),
    StructField("GRUPO ETARIO", StringType(), True),
    StructField("TIPO DE HURTO", StringType(), True),
    StructField("CANTIDAD", IntegerType(), True)
])

# Define la ruta del archivo .csv en HDFS
file_path = 'hdfs://localhost:9000/Tarea-PD/modalidades-hurto.csv'

# Lee el archivo .csv
df = spark.read.format('csv').option('header','true').option('delimiter', ',').option('dateFormat', 'dd/MM/yyyy').schema(esquema_datos).load(file_path)

#imprimimos el esquema
df.printSchema()

# Muestra las primeras filas del DataFrame
df.show()

# Estadísticas básicas

## Total de casos por Departamento
print("Total de casos por Departamento")
df.groupBy("DEPARTAMENTO").agg(F.sum("CANTIDAD").alias("TOTAL_CASOS")).orderBy(F.desc("TOTAL_CASOS")).show()

## Top 10 Municipios más afectados
print("Top 10 Municipios más afectados")
df.groupBy("DEPARTAMENTO", "MUNICIPIO").agg(F.sum("CANTIDAD").alias("TOTAL_CASOS")).orderBy(F.desc("TOTAL_CASOS")).show(10, truncate=False)

## Top 10 Medios y armas empleadas en la comisión del delito
print("Medios y armas empleadas en la comisión del delito")
df.groupBy("ARMAS MEDIOS").agg(F.sum("CANTIDAD").alias("TOTAL_CASOS")).orderBy(F.desc("TOTAL_CASOS")).show(10, truncate=False)

## Tabla cruzada entre Género y Grupo Etario
print("Tabla cruzada entre Género y Grupo Etario")
df.groupBy("GRUPO ETARIO").pivot("GENERO").agg(F.sum("CANTIDAD")).na.fill(0).show()
