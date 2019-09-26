import sys
import json
import logging
import requests
from platform import python_version

from supaharrisclient import __version__


def response_to_json(response):
    return json.loads(response.content.decode("utf8"))


class SupaHarris(object):
    def __init__(self, base_url="https://www.supaharris.com/api/v1/",
            loglevel=logging.DEBUG, verify=True):
        """ SupaHarris: a Python client implementation for the SupaHarris API
        (Django REST Framework).

        Keyword arguments:
        base_url -- the base url of the API (could be localhost for development)
        loglevel -- verbosity of the output. Choose any one of
            logging.CRITICAL/ERROR/WARNING/INFO/DEBUG/NOTSET """

        # Set up a logger to 'print' to stdout
        self.logger = logging.getLogger(__file__)
        self.logger.setLevel(loglevel)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(loglevel)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        self.logger.handlers = []
        self.logger.addHandler(handler)

        self.base_url = base_url

        # If we run locally (development), then we GET 443 /w self-signed certificate.
        # We tell the requests library not verify the ssl certificate, and we suppress
        # the InsecureRequestWarning.
        self.verify = verify
        if not self.verify:
            import urllib3
            urllib3.disable_warnings()

        url_params = "?format=json"  # Size not yet implemented for all ViewSets
        self.reference_list = "{0}catalogue/reference/{1}".format(
            self.base_url, url_params)
        self.astro_object_list = "{0}catalogue/astro_object/{1}".format(
            self.base_url, url_params)
        self.astro_object_classifcation_list = "{0}catalogue/astro_object_classifcation/{1}".format(
            self.base_url, url_params)
        self.parameter_list = "{0}catalogue/parameter/{1}".format(
            self.base_url, url_params)
        # Takes roughly 2 seconds to process a request /w 1000 Observation instances
        url_params = "?format=json&size=1000"
        self.observation_list = "{0}catalogue/observation/{1}".format(
            self.base_url, url_params)

        self.headers = {
            "Accept": "application/json",
            "User-Agent": "SupaHarris for Python ({0}); Python ({1}).".format(
                __version__, str(python_version()))
        }

    def set_reference_list(self):
        self.references = self.get_list(self.reference_list, recursive=True)

    def print_references(self):
        self.logger.info("\nRetrieved {0} references\n".format(len(self.references)))

        self.logger.info("-"*79)
        self.logger.info("  {0:<5s}{1} ({2})".format("id", "first_author", "year"))
        self.logger.info("-"*79)
        for r in self.references:
            self.logger.info("  {0:<5d}{1} ({2})".format(
                r["id"], r["first_author"], r["year"] if "year" in r.keys() else ""))
        self.logger.info("-"*79)

    def set_astro_object_list(self):
        self.astro_objects = self.get_list(self.astro_object_list, recursive=True)

    def print_astro_objects(self):
        self.logger.info("\nRetrieved {0} astro_objects\n".format(len(self.astro_objects)))

        self.logger.info("-"*79)
        self.logger.info("  {0:<5s}{1:<15s}{2}".format("id", "name", "altname"))
        self.logger.info("-"*79)
        for o in self.astro_objects:
            self.logger.info("  {0:<5d}{1:<15s}{2}".format(
                o["id"], o["name"], o["altname"] if o["altname"] else ""))
        self.logger.info("-"*79)

    def set_astro_object_classification_list(self):
        self.astro_object_classifications = self.get_list(
            self.astro_object_classifcation_list, recursive=True)

    def print_astro_object_classifications(self):
        self.logger.info("\nRetrieved {0} astro_object_classifications\n".format(
            len(self.astro_object_classifications)))

        self.logger.info("-"*79)
        self.logger.info("  {0:<5s}{1:<15s}".format("id", "name"))
        self.logger.info("-"*79)
        for c in self.astro_object_classifications:
            self.logger.info("  {0:<5d}{1:<15s}".format(c["id"], c["name"] ))
        self.logger.info("-"*79)

    def set_parameter_list(self):
        self.parameters = self.get_list(self.parameter_list, recursive=True)

    def print_parameters(self):
        self.logger.info("\nRetrieved {0} parameters\n".format(len(self.parameters)))

        self.logger.info("-"*79)
        self.logger.info("  {0:<5s}{1:<15s}{2}".format("id", "name", "description"))
        self.logger.info("-"*79)
        for p in self.parameters:
            self.logger.info("  {0:<5d}{1:<15s}{2}".format(p["id"], p["name"], p["description"]))
        self.logger.info("-"*79)

    def set_observation_list(self):
        # TODO: if response.data["count"] == len(self.observations) then don't update?
        self.observations = self.get_list(self.observation_list, recursive=True)

    def set_all_data(self):
        self.set_parameter_list()
        self.set_reference_list()
        self.set_astro_object_list()
        self.set_astro_object_classification_list()
        self.set_observation_list()

    def get_list(self, uri, recursive=False, total_count=0):
        """ Send a GET request to the SupaHarris API endpoint uri. The Django
        REST response contains 'count' (int), 'next' (string), 'previous' (string),
        'results' (list). The response is paginated so we recursively GET the
        'next' uri until 'next' is 'null' (JSON) / None (Python). At that point
        len(results) should equal the value of count. """

        self.logger.debug("GET {0}".format(uri))

        response = requests.get(uri, headers=self.headers, verify=self.verify)
        if response.status_code != 200:
            self.logger.error("  Could not retrieve uri = '{0}'. Better stop.".format(uri))
            sys.exit(1)

        results = []

        data = response_to_json(response)
        count = data["count"]
        next = data["next"]
        results += data["results"]
        total_count += len(results)
        self.logger.debug("  retrieved {0}/{1} instances".format(total_count, count))
        self.logger.debug("  next = {0}".format(next))

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
