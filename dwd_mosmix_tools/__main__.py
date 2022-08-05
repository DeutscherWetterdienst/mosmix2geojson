#!/usr/bin/env python3
import argparse
import json
import sys

from dwd_mosmix_tools.kml2json import kml2geojson
from dwd_mosmix_tools import __version__

# define parser for argparse
# dwdkml2geojson --max-stations 7 --jsonindent 2 file.kml > file.geojson
argparser = argparse.ArgumentParser(description='Convert DWD MOSMIX data to GeoJSON.')

# define arguments
argparser.add_argument('file',
                       metavar='FILE',
                       type=str,
                       help='KML file name')

argparser.add_argument('--mapfile',
                       type=str,
                       help='JSON mapping file from DWD KML to geoJSON')

argparser.add_argument('--max-stations',
                       type=int,
                       help='number of stations to be processed')

argparser.add_argument('--json-indent',
                       type=int,
                       help='indentation blanks for json')

argparser.add_argument('-v', '--version', action='version', version=__version__)


def main():
    args = argparser.parse_args()

    file = args.file
    json_indent = args.json_indent
    mapfile = args.mapfile
    max_stations = args.max_stations

    # todo: hand over list of stations to be plotted

    param_mapping = None
    if mapfile:
        with open(mapfile) as fp:
            param_mapping = json.load(fp)

    geojson = kml2geojson(file, param_mapping=param_mapping, max_stations=max_stations)

    json.dump(geojson, sys.stdout, indent=json_indent)


if __name__ == "__main__":
    main()
