import datetime
import unittest
import logging
import os
import pymongo
from components.zhvi.zhvi_data_gateway import (
    ZhviDataGateway,
    DB_COLLECTION_ZHVI_RECORDS
)
from components.zhvi.zhvi_history_item import ZhviHistoryItem
from components.zhvi.zhvi_record import ZhviRecord


class TestZhviNeighborhoodDataGateway(unittest.TestCase):

    def setUp(self) -> None:
        db_uri = os.getenv("ZHVI_DB_URI")
        if db_uri is None or db_uri == "":
            logging.fatal("Missing required ENV: $ZHVI_DB_URI")

        db_name = os.getenv("ZHVI_DB_NAME")
        if db_name is None or db_name == "":
            logging.fatal("Missing required ENV: $ZHVI_DB_NAME")

        self.gateway = ZhviDataGateway(db_uri=db_uri, db_name=db_name)

        client = pymongo.MongoClient(db_uri)
        db = client[db_name]
        self.collection = db[DB_COLLECTION_ZHVI_RECORDS]

    def test_create_neighborhood_record(self):
        self.collection.drop()
        record = ZhviRecord(
            region_id=1,
            size_rank=1,
            region_name="test_region_name",
            region_type="test_region_type",
            state_name="test_state_name",
            state="test_state",
            city="test_city",
            metro="test_metro",
            county_name="test_county_name",
            zhvi_history=[
                ZhviHistoryItem(
                    date=datetime.datetime(year=2000, month=1, day=31),
                    zhvi_value=75553.2814897809
                ),
                ZhviHistoryItem(
                    date=datetime.datetime(year=2000, month=2, day=29),
                    zhvi_value=75756.46950997740
                ),
            ]
        )
        self.gateway.create_zhvi_record(record)

        documents = self.collection.find()
        actual_document = documents[0]

        self.assertEqual(actual_document["region_id"], 1)
        self.assertEqual(actual_document["size_rank"], 1)
        self.assertEqual(actual_document["region_name"], "test_region_name")
        self.assertEqual(actual_document["region_type"], "test_region_type")
        self.assertEqual(actual_document["state_name"], "test_state_name")
        self.assertEqual(actual_document["state"], "test_state")
        self.assertEqual(actual_document["city"], "test_city")
        self.assertEqual(actual_document["metro"], "test_metro")
        self.assertEqual(actual_document["county_name"], "test_county_name")

        actual_history_1 = actual_document["zhvi_history"][0]
        self.assertEqual(datetime.date.isoformat(actual_history_1["date"]), "2000-01-31")
        self.assertEqual(actual_history_1["zhvi_value"], 75553.2814897809)
