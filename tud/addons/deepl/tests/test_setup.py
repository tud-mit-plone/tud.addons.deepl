"""Setup tests for this package."""
from tud.addons.deepl.testing import TUD_ADDONS_DEEPL_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest

try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that tud.addons.deepl is properly installed."""

    layer = TUD_ADDONS_DEEPL_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if tud.addons.deepl is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'tud.addons.deepl'))

    def test_browserlayer(self):
        """Test that ITudAddonsDeeplLayer is registered."""
        from tud.addons.deepl.interfaces import (
            ITudAddonsDeeplLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ITudAddonsDeeplLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = TUD_ADDONS_DEEPL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['tud.addons.deepl'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if tud.addons.deepl is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'tud.addons.deepl'))

    def test_browserlayer_removed(self):
        """Test that ITudAddonsDeeplLayer is removed."""
        from tud.addons.deepl.interfaces import \
            ITudAddonsDeeplLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ITudAddonsDeeplLayer,
            utils.registered_layers())
