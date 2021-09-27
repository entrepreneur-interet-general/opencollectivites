import logging
import time
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
import requests

import xmltodict

from xml.parsers.expat import ExpatError


class GallicaSearch:
    # API defaults
    DEFAULT_API_ENDPOINT = "https://gallica.bnf.fr/SRU"
    DEFAULT_MAX_RECORDS = 15  # Max: 50
    DEFAULT_START_RECORD = 1
    DEFAULT_MAX_RETRIES = 3

    def __init__(
        self,
        max_records: int = DEFAULT_MAX_RECORDS,
        endpoint: str = DEFAULT_API_ENDPOINT,
    ) -> None:
        self.set_max_records(max_records)
        self.set_api_endpoint(endpoint)
        self.raw_records = []
        self.total_records = 0
        self.records = {}
        self.slow_mode = 0

    def set_max_records(self, max_records: int) -> None:
        """
        Set the value of the max_records parameter (1-50)
        """
        if not isinstance(max_records, int):
            raise ValueError("Error: max_records must be an integer between 1 and 50")

        if 0 < max_records <= 50:
            self.max_records = max_records
        else:
            self.max_records = self.DEFAULT_MAX_RECORDS

    def set_api_endpoint(self, endpoint: str) -> None:
        """
        Changes the SRU API endpoint.

        param:
        - endpoint: the base URL of the SRU on a white-label version of Gallica
          (ex: "https://nutrisco-patrimoine.lehavre.fr/SRU")
        """
        self.api_endpoint = endpoint

    def set_slow_mode(self, slow_mode: float = 0) -> None:
        """
        Set the value of the slow_mode parameter (defaults to zero)
        if set, adds a waiting time between requests
        """
        if slow_mode > 0:
            self.slow_mode = slow_mode

    def gallica_search_retrieve(
        self,
        query: str,
        start_record: int = DEFAULT_START_RECORD,
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

            response = requests.get(self.api_endpoint, params=payload)

            retries = self.DEFAULT_MAX_RETRIES
            if response.status_code == 500:
                while retries:
                    logging.warning(f"Error 500, retrying (retries: {retries})")
                    time.sleep(5)
                    response = requests.get(self.api_endpoint, params=payload)
                    if response.status_code == 200:
                        break
                    else:
                        retries -= 1

            return xmltodict.parse(response.content)
        except ExpatError:
            raise ValueError(
                "The API endpoint did not return XML content. This is likely the result of an invalid query."
            )

    def count_records(self, query: str) -> dict:
        """
        Retrieve the expected number of records for a query.
        """
        results = self.gallica_search_retrieve(query)
        srr = results["srw:searchRetrieveResponse"]

        self.total_records = int(srr["srw:numberOfRecords"])

        return {"total_records": self.total_records}

    def fetch_records(self, query: str) -> None:
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
            logging.info("The research returned no (new) results.")

    def parse_records(self) -> None:
        for raw in self.raw_records:
            raw = dict(raw)
            record = Record(raw)
            self.records[record.ark_id] = record

    def get_records(self) -> dict:
        """
        Returns the dict with the records
        """
        return self.records


class Record:
    def __init__(self, raw: dict) -> None:
        self.raw = raw
        self.set_ark()
        self.set_date()
        self.ark_id = self.ark_url.split("/")[-1]
        self.title = self.get_first_value("dc:title")

    def get_values(self, key: str) -> list:
        """
        A datapoint can either be a string or a list of strings.

        This function casts everything into a list to streamline the parsing.

        It also returns an empty list if the key is missing in the record.
        """
        if key in self.raw:
            values = self.raw[key]

            if isinstance(values, str):
                values = [values]
        else:
            values = []

        return values

    def get_first_value(self, key: str) -> str:
        """
        Returns the first value, or an empty string if no value is present
        """
        values = self.get_values(key)
        if len(values):
            return values[0]
        else:
            return ""

    def set_date(self) -> None:
        """
        Stores the 'dc:date' value as a string
        """
        if "dc:date" in self.raw:
            date = self.get_first_value("dc:date")

            # Manage some common bad values
            if date == "[S.d.]":
                date = ""

            if "à nos jours" in date:
                date = ""

            # If a date range is provided, only keep the latest year
            if "-" in date:
                date_range = date.split("-")
                date = date_range[-1]
            self.date = date

        else:
            self.date = ""

    def set_ark(self, ark_root="https://gallica.bnf.fr/ark") -> str:
        ids = self.get_values("dc:identifier")

        self.ark_url = ""
        # First, check for the proper Gallica ark
        for id in ids:
            if ark_root in id:
                self.ark_url = id

        # Else, check for any URL
        if not self.ark_url:
            url_validate = URLValidator()
            for id in ids:
                try:
                    url_validate(id)
                    self.ark_url = id
                except ValidationError:
                    pass

        return self.ark_url

    def get_thumbnail(self) -> str:
        return f"{self.ark_url}/container1"
