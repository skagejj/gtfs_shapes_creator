from .resources import *

import os.path

import pandas as pd
from collections import defaultdict
import os

from pathlib import Path


def update_agences(gtfs_folder_path):
    agency = pd.read_csv(str(gtfs_folder_path) + "/agency.txt", dtype="str")
    agency["id_name"] = (
        agency["agency_id"].astype(str).fillna("")
        + " - "
        + agency["agency_name"].astype(str).fillna("")
    )

    agency = agency.sort_values(by="agency_name")
    ls_agency = agency.id_name.unique()
    return ls_agency


def check_gtfs_folder(gtfs_folder_path):
    ls_gtfs_files = [
        "agency.txt",
        "routes.txt",
        "trips.txt",
        "stops.txt",
        "stop_times.txt",
    ]
    ls_missing = []
    for file in ls_gtfs_files:
        file_path = os.path.join(gtfs_folder_path, file)
        if not os.path.exists(file_path):
            ls_missing.append(file)
    if len(ls_missing) > 0:
        if len(ls_missing) == len(ls_gtfs_files):
            raise TypeError(
                "It's not the GTFS folder, make sure you unziped the GTFS file"
            )
        else:
            raise TypeError(
                f"Something wrong with your GTFS folder {ls_missing} are missing! in the {gtfs_folder_path}"
            )


def get_agecy_s_routes(ls_agencies_selected, gtfs_folder_path):

    print("you selected:")
    for agen in ls_agencies_selected:
        print(agen)
    agencies_num = [agen.split(" - ")[0] for agen in ls_agencies_selected]
    agencies_folder = "agen"
    agencies_num = [agen.split(" - ")[0] for agen in ls_agencies_selected]
    for agen in agencies_num:
        agencies_folder = str(agencies_folder) + "_" + str(agen)

    routes_txt = str(gtfs_folder_path) + "/routes.txt"
    routes = pd.read_csv(routes_txt, dtype="str")

    agency_routes = routes[routes.agency_id.isin(agencies_num)]

    return agency_routes, agencies_folder


def generate_agencies_gtfs(gtfs_folder_path, selected_agencies, count_all_agencies):

    ls_agencies_selected = [item.text() for item in selected_agencies]
    if len(selected_agencies) == count_all_agencies:
        agencies_folder = str(Path(gtfs_folder_path))
        gtfs_folder_path = str(Path(gtfs_folder_path).parent.absolute())
    else:
        agen_folder = "agen"
        agencies_num = [agen.split(" - ")[0] for agen in ls_agencies_selected]
        for agen in agencies_num:
            agen_folder = str(agen_folder) + "_" + str(agen)
        agencies_folder = os.path.join(gtfs_folder_path, agen_folder)

        if not os.path.exists(agencies_folder):
            create_agecies_gtfs(agen_folder, agencies_num, gtfs_folder_path)

    outputspath = os.path.join(agencies_folder, "outputs")
    os.makedirs(outputspath, exist_ok=True)
    return agencies_folder, outputspath


def create_agecies_gtfs(agen_folder, agencies_num, gtfs_folder_path):

    agency_txt = str(gtfs_folder_path) + "/agency.txt"
    routes_txt = str(gtfs_folder_path) + "/routes.txt"
    trips_txt = str(gtfs_folder_path) + "/trips.txt"
    stop_times_txt = str(gtfs_folder_path) + "/stop_times.txt"
    stops_txt = str(gtfs_folder_path) + "/stops.txt"
    calendar_txt = str(gtfs_folder_path) + "/calendar.txt"
    calendar_dates_txt = str(gtfs_folder_path) + "/calendar_dates.txt"

    agency = pd.read_csv(agency_txt, dtype={"agency_id": "str"})
    routes = pd.read_csv(routes_txt, dtype="str")
    trips = pd.read_csv(trips_txt, dtype="str")
    types = defaultdict(lambda: str, stop_sequence="int")
    stop_times = pd.read_csv(stop_times_txt, dtype=types)
    types = defaultdict(lambda: str, stop_lon="float", stop_lat="float")
    stops = pd.read_csv(stops_txt, dtype=types)
    calendar = pd.read_csv(calendar_txt, dtype="str")
    calendar_dates = pd.read_csv(calendar_dates_txt, dtype="str")

    agency_fld = os.path.join(gtfs_folder_path, agen_folder)

    os.makedirs(agency_fld, exist_ok=True)

    agency_select = pd.DataFrame()

    for agen in agencies_num:
        agencies = agency[agency["agency_id"] == agen]
        agency_select = pd.concat([agency_select, agencies], ignore_index=True)

    agency_select.to_csv(str(agency_fld) + "/agency.txt", index=False)

    agency_routes = routes[routes.agency_id.isin(agencies_num)]
    trnsprt_correspondant = {
        "T": "Tram",
        "B": "Bus",
        "R": "RegRailServ",
        "FUN": "Funicular",
    }
    agency_routes["trnsprt"] = (
        agency_routes["route_desc"].map(trnsprt_correspondant).fillna("trnsprt")
    )
    agency_routes["trnsp_shrt_name"] = (
        agency_routes["trnsprt"].astype(str)
        + "_"
        + agency_routes["route_short_name"].astype(str)
    )
    agency_routes.to_csv(str(agency_fld) + "/routes.txt", index=False)

    ls_routes = agency_routes.route_id.unique()
    trips_agency = trips[trips.route_id.isin(ls_routes)]
    trips_agency.to_csv(str(agency_fld) + "/trips.txt", index=False)

    ls_trips = trips_agency.trip_id.unique()
    agency_stop_times = stop_times[stop_times.trip_id.isin(ls_trips)]
    agency_stop_times.to_csv(str(agency_fld) + "/stop_times.txt", index=False)

    ls_stops = agency_stop_times.stop_id.unique()
    agency_stops = stops[stops.stop_id.isin(ls_stops)]
    agency_stops.to_csv(str(agency_fld) + "/stops.txt", index=False)

    ls_service = trips_agency.service_id.unique()

    agency_calendar = calendar[calendar.service_id.isin(ls_service)]
    agency_calendar.to_csv(str(agency_fld) + "/calendar.txt")

    agency_calendar_dates = calendar_dates[calendar_dates.service_id.isin(ls_service)]
    agency_calendar_dates.to_csv(str(agency_fld) + "/calendar_dates.txt")
