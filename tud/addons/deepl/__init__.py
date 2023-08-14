# -*- coding: utf-8 -*-
"""Init and utils."""
import logging

from zope.i18nmessageid import MessageFactory


logger = logging.getLogger("tud.addons.deepl")
DeepLAPIMessageFactory = MessageFactory('tud.addons.deepl')
