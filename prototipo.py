
import tkinter as tk
from tkinter import messagebox
import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime



########################   funciones   #################################

def search():

    # Creamos la query
    query = f'{palabraString.get()} since:{FechaInicioString.get()} until:{FechaFinString.get()}'
    ciudad = CiudadString.get()
    usuario = UsuarioString.get()
    maxTweets = int(LimiteInt.get()) if LimiteInt.get() else 100  # TENGO QUE CAMBIAR ESTO  

    # Preparar la búsqueda
    query += f' {"near:"+ciudad}' if ciudad else ''
    query += f' {"from:"+usuario}' if usuario else ''
        
    tweets = []
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if len(tweets) == maxTweets:
            break
        else:
            tweets.append([tweet.date, tweet.user.username, tweet.user.displayname, tweet.rawContent])
    
    # Mostrar los resultados de la búsqueda en la consola
    df = pd.DataFrame(tweets, columns=['Datetime', 'User', 'Username', 'Content'])
    print(df)

    # Actualizar la etiqueta de resultado
    resultadosString.set(f'Se encontraron {len(tweets)} tweets')

    # Devolver los tweets para guardarlos en un archivo Excel
    return tweets


def storesearch():
    # Guardar los tweets en un archivo Excel
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_tweets.xlsx"
    tweets = search()
    if tweets:
        df = pd.DataFrame(tweets, columns=['Datetime', 'User', 'Username', 'Content'])
        # para evitar el error timezone: Excel does not support datetimes with timezones. Please ensure that datetimes are timezone unaware before writing to Excel.
        df['Datetime'] = [celda.replace(tzinfo=None) for celda in df['Datetime']]
        # transfiero el dataframe a un archivo excel
        df.to_excel(filename, index=False)
        resultadosString2.set(f'Los resultados se guardaron en {filename}')
    else:
        resultadosString2.set('No se encontraron tweets para guardar')
    return


########################################################################

# Incio del widget

widget = tk.Tk()
widget.geometry('900x300')
widget.title(" TFG Aitor - Twitter")
# Busqueda por palabra
labelpalabra = tk.Label(widget,text="Palabra a buscar: ")
labelpalabra.grid(column=0, row=0, sticky=tk.W)
# Busqueda por fecha
labelFechaInicio = tk.Label(widget, text="Desde Fecha: (yyyy-mm-dd) ")
labelFechaInicio.grid(column=0, row=1, sticky=tk.W)
labelFechaFin = tk.Label(widget, text="Hasta fecha: (yyyy-mm-dd) ")
labelFechaFin.grid(column=0, row=2, sticky=tk.W)
# Busqueda por ciudad
labelCiudad = tk.Label(widget, text="En Ciudad: ")
labelCiudad.grid(column=0, row=3, sticky=tk.W)

labelUsuario = tk.Label(widget, text="De Usuario: ")
labelUsuario.grid(column=0, row=4, sticky=tk.W)
# Limite de tweets
labelLimite = tk.Label(widget, text="Número Máximo Tweets: \n (por defecto 100)")
labelLimite.grid(column=0, row=5, sticky=tk.W)

# Variables

palabraString = tk.StringVar()
FechaInicioString = tk.StringVar()
FechaFinString = tk.StringVar()
CiudadString = tk.StringVar()
UsuarioString = tk.StringVar()
LimiteInt = tk.StringVar()

# Entradas de texto
entrypalabra = tk.Entry(widget, width=30, textvariable=palabraString)
entryFechaInicio = tk.Entry(widget, width=30, textvariable=FechaInicioString)
entryFechaFin = tk.Entry(widget, width=30, textvariable=FechaFinString)
entryCiudad = tk.Entry(widget, width=30, textvariable=CiudadString)
entryUsuario = tk.Entry(widget, width=30, textvariable=UsuarioString)
entryLimite = tk.Entry(widget, width=30, textvariable=LimiteInt)

# Pack de entradas de texto
entrypalabra.grid(column=1, row=0, padx=10)
entryFechaInicio.grid(column=1, row=1, padx=10)
entryFechaFin.grid(column=1, row=2, padx=10)
entryCiudad.grid(column=1, row=3, padx=10)
entryUsuario.grid(column=1, row=4, padx=10)
entryLimite.grid(column=1, row=5, padx=10)

# Botones
buttonResultados = tk.Button(widget, text='Buscar Tweets', command=search)
buttonResultados.grid(column=1, row=6, pady=10, sticky=tk.W)
buttont2excel = tk.Button(widget, text='Guardar Resultados en Excel', command=storesearch)
buttont2excel.grid(column=1, row=7, pady=10, sticky=tk.W)
buttonQuit = tk.Button(widget, text="Salir", command=widget.quit)
buttonQuit.grid(column=1, row=8, pady=10, sticky=tk.W)

# Icono
icono = tk.PhotoImage(file="icono.png")
labellIcono = tk.Label(image=icono)
labellIcono.grid(column=2, row=0, rowspan=6, padx=10)

# Etiqueta de resultado
resultadosString = tk.StringVar()
labellResultados = tk.Label(widget, textvariable=resultadosString)
labellResultados.grid(column=2, row=6, padx=10, sticky=tk.W)
resultadosString2 = tk.StringVar()
labellResultados2 = tk.Label(widget, textvariable=resultadosString2)
labellResultados2.grid(column=2, row=7, padx=10, sticky=tk.W)

widget.mainloop()

