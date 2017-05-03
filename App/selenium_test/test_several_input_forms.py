from basic_selenium_test import BasicSeleniumTest


TEST_URL = '/'
TEST_BUTTON_CLASS = 'btn-add'
TEST_INPUT_CLASS = 'get-input-from-fields'
TEST_DELETE_BUTTON_CLASS = 'btn-remove'
TEST_BUTTON_SUBMIT = 'show-res'


TEST_DATE_FROM_ID = 'first_date'
TEST_DATE_TO_ID = 'second_date'
TEST_DATE_FROM_VALUE = '2016-4-1 0:4:0.00'
TEST_DATE_TO_VALUE = '2016-5-31 0:5:0.00'

TEST_FILTER_VALUE_1 = 'www'
TEST_FILTER_VALUE_2 = 'pdaemon'

class TestSeveralInputForms(BasicSeleniumTest):

    def addFields(self, number):
        i = 0
        while i < number:
            button = self.driver.find_element_by_class_name(TEST_BUTTON_CLASS)
            button.click()
            i  = i + 1

    def getInputFieldsCount(self):
        inputs = self.driver.find_elements_by_class_name(TEST_INPUT_CLASS)
        return len(inputs)


    def deleteFields(self, number):
        i = 0
        while i < number:
            button = self.driver.find_element_by_class_name(TEST_DELETE_BUTTON_CLASS)
            button.click()
            i  = i + 1

    def setDatePeriod(self):
        firstDate = self.driver.find_element_by_id(TEST_DATE_FROM_ID)
        firstDate.clear()
        firstDate.send_keys(TEST_DATE_FROM_VALUE)
        secondDate = self.driver.find_element_by_id(TEST_DATE_TO_ID)
        secondDate.clear()
        secondDate.send_keys(TEST_DATE_TO_VALUE)

    def setFilters(self):
        inputs = self.driver.find_elements_by_class_name(TEST_INPUT_CLASS)

        inputs[0].send_keys(TEST_FILTER_VALUE_1)
        inputs[1].send_keys(TEST_FILTER_VALUE_2)


    def clickSubmitButton(self):
        btn_submit = self.driver.find_element_by_id(TEST_BUTTON_SUBMIT)
        btn_submit.click()


    def testSeveralInputForms(self):
        self.driver = self.getDriver()
        self.driver.get(self.getUrl(TEST_URL))

        self.addFields(3)
        self.assertEqual(self.getInputFieldsCount(),4)

        self.deleteFields(2)
        self.assertEqual(self.getInputFieldsCount(),2)

        self.setDatePeriod()
        self.setFilters()

        self.clickSubmitButton()
