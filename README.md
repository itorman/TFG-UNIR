## Trabajo de fin de grado de Ingeniería informática del alumno Aitor Sánchez Garzón.
### UNIR (Universidad Internacional de La Rioja)

En la era digital, las redes sociales como Twitter han generado una gran cantidad de información, convirtiéndose en una fuente valiosa de datos y opiniones sobre diversos temas. El presente trabajo académico se centra en el diseño y desarrollo de un prototipo de aplicación que facilita la búsqueda, análisis y clasificación de tweets utilizando técnicas de procesamiento de lenguaje natural y aprendizaje automático, con un enfoque particular en la detección de contenido que favorece el discurso del terrorismo yihadista. Este trabajo abarca la revisión de la literatura relacionada con el análisis de tweets, procesamiento de lenguaje natural y aprendizaje automático, así como la selección e implementación de herramientas y librerías apropiadas para el desarrollo del prototipo. De igual manera, se incluye la evaluación del desempeño y la eficacia de la aplicación mediante pruebas experimentales y la identificación de posibles mejoras y extensiones futuras, entre las que se incluyen la posibilidad de adaptarse para identificar y clasificar cualquier otro tipo de contenido, siempre que se ajuste el modelo entrenado de manera adecuada.![image](https://github.com/itorman/TFG-UNIR/assets/30757903/e6f9e6a3-42ec-44aa-a026-d7a915e475e2)


![GUI](https://user-images.githubusercontent.com/30757903/227030858-d44fcef9-64c1-4d58-a5ee-3c162281adc5.jpeg)


Para ejecutar la aplicación se debe configurar el entorno de ejcución con Python 3.8, y con las dependencias especificadas en fichero 'requirements.txt'. 
Al final de este texto introductorio encontraréis tres videos explicativos de como funciona la aplicación, y una breve introducción a los ficheros que conforman la misma, así como una breve referencia a la creación del modelo generado para clasificar los tweets.


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
