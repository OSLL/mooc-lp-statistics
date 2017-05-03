#!/bin/bash

echo
echo "==================== UNITTESTS ====================="
echo

cd App/unittest
python -m unittest test_pickup_from_database_events.py