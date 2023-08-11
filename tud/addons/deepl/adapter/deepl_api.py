# -*- coding: utf8 -*-
"""DeepL API utility
"""
import requests
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import implements


from tud.addons.deepl import DeepLAPIMessageFactory as _
from tud.addons.deepl.interfaces import IDeepLAPI
from tud.addons.deepl.interfaces import IDeepLAPISettings


class DeepLAPI(object):
    """Utility for communicating with the DeepL API."""

    implements(IDeepLAPI)

    def _callDeepLAPI(self, endpoint, params=None):
        """Returns the result of a DeepL API call. If an error occured, it raises an DeepLAPIError.

        :param endpoint: endpoint that should be called
        :type endpoint: str
        :param params: arguments that should be send to the endpoint
        :type params: dict
        """
        settings = getUtility(IRegistry).forInterface(IDeepLAPISettings)
        api_timeout = settings.deepl_api_timeout
        api_url = settings.deepl_api_url
        auth_token = settings.deepl_api_auth_token

        if not api_url:
            raise DeepLAPIError("Error: DeepL API URL is not set")
        elif api_url[-1] != "/":
            api_url += "/"
        if not auth_token:
            raise DeepLAPIError("Error: DeepL API authentication token is not set")
        else:
            auth_token = "DeepL-Auth-Key {}".format(auth_token)

        result = requests.get(
            "{}{}".format(api_url, endpoint),
            params=params,
            timeout=api_timeout,
            headers={"Authorization": auth_token},
        )

        if result.status_code == 403:
            raise DeepLAPIError("Error: Authentication token was not accepted (status code {})".format(result.status_code))
        elif result.status_code == 456:
            raise DeepLAPIError("Error: Translation quota exeeded (status code {})".format(result.status_code))
        elif not result.ok:
            raise DeepLAPIError("Error: Deepl API request returns with status code {}".format(result.status_code))

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
        params = dict()
        params.update(
            {
                "source_lang": source_language,
                "target_lang": target_language,
                "text": text,
                "tag_handling": "xml",
                "split_sentences": "nonewlines",
            }
        )

        try:
            result = self._callDeepLAPI(endpoint="translate", params=params)
        except DeepLAPIError as e:
            return e.message

        if result.has_key("translations"):
            return result["translations"][0]["text"]
        else:
            return "Error: Result does not contain translated text"

    def usage(self):
        """Returns usage information within the current billing period together with the corresponding account limits.
        Depending on the user account type, the result information differs. Therefore see
        https://www.deepl.com/de/docs-api/general/get-usage
        """
        try:
            result = self._callDeepLAPI(endpoint="usage")
        except DeepLAPIError as e:
            return e.message

        return result


class DeepLAPIError(Exception):
    """This exception is thrown when communicating with the DeepL API and an error occures.
    """

    def __call__(self, message):
        self.message = message

        return super().__call__(self.message)
