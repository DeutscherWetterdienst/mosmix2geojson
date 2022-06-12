#!/usr/bin/env python3
from doctest import testfile
import json
from lib2to3.pgen2.token import INDENT
import sys
import argparse

from dwd_mosmix_tools.kml2json import kml2geojson

if __name__ == "__main__":

  # define parser for argparse
  # dwdkml2geojson --max-stations 7 --jsonindent 2 file.kml > file.geojson
  argparser = argparse.ArgumentParser(prog='python3 -m dwd_mosmix_tools',
                                      description='Convert unzipped DWD MOSMIX KML file to geoJSON file, using the CF naming convention where possible')

  # define arguments
  argparser.add_argument('File',
                         metavar='file',
                         type=str,
                         help='KML file name')

  argparser.add_argument('--mapfile',
                         type=str,
                         help='JSON mapping file from DWD KML to geoJSON')

  argparser.add_argument('--max_stations',
                         type=int,
                         help='number of stations to be processed')

  argparser.add_argument('--json_indent',
                         type=int,
                         help='indentation blanks for json')


  args = argparser.parse_args()

  testfile   = args.File
  json_indent = args.json_indent
  mapfile    = args.mapfile
  max_stations = args.max_stations

  # todo:
  # hand over list of stations to be plotted
  # hand over json file contents as dict instead of path

  geojson = kml2geojson(testfile, max_stations)

  json.dump(geojson, sys.stdout, indent=json_indent)

