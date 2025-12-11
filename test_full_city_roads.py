import pandas as pd
from gtfs_shapes_creator.OSM_PT_routing import vector_layer_to_csv, vector_layer_to_gpkg
import os
from qgis.core import QgsVectorLayer
from gtfs_shapes_creator.osmimport_routes_ptstops import (
    busroutes,
    full_city_roads,
)

agencies_folder = "F:\\Downloads\\gtfs_fp2026_20251206\\agen_881"

temp_folder = "OSM_data"
road_temp_folder = os.path.join(agencies_folder, temp_folder)

OSM_roads_name = "OSM_roads"
bus_lanes_name = "OSM_bus_lanes"
OSM_bus_lanes_gpkg = road_temp_folder + "/" + bus_lanes_name + ".gpkg"
OSM_bus_lanes_csv = road_temp_folder + "/" + bus_lanes_name + ".csv"

OSM_roads_nameCSV = "OSM_roads_CSV"
OSM_roads_csv = road_temp_folder + "/" + OSM_roads_name + ".csv"

full_roads_name = "full_city_roads"
full_roads_gpgk = road_temp_folder + "/" + full_roads_name + ".gpkg"

city_roads_name = "city roads"


OSM_roads_gpkg = road_temp_folder + "/" + OSM_roads_name + ".gpkg"
highway_speed_name = "highway_average_speed"
highway_speed_csv = road_temp_folder + "/" + highway_speed_name + ".csv"


OSM_ways_name = "OSM_ways"
OSM_ways_layer_name = "OSM_ways_lines"
OSM_ways_gpkg = str(road_temp_folder) + "/" + str(OSM_ways_name) + ".gpkg"

Roads_layer_file = str(OSM_ways_gpkg) + "|layername=" + OSM_ways_layer_name
Roads_layer = QgsVectorLayer(Roads_layer_file, "Roads", "ogr")
vector_layer_to_gpkg(Roads_layer, OSM_roads_name, OSM_roads_gpkg)

vector_layer_to_csv(Roads_layer, OSM_roads_csv)

busroutes(
    bus_lanes_name,
    OSM_bus_lanes_gpkg,
    OSM_bus_lanes_csv,
    OSM_roads_gpkg,
    highway_speed_csv,
)
full_city_roads(
    OSM_roads_gpkg,
    OSM_roads_csv,
    OSM_bus_lanes_gpkg,
    full_roads_gpgk,
    city_roads_name,
    highway_speed_csv,
    bus_lanes_name,
)
