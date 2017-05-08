import unittest
from pymongo import MongoClient
from another_functions import pickup_from_database

class TestPickupFromDatabaseEvents(unittest.TestCase):
    def setUp(self):
        print("start")
        self.connection = MongoClient()
        self.db = self.connection.local
        self.collection = self.db.collect
        entry_one = {"Time": "2015-05-01 15:35:01.0", "UID": "1", "Event": "Test_Event_1"}
        entry_two = {"Time": "2015-05-01 15:35:01.0", "UID": "2", "Event": "Test_Event_2"}
        entry_three = {"Time": "2015-05-01 15:35:01.0", "UID": "3", "Event": "Test_Event_3"}
        self.collection.insert_one(entry_one)
        self.collection.insert_one(entry_two)
        self.collection.insert_one(entry_three)
    
    def tearDown(self):
        self.db.collect.drop()

    def test_pickup_from_database_events(self):
        events = ["www"]
        #result = pickup_from_database(date_from='2015-05-01 15:35:01.0', date_to='2015-05-01 15:35:01.0', event=events, number=0, offset=0, interval="month")
        result = pickup_from_database('2016-05-01 15:35:01.0', '2016-06-30 15:35:01.0',events)    
        print(result.items())
        print(len(result["b"]))
        for elem in result["b"]:
            print(elem)   
        self.assertEqual(len(result["b"]), 2)

if __name__ == '__main__':
    unittest.main()
