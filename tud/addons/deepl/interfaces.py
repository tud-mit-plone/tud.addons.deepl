# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ITudAddonsDeeplLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""

class IDeepLAPI(Interface):
    """Interface to retrieve data from the DeepL API.
    """
