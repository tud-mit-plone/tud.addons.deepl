# -*- coding: utf-8 -*-
import json

from plone.rest import Service
from zope.component import getUtility

from tud.addons.deepl.interfaces import IDeepLAPI

class DeepLTranslateService(Service):
    """
    """

    def render(self):
        """
        """
        self.request.response.setHeader("Content-Type", "application/json")

        text = self.request.form.get("text", None)
        source_lang = self.request.form.get("source_lang", "de")
        dest_lang = self.request.form.get("destination_lang", "en")

        if text is None or len(text.strip()) < 1:
            return "Error: empty text"

        deepl_api = getUtility(IDeepLAPI, "deeplapi")
        result = deepl_api.translate(
            text=text,
            source_lang=source_lang,
            destination_lang=dest_lang
        )

        return json.dumps(result)
