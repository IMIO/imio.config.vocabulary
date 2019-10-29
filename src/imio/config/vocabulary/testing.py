# -*- coding: utf-8 -*-

from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing import z2

import transaction

import unittest

import imio.schedule


class NakedPloneLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        self.loadZCML(package=imio.schedule,
                      name='testing.zcml')
        # need to do this for archetypes products having 'initialize'
        # method for their content types in their __init__.py
        z2.installProduct(app, 'imio.dashboard')

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'imio.dashboard')


NAKED_PLONE_FIXTURE = NakedPloneLayer(
    name='NAKED_PLONE_FIXTURE'
)

NAKED_PLONE_INTEGRATION = IntegrationTesting(
    bases=(NAKED_PLONE_FIXTURE,),
    name='NAKED_PLONE_INTEGRATION'
)


class ConfigVocabularyLayer(NakedPloneLayer):

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'Products.CMFPlone:plone')
        applyProfile(portal, 'imio.schedule:default')

        # Login and create some test content
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        # Commit so that the test browser sees these objects
        transaction.commit()


TEST_INSTALL_FIXTURE = ConfigVocabularyLayer(
    name='TEST_INSTALL_FIXTURE'
)

TEST_INSTALL_INTEGRATION = IntegrationTesting(
    bases=(TEST_INSTALL_FIXTURE,),
    name='TEST_INSTALL_INTEGRATION'
)


TEST_INSTALL_FUNCTIONAL = FunctionalTesting(
    bases=(TEST_INSTALL_FIXTURE,),
    name='TEST_INSTALL_FUNCTIONAL'
)


class BaseTest(unittest.TestCase):
    """
    Helper class for tests.
    """

    def setUp(self):
        self.portal = self.layer['portal']


class BrowserTest(BaseTest):
    """
    Helper class for Browser tests.
    """

    def setUp(self):
        super(BrowserTest, self).setUp()
        self.browser = z2.Browser(self.portal)
        self.browser.handleErrors = False

    def browser_login(self, user, password):
        login(self.portal, user)
        self.browser.open(self.portal.absolute_url() + '/logout')
        self.browser.open(self.portal.absolute_url() + '/login_form')
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = password
        self.browser.getControl(name='submit').click()
