import unittest
import logging
import os
import pymongo
from flask import Flask
from src.components.zhvi_neighborhoods.zhvi_neighborhood_data_gateway import (
    ZhviNeighborhoodDataGateway,
    DB_COLLECTION_NEIGHBORHOODS
)
from src.components.zhvi_neighborhoods.zhvi_neighborhood_record import ZhviNeighborhoodRecord


class TestZhviNeighborhoodDataGateway(unittest.TestCase):

    def setUp(self) -> None:
        db_uri = os.getenv("TEST_ZHVI_DB_URI")
        if db_uri is None or db_uri == "":
            logging.fatal("Missing required ENV: $TEST_ZHVI_DB_URI")

        db_name = os.getenv("TEST_ZHVI_DB_NAME")
        if db_name is None or db_name == "":
            logging.fatal("Missing required ENV: $TEST_ZHVI_DB_NAME")

        self.gateway = ZhviNeighborhoodDataGateway(db_uri=db_uri, db_name=db_name)

        client = pymongo.MongoClient(db_uri)
        db = client[db_name]
        self.collection = db[DB_COLLECTION_NEIGHBORHOODS]

    def test_create_neighborhoods_from_df(self):
        record = ZhviNeighborhoodRecord(
            region_id=1,
            size_rank=1,
            region_name="test_region_name",
            region_type="test_region_type",
            state_name="test_state_name",
            state="test_state",
            city="test_city",
            metro="test_metro",
            county_name="test_county_name",
        )
        self.gateway.create_neighborhood_record(record)

        documents = self.collection.find()
        document = documents[0]

        self.assertEqual(document["region_id"], 1)
        self.assertEqual(document["size_rank"], 1)
        self.assertEqual(document["region_name"], "test_region_name")
        self.assertEqual(document["region_type"], "test_region_type")
        self.assertEqual(document["state_name"], "test_state_name")
        self.assertEqual(document["state"], "test_state")
        self.assertEqual(document["city"], "test_city")
        self.assertEqual(document["metro"], "test_metro")
        self.assertEqual(document["county_name"], "test_county_name")
