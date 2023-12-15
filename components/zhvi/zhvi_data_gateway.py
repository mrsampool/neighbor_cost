#!/usr/bin/env python3
import logging

import pymongo
from typing import List

from components.zhvi.zhvi_record import ZhviRecord
from components.zhvi.zhvi_history_item import ZhviHistoryItem

DB_COLLECTION_ZHVI_RECORDS = "zvhi_records"


class ZhviDataGateway:
    def __init__(self, db_uri: str, db_name: str):
        self.client = pymongo.MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db[DB_COLLECTION_ZHVI_RECORDS]

    def create_zhvi_record(
            self,
            record: ZhviRecord = None,
            region_id: int = 0,
            size_rank: int = 0,
            region_name: str = "",
            region_type: str = "",
            state_name: str = "",
            state: str = "",
            city: str = "",
            metro: str = "",
            county_name: str = "",
            zhvi_history: List[ZhviHistoryItem] = None
    ):
        if zhvi_history is None:
            zhvi_history = []
        if record is None:
            record = ZhviRecord(
                region_id=region_id,
                size_rank=size_rank,
                region_name=region_name,
                region_type=region_type,
                state_name=state_name,
                state=state,
                city=city,
                metro=metro,
                county_name=county_name,
                zhvi_history=zhvi_history
            )

        doc_history = []
        for item in record.zhvi_history:
            item_doc = {
                "date": item.date,
                "zhvi_value": item.zhvi_value
            }
            doc_history.append(item_doc)

        doc = {
            "region_id": record.region_id,
            "size_rank": record.size_rank,
            "region_name": record.region_name,
            "region_type": record.region_type,
            "state_name": record.state_name,
            "state": record.state,
            "city": record.city,
            "metro": record.metro,
            "county_name": record.county_name,
            "zhvi_history": doc_history
        }
        self.collection.update_one({"region_id": record.region_id}, {"$set": doc}, True)

    def get_regions_by_type(self, region_type: str):
        return self.collection.find({"region_type": region_type})

    def get_region_by_id(self, region_id) -> ZhviRecord:
        doc = self.collection.find_one({"region_id": region_id})
        return ZhviRecord(document=doc)

    def get_us_doc(self) -> ZhviRecord:
        doc = self.collection.find_one({"region_type": "country", "region_name": "United States"})
        return ZhviRecord(document=doc)
