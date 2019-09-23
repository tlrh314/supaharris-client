import time
import json
import requests
import unittest
from platform import python_version

import supaharrisclient
from supaharrisclient.models import SupaHarris


class TestModels(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()
        self.sh = SupaHarris()

    def tearDown(self):
        total = time.time() - self.startTime
        print("\n\t\033[91m[{0}] took {1:.3f}s\033[0m".format(self.id(), total))

    def test_string(self):
        self.assertEqual(str(self.sh), "SupaHarris API client for 'https://www.supaharris.com/api/v1/'")

    def test_headers(self):
        headers = self.sh.headers
        self.assertEqual(self.sh.headers["Accept"], "application/json")
        self.assertEqual(self.sh.headers["User-Agent"],
            "SupaHarris for Python ({0}); Python ({1}).".format(
            supaharrisclient.__version__, str(python_version())
            )
        )

    def test_set_reference_list(self):
        # Here we send a GET request because we want to check the response
        response = requests.get(self.sh.reference_list, headers=self.sh.headers)
        content = json.loads(response.content.decode("utf8"))
        self.assertEqual(response.status_code, 200)

        # This class method will set self.sh.references
        self.sh.set_reference_list()
        self.assertEqual(content["count"], len(self.sh.references))

    def test_set_astro_object_list(self):
        response = requests.get(self.sh.astro_object_list, headers=self.sh.headers)
        content = json.loads(response.content.decode("utf8"))
        self.assertEqual(response.status_code, 200)

        self.sh.set_astro_object_list()
        self.assertEqual(content["count"], len(self.sh.astro_objects))

    def test_set_astro_object_classification_list(self):
        response = requests.get(self.sh.astro_object_classifcation_list, headers=self.sh.headers)
        content = json.loads(response.content.decode("utf8"))
        self.assertEqual(response.status_code, 200)

        self.sh.set_astro_object_classification_list()
        self.assertEqual(content["count"], len(self.sh.astro_object_classifications))

    def test_set_parameter_list(self):
        response = requests.get(self.sh.parameter_list, headers=self.sh.headers)
        content = json.loads(response.content.decode("utf8"))
        self.assertEqual(response.status_code, 200)

        self.sh.set_parameter_list()
        self.assertEqual(content["count"], len(self.sh.parameters))

    def test_set_observation_list(self):
        response = requests.get(self.sh.observation_list, headers=self.sh.headers)
        content = json.loads(response.content.decode("utf8"))
        self.assertEqual(response.status_code, 200)

        self.sh.set_observation_list()
        self.assertEqual(content["count"], len(self.sh.observations))


if __name__ == "__main__":
    unittest.main()
