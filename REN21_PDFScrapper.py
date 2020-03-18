import numpy as np
import pandas as pd
import PyPDF2
from itertools import cycle
from itertools import chain
import sys
import os

def openfile(dir, filename, pagenumber):
    # Función openfile(). Se requiere de argumento la ubicación del directorio donde se encuentra el PDF, el nombre del archivo, y la página de la
    # cual se quiere realizar el scrapping
    os.chdir(dir)
    data = open(filename, 'rb')  # Se crea un objeto "data" que incluye la información en formato "rb" del documento pdf
    dataread = PyPDF2.PdfFileReader(data)  # Se aplica la clase PdfFileReader al objeto "data" para obtener una formato de trabajo adecuado
    page = dataread.getPage(pagenumber)  # Función getPage() que se aplica a "dataread" para obtener la página para el scrapper
    page_content = page.extractText()  # Función extractText() que se aplica a "page" para recuperar el texto en string
    page_content = list(filter(None, page_content))  # Se agrupan los strings en una lista después de filtrar los None
    page = page_content

    return page
def strip_page(obj):
    for i in range(len(obj)):
        obj[i] = obj[i].strip()  # Clase strip() nos permite quitar los espacios en blanco de los strings en la lista
        obj[i] = obj[i].split()  # Clase split() nos permite separar el contenido de la lista

    obj = list(chain.from_iterable(obj))  # Clase chain.from_iterable que nos permite eliminar el nesting que ocurre en lista

    return obj
def clean_empty(list):
    # Función clean_empty(). Esta función se dedica a eliminar secuencialmente elementos de una lista de acuerdo a su indexado.
    for i in range(len(list)):
        try:
            del list[list.index("")]
        except:
            pass

    return list
def transform_strings(list):
    # Función transform_strings(), que compara el type() del obj en lista, principalmente transformando str en int/float
    for obj in range(len(list)):
        if type(list[obj]) == str:
            try:
                list[obj] = int(list[obj])
            except:
                try:
                    list[obj] = float(list[obj])
                except:
                    pass
    return list
def split_floats(obj):
    # Función split_floats(), la cual verifica que nuestros objetos en lista presenten un formato adecuado
    # las comparaciones que se realizan dentro de la lista es exclusivo en str.
    # El loop se esta realizando fuera de la función split_floats

    # Primera comparativa in, el cual identifica el punto correspondiente a un obj float, además de recuperar el número
    # después al punto
    if "." in obj:
        try:
            obj = list(chain.from_iterable(obj))  # Función chain.from_iterable(), que separa los componentes individuales del objeto
            for i in range(len(obj)):
                if obj[i] == ".":
                    obj[i] = "".join((obj[i], obj[i + 1])) # Función de clase .join(), que permite unir elementos em un string
                    obj[i + 1] = ""  # Correción del elemento que se uso para la unión, se coloca un espacio vacio
        except:
            pass

    # El obj consecuente se limpia a partir de la función clean_empty, el cual elimina los elementos de la lista ""
    obj = clean_empty(list=obj)

    # Segunda comparativa in, el cual permite recuperar el número previo al punto
    for i in range(len(obj)):
        if "." in obj[i]:
            obj[i] = "".join((obj[i - 1], obj[i]))
            obj[i - 1] = ""

    # Se vuelve a limpiar el obj con clean_empty()
    obj = clean_empty(list=obj)

    # Pequeña comparativa para convertir los objetos en lista, si es posible, en float
    for i in range(len(obj)):
        try:
            obj[i] = float(obj[i])
        except:
            pass

    # A partir de la lista que se tiene en el objeto, se intenta indexar el elemento float en una segunda lista
    # y el residuo str se une con join() antes de indexarla en la segunda lista
    result = []
    for i in range(len(obj)):
        try:
            if type(obj[i]) != str:
                result.append(obj[i])
                obj[i] = ""
            elif type(obj[i]) == str and "".join(obj) not in result:
                result.append("".join(obj))
        except:
            pass

    return result
def set_values(df, list, nrows, ncols):
    # Función set_values(), la cual se usa para organizar los elementos de la lista en un dataframe
    # Se usan de argumentos las dimensiones de tabla de acuerdo al documento original del PDF

    df = pd.DataFrame()

    rows = []
    cols = []
    # Se realiza un for que anexa los flotantes y titulos en una lista "rows"
    # Mientras se anexa los int en una lista "cols"
    for i in range(len(list)):
        if type(list[i]) == str and type(list[i + 1]) == float:
            rows.append(list[i])
        elif type(list[i]) == int:
            cols.append(list[i])

    # De acuerdo a los argumentos de la función, se hace el conjunto de acuerdo al número de elementos
    # que se desean mantener
    rows = rows[0:nrows]
    cols = cols[0:ncols]



    # Tres loops for con el fin de anexar los elementos individuales de la lista de acuerdo a su fila [rows], columna [col] o observación [lista]
    for i in range(len(list)):
        for j in range(len(rows)):
            if list[i] == rows[j]:
                for k in range(len(cols)):
                    df.loc[rows[j], cols[k]] = list[i + k + 1]

    df["Sector"] = rows
    """
    for i in range(len(list)):
        for j in range(len(rows)):
            if list[i] == rows[j]:
                df.loc[rows[j], 0] = list[i + 1]
                df.loc[rows[j], 1] = list[i + 2]
                df.loc[rows[j], 2] = list[i + 3]
                df.loc[rows[j], 3] = list[i + 4]
                df.loc[rows[j], 4] = list[i + 5]
                df.loc[rows[j], 5] = list[i + 6]
                df.loc[rows[j], 6] = list[i + 7]
                df.loc[rows[j], 7] = list[i + 8]
                df.loc[rows[j], 8] = list[i + 9]
                df.loc[rows[j], 9] = list[i + 10]
                df.loc[rows[j], 10] = list[i + 11]
    df.columns = cols            
    """
    return df

### Fase 1: Creación de listas
getdir = os.getcwd()
pdf = openfile(dir=getdir, filename="REN21_2019.pdf", pagenumber=235)

### Fase 2: Procesamiento de la lista
# Se generan dos listas para incluir el los strings de pdf, separandolos por el espacio "/n"
value = []
page = []
for string in pdf:
    if string != "\n":
        page.append(string)
    elif string == "\n":
        value.append(list(page))
        page = []

# Se unen los caracteres individuales de los strings para generar un solo objeto a partir de la lista
for i in value:
    page.append("".join(i))

# Se transforman los str en int/float de acuerdo a sus caracteristicas
page = transform_strings(page)

# En el caso que se tengan strings que incluyan floats o floats unidos, se utiliza un loop que emplea la función
# split_floats() para poder separar individualmente los elementos. Solamente se emplea en observaciones tipo(str)
for i in range(len(page)):
    if type(page[i]) == str:
        page[i] = split_floats(page[i])

# En el caso que la función anterior regrese elementos en lista, se emplea un for que sea capaz de unnest/desanidar
# los elementos y anexarlos en una nueva lista
vector = []
for i in range(len(page)):
    if type(page[i]) != list:
        vector.append(page[i])
    elif type(page[i]) == list:  # Si se encuentra un objeto tipo lista en la lista,
       for j in page[i]:  # Se realiza un for para capturar los objetos individuales de la lista
           vector.append(j)  # Se anexa los elementos individuales

### Fase 3: Generación de los dataframes
# Se genera un df para usarlo como base para la función set_values()
stage = pd.DataFrame()
stage = set_values(stage, vector, nrows=16, ncols=11)
for i in stage["Sector"]:
    stage.loc[i, "Sector"] = i.replace(" ", "")
    if "Biomass" in i:
        stage.loc[i, "Sector"] = "Biomass"
    elif "Hydro" in i:
        stage.loc[i, "Sector"] = "Hydropower"

# Se genera un segundo dataframe para separar el df que resulta de la función anterior
technology = pd.DataFrame()

# Se separan a partir del argumento iloc[], utilizando un for que sean de las filas 9,16 y las filas 0,9
technology = stage.iloc[[f for f in range(9, 16)]]
stage = stage.iloc[[f for f in range(0, 9)]]

# Se anexa la última fila al df technology
technology = technology.append(stage.iloc[[8]])

### Fase 4: Se guardan los dataframes en formato csv

stage.to_csv("ren21_stage.csv", sep=",", encoding='utf-8', index=False)
technology.to_csv("ren21_technology.csv", sep=",", encoding='utf-8', index=False)

