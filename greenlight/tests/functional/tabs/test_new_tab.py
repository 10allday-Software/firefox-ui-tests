# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from greenlight.harness.testcase import FirefoxTestCase
from greenlight.harness.decorators import uses_lib


class TestNewTab(FirefoxTestCase):
    def setUp(self):
        FirefoxTestCase.setUp(self)

        with self.marionette.using_context('content'):
            url = self.marionette.absolute_url('layout/mozilla.html')
            self.marionette.navigate(url)

    def tearDown(self):
        # TODO close active tab
        # bug 1088223: active_tab not working
        FirefoxTestCase.tearDown(self)

    @uses_lib('tabstrip', 'navbar', 'prefs')
    def test_open_tab_by_newtab_button(self):
        self.marionette.set_context('chrome')

        num_tabs = len(self.tabstrip.tabs)
        self.tabstrip.newtab_button.click()
        self.assertEqual(len(self.tabstrip.tabs), num_tabs + 1)

        newtab_url = self.prefs.get_pref('browser.newtab.url')
        self.assertEqual(self.navbar.location, newtab_url)
