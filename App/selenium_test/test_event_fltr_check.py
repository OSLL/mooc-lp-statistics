from App.selenium_test.basic_selenium_test import BasicSeleniumTest
from selenium import webdriver


TEST_URL = '/'
TEST_FLTR_ID1 = 'first_event'
TEST_FLTR_ID2 = 'second_event'
TEST_FLTR_ID3 = 'third_event'


class TestEventFilterOnExist(BasicSeleniumTest):
    driver = webdriver.Chrome()
    driver.get(TEST_URL)
    filter1 = driver.find_element_by_id(TEST_FLTR_ID1)
    filter2 = driver.find_element_by_id(TEST_FLTR_ID2)
    filter3 = driver.find_element_by_id(TEST_FLTR_ID3)
