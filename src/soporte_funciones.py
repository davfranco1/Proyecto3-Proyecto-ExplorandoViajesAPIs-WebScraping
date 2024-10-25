# Importamos liberías

from tqdm import tqdm  # Usar barras de progreso
import requests  # Trabajar con APIs
from time import sleep  # Funciones con time (pausas, espera)
import pandas as pd  # Trabajar con DataFrames para análisis de datos
import numpy as np # Trabajar con arrays y operaciones matemáticas avanzadas
from IPython.display import display  # Mostrar salidas de manera más clara en entornos interactivos (como Jupyter)
import time  # Funciones relacionadas con el tiempo
import datetime  # Obtener la fecha y hora actuales
import os  # Interactuar con el sistema operativo, como rutas y variables de entorno
import dotenv  # Manejo de archivos .env para cargar tokens y claves
dotenv.load_dotenv()  # Cargar variables de entorno desde un archivo .env

from selenium import webdriver  # Selenium es una herramienta para automatizar la interacción con navegadores web.
from webdriver_manager.chrome import ChromeDriverManager  # ChromeDriverManager gestiona la instalación del controlador de Chrome.
from selenium.webdriver.common.by import By # By permite localizar elementos web usando diferentes estrategias de búsqueda (ID, CSS_SELECTOR, XPATH, etc.)
from selenium.webdriver.common.keys import Keys  # Keys es útil para simular eventos de teclado en Selenium.
from selenium.webdriver.support.ui import Select  # Select se utiliza para interactuar con elementos <select> en páginas web.
from selenium.webdriver.support.ui import WebDriverWait  # Esperas explícitas para que ciertos elementos sean visibles o interactuables.
from selenium.webdriver.support import expected_conditions as EC  # Condiciones esperadas que ayudan a realizar esperas explícitas en Selenium.
from selenium.common.exceptions import NoSuchElementException  # Excepciones comunes de selenium, como cuando no se encuentra un elemento.
from bs4 import BeautifulSoup  # Herramienta para extraer y analizar datos de páginas HTML.
import re


#Este script automatiza la consulta de vuelos, hoteles y actividades utilizando varias APIs y web scraping.
#Las principales funcionalidades incluyen:
#- Consultar precios de vuelos en diferentes fechas.
#- Consultar disponibilidad de hoteles con diferentes rangos de precios.
#- Extraer actividades turísticas mediante web scraping de una página web.
#- Mostrar la información en DataFrames para fácil visualización.

# Consulta el archivo "Documentación de Soporte APIs y WebScraping" en esta misma carpeta para obtener más información.

# Importamos token para Rapidapi
key = os.getenv("rapidapi_key")


def calendario_precios_vuelos(origen_cal,destino_cal,fecha_inicio_cal):
    """
        Consulta un calendario de precios de vuelos para una ruta específica desde el origen al destino en una fecha dada.

        Args:
            origen_cal (str): Código de la ciudad de origen.
            destino_cal (str): Código de la ciudad de destino.
            fecha_inicio_cal (str): Fecha de inicio de la búsqueda de vuelos en formato 'YYYY-MM-DD'.

        Returns:
            pd.DataFrame: Un DataFrame con los detalles del calendario de precios de vuelos, incluyendo la fecha, el tipo de precio y el precio en EUR.
        """

    url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/getPriceCalendar"

    querystring = {"originSkyId":{origen_cal},
            "destinationSkyId":{destino_cal},
            "fromDate":{fecha_inicio_cal},
            "currency":"EUR"}

    headers = {
    "x-rapidapi-key": key,
    "x-rapidapi-host": "sky-scrapper.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    json_response = response.json()

    fecha_captura = datetime.datetime.now().strftime("%Y-%m-%d")
    datos_calendario = json_response["data"]["flights"]["days"]
    
    dicc_calendario_list = []
    for fecha in datos_calendario:
        fecha_dict = {
            "Fecha": fecha["day"],
            "Tipo de Precio": fecha["group"],
            "Precio": fecha["price"],
            "Fecha Captura": fecha_captura
            }
    dicc_calendario_list.append(fecha_dict)

    df_calendario = pd.DataFrame(dicc_calendario_list)
    df_calendario.replace(to_replace="high", value="Alto", inplace=True)
    df_calendario.replace(to_replace="medium", value="Medio", inplace=True)
    df_calendario.replace(to_replace="low", value="Bajo", inplace=True)
    df_calendario[["Fecha","Fecha Captura"]] = df_calendario[["Fecha","Fecha Captura"]].apply(pd.to_datetime)
    display(df_calendario)

    return df_calendario


def consulta_vuelos(fecha_ida, fecha_vuelta, aerop_destino, cod_destino):
    """
    Consulta información de vuelos disponibles para un viaje de ida y vuelta entre Madrid y un destino específico.

    Args:
        fecha_ida (str): Fecha de ida en formato 'YYYY-MM-DD'.
        fecha_vuelta (str): Fecha de vuelta en formato 'YYYY-MM-DD'.
        aerop_destino (str): Código IATA del aeropuerto de destino.
        cod_destino (int): Código del destino en el sistema.

    Returns:
        dict: Respuesta JSON con los datos de los vuelos.
    """

    url = "https://sky-scrapper.p.rapidapi.com/api/v2/flights/searchFlights"

    querystring = {"originSkyId":"MAD",
                   "destinationSkyId":{aerop_destino},
                   "originEntityId":"95565077",
                   "destinationEntityId":{cod_destino},
                   "date":{fecha_ida},
                   "returnDate":{fecha_vuelta},
                   "cabinClass":"economy",
                   "adults":"2",
                   "limit":50,
                   "sortBy":"best",
                   "currency":"EUR",
                   "countryCode":"ES"}

    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": "sky-scrapper.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


def mostrar_vuelos(datos_vuelos):  
    """
    Muestra una lista de vuelos basada en los datos proporcionados, estructurados en un DataFrame.

    Args:
        datos_vuelos (dict): Diccionario con los datos de los vuelos.

    Returns:
        pd.DataFrame: Un DataFrame con detalles de los vuelos, como la fecha y hora de salida/llegada, origen, destino, duración, escalas y precio.
    """
  
    dicc_vuelos_list = []
    fecha_captura = datetime.datetime.now().strftime("%Y-%m-%d")

    for vuelos in datos_vuelos['itineraries']:
        for trayecto in vuelos['legs']:
            dicc_vuelo = {
                "Salida": trayecto["departure"],
                "Llegada": trayecto["arrival"],
                "Origen": trayecto["origin"]["name"],
                "Destino": trayecto["destination"]["name"],
                "Duración": trayecto["durationInMinutes"],
                "Escalas": trayecto["stopCount"],
                "Aerolínea": trayecto["carriers"]["marketing"][0]["name"],
                "Precio": round(vuelos["price"]["raw"],2),
                "Fecha Captura": fecha_captura
            }
            dicc_vuelos_list.append(dicc_vuelo)


    df_vuelos = pd.DataFrame(dicc_vuelos_list)

    df_vuelos[["Fecha Salida","Hora Salida"]] = df_vuelos["Salida"].str.split("T", expand = True)
    df_vuelos[["Fecha Llegada","Hora Llegada"]] = df_vuelos["Llegada"].str.split("T", expand = True)
    df_vuelos.drop(columns=["Salida","Llegada"], inplace=True)
    df_vuelos = df_vuelos.reindex(columns=["Fecha Salida","Hora Salida","Fecha Llegada","Hora Llegada","Origen","Destino","Duración","Escalas","Aerolínea","Precio","Fecha Captura"])
    df_vuelos[["Fecha Salida","Fecha Llegada","Fecha Captura"]] = df_vuelos[["Fecha Salida","Fecha Llegada","Fecha Captura"]].apply(pd.to_datetime)
    df_vuelos["Hora Salida"] = pd.to_datetime(df_vuelos["Hora Salida"], format="%H:%M:%S").dt.time
    df_vuelos["Hora Llegada"] = pd.to_datetime(df_vuelos["Hora Llegada"], format="%H:%M:%S").dt.time

    return df_vuelos


def mostrar_destinos_vuelos():
    """
    Solicita al usuario que seleccione un destino de vuelo y muestra los vuelos disponibles para las fechas elegidas.

    Returns:
        pd.DataFrame: Un DataFrame con la información de los vuelos disponibles para el destino y fechas seleccionados.
    """

    print("Los destinos disponibles son:")
    print("1. Londres Gatwick")
    print("2. Munich")
    
    try:
        input_destino_vuelo = int(input("¿Dónde te gustaría viajar?"))
    except ValueError:
        print("Por favor, introduce un número válido.")
        return

    if input_destino_vuelo == 1:
        codigo_aeropuerto = 95565051
        aeropuerto = "LGW"
        input_ida = input("¿En qué fecha te gustaría volar? Por ejemplo: 2024-10-26 ")
        input_vuelta = input("¿Cuándo sería la vuelta? Por ejemplo: 2024-10-30 ")
        print(f"Te mostramos los vuelos disponibles para Londres Gatwick con salida el {input_ida} y regreso el {input_vuelta}.")
        json_response_vuelos = consulta_vuelos(input_ida, input_vuelta, aeropuerto, codigo_aeropuerto)
        datos_vuelos = json_response_vuelos["data"]
        df_vuelos = mostrar_vuelos(datos_vuelos)
        display(df_vuelos)
        return df_vuelos

    elif input_destino_vuelo == 2:
        codigo_aeropuerto = 95673491
        aeropuerto = "MUC"
        input_ida = input("¿En qué fecha te gustaría volar? Por ejemplo: 2024-10-26 ")
        input_vuelta = input("¿Cuándo sería la vuelta? Por ejemplo: 2024-10-30 ")
        print(f"Te mostramos los vuelos disponibles para Munich con salida el {input_ida} y regreso el {input_vuelta}.")
        json_response_vuelos = consulta_vuelos(input_ida, input_vuelta, aeropuerto, codigo_aeropuerto)
        datos_vuelos = json_response_vuelos["data"]
        mostrar_vuelos(datos_vuelos)
        df_vuelos = mostrar_vuelos(datos_vuelos)
        display(df_vuelos)
        return df_vuelos

    else:
        print("No has elegido una opción válida. Se cerrará la consulta.")


def consulta_fechas_hoteles(ubicacion, entrada, salida, precio_min, precio_max):
    """
    Consulta la disponibilidad de hoteles en una ubicación específica dentro de un rango de fechas y precios.

    Args:
        ubicacion (str): Código de la ubicación del hotel.
        entrada (str): Fecha de entrada en formato 'YYYY-MM-DD'.
        salida (str): Fecha de salida en formato 'YYYY-MM-DD'.
        precio_min (int): Precio mínimo en EUR.
        precio_max (int): Precio máximo en EUR.

    Returns:
        dict: Respuesta JSON con los datos de los hoteles disponibles.
    """

    url = "https://booking-com18.p.rapidapi.com/stays/search"

    querystring = {"locationId":{ubicacion},
                   "checkinDate":{entrada},
                   "checkoutDate":{salida},
                   "page":"2",
                   "sortBy":"popularity",
                   "rooms":"1",
                   "adults":"2",
                   "minPrice":{precio_min},
                   "maxPrice":{precio_max},
                   "units":"metric",
                   "temperature":"c",
                   "languageCode":"es",
                   "currencyCode":"EUR"}

    headers = {
        "x-rapidapi-key": key,
        "x-rapidapi-host": "booking-com18.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


def mostrar_hoteles(datos_hoteles):
    """
    Muestra una lista de hoteles disponibles basados en los datos proporcionados, estructurados en un DataFrame.

    Args:
        datos_hoteles (dict): Diccionario con los datos de los hoteles.

    Returns:
        pd.DataFrame: Un DataFrame con detalles de los hoteles, como el nombre, fecha de entrada/salida, puntuación, precio, y coordenadas.
    """

    dicc_hoteles_list = []
    fecha_captura = datetime.datetime.now().strftime("%Y-%m-%d")

    for hotel in datos_hoteles:
        dicc_hotel = {
            "Nombre": hotel["name"],
            "Entrada": hotel["checkinDate"],
            "Salida": hotel["checkoutDate"],
            "Puntuación": hotel["reviewScore"],
            "Precio": round(hotel["priceBreakdown"]["grossPrice"]["value"], 2),
            "Latitud": hotel["latitude"],
            "Longitud": hotel["longitude"],
            "Fecha Captura": fecha_captura
        }
        
        dicc_hoteles_list.append(dicc_hotel)
        
    df_hoteles = pd.DataFrame(dicc_hoteles_list)
    df_hoteles[["Entrada","Salida"]] = df_hoteles[["Entrada","Salida"]].apply(pd.to_datetime)

    return df_hoteles


def mostrar_destinos_hoteles():
    """
    Solicita al usuario que seleccione un destino de hotel y muestra los hoteles disponibles para las fechas y rangos de precios seleccionados.

    Returns:
        pd.DataFrame: Un DataFrame con la información de los hoteles disponibles para el destino y fechas seleccionados.
    """

    print("Los destinos disponibles son:")
    print("1. Londres")
    print("2. Munich")
    
    try:
        input_destino_hotel = int(input("¿Dónde te gustaría viajar?"))
    except ValueError:
        print("Por favor, introduce un número válido.")
        return

    if input_destino_hotel == 1:
        codigo_ubicacion = "eyJjaXR5X25hbWUiOiJMb25kcmVzIiwiY291bnRyeSI6IlJlaW5vIFVuaWRvIiwiZGVzdF9pZCI6Ii0yNjAxODg5IiwiZGVzdF90eXBlIjoiY2l0eSJ9"
        input_entrada = input("¿En qué fecha te gustaría reservar? Por ejemplo: 2024-10-26 ")
        input_salida = input("¿Cuándo sería la salida? Por ejemplo: 2024-10-30 ")
        input_pmin = int(input("Introduce el precio mínimo en EUR que te gustaría pagar en total "))
        input_pmax = int(input("Introduce el precio máximo en EUR que te gustaría pagar en total "))
        print(f"Te mostramos los hoteles disponibles en Londres con entrada el {input_entrada} y salida el {input_salida}, con precio total entre {input_pmin} y {input_pmax} euros.")
        json_response_vuelos = consulta_fechas_hoteles(codigo_ubicacion, input_entrada, input_salida, input_pmin, input_pmax)
        datos_hoteles = json_response_vuelos["data"]
        df_hoteles = mostrar_hoteles(datos_hoteles)
        display(df_hoteles)
        return df_hoteles

    elif input_destino_hotel == 2:
        codigo_ubicacion = "eyJjaXR5X25hbWUiOiJNw7puaWNoIiwiY291bnRyeSI6IkFsZW1hbmlhIiwiZGVzdF9pZCI6Ii0xODI5MTQ5IiwiZGVzdF90eXBlIjoiY2l0eSJ9"
        input_entrada = input("¿En qué fecha te gustaría reservar? Por ejemplo: 2024-10-26 ")
        input_salida = input("¿Cuándo sería la salida? Por ejemplo: 2024-10-30 ")
        input_pmin = int(input("Introduce el precio mínimo en EUR que te gustaría pagar en total "))
        input_pmax = int(input("Introduce el precio máximo en EUR que te gustaría pagar en total "))
        print(f"Te mostramos los hoteles disponibles en Munich con entrada el {input_entrada} y salida el {input_salida}, con precio total entre {input_pmin} y {input_pmax} euros.")
        json_response_vuelos = consulta_fechas_hoteles(codigo_ubicacion, input_entrada, input_salida, input_pmin, input_pmax)
        datos_hoteles = json_response_vuelos["data"]
        df_hoteles = mostrar_hoteles(datos_hoteles)
        display(df_hoteles)
        return df_hoteles

    else:
        print("No has elegido una opción válida. Se cerrará la consulta.")


def sopa_hellotix(ciudad):
    """
    Realiza un scraping en el sitio web de Hellotickets para obtener actividades disponibles en una ciudad específica.

    Args:
        ciudad (str): Nombre de la ciudad donde se busca realizar actividades.

    Returns:
        list: Lista de elementos HTML que contienen información de las actividades disponibles.
    """

    # Configurar el driver y abrir la URL
    driver = webdriver.Chrome()
    url = "https://www.hellotickets.es/"
    driver.get(url)

    # Esperar a que aparezca el banner de cookies y aceptar cookies
    sleep(3)
    try:
        driver.find_element("css selector", "#__layout > div > div.cookie-banner.cookie-banner-desktop.cookie-banner--v2 > div.cookie-banner__btns-container--v2 > button:nth-child(2)").click()
        print("Cookies aceptadas")    
    except Exception as e:
        print(f"Error al aceptar cookies: {e}")

    # Esperar a que el campo de búsqueda esté visible, luego buscar la ciudad y presionar ENTER
    sleep(2)
    try:
        driver.find_element("css selector", "#input-search").send_keys({ciudad})
        sleep(1)
        driver.find_element("css selector", "#input-search").send_keys(Keys.ENTER)
        print(f"Ciudad introducida")
    except Exception as e:
        print(f"Error al buscar la ciudad: {e}")

    sleep(5)
    # Scroll para cargar más contenido
    print("En página de resultados")
    hora_inicio = time.time()
    pausa_scroll = 2  # Pausa entre scrolls

    while time.time() - hora_inicio < 60:  # Scroll 60 segu
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(pausa_scroll)
        # Verificar si se ha llegado al final de la página
        if driver.execute_script("return window.innerHeight + window.scrollY >= document.body.scrollHeight"):
            print("Se ha llegado al final de la página.")
            break

    # Obtener el código fuente de la página y analizarlo con BeautifulSoup
    html = driver.page_source
    sopa = BeautifulSoup(html, 'html.parser')

    # Extraer actividades
    sopa_actividades = sopa.find_all('a', class_='product-grid__wrapper')

    # Imprimir confirmación
    print("Scraping finalizado")

    # Cerrar el navegador
    driver.quit()

    return sopa_actividades


def mostrar_actividades(sopa_actividades):
    """
    Procesa y muestra una lista de actividades basadas en los datos obtenidos del scraping, estructurados en un DataFrame.

    Args:
        sopa_actividades (list): Lista de elementos HTML con datos de las actividades obtenidas por scraping.

    Returns:
        pd.DataFrame: Un DataFrame con detalles de las actividades, como el nombre, precio, puntuación y enlace.
    """

    fecha_captura = datetime.datetime.now().strftime("%Y-%m-%d")

    # Inicializar la lista fuera del bucle para almacenar todas las actividades
    list_actividades = []

    # Extraer datos relevantes de cada actividad
    for actividad in sopa_actividades:
        
        # Extraer el nombre de la actividad
        nombre = actividad.find("span", class_="product-grid__title")
        if nombre:
            nombre = nombre.get_text(strip = True)
        else:
            nombre = np.nan
        
        # Extraer duración (no consigo extraer duración)
        #duracion = actividad.select_one("span", class_="#__layout > div > main > div > section > div.page-search__search-grid-desktop-redesign > ul > li:nth-child(3) > a > div.product-grid__info > div.product-grid__description > div > span:nth-child(1)")
        #if duracion:
        #    duracion = duracion.get_text(strip = True)
        #else:
        #    duracion = np.nan

        # Extraer el precio
        precio = actividad.find("div", class_="about-activity-grid-price__new-price")
        if precio:
            precio = precio.get_text(strip = True)
            # Usamos regex para extraer solo los números
            precio = re.findall(r'\d+', precio)
            precio = float(precio[0]) if precio else np.nan  # Convertir el precio a número si se encuentra
        else:
            precio = np.nan

        # Extraer valoración
        puntuacion = actividad.find("span", class_="rating-stars__rating")
        if puntuacion:
            puntuacion = puntuacion.get_text(strip = True)
        else:
            puntuacion = np.nan

        # Extraer enlace
        enlace = actividad.get("href", "")

        # Agregar los datos extraídos a la lista
        list_actividades.append({
            "Actividad": nombre,
            "Precio": precio * 2 if not np.isnan(precio) else np.nan,  # Multiplicar solo si el precio es un número
            #"Duración": duracion,
            "Puntuación": puntuacion,
            "Enlace": enlace,
            "Fecha captura": fecha_captura
        })

    # Crear el DataFrame a partir de la lista de diccionarios
    df_actividades = pd.DataFrame(list_actividades)

    return df_actividades


def mostrar_destinos_actividades():
    """
    Solicita al usuario que seleccione un destino de actividades y muestra las actividades disponibles en la ciudad seleccionada.

    Returns:
        pd.DataFrame: Un DataFrame con la información de las actividades disponibles en la ciudad seleccionada.
    """

    print("Los destinos disponibles son:")
    print("1. Londres")
    print("2. Munich")
    
    try:
        input_destino_hotel = int(input("¿Dónde te gustaría viajar?"))
    except ValueError:
        print("Por favor, introduce un número válido.")
        return

    if input_destino_hotel == 1:
        ciudad = "Londres"
        print(f"Te mostramos las actividades disponibles en {ciudad}")
        df_actividades = mostrar_actividades(sopa_hellotix(ciudad))
        display(df_actividades)
        return df_actividades

    elif input_destino_hotel == 2:
        ciudad = "Múnich"
        print(f"Te mostramos las actividades disponibles en {ciudad}")
        df_actividades = mostrar_actividades(sopa_hellotix(ciudad))
        display(df_actividades)
        return df_actividades
    
    else:
        print("No has elegido una opción válida. Se cerrará la consulta.")