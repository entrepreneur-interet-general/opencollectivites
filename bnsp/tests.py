from bnsp.models import Query
from core.models import Source
from django.db import IntegrityError
from django.test import TestCase


class QueryTestCase(TestCase):
    def setUp(self) -> None:
        test_source = Source.objects.create(title="Test source")
        Query.objects.create(
            name="Test query", query='dc.name all "query"', source=test_source
        )

    def test_query_is_created(self) -> None:
        test_item = Query.objects.get(name="Test query")
        self.assertEqual(test_item.query, 'dc.name all "query"')

    def test_query_name_is_unique(self) -> None:
        test_source = Source.objects.get(title="Test source")
        with self.assertRaises(IntegrityError):
            Query.objects.create(
                name="Test query", query='dc.name all "query2"', source=test_source
            )

    def test_query_chain_is_unique(self) -> None:
        test_source = Source.objects.get(title="Test source")
        with self.assertRaises(IntegrityError):
            Query.objects.create(
                name="Test query 2", query='dc.name all "query"', source=test_source
            )
