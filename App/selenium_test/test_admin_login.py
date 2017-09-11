from basic_selenium_test import BasicSeleniumTest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

TEST_URL = '/'
DEFAULT_LOGIN='testSeleniumLogin'
DEFAULT_PASSWORD='testSeleniumPassword'

class TestAdminLogin(BasicSeleniumTest):

    def testAdminLogin(self):
        #BasicSeleniumTest.testAdminLogin(self)
        self.driver = self.getDriver()
        self.driver.get(self.getUrl(TEST_URL))

        username = self.driver.find_element_by_id('id_username')
        username.send_keys(DEFAULT_LOGIN)
        password = self.driver.find_element_by_id('id_password')
        password.send_keys(DEFAULT_PASSWORD)
        submitButton = self.driver.find_element_by_xpath("//input[@type='submit' and @value='Log in']")
        submitButton.click()
        timeout = 5
        try:
            element_present = EC.presence_of_element_located((By.ID, 'show-res'))
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            print ("Timed out waiting for page to load")

