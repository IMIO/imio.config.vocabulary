# -*- coding: utf-8 -*-

from imio.config.vocabulary.testing import NAKED_PLONE_INTEGRATION
from imio.config.vocabulary.testing import TEST_INSTALL_INTEGRATION  # noqa

from plone import api
from plone.app.testing import applyProfile

import unittest


class TestInstallDependencies(unittest.TestCase):

    layer = NAKED_PLONE_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_z3cformdatagridfield_is_dependency_of_config_vocabulary(self):
        """
        z3cform.datagridfield should be installed when we install imio.config.vocabulary
        """
        self.assertTrue(not self.installer.isProductInstalled('collective.z3cform.datagridfield'))
        applyProfile(self.portal, 'imio.config.vocabulary:default')
        self.assertTrue(self.installer.isProductInstalled('collective.z3cform.datagridfield'))


class TestSetup(unittest.TestCase):
    """
    Test that imio.config.vocabulary is properly installed.
    """

    layer = TEST_INSTALL_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """
        Test if imio.config.vocabulary is installed.
        """
        self.assertTrue(self.installer.isProductInstalled('imio.config.vocabulary'))

    def test_testing_profile_is_registered(self):
        """
        Test testing profile is registered.
        """
        portal_setup = api.portal.get_tool(name='portal_setup')
        demo_profile_name = u'imio.config.vocabulary:testing'
        profile_ids = [info['id'] for info in portal_setup.listProfileInfo()]
        msg = 'testing profile is not registered'
        self.assertTrue(demo_profile_name in profile_ids, msg)


class TestUninstall(unittest.TestCase):

    layer = TEST_INSTALL_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['imio.config.vocabulary'])

    def test_product_uninstalled(self):
        """Test if imio.config.vocabulary is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'imio.config.vocabulary'))
