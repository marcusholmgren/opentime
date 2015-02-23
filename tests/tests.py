#!flask/bin/python
import os
import unittest
import datetime
from src import appengine_config
from src.main import DayModule, TimeEntry
from google.appengine.ext import testbed


class TestCase(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_daymodule_tostring(self):
        sut = DayModule(day="2015-02-10")

        self.assertEqual(str(sut), "[DayModule 2015-02-10]", "Expected DayModule to contains date in representation.")

    def test_create_daymodule_from_datetime_representation(self):
        day = datetime.datetime(2013, 02, 28).strftime("%Y-%m-%d")
        sut = DayModule(day=day)

        self.assertEqual(str(sut), "[DayModule 2013-02-28]", "Expected format of day to be ISO string.")

    def test_add_time_to_same_day_and_code_increases_total_time(self):
        sut = DayModule(day="2015-02-10")
        sut.add_time(code="A", time=2.5)
        sut.add_time(code="B", time=-20.0)
        sut.add_time(code="A", time=3)

        self.assertEqual(sut.details[0].time, 5.5, "Expected time to be positive.")


if __name__ == '__main__':
    unittest.main()