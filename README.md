### Taller 2 - Ingenieria de Datos

Extraer 10.000 repositorios
Generar graficos a partir de ellos.

### 
Extractor Service:
Es es el servicio encargado de recopilar toda la información necesaria para llevar a cabo un analisis respecto a los repositorios.
LO que hace es realizar peticiones HTTP hacia la API de Github, extrayendo todos los repositorios publicos de distintos usuarios.
Luego lo guarda en un archivo.csv y los datos son manipulados en un Notebook.
En el Notebook se realiza la limpieza de datos y la extracción de datos en archivo JSON para que el Frontend pueda utilizarlo y mostrarlo al usuario.


###
Analyzer:
Interfaz Web que muestra los graficos, resultado de nuestro analisis.
Utiliza un Framework denominado observerhb.js
Para visualizar los resultados de este taller, visite el siguiente link:

[Interfaz Web](https://learn9.observablehq.cloud/t2-extract/)