from unittest import TestCase
from external_apis.services.opendatasoft_api import OpenDataSoftSearch


class OpenDataSoftSearchTestCase(TestCase):
    def setUp(self) -> None:
        self.test_ods = OpenDataSoftSearch()
        self.test_query_string = ""

    def test_search_instance_is_created(self) -> None:
        self.assertIsInstance(self.test_ods, OpenDataSoftSearch)

    def test_limit_can_be_set(self) -> None:
        self.test_ods.set_limit(50)
        self.assertEqual(self.test_ods.limit, 50)

    def test_limit_value_cant_be_below_one(self) -> None:
        self.test_ods.set_limit(0)
        self.assertEqual(self.test_ods.limit, 10)

    def test_limit_value_cant_be_above_100(self) -> None:
        self.test_ods.set_limit(101)
        self.assertEqual(self.test_ods.limit, 100)
