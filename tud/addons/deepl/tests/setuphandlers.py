import os

from plone import api


def post_install_testing(context):
    """Post install script for the test profile"""
    setup_deepl_from_environment()


def setup_deepl_from_environment():
    """Setup Deepl key from environment"""
    token = os.getenv("DEEPL_API_TOKEN", "")
    api.portal.set_registry_record("tud.addons.deepl.interfaces.IDeepLAPISettings.deepl_api_auth_token", unicode(token))
