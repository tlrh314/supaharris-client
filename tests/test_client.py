import time
import json
import urllib3
import logging
import requests
import unittest
from platform import python_version

import supaharrisclient
from supaharrisclient.client import SupaHarrisClient


class TestSupaHarrisClient(unittest.TestCase):
    # TODO: setup a container that runs SupaHarris in test environment,
    # then run w/ supaharris_dot_com=False :-)
    def setUp(self, supaharris_dot_com=True):
        urllib3.disable_warnings()
        self.startTime = time.time()

        self.supaharris_dot_com = supaharris_dot_com
        if supaharris_dot_com:
            self.shc = SupaHarrisClient(set_all_data=False)
        else:
            self.shc = SupaHarrisClient(
                base_url="https://nginx/api/v1/", verify=False, set_all_data=False
            )

        self.shc.logger.handlers.pop()
        self.shc.logger.level = logging.CRITICAL
        for h in self.shc.logger.handlers: h.level = logging.CRITICAL

    def tearDown(self):
        total = time.time() - self.startTime
        print("\n\t\033[91m[{0}] took {1:.3f}s\033[0m".format(self.id(), total))

    def test_string(self):
        self.assertEqual(str(self.shc), "SupaHarrisClient for '{0}'".format(
            "https://www.supaharris.com/api/v1/" if self.supaharris_dot_com else "https://nginx/api/v1/"
        ))

    def test_headers(self):
        headers = self.shc.headers
        self.assertEqual(self.shc.headers["Accept"], "application/json")
        self.assertEqual(self.shc.headers["User-Agent"],
            "SupaHarris for Python ({0}); Python ({1}).".format(
            supaharrisclient.__version__, str(python_version())
            )
        )

    def test_set_reference_list(self):
        # Here we send a GET request because we want to check the response
        response = requests.get(
            self.shc.reference_list, headers=self.shc.headers,
            verify=self.supaharris_dot_com
        )
        content = json.loads(response.content.decode("utf8"))
        self.assertEqual(response.status_code, 200)

        # This class method will set self.shc.references
        self.shc.set_reference_list()
        self.assertEqual(content["count"], len(self.shc.references))

    def test_set_astro_object_list(self):
        response = requests.get(
            self.shc.astro_object_list, headers=self.shc.headers,
            verify=self.supaharris_dot_com
        )
        content = json.loads(response.content.decode("utf8"))
        self.assertEqual(response.status_code, 200)

        self.shc.set_astro_object_list()
        self.assertEqual(content["count"], len(self.shc.astro_objects))

    def test_set_astro_object_classification_list(self):
        response = requests.get(
            self.shc.astro_object_classifcation_list, headers=self.shc.headers,
            verify=self.supaharris_dot_com
        )
        content = json.loads(response.content.decode("utf8"))
        self.assertEqual(response.status_code, 200)

        self.shc.set_astro_object_classification_list()
        self.assertEqual(content["count"], len(self.shc.astro_object_classifications))

    def test_set_parameter_list(self):
        response = requests.get(
            self.shc.parameter_list, headers=self.shc.headers,
            verify=self.supaharris_dot_com
        )
        content = json.loads(response.content.decode("utf8"))
        self.assertEqual(response.status_code, 200)

        self.shc.set_parameter_list()
        self.assertEqual(content["count"], len(self.shc.parameters))

    def test_set_observation_list(self):
        response = requests.get(
            self.shc.observation_list, headers=self.shc.headers,
            verify=self.supaharris_dot_com
        )
        content = json.loads(response.content.decode("utf8"))
        self.assertEqual(response.status_code, 200)

        self.shc.set_observation_list()
        self.assertEqual(content["count"], len(self.shc.observations_json))

        # TODO: test for self.shc.observations


if __name__ == "__main__":
    unittest.main()
