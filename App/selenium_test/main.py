import unittest
import sys
from App.selenium_test.basic_selenium_test import BasicSeleniumTest
from App.selenium_test.test_event_fltr_check import TestEventFilterOnExist
from App.selenium_test.test_event_list_check import TestEventListOnExist
from App.selenium_test.test_time_fltr_check import TestTimeFilterOnExist


def main(host):
    suite = unittest.TestSuite()

    suite.addTest(BasicSeleniumTest.parametrize(TestTimeFilterOnExist,param=host))
    suite.addTest(BasicSeleniumTest.parametrize(TestEventFilterOnExist, param=host))
    suite.addTest(BasicSeleniumTest.parametrize(TestEventListOnExist, param=host))

    returnCode = not unittest.TextTestRunner(
        verbosity=2).run(suite).wasSuccessful()

    BasicSeleniumTest.closeDriver()
    sys.exit(returnCode)

if __name__ == '__main__':
    host_arg = sys.argv[1]
    main(host_arg)