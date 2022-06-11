#!/usr/bin/env python3

import json
import os
import xml.etree.ElementTree as ET
from importlib_resources import open_text
from typing import Iterator, Tuple, Union, IO, Optional
from xml.etree.ElementTree import Element


with open_text("dwd_mosmix_tools", "parameter_shortnames.json") as file:
    MAPPING = json.load(file)


def map_shortname(mosmix_shortname):
    return MAPPING.get(mosmix_shortname, {"name": mosmix_shortname})


def iterparse(*args) -> Iterator[Tuple[str, Element]]:
    return ET.iterparse(*args)


def strip_ns(string):
    return string[string.find("}") + 1:]


def get_tag_without_ns(element: Element):
    return strip_ns(element.tag)


def get_attrs_without_ns(element: Element):
    return {strip_ns(key): value for key, value in element.attrib.items()}

# todo: extract from KML
default_undef_sign = "-"
time_steps = []


def process_time_step(event, element):
    global time_steps
    # only process "end" events
    if event == "end":
        time_steps.append(element.text.strip())


forecasts = {}
current_value = None

current_station = None
def process_forecast(event, element):
    global forecasts
    global current_station
    # only process "end" events
    if event == "end":
        mosmix_shortname = get_attrs_without_ns(element)["elementName"]
        json_shortname = map_shortname(mosmix_shortname)["name"]
        forecasts[json_shortname] = current_value


def process_value(event, element):
    global current_value
    if event == "end":
        current_value = [float(value) if value != default_undef_sign else None
                         for value in element.text.split()]


number_of_processed_placemarks = 0
features = []
def process_placemark(event, element):
    global number_of_processed_placemarks
    if event == "end":
        timeseries = []
        for ix, time in enumerate(time_steps):
            timeseries.append({
                "time": time,
                **{short_name: values[ix] for short_name, values in forecasts.items() if values[ix] is not None},
            })

        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [8.9, 50.7],
            },
            "properties": {
                "name": current_station_name,
                "stationId": current_station_id,
                "timeseries": timeseries,
            },
        })

        number_of_processed_placemarks += 1


current_station_id = None
def process_name(event, element):
    global current_station_id
    if event == "end":
        current_station_id = element.text


current_station_name = None
def process_description(event, element):
    global current_station_name
    if event == "end":
        current_station_name = element.text


def kml2geojson(source: Union[str, bytes, os.PathLike, IO], max_stations: Optional[int] = None):
    for event, element in iterparse(source, ["start", "end"]):
        tag_name = get_tag_without_ns(element)
        if tag_name == "TimeStep":
            process_time_step(event, element)
        elif tag_name == "name":
            process_name(event, element)
        elif tag_name == "description":
            process_description(event, element)
        elif tag_name == "Forecast":
            process_forecast(event, element)
        elif tag_name == "value":
            process_value(event, element)
        elif tag_name == "Placemark":
            process_placemark(event, element)
        if number_of_processed_placemarks >= max_stations:
            break


    featureCollection = {
        "type": "FeatureCollection",
        "features": features,
    }
    return featureCollection
