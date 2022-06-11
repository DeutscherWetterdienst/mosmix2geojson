SHELL:=/bin/bash


.PHONY: download-test-data
download-test-data:
	mkdir -p data/
	wget -P data/ https://opendata.dwd.de/weather/local_forecasts/mos/MOSMIX_L/all_stations/kml/MOSMIX_L_2022061109.kmz
	wget -P data/ https://opendata.dwd.de/weather/local_forecasts/mos/MOSMIX_L/all_stations/kml/MOSMIX_L_2022061103.kmz
	wget -P data/ https://opendata.dwd.de/weather/local_forecasts/mos/MOSMIX_L/all_stations/kml/MOSMIX_L_2022061021.kmz


.PHONY: extract-test-data
extract-test-data:
	unzip -d data/ data/*.kmz
