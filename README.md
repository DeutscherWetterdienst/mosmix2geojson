# SunnyPoints
June 2022 ECMWF #vismethack DWD MOSMIX kmz to geoJSON converter

This repo offers a way to convert DWD MOSMIX data to geoJSON, using the CF naming scheme. Possible uses after conversion include visualization of this global point data with [skinnyWMS](https://github.com/ecmwf/skinnywms).

MOSMIX data is generated from model output statistics. DWD MOSMIX data is published on DWD open data at https://opendata.dwd.de/weather/local_forecasts/mos/. MOSMIX_L contains a large selection of parameters; MOSMIX_S contains a smaller selection of parameters.

The chosen KMZ format is a zipped KML, which contains MOSMIX data in a [special format](https://www.dwd.de/DE/leistungen/opendata/hilfe.html?nn=16102#doc625266bodyText5).


This software is intended to be used with [DWD's MOSMIX data](https://dwd-geoportal.de/products/G_FJM/).

## Step-by-step example usage
This is an example step-by-step usage. The [latest MOSMIX_L data from opendata.dwd.de](https://opendata.dwd.de/weather/local_forecasts/mos/MOSMIX_L/all_stations/kml/MOSMIX_L_LATEST.kmz)
is downloaded to the working directory and converted to GeoJSON.

* (run all commands from project root)
* `wget https://opendata.dwd.de/weather/local_forecasts/mos/MOSMIX_L/all_stations/kml/MOSMIX_L_LATEST.kmz`
* `unzip MOSMIX_L_LATEST.kmz`
* `python3 -m dwd_mosmix_tools --max-stations 2 --json-indent 2 MOSMIX_L_*.kml > mosmix-l.geojson`

This will stop after a maximum of 2 MOSMIX stations, which is just to reduce processing time for demo purposes. A file
`example_parameter_mapping.json` is included, which renames and rescales some parameters to the CF conventions.
You can apply the mapping by adding the option `--mapfile example_parameter_mapping.json` to the command.

## Advanced usage
```
usage: python3 -m dwd_mosmix_tools [-h] [--mapfile MAPFILE] [--max-stations MAX_STATIONS] [--json-indent JSON_INDENT] file

Convert unzipped DWD MOSMIX KML file to geoJSON file.

positional arguments:
  file                  KML file name

optional arguments:
  -h, --help            show this help message and exit
  --mapfile MAPFILE     JSON mapping file from DWD KML to geoJSON
  --max-stations MAX_STATIONS
                        number of stations to be processed
  --json-indent JSON_INDENT
                        indentation blanks for json
```
