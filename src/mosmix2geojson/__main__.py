#!/usr/bin/env python3
import argparse
import json
import sys
from importlib import resources

from mosmix2geojson.kml2json import kml2geojson
from mosmix2geojson import __version__

# define parser for argparse
# dwdkml2geojson --max-stations 7 --jsonindent 2 file.kml > file.geojson
argparser = argparse.ArgumentParser(description='Convert DWD MOSMIX data to GeoJSON.')

# define arguments
argparser.add_argument('file',
                       metavar='FILE',
                       type=str,
                       nargs="?",
                       help='KML file (default: STDIN)')

mapping_group = argparser.add_argument_group("mapping arguments",
                                             description="Transform the output with mapped parameters. "
                                                         "When a mapping of any kind is applied, unmapped parameters "
                                                         "will not be included by default. Change this behaviour with "
                                                         "the --keep-unmapped flag. Use this feature at your own risk.")

mapping_file_arg = mapping_group.add_mutually_exclusive_group()

mapping_file_arg.add_argument('-cf', '--map-to-cf',
                              action='store_const',
                              const='cf',
                              help='produce output with CF standard names or another human readable name where no CF standard name exists',
                              dest="integrated_mapping")

mapping_file_arg.add_argument('-m', '--mapping-file',
                              type=str,
                              help='apply a custom mapping to the output')

mapping_group.add_argument('-k', '--keep-unmapped',
                           action='store_true',
                           help='include unmapped parameters in output')

mapping_group.add_argument('-e-cf', '--export-cf-mapping',
                           action='store_const',
                           const='cf',
                           help='print the mapping configuration used by --map-to-cf and exit',
                           dest='export_mapping')

argparser.add_argument('-x', '--max-stations',
                       type=int,
                       help='number of stations to be processed (default: all stations)')

argparser.add_argument('-i', '--json-indent',
                       type=int,
                       help='indentation blanks for json (default: no indentation)')

argparser.add_argument('-v', '--version', action='version', version=__version__)


def main():
    args = argparser.parse_args()

    export_mapping = args.export_mapping
    if export_mapping:
        with resources.open_text("mosmix2geojson", f"{export_mapping}.mapping.json") as fp:
            for line in fp:
                print(line, end="")
        return

    file = args.file
    if file is None:
        file = sys.stdin
    json_indent = args.json_indent
    max_stations = args.max_stations

    param_mapping = None
    integraded_mapping = args.integrated_mapping
    mapping_file = args.mapping_file
    if integraded_mapping:
        with resources.open_text("mosmix2geojson", f"{integraded_mapping}.mapping.json") as fp:
            param_mapping = json.load(fp)
    elif mapping_file:
        with open(mapping_file) as fp:
            param_mapping = json.load(fp)

    geojson = kml2geojson(file, param_mapping=param_mapping, max_stations=max_stations,
                          keep_unmapped=args.keep_unmapped)

    json.dump(geojson, sys.stdout, indent=json_indent)


if __name__ == "__main__":
    main()
