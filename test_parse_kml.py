#!/usr/bin/env python3

import unittest
from parse_kml import strip_ns


class TestStringMethods(unittest.TestCase):
    def test_strip_ns(self):
        test_string = "{my-namespace}my-tag-name"
        result = strip_ns(test_string)
        self.assertIsInstance(result, str)
        self.assertFalse("{" in result)
