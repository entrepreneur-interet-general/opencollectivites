from unittest import TestCase
from unittest.mock import patch
from bnsp.services.gallica_search_api import GallicaSearch, Record
import responses

from bnsp.tests.testdata import data_objects


class GallicaSearchTestCase(TestCase):
    def setUp(self) -> None:
        self.test_gs = GallicaSearch()
        self.test_query_string = 'dc.title all "jaune bleu"'
        self.test_query_full_url = (
            "https://gallica.bnf.fr/SRU"
            "?operation=searchRetrieve&version=1.2&maximumRecords=15"
            "&startRecord=1&query=dc.title+all+%22jaune+bleu%22"
        )
        with open("bnsp/tests/testdata/SRU_jaune_bleu_p1.xml", "r") as f:
            self.test_response_p1 = f.read()

        with open("bnsp/tests/testdata/SRU_jaune_bleu_p2.xml", "r") as f:
            self.test_response_p2 = f.read()

    def test_search_instance_is_created(self) -> None:
        self.assertIsInstance(self.test_gs, GallicaSearch)

    def test_max_records_can_be_set(self) -> None:
        self.test_gs.set_max_records(30)
        self.assertEqual(self.test_gs.max_records, 30)

    def test_sru_endpoint_can_be_set(self) -> None:
        test_endpoint = "https://nutrisco-patrimoine.lehavre.fr/SRU"
        self.test_gs.set_api_endpoint(test_endpoint)
        self.assertEqual(self.test_gs.api_endpoint, test_endpoint)

    def test_max_records_value_cant_be_below_one(self) -> None:
        self.test_gs.set_max_records(0)
        self.assertEqual(self.test_gs.max_records, 15)

    def test_max_records_value_cant_be_above_50(self) -> None:
        self.test_gs.set_max_records(60)
        self.assertEqual(self.test_gs.max_records, 15)

    def test_slow_mode_value_defaults_to_0(self) -> None:
        self.assertEqual(self.test_gs.slow_mode, 0)

    def test_slow_mode_value_can_be_set(self) -> None:
        self.test_gs.set_slow_mode(5)
        self.assertEqual(self.test_gs.slow_mode, 5)

    @responses.activate
    def test_gallica_search_retrieve_returns_the_expected_dict(self) -> None:
        responses.add(
            responses.GET,
            self.test_query_full_url,
            body=self.test_response_p1,
            status=200,
        )
        test_retrieve = self.test_gs.gallica_search_retrieve(self.test_query_string)
        self.assertEqual(list(test_retrieve.keys()), ["srw:searchRetrieveResponse"])

    @responses.activate
    def test_gallica_search_retries_on_error_500(self) -> None:
        responses.add(
            responses.GET,
            self.test_query_full_url,
            body="",
            status=500,
        )
        responses.add(
            responses.GET,
            self.test_query_full_url,
            body="",
            status=500,
        )
        responses.add(
            responses.GET,
            self.test_query_full_url,
            body=self.test_response_p1,
            status=200,
        )
        self.test_gs.set_slow_mode(0)
        self.test_gs.gallica_search_retrieve(self.test_query_string)
        self.assertEqual(len(responses.calls), 3)

    @responses.activate
    def test_gallica_search_retrieve_returns_an_error_if_no_valid_xml(self) -> None:
        responses.add(
            responses.GET,
            self.test_query_full_url,
            body="No valid XML here",
            status=200,
        )
        with self.assertRaises(ValueError):
            self.test_gs.gallica_search_retrieve(self.test_query_string)

    @responses.activate
    def test_count_records_returns_the_expected_dict(self) -> None:
        responses.add(
            responses.GET,
            self.test_query_full_url,
            body=self.test_response_p1,
            status=200,
        )
        test_count = self.test_gs.count_records(self.test_query_string)
        self.assertEqual(test_count, {"total_records": 61})

    @responses.activate
    def test_fetch_records_gets_all_the_pages(self) -> None:
        test_query_full_url_p1 = (
            "https://gallica.bnf.fr/SRU"
            "?operation=searchRetrieve&version=1.2&maximumRecords=50"
            "&startRecord=1&query=dc.title+all+%22jaune+bleu%22"
        )
        test_query_full_url_p2 = (
            "https://gallica.bnf.fr/SRU"
            "?operation=searchRetrieve&version=1.2&maximumRecords=50"
            "&startRecord=51&query=dc.title+all+%22jaune+bleu%22"
        )

        responses.add(
            responses.GET,
            test_query_full_url_p1,
            body=self.test_response_p1,
            status=200,
        )
        responses.add(
            responses.GET,
            test_query_full_url_p2,
            body=self.test_response_p2,
            status=200,
        )

        self.test_gs.set_max_records(50)
        self.test_gs.fetch_records(self.test_query_string)
        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(len(self.test_gs.records), 61)
        self.assertEqual(len(self.test_gs.get_records()), 61)


class RecordTestCase(TestCase):
    def setUp(self) -> None:
        self.test_record = Record(data_objects.sample_raw_record)

    def test_record_instance_is_created(self) -> None:
        self.assertIsInstance(self.test_record, Record)

    def test_get_values_returns_a_list(self) -> None:
        two_items_list = self.test_record.get_values("dc:language")
        self.assertEqual(two_items_list, ["fre", "français"])

        one_item_list = self.test_record.get_values("dc:date")
        self.assertEqual(one_item_list, ["1906"])

        no_item_list = self.test_record.get_values("missing_key")
        self.assertEqual(no_item_list, [])

    def test_get_first_value_returns_a_str(self) -> None:
        two_items_first = self.test_record.get_first_value("dc:language")
        self.assertEqual(two_items_first, "fre")

        one_item_first = self.test_record.get_first_value("dc:date")
        self.assertEqual(one_item_first, "1906")

        no_item_first = self.test_record.get_first_value("missing_key")
        self.assertEqual(no_item_first, "")

    def test_set_date_has_stored_the_date_at_init(self) -> None:
        self.assertEqual(self.test_record.date, "1906")

    def test_set_ark_has_stored_the_ark_at_init(self) -> None:
        self.assertEqual(
            self.test_record.ark_url, "https://gallica.bnf.fr/ark:/12148/btv1b10547034q"
        )
        self.assertEqual(self.test_record.ark_id, "btv1b10547034q")

    def test_set_ark_finds_a_url_if_no_url_matching_arkroot_is_present(self) -> None:
        test_record = Record(data_objects.sample_raw_record_bad_ids)
        self.assertEqual(test_record.ark_url, "https://sample-site.fr/sample_id")

    def test_get_thumbnail(self) -> None:
        self.assertEqual(
            self.test_record.get_thumbnail(),
            "https://gallica.bnf.fr/ark:/12148/btv1b10547034q/container1",
        )
