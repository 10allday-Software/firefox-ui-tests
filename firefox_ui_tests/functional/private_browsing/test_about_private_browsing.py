# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import By, errors

from firefox_ui_harness.decorators import skip_if_e10s
from firefox_ui_harness.testcase import FirefoxTestCase


class TestAboutPrivateBrowsing(FirefoxTestCase):

    def setUp(self):
        FirefoxTestCase.setUp(self)
        self.pb_url = self.marionette.absolute_url('private_browsing/'
                                                   'about.html?')

    def tearDown(self):
        self.marionette.close()

    @skip_if_e10s
    def testCheckAboutPrivateBrowsing(self):
        self.assertFalse(self.browser.is_private)

        self.prefs.set_pref('app.support.baseURL', self.pb_url)

        with self.marionette.using_context('content'):
            self.marionette.navigate('about:privatebrowsing')

            description = self.browser.get_localized_entity(
                'aboutPrivateBrowsing.subtitle.normal')

            status_node = self.marionette.find_element(By.CSS_SELECTOR,
                                                       'p.showNormal')
            self.assertEqual(status_node.text, description)

            access_key = self.browser.get_localized_entity(
                'privatebrowsingpage.openPrivateWindow.accesskey')

            # Send keys to the top html element.
            top_html = self.marionette.find_element(By.TAG_NAME, 'html')
            top_html.send_keys(self.keys.SHIFT, self.keys.ACCEL, access_key)

        self.wait_for_condition(lambda mn: len(self.windows.all) == 2)
        self.windows.switch_to(lambda win: win.is_private)
        self.browser_pb = self.windows.current

        self.assertTrue(self.browser_pb.is_private)

        with self.marionette.using_context('content'):
            def find_element(mn):
                try:
                    link = self.marionette.find_element(By.ID, 'learnMore')
                    link.click()
                    return True
                except errors.NoSuchElementException:
                    return False

            self.wait_for_condition(find_element)

        self.assertEqual(len(self.browser.tabbar.tabs), 2,
                         "A new tab has been opened")

        target_url = self.pb_url + 'private-browsing'
        url_bar = self.marionette.find_element(By.ID, 'urlbar')

        # TODO: get_url does not correspond to what we want here.
        self.assertIn(url_bar.get_attribute('value'), target_url)

        self.browser_pb.close()

        # TODO: Can be removed once Marionette can directly close a window.
        # For now the opened tab gets closed first. See bug 1114623
        self.browser_pb.close()

        self.assertTrue(self.browser_pb.closed)
