# this is where I try to stock all the def of the main OSM_PT_routing.py funcitons

from qgis.core import (
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsVectorFileWriter,
    QgsField,
    QgsExpression,
    QgsExpressionContext,
    QgsExpressionContextUtils,
    edit,
    QgsFeatureRequest,
    QgsProcessingFeatureSourceDefinition,
    QgsCoordinateTransformContext,
    QgsWkbTypes,
)

import pandas as pd
from qgis import processing
from qgis.PyQt.QtCore import QVariant
import re
import os
import time


def if_remove(file_path, files_to_del):
    if os.path.exists(file_path):
        try:
            if file_path in files_to_del["path"]:
                files_to_del["path"].remove(file_path)
            os.remove(file_path)
        except Exception as e:
            files_to_del["path"].append(file_path)
            print(f"Error removing file {file_path}: {e}")
    return files_to_del


def if_remove_single_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def save_and_stop_editing_layers(layers):
    for layer in layers:
        if layer.isEditable():
            if layer.commitChanges():
                print(f"Changes saved successfully for layer: {layer.name()}")
            else:
                print(f"Failed to save changes for layer: {layer.name()}")
                if not layer.rollBack():
                    print(f"Failed to rollback changes for layer: {layer.name()}")
        else:
            print(f"Layer '{layer.name()}' is not in editing mode.")


# Debugging the changing in field type in some step before
def create_minitrips(OSM4rout_csv, OSM4routing_csv, lines_trips_csv):
    OSM4rout_unsorted = pd.read_csv(
        OSM4rout_csv, dtype={"trip": int, "pos": int, "stop_id": str}
    )

    # Debugging the changing in field type in some step before
    if OSM4rout_unsorted.dtypes.pos == "object":
        i_row = 0
        while i_row < len(OSM4rout_unsorted):
            if OSM4rout_unsorted.loc[i_row, "pos"] == "true":
                OSM4rout_unsorted.loc[i_row, "pos"] = 1
            if OSM4rout_unsorted.loc[i_row, "pos"] == "false":
                OSM4rout_unsorted.loc[i_row, "pos"] = 0
            i_row += 1

    OSM4rout_unsorted = OSM4rout_unsorted.astype({"pos": "int64", "trip": "int64"})
    OSM4rout = OSM4rout_unsorted.sort_values(["line_name", "trip", "pos"]).reset_index(
        drop=True
    )

    # creation and adding segments
    i_row = 0
    i_row2 = 1
    while i_row2 < len(OSM4rout):
        if OSM4rout.loc[i_row, "pos"] < OSM4rout.loc[i_row2, "pos"]:
            OSM4rout.loc[i_row, "line_trip"] = (
                str(OSM4rout.loc[i_row, "line_name"])
                + "_trip"
                + str(OSM4rout.loc[i_row, "trip"])
            )
            OSM4rout.loc[i_row, "mini_trip"] = (
                str(OSM4rout.loc[i_row, "GTFS_stop_id"])
                + " "
                + str((OSM4rout.loc[i_row2, "GTFS_stop_id"]))
            )
            OSM4rout.loc[i_row, "mini_tr_pos"] = (
                str(OSM4rout.loc[i_row, "line_name"])
                + "_trip"
                + str(OSM4rout.loc[i_row, "trip"])
                + "_pos"
                + str((OSM4rout.loc[i_row, "pos"]))
                + "-pos"
                + str((OSM4rout.loc[i_row2, "pos"]))
            )
            OSM4rout.loc[i_row, "next_lon"] = OSM4rout.loc[i_row2, "lon"]
            OSM4rout.loc[i_row, "next_lat"] = OSM4rout.loc[i_row2, "lat"]
        i_row += 1
        i_row2 += 1

    OSM4routing = OSM4rout[~OSM4rout["next_lon"].isna()]

    # creating dataframe for the lines for the specifc trips
    ls_lines_trips = OSM4routing.line_trip.unique()
    lines_trips = pd.DataFrame(ls_lines_trips)
    lines_trips = lines_trips.rename(columns={0: "line_trip"})
    pattern = re.compile(r"(?:Bus|RegRailServ|Tram|Funicular|trnsprt)([A-Za-z0-9+]+)_")
    pattern2 = re.compile(r"^(Bus|RegRailServ|Tram|Funicular|transport)(.*)_[^_]+$")
    trip_number_pattern = re.compile(r"_trip(\d+)$")

    for idx in lines_trips.index:
        lines_trips.loc[idx, "route_short_name"] = pattern.search(
            str(lines_trips.loc[idx, "line_trip"])
        ).group(1)

        transport_type = pattern2.match(str(lines_trips.loc[idx, "line_trip"])).group(1)
        bus_code = pattern2.match(str(lines_trips.loc[idx, "line_trip"])).group(2)
        lines_trips.loc[idx, "line_name"] = str(transport_type + bus_code)

        lines_trips.loc[idx, "trip"] = trip_number_pattern.search(
            str(lines_trips.loc[idx, "line_trip"])
        ).group(1)

    if_remove_single_file(OSM4routing_csv)
    OSM4routing.to_csv(OSM4routing_csv, index=False)
    if_remove_single_file(lines_trips_csv)
    lines_trips.to_csv(lines_trips_csv, index=False)


def mini_routing(
    OSM4routing_csv,
    full_roads_gpgk,
    tram_rails_gpgk,
    OSM_Regtrain_gpkg,
    OSM_funicular_gpkg,
    tempfld,
    trnsprt_shapes,
):
    mini_trips_unsorted = pd.read_csv(OSM4routing_csv)
    mini_trips_to_select = mini_trips_unsorted.sort_values(
        ["line_name", "trip", "pos"]
    ).reset_index(drop=True)

    ls_files_tempfld = os.listdir(tempfld)
    ls_mini_tr_gpkg = [file for file in ls_files_tempfld if "gpkg" in file]
    ls_mini_trips_done = [file[:-5] for file in ls_mini_tr_gpkg]

    mini_trips = mini_trips_to_select[
        ~mini_trips_to_select.mini_tr_pos.isin(ls_mini_trips_done)
    ]

    unique_mini_tr_name = "uq_mini_trips"
    unique_mini_tr_csv = os.path.join(tempfld, str(unique_mini_tr_name) + ".csv")

    # ls_minitrips = [str(tempfld)+'/'+str(file) for file in ls_mini_tr_gpkg]

    if not mini_trips.empty:
        mini_trips = mini_trips.reset_index(drop=True)
        print("There are " + str(len(mini_trips)) + " mini-trips to calculate")
        tot = len(mini_trips)
        total = tot
        i_row = 0
        n_minitr = 1
        tm0 = time.time()
        if os.path.exists(unique_mini_tr_csv):
            unique_mini_tr = pd.read_csv(unique_mini_tr_csv)
        else:
            unique_mini_tr = pd.DataFrame()
        while i_row < len(mini_trips):
            start_point = (
                str(mini_trips.loc[i_row, "lon"])
                + ","
                + str(mini_trips.loc[i_row, "lat"])
                + " [EPSG:4326]"
            )
            end_point = (
                str(mini_trips.loc[i_row, "next_lon"])
                + ","
                + str(mini_trips.loc[i_row, "next_lat"])
                + " [EPSG:4326]"
            )
            if start_point == end_point:
                i_row += 1
                continue
            mini_trip_gpkg = (
                str(tempfld) + "/" + str(mini_trips.loc[i_row, "mini_tr_pos"]) + ".gpkg"
            )
            if mini_trips.loc[i_row, "mini_tr_pos"]:
                i_row_uq_tr = 0
                IDstr_end_pt = str(start_point) + " " + str(end_point)
                # check for same mini trip
                while i_row_uq_tr < len(unique_mini_tr):
                    if unique_mini_tr.loc[i_row_uq_tr, "IDstr_end_pt"] == IDstr_end_pt:
                        print(
                            "copying "
                            + str(mini_trips.loc[i_row, "mini_tr_pos"])
                            + " from another mini trip"
                        )
                        if n_minitr != 1:
                            n_minitr = n_minitr - 1
                        total = total - 1
                        src = unique_mini_tr.loc[i_row_uq_tr, "mini_tr_path"]
                        if os.name == "nt":  # Windows
                            cmd = f'copy "{src}" "{mini_trip_gpkg}"'
                        else:  # Unix/Linux
                            cmd = f'cp "{src}" "{mini_trip_gpkg}"'
                        os.system(cmd)
                        break
                    i_row_uq_tr += 1
                # in absence of the same mini trip
                if i_row_uq_tr == len(unique_mini_tr):
                    print("creating " + str(mini_trips.loc[i_row, "mini_tr_pos"]))
                    unique_mini_tr.loc[i_row_uq_tr, "mini_tr_path"] = mini_trip_gpkg
                    unique_mini_tr.loc[i_row_uq_tr, "IDstr_end_pt"] = IDstr_end_pt
                    try:
                        if "Tram" in str(mini_trips.loc[i_row, "line_name"]):
                            if_remove_single_file(mini_trip_gpkg)
                            params = {
                                "INPUT": tram_rails_gpgk,
                                "STRATEGY": 0,
                                "DIRECTION_FIELD": "",
                                "VALUE_FORWARD": "",
                                "VALUE_BACKWARD": "",
                                "VALUE_BOTH": "",
                                "DEFAULT_DIRECTION": 2,
                                "SPEED_FIELD": "",
                                "DEFAULT_SPEED": 50,
                                "TOLERANCE": 0,
                                "START_POINT": start_point,
                                "END_POINT": end_point,
                                "OUTPUT": mini_trip_gpkg,
                            }
                            processing.run("native:shortestpathpointtopoint", params)
                        elif "RegRailServ" in str(mini_trips.loc[i_row, "line_name"]):
                            if_remove_single_file(mini_trip_gpkg)
                            params = {
                                "INPUT": OSM_Regtrain_gpkg,
                                "STRATEGY": 0,
                                "DIRECTION_FIELD": "",
                                "VALUE_FORWARD": "",
                                "VALUE_BACKWARD": "",
                                "VALUE_BOTH": "",
                                "DEFAULT_DIRECTION": 2,
                                "SPEED_FIELD": "",
                                "DEFAULT_SPEED": 50,
                                "TOLERANCE": 0,
                                "START_POINT": start_point,
                                "END_POINT": end_point,
                                "OUTPUT": mini_trip_gpkg,
                            }
                            processing.run("native:shortestpathpointtopoint", params)
                        elif "Funicular" in str(mini_trips.loc[i_row, "line_name"]):
                            if_remove_single_file(mini_trip_gpkg)
                            params = {
                                "INPUT": OSM_funicular_gpkg,
                                "STRATEGY": 0,
                                "DIRECTION_FIELD": "",
                                "VALUE_FORWARD": "",
                                "VALUE_BACKWARD": "",
                                "VALUE_BOTH": "",
                                "DEFAULT_DIRECTION": 2,
                                "SPEED_FIELD": "",
                                "DEFAULT_SPEED": 50,
                                "TOLERANCE": 0,
                                "START_POINT": start_point,
                                "END_POINT": end_point,
                                "OUTPUT": mini_trip_gpkg,
                            }
                            processing.run("native:shortestpathpointtopoint", params)
                        else:
                            if_remove_single_file(mini_trip_gpkg)
                            params = {
                                "INPUT": full_roads_gpgk,
                                "STRATEGY": 1,
                                "DIRECTION_FIELD": "oneway_routing",
                                "VALUE_FORWARD": "forward",
                                "VALUE_BACKWARD": "backward",
                                "VALUE_BOTH": "",
                                "DEFAULT_DIRECTION": 2,
                                "SPEED_FIELD": "maxspeed_routing",
                                "DEFAULT_SPEED": 50,
                                "TOLERANCE": 0,
                                "START_POINT": start_point,
                                "END_POINT": end_point,
                                "OUTPUT": mini_trip_gpkg,
                            }
                            processing.run("native:shortestpathpointtopoint", params)
                    except Exception:
                        os.remove(mini_trip_gpkg)
                        print(
                            "something wrong with "
                            + str(mini_trips.loc[i_row, "mini_tr_pos"])
                        )
                        break
                # ls_minitrips.append(mini_trip_gpkg)
            print("There are " + str(tot) + " mini-trips to calculate")
            tm1 = time.time()
            dtm = tm1 - tm0
            tmtot = dtm / n_minitr * (total)
            tmrest = tmtot - dtm
            hours = int(tmrest / 3600)
            min = int(int(tmrest / 60) - int(tmrest / 3600) * 60)
            if hours > 0:
                print("    " + str(hours) + " hours and " + str(min) + " minutes left")
            else:
                print("    " + str(min) + " minutes left")
            tot = tot - 1
            i_row += 1
            n_minitr += 1
        if_remove_single_file(unique_mini_tr_csv)
        unique_mini_tr.to_csv(unique_mini_tr_csv, index=False)

    # if_remove(trnsprt_shapes)
    # params = {'LAYERS':ls_minitrips,
    #           'CRS':QgsCoordinateReferenceSystem('EPSG:4326'),
    #           'OUTPUT':trnsprt_shapes}
    # processing.run("native:mergevectorlayers",params)

    # return trnsprt_shapes


def trips(mini_shapes_file, trip, trip_gpkg, trip_csv, temp_folder_minitrip):

    ls_files_tempfld = os.listdir(temp_folder_minitrip)
    ls_mini_tr_gpkg = [file for file in ls_files_tempfld if "gpkg" in file]
    ls_mini_tr = [file for file in ls_mini_tr_gpkg if trip in file]

    mini_tr_df_unsorted = pd.DataFrame(ls_mini_tr)

    pattern2 = r"(\d+)\.gpkg$"
    i_row = 0
    while i_row < len(mini_tr_df_unsorted):
        nd2pos = re.search(pattern2, mini_tr_df_unsorted.loc[i_row, 0]).group(1)
        mini_tr_df_unsorted.loc[i_row, "nd2pos"] = int(nd2pos)
        i_row += 1

    mini_tr_df = mini_tr_df_unsorted.sort_values(["nd2pos"]).reset_index(drop=True)
    mini_tr_df = mini_tr_df.rename(columns={0: "gpkg"})

    ls_minitrips_gpkg = mini_tr_df.gpkg.unique()

    ls_minitrips = [
        str(temp_folder_minitrip) + "/" + str(file) for file in ls_minitrips_gpkg
    ]

    if_remove_single_file(trip_gpkg)
    params = {
        "LAYERS": ls_minitrips,
        "CRS": QgsCoordinateReferenceSystem("EPSG:4326"),
        "OUTPUT": trip_gpkg,
    }
    processing.run("native:mergevectorlayers", params)

    # to_search = str(trip)+'%'
    # trip_selection =  '"layer" LIKE \''+ str(to_search)+'\''
    # if_remove(trip_gpkg)
    # params = {'INPUT':mini_shapes_file,
    #         'EXPRESSION':trip_selection,
    #         'OUTPUT':trip_gpkg}
    # processing.run("native:extractbyexpression", params)

    trip_layer = QgsVectorLayer(trip_gpkg, trip, "ogr")

    # ,QgsField("nd2pos", QVariant.Int)
    pr = trip_layer.dataProvider()
    pr.addAttributes([QgsField("dist_stops", QVariant.Double)])
    trip_layer.updateFields()

    expression1 = QgsExpression("$length")
    # expression2 = QgsExpression('regexp_substr( "layer" ,\'(\\d+)$\')')

    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(trip_layer))

    with edit(trip_layer):
        for f in trip_layer.getFeatures():
            context.setFeature(f)
            f["dist_stops"] = expression1.evaluate(context)
            # f['nd2pos'] = expression2.evaluate(context)
            trip_layer.updateFeature(f)
    trip_layer.commitChanges()

    lsto_keep = ["layer", "dist_stops", "start", "end"]

    IDto_delete = [trip_layer.fields().indexOf(field_name) for field_name in lsto_keep]
    IDto_delete = [index for index in IDto_delete if index != -1]

    if_remove_single_file(trip_csv)
    QgsVectorFileWriter.writeAsVectorFormat(
        trip_layer, trip_csv, "utf-8", driverName="CSV", attributes=IDto_delete
    )

    trip_df = pd.read_csv(trip_csv, dtype={"dist_stops": "float"})

    i_row2 = -1
    i_row = 0
    while i_row < len(trip_df):
        line_trip_1st_2nd = str(trip_df.loc[i_row, "layer"])
        pattern1 = r"^(.*)_"
        pattern2 = r"(\d+)$"
        line_trip = re.match(pattern1, line_trip_1st_2nd).group(1)
        nd2pos = re.search(pattern2, line_trip_1st_2nd).group(1)
        trip_df.loc[i_row, "seq_stpID"] = str(line_trip) + "_pos" + str(nd2pos)
        if i_row2 > -1:
            trip_df.loc[i_row, "shape_dist_traveled"] = (
                trip_df.loc[i_row, "dist_stops"]
                + trip_df.loc[i_row2, "shape_dist_traveled"]
            )
        else:
            trip_df.loc[i_row, "shape_dist_traveled"] = trip_df.loc[i_row, "dist_stops"]
        i_row2 += 1
        i_row += 1

    if_remove_single_file(trip_csv)
    trip_df.to_csv(trip_csv, index=False)


def move_OSMstops_on_the_road(
    temp_OSM_for_routing,
    nmRD_temp_folder,
    OSMallroad_gpkg,
    ls_to_check,
    lines_df,
    files_to_del,
):

    for to_check in ls_to_check:
        to_check_name = to_check[:-5]
        to_check_gpkg = os.path.join(temp_OSM_for_routing, to_check)
        to_check_csv = os.path.join(nmRD_temp_folder, str(to_check_name) + ".csv")
        OSM_new_pos_gpkg = os.path.join(
            nmRD_temp_folder, str(to_check_name) + "_new_pos1.gpkg"
        )

        if_remove_single_file(to_check_csv)
        to_check_layer = QgsVectorLayer(to_check_gpkg, to_check_name, "ogr")
        virtual_layer_to_csv(to_check_layer, to_check_csv)

        ls_fields_name_to_remove = ["lon", "lat"]

        for field_name in ls_fields_name_to_remove:
            field_index = to_check_layer.fields().indexFromName(field_name)
            if field_index != -1:
                to_check_layer.startEditing()
                to_check_layer.deleteAttribute(field_index)
                to_check_layer.commitChanges()
            else:
                print(f"Field '{field_name}' not found.")

        pr = to_check_layer.dataProvider()
        pr.addAttributes(
            [QgsField("lon", QVariant.Double), QgsField("lat", QVariant.Double)]
        )
        to_check_layer.updateFields()
        to_check_layer.commitChanges()

        expression2 = QgsExpression("$x")
        expression3 = QgsExpression("$y")

        context = QgsExpressionContext()
        context.appendScopes(
            QgsExpressionContextUtils.globalProjectLayerScopes(to_check_layer)
        )

        with edit(to_check_layer):
            for f in to_check_layer.getFeatures():
                context.setFeature(f)
                f["lon"] = expression2.evaluate(context)
                f["lat"] = expression3.evaluate(context)
                to_check_layer.updateFeature(f)
        param = {
            "INPUT": to_check_layer,
            "REFERENCE": OSMallroad_gpkg,
            "DISTANCE": 0.0000001,
            "METHOD": 0,
        }
        processing.run("native:selectwithindistance", param)

        to_check_layer.invertSelection()

        if to_check_layer.selectedFeatureCount() > 0:

            OSM_off_road_gpkg = os.path.join(
                nmRD_temp_folder, to_check_name + "_OSM_off_road.gpkg"
            )

            nmRD_stops_csv = os.path.join(
                nmRD_temp_folder, to_check_name + "_OSM_off_road.csv"
            )

            OSM_new_pos_csv = os.path.join(
                nmRD_temp_folder, str(to_check_name) + "_new_pos1.csv"
            )

            virtual_layer_to_csv(to_check_layer, nmRD_stops_csv, seletedFeatures=True)

            QgsVectorFileWriter.writeAsVectorFormat(
                to_check_layer,
                OSM_off_road_gpkg,
                "utf-8",
                to_check_layer.crs(),
                driverName="GPKG",
                onlySelected=True,
            )

            nmRD_stops = pd.read_csv(nmRD_stops_csv)

            line_name = nmRD_stops.loc[0, "line_name"]
            idx = lines_df.index[lines_df["line_name"] == line_name].tolist()[0]
            spl_road_gpkg = lines_df.loc[idx, "Spl_roads"]

            params = {
                "INPUT": OSM_off_road_gpkg,
                "INPUT_2": spl_road_gpkg,
                "FIELDS_TO_COPY": ["fid"],
                "DISCARD_NONMATCHING": True,
                "PREFIX": "nrstrd_",
                "NEIGHBORS": 1,
                "MAX_DISTANCE": 0.00015,
                "OUTPUT": OSM_new_pos_gpkg,
            }
            processing.run("native:joinbynearest", params)

            OSM_new_pos_layer = QgsVectorLayer(
                to_check_name + "_OSM_off_road", OSM_new_pos_gpkg, "ogr"
            )
            virtual_layer_to_csv(OSM_new_pos_layer, OSM_new_pos_csv)

            OSM_new_pos_df = pd.read_csv(
                OSM_new_pos_csv,
                dtype={"trip": int, "pos": int, "stop_id": str, "fid": int},
            )

            cols_to_keep = [
                "GTFS_stop_id",
                "line_name",
                "trip",
                "pos",
                "lon",
                "lat",
                "loc_base",
                "line_trip",
                "stop_id",
                "nearest_x",
                "nearest_y",
            ]

            ls_to_drop = [
                col for col in OSM_new_pos_df.columns if not col in cols_to_keep
            ]
            OSM_new_pos_df = OSM_new_pos_df.drop(ls_to_drop, axis=1)
            OSM_new_pos_df["lon"] = OSM_new_pos_df["nearest_x"].fillna(
                OSM_new_pos_df["lon"]
            )
            OSM_new_pos_df["lat"] = OSM_new_pos_df["nearest_y"].fillna(
                OSM_new_pos_df["lat"]
            )
            OSM_new_pos_df["loc_base"] = "moved off-road-OSM on the nearest"

            cols_to_keep = [
                "GTFS_stop_id",
                "line_name",
                "trip",
                "pos",
                "loc_base",
                "line_trip",
                "stop_id",
                "lon",
                "lat",
            ]

            OSM_new_pos_df = OSM_new_pos_df[cols_to_keep]
            print(OSM_new_pos_df)

            df_to_check = pd.read_csv(
                to_check_csv,
                dtype={"trip": int, "pos": int, "stop_id": str},
            )
            df_to_check = df_to_check[cols_to_keep]
            row_to_drop = OSM_new_pos_df.pos.unique()
            df_to_check = df_to_check[~df_to_check["pos"].isin(row_to_drop)]
            print(df_to_check)
            to_save = (
                pd.concat([df_to_check, OSM_new_pos_df], ignore_index=True)
                .sort_values("pos")
                .reset_index(drop=True)
            )
            to_save["fid"] = to_save["pos"] + 1
            to_save = to_save.set_index("fid")
            print(to_save)
            if_remove_single_file(to_check_csv)
            to_save.to_csv(to_check_csv)
            if_remove(OSM_new_pos_csv, files_to_del)
            if_remove(OSM_new_pos_gpkg, files_to_del)
            if_remove(nmRD_stops_csv, files_to_del)
            if_remove(OSM_off_road_gpkg, files_to_del)
            save_csv_overwrite_gpkg(to_check_name, to_check_gpkg, to_check_csv)


def virtual_layer_to_csv(
    virtual_layer: QgsVectorLayer, csv_path, seletedFeatures: bool = False
):
    save_options = QgsVectorFileWriter.SaveVectorOptions()
    save_options.driverName = "csv"
    save_options.fileEncoding = "utf-8"
    save_options.onlySelectedFeatures = seletedFeatures
    layer_context = virtual_layer.transformContext()
    coordinates = QgsCoordinateTransformContext(layer_context)
    QgsVectorFileWriter.writeAsVectorFormatV3(
        virtual_layer, csv_path, coordinates, save_options
    )


def save_csv_overwrite_gpkg(name, gpkg, csv):
    print("starting overwriting the gpkg positions")
    to_check_path = r"file:///{}?crs={}&delimiter={}&xField={}&yField={}".format(
        csv, "epsg:4326", ",", "lon", "lat"
    )
    save_options = QgsVectorFileWriter.SaveVectorOptions()
    save_options.driverName = "gpkg"
    save_options.fileEncoding = "utf-8"
    save_options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile

    new_OSM_pos_layer = QgsVectorLayer(to_check_path, name, "delimitedtext")
    layer_context = new_OSM_pos_layer.transformContext()
    coordinates = QgsCoordinateTransformContext(layer_context)
    QgsVectorFileWriter.writeAsVectorFormatV3(
        new_OSM_pos_layer, gpkg, coordinates, save_options
    )


def check_the_off_road_pt_stops(
    temp_OSM_for_routing,
    nmRD_temp_folder,
    OSMallroad_gpkg,
    allstops_name,
    allstops_csv,
    nmRD_stops_csv,
    ls_to_check,
):
    allstops_to_check = pd.DataFrame()
    for to_check in ls_to_check:
        to_check_name = to_check[:-5]
        to_check_gpkg = os.path.join(temp_OSM_for_routing, to_check)
        to_check_csv = os.path.join(nmRD_temp_folder, str(to_check_name) + ".csv")
        to_check_layer = QgsVectorLayer(to_check_gpkg, to_check_name, "ogr")
        ls_fields_name_to_remove = ["lon", "lat"]

        for field_name in ls_fields_name_to_remove:
            field_index = to_check_layer.fields().indexFromName(field_name)
            if field_index != -1:
                to_check_layer.startEditing()
                to_check_layer.deleteAttribute(field_index)
                to_check_layer.commitChanges()
            else:
                print(f"Field '{field_name}' not found.")

        pr = to_check_layer.dataProvider()
        pr.addAttributes(
            [QgsField("lon", QVariant.Double), QgsField("lat", QVariant.Double)]
        )
        to_check_layer.updateFields()
        to_check_layer.commitChanges()

        expression2 = QgsExpression("$x")
        expression3 = QgsExpression("$y")

        context = QgsExpressionContext()
        context.appendScopes(
            QgsExpressionContextUtils.globalProjectLayerScopes(to_check_layer)
        )

        with edit(to_check_layer):
            for f in to_check_layer.getFeatures():
                context.setFeature(f)
                f["lon"] = expression2.evaluate(context)
                f["lat"] = expression3.evaluate(context)
                to_check_layer.updateFeature(f)

        if_remove_single_file(to_check_csv)
        QgsVectorFileWriter.writeAsVectorFormat(
            to_check_layer, to_check_csv, "utf-8", driverName="CSV"
        )
        df_to_check = pd.read_csv(
            to_check_csv, dtype={"trip": int, "pos": int, "stop_id": str}
        )
        if not df_to_check.empty:
            allstops_to_check = pd.concat(
                [allstops_to_check, df_to_check], ignore_index=True
            )

    allstops_to_check.to_csv(allstops_csv, index=False)

    allstops_path = r"file:///{}?crs={}&delimiter={}&xField={}&yField={}".format(
        allstops_csv, "epsg:4326", ",", "lon", "lat"
    )
    allstops_layer = QgsVectorLayer(allstops_path, allstops_name, "delimitedtext")

    param = {
        "INPUT": allstops_layer,
        "REFERENCE": OSMallroad_gpkg,
        "DISTANCE": 0.0000001,
        "METHOD": 0,
    }
    processing.run("native:selectwithindistance", param)

    allstops_layer.invertSelection()

    QgsVectorFileWriter.writeAsVectorFormat(
        allstops_layer, nmRD_stops_csv, "utf-8", driverName="CSV", onlySelected=True
    )

    to_check = pd.read_csv(
        nmRD_stops_csv, dtype={"trip": int, "pos": int, "stop_id": str}
    )

    return to_check
