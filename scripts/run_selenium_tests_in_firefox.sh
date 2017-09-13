#!/bin/bash

CATALOG='mooc-lp-statistics'

echo
echo "==================== SELENIUMTESTS ====================="
echo

python /var/www/"$CATALOG"/manage.py createadminuser --login=testSeleniumLogin --email=admin@testSeleniumLogin.ru --password=testSeleniumPassword

cd App/selenium_test
PATH=./:$PATH python ./main.py http://mooc-lp-statistics/

python /var/www/"$CATALOG"/manage.py createadminuser --login=testSeleniumLogin --email=admin@testSeleniumLogin.ru --password=testSeleniumPassword --delete=yes
