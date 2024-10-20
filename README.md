# Proyecto 3: Explorando Viajes. APIs y WebScraping

![imagen](images/header.png)


## Planteamiento: **Diseñando las vacaciones perfectas con ayuda de la tecnología**

Este proyecto forma parte de un bootcamp de formación en Data Science e Inteligencia Artificial.

En nuestra agencia de viajes, nos centramos en aprovechar al máximo las tecnologías disponibles para proporcionar a nuestros clientes una experiencia de viaje excepcional. Nuestros servicios incluyen transporte, alojamiento y una variedad de excursiones y actividades emocionantes.

Para recopilar datos precisos y actualizados, empleamos una combinación de métodos. Aprovechamos APIs proporcionadas por proveedores de transporte, hoteles y empresas de actividades turísticas. Estas APIs nos permiten acceder a datos estructurados de manera eficiente. Sin embargo, somos conscientes de que algunas fuentes pueden no ofrecer APIs completas o accesibles.

Para superar esta limitación, recurrimos al Web Scraping, una técnica muy útil pero compleja. Utilizamos herramientas como Selenium y Beautiful Soup para extraer datos directamente de los sitios web de proveedores de transporte, hoteles y empresas de actividades turísticas. Esta estrategia nos permite obtener información detallada sobre horarios de transporte, disponibilidad de habitaciones, descripciones de actividades y otros detalles relevantes para nuestros clientes.


## Objetivo del Proyecto

- **Diseñar la escapada perfecta en pareja para salir de la rutina:** Utilizando las herramientas mencionadas en el planteamiento, realizaremos un EDA que trasladaremos a nuestros clientes, para que tomen la decisión que consideren más acertada para un viaje de fin de semana a Londres o Múnich.


## Estructura del repositorio

El proyecto está construido de la siguiente manera:

- **datos/**: Carpeta que contiene los archivos `.csv` y `.json` generados durante la captura y tratamiento de los datos.

- **images/**: Carpeta que contiene archivos de imagen tanto generados durante la ejecución del código como externos.

- **notebooks/**: Carpeta que contiene los archivos `.ipynb` utilizados en la captura y tratamiento de los datos. Están numerados para su ejecución secuencial.
  - `1_Captura y Limpieza`
  - `2_Análisis de Datos y Visualización_`

- **src/**: Carpeta que contiene los archivos `.py`, con las funciones utilizadas en los distintos notebooks.
  - `soporte_funciones.py`

- `.gitignore`: Archivo que contiene los archivos y extensiones que no se subirán a nuestro repositorio, como los archivos .env, con los tokens de las APIs.


## Lenguaje, librerías y temporalidad
- El proyecto fué elaborado con Python 3.9 y múltiples librerías de soporte. Consulta la parte superior de los notebooks y el `soporte_funciones.py` para conocer las instalaciones necesarias. 

- Este proyecto es funcional a fecha 20 de octubre de 2024, sin embargo, dependendiendo de terceros para la captura de datos (APIs y sitios web), los mismos podrían no estar disponibles o requerir de modificaciones para su tratamiento y captura en el futuro.


## Instalación

1. Crea una cuenta gratuita en [Rapidapi](https://rapidapi.com) y en [Mapbox](https://mapbox.com) (tendrás que registrar un método de pago). Consulta el paso 4.
2. Clona el repositorio
   ```sh
   git clone https://github.com/davfranco1/Proyecto3-Proyecto-ExplorandoViajesAPIs-WebScraping.git
   ```
3. Instala las librerías que aparecen en la parte superior de los notebooks y soporte_funciones.py.
   ```sh
   !pip install nombre_librería
   ```
4. Con las cuentas que has creado en el paso 1, obtén los tokens para las APIs. Dentro de la carpeta `src`, consulta el archivo `Documentación de Soporte` para más información sobre las APIs que vamos a utilizar, y sus enlaces. Crea dos archivos nuevos .env con tu token. En el caso de Rapiadpi, utilizaremos un mismo token para todas las APIs, pero deberás activarlas primero en su web.

Primero en las carpeta `notebooks` (.env):
   ```js
   token_mapbox = 'token_de_mapbox'
   ```

   Y luego en las carpeta `src` (.env):
   ```js
   rapidapi_key = 'token_de_rapidapi'
   ```

5. Cambia la URL del repositorio remoto para evitar cambios al original.
   ```sh
   git remote set-url origin usuario_github/nombre_repositorio
   git remote -v # Confirma los cambios
   ```


## Hallazgos, Conclusiones y Próximos Pasos
![imagen](images/munich_resultados.jpg)

- Te invitamos a descargar el [PDF Resultados](https://github.com/davfranco1/Proyecto3-Proyecto-ExplorandoViajesAPIs-WebScraping/blob/main/datos/Resultados.pdf), que resume de manera gráfica el EDA que hemos presentado a nuestros clientes.

- Además, el notebook `2_Análisis de Datos y Visualización`, contiene explicaciones de los datos y las visualizaciones generadas durante el proyecto.


## Autor

David Franco - [LinkedIn](https://linkedin.com/in/franco-david)

Enlace del proyecto: [https://github.com/davfranco1/Proyecto3-Proyecto-ExplorandoViajesAPIs-WebScraping](https://github.com/davfranco1/Proyecto3-Proyecto-ExplorandoViajesAPIs-WebScraping)
