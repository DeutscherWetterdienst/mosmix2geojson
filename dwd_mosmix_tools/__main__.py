#!/usr/bin/env python3
import json
import sys

from dwd_mosmix_tools.kml2json import kml2geojson

if __name__ == "__main__":
    max_stations = 7
    geojson = kml2geojson("../data/MOSMIX_L_2022061021.kml", max_stations)
    json.dump(geojson, sys.stdout, indent=2)
