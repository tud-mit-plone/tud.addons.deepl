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
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=tud.addons.deepl)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'tud.addons.deepl:default')


TUD_ADDONS_DEEPL_FIXTURE = TudAddonsDeeplLayer()


TUD_ADDONS_DEEPL_INTEGRATION_TESTING = IntegrationTesting(
    bases=(TUD_ADDONS_DEEPL_FIXTURE,),
    name='TudAddonsDeeplLayer:IntegrationTesting',
)


TUD_ADDONS_DEEPL_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(TUD_ADDONS_DEEPL_FIXTURE,),
    name='TudAddonsDeeplLayer:FunctionalTesting',
)


TUD_ADDONS_DEEPL_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        TUD_ADDONS_DEEPL_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='TudAddonsDeeplLayer:AcceptanceTesting',
)
