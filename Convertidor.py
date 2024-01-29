import geopandas as gpd
import json
from shapely.geometry import Point
import os

# Carpeta que contiene los archivos JSON
carpeta_contenedora = 'C:/Users/jaeg1/Documents/intento_python/Locations'

# Lista para almacenar los nombres de archivos a procesar
archivos_a_procesar = []

# Iterar sobre los archivos en la carpeta
for archivo in os.listdir(carpeta_contenedora):
    if archivo.endswith('.json'):  # Asegurarse de que solo procesamos archivos JSON
        archivos_a_procesar.append(os.path.join(carpeta_contenedora, archivo))

# Iterar sobre la lista de archivos
for archivo in archivos_a_procesar:
    # Cargar el archivo JSON con encoding utf-8
    with open(archivo, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Crear una lista para almacenar las geometrías (puntos)
    geometries = []

    # Iterar sobre los objetos en timelineObjects
    for obj in data.get('timelineObjects', []):
        place_visit = obj.get('placeVisit')
        if place_visit:
            location = place_visit.get('location')
            if location:
                latitude = location.get('latitudeE7')
                longitude = location.get('longitudeE7')

                # Verificar si latitude y longitude existen y no son None
                if latitude is not None and longitude is not None:
                    latitude = latitude / 1e7
                    longitude = longitude / 1e7
                    point = Point(longitude, latitude)
                    geometries.append(point)

    # Crear un GeoDataFrame
    gdf = gpd.GeoDataFrame(geometry=geometries)

    # Crear el directorio si no existe
    directorio_salida = os.path.join(carpeta_contenedora, 'salida_geojson')
    os.makedirs(directorio_salida, exist_ok=True)

    # Guardar el GeoJSON con un nombre basado en el archivo original
    nombre_salida = os.path.splitext(os.path.basename(archivo))[0] + '_salida.geojson'
    ruta_completa_salida = os.path.join(directorio_salida, nombre_salida)
    gdf.to_file(ruta_completa_salida, driver='GeoJSON')

    print(f"Conversión completada. GeoJSON guardado como '{ruta_completa_salida}'.")
