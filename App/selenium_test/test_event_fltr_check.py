from basic_selenium_test import BasicSeleniumTest


TEST_URL = 'http://127.0.0.1:8000/'
TEST_FLTR_ID1 = 'first_event'
TEST_FLTR_ID2 = 'second_event'
TEST_FLTR_ID3 = 'third_event'


class TestEventFilterOnExist(BasicSeleniumTest):
    def testEventFilterOnExist(self):
        driver = self.getDriver()
        driver.get(self.getUrl(TEST_URL))
        filter1 = driver.find_element_by_id(TEST_FLTR_ID1)
        filter2 = driver.find_element_by_id(TEST_FLTR_ID2)
        filter3 = driver.find_element_by_id(TEST_FLTR_ID3)
