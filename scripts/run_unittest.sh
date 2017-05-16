#!/bin/bash

echo
echo "==================== UNITTESTS ====================="
echo

cd App/unittest
PYTHONPATH=../../ python -m unittest discover -v 2>&1 | tee unittest.log
exit_code="${PIPESTATUS[0]}"
cat unittest.log
