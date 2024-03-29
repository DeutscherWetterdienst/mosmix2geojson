#!/usr/bin/env python3

import os
import xml.etree.ElementTree as ET
from typing import Iterator, Tuple, Union, IO, Optional
from xml.etree.ElementTree import Element


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
current_value: Optional[list] = None

current_station: Optional[list] = None


def scale_values(values, factor):
    if factor is None or factor == 1 or factor == 1.:
        return values
    return [value*factor if value is not None else None for value in values]


def process_forecast(event, element, params_metadata: Optional[dict] = None, param_list: Optional[list] = None, keep_unmapped=False):
    global forecasts
    global current_station
    # only process "end" events
    if event == "end":
        shortname = get_attrs_without_ns(element)["elementName"]
        if params_metadata is not None:
            if keep_unmapped:
                param = params_metadata.get(shortname, {"name": shortname})
            else:
                param = params_metadata[shortname]
        else:
            param = {"name": shortname}
        if param_list is not None and param["name"] not in param_list:
            return
        forecasts[param["name"]] = scale_values(current_value, param.get("scalefactor"))


def process_value(event, element):
    global current_value
    if event == "end":
        current_value = [float(value) if value != default_undef_sign else None
                         for value in element.text.split()]

current_coordinates: Optional[list] = None
def process_coordinates(event, element):
    global current_coordinates
    if event == "end":
        # lon, lat, elevation
        current_coordinates = [float(value) for value in element.text.split(",")]

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
                "coordinates": current_coordinates[:2],
            },
            "properties": {
                "name": current_station_name,
                "stationId": current_station_id,
                "elevation": current_coordinates[2],
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


def kml2geojson(source: Union[str, bytes, os.PathLike, IO], *,
                param_mapping: Optional[dict] = None, param_list: Optional[list] = None,
                max_stations: Optional[int] = None, keep_unmapped=False):

    for event, element in iterparse(source):
        tag_name = get_tag_without_ns(element)
        if tag_name == "TimeStep":
            process_time_step(event, element)
        elif tag_name == "name":
            process_name(event, element)
        elif tag_name == "description":
            process_description(event, element)
        elif tag_name == "Forecast":
            try:
                # may throw KeyErrors when keep_unmapped is False
                process_forecast(event, element, param_mapping, param_list, keep_unmapped)
            except KeyError:
                # KeyErrors are thrown when a mapping is applied but no mapping exists
                # for this Forecast and keep_unmapped is False.
                continue
        elif tag_name == "value":
            process_value(event, element)
        elif tag_name == "coordinates":
            process_coordinates(event, element)
        elif tag_name == "Placemark":
            process_placemark(event, element)

        # for quicker dev cycles, limit loop to max_stations
        if max_stations is not None and number_of_processed_placemarks >= max_stations:
            break

    return {
        "type": "FeatureCollection",
        "features": features,
    }
