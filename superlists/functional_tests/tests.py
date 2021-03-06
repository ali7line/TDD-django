from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os


class NewVisitorTest(StaticLiveServerTestCase):

    def createBrowser(self):
        chrome_options = Options()
        chrome_options.add_argument('headless')
        # chrome_options.binary_location = '/usr/bin/google-chrome-stable'
        chrome_options.add_argument('window-size=1024x768')
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.implicitly_wait(10)
        return browser

    def setUp(self):
        self.browser = self.createBrowser()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            print('Found ENV variable: ' + staging_server + '\n')
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, raw_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_class_name('item_row')
        self.assertIn(raw_text, [row.text for row in rows])

    def enter_text_into_list(self, raw_text):
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(raw_text)
        inputbox.send_keys(Keys.ENTER)

    def test_visitor_cresates_list_and_retrieves_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)
        # She notices the page title and header mention to-do lists
        self.assertEqual('To-Do List', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do List', header_text)
        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual('Enter a to-do item', inputbox.get_attribute('placeholder'))

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        self.enter_text_into_list('Buy peacock feathers')

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)
        # The page updates again, and now shows both items on her list
        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.
        # She visits that URL - her to-do list is still there.
        # Satisfied, she goes back to sleep
        self.enter_text_into_list('Use peacock feather to make a fly')
        self.check_for_row_in_list_table('2: Use peacock feather to make a fly')
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.browser.quit()

        # A new user , Francis, comes along to the site
        # and sees a blank page asking him to enter new item
        self.browser = self.createBrowser()
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text

        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)
        # He adds an item and will be redirected to a new url (different from edith)
        self.enter_text_into_list('Buy milk')

        francis_list_url = self.browser.current_url
        self.assertNotEqual(edith_list_url, francis_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.check_for_row_in_list_table('1: Buy milk')

    def test_layout_styling(self):
        self.browser = self.createBrowser()
        self.browser.get(self.live_server_url)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
                inputbox.location['x'] + inputbox.size['width']/2,
                512,
                delta=5
                )
