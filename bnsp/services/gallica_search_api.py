from typing import List, Union
import time
import requests

import xmltodict

from xml.parsers.expat import ExpatError


class GallicaSearch:
    # API defaults
    API_ENDPOINT = "https://gallica.bnf.fr/SRU"
    MAX_RECORDS = 15  # Max: 50
    START_RECORD = 1
    MAX_RETRIES = 3

    def __init__(self, max_records: int = MAX_RECORDS) -> None:
        self.set_max_records(max_records)

        self.raw_records = []
        self.total_records = 0
        self.records = {}
        self.slow_mode = 0

    def set_max_records(self, max_records: int):
        """
        Set the value of the max_records parameter (1-50)
        """
        if not isinstance(max_records, int):
            raise ValueError("Error: max_records must be an integer between 1 and 50")

        if 0 < max_records <= 50:
            self.max_records = max_records
        else:
            self.max_records = self.MAX_RECORDS

    def set_slow_mode(self, slow_mode: float = 0):
        """
        Set the value of the slow_mode parameter (defaults to zero)
        if set, adds a waiting time between requests
        """
        if slow_mode > 0:
            self.slow_mode = slow_mode

    def gallica_search_retrieve(
        self,
        query: str,
        start_record: int = START_RECORD,
    ) -> dict:
        """
        Perform a query on the SRU endpoint
        """
        try:

            payload = {
                "operation": "searchRetrieve",
                "version": 1.2,
                "maximumRecords": self.max_records,
                "startRecord": start_record,
                "query": query,
            }

            response = requests.get(self.API_ENDPOINT, params=payload)

            retries = self.MAX_RETRIES
            if response.status_code == 500:
                while retries:
                    print(f"Error 500, retrying (retries: {retries})")
                    time.sleep(5)
                    response = requests.get(self.API_ENDPOINT, params=payload)
                    if response.status_code == 200:
                        break
                    else:
                        retries -= 1

            return xmltodict.parse(response.content)
        except ExpatError:
            # print(f"Problem with the query {query}. See returned page below")
            # print(response.content)
            raise ValueError(
                "The API endpoint did not return XML content. This is likely the result of an invalid query."
            )

    def count_records(self, query: str) -> int:
        """
        Retrieve the expected number of records for a query.
        """
        results = self.gallica_search_retrieve(query)
        srr = results["srw:searchRetrieveResponse"]

        self.total_records = int(srr["srw:numberOfRecords"])

        return {"total_records": self.total_records}

    def get_records(
        self,
        query: str,
    ) -> dict:
        """
        Retrieve the full lists of records for a query.
        Calls the gallica_search_retrieve recursively until all results are retrieved.
        """
        results = self.gallica_search_retrieve(query)
        srr = results["srw:searchRetrieveResponse"]

        total_records = int(srr["srw:numberOfRecords"])
        self.total_records = total_records

        if total_records > 0:
            next_record_position = int(srr["srw:nextRecordPosition"])

            local_raw_records = srr["srw:records"]["srw:record"]

            while next_record_position < total_records:
                if self.slow_mode:
                    time.sleep(self.slow_mode)
                results = self.gallica_search_retrieve(
                    query, start_record=next_record_position
                )
                srr = results["srw:searchRetrieveResponse"]
                next_record_position = int(srr["srw:nextRecordPosition"])

                new_records = srr["srw:records"]["srw:record"]
                local_raw_records.extend(new_records)

            for raw in local_raw_records:
                if "srw:recordData" in raw and "oai_dc:dc" in raw["srw:recordData"]:
                    record = raw["srw:recordData"]["oai_dc:dc"]

                    record["id"] = raw["srw:extraRecordData"]["uri"]

                    self.raw_records.append(record)

            self.parse_records()

        else:
            print("The research has no results")

        return {"records": self.raw_records, "total_records": self.total_records}

    def parse_records(self):
        for raw in self.raw_records:
            record = Record(raw)
            self.records[record.ark_id] = record


class Record:
    def __init__(self, raw: dict) -> None:
        self.raw = raw
        self.get_ark()
        self.ark_id = self.ark_url.split("/")[-1]
        self.title = raw["dc:title"]
        self.date = raw["dc:date"]

    def get_values(self, key: str) -> list:
        """
        A datapoint can either be a string or a list of strings.

        This function casts everything into a list to streamline the parsing.
        """
        values = self.raw[key]
        if isinstance(values, str):
            values = [values]

        return values

    def get_ark(self) -> str:
        ids = self.get_values("dc:identifier")

        for id in ids:
            if "https://gallica.bnf.fr/ark" in id:
                self.ark_url = id

        return self.ark_url

    def get_thumbnail(self) -> str:
        return f"{self.ark_url}/container1"
