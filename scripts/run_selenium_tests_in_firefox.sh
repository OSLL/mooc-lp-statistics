#!/bin/bash

echo
echo "==================== SELENIUMTESTS ====================="
echo

python ./manage.py createadminuser --login=testSeleniumLogin --email=admin@testSeleniumLogin.ru --password=testSeleniumPassword

cd App/selenium_test
PATH=./:$PATH python ./main.py http://mooc-lp-statistics/

python ../../manage.py createadminuser --login=testSeleniumLogin --email=admin@testSeleniumLogin.ru --password=testSeleniumPassword --delete=yes