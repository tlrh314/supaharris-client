import json
import logging
import requests
from platform import python_version

from supaharrisclient import __version__


def response_to_json(response):
    return json.loads(response.content.decode("utf8"))


class SupaHarris(object):
    def __init__(self, base_url="https://www.supaharris.com/api/v1/"):
        self.logger = logging.getLogger(__file__)

        self.base_url = base_url
        self.reference_list = "{0}catalogue/reference/".format(self.base_url)
        self.astro_object_list = "{0}catalogue/astro_object/".format(self.base_url)
        self.astro_object_classifcation_list = "{0}catalogue/astro_object_classifcation/".format(self.base_url)
        self.parameter_list = "{0}catalogue/parameter/".format(self.base_url)
        self.observation_list = "{0}catalogue/observation/".format(self.base_url)

        self.headers = {
            "Accept": "application/json",
            "User-Agent": "SupaHarris for Python ({0}); Python ({1}).".format(
                __version__, str(python_version()))
        }

    def set_reference_list(self):
        self.references = self.get_list(self.reference_list, recursive=True)

    def set_astro_object_list(self):
        self.astro_objects = self.get_list(self.astro_object_list, recursive=True)

    def set_astro_object_classification_list(self):
        self.astro_object_classifications = self.get_list(self.astro_object_classifcation_list, recursive=True)

    def set_parameter_list(self):
        self.parameters = self.get_list(self.parameter_list, recursive=True)

    def set_observation_list(self):
        self.observations = self.get_list(self.observation_list, recursive=True)

    def get_list(self, uri, recursive=False, total_count=0):
        """ Send a GET request to the SupaHarris API endpoint uri. The Django
        REST response contains 'count' (int), 'next' (string), 'previous' (string),
        'results' (list). The response is paginated so we recursively GET the
        'next' uri until 'next' is 'null' (JSON) / None (Python). At that point
        len(results) should equal the value of count. """

        self.logger.debug("GET {0}".format(uri))

        response = requests.get(uri, headers=self.headers)
        if response.status_code != 200:
            self.logger.error("  Could not retrieve uri = '{0}'. Better stop.".format(uri))
            sys.exit(1)

        results = []

        data = response_to_json(response)
        count = data["count"]
        next = data["next"]
        results += data["results"]
        total_count += len(results)
        self.logger.debug("  GET {0} retrieved {1}/{2} instances".format(uri, total_count, count))
        self.logger.debug("    next = {0}".format(next))

        if next and recursive:
            results += self.get_list(next, recursive=True, total_count=total_count)

        return results

    def __str__(self):
        return "SupaHarris API client for '{0}'".format(self.base_url)


class Parameter(object):
    def __init__(self):
        pass


class Reference(object):
    def __init__(self):
        pass


class AstroObjectClassification(object):
    def __init__(self):
        pass


class AstroObject(object):
    def __init__(self):
        pass


class Profile(object):
    def __init__(self):
        pass


class Auxiliary(object):
    def __init__(self):
        pass


class Observation(object):
    def __init__(self):
        pass


class Rank(object):
    def __init__(self):
        pass
