# -*- coding: utf-8 -*-
"""DeepL API Unit Test"""
import os
import unittest

from plone import api

from tud.addons.deepl.adapter.deepl_api import DeepLAPI
from tud.addons.deepl.testing import TUD_ADDONS_DEEPL_INTEGRATION_TESTING


class TestDeepLAPI(unittest.TestCase):
    """ """

    layer = TUD_ADDONS_DEEPL_INTEGRATION_TESTING
    html_de = "\n".join(
        (
            "<h2>Überschrift</h2>",
            "<p>Einfacher Text.</p>",
            '<div class="tudbox tudbox_align_left tudbox_float_next tudbox_width_half tudboxcontact" src="resolveuid/a6b054e259394687bfa4a9581f97376d">&#8203;</div>',
            "<p>Weiterer Text.</p>",
        )
    )
    word_de = "Auto"
    word_en = "car"

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.deepl_api = DeepLAPI()

        api_url = os.getenv("DEEPL_API_URL", None)
        if api_url:
            api.portal.set_registry_record(
                "tud.addons.deepl.interfaces.IDeepLAPISettings.deepl_api_url", unicode(api_url)
            )

    def test_APIBase(self):
        result = self.deepl_api.translate(text=self.word_de)
        self.assertIsNone(result["error"])
        self.assertIsNotNone(result["result"])

    def test_translate(self):
        result = self.deepl_api.translate(text=self.word_de)
        self.assertEqual(result["result"].lower(), self.word_en.lower())
        result = self.deepl_api.translate(text=self.word_en, source_language="en", target_language="de")
        self.assertEqual(result["result"].lower(), self.word_de.lower())
        result = self.deepl_api.translate(self.html_de)
        self.assertIn("<h2>", result["result"])
        self.assertIn('src="resolveuid/a6b054e259394687bfa4a9581f97376d"', result["result"])

    def test_usage(self):
        usage = self.deepl_api.usage()
        self.assertIsInstance(usage["result"], dict)
        self.assertIn("character_count", usage["result"].keys())
