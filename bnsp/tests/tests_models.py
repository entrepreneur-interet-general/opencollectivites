from bnsp.models import Query
from core.models import Document, Source
from django.db import IntegrityError
from django.test import TestCase

from bnsp.tests.testdata import data_objects
from unittest.mock import patch, MagicMock


class QueryTestCase(TestCase):
    def setUp(self) -> None:
        test_source = Source.objects.create(title="Test source")
        Query.objects.create(
            name="Test query", query='dc.title all "query"', source=test_source
        )

    def test_query_is_created(self) -> None:
        test_item = Query.objects.get(name="Test query")
        self.assertEqual(test_item.query, 'dc.title all "query"')

    def test_query_string_returns_the_title(self) -> None:
        test_item = Query.objects.get(name="Test query")
        self.assertEqual(str(test_item), "Test query")

    def test_query_name_is_unique(self) -> None:
        test_source = Source.objects.get(title="Test source")
        with self.assertRaises(IntegrityError):
            Query.objects.create(
                name="Test query", query='dc.title all "query2"', source=test_source
            )

    def test_query_chain_is_unique(self) -> None:
        test_source = Source.objects.get(title="Test source")
        with self.assertRaises(IntegrityError):
            Query.objects.create(
                name="Test query 2", query='dc.title all "query"', source=test_source
            )

    @patch("bnsp.models.GallicaSearch")
    def test_query_run(self, gallica_search_mock) -> None:
        test_item = Query.objects.get(name="Test query")

        self.assertIsNone(test_item.last_polled)

        gallica_search_mock_instance = MagicMock()
        gallica_search_mock_instance.fetch_records.return_value = None
        gallica_search_mock_instance.get_records.return_value = (
            data_objects.get_records_result
        )
        gallica_search_mock.return_value = gallica_search_mock_instance

        test_item.run()
        self.assertIsNotNone(test_item.last_polled)

        gallica_search_mock_instance.fetch_records.assert_called()
        gallica_search_mock_instance.get_records.assert_called()

        docs = Document.objects.all()
        self.assertEqual(docs.count(), 3)
