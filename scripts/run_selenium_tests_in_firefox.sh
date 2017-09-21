#!/bin/bash

CATALOG='mooc-lp-statistics'

echo
echo "==================== SELENIUMTESTS ====================="
echo

cd App/selenium_test
PATH=./:$PATH python ./main.py http://mooc-lp-statistics/
