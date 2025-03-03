# -*- coding: utf8 -*-
"""DeepL API utility
"""
import requests
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.globalrequest import getRequest
from zope.interface import implements
from zope.i18n import translate

from tud.addons.deepl import logger
from tud.addons.deepl import _
from tud.addons.deepl.interfaces import IDeepLAPI
from tud.addons.deepl.interfaces import IDeepLAPISettings


class RequestMethods(object):
    """Emulate sort of an enum. Provide ALL to replace the isinstance check."""
    # TODO: solve this as enum in py3 and use 'isinstance' instead 'in' for checks
    GET = "GET"
    POST = "POST"
    ALL = ["GET", "POST"]


class DeepLAPI(object):
    """Utility for communicating with the DeepL API."""

    implements(IDeepLAPI)

    def _callDeepLAPI(self, endpoint, request_method=RequestMethods.GET, params=None):
        """Returns the result of a DeepL API call. If an error occured, it raises an DeepLAPIError.

        :param endpoint: endpoint that should be called
        :type endpoint: str
        :param request_method: request method to use (POST/GET)
        :type request_method: str
        :param params: arguments that should be send to the endpoint
        :type params: dict
        """
        settings = getUtility(IRegistry).forInterface(IDeepLAPISettings)
        api_timeout = settings.deepl_api_timeout
        api_url = settings.deepl_api_url
        auth_token = settings.deepl_api_auth_token

        if not api_url:
            raise DeepLAPIError("DeepL API URL is not set")
        elif api_url[-1] != "/":
            api_url += "/"
        if not auth_token:
            raise DeepLAPIError("DeepL API authentication token is not set")
        else:
            auth_token = "DeepL-Auth-Key {}".format(auth_token)

        if request_method not in RequestMethods.ALL:
            raise DeepLAPIError(_("Unknown request type"))

        request_params = {
            "method": request_method,
            "url": "{}{}".format(api_url, endpoint),
            "timeout": api_timeout,
            "headers": {"Authorization": auth_token},
        }

        if request_method == RequestMethods.POST:
            request_params["data"] = params
        elif request_method == RequestMethods.GET:
            request_params["params"] = params

        try:
            result = requests.request(**request_params)
        except requests.exceptions.ConnectionError:
            raise DeepLAPIError(_("Can not connect to DeepL API URL"))

        if result.status_code == 403:
            raise DeepLAPIError(
                _("Authentication token was not accepted"), result.status_code
            )
        elif result.status_code == 429:
            raise DeepLAPIError(
                _("Too many concurrent requests to DeepL"), result.status_code
            )
        elif result.status_code == 456:
            raise DeepLAPIError(
                _("DeepL translation quota exeeded"),
                result.status_code,
            )

        elif not result.ok:
            msg = translate(
                _("DeepL API request returns with an error. Server response:"),
                context=getRequest(),
            )
            raise DeepLAPIError(
                msg + u" " + result.text,
                result.status_code,
            )

        return result.json()

    def translate(self, text, source_language="de", target_language="en"):
        """Translates a text from source language to target language via DeepL API.

        :param text: text that should be translated
        :type text: str
        :param source_language: current language of the text
        :type source_language: str
        :param target_language: language into which the text should be translated
        :type target_language: str
        """
        if not isinstance(text, list):
            text = [text]

        params = dict()
        params.update(
            {
                "source_lang": source_language,
                "target_lang": target_language,
                "text": text,
                "tag_handling": "html",
                "split_sentences": "nonewlines",
            }
        )

        settings = getUtility(IRegistry).forInterface(IDeepLAPISettings)
        if settings.deepl_api_glossary_id:
            params["glossary_id"] = settings.deepl_api_glossary_id

        try:
            result = self._callDeepLAPI(
                # use POST for translation calls to avoid the url-length-textsize-cap
                endpoint="translate", request_method=RequestMethods.POST, params=params
            )
        except DeepLAPIError as e:
            return {"error": e.message, "result": None, "status_code": e.status_code}

        if "translations" in result:
            return {
                "error": None,
                "result": result["translations"][0]["text"],
                "status_code": 200,
            }
        else:
            return {
                "error": "Result does not contain translated text",
                "result": None,
                "status_code": 500,
            }

    def usage(self):
        """Returns usage information within the current billing period together with the corresponding account limits.
        Depending on the user account type, the result information differs. Therefore see
        https://www.deepl.com/de/docs-api/general/get-usage
        """
        try:
            result = self._callDeepLAPI(endpoint="usage")
        except DeepLAPIError as e:
            return {"error": e.message, "result": None, "status_code": e.status_code}

        return {"error": None, "result": result, "status_code": 200}


class DeepLAPIError(Exception):
    """This exception is thrown when communicating with the DeepL API and an error occures."""

    def __init__(self, message, status_code=None):
        super(DeepLAPIError, self).__init__(message)
        self.message = message
        self.status_code = status_code if status_code else 500

        logger.exception(
            "DeepLAPIError: {} (status code: {})".format(self.message, self.status_code)
        )
