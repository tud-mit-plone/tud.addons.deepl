import json

from plone.rest import Service
from zope.component import getUtility

from tud.addons.deepl.interfaces import IDeepLAPI


class DeepLTranslateService(Service):
    """Service that uses the Deepl API Utility to translate a text. It accepts POST requests with the arguments text,
    source_language and target_language.
    """

    def render(self):
        self.request.response.setHeader("Content-Type", "application/json")

        text = self.request.form.get("text", None)
        source_lang = self.request.form.get("source_language", "de")
        target_lang = self.request.form.get("target_language", "en")

        if text is None or len(text.strip()) < 1:
            return "Error: empty text"

        deepl_api = getUtility(IDeepLAPI, "deeplapi")
        result = deepl_api.translate(text=text, source_language=source_lang, target_language=target_lang)

        if result["error"]:
            if result["status_code"]:
                self.request.response.setStatus(result["status_code"])
                self.request.response.setBody(json.dumps(result))
            else:
                raise Exception(result["error"])
        else:
            return json.dumps(result)


class DeepLTranslateServiceUsage(Service):
    """Service to query the current usage status of the DeepL API account."""

    def render(self):
        self.request.response.setHeader("Content-Type", "application/json")

        deepl_api = getUtility(IDeepLAPI, "deeplapi")
        result = deepl_api.usage()

        return json.dumps(result)
