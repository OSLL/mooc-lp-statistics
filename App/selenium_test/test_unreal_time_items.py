from basic_selenium_test import BasicSeleniumTest


TEST_URL = 'http://127.0.0.1:8000/'
TEST_BTN_ID = 'show-res'
TEST_LST_CSS = '.prokrutka'
TEST_FLTR_FROM_ID = 'first_date'
TEST_FLTR_TO_ID = 'second_date'

class TestUnrealTimeItems(BasicSeleniumTest):
    def testUnrealTimeItems(self):
        driver = self.getDriver()
        driver.get(self.getUrl(TEST_URL))
        ffrom = driver.find_element_by_id(TEST_FLTR_FROM_ID)
        fto = driver.find_element_by_id(TEST_FLTR_TO_ID)
        ffrom.text = '1234-05-13 15:33:01.0'
        fto.text = '1234-05-16 15:35:01.0'
        button = driver.find_element_by_id(TEST_BTN_ID)
        button.click()
        listi = driver.find_element_by_css_selector(TEST_LST_CSS)
        self.assertEqual("",listi)




