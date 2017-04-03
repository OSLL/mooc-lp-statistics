from basic_selenium_test import BasicSeleniumTest


TEST_URL = '/'
TEST_BTN_ID = 'show-res'
TEST_CHECK_ID = 'popup-filter'

class TestEmptyFieldAlert(BasicSeleniumTest):
    def testEmptyFieldAlert(self):
        driver = self.getDriver()
        driver.get(self.getUrl(TEST_URL))

        button = driver.find_element_by_id(TEST_BTN_ID)
        button.click()
        alert_div = driver.find_element_by_id(TEST_CHECK_ID)
        self.assertTrue(alert_div.is_displayed())
