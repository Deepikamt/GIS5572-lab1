# Import Libraries
import psycopg2
import arcpy
import json
import requests
import re #regular expression
import os
from arcgis.gis import GIS
import sys

# Set the value to the polygon geometry 
polygon = arcpy.Polygon(
    arcpy.Array([
        arcpy.Point(-93.22773898145596, 44.974068636239615),
        arcpy.Point(-93.18973295365898, 44.94326043904516),
        arcpy.Point(-93.17042775766252, 44.988360414486756), 
        arcpy.Point(-93.35274409842755, 45.09143303212043)
    ])
)

#convert the polygon to WKT
polygon_wkt = polygon.WKT

# Original MULTIPOLYGON WKT string
wkt_mp = "MULTIPOLYGON (((-93.22773898145596 44.974068636239615, -93.18973295365898 44.94326043904516, -93.17042775766252 44.988360414486756, -93.35274409842755 45.09143303212043)))"

# Convert MULTIPOLYGON to POLYGON (simple case)
wkt_p = wkt_mp.replace("MULTIPOLYGON (((","POLYGON ((").replace(")))", "))")

print("Converted WKT representation:")
print(wkt_p)

#connect to PostGIS database
conn = psycopg2.connect(
    host="35.224.213.125",
    database="gis5572",
    user="postgres",  
    password="",
    port="5432"
)

#cursor to execute SQL query
cur = conn.cursor()

#conn.rollback()

# Define your SQL query to insert the polygon into the database
sql = f"INSERT INTO Deepika_table (geom) VALUES (ST_GeomFromText('{polygon_wkt}', 4326))"

cur.execute(sql)

conn.commit()
cur.close()
conn.close

# Your API endpoint
api = 'http://35.221.47.162:5000/get_polygon'

try:
    response = requests.get(api)
    response.raise_for_status()
    dictionary = json.loads(response.text)
except requests.exceptions.RequestException as e:
    print(f"Error during API request: {e}")
    exit()
     

# Check if 'features' key exists
if 'features' in dictionary and len(dictionary['features']) > 0:
    # Extract geometry from the first feature
    geometry_str = dictionary['features'][0]['geometry']

    # Replace multiple occurrences using a regular expression
    geometry_str = re.sub(r'\[\[\[\[\[', '[[[', geometry_str)
    geometry_str = re.sub(r'\]\]\]\]\]', ']]]', geometry_str)

    try:
        # Parse the cleaned geometry string into a dictionary
        geometry_dict = json.loads(geometry_str)
        print(geometry_dict)
    except json.JSONDecodeError as e:
        print(f"Error decoding geometry string: {e}")
else:
    print("Error: 'features' key not found or empty in the API response.")

# Specify GeoJSON dictionary name and then create
Lab1geojson = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": geometry_dict['coordinates'],
        "type": "Polygon"
      }
    }
  ]
}

path = os.path.join(r'D:\4th sem_minnesota\ArcGIS_II\data_pipeline', 'Lab1geojson.json')

# Use 'with' statement for file handling to ensure proper closing
with open(path, 'w') as json_file:
    json.dump(Lab1geojson, json_file, indent=2)  # Indent for better readability
     


