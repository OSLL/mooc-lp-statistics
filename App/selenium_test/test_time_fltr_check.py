from basic_selenium_test import BasicSeleniumTest


TEST_URL = 'http://127.0.0.1:8000/'
TEST_FLTR_ID1 = 'first_date'
TEST_FLTR_ID2 = 'second_date'


class TestTimeFilterOnExist(BasicSeleniumTest):
    def testTimeFilterOnExist(self):
        driver = self.getDriver()
        driver.get(TEST_URL)
        filter1 = driver.find_element_by_id(TEST_FLTR_ID1)
        filter2 = driver.find_element_by_id(TEST_FLTR_ID2)

