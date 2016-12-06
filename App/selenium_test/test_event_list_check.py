from App.selenium_test.basic_selenium_test import BasicSeleniumTest
from selenium import webdriver


TEST_URL = '/'
TEST_LIST_ID = 'list-group'



class TestEventListOnExist(BasicSeleniumTest):
    driver = webdriver.Chrome()
    driver.get(TEST_URL)
    list1 = driver.find_element_by_id(TEST_LIST_ID)

