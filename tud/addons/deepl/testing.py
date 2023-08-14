# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import tud.addons.deepl


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
        z2.installProduct(app, "tud.addons.deepl")

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'tud.addons.deepl:test')


FIXTURE = TudAddonsDeeplLayer()


TUD_ADDONS_DEEPL_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='TudAddonsDeeplLayer:IntegrationTesting',
)


TUD_ADDONS_DEEPL_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='TudAddonsDeeplLayer:FunctionalTesting',
)


TUD_ADDONS_DEEPL_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='TudAddonsDeeplLayer:AcceptanceTesting',
)
