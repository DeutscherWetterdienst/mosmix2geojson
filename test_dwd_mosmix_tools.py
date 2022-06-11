#!/usr/bin/env python3

import unittest
from dwd_mosmix_tools.kml2json import strip_ns


class TestStringMethods(unittest.TestCase):
    def test_strip_ns(self):
        test_string = "{my-namespace}my-tag-name"
        result = strip_ns(test_string)
        self.assertIsInstance(result, str)
        self.assertFalse("{" in result)
