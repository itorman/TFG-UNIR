
import tkinter as tk
from tkinter import messagebox
import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime
import os
from tqdm import tqdm
import nltk
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
nltk.download('93mwordnet')
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import regex as re

########################   funciones   #################################

def search():
    try:
        print('Buscando tweets...')
        # Creamos la query
        query = f'{palabra_string.get()} since:{fecha_inicio_string.get()} until:{fecha_fin_string.get()}'
        ciudad = ciudad_string.get()
        usuario = usuario_string.get()
        max_tweets = int(limite_int.get()) if limite_int.get() else 100

        # Preparar la búsqueda con parámetros adicionales si hubiera
        query += f' {"near:"+ciudad}' if ciudad else ''
        query += f' {"from:"+usuario}' if usuario else ''

        # Realizar la búsqueda
        tweets = []
        # Utilizo modulo tqdm para mostrar el progreso de la búsqueda
        # https://github.com/tqdm/tqdm#installation
        with tqdm(total=max_tweets) as pbar:
            for tweet in sntwitter.TwitterSearchScraper(query).get_items():
                if len(tweets) == max_tweets:
                    break
                else:
                    tweets.append([tweet.date, tweet.user.username, tweet.user.displayname, tweet.rawContent, tweet.place])
                    pbar.update(1)

        # Mostrar los resultados de la búsqueda en la consola
        df = pd.DataFrame(tweets, columns=['Fecha', 'Usuario', 'Displayed name', 'Contenido', 'Ubicacion'])
        # si el df no esta vacio imprimirlo en pantalla
        if not df.empty:
            print(df)
        else:
            print('No se han encontrado tweets. Revisa los parámetros de búsqueda.')

        # Actualizar la etiqueta de resultado en el widget
        resultados_string.set(f'Se han encontrado {len(tweets)} tweets')

        # Retorna la lista con los tweets encontrados
        return tweets
    except Exception as e:
        messagebox.showerror("Error", str(e))


def storesearch():
    try:
        # Guardar los tweets en un archivo Excel
        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_tweets.xlsx"
        tweets = search()
        if tweets:
            df = pd.DataFrame(tweets, columns=['Fecha', 'Usuario', 'Displayed name', 'Contenido', 'Ubicacion'])

            # para evitar el error timezone: Excel does not support datetimes with timezones. Please ensure that datetimes are timezone unaware before writing to Excel.
            df['Fecha'] = [celda.replace(tzinfo=None) for celda in df['Fecha']]
            # transfiero el dataframe a un archivo excel
            df.to_excel(filename, index=False)
            resultados_string2.set(f'Los resultados se han guardado en {filename}')
        else:
            resultados_string2.set('No se han encontrado tweets. Revisa los parámetros de búsqueda.')
    except Exception as e:
        messagebox.showerror("Error", str(e))


############################# NEW FEATURE LIMPIAR TWEETS ########################################
def cleanData():
    try:
        # Proceso de limpia de los tweets   
        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "__tweets_limpios.xlsx"
        tweets = search()
        if tweets:
            # para evitar de error en la descarga de nltk -->nltk.download()
            df = pd.DataFrame(tweets, columns=['Fecha', 'Usuario', 'Displayed name', 'Contenido', 'Ubicacion'])
            columna_contenido = df['Contenido']
            # Limpiar los tweets
            # Eliminar los caracteres no occidentales
            columna_contenido = [re.sub(r'[^\x00-\x7F]+', '', texto) for texto in columna_contenido]
            # Eliminar los signos de puntuación
            columna_contenido = [re.sub(r'[^\w\s]', '', texto) for texto in columna_contenido]
            # Eliminar los números
            columna_contenido = [re.sub(r'\d+', '', texto) for texto in columna_contenido]
            # Eliminar los espacios en blanco
            columna_contenido = [re.sub(r'\s+', ' ', texto) for texto in columna_contenido]
                
            # tokeniza el texto en la columna utilizando la función 'word_tokenize' de la librería nltk
            tokens = [word_tokenize(texto) for texto in columna_contenido]
            # mayusculas a minusculas
            tokens = [[palabra.lower() for palabra in texto] for texto in tokens]
            # elminna las stopwords (palabras que no aportan significado)
            stop_words = set(stopwords.words('english')) # Cambiar 'english' por el idioma que deseemos
            tokens = [[palabra for palabra in texto if not palabra in stop_words] for texto in tokens]
            # lemantizar los tokens (las convierte a su forma raiz)
            lemmatizer = WordNetLemmatizer()
            tokens = [[lemmatizer.lemmatize(palabra) for palabra in texto] for texto in tokens]
            # unir los tokens en una cadena de texto separados por espacios
            texto_limpio = [' '.join(texto) for texto in tokens]
            # eliminar referencias html
            texto_limpio = [re.sub(r'http\S+', '', texto) for texto in texto_limpio]
            # eliminar referencias a usuarios
            texto_limpio = [re.sub(r'@(\w+)', '', texto) for texto in texto_limpio]
            # eliminar el "#" de los hashtags
            texto_limpio = [re.sub(r'#', '', texto) for texto in texto_limpio]
           
            # añadir la columna con los tweets limpios al dataframe
            df['Contenido'] = texto_limpio

            ## Guardar los tweets limpios en un archivo Excel ##
            # para evitar el error timezone: Excel does not support datetimes with timezones. Please ensure that datetimes are timezone unaware before writing to Excel.
            df['Fecha'] = [celda.replace(tzinfo=None) for celda in df['Fecha']]
            # transfiero el dataframe a un archivo excel
            df.to_excel(filename, index=False)
            resultados_string3.set(f'Los resultados se han guardado en {filename}')
        else:
            resultados_string3.set('No se han encontrado tweets. Revisa los parámetros de búsqueda.')
    except Exception as e:
        messagebox.showerror("Error", str(e))
    return      



###############################################################################################

# Incio del widget

widget = tk.Tk()
widget.geometry('1000x370')
widget.title(" TFG Aitor - Twitter")
# Busqueda por palabra
label_palabra = tk.Label(widget,text="Palabra a buscar: ").grid(column=0, row=0, sticky=tk.W)
# Busqueda por fecha
label_fecha_inicio = tk.Label(widget, text="Desde Fecha: (yyyy-mm-dd) ").grid(column=0, row=1, sticky=tk.W)
label_fecha_fin = tk.Label(widget, text="Hasta fecha: (yyyy-mm-dd) ").grid(column=0, row=2, sticky=tk.W)
# Busqueda por ciudad
label_ciudad = tk.Label(widget, text="En Ciudad: ").grid(column=0, row=3, sticky=tk.W)
label_usuario = tk.Label(widget, text="De Usuario: ").grid(column=0, row=4, sticky=tk.W)
# Limite de tweets
label_limite = tk.Label(widget, text="Número Máximo Tweets: \n (por defecto 100)").grid(column=0, row=5, sticky=tk.W)

# Variables
palabra_string = tk.StringVar()
fecha_inicio_string = tk.StringVar()
fecha_fin_string = tk.StringVar()
ciudad_string = tk.StringVar()
usuario_string = tk.StringVar()
limite_int = tk.StringVar()

# Entradas de texto
entry_palabra = tk.Entry(widget, width=30, textvariable=palabra_string).grid(column=1, row=0, padx=10)
entry_fecha_inicio = tk.Entry(widget, width=30, textvariable=fecha_inicio_string).grid(column=1, row=1, padx=10)
entry_fecha_fin = tk.Entry(widget, width=30, textvariable=fecha_fin_string).grid(column=1, row=2, padx=10)
entry_ciudad = tk.Entry(widget, width=30, textvariable=ciudad_string).grid(column=1, row=3, padx=10)
entry_usuario = tk.Entry(widget, width=30, textvariable=usuario_string).grid(column=1, row=4, padx=10)
entry_limite = tk.Entry(widget, width=30, textvariable=limite_int).grid(column=1, row=5, padx=10)

# Botones
button_resultados = tk.Button(widget, text='Buscar Tweets', command=search).grid(column=1, row=6, pady=10, sticky=tk.W)
button_t2excel = tk.Button(widget, text='Guardar Resultados en Excel', command=storesearch).grid(column=1, row=7, pady=10, sticky=tk.W)
button_limpiar = tk.Button(widget, text='Limpia los datos', command=cleanData).grid(column=1, row=8, pady=10, sticky=tk.W)
button_quit = tk.Button(widget, text="Salir", command=widget.quit).grid(column=1, row=10, pady=10, sticky=tk.W)
# Icono
icono = tk.PhotoImage(file="icono.png")
label_icono = tk.Label(image=icono).grid(column=0, row=6, rowspan=6, padx=8)

# Etiqueta de resultado
resultados_string = tk.StringVar()
resultados_string2 = tk.StringVar()
resultados_string3 = tk.StringVar()

label_resultados = tk.Label(widget, textvariable=resultados_string).grid(column=2, row=6, padx=10)
label_resultados2 = tk.Label(widget, textvariable=resultados_string2).grid(column=2, row=7, padx=10)
label_resultados3 = tk.Label(widget, textvariable=resultados_string3).grid(column=2, row=8, padx=10)

widget.mainloop()