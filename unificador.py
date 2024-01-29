import geopandas as gpd
import os
import pandas as pd

# Carpeta que contiene los archivos GeoJSON
carpeta_contenedora = './Locations/salida_geojson'

# Lista para almacenar los nombres de archivos a procesar
archivos_a_procesar = []

# Iterar sobre los archivos en la carpeta
for archivo in os.listdir(carpeta_contenedora):
    if archivo.endswith('.geojson'):  # Asegurarse de que solo procesamos archivos GeoJSON
        archivos_a_procesar.append(os.path.join(carpeta_contenedora, archivo))

# Lista para almacenar los GeoDataFrames individuales
gdfs = []

# Iterar sobre la lista de archivos
for archivo in archivos_a_procesar:
    gdf = gpd.read_file(archivo)
    gdfs.append(gdf)

# Concatenar todos los GeoDataFrames en uno solo
gdf_final = pd.concat(gdfs, ignore_index=True)

# Guardar el GeoDataFrame final como un solo archivo GeoJSON
archivo_salida = './Locations/ubicaciones_totales.geojson'
gdf_final.to_file(archivo_salida, driver='GeoJSON')

print(f"Conversión completada. GeoJSON final guardado como '{archivo_salida}'.")
