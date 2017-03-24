from basic_selenium_test import BasicSeleniumTest


TEST_URL = '/'
TEST_BUTTON_CLASS = 'btn-add'


class TestEventPlusButton(BasicSeleniumTest):
    def testEventPressPlusButton(self):
        driver = self.getDriver()
        driver.get(self.getUrl(TEST_URL))
        i = 0
        while i < 5:
            button = driver.find_element_by_class_name(TEST_BUTTON_CLASS)
            button.click()
            i  = i + 1