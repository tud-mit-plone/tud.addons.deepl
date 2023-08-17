"""Module where all interfaces, events and exceptions live."""

from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from tud.addons.deepl import DeepLAPIMessageFactory as _


class ITudAddonsDeeplLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""

class IDeepLAPI(Interface):
    """Interface to retrieve data from the DeepL API.
    """

class IDeepLAPISettings(Interface):
    """Settings schema for the DeepL API.
    """
    deepl_api_url = schema.TextLine(
        title=_(u"deepl_api_url", default=u"URL of DeepL API without endpoint"),
        required=True,
        default=u"https://api-free.deepl.com/v2",
    )

    deepl_api_timeout = schema.Float(
        title=_(u"deepl_api_timeout", default=u"Connect/Read timeout for the remote connection to the DeepL API"),
        description=_(u"deepl_api_timeout_desc", default=u"Time in seconds; should be between 3 and 10"),
        required=True,
        default=10.0,
    )

    deepl_api_auth_token = schema.TextLine(
        title=_(u"deepl_api_auth_token", default=u"Authentication key for the DeepL API"),
        required=True,
        default=u"",
    )

    deepl_api_glossary_id = schema.TextLine(
        title=_(u"deepl_api_glossary_id", default=u"ID of the glossary"),
        required=False,
        default=u"",
    )
