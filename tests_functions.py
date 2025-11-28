import sys

system_paths = [
    "/usr/lib",
    "/usr/share/qgis/python",
    "/home/luigi/.local/share/QGIS/QGIS3/profiles/default/python",
    "/home/luigi/.local/share/QGIS/QGIS3/profiles/default/python/plugins",
    "/usr/share/qgis/python/plugins",
    "/usr/lib/python312.zip",
    "/usr/lib/python3.12",
    "/usr/lib/python3.12/lib-dynload",
    "/usr/local/lib/python3.12/dist-packages",
    "/usr/lib/python3/dist-packages",
    "/home/luigi/.local/share/QGIS/QGIS3/profiles/default/python",
    "D:\\eclipse\\plugins\\org.python.pydev.core_7.0.3.201811082356\\pysrc",
]
for path in system_paths:
    sys.path.append(path)
from qgis.core import QgsApplication
from OSM_PT_routing import move_OSMstops_on_the_road
import os


QgsApplication.setPrefixPath("/usr/share/qgis/python", True)

qgs = QgsApplication([], False)

qgs.initQgis()


def test_move_OSMstops_on_the_road():
    temp_OSM_for_routing = "data_for_tests"
    nmRD_temp_folder = "data_for_tests"
    OSMallroad_gpkg = "data_for_tests/OSMallroad.gpkg"
    ls_to_check = "data_for_tests/OSM4routing_Bus815_trip1.gpkg"
    lines_df = "data_for_tests/lines_files_list.csv"
    move_OSMstops_on_the_road(
        temp_OSM_for_routing,
        nmRD_temp_folder,
        OSMallroad_gpkg,
        ls_to_check,
        lines_df,
    )
    pass


def test_look_for_floder():
    if os.path.exists("test/data_for_tests/OSMallroad.gpkg"):
        print("it does")
    else:
        print("it doen't")


if __name__ == "__main__":
    test_look_for_floder()

qgs.exitQgis()
