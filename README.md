# mosmix2geojson

This code was DWD's contribution to the #vismethack on June 2022 at ECMWF.

This repo offers a way to convert DWD MOSMIX data to geoJSON. Possible uses after conversion include visualization of
this global point data with [skinnyWMS](https://github.com/ecmwf/skinnywms).

MOSMIX data is generated from model output statistics. DWD MOSMIX data is published on DWD open data at
https://opendata.dwd.de/weather/local_forecasts/mos/. MOSMIX_L contains a large selection of parameters; MOSMIX_S contains a smaller selection of parameters.

The chosen KMZ format is a zipped KML, which contains MOSMIX data in a
[special format](https://www.dwd.de/DE/leistungen/opendata/hilfe.html?nn=16102#doc625266bodyText5).


This software is intended to be used with [DWD's MOSMIX data](https://dwd-geoportal.de/products/G_FJM/).

## Installation
Run `pip install git+https://github.com/DeutscherWetterdienst/mosmix2geojson.git@v1.0.0#egg=mosmix2geojson` (preferably
in a virtual env) to install the latest version of the Python package along with it's CLI.

## Step-by-step example usage
This is an example step-by-step usage. The [latest MOSMIX_L data from opendata.dwd.de](https://opendata.dwd.de/weather/local_forecasts/mos/MOSMIX_L/all_stations/kml/MOSMIX_L_LATEST.kmz)
is downloaded to the working directory and converted to GeoJSON.

* `wget https://opendata.dwd.de/weather/local_forecasts/mos/MOSMIX_L/all_stations/kml/MOSMIX_L_LATEST.kmz`
* `unzip MOSMIX_L_LATEST.kmz`
* `mosmix2geojson --max-stations 2 --json-indent 2 MOSMIX_L_*.kml > mosmix-l.geojson`

This will stop after a maximum of 2 MOSMIX stations, which is just to reduce processing time for demo purposes.

## Output mapping

The output uses MOSMIX parameter names by default. This can be changed by mapping the output with an integrated or a
custom mapping file. Use the option `--map-to-cf` to map the output to CF standard names (or to a human-readable name if
no CF standard name exists for this parameter). Alternatively, a custom mapping can be applied via
`--mapping-file MAPPING_FILE`.

When a mapping of any kind is applied, any unmapped parameters will be excluded from the output by default. Beware that
`--map-to-cf` is currently incomplete and will therefore lack many MOSMIX parameters. Combine any mapping with
`--keep-unmapped` to include any unmapped parameters with their original MOSMIX names in the output. Use this feature
at your own risk as the combination of `--map-to-cf` and `--keep-unmapped` will lead to broken code when we extend this
mapping in the future releases.

## Advanced usage
```
usage: mosmix2geojson [-h] [--map-to-cf | -m MAPPING_FILE] [-k] [--export-cf-mapping] [-x MAX_STATIONS] [-i JSON_INDENT] [-v] [SOURCE] [TARGET]

Convert DWD MOSMIX data to GeoJSON.

positional arguments:
  SOURCE                source KML file, - for stdin (default: stdin)
  TARGET                target JSON file, - for stdout (default: stdout)

optional arguments:
  -h, --help            show this help message and exit
  -x MAX_STATIONS, --max-stations MAX_STATIONS
                        number of stations to be processed (default: all stations)
  -i JSON_INDENT, --json-indent JSON_INDENT
                        indentation blanks for json (default: no indentation)
  -v, --version         show program's version number and exit

mapping arguments:
  Transform the output with mapped parameters. When a mapping of any kind is applied, unmapped parameters will not be included by default. Change this behaviour with the --keep-unmapped flag. Use this feature at your own risk.

  --map-to-cf           produce output with CF standard names or another human readable name where no CF standard name exists
  -m MAPPING_FILE, --mapping-file MAPPING_FILE
                        apply a custom mapping to the output
  -k, --keep-unmapped   include unmapped parameters in output
  --export-cf-mapping   print the mapping configuration used by --map-to-cf and exit
```

## Develop

1. Clone this repo.
2. Create a Python virtualenv, e.g. `python3 -m venv venv`
3. Perform an editable installation of the package with dev extras, i.e. `pip install -e .[dev]`

Now you can use the CLI interface with your latest changes. To create a new tagged version, commit your changes and then
run `bump2version major|minor|patch` to automatically do the following:
* calculate the new version string
* update it in all the relevant files (as specified in `.bumpversion.cfg`)
* commit the changed files and tag the commit with a suitable version tag
