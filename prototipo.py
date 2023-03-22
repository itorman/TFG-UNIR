import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import snscrape.modules.twitter as sntwitter
import pandas as pd
import pickle
from datetime import datetime
import regex as re
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

########################   FUNCIONES   #################################

def search():
    ''''
    Función que realiza la búsqueda de tweets en Twitter
    Los parámetros de búsqueda se obtienen de los widgets de la interfaz gráfica
    '''
    try:
        # borrar el contenido del label de resultados
        resultados_string.set('')
        print('Buscando tweets...')
        # Creamos la query
        query = f'{palabra_string.get()} since:{fecha_inicio_string.get()} until:{fecha_fin_string.get()}'
        ciudad = ciudad_string.get()
        usuario = usuario_string.get()
        idioma = idioma_string.get()
        max_tweets = int(limite_int.get()) if limite_int.get() else 100

        # Preparar la búsqueda con parámetros adicionales si hubiera
        query += f' {"near:"+ciudad}' if ciudad else ''
        query += f' {"from:"+usuario}' if usuario else ''
        query += f' {"lang:"+idioma.lower()}' if idioma else ''

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
    ''''
    Función que realiza la búsqueda de tweets en Twitter y los guarda en un archivo Excel
    Los parámetros de búsqueda se obtienen de los widgets de la interfaz gráfica
    '''
    try:
        # limpiar el label de resultados2
        resultados_string2.set('')
        tweets = search()
        if tweets:
            df = pd.DataFrame(tweets, columns=['Fecha', 'Usuario', 'Displayed name', 'Contenido', 'Ubicacion'])

            # para evitar el error timezone: Excel does not support datetimes with timezones. Please ensure that datetimes are timezone unaware before writing to Excel.
            df['Fecha'] = [celda.replace(tzinfo=None) for celda in df['Fecha']]

            # ruta guardado
            # y guardar los tweets en un archivo Excel
            filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_tweets.xlsx"
            ruta_carpeta = 'resultados/busquedas/'
            ruta_completa = ruta_carpeta + filename
            
            # transfiero el dataframe a un archivo excel
            df.to_excel(ruta_completa, index=False)
            resultados_string2.set(f'Los resultados se han guardado en:  {ruta_completa}')
        else:
            resultados_string2.set('No se han encontrado tweets. Revisa los parámetros de búsqueda.')
    except Exception as e:
        messagebox.showerror("Error", str(e))


############################# NEW FEATURE LIMPIAR TWEETS ########################################
def cleanData():
    ''''
    Función que realiza la búsqueda de tweets en Twitter, los pre-procesa, y los guarda en un archivo Excel
    Los parámetros de búsqueda se obtienen de los widgets de la interfaz gráfica
    '''
    try:
        # limpiar el label de resultados3
        resultados_string3.set('')
        # Proceso de limpia de los tweets   
        tweets = search()
        if tweets:
            # para evitar de error en la descarga de nltk -->nltk.download()
            df = pd.DataFrame(tweets, columns=['Fecha', 'Usuario', 'Displayed name', 'Contenido', 'Ubicacion'])
    
            # Limpiar los tweets
            # Eliminar los caracteres no occidentales
            df['Contenido'] = df['Contenido'].apply(lambda x: re.sub(r'http\S+', '', x))
            df['Contenido'] = df['Contenido'].apply(lambda x: re.sub(r'@(\w+)', '', x))
            df['Contenido'] = df['Contenido'].apply(lambda x: re.sub(r'#', '', x))
            df['Contenido'] = df['Contenido'].apply(lambda x: re.sub(r'[^\w\s]', '', x))
            df['Contenido'] = df['Contenido'].apply(lambda x: re.sub(r'\d+', '', x))
            df['Contenido'] = df['Contenido'].apply(lambda x: re.sub(r'[^\x00-\x7F]+', '', x))
            df['Contenido'] = df['Contenido'].apply(lambda x: re.sub(r'\s+', ' ', x))
    
            stop_words = set(stopwords.words('english'))
            lemmatizer = WordNetLemmatizer()

            # remove stopwords and lemmatize tokens using apply() method
            df['Contenido'] = df['Contenido'].apply(lambda x: x.lower())
            df['Contenido'] = df['Contenido'].apply(lambda x: word_tokenize(x))
            df['Contenido'] = df['Contenido'].apply(lambda x: [word for word in x if word not in stop_words])
            df['Contenido'] = df['Contenido'].apply(lambda x: [lemmatizer.lemmatize(word) for word in x])
            df['Contenido'] = df['Contenido'].apply(lambda x: ' '.join(x))

            # remove timezone information using tz_localize() method
            df['Fecha'] = pd.to_datetime(df['Fecha']).dt.tz_localize(None)
            ## Guardar los tweets limpios en un archivo Excel ##
            # ruta guardado
            # y guardar los tweets en un archivo Excel
            filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_tweets_limpios.xlsx"
            ruta_carpeta = 'resultados/limpios/'
            ruta_completa = ruta_carpeta + filename
            # transfiero el dataframe a un archivo excel
            df.to_excel(ruta_completa, index=False)
            resultados_string3.set(f'Los resultados se han guardado en:  {ruta_completa}')
        else:
            resultados_string3.set('No se han encontrado tweets. Revisa los parámetros de búsqueda.')
    except Exception as e:
        messagebox.showerror("Error", str(e))
    return      
############################# NEW FEATURE CLASIFICAR TWEETS ########################################

def classify():
    ''''
    Función que realiza la clasificación de los tweets elegidos de un archivo excel, y los clasifica en
    función de un modelo previamente entrenado. La salida será los tweets con contenido potencialmente relacionado
    con el terrorismo
    '''
    try:
        # Cargar el modelo y el vectorizador
        with open('./models/model4.pkl', 'rb') as model_file:
            model = pickle.load(model_file)
        with open('./models/vectorizer4.pkl', 'rb') as vectorizer_file:
            vectorizer = pickle.load(vectorizer_file)
        
        # Abre el cuadro de diálogo para seleccionar el archivo Excel
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            # Lee el archivo seleccionado
            tweets = pd.read_excel(file_path)
        
        # casting a string para evitar problemas con vectorizer    
        tweets_contenido = tweets['Contenido'].values.astype(str)
        # crear vectores numéricos a partir del texto de los tweets
        lista_vec = vectorizer.transform(tweets_contenido)

        # hacer predicciones de la clase de los tweets
        predicciones = model.predict(lista_vec)

        # identificar cuáles tweets son de la categoría "es_terrorismo"
        es_terrorismo = predicciones == 'N'

        # obtener los tweets clasificados como "terrorismo"
        #terrorismo_tweets = [t for i, t in enumerate(tweets) if es_terrorismo[i]]
        
        # convertir la lista de tweets en un DataFrame
        terrorismo_df = tweets[es_terrorismo]
        
        # si el df no esta vacio lo remarco en la etiqueta en el widget
        if terrorismo_df.empty:
            resultados_string4.set('No se han encontrado tweets con contenido terrorista')
        # Actualizar la etiqueta de resultado en el widget
        else:
            # guardar el DataFrame en un archivo Excel

            filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_tweets_terrorismo.xlsx"
            ruta_carpeta = 'resultados/terrorismo/'
            ruta_completa = ruta_carpeta + filename
            # transfiero el dataframe a un archivo excel
            terrorismo_df.to_excel(ruta_completa, index=False)
            resultados_string4.set(f'Tweets clasificados como terrorismo guardados en: {ruta_completa}')
        
    except Exception as e:
        messagebox.showerror("Error", str(e))

    return
    

############################ VENTANA ######################################################

# Incio del widget

widget = tk.Tk()
widget.geometry('1275x430')
widget.title(" TFG Aitor - Twitter")
# Busqueda por palabra
label_palabra = tk.Label(widget,text="Palabra o hastag a buscar: ").grid(column=0, row=0, sticky=tk.W)
# Busqueda por fecha
label_fecha_inicio = tk.Label(widget, text="Desde: (yyyy-mm-dd) ").grid(column=0, row=1, sticky=tk.W)
label_fecha_fin = tk.Label(widget, text="Hasta: (yyyy-mm-dd) ").grid(column=0, row=2, sticky=tk.W)
# Busqueda por ciudad
label_ciudad = tk.Label(widget, text="Twitteado desde (ciudad) : ").grid(column=0, row=3, sticky=tk.W)
# Busqueda por usuario
label_usuario = tk.Label(widget, text="Twitteado por (usuario) : ").grid(column=0, row=4, sticky=tk.W)
# Idioma de los tweets
label_idioma = tk.Label(widget, text="Idioma de tweet (ISO --> en, es..) : ").grid(column=0, row=5, sticky=tk.W)
# Limite de tweets
label_limite = tk.Label(widget, text="Número Máximo Tweets: \n (por defecto 100)").grid(column=0, row=6, sticky=tk.W)

# Variables
palabra_string = tk.StringVar()
fecha_inicio_string = tk.StringVar()
fecha_fin_string = tk.StringVar()
ciudad_string = tk.StringVar()
usuario_string = tk.StringVar()
idioma_string = tk.StringVar()
limite_int = tk.StringVar()

# Entradas de texto
entry_palabra = tk.Entry(widget, width=30, textvariable=palabra_string).grid(column=1, row=0, padx=10)
entry_fecha_inicio = tk.Entry(widget, width=30, textvariable=fecha_inicio_string).grid(column=1, row=1, padx=10)
entry_fecha_fin = tk.Entry(widget, width=30, textvariable=fecha_fin_string).grid(column=1, row=2, padx=10)
entry_ciudad = tk.Entry(widget, width=30, textvariable=ciudad_string).grid(column=1, row=3, padx=10)
entry_usuario = tk.Entry(widget, width=30, textvariable=usuario_string).grid(column=1, row=4, padx=10)
entry_idioma = tk.Entry(widget, width=30, textvariable=idioma_string).grid(column=1, row=5, padx=10)
entry_limite = tk.Entry(widget, width=30, textvariable=limite_int).grid(column=1, row=6, padx=10)

# Botones
button_resultados = tk.Button(widget, text='Buscar Tweets', command=search).grid(column=1, row=7, pady=10, sticky=tk.W)
button_t2excel = tk.Button(widget, text='Guardar Resultados en Excel', command=storesearch).grid(column=1, row=8, pady=10, sticky=tk.W)
button_limpiar = tk.Button(widget, text='Limpia los datos', command=cleanData).grid(column=1, row=9, pady=10, sticky=tk.W)
button_clasificar = tk.Button(widget, text='Clasificar Tweets', command=classify).grid(column=1, row=10, pady=10, sticky=tk.W)
button_quit = tk.Button(widget, text="Salir", command=widget.quit).grid(column=1, row=11, pady=10, sticky=tk.W)
# Icono
icono = tk.PhotoImage(file="./static/icono.png")
label_icono = tk.Label(image=icono).grid(column=0, row=6, rowspan=6, padx=8)

# Etiqueta de resultado
resultados_string = tk.StringVar()
resultados_string2 = tk.StringVar()
resultados_string3 = tk.StringVar()
resultados_string4 = tk.StringVar()

label_resultados = tk.Label(widget, textvariable=resultados_string).grid(column=2, row=7, padx=10)
label_resultados2 = tk.Label(widget, textvariable=resultados_string2).grid(column=2, row=8, padx=10)
label_resultados3 = tk.Label(widget, textvariable=resultados_string3).grid(column=2, row=9, padx=10)
label_resultados4 = tk.Label(widget, textvariable=resultados_string4).grid(column=2, row=10, padx=10)

widget.mainloop()