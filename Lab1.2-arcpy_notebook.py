#importing library
import arcpy

# Set working environment
working_dir = r"C:\Users\Deepika\OneDrive\Documents\ArcGIS\Projects\ArcGIS_II-Lab1.2(arcpy)\ArcGIS_II-Lab1.gdb"

# Define spatial reference 
spatial_reference = arcpy.SpatialReference(4326)

# name the feature class
point = "feature_point"
line = "feature_line"
polygon = "feature_polygon"

geometry_type_point = "POINT"
geometry_type_line = "POLYLINE"
geometry_type_polygon = "POLYGON"


# Define feature class names and geometry types
feature_classes = [("feature_point", "POINT"), ("feature_line", "POLYLINE"), ("feature_polygon", "POLYGON")]


# Create a new feature class for points
arcpy.CreateFeatureclass_management(working_dir, point , geometry_type_point)
arcpy.CreateFeatureclass_management(working_dir, line , geometry_type_line)
arcpy.CreateFeatureclass_management(working_dir, polygon , geometry_type_polygon)

# Define the workspace and feature class name
working_dir = r"C:\Users\Deepika\OneDrive\Documents\ArcGIS\Projects\ArcGIS_II-Lab1.2(arcpy)\ArcGIS_II-Lab1.gdb"
featureclass_point = "feature_point"

# Define spatial reference
spatial_reference = arcpy.SpatialReference(4326)  # WGS 1984

# Create the feature class
arcpy.CreateFeatureclass_management(working_dir, featureclass_point, "POINT", spatial_reference=spatial_reference)

# Create an insert cursor to add features to the point feature class
with arcpy.da.InsertCursor(f"{working_dir}\\{featureclass_point}", ["SHAPE@XY"]) as cursor:
    # Add points
    cursor.insertRow(((-93.2432978030554, 44.9720771737284),))
    cursor.insertRow(((-93.2354298571532, 44.9734399517614),))

# Define the workspace and feature class name for line
working_dir = r"C:\Users\Deepika\OneDrive\Documents\ArcGIS\Projects\ArcGIS_II-Lab1.2(arcpy)\ArcGIS_II-Lab1.gdb"
featureclass_line = "feature_line"

# Define spatial reference
spatial_reference = arcpy.SpatialReference(4326)  # WGS 1984

# Create the feature class for line
arcpy.CreateFeatureclass_management(working_dir, featureclass_line, "POLYLINE", spatial_reference=spatial_reference)

# Create an insert cursor to add features to the line feature class
with arcpy.da.InsertCursor(f"{working_dir}\\{featureclass_line}", ["SHAPE@"]) as cursor:
    # Add polyline feature
    array = arcpy.Array([arcpy.Point(-93.2432978030554, 44.9720771737284),
                         arcpy.Point(-93.2354298571532, 44.9734399517614)])
    polyline = arcpy.Polyline(array, spatial_reference)
    cursor.insertRow([polyline])

# Define the workspace and feature class name for polygon
working_dir = r"C:\Users\Deepika\OneDrive\Documents\ArcGIS\Projects\ArcGIS_II-Lab1.2(arcpy)\ArcGIS_II-Lab1.gdb"
featureclass_polygon = "feature_polygon"

# Define spatial reference
spatial_reference = arcpy.SpatialReference(4326)

# Create the feature class for polygon
arcpy.CreateFeatureclass_management(working_dir, featureclass_polygon, "POLYGON", spatial_reference=spatial_reference)

# Create an insert cursor to add features to the polygon feature class
with arcpy.da.InsertCursor(f"{working_dir}\\{featureclass_polygon}", ["SHAPE@"]) as cursor:
    # Add polygon feature
    array = arcpy.Array([arcpy.Point(-93.2432978030554, 44.9720771737284),
                         arcpy.Point(-93.25324747652463, 45.06680869398418),
                         arcpy.Point(-93.18556380476504, 44.985945669616754),
                         arcpy.Point(-93.2354298571532, 44.9734399517614)])
    polygon = arcpy.Polygon(array, spatial_reference)
    cursor.insertRow([polygon])

#To view each geometry
featureclass_point = "feature_point"

# Open a search cursor to iterate over features
with arcpy.da.SearchCursor(f"{working_dir}\\{featureclass_point}", ["SHAPE@XY"]) as cursor:
    for row in cursor:
        # Access the point coordinates
        x, y = row[0]

        # Print the coordinates in the desired format
        print(f"POINT ({x} {y})")


#view line
# Open a search cursor to iterate over features
with arcpy.da.SearchCursor(f"{working_dir}\\{featureclass_line}", ["SHAPE@"]) as cursor:
    for row in cursor:
        # Access the geometry object
        polyline = row[0]
        
        # Print or visualize the geometry (e.g., print its WKT representation)
        print(polyline.WKT)

#view polygon
featureclass_polygon = "feature_polygon"

# Open a search cursor to iterate over features
with arcpy.da.SearchCursor(f"{working_dir}\\{featureclass_polygon}", ["SHAPE@"]) as cursor:
    for row in cursor:
        # Access the geometry object
        polygon = row[0]
        
        # Print or visualize the geometry (e.g., print its WKT representation)
        print(polygon.WKT)

#Smmarize the content
# Function to print feature information
def print_feature_info(feature_class):
    print(f"Feature Class: {feature_class}")
    print("---------------------------------------------------------")
    fields = ["OID@", "SHAPE@"]
    with arcpy.da.SearchCursor(f"{working_dir}\\{feature_class}", fields) as cursor:
        for row in cursor:
            oid = row[0]
            shape = row[1]
            print(f"OID: {oid}")
            print(f"Geometry Type: {shape.type}")
            if shape.type == "Point":
                print(f"Coordinates: {shape.firstPoint.X}, {shape.firstPoint.Y}")
            elif shape.type == "Polyline":
                for part in shape:
                    for point in part:
                        print(f"Line: {point.X}, {point.Y}")
            elif shape.type == "Polygon":
                for part in shape:
                    for point in part:
                        print(f"Vertex: {point.X}, {point.Y}")
            print("---------------------------------------------------------")

# Print information for each feature class
print_feature_info(featureclass_point)
print_feature_info(featureclass_line)
print_feature_info(featureclass_polygon)

# Export each feature class as a shapefile
output_dir = r"D:\4th sem_minnesota\ArcGIS_II" 
arcpy.FeatureClassToShapefile_conversion([f"{working_dir}\\{featureclass_point}", f"{working_dir}\\{featureclass_line}", f"{working_dir}\\{featureclass_polygon}"], output_dir)


# Export each feature class to a geodatabase
output_gdb = r"C:\output_folder\output_geodatabase.gdb"  
arcpy.env.workspace = output_gdb
arcpy.Copy_management(f"{working_dir}\\{featureclass_point}", "feature_point")
arcpy.Copy_management(f"{working_dir}\\{featureclass_line}", "feature_line")
arcpy.Copy_management(f"{working_dir}\\{featureclass_polygon}", "feature_polygon")
