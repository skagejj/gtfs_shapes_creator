from qgis import processing
from qgis.core import (
    QgsProperty,
    QgsVectorFileWriter,
    QgsVectorLayer,
    QgsField,
    QgsExpressionContext,
    QgsExpressionContextUtils,
    edit,
    QgsExpression,
    QgsCoordinateReferenceSystem,
    QgsProcessingFeatureSourceDefinition,
    QgsFeatureRequest,
    QgsProject,
    QgsCoordinateTransformContext,
    QgsFields,
    QgsWkbTypes,
    QgsRasterLayer,
)
from qgis.utils import iface
from qgis.PyQt.QtCore import QVariant
import pandas as pd
import re
import numpy as np
import os
import json
import fnmatch
import math
import statistics as stat
import time
import datetime
from urllib.parse import urlencode
from .OSM_PT_routing import (
    if_remove_single_file,
    vector_layer_to_csv,
    correct_uri_for_windows,
)


def if_not_make(folders_to_make: list):
    for folder in folders_to_make:
        os.makedirs(folder, exist_ok=True)


def load_files_to_del(agencies_folder):
    files_to_delete_next_bus_loading_json = os.path.join(
        agencies_folder, "temp/files_to_delete_next_bus_loading.json"
    )
    if os.path.exists(files_to_delete_next_bus_loading_json):
        with open(files_to_delete_next_bus_loading_json, "r") as f:
            files_to_del = json.load(f)
        for file in files_to_del["path"]:
            files_to_del = if_remove(file, files_to_del)
        files_to_del_str = json.dumps(files_to_del, indent=2)
        with open(files_to_delete_next_bus_loading_json, "w") as f:
            f.write(files_to_del_str)
    else:
        files_to_del = {"path": []}
    return files_to_del


def if_remove(file_path, files_to_del):
    if os.path.exists(file_path):
        try:
            if file_path in files_to_del["path"]:
                files_to_del["path"].remove(file_path)
            os.remove(file_path)
        except Exception as e:
            files_to_del["path"].append(file_path)
    return files_to_del


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def add_filepath_to_lines_csv(lines_df, lines_df_csv, i_row, files_to_save: dict):
    for file in files_to_save.keys():
        lines_df.loc[i_row, file] = files_to_save[file]
    if_remove_single_file(lines_df_csv)
    lines_df.to_csv(lines_df_csv, index=False)
    return lines_df


def quickOSM_API(params):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            processing.run("quickosm:downloadosmdatarawquery", params)
            break
        except Exception as e:
            if "Gateway Timeout" in str(e) or "NetWorkErrorException" in str(e):
                if attempt < max_retries - 1:
                    wait_time = (
                        attempt + 1
                    ) * 30  # Wait 30, 60 seconds between retries
                    time.sleep(wait_time)
                else:
                    raise
            else:
                # Re-raise non-timeout errors immediately
                raise


def downloading_ways(extent, extent_quickosm, OSM_ways_gpkg):
    params = {
        "QUERY": '[out:xml] [timeout:25];\n(    \n    way["highway"="service"]('
        + str(extent)
        + ');\n    way["highway"="living_street"]('
        + str(extent)
        + ');\n    way["highway"="motorway"]('
        + str(extent)
        + ');\n    way["highway"="primary"]('
        + str(extent)
        + ');\n    way["highway"="secondary"]('
        + str(extent)
        + ');\n    way["highway"="tertiary"]('
        + str(extent)
        + ');\n    way["highway"="residential"]('
        + str(extent)
        + ');\n    way["highway"="unclassified"]('
        + str(extent)
        + ');\n    way["highway"="motorway_link"]('
        + str(extent)
        + ');\n    way["highway"="primary_link"]('
        + str(extent)
        + ');\n    way["highway"="secondary_link"]('
        + str(extent)
        + ');\n    way["highway"="tertiary_link"]('
        + str(extent)
        + ');\n    way["highway"="residential"]('
        + str(extent)
        + ');\n    way["highway"="motorway_junction"]('
        + str(extent)
        + ");\n    \n  \t\n);\n(._;>;);\nout body;",
        "TIMEOUT": 180,
        "SERVER": "https://overpass-api.de/api/interpreter",
        "EXTENT": extent_quickosm,
        "AREA": "",
        "FILE": OSM_ways_gpkg,
    }
    quickOSM_API(params)


def downloading_railway(extent, extent_quickosm, OSM_tramways_gpkg, trnsprt):

    params = {
        "QUERY": '[out:xml] [timeout:25];\n(    \n    way["railway"="'
        + str(trnsprt)
        + '"]('
        + str(extent)
        + ");\n    \n  \t\n);\n(._;>;);\nout body;",
        "TIMEOUT": 180,
        "SERVER": "https://overpass-api.de/api/interpreter",
        "EXTENT": extent_quickosm,
        "AREA": "",
        "FILE": OSM_tramways_gpkg,
    }
    quickOSM_API(params)


def highway_average_speed(OSM_roads_csv, highway_speed_csv):

    city_roads = pd.read_csv(OSM_roads_csv, low_memory=False)

    ls_highway = city_roads.highway.unique()

    highway_speed = pd.DataFrame(ls_highway)

    highway_speed = highway_speed.rename(columns={0: "highway"})

    i_hgw = 0
    while i_hgw < len(highway_speed):
        ls_speeds = []
        Roads = city_roads[
            city_roads["highway"] == highway_speed.loc[i_hgw, "highway"]
        ].reset_index(drop=True)
        all_speeds = list(Roads["maxspeed"])
        i_row = 0
        while i_row < len(all_speeds):
            if str(all_speeds[i_row]).isnumeric():
                ls_speeds.append(int(all_speeds[i_row]))
            i_row += 1
        if ls_speeds:
            highway_speed.loc[i_hgw, "average_speed"] = stat.mean(ls_speeds)
        i_hgw += 1
        del Roads, i_row, ls_speeds, all_speeds

    highway_speed["bus_lanes"] = highway_speed["average_speed"] * 2

    highway_speed.to_csv(highway_speed_csv, index=False)


def busroutes(
    bus_lanes_name,
    OSM_bus_lanes_gpkg,
    OSM_bus_lanes_csv,
    OSM_roads_gpkg,
    highway_speed_csv,
    OSM_bus_lanes_with_ms_ow_fr_gpkg,
    OSM_bus_lanes_with_ms_ow_fr_name,
):

    # extract bus lanes in a gpkg
    bus_lanes_selection = '"bus" is not NULL OR "bus:lanes" is not NULL OR "bus:lanes:backward" is not NULL OR "bus:lanes:forward" is not NULL OR "busway" is not NULL OR "busway:left" is not NULL OR "busway:left" is not NULL   OR "busway:right" is not NULL OR "busway:right" is not NULL   OR "hgv" is not NULL OR "hgv:lanes" is not NULL OR "lanes:bus" is not NULL OR "lanes:bus:backward" is not NULL OR "lanes:bus:forward" is not NULL OR "lanes:psv" is not NULL   OR "lanes:psv:forward" is not NULL   OR "maxheight:physical" is not NULL   OR "oneway:bus" is not NULL   OR "oneway:psv" is not NULL   OR "trolley_wire" is not NULL   OR "trolleybus" is not NULL   OR "tourist_bus:lanes" is not NULL   OR "psv" is not NULL   OR "psv:lanes" is not NULL   OR "highway" is \'busway\' OR "psv:lanes:forward" is not NULL OR "psv:lanes:backward" is not NULL'
    params = {
        "INPUT": OSM_roads_gpkg,
        "EXPRESSION": bus_lanes_selection,
        "OUTPUT": OSM_bus_lanes_gpkg,
    }
    processing.run("native:extractbyexpression", params)

    bus_lanes_layer = QgsVectorLayer(OSM_bus_lanes_gpkg, bus_lanes_name, "ogr")
    highway_speed = pd.read_csv(highway_speed_csv)

    vector_layer_to_csv(bus_lanes_layer, OSM_bus_lanes_csv)
    OSM_bus_lanes_df = pd.read_csv(OSM_bus_lanes_csv, dtype=str)

    all_cols = [
        "bus:lanes:backward",
        "lanes:bus:backward",
        "busway:left",
        "lanes:bus:backward",
        "psv:lanes:backward",
    ]
    cols_to_check = [col for col in OSM_bus_lanes_df.columns if col in all_cols]
    condition = (
        OSM_bus_lanes_df.reindex(columns=cols_to_check).notna().any(axis=1)
        | (OSM_bus_lanes_df.get("oneway:bus") == "no")
        | (OSM_bus_lanes_df.get("oneway:psv") == "no")
    )

    params = {
        "if_true": "backward",
        "if_false": "forward",
        "multiplicator_speed": 2,
        "average_speed": "bus_lanes",
    }
    OSM_bus_lanes_df = get_oneway_maxspeed_routing_df(
        highway_speed, OSM_bus_lanes_df, condition, params
    )

    joined_vector_layer = join_oneway_maxspeed_routing_to_vl(
        OSM_bus_lanes_gpkg,
        OSM_bus_lanes_df,
        OSM_bus_lanes_csv,
    )

    vector_layer_to_gpkg(
        joined_vector_layer,
        OSM_bus_lanes_with_ms_ow_fr_name,
        OSM_bus_lanes_with_ms_ow_fr_gpkg,
    )


def full_city_roads(
    OSM_roads_gpkg,
    OSM_roads_csv,
    full_roads_gpgk,
    highway_speed_csv,
    OSM_roads_with_ms_ow_fr_name,
    OSM_roads_with_ms_ow_fr_gpkg,
    OSM_bus_lanes_with_ms_ow_fr_gpkg,
):
    highway_speed = pd.read_csv(highway_speed_csv)

    OSM_roads_df = pd.read_csv(OSM_roads_csv, dtype=str)
    condition = (OSM_roads_df["oneway"] == "yes") | (
        OSM_roads_df["junction"] == "roundabout"
    )
    params = {
        "if_true": "forward",
        "if_false": None,
        "multiplicator_speed": 1,
        "average_speed": "average_speed",
    }
    OSM_roads_df = get_oneway_maxspeed_routing_df(
        highway_speed, OSM_roads_df, condition, params
    )

    # road_layer = QgsVectorLayer(OSM_roads_gpkg, OSM_roads_name, "ogr")

    joined_vector_layer = join_oneway_maxspeed_routing_to_vl(
        OSM_roads_gpkg,
        OSM_roads_df,
        OSM_roads_csv,
    )

    vector_layer_to_gpkg(
        joined_vector_layer, OSM_roads_with_ms_ow_fr_name, OSM_roads_with_ms_ow_fr_gpkg
    )

    ls_roads = [
        OSM_roads_with_ms_ow_fr_gpkg,
        OSM_bus_lanes_with_ms_ow_fr_gpkg,
    ]

    params = {
        "LAYERS": ls_roads,
        "CRS": QgsCoordinateReferenceSystem("EPSG:4326"),
        "OUTPUT": full_roads_gpgk,
    }
    processing.run("native:mergevectorlayers", params)


def get_oneway_maxspeed_routing_df(highway_speed, OSM_roads_df, condition, params):
    OSM_roads_df["oneway_routing"] = np.where(
        condition,
        params["if_true"],
        params["if_false"],
    )

    highway_speed_dict = (
        highway_speed[["highway", params["average_speed"]]]
        .set_index("highway")[params["average_speed"]]
        .to_dict()
    )

    def maxspeed_routing(row, highway_speed_dict):
        maxspeed = row["maxspeed"]
        if str(maxspeed) == "nan":
            highway = row["highway"]
            if highway in highway_speed_dict:
                return highway_speed_dict[highway]
        if isinstance(maxspeed, (int, float)):
            return maxspeed * params["multiplicator_speed"]
        if isinstance(maxspeed, str):
            digits = re.search(r"[0-9]+", maxspeed)
            if digits:
                return int(digits.group()) * params["multiplicator_speed"]
        return 80

    OSM_roads_df["maxspeed_routing"] = OSM_roads_df.apply(
        maxspeed_routing, axis=1, highway_speed_dict=highway_speed_dict
    )
    return OSM_roads_df


def join_oneway_maxspeed_routing_to_vl(
    gpkg_file_path,
    df_oneway_maxspeed_routing,
    oneway_new_speed_csv,
):
    df_oneway_maxspeed_routing[
        ["full_id", "oneway_routing", "maxspeed_routing"]
    ].to_csv(oneway_new_speed_csv, index=False)

    # uri = f"file:///{oneway_new_speed_csv}?type=csv&detectTypes=yes&geomType=none&delimiter=,"
    # if os.name == "nt":  # Windows
    #     csv_path = oneway_new_speed_csv.replace("\\", "/")
    #     uri = f"file:///{csv_path}?type=csv&detectTypes=yes&geomType=none&delimiter=,"

    # join_attributes_layer = QgsVectorLayer(uri, "bl_oneway_new_speed", "delimitedtext")
    output_mempry_layer = "TEMPORARY_OUTPUT" if os.name == "nt" else "memory:"
    result = processing.run(
        "native:joinattributestable",
        {
            "INPUT": gpkg_file_path,
            "FIELD": "full_id",
            "INPUT_2": oneway_new_speed_csv,
            "FIELD_2": "full_id",
            "FIELDS_TO_COPY": ["oneway_routing", "maxspeed_routing"],
            "METHOD": 1,  # Take matching only
            "DISCARD_NONMATCHING": False,
            "PREFIX": "",
            "OUTPUT": output_mempry_layer,
        },
    )

    return result["OUTPUT"]


def vector_layer_to_gpkg(
    vector_layer,
    layer_name,
    gpkg,
    seleted_features=False,
    fields_to_keep: list = [],
):
    if fields_to_keep:
        IDs_to_keep = [
            vector_layer.fields().indexFromName(field_name)
            for field_name in fields_to_keep
        ]
        all_IDs = vector_layer.fields().allAttributesList()
        IDs_to_del = [idx for idx in all_IDs if idx not in IDs_to_keep]
        if IDs_to_del:
            fields_to_del = [vector_layer.fields()[idx].name() for idx in IDs_to_del]
            for field in fields_to_del:
                idx = vector_layer.fields().indexFromName(field)
                if idx != -1:
                    vector_layer.startEditing()
                    vector_layer.deleteAttribute(idx)
                    vector_layer.commitChanges()

    layer_context = vector_layer.transformContext()
    coordinates = QgsCoordinateTransformContext(layer_context)
    save_options = QgsVectorFileWriter.SaveVectorOptions()
    save_options.driverName = "gpkg"
    save_options.layerName = layer_name
    save_options.fileEncoding = "utf-8"
    save_options.onlySelectedFeatures = seleted_features
    if os.path.exists(gpkg):
        save_options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile
    QgsVectorFileWriter.writeAsVectorFormatV3(
        vector_layer, gpkg, coordinates, save_options
    )


def Ttbls_plus(Ttlbs_txt, Ttbls_plus_csv, dwnldfld, trips_txt):
    Ttbls_orig = pd.read_csv(Ttlbs_txt)

    Ttbls_orig.to_csv(Ttlbs_txt, index_label="orig_id")

    Ttbls = pd.read_csv(Ttlbs_txt)

    # calculate the parent_stop_id in Ttbls

    Ttbls["prnt_stp_id"] = Ttbls["stop_id"].apply(lambda x: x[:7])

    # merge route_id

    trips = pd.read_csv(trips_txt)
    trps = trips[["trip_id", "route_id"]]
    Ttbls = pd.merge(Ttbls, trps, on="trip_id", how="left")

    # join the route_short_name
    routes = pd.read_csv(os.path.join(dwnldfld, "routes.txt"))
    rts = routes.filter(
        ["route_id", "route_short_name", "trnsprt", "trnsp_shrt_name"], axis=1
    )

    Ttbls = Ttbls.merge(rts, on="route_id", how="left")

    Ttbls.to_csv(Ttbls_plus_csv, index=False)


def Selected_Ttbls(ls_buses, Ttbls_selected_txt, Ttbls_plus_csv, files_to_del):

    Ttbls = pd.read_csv(Ttbls_plus_csv)

    Ttbls_selected = Ttbls[Ttbls["trnsp_shrt_name"].isin(ls_buses)]

    if_remove(Ttbls_selected_txt, files_to_del)
    Ttbls_selected.to_csv(Ttbls_selected_txt, index=False)
    return files_to_del


def time_tables_perTransport(rt, Ttbls, tempfldr, lstrnsprt):

    Ttbl = Ttbls[Ttbls.route_id == rt]
    num = str(Ttbl["route_short_name"].iloc[0])
    trnsprt_type = str(Ttbl["trnsprt"].iloc[0])
    trnsp_shrt_name = str(Ttbl["trnsp_shrt_name"].iloc[0])

    if re.findall("[+]", num):
        num = str(re.findall("[a-zA-Z]+|[0-9]+", num)[0]) + "plus"
    id_line = 0
    if str(str(trnsprt_type) + str(num)) in lstrnsprt:
        id_line = id_line + 1
    while str(str(trnsprt_type) + str(num) + "_" + str(id_line)) in lstrnsprt:
        id_line = id_line + 1
    if id_line == 0:
        nametbl = str(trnsprt_type) + str(num)
    else:
        nametbl = str(trnsprt_type) + str(num) + "_" + str(id_line)

    Ttbl["line_name"] = nametbl
    Ttbl = Ttbl.reset_index(drop=True)
    pattern = r"[^:]+$"
    i_row = 0
    while i_row < len(Ttbl):
        stop_id = str(Ttbl.loc[i_row, "stop_id"])
        if re.search(r"[0-9]+:", stop_id):
            Ttbl.loc[i_row, "stp_pltfrm"] = str(re.search(pattern, stop_id).group())
        else:
            Ttbl.loc[i_row, "stp_pltfrm"] = ""
        i_row += 1

    Ttbl_file = os.path.join(tempfldr, str(nametbl) + "_stop_times.csv")
    Ttbl.to_csv(Ttbl_file, index=False)
    rt_srt_nm = str(Ttbl["route_short_name"].iloc[0])
    return Ttbl, nametbl, Ttbl_file, rt_srt_nm, trnsprt_type, trnsp_shrt_name


def preapare_GTFSstops_by_transport(
    stops_txt,
    Ttbl_file,
    trnsprt,
    tempfolder,
    shrt_name,
    tempfolderstptimes,
    files_to_del,
):
    stps = pd.read_csv(stops_txt, dtype={"stop_id": str})
    # load the stop times (Time Table) ot the transport
    Ttbl_unsorted = pd.read_csv(Ttbl_file, dtype={"stop_id": str})
    Ttbl = Ttbl_unsorted.sort_values(
        ["trip_id", "departure_time", "stop_sequence"]
    ).reset_index(drop=True)

    # create the stop table per transport
    seq_ls = []

    sequences = pd.DataFrame()

    # create sequence with prnt_stp_id
    i_row = 0
    i_row2 = 1
    seq_init = 0
    seq_end = 0
    i_seq = 0
    i_max = len(Ttbl) - 1
    while i_row < i_max:
        if Ttbl.loc[i_row, "stop_sequence"] < Ttbl.loc[i_row2, "stop_sequence"]:
            seq_ls.append(str(Ttbl.loc[i_row, "prnt_stp_id"]))
            seq_end += 1
        else:
            seq_ls.append(str(Ttbl.loc[i_row, "prnt_stp_id"]))

            seq_str = " ".join(seq_ls)

            sequences.loc[i_seq, 0] = i_seq
            sequences.loc[i_seq, "sequence"] = seq_str
            i_seq += 1
            while seq_init <= seq_end:
                Ttbl.loc[seq_init, "sequence"] = seq_str
                seq_init += 1
            del seq_ls, seq_str  # , i_ls
            seq_ls = []
            seq_end += 1
        i_row += 1
        i_row2 += 1

    # add the sequence to the record of the last sequence >bug resolved<
    seq_ls.append(str(Ttbl.loc[i_row, "prnt_stp_id"]))

    seq_str = " ".join(seq_ls)

    sequences.loc[i_seq, 0] = i_seq
    sequences.loc[i_seq, "sequence"] = seq_str
    del i_seq
    while seq_init <= seq_end:
        Ttbl.loc[seq_init, "sequence"] = seq_str
        seq_init += 1
    del seq_ls, seq_str  # i_ls

    # create listo of unique sequences
    del i_row, i_row2, i_max
    sequences = sequences.rename(columns={0: "id"})
    lsuniseqs = sequences.sequence.unique()

    # create the mother_sequences list without sub-sequences
    lstodelete = []
    mother_sequences = lsuniseqs
    i_row = 0
    i_max = len(lsuniseqs) - 1
    while i_row < i_max:
        i_row2 = i_row + 1
        while i_row2 < len(lsuniseqs):
            if len(lsuniseqs[i_row]) > len(lsuniseqs[i_row2]):
                seq1 = lsuniseqs[i_row]
                seq2 = lsuniseqs[i_row2]
                i_del = i_row2
            else:
                seq2 = lsuniseqs[i_row]
                seq1 = lsuniseqs[i_row2]
                i_del = i_row
            if seq2 in seq1:
                if not lsuniseqs[i_del] in lstodelete:
                    lstodelete.append(lsuniseqs[i_del])
            i_row2 += 1
        del i_row2
        i_row += 1
    mother_sequences = [seq for seq in mother_sequences if seq not in lstodelete]

    # for each Ttbl value add the sequence stop ID
    # to define the position of the stop in the beloging sequence
    i_row = 0
    while i_row < len(mother_sequences):
        moth_seq = mother_sequences[i_row].split(" ")
        ls_repet = []
        for elem in moth_seq:
            if moth_seq.count(elem) > 1:
                ls_repet.append(elem)
        i_row2 = 0
        while i_row2 < len(Ttbl):
            if Ttbl.loc[i_row2, "sequence"] in mother_sequences[i_row]:
                pos = (
                    mother_sequences[i_row]
                    .split(" ")
                    .index(str(Ttbl.loc[i_row2, "prnt_stp_id"]))
                )
                row_init = i_row2
                row_after = i_row2 + 1
                if ls_repet and str(Ttbl.loc[i_row2, "prnt_stp_id"]) in ls_repet:
                    sequ_ls = [str(Ttbl.loc[row_init, "prnt_stp_id"])]
                    while (
                        row_after < len(Ttbl)
                        and Ttbl.loc[row_init, "stop_sequence"]
                        < Ttbl.loc[row_after, "stop_sequence"]
                    ):
                        sequ_ls.append(str(Ttbl.loc[row_after, "prnt_stp_id"]))
                        row_init += 1
                        row_after += 1
                    sequ_str = " ".join(sequ_ls)
                    idx_ls = 0
                    while idx_ls < len(moth_seq):
                        if not sequ_str in " ".join(moth_seq[idx_ls : len(moth_seq)]):
                            pos = idx_ls - 1
                            break
                        idx_ls += 1
                        pos = idx_ls - 1
                Ttbl.loc[i_row2, "seq_stpID"] = (
                    str(trnsprt) + "_trip" + str(i_row + 1) + "_pos" + str(pos)
                )
            i_row2 += 1
        i_row += 1

    i_row = 0
    while i_row < len(Ttbl):
        Ttbl.loc[i_row, "trip"] = int(Ttbl.loc[i_row, "seq_stpID"].split("_")[1][4:])
        Ttbl.loc[i_row, "pos"] = int(Ttbl.loc[i_row, "seq_stpID"].split("_")[2][3:])
        i_row += 1
    Ttbl = Ttbl.astype({"trip": "int", "pos": "int"})

    Ttbl_with_sequences_csv = os.path.join(
        tempfolderstptimes, str(trnsprt) + "_stops_times_with_seq.csv"
    )

    Ttbl.to_csv(Ttbl_with_sequences_csv, index=False)

    # most frequent stops
    ls_GTFS_stops = list(Ttbl.seq_stpID.unique())
    most_freq_stps = pd.DataFrame(ls_GTFS_stops)
    most_freq_stps = most_freq_stps.rename(columns={0: "seq_stpID"})
    i_ls = 0
    while i_ls < len(ls_GTFS_stops):
        ls_stp_id_most_frequent = list(
            Ttbl["stop_id"][Ttbl["seq_stpID"] == ls_GTFS_stops[i_ls]][
                Ttbl["stp_pltfrm"] != ""
            ]
        )
        if ls_stp_id_most_frequent:
            most_freq_stps.loc[i_ls, "stop_id"] = max(
                set(ls_stp_id_most_frequent), key=ls_stp_id_most_frequent.count
            )
        else:
            most_freq_stps.loc[i_ls, "stop_id"] = Ttbl["stop_id"][
                Ttbl["seq_stpID"] == ls_GTFS_stops[i_ls]
            ].iloc[0]
        i_ls += 1
        del ls_stp_id_most_frequent

    i_row = 0
    while i_row < len(most_freq_stps):
        most_freq_stps.loc[i_row, "trip"] = int(
            most_freq_stps.loc[i_row, "seq_stpID"].split("_")[1][4:]
        )
        most_freq_stps.loc[i_row, "pos"] = int(
            most_freq_stps.loc[i_row, "seq_stpID"].split("_")[2][3:]
        )
        i_row += 1

    most_freq_stps_unsorted = most_freq_stps.astype({"trip": "int", "pos": "int"})
    del most_freq_stps

    most_freq_stps = most_freq_stps_unsorted.sort_values(["trip", "pos"]).reset_index(
        drop=True
    )

    # creation and adding segments
    i_row = 0
    i_row2 = 1
    i_max = len(most_freq_stps) - 1
    while i_row < i_max:
        if most_freq_stps.loc[i_row, "pos"] < most_freq_stps.loc[i_row2, "pos"]:
            most_freq_stps.loc[i_row, "mini_trip"] = (
                str(most_freq_stps.loc[i_row, "stop_id"])
                + " "
                + str((most_freq_stps.loc[i_row2, "stop_id"]))
            )
            most_freq_stps.loc[i_row, "mini_tr_pos"] = (
                str(trnsprt)
                + "_trip"
                + str(most_freq_stps.loc[i_row, "trip"])
                + "_pos"
                + str((most_freq_stps.loc[i_row, "pos"]))
                + "-pos"
                + str((most_freq_stps.loc[i_row2, "pos"]))
            )
        i_row += 1
        i_row2 += 1

    if not most_freq_stps.stop_id.dtypes == "object":
        most_freq_stps = most_freq_stps.astype({"stop_id": "int"})
        most_freq_stps = most_freq_stps.astype({"stop_id": "str"})
    most_freq_stps = most_freq_stps.merge(stps, how="left", on="stop_id")

    i = 0

    # calculate the parent_stop_id in transport stops table
    while i < len(most_freq_stps):
        most_freq_stps.loc[i, "prnt_stp_id"] = str(most_freq_stps.loc[i, "stop_id"][:7])
        i = i + 1
    del i

    # calculate the stp_pltfrm in Ttbls

    pattern = r"[^:]+$"
    i_row = 0
    while i_row < len(most_freq_stps):
        stop_id = str(most_freq_stps.loc[i_row, "stop_id"])
        if re.search(r"[0-9]+:", stop_id):
            most_freq_stps.loc[i_row, "stp_pltfrm"] = str(
                re.search(pattern, stop_id).group()
            )
        else:
            most_freq_stps.loc[i_row, "stp_pltfrm"] = ""
        i_row += 1

    most_freq_stps["line_name"] = trnsprt

    most_freq_stps["route_short_name"] = shrt_name

    GTFSstops_path = os.path.join(tempfolder, str(trnsprt) + "_stops_segments.csv")
    if_remove(GTFSstops_path, files_to_del)
    most_freq_stps.to_csv(GTFSstops_path, index=False)
    return GTFSstops_path, Ttbl_with_sequences_csv, files_to_del


def shape_assignement(GTFSstops_csv, Ttbl_file, line_trip_csv, trips_txt):

    GTFSstops = pd.read_csv(
        GTFSstops_csv,
        dtype={"pos": "int", "trip": "int", "prnt_stp_id": "str", "stop_id": "str"},
    )
    Ttbl = pd.read_csv(
        Ttbl_file,
        dtype={"pos": "int", "trip": "int", "prnt_stp_id": "str", "stop_id": "str"},
    )

    i_row = 0
    while i_row < len(GTFSstops):
        GTFSstops.loc[i_row, "line_trip"] = (
            str(GTFSstops.loc[i_row, "line_name"])
            + "_trip"
            + str(GTFSstops.loc[i_row, "trip"])
        )
        i_row += 1

    line_trip_df = pd.DataFrame(GTFSstops.line_trip.unique()).rename(
        columns={0: "line_trip"}
    )
    str_prnt_stp = ""
    i_row = 0
    while i_row < len(line_trip_df):
        GTFSstops_line_trip = GTFSstops[
            GTFSstops["line_trip"] == line_trip_df.loc[i_row, "line_trip"]
        ].reset_index(drop=True)
        str_prnt_stp = ""
        i_row2 = 0
        while i_row2 < len(GTFSstops_line_trip):
            str_prnt_stp = (
                str(str_prnt_stp)
                + " "
                + str(GTFSstops_line_trip.loc[i_row2, "prnt_stp_id"])
            )
            i_row2 += 1

        line_trip_df.loc[i_row, "main_seq"] = str_prnt_stp
        i_row += 1

    trip_id_df = pd.DataFrame(Ttbl.trip_id.unique()).rename(columns={0: "trip_id"})
    str_prnt_stp = ""
    i_row = 0
    while i_row < len(trip_id_df):
        Ttbl_trip = Ttbl[
            Ttbl["trip_id"] == trip_id_df.loc[i_row, "trip_id"]
        ].reset_index(drop=True)
        str_prnt_stp = ""
        i_row2 = 0
        while i_row2 < len(Ttbl_trip):
            str_prnt_stp = (
                str(str_prnt_stp) + " " + str(Ttbl_trip.loc[i_row2, "prnt_stp_id"])
            )
            i_row2 += 1

        trip_id_df.loc[i_row, "seq"] = str_prnt_stp
        i_row += 1

    i_row = 0
    while i_row < len(trip_id_df):
        line_trip = ""
        i_row2 = 0
        while line_trip == "":
            if str(trip_id_df.loc[i_row, "seq"]) in str(
                line_trip_df.loc[i_row2, "main_seq"]
            ):
                line_trip = str(line_trip_df.loc[i_row2, "line_trip"])
            i_row2 += 1

        trip_id_df.loc[i_row, "line_trip"] = line_trip
        i_row += 1

    trips = pd.read_csv(trips_txt, index_col="trip_id", dtype="str")

    i_row = 0
    while i_row < len(trip_id_df):
        trip_idx = str(trip_id_df.loc[i_row, "trip_id"])
        trips.loc[trip_idx, "shape_id"] = trip_id_df.loc[i_row, "line_trip"]
        i_row += 1

    os.remove(trips_txt)
    trips.to_csv(trips_txt)

    line_trip_df.to_csv(line_trip_csv, index=False)


def angles_tram(
    city_rails_layer, trnsprt, trnsprt_GTFSstops_file, temp_road_folder, GTFSnm_folder
):
    GTFSstopspath = correct_uri_for_windows(
        trnsprt_GTFSstops_file, "stop_lon", "stop_lat"
    )

    GTFSstopslayer = QgsVectorLayer(
        GTFSstopspath, str(trnsprt) + "_GTFSstops", "delimitedtext"
    )
    params = {
        "INPUT": GTFSstopslayer,
        "DISTANCE": 0.00150,
        "SEGMENTS": 5,
        "END_CAP_STYLE": 0,
        "JOIN_STYLE": 0,
        "MITER_LIMIT": 2,
        "DISSOLVE": True,
        "SEPARATE_DISJOINT": False,
        "OUTPUT": os.path.join(
            temp_road_folder, "bf_" + str(trnsprt) + "_GTFSstops.gpkg"
        ),
    }
    processing.run("native:buffer", params)
    del params

    # clippint roads to make it smaller
    params = {
        "INPUT": city_rails_layer,
        "OVERLAY": os.path.join(
            temp_road_folder, "bf_" + str(trnsprt) + "_GTFSstops.gpkg"
        ),
        "OUTPUT": os.path.join(temp_road_folder, "cl_" + str(trnsprt) + "_rail.gpkg"),
    }
    processing.run("native:clip", params)
    del params

    spl_file = os.path.join(temp_road_folder, "Spl_" + str(trnsprt) + "_rail.gpkg")

    # splitting in to more simple lines
    params = {
        "INPUT": os.path.join(temp_road_folder, "cl_" + str(trnsprt) + "_rail.gpkg"),
        "OUTPUT": spl_file,
    }
    processing.run("native:multiparttosingleparts", params)
    del params

    # expression to calculate angle_at_vertex($geometry,0)
    splt_roads = QgsVectorLayer(spl_file, "Spl_" + str(trnsprt) + "_rail", "ogr")
    pr = splt_roads.dataProvider()
    pr.addAttributes([QgsField("stp_angl", QVariant.Double)])
    splt_roads.updateFields

    expression = QgsExpression("angle_at_vertex($geometry,0)")

    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(splt_roads))

    with edit(splt_roads):
        for f in splt_roads.getFeatures():
            context.setFeature(f)
            f["stp_angl"] = expression.evaluate(context)
            splt_roads.updateFeature(f)

    anglefile = os.path.join(temp_road_folder, "GTFS" + str(trnsprt) + "_angle.gpkg")
    GTFSnomatchangl = os.path.join(
        GTFSnm_folder, "GTFS_NOmatch_RD" + str(trnsprt) + ".gpkg"
    )
    GTFS_NMangcsv = os.path.join(
        GTFSnm_folder, "GTFS_NOmatch_RD" + str(trnsprt) + ".csv"
    )

    # join attributes by nearest for angle
    params = {
        "INPUT": GTFSstopslayer,
        "INPUT_2": splt_roads,
        "FIELDS_TO_COPY": [
            "full_id",
            "osm_id",
            "osm_type",
            "name",
            "highway",
            "stp_angl",
        ],
        "DISCARD_NONMATCHING": True,
        "PREFIX": "nrstrd_",
        "NEIGHBORS": 1,
        "MAX_DISTANCE": 0.00015,
        "OUTPUT": anglefile,
        "NON_MATCHING": GTFSnomatchangl,
    }
    processing.run("native:joinbynearest", params)
    GTFSnomatchplt = QgsVectorLayer(GTFSnomatchangl, "GTFSnmRD" + str(trnsprt), "ogr")

    vector_layer_to_csv(GTFSnomatchplt, GTFS_NMangcsv)

    del params, context, expression
    return anglefile, GTFSnomatchangl, GTFS_NMangcsv, spl_file


def angles_buses(
    roadlayer, trnsprt, trnsprt_GTFSstops_file, temp_road_folder, GTFSnm_folder
):
    GTFSstopspath = correct_uri_for_windows(
        trnsprt_GTFSstops_file, "stop_lon", "stop_lat"
    )

    GTFSstopslayer = QgsVectorLayer(
        GTFSstopspath, str(trnsprt) + "_GTFSstops", "delimitedtext"
    )
    params = {
        "INPUT": GTFSstopslayer,
        "DISTANCE": 0.00015,
        "SEGMENTS": 5,
        "END_CAP_STYLE": 0,
        "JOIN_STYLE": 0,
        "MITER_LIMIT": 2,
        "DISSOLVE": True,
        "SEPARATE_DISJOINT": False,
        "OUTPUT": os.path.os.path.join(
            temp_road_folder, "bf_" + str(trnsprt) + "_GTFSstops.gpkg"
        ),
    }
    processing.run("native:buffer", params)
    del params

    # clippint roads to make it smaller
    params = {
        "INPUT": roadlayer,
        "OVERLAY": os.path.join(
            temp_road_folder, "bf_" + str(trnsprt) + "_GTFSstops.gpkg"
        ),
        "OUTPUT": os.path.join(
            temp_road_folder, "cl_" + str(trnsprt) + "_swissroad.gpkg"
        ),
    }
    processing.run("native:clip", params)
    del params

    spl_file = os.path.join(temp_road_folder, "Spl_" + str(trnsprt) + "_swissroad.gpkg")

    # splitting in to more simple lines
    params = {
        "INPUT": os.path.join(
            temp_road_folder, "cl_" + str(trnsprt) + "_swissroad.gpkg"
        ),
        "OUTPUT": spl_file,
    }
    processing.run("native:multiparttosingleparts", params)
    del params

    splt_roads = QgsVectorLayer(spl_file, "Spl_" + str(trnsprt) + "_roads", "ogr")
    pr = splt_roads.dataProvider()
    pr.addAttributes([QgsField("stp_angl", QVariant.Double)])
    splt_roads.updateFields

    expression = QgsExpression("angle_at_vertex($geometry,0)")

    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(splt_roads))

    with edit(splt_roads):
        for f in splt_roads.getFeatures():
            context.setFeature(f)
            f["stp_angl"] = expression.evaluate(context)
            splt_roads.updateFeature(f)

    anglefile = os.path.join(temp_road_folder, "GTFS" + str(trnsprt) + "_angle.gpkg")
    GTFSnomatchangl = os.path.join(
        GTFSnm_folder, "GTFS_NOmatch_RD" + str(trnsprt) + ".gpkg"
    )
    GTFS_NMangcsv = os.path.join(
        GTFSnm_folder, "GTFS_NOmatch_RD" + str(trnsprt) + ".csv"
    )

    # join attributes by nearest for angle
    params = {
        "INPUT": GTFSstopslayer,
        "INPUT_2": splt_roads,
        "FIELDS_TO_COPY": [
            "full_id",
            "osm_id",
            "osm_type",
            "name",
            "highway",
            "stp_angl",
        ],
        "DISCARD_NONMATCHING": True,
        "PREFIX": "nrstrd_",
        "NEIGHBORS": 1,
        "MAX_DISTANCE": 0.00015,
        "OUTPUT": anglefile,
        "NON_MATCHING": GTFSnomatchangl,
    }
    processing.run("native:joinbynearest", params)
    GTFSnomatchplt = QgsVectorLayer(GTFSnomatchangl, "GTFSnmRD" + str(trnsprt), "ogr")

    vector_layer_to_csv(GTFSnomatchplt, GTFS_NMangcsv)

    del params, context, expression
    return anglefile, GTFSnomatchangl, GTFS_NMangcsv, spl_file


def angle_onRD_sidewalk(
    GTFSstops_angle,
    GTFSstops_angle_sidewalk_gpkg,
    GTFSstops_angle_OSMonROADline_gpkg,
    agency_txt,
):
    agency = pd.read_csv(agency_txt)
    ls_agency = agency.agency_id.unique()
    if 881 in ls_agency:
        dist = 0.00001
    else:
        dist = 0.001
    params = {
        "INPUT": GTFSstops_angle,
        "EXPRESSION": '"distance" > ' + str(dist),
        "OUTPUT": GTFSstops_angle_sidewalk_gpkg,
        "FAIL_OUTPUT": GTFSstops_angle_OSMonROADline_gpkg,
    }
    processing.run("native:extractbyexpression", params)


def rectangles_sidewalk(
    GTFSstops_angle_sidewalk_gpkg,
    buses_long,
    tram_long,
    line_name,
    GTFSstps_rect_sidewalk_gpkg,
    GTFSstps_rect_sidewalk_csv,
    trnsprt_type,
    files_to_del,
):

    rect_type = "sidewalk"

    if (
        trnsprt_type == "Tram"
        or trnsprt_type == "RegRailServ"
        or trnsprt_type == "Funicular"
    ):
        trnsprt_long = tram_long
    else:
        trnsprt_long = buses_long

    GTFS_angl = QgsVectorLayer(
        GTFSstops_angle_sidewalk_gpkg, "angl_" + str(line_name), "ogr"
    )
    pr = GTFS_angl.dataProvider()
    pr.addAttributes(
        [
            QgsField("rect_angle", QVariant.Double),
            QgsField("rect_x2", QVariant.Double),
            QgsField("rect_y2", QVariant.Double),
            QgsField("rect_type", QVariant.String),
        ]
    )
    GTFS_angl.updateFields()

    expression1 = QgsExpression(
        'azimuth( make_point( "feature_x" ,  "feature_y" ), make_point( "nearest_x" ,  "nearest_y" ) )-1.570796327'
    )
    expression2 = QgsExpression('(("nearest_x" - "feature_x" )*0.60)+ "feature_x"')
    expression3 = QgsExpression('(("nearest_y" - "feature_y" )*0.60)+ "feature_y"')

    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(GTFS_angl))

    with edit(GTFS_angl):
        for f in GTFS_angl.getFeatures():
            context.setFeature(f)
            f["rect_angle"] = expression1.evaluate(context)
            f["rect_x2"] = expression2.evaluate(context)
            f["rect_y2"] = expression3.evaluate(context)
            f["rect_type"] = rect_type
            GTFS_angl.updateFeature(f)
    GTFS_angl.commitChanges()

    del context

    vector_layer_to_csv(GTFS_angl, GTFSstps_rect_sidewalk_csv)

    # the QgsExpression function doesn't work with sin() function that works on the QGIS FieldCalculator
    GTFS_angldf = pd.read_csv(GTFSstps_rect_sidewalk_csv)
    posXY = trnsprt_long / 2
    GTFS_angldf["rect_x"] = GTFS_angldf["rect_x2"] + posXY * np.sin(
        GTFS_angldf["rect_angle"]
    )
    GTFS_angldf["rect_y"] = GTFS_angldf["rect_y2"] + posXY * np.cos(
        GTFS_angldf["rect_angle"]
    )

    files_to_del = if_remove(GTFSstps_rect_sidewalk_csv, files_to_del)

    GTFS_angldf.to_csv(GTFSstps_rect_sidewalk_csv, index=False)

    GTFScsvpath = correct_uri_for_windows(
        GTFSstps_rect_sidewalk_csv, "rect_x", "rect_y"
    )

    GTFS_angl_layer = QgsVectorLayer(
        GTFScsvpath, "GTFSangl_" + str(line_name), "delimitedtext"
    )

    params = {
        "INPUT": GTFS_angl_layer,
        "SHAPE": 0,
        "WIDTH": QgsProperty.fromExpression('"distance"*1.20'),
        "HEIGHT": trnsprt_long,
        "ROTATION": QgsProperty.fromExpression('degrees("rect_angle")'),
        "SEGMENTS": 36,
        "OUTPUT": GTFSstps_rect_sidewalk_gpkg,
    }
    processing.run("native:rectanglesovalsdiamonds", params)

    del params, expression1, expression2, expression3
    return files_to_del


def rectangles_OSMonROADline(
    GTFSstops_path_OSMonROADline,
    buses_long,
    tram_long,
    road_average_width,
    line,
    GTFSstps_rect_OSMonROADline_gpkg,
    trnsprt_type,
):

    if (
        trnsprt_type == "Tram"
        or trnsprt_type == "RegRailServ"
        or trnsprt_type == "Funicular"
    ):
        trnsprt_long = tram_long
    else:
        trnsprt_long = buses_long

    long = trnsprt_long * 4
    params = {
        "INPUT": str(GTFSstops_path_OSMonROADline),
        "SHAPE": 0,
        "WIDTH": road_average_width,
        "HEIGHT": long,
        "ROTATION": QgsProperty.fromExpression('"nrstrd_stp_angl"'),
        "SEGMENTS": 36,
        "OUTPUT": GTFSstps_rect_OSMonROADline_gpkg,
    }
    processing.run("native:rectanglesovalsdiamonds", params)

    rect_type = "OSMonROADline"

    vlayer = QgsVectorLayer(
        GTFSstps_rect_OSMonROADline_gpkg, "rects_OSMonROADline_" + str(line), "ogr"
    )
    pr = vlayer.dataProvider()
    pr.addAttributes([QgsField("rect_type", QVariant.String)])
    vlayer.updateFields()

    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(vlayer))

    with edit(vlayer):
        for f in vlayer.getFeatures():
            context.setFeature(f)
            f["rect_type"] = rect_type
            vlayer.updateFeature(f)
    vlayer.commitChanges()

    # deleting useless fields in rectfile
    lstodelete = [
        "stop_lat",
        "stop_lon",
        "location_type",
        "parent_station",
        "OBJECTID",
        "Shape_Length",
        "STR_ESID",
        "nrstrd_stp_angl",
        "n",
        "distance",
        "feature_x",
        "feature_y",
        "nearest_x",
        "nearest_y",
        "layer",
        "path",
    ]

    idtodelete = [vlayer.fields().indexOf(field_name) for field_name in lstodelete]
    idtodelete = [index for index in idtodelete if index != -1]
    if not vlayer.isEditable():
        vlayer.startEditing()
    res = vlayer.dataProvider().deleteAttributes(idtodelete)
    if res:
        vlayer.updateFields()  # Update the layer's fields
    vlayer.commitChanges()

    del params, lstodelete, idtodelete


def OSM_PTstps_dwnld(
    extent,
    extent_quickosm,
    OSM_PTstp_rel_gpkg,
    OSM_PTstp_gpkg,
    shrt_name,
    OSM_PTstp_rel_name,
    OSM_PTstp_name,
    trnsprt_type,
):
    if trnsprt_type == "Tram":
        route = "tram"
        route_cond = "\"railway\" is 'tram_stop'"
    elif trnsprt_type == "RegRailServ":
        route = "train"
        route_cond = "\"railway\" is 'stop'"
    elif trnsprt_type == "Funicular":
        route = "funicular"
        route_cond = "\"station\" is 'funicular'"
    else:
        route = "bus"
        route_cond = "\"highway\" is 'bus_stop'"

    params = {
        "QUERY": '[out:xml] [timeout:25];\n(    \n    relation["route"="'
        + str(route)
        + '"]["ref"="'
        + str(shrt_name)
        + '"]('
        + str(extent)
        + ");\n);\n(._;>;);\nout body;",
        "TIMEOUT": 180,
        "SERVER": "https://overpass-api.de/api/interpreter",
        "EXTENT": extent_quickosm,
        "AREA": "",
        "FILE": OSM_PTstp_rel_gpkg,
    }
    try:
        quickOSM_API(params)
    except:
        # Overpass API request failed for "server replied Gateway Timeout" -> (skipped)'
        schema = QgsFields()
        schema.append(QgsField("id", QVariant.Int))

        crs = QgsCoordinateReferenceSystem("epsg:4326")
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = "GPKG"
        options.fileEncoding = "utf-8"

        fw = QgsVectorFileWriter.create(
            fileName=OSM_PTstp_rel_gpkg,
            fields=schema,
            geometryType=QgsWkbTypes.Polygon,
            srs=crs,
            transformContext=QgsCoordinateTransformContext(),
            options=options,
        )
        del fw

    OSM_PTstp_rel_layer_file = (
        str(OSM_PTstp_rel_gpkg) + "|layername=" + str(OSM_PTstp_rel_name) + "_points"
    )
    OSM_PTstp_rel_layer = QgsVectorLayer(
        OSM_PTstp_rel_layer_file, OSM_PTstp_name, "ogr"
    )

    bus_stops_selection = (
        str(route_cond) + " OR \"public_transport\" is 'stop_position'"
    )
    params = {
        "INPUT": OSM_PTstp_rel_layer,
        "EXPRESSION": bus_stops_selection,
        "OUTPUT": OSM_PTstp_gpkg,
    }
    processing.run("native:extractbyexpression", params)


def OSMintersecGTFS(rectangles, OSMgpkg, tempOSMfolder, line):
    OSMlayer = QgsVectorLayer(OSMgpkg, "OSM" + str(line), "ogr")
    OSMintersecGTFSgpkg = os.path.join(
        tempOSMfolder, "OSMjoinGTFS" + str(line) + ".gpkg"
    )
    OSMnomatchGTFSgpkg = os.path.join(
        tempOSMfolder, "OSM" + str(line) + "_NOmatch.gpkg"
    )

    # adding coordinates in the attribute tables for the OSMlayer
    pr = OSMlayer.dataProvider()
    pr.addAttributes(
        [QgsField("lon", QVariant.Double), QgsField("lat", QVariant.Double)]
    )
    OSMlayer.updateFields()

    expression1 = QgsExpression("$x")
    expression2 = QgsExpression("$y")

    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(OSMlayer))

    with edit(OSMlayer):
        for f in OSMlayer.getFeatures():
            context.setFeature(f)
            f["lon"] = expression1.evaluate(context)
            f["lat"] = expression2.evaluate(context)
            OSMlayer.updateFeature(f)
    OSMlayer.commitChanges()

    # intersecating the GTFS rectangle and the OSM stop position
    params = {
        "INPUT": OSMlayer,
        "OVERLAY": QgsProcessingFeatureSourceDefinition(
            rectangles,
            selectedFeaturesOnly=False,
            featureLimit=-1,
            flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
            geometryCheck=QgsFeatureRequest.GeometrySkipInvalid,
        ),
        "INPUT_FIELDS": [
            "full_id",
            "osm_id",
            "lon",
            "lat",
            "osm_type",
            "local_ref",
            "level:ref",
            "ref",
            "old_name",
            "uic_ref",
            "uic_name",
            "public_transport",
            "operator",
        ],
        "OVERLAY_FIELDS": [
            "line_name",
            "trip",
            "pos",
            "stop_id",
            "stop_name",
            "stop_lon",
            "stop_lat",
            "parent_station",
            "prnt_stp_id",
            "stp_pltfrm",
            "route_short_name",
        ],
        "OVERLAY_FIELDS_PREFIX": "GTFS_",
        "OUTPUT": OSMintersecGTFSgpkg,
        "GRID_SIZE": None,
    }
    processing.run("native:intersection", params)

    del params

    params = {"INPUT": OSMlayer, "PREDICATE": [0], "INTERSECT": rectangles, "METHOD": 0}
    processing.run("native:selectbylocation", params)

    OSMlayer.invertSelection()

    vector_layer_to_gpkg(
        OSMlayer, "OSM" + str(line), OSMnomatchGTFSgpkg, seleted_features=True
    )

    # - saving tables CSV and loading
    OSMjoinGTFSlayer = QgsVectorLayer(
        OSMintersecGTFSgpkg, "OSMintersecGTFS" + str(line), "ogr"
    )
    OSMjoinGTFScsv = os.path.join(tempOSMfolder, "OSMjoinGTFS_" + str(line) + ".csv")
    vector_layer_to_csv(OSMjoinGTFSlayer, OSMjoinGTFScsv)

    OSMjnGTFS = pd.read_csv(
        OSMjoinGTFScsv, dtype={"GTFS_trip": int, "GTFS_pos": int, "GTFS_stop_id": str}
    )

    OSMnomatchGTFSlayer = QgsVectorLayer(
        OSMnomatchGTFSgpkg, "OSM" + str(line) + "_NOmatch", "ogr"
    )
    OSMnomatchGTFScsv = os.path.join(tempOSMfolder, "OSM" + str(line) + "_NOmatch.csv")
    vector_layer_to_csv(OSMnomatchGTFSlayer, OSMnomatchGTFScsv)

    OSMnomatch = pd.read_csv(OSMnomatchGTFScsv)
    del params
    return OSMjnGTFS, OSMnomatch, OSMjoinGTFScsv, OSMnomatchGTFScsv


def stp_posGTFSnm_rect(
    GTFSnm_rectCSV,
    line_name,
    splt_roads,
    temp_posRCT_folder,
    buses_long,
    tram_long,
    trnsprt_type,
    agency_txt,
    files_to_del,
):

    if (
        trnsprt_type == "Tram"
        or trnsprt_type == "RegRailServ"
        or trnsprt_type == "Funicular"
    ):
        trnsprt_long = tram_long
    else:
        trnsprt_long = buses_long

    GTFSnm_rect_path = correct_uri_for_windows(GTFSnm_rectCSV, "stop_lon", "stop_lat")

    GTFSnm_rect_layer = QgsVectorLayer(
        GTFSnm_rect_path, "GTFSNMrect_" + str(line_name), "delimitedtext"
    )

    GTFS_nmRCT_pos_CSV1 = os.path.join(
        temp_posRCT_folder, "GTFSnmRCT_pos_" + str(line_name) + "_1.csv"
    )

    GTFS_nmRCT_pos_CSV2 = os.path.join(
        temp_posRCT_folder, "GTFSnmRCT_pos_" + str(line_name) + "_2.csv"
    )

    GTFS_nmRCT_pos_CSV3 = os.path.join(
        temp_posRCT_folder, "GTFSnmRCT_pos_" + str(line_name) + "_3.csv"
    )

    GTFS_nmRCT_NEWpos_CSV = os.path.join(
        temp_posRCT_folder, "GTFSnmRCT_pos_" + str(line_name) + ".csv"
    )

    GTFS_pos1 = os.path.join(
        temp_posRCT_folder, "GTFSnmRCT_pos_" + str(line_name) + "_1.gpkg"
    )
    GTFS_pos = os.path.join(
        temp_posRCT_folder, "GTFSnmRCT_pos_" + str(line_name) + ".gpkg"
    )

    params = {
        "INPUT": GTFSnm_rect_layer,
        "INPUT_2": splt_roads,
        "FIELDS_TO_COPY": ["full_id", "osm_id", "osm_type", "name", "highway"],
        "DISCARD_NONMATCHING": True,
        "PREFIX": "nrstrd_",
        "NEIGHBORS": 1,
        "MAX_DISTANCE": 0.00015,
        "OUTPUT": GTFS_pos1,
    }
    processing.run("native:joinbynearest", params)

    GTFS_posangl = QgsVectorLayer(
        GTFS_pos1, "GTFSnmRCT_posangl_" + str(line_name), "ogr"
    )

    pr = GTFS_posangl.dataProvider()
    pr.addAttributes([QgsField("pos_angl", QVariant.Double)])
    GTFS_posangl.updateFields()

    expression1 = QgsExpression(
        'azimuth( make_point( "feature_x" ,  "feature_y" ), make_point( "nearest_x" ,  "nearest_y" ) )-1.570796327'
    )

    context = QgsExpressionContext()
    context.appendScopes(
        QgsExpressionContextUtils.globalProjectLayerScopes(GTFS_posangl)
    )

    with edit(GTFS_posangl):
        for f in GTFS_posangl.getFeatures():
            context.setFeature(f)
            f["pos_angl"] = expression1.evaluate(context)
            GTFS_posangl.updateFeature(f)
    GTFS_posangl.commitChanges()

    del context
    vector_layer_to_csv(GTFS_posangl, GTFS_nmRCT_pos_CSV1)

    # calculate the angle of the new stop_position
    # the QgsExpression function doesn't work with sin() function that works on the QGIS FieldCalculator
    GTFS_angldf = pd.read_csv(GTFS_nmRCT_pos_CSV1)
    posXY = trnsprt_long / 2
    GTFS_angldf["pos_x2"] = GTFS_angldf["stop_lon"] + posXY * np.sin(
        GTFS_angldf["pos_angl"]
    )
    GTFS_angldf["pos_y2"] = GTFS_angldf["stop_lat"] + posXY * np.cos(
        GTFS_angldf["pos_angl"]
    )

    agency = pd.read_csv(agency_txt)
    ls_agency = agency.agency_id.unique()
    i_row = 0
    while i_row < len(GTFS_angldf):
        if GTFS_angldf.loc[i_row, "distance"] < 0.00001 or not 881 in ls_agency:
            GTFS_angldf.loc[i_row, "pos_x2"] = GTFS_angldf.loc[i_row, "feature_x"]
            GTFS_angldf.loc[i_row, "pos_y2"] = GTFS_angldf.loc[i_row, "feature_y"]
        i_row += 1

    ls_to_delete = [
        "distance",
        "feature_x",
        "feature_y",
        "nearest_x",
        "nearest_y",
        "nrstrd_full_id",
        "nrstrd_osm_id",
        "nrstrd_osm_type",
        "nrstrd_name",
        "nrstrd_highway",
        "n",
    ]
    exist_cols = GTFS_angldf.columns
    ls_to_drop = [col for col in ls_to_delete if col in exist_cols]
    GTFS_angldf = GTFS_angldf.drop(ls_to_drop, axis=1)

    GTFS_angldf.to_csv(GTFS_nmRCT_pos_CSV2, index=False)

    GTFS_angl_pos_path = correct_uri_for_windows(
        GTFS_nmRCT_pos_CSV2, "pos_x2", "pos_y2"
    )

    GTFS_angl_pos = QgsVectorLayer(
        GTFS_angl_pos_path, "angl_pos_" + str(line_name), "delimitedtext"
    )

    params = {
        "INPUT": GTFS_angl_pos,
        "INPUT_2": splt_roads,
        "FIELDS_TO_COPY": ["full_id", "osm_id", "osm_type", "name", "highway"],
        "DISCARD_NONMATCHING": True,
        "PREFIX": "nrstrd_",
        "NEIGHBORS": 1,
        "MAX_DISTANCE": 0.00015,
        "OUTPUT": GTFS_pos,
    }
    processing.run("native:joinbynearest", params)

    GTFS_pos_layer = QgsVectorLayer(GTFS_pos, "GTFSnmRCT_" + str(line_name), "ogr")
    vector_layer_to_csv(GTFS_pos_layer, GTFS_nmRCT_pos_CSV3)

    GTFS_posdf = pd.read_csv(GTFS_nmRCT_pos_CSV3)

    ls_to_delete = ["distance", "feature_x", "feature_y", "pos_x2", "pos_y2"]
    exist_cols = GTFS_posdf.columns
    ls_to_drop = [col for col in ls_to_delete if col in exist_cols]
    GTFS_posdf = GTFS_posdf.drop(ls_to_drop, axis=1)
    GTFS_posdf = GTFS_posdf.rename(columns={"nearest_x": "lon", "nearest_y": "lat"})

    GTFS_posdf.to_csv(GTFS_nmRCT_NEWpos_CSV, index=False)

    files_to_del = if_remove(GTFS_nmRCT_pos_CSV1, files_to_del)
    files_to_del = if_remove(GTFS_nmRCT_pos_CSV2, files_to_del)
    files_to_del = if_remove(GTFS_nmRCT_pos_CSV3, files_to_del)
    files_to_del = if_remove(GTFS_pos1, files_to_del)

    return GTFS_nmRCT_NEWpos_CSV, files_to_del


def joinNEWandValidOSM(
    newOSMpos,
    GTFSnomatch_RD,
    OSMintersectGTFS,
    GTFSstps_seg,
    temp_OSM_for_routing,
    line,
    stops_txt,
    files_to_del,
):

    GTFSnm = pd.read_csv(
        GTFSnomatch_RD, dtype={"trip": int, "pos": int, "stop_id": str}
    )
    validOSM = pd.read_csv(OSMintersectGTFS)
    GTFSss = pd.read_csv(GTFSstps_seg)
    OSMstops_unsorted = pd.DataFrame()

    if os.path.exists(newOSMpos):
        newOSM = pd.read_csv(newOSMpos, dtype={"trip": int, "pos": int, "stop_id": str})
        newOSM = newOSM[["stop_id", "line_name", "trip", "pos", "lon", "lat"]]
        newOSM["loc_base"] = "generated from GTFS on OSM roads"
        newOSM = newOSM.rename(columns={"stop_id": "GTFS_stop_id"})
        OSMstops_unsorted = pd.concat([OSMstops_unsorted, newOSM], ignore_index=True)

    if not GTFSnm.empty:
        GTFSnm = GTFSnm[["stop_id", "line_name", "trip", "pos", "stop_lon", "stop_lat"]]
        GTFSnm["loc_base"] = "GTFS points"
        GTFSnm = GTFSnm.rename(
            columns={"stop_id": "GTFS_stop_id", "stop_lat": "lat", "stop_lon": "lon"}
        )
        OSMstops_unsorted = pd.concat([OSMstops_unsorted, GTFSnm], ignore_index=True)

    if not validOSM.empty:
        validOSM = validOSM[
            ["GTFS_stop_id", "GTFS_line_name", "GTFS_trip", "GTFS_pos", "lon", "lat"]
        ]
        validOSM["loc_base"] = "already present on OSM"
        validOSM = validOSM.rename(
            columns={
                "GTFS_trip": "trip",
                "GTFS_pos": "pos",
                "GTFS_line_name": "line_name",
            }
        )
        OSMstops_unsorted = pd.concat([OSMstops_unsorted, validOSM], ignore_index=True)

    OSMstops_updated = OSMstops_unsorted.sort_values(["trip", "pos"]).reset_index(
        drop=True
    )

    # if there is more than one stop in OSM per GTFS
    # few lines later the closer OSM is taken !!!
    i_row = 0
    while i_row < len(OSMstops_updated):
        OSMstops_updated.loc[i_row, "line_trip"] = (
            str(OSMstops_updated.loc[i_row, "line_name"])
            + "_trip"
            + str(OSMstops_updated.loc[i_row, "trip"])
        )
        i_row += 1
    ls_trips = OSMstops_updated.line_trip.unique()

    stops = pd.read_csv(stops_txt, dtype={"stop_id": str})
    OSMstops_updated = OSMstops_updated.astype({"GTFS_stop_id": "str"})
    stops = stops[["stop_id", "stop_lon", "stop_lat"]]
    OSMstops_updated = OSMstops_updated.merge(
        stops, how="left", left_on="GTFS_stop_id", right_on="stop_id"
    )

    # in case there is more than one OSM stop for an GTFS,
    # the farest is deleted
    todelete = []
    i_row = 0
    i_row2 = 1
    while i_row2 < len(OSMstops_updated):
        if OSMstops_updated.loc[i_row, "pos"] == OSMstops_updated.loc[i_row2, "pos"]:
            dist1 = math.sqrt(
                (
                    (
                        OSMstops_updated.loc[i_row, "lon"]
                        - OSMstops_updated.loc[i_row, "stop_lon"]
                    )
                    ** 2
                )
                + (
                    (
                        OSMstops_updated.loc[i_row, "lat"]
                        - OSMstops_updated.loc[i_row, "stop_lat"]
                    )
                    ** 2
                )
            )
            dist2 = math.sqrt(
                (
                    (
                        OSMstops_updated.loc[i_row2, "lon"]
                        - OSMstops_updated.loc[i_row2, "stop_lon"]
                    )
                    ** 2
                )
                + (
                    (
                        OSMstops_updated.loc[i_row2, "lat"]
                        - OSMstops_updated.loc[i_row2, "stop_lat"]
                    )
                    ** 2
                )
            )
            if dist1 < dist2:
                todelete.append(i_row2)
            else:
                todelete.append(i_row)
        i_row += 1
        i_row2 += 1

    OSMstops_tosave = OSMstops_updated.drop(todelete).reset_index(drop=True)

    OSMstops_tosave = OSMstops_tosave.drop(["stop_lon", "stop_lat"], axis=1)
    for line_trip in ls_trips:
        OSMstops_trip = OSMstops_tosave[OSMstops_tosave["line_trip"] == line_trip]
        OSMstops_trip_name = "OSM4routing_" + line_trip
        OSMstops_trip_csv = os.path.join(
            temp_OSM_for_routing, OSMstops_trip_name + ".csv"
        )

        OSMstops_trip_gpkg = os.path.join(
            temp_OSM_for_routing, OSMstops_trip_name + ".gpkg"
        )

        OSMstops_trip.to_csv(OSMstops_trip_csv, index=False)
        OSM4rout_path = correct_uri_for_windows(
            OSMstops_trip_csv, "lon", "lat", additional_args={"field": "trip:integer"}
        )

        OSM4rout_layer = QgsVectorLayer(
            OSM4rout_path, OSMstops_trip_name, "delimitedtext"
        )
        vector_layer_to_gpkg(OSM4rout_layer, OSMstops_trip_name, OSMstops_trip_gpkg)

        files_to_del = if_remove(OSMstops_trip_csv, files_to_del)
    return files_to_del


# to attach at the end of the stops correctly visualized on the map
# to finish


def display_vector_layer(OSMcheckedstops_layer):
    QgsProject.instance().addMapLayer(OSMcheckedstops_layer)


def zoom_to_layer(OSMcheckedsotps_layer):
    canvas = iface.mapCanvas()
    extent = OSMcheckedsotps_layer.extent()
    canvas.setExtent(extent)
    canvas.refresh()


def transcript_main_files(
    main_files_fld,
    main_files_csv,
    OSM_ways_name,
    OSM_ways_gpkg,
    OSM_roads_name,
    OSM_roads_gpkg,
    OSM_roads_nameCSV,
    OSM_roads_csv,
    highway_speed_name,
    highway_speed_csv,
    bus_lanes_name,
    OSM_bus_lanes_gpkg,
    OSM_bus_lanes_csv,
    full_roads_name,
    full_roads_gpgk,
    Ttbls_selected_name,
    Ttbls_selected_txt,
    files_to_delete_next_bus_loading_name,
    files_to_delete_next_bus_loading_json,
):
    main_files_dict = {
        "name": [
            OSM_ways_name,
            OSM_roads_name,
            OSM_roads_nameCSV,
            highway_speed_name,
            bus_lanes_name,
            bus_lanes_name + "_csv",
            full_roads_name,
            Ttbls_selected_name,
            files_to_delete_next_bus_loading_name,
        ],
        "path": [
            OSM_ways_gpkg,
            OSM_roads_gpkg,
            OSM_roads_csv,
            highway_speed_csv,
            OSM_bus_lanes_gpkg,
            OSM_bus_lanes_csv,
            full_roads_gpgk,
            Ttbls_selected_txt,
            files_to_delete_next_bus_loading_json,
        ],
    }
    main_files = pd.DataFrame(main_files_dict)
    os.makedirs(main_files_fld)
    main_files.to_csv(main_files_csv, index=False)


def display_OSM_and_SWISSTOPO_IMAGE_maps():
    if not QgsProject.instance().mapLayersByName("SWISSIMAGE 10 cm"):
        uri = "contextualWMSLegend=0&crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/jpeg&layers=ch.swisstopo.swissimage&styles=default&tilePixelRatio=0&url=https://wms.geo.admin.ch/"
        CHimage_layer = QgsRasterLayer(uri, "SWISSIMAGE 10 cm", "wms")
        QgsProject.instance().addMapLayer(CHimage_layer)

    if not QgsProject.instance().mapLayersByName("OSM Standard"):
        uri = (
            "type=xyz&zmin=0&zmax=19&url=http://tile.openstreetmap.org/{z}/{x}/{y}.png"
        )
        OSMmap_layer = QgsRasterLayer(uri, "OSM Standard", "wms")
        QgsProject.instance().addMapLayer(OSMmap_layer)


def if_display_r_layer(
    file_path,
    layer_name,
):
    if os.path.exists(file_path):
        if not QgsProject.instance().mapLayersByName(layer_name):
            city_r_layer = QgsVectorLayer(file_path, layer_name, "ogr")
            symbol = city_r_layer.renderer().symbol()
            symbol.setWidth(0.35)
            QgsProject.instance().addMapLayer(city_r_layer)


def display_all_OSM4routing_trips_stops(
    temp_OSM_for_routing, ls_buses_selected, lines_df
):
    ls_buses_todisp = [str(bus) for bus in ls_buses_selected]
    ls_buses_select_df = pd.DataFrame(ls_buses_todisp).rename(
        columns={0: "trnsp_shrt_name"}
    )
    ls_buses_select_df = ls_buses_select_df.astype({"trnsp_shrt_name": "str"})
    ls_buses_select_df = ls_buses_select_df.merge(
        lines_df, how="left", on="trnsp_shrt_name"
    )
    ls_trnsprt_todisplay = list(ls_buses_select_df.line_name.unique())
    ls_files = os.listdir(temp_OSM_for_routing)
    ls_with_gpkg = [file for file in ls_files if ".gpkg" in file]
    ls_gpkg = [file for file in ls_with_gpkg if "shm" not in file and "wal" not in file]

    for trnsprt in ls_trnsprt_todisplay:
        to_display = [str(gpkg) for gpkg in ls_gpkg if trnsprt in gpkg]
        for layer in to_display:
            if not QgsProject.instance().mapLayersByName(str(layer[:-5])):
                OSM_trip4rout_gpkg = os.path.join(temp_OSM_for_routing, str(layer))
                OSM_trip4rout_layer = QgsVectorLayer(
                    OSM_trip4rout_gpkg, str(layer[:-5]), "ogr"
                )
                QgsProject.instance().addMapLayer(OSM_trip4rout_layer)
