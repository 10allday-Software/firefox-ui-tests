# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.errors import MarionetteException

from greenlight.harness.decorators import uses_lib
from greenlight.harness.testcase import FirefoxTestCase


class TestL10n(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)
        for tab in self.tabstrip.tabs:
            if len(self.tabstrip.tabs) > 1:
                self.tabstrip.tabs[-1].close()

    def tearDown(self):
        with self.marionette.using_context('content'):
            self.marionette.navigate('about:blank')
        FirefoxTestCase.tearDown(self)

    def test_dtd_entity_chrome(self):
        dtds = ['chrome://global/locale/filepicker.dtd',
                'chrome://browser/locale/baseMenuOverlay.dtd']

        value = self.l10n.get_localized_entity(dtds, 'helpSafeMode.label')
        elm = self.marionette.find_element('id', 'helpSafeMode')
        self.assertEqual(value, elm.get_attribute('label'))

        self.assertRaises(MarionetteException,
                          self.l10n.get_localized_entity,
                          dtds, 'notExistent')

    def test_dtd_entity_content(self):
        dtds = ['chrome://global/locale/filepicker.dtd',
                'chrome://global/locale/aboutSupport.dtd']

        value = self.l10n.get_localized_entity(dtds, 'aboutSupport.pageTitle')

        self.marionette.set_context(self.marionette.CONTEXT_CONTENT)
        self.marionette.navigate('about:support')

        elm = self.marionette.find_element('tag name', 'title')
        self.assertEqual(value, elm.text)

    def test_properties(self):
        properties = ['chrome://global/locale/filepicker.properties',
                      'chrome://global/locale/findbar.properties']

        # TODO: Find a way to verify the retrieved translated string
        value = self.l10n.get_localized_property(properties, 'NotFound')
        self.assertNotEqual(value, '')

        self.assertRaises(MarionetteException,
                          self.l10n.get_localized_property,
                          properties, 'notExistent')
