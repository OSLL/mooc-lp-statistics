#!/bin/bash

echo
echo "==================== UNITTESTS ====================="
echo

EXIST_ERROR_TEST=1
NO_ERROR_TEST=0

cd App/unittest
PYTHONPATH=../../ python -m unittest discover -v 2>&1 | tee unittest.log

if grep -c 'FAIL' unittest.log
then
    exit $EXIST_ERROR_TEST
else
    exit $NO_ERROR_TEST
fi