from bnsp.models import Query
from django.test import TestCase


class QueryTestCase(TestCase):
    def setUp(self) -> None:
        Query.objects.create(name="Test", query='dc.name all "query"')

    def test_query_is_created(self) -> None:
        test_item = Query.objects.get(name="Test")
        self.assertEqual(test_item.query, 'dc.name all "query"')

    def test_query_name_is_unique(self) -> None:
        Query.objects.create(name="Test", query='dc.name all "query2"')

        test_item = Query.objects.get(name="Test")
        self.assertEqual(test_item.count(), 2)

    def test_query_chain_is_unique(self) -> None:
        Query.objects.create(name="Test 2", query='dc.name all "query"')
