"""FIS API adapter
"""
import requests
from plone.memoize.view import memoize
from zope.interface import implements

from tud.boxes.webcms import boxes_webcmsMessageFactory as _
from tud.boxes.webcms import logger
from tud.boxes.webcms.content.fisbox import ORGANISATIONAL_UNITS_TYPE
from tud.boxes.webcms.content.fisbox import PERSONS_TYPE
from tud.boxes.webcms.content.fisbox import PROJECTS_TYPE
from tud.boxes.webcms.content.fisbox import RESEARCH_OUTPUTS_TYPE
from tud.boxes.webcms.content.fisbox import get_api_endpoint
from tud.boxes.webcms.content.fisbox import get_api_timeout
from tud.boxes.webcms.interfaces import IFISAPI

from tud.addons.deepl.interfaces import IDeepLAPI


class DeepLAPI:
    """Adapter for communicating with with the FIS API."""

    implements(IDeepLAPI)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    # def _create_entry(self, entity_data, entity_type):
    #     """Helper to manifacture a select2 compatible entry with a human
    #     readable text.

    #     :param entity_data: data for a single entity from the FIS API
    #     :type entity_data: dict
    #     :param entity_type: entity type
    #     :type entity_type: str
    #     """
    #     entry = {
    #         "fis_uuid": entity_data["uuid"],
    #         "type": entity_type,
    #         "id": entity_data["uuid"],
    #     }
    #     if entity_type == ORGANISATIONAL_UNITS_TYPE:
    #         # select2 mandatory data
    #         entry["text"] = entry["name"] = entity_data["name"]
    #     else:
    #         entry.update(
    #             {
    #                 "firstName": entity_data.get("firstName", u""),
    #                 "lastName": entity_data["lastName"],
    #                 "organisations": entity_data.get("organisationalUnits", []),
    #             }
    #         )
    #         # select2 mandatory data
    #         entry["text"] = u"{}{} {}".format(
    #             entry["firstName"] + u" " if entry["firstName"] else u"",
    #             entry["lastName"],
    #             u"({})".format(u", ".join(entry["organisations"])) if entry["organisations"] else u"",
    #         )
    #     return entry

    # def get_results(self, start=0, size=10):
    #     """Returns the results set based on a query.

    #     :param start: current offset
    #     :type start: int
    #     :param size: number of items per page
    #     :type size: int
    #     :return:
    #     :rtype: dict
    #     """
    #     error = ""
    #     organisations = self.context.getOrganisations()
    #     persons = self.context.getPersons()
    #     publication_subtypes = self.context.getResearchOutputSubtypes()

    #     endpoint = "{}/{}".format(
    #         get_api_endpoint(),
    #         "research-outputs-html"
    #     )

    #     api_timeout = get_api_timeout()
    #     params = dict()
    #     params.update(
    #         {
    #             "locale": self.context.getCurrentLanguageForFIS(),
    #             # pagination parameters
    #             "offset": start,
    #             "size": size,
    #             "research_output_types": publication_subtypes,
    #             "peerreviewedonly": self.context.getShowOnlyPeerreviewed(),
    #         }
    #     )

    #     if organisations:
    #         params["organisation_uuids"] = organisations
    #     if persons:
    #         params["person_uuids"] = persons


    #     # optional time period filter
    #     start = self.context.getYearStart()
    #     end = self.context.getYearEnd()
    #     if start:
    #         params["startDate"] = "{}-01-01".format(start)
    #     if end:
    #         params["endDate"] = "{}-12-31".format(end)

    #     try:
    #         # Sanity check
    #         if not organisations and not persons:
    #             raise ValueError("Neither filtered by organisations nor persons.")

    #         response = requests.get(
    #             endpoint,
    #             params=params,
    #             timeout=api_timeout,
    #         )
    #         status_code = response.status_code
    #         response = response.json()

    #         if status_code != 200:

    #             detail = response.get("detail")

    #             if isinstance(detail, list) and detail:
    #                 msg = detail[0].get("msg", "No message given")
    #             else:
    #                 msg = detail or "No message given"

    #             raise Exception(
    #                 "Unexpected status code (expected: 200, got {}). Message: {}".format(
    #                     str(status_code),
    #                     msg,
    #                 )
    #             )

    #         max_results = response.get("count", 0)
    #         results = response.get("items", [])

    #     except Exception:
    #         error = self.context.translate(
    #             _(
    #                 "fisbox_api_error",
    #                 default="An error occurred when trying to connect with the FIS.",
    #             )
    #         )
    #         results = []
    #         max_results = 0
    #         logger.exception("Error when communicating with Research Information Portal API")
    #     return {
    #         "error": error,
    #         "items": results,
    #         "max_results": max_results,
    #     }

    # @memoize
    # def search_entities(self, query, entity_type=PERSONS_TYPE):
    #     """Get search results (both units and persons) for a given query string.

    #     :param query: query string
    #     :type query: str, optional
    #     :param entity_type: entity type
    #     :type  entity_type: str, optional
    #     :return: list of dicts
    #     :rtype: list[dict]
    #     """
    #     endpoint = get_api_endpoint()
    #     params = dict()
    #     params.update(
    #         {
    #             "query": query.strip(),
    #             "locale": self.context.getCurrentLanguageForFIS(),
    #         }
    #     )

    #     results = []

    #     api_timeout = get_api_timeout()

    #     # search units
    #     if entity_type == ORGANISATIONAL_UNITS_TYPE:
    #         organisations = requests.get(
    #             endpoint + "/organisational-units/search",
    #             params=params,
    #             timeout=api_timeout,
    #         ).json()

    #         for organisation in organisations:
    #             results.append(self._create_entry(organisation, entity_type))
    #     # search persons
    #     elif entity_type == PERSONS_TYPE:
    #         persons = requests.get(
    #             endpoint + "/persons/search",
    #             params=params,
    #             timeout=api_timeout,
    #         ).json()

    #         for person in persons:
    #             results.append(self._create_entry(person, entity_type))

    #     return results

    # @memoize
    # def get_entity(self, uuid, entity_type=PERSONS_TYPE):
    #     """Get search results (both units and persons) for a given query string.

    #     :param uuid: UUID
    #     :type uuid: str, optional
    #     :param entity_type: entity type
    #     :type  entity_type: str, optional
    #     :return: dict
    #     :rtype: dict
    #     :raises: Exception
    #     """
    #     endpoint = get_api_endpoint()
    #     params = {
    #         "locale": self.context.getCurrentLanguageForFIS(),
    #     }
    #     if entity_type == ORGANISATIONAL_UNITS_TYPE:
    #         endpoint += "/organisational-units/{uuid}".format(uuid=uuid)
    #     else:
    #         endpoint += "/persons/{uuid}".format(uuid=uuid)

    #     response = requests.get(
    #         endpoint,
    #         params=params,
    #         timeout=get_api_timeout(),
    #     )

    #     status_code = response.status_code
    #     response = response.json()

    #     if status_code != 200:


    #         detail = response.get("detail")

    #         if isinstance(detail, list) and detail:
    #             msg = detail[0].get("msg", "No message given")
    #         else:
    #             msg = detail or "No message given"

    #         raise Exception(
    #             "Unexpected status code (expected: 200, got {}). Message: {}".format(
    #                 str(status_code),
    #                 msg,
    #             )
    #         )

    #     return self._create_entry(response, entity_type)
