from basic_selenium_test import BasicSeleniumTest


TEST_URL = '/'
TEST_LIST_ID = 'list-group'



class TestEventListOnExist(BasicSeleniumTest):
    def testEventListOnExist(self):
        driver = self.getDriver()
        driver.get(self.getUrl(TEST_URL))
        list1 = driver.find_element_by_id(TEST_LIST_ID)

