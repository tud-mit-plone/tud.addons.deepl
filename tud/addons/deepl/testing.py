import os

from plone import api
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE
from plone.testing.zope import installProduct
import tud.addons.deepl


def setup_deepl_from_environment():
    """Setup Deepl key from environment
    """
    token = os.getenv("DEEPL_API_TOKEN", "")
    api.portal.set_registry_record("tud.addons.deepl.interfaces.IDeepLAPISettings.deepl_api_auth_token", unicode(token))


class TudAddonsDeeplLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # call super setUpZope
        super(TudAddonsDeeplLayer, self).setUpZope(app, configurationContext)

        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        # import plone.app.dexterity
        # self.loadZCML(package=plone.app.dexterity)
        import plone.rest

        self.loadZCML(package=plone.rest)

        self.loadZCML(name="testing.zcml", package=tud.addons.deepl)
        installProduct(app, "tud.addons.deepl")

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, "tud.addons.deepl:test")
        setup_deepl_from_environment()

FIXTURE = TudAddonsDeeplLayer()


TUD_ADDONS_DEEPL_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="TudAddonsDeeplLayer:IntegrationTesting",
)


TUD_ADDONS_DEEPL_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name="TudAddonsDeeplLayer:FunctionalTesting",
)


TUD_ADDONS_DEEPL_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="TudAddonsDeeplLayer:AcceptanceTesting",
)
