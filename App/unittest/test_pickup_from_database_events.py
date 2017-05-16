# -*- coding: utf-8 -*-
import unittest
import json
from datetime import datetime
from pymongo import MongoClient
import sys
sys.path.append("../")
from another_functions import pickup_from_database

class TestPickupFromDatabaseEvents(unittest.TestCase):
    def setUp(self):
        self.connection = MongoClient()
        self.db1 = self.connection.db_test
        self.collect = self.db1.collect
        date_one = datetime.strptime('2015-05-01 15:35:01.0', '%Y-%m-%d %H:%M:%S.%f')
        date_two = datetime.strptime('2015-05-02 15:35:01.0', '%Y-%m-%d %H:%M:%S.%f')
        date_three = datetime.strptime('2015-05-03 15:35:01.0', '%Y-%m-%d %H:%M:%S.%f')

        entry_one = {"Time": date_one, "UID": "1", "Event": "Test_Event_1"}
        entry_two = {"Time": date_two, "UID": "2", "Event": "Test_Event_2"}
        entry_three = {"Time": date_three, "UID": "3", "Event": "Test_Event_3"}
        entry_four = {"Time": date_one, "UID": "1", "Event": "Test_Event_11"}

        self.collect.insert_one(entry_one)
        self.collect.insert_one(entry_two)
        self.collect.insert_one(entry_three)
        self.collect.insert_one(entry_four)

    def tearDown(self):
        self.db1.collect.drop()

    def test_pickup_from_database_events(self):
        print("test_db contents: 'Test_Event_1', 'Test_Event_11','Test_Event_2','Test_Event_3'" )
        events = ["Test_Event_1", "Test_Event_2"]
        print('Testing events:', events)
        result_dict = pickup_from_database(data_base = self.db1, date_from='1015-05-16 15:35:01.0', date_to='3016-05-16 15:35:01.0', event=events)
        result_b = json.loads(result_dict["b"])
        print("Number events for the chart's legend = ", len(result_b) )
        self.assertEqual(len(result_b), 2)

        for elem in result_b:
            if (elem["Event"] == "Test_Event_1"):
                qty = elem["Result"][0]["count"]
        print("count 'Test_Event_1' = ", qty)
        self.assertEqual(qty, 2)

if __name__ == '__main__':
    unittest.main()