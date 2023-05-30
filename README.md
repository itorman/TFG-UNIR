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


A final de este texto introductorio encontraréis tres videos explicativos de como funciona la aplicación, y una breve introducción a los ficheros que conforman la misma, así como una breve referencia a la creación del modelo generado para clasificar los tweets.


Al objeto de facilitar la posible ejecución de la aplicación en máquinas locales, he generado también una imagen Docker de la aquella. La misma se encuentra en Docker Hub (https://hub.docker.com/repositories/aitorman).

## Instrucciones para ejecutar la aplicación usando Docker

### En Mac

Primero necesitarás una aplicación que proporcione un servidor X11 para Mac, como XQuartz. Aquí te dejo los pasos generales:

1. Instala [XQuartz](https://www.xquartz.org/) en tu Mac.

2. Abre XQuartz y luego ve a las preferencias (`Command` + `,`). En la pestaña de seguridad, asegúrate de que esté marcada la opción "Allow connections from network clients".

3. Reinicia XQuartz para que los cambios surtan efecto.

4. Abre una terminal y ejecuta el siguiente comando para permitir que tu localhost se conecte al nuevo servidor X11:

   ```bash
   xhost + 127.0.0.1
   ```

Ahora puedes ejecutar tu contenedor Docker con las opciones -e y -v, pero también necesitarás agregar la opción --net=host para que tu contenedor pueda comunicarse con el servidor X11:


   ```bash
   docker run -it --net=host -e DISPLAY=host.docker.internal:0 aitorman/aitor-tfg-unir
   ```
    
### En Windows

1. Instala VcXsrv Windows X Server: Puedes descargar [VcXsrv Windows X Server](https://sourceforge.net/projects/vcxsrv/) y seguir las instrucciones de instalación.

2. Inicia XLaunch: Una vez instalado VcXsrv, puedes iniciar XLaunch desde tu menú de inicio. Te guiará a través de varias pantallas de configuración, puedes mantener los valores predeterminados y luego ejecutar el servidor X.

3. Configura la variable de entorno DISPLAY: Abre PowerShell o la terminal de tu elección y agrega la dirección IP de tu servidor X a la variable de entorno DISPLAY. Puedes hacerlo con el siguiente comando:


   ```bash
   setx DISPLAY [tu-ip]:0.0
   ```

    Recuerda reemplazar [tu-ip] con la dirección IP de tu servidor X en las instrucciones.

4. Ejecuta tu contenedor Docker: Ahora puedes ejecutar tu contenedor Docker con la opción `-e` para pasar la variable de entorno DISPLAY a tu contenedor:

    ```bash
    docker run -it -e DISPLAY=%DISPLAY% aitorman/aitor-tfg-unir
    ```


Ten en cuenta que para ejecutar tu aplicación necesitaras tener Docker instalado en tu sistema. 


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
