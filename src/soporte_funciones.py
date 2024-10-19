# Importamos liberías

from tqdm import tqdm #Usar barras de progreso
import requests #Trabajar con APIs
from time import sleep #Funciones con time
import pandas as pd
from IPython.display import display
import datetime 
import os
import dotenv #Uso de tokens
dotenv.load_dotenv()


key = os.getenv("rapidapi_key")


def calendario_precios_vuelos(origen_cal,destino_cal,fecha_inicio_cal):

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
        "x-rapidapi-key": "e9d53ce8f2msh50c48f79aa0b1b1p1674b7jsn7a3fd4b9a409",
        "x-rapidapi-host": "booking-com18.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()


def mostrar_hoteles(datos_hoteles):
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
        print(f"Te mostramos los hoteles disponibles en Londres con entrada el {input_entrada} y salida el {input_salida}, con precio total entre {input_pmin} y {input_pmax}.")
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
        print(f"Te mostramos los hoteles disponibles en Munich con entrada el {input_entrada} y salida el {input_salida}, con precio total entre {input_pmin} y {input_pmax}.")
        json_response_vuelos = consulta_fechas_hoteles(codigo_ubicacion, input_entrada, input_salida, input_pmin, input_pmax)
        datos_hoteles = json_response_vuelos["data"]
        df_hoteles = mostrar_hoteles(datos_hoteles)
        display(df_hoteles)
        return df_hoteles

    else:
        print("No has elegido una opción válida. Se cerrará la consulta.")