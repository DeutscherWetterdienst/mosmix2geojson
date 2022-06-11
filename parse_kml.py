#!/usr/bin/env python3

import xml.etree.ElementTree as ET
from itertools import islice
from typing import Iterator, Tuple
from xml.etree.ElementTree import Element

TEST_FILE = "data/MOSMIX_L_2022061021.kml"
MAX_EVENTS = 1000


def iterparse(*args) -> Iterator[Tuple[str, Element]]:
    return ET.iterparse(*args)


def strip_ns(string):
    return string[string.find("}") + 1:]


def get_tag_without_ns(element: Element):
    return strip_ns(element.tag)


def get_attrs_without_ns(element: Element):
    return {strip_ns(key): value for key, value in element.attrib.items()}


default_undef_sign = "-"
time_steps = []


def process_time_step(event, element):
    global time_steps
    # only process "end" events
    if event == "end":
        time_steps.append(element.text.strip())


forecasts = {}
current_value = None


def process_forecast(event, element):
    global forecasts
    # only process "end" events
    if event == "end":
        element_name = get_attrs_without_ns(element)["elementName"]
        forecasts[element_name] = current_value


def process_value(event, element):
    global current_value
    if event == "end":
        current_value = [float(value) if value != default_undef_sign else None
                         for value in element.text.split()]


def main():
    for event, element in islice(iterparse(TEST_FILE, ["start", "end"]), MAX_EVENTS):
        tag_name = get_tag_without_ns(element)
        if tag_name == "TimeStep":
            process_time_step(event, element)
        elif tag_name == "Forecast":
            process_forecast(event, element)
        elif tag_name == "value":
            process_value(event, element)

    print(time_steps[:5])
    for key, val in forecasts.items():
        print(f"{key}={val[:5]}")


if __name__ == "__main__":
    main()
