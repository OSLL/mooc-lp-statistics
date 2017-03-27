from basic_selenium_test import BasicSeleniumTest


TEST_URL = '/'
TEST_FLTR_ID1 = 'first_date'
TEST_FLTR_ID2 = 'second_date'


class TestEventFilterOnExist(BasicSeleniumTest):
    def testEventFilterOnExist(self):
        driver = self.getDriver()
        driver.get(self.getUrl(TEST_URL))
        filter1 = driver.find_element_by_id(TEST_FLTR_ID1)
        filter2 = driver.find_element_by_id(TEST_FLTR_ID2)
