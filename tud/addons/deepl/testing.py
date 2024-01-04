from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE
from plone.testing.zope import installProduct


class TudAddonsDeeplLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # call super setUpZope
        super(TudAddonsDeeplLayer, self).setUpZope(app, configurationContext)

        import plone.rest
        import tud.addons.deepl

        self.loadZCML(package=plone.rest)
        self.loadZCML(name="testing.zcml", package=tud.addons.deepl)
        installProduct(app, "tud.addons.deepl")

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, "tud.addons.deepl:test")


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
