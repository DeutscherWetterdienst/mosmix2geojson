# vismethack
June 2022 ECMWF #vismethack DWD MOSMIX kmz to geoJSON converter

This repo offers a way to convert DWD MOSMIX data to geoJSON, using the CF naming scheme. Possible uses after conversion include visualization of this global point data with skinnyWMS.

MOSMIX data is generated from model output statistics. DWD MOSMIX data is published on DWD open data at https://opendata.dwd.de/weather/local_forecasts/mos/. MOSMIX_L contains a large selection of parameters; MOSMIX_S contains a smaller selection of parameters.

The chosen KMZ format is a zipped KML, which contains MOSMIX data in the following format:
https://www.dwd.de/DE/leistungen/opendata/hilfe.html?nn=16102#doc625266bodyText5


This repo has been tested with the following datasets:
https://opendata.dwd.de/weather/local_forecasts/mos/MOSMIX_L/all_stations/kml/MOSMIX_L_2022061109.kmz
https://opendata.dwd.de/weather/local_forecasts/mos/MOSMIX_L/all_stations/kml/MOSMIX_L_2022061103.kmz
https://opendata.dwd.de/weather/local_forecasts/mos/MOSMIX_L/all_stations/kml/MOSMIX_L_2022061021.kmz