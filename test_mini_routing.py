from gtfs_shapes_creator.OSM_PT_routing import mini_routing

OSM4routing_csv = "F:\\Downloads\\gtfs_fp2026_20251206\\agen_738\\outputs\\OSM4routing_XYminiTrips.csv"

full_roads_gpgk = (
    "F:\\Downloads\\gtfs_fp2026_20251206\\agen_738\\OSM_data\\full_city_roads.gpkg"
)

tram_rails_gpgk = ""

OSM_Regtrain_gpkg = ""

OSM_funicular_gpkg = ""

temp_folder_minitrip = "F:\\Downloads\\gtfs_fp2026_20251206\\agen_738\\temp/mini-trips"

mini_routing(
    OSM4routing_csv,
    full_roads_gpgk,
    tram_rails_gpgk,
    OSM_Regtrain_gpkg,
    OSM_funicular_gpkg,
    temp_folder_minitrip,
)
