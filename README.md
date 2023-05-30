## Trabajo de fin de grado de Ingeniería informática del alumno Aitor Sánchez Garzón.
### UNIR (Universidad Internacional de La Rioja)

![GUI](https://user-images.githubusercontent.com/30757903/227030858-d44fcef9-64c1-4d58-a5ee-3c162281adc5.jpeg)


Durante la última década, la comunicación ha sufrido una metamorfosis total. El desarrollo de aplicaciones para dispositivos móviles, y el masivo uso de estos, ha devenido en una masificación de informaciones y opiniones publicadas en determinadas redes sociales. 
La gran diferencia entre los medios de comunicación social clásicos, y las actuales redes sociales, radica en que los mensajes publicados en estas últimas, llegan a miles o millones de personas, pudiendo causar potencialmente un daño considerable. Por un lado, la propagación del mensaje se magnifica exponencialmente, afectando directamente a la persona o grupo al que se dirige, y por otro cataliza la radicalización a través de lo que se ha venido a denominar “discurso de odio”.

La Constitución española garantiza el derecho a la libertad de expresión, pero si las opiniones y comentarios en estas redes sociales se consideran ofensivos o insultantes, podrían constituir un delito de incitación al odio. Dependiendo del contenido, estos comentarios también podrían ser considerados como apología del terrorismo. Es por ello por lo que las fuerzas y cuerpos de seguridad del estado necesitan detectar estos mensajes para determinar si representan un delito y, en caso afirmativo, actuar en consecuencia.

En mi TFG (Trabajo de Fin de Grado) he desarrollado una aplicación de escritorio para la extracción y salvado de datos de la red social Twitter en ficheros de tipo Excel. La aplicación permite su procesamiento y análisis a través de un modelo, generado previamente mediante técnicas de aprendizaje automático, para la clasificación de los mensajes extraídos en aquellos que potencialmente promuevan o están a favor del terrorismo islámico, y de los que no. 

La aplicación tiene las siguientes funcionalidades:

* Extracción eficiente de datos de Twitter: El proyecto implementa una solución que permite la captación eficiente y precisa de tweets basados en criterios específicos, como palabras clave, hashtags o usuarios. 

* Limpieza y preprocesamiento de datos: Un objetivo fundamental del proyecto es garantizar la calidad de los datos mediante la implementación de técnicas de procesamiento del lenguaje natural (NLP) para limpiar y preprocesar los tweets captado. Esto implica la eliminación de ruido, como caracteres especiales, enlaces, emojis y menciones, así como la tokenización y normalización del texto para facilitar el análisis posterior.

* Clasificación automatizada de tweets: La aplicación es capaz de clasificar automáticamente los tweets recolectados en función de un modelo previamente entrenado. Esto permite a los usuarios identificar rápidamente temas relevantes, detectar discursos favorecedores del terrorismo islámico, y analizar tendencias y patrones en las conversaciones de Twitter.

* Interfaz gráfica de usuario intuitiva y fácil de usar: El proyecto proporciona una interfaz gráfica de usuario (GUI) desarrollada con la librería Tkinter que facilita la interacción con la aplicación y permitea los usuarios realizar búsquedas, analizar y procesar los datos de manera sencilla e intuitiva.


A final de este texto introductorio encontraréis tres videos explicativos de como funciona la aplicación, una breve introducción a los ficheros que conforman la misma, así como una breve referencia a la creación del modelo generado para clasificar los tweets.


Al objeto de facilitar la posible ejecución de la aplicación en máquinas locales, he generado también una imagen Docker de la aquella. La misma se encuentra en el fichero aitor-tfg-unir.tar. 
También se puede encontrar en Docker Hub.

## Instrucciones para ejecutar la aplicación usando Docker

### Usando Docker Hub

1. **Descargar la imagen desde Docker Hub**. Para hacerlo, necesitarás abrir tu terminal y ejecutar el siguiente comando:

    ```bash
    docker pull aitorman/aitor-tfg-unir
    ```
    Esto descargará la imagen de Docker y la almacenará en tu máquina local.

2. **Ejecutar la imagen**. Una vez descargada la imagen, puedes ejecutarla en tu máquina con el siguiente comando:

    ```bash
    docker run -p 80:80 aitorman/aitor-tfg-unir
    ```
    Esto iniciará el contenedor en tu máquina y expondrá el puerto 80 del contenedor al puerto 80 de tu máquina local. 

### Usando un archivo `.tar`

1. **Cargar la imagen desde el archivo `.tar`**. En primer lugar, necesitarás obtener el archivo `.tar` que contiene la imagen de Docker. La misma se encuentra en la raiz del directorio del presente proyecto. Para cargar la imagen en tu sistema, ejecuta:

    ```bash
    docker load -i aitor-tfg-unir.tar
    ```
    
2. **Ejecutar la imagen**. Una vez cargada la imagen en tu sistema, puedes ejecutarla con el siguiente comando:

    ```bash
    docker run -p 80:80 aitor-tfg-unir
    ```
    Esto iniciará el contenedor y expondrá el puerto 80 del contenedor al puerto 80 de tu máquina local, permitiéndote interactuar con la aplicación.


Recuerda que para ejecutar tu aplicación necesitaras tener Docker instalado en tu sistema. 


-----------------------------------
### Video funcionamiento aplicación
-----------------------------------
[![Funcionamiento aplicación](https://img.youtube.com/vi/M7gv71N6dwg/0.jpg)](https://youtu.be/M7gv71N6dwg "Aplicación búsqueda y clasificación de tweets")

-----------------------------------
### Video con la estructura de directorios y distintos ficheros
-----------------------------------
[![Estructura de directorios y distintos ficheros](https://img.youtube.com/vi/yNNKi3r1JQo/0.jpg)](https://youtu.be/yNNKi3r1JQo "Aplicación búsqueda y clasificación de tweets")

-----------------------------------
### Video con explicación del modelo
-----------------------------------
[![Explicación del modelo](https://img.youtube.com/vi/YYCA7AtKmiQ/0.jpg)](https://youtu.be/YYCA7AtKmiQ "Aplicación búsqueda y clasificación de tweets")
