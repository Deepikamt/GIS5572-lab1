-- Create the point feature class
CREATE TABLE featureclass_point (
    id SERIAL PRIMARY KEY,
    geom GEOMETRY (Point, 4326)
);

-- Add coordinates to the point feature class
INSERT INTO featureclass_point (geom) VALUES
    (ST_SetSRID(ST_MakePoint(-93.2432978030554, 44.9720771737284), 4326)),
    (ST_SetSRID(ST_MakePoint(-93.2354298571532, 44.9734399517614), 4326));

-- Create the line feature class
CREATE TABLE featureclass_line (
    id SERIAL PRIMARY KEY,
    geom GEOMETRY (LineString, 4326)
);

-- Add coordinates to the line feature class
INSERT INTO featureclass_line (geom) VALUES
    (ST_SetSRID(ST_MakeLine(
        ST_MakePoint(-93.2432978030554, 44.9720771737284),
        ST_MakePoint(-93.2354298571532, 44.9734399517614)
    ), 4326));

   --To view featureclass_line 
select * from featureclass_line fl ;

-- Create the polygon feature class
CREATE TABLE featureclass_polygon (
    id SERIAL PRIMARY KEY,
    geom GEOMETRY (Polygon, 4326)
);


-- Add polygon to feature_class_polygon
INSERT INTO featureclass_polygon (geom)
VALUES
(
    ST_GeomFromText('POLYGON((-93.22456694058349 44.97656707355932,
                                -93.25750208433475 44.97369530667097,
                                -93.21775917100368 44.884844671870496,
                                -93.89021376922068 44.95341865769891,
                                -93.22456694058349 44.97656707355932))', 4326)
);


-- To View the Table
select * from featureclass_polygon fp;





SELECT id, ST_AsText(geom) AS point_geometry FROM featureclass_point;

SELECT id, ST_AsText(geom) AS line_geometry FROM featureclass_line;

SELECT id, ST_AsText(geom) AS line_geometry FROM featureclass_polygon;


--view each row in an attribute
SELECT * FROM featureclass_point;



---- summarize the content
-- Count the total number of features in the feature class
SELECT COUNT(*) AS total_features FROM featureclass_point;
SELECT COUNT(*) AS total_features FROM featureclass_line;
SELECT COUNT(*) AS total_features FROM featureclass_polygon;





-- Export the point feature class to Shapefile
SELECT id, ST_AsText(geom) AS geom
INTO "D:\4th sem_minnesota\ArcGIS_II\Lab1.2-postgress/point_shapefile.shp"
FROM featureclass_point;

-- Export the line feature class to Shapefile
SELECT id, ST_AsText(geom) AS geom
INTO "D:\4th sem_minnesota\ArcGIS_II\Lab1.2-postgress/line_shapefile.shp"
FROM featureclass_line;

-- Export the polygon feature class to Shapefile
SELECT id, ST_AsText(geom) AS geom
INTO "D:\4th sem_minnesota\ArcGIS_II\Lab1.2-postgress/polygon_shapefile.shp"
FROM featureclass_polygon;


CREATE TABLE Deepika_table (
    id SERIAL PRIMARY KEY,
    geom GEOMETRY (MultiPolygon, 4326)
);

select * from Deepika_table;


