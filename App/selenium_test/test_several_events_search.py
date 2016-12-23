from App.selenium_test.basic_selenium_test import BasicSeleniumTest


TEST_URL = '/'
TEST_BTN_ID = 'show-res'
TEST_LST_CSS = '.prokrutka'
TEST_CHECK_ID1 = 'first_event'


class TestSeveralEventsSearch(BasicSeleniumTest):
    def TestSeveralEventsSearch(self):
        driver = self.getDriver()
        driver.get(self.getUrl(TEST_URL))
        checkbox1 = driver.find_element_by_id(TEST_CHECK_ID1)

        button = driver.find_element_by_id(TEST_BTN_ID)
        checkbox1.click()
        eventText1 = 'pdaemon is already running'
        # add other events if u need
        # eventText2 = 'some other stuff'

        button.click()
        listi = driver.find_element_by_css_selector(TEST_LST_CSS)
        self.assertIn(eventText1,listi)


