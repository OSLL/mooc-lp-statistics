import unittest
import sys
from basic_selenium_test import BasicSeleniumTest

from test_admin_login import TestAdminLogin
from test_time_fltr_check import TestTimeFilterOnExist
from test_event_fltr_check import TestEventFilterOnExist
from test_event_list_check import TestEventListOnExist
from test_event_plus_button import TestEventPlusButton
from test_empty_field_alert import TestEmptyFieldAlert
from test_several_input_forms import TestSeveralInputForms

def main(host):
    suite = unittest.TestSuite()

    suite.addTest(BasicSeleniumTest.parametrize(TestAdminLogin,param=host))
    suite.addTest(BasicSeleniumTest.parametrize(TestTimeFilterOnExist,param=host))
    suite.addTest(BasicSeleniumTest.parametrize(TestEventFilterOnExist, param=host))
    suite.addTest(BasicSeleniumTest.parametrize(TestEventListOnExist, param=host))
    suite.addTest(BasicSeleniumTest.parametrize(TestEventPlusButton, param=host))
    suite.addTest(BasicSeleniumTest.parametrize(TestEmptyFieldAlert, param=host))
    suite.addTest(BasicSeleniumTest.parametrize(TestSeveralInputForms, param=host))

    returnCode = not unittest.TextTestRunner(
        verbosity=2).run(suite).wasSuccessful()
    BasicSeleniumTest.closeDriver()
    sys.exit(returnCode)

if __name__ == '__main__':
    host_arg = sys.argv[1]
    main(host_arg)