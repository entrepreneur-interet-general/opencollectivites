from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.test import override_settings

from francedata.models import (
    Commune,
    CommuneData,
    DataMapping,
    DataSourceFile,
    DepartementData,
    Epci,
    DataSource,
    DataYear,
    Departement,
    EpciData,
    Metadata,
    Region,
    RegionData,
)

from francedata.tests.testdata.sample_data import sample_commune_mapping

import json


class MetadataTestCase(TestCase):
    def setUp(self) -> None:
        Metadata.objects.create(prop="Test", value="first")
        Metadata.objects.create(prop="Test", value="second")

    def test_metadata_is_created(self) -> None:
        test_item = Metadata.objects.get(prop="Test", value="first")
        self.assertEqual(test_item.value, "first")

    def test_metadata_prop_can_have_several_values(self) -> None:
        test_items = Metadata.objects.filter(prop="Test")
        self.assertEqual(test_items.count(), 2)


class DataYearTestCase(TestCase):
    def setUp(self) -> None:
        DataYear.objects.create(year=2020)

    def test_datayear_is_created(self) -> None:
        test_item = DataYear.objects.get(year=2020)
        self.assertEqual(test_item.year, 2020)

    def test_datayear_has_no_duplicate(self) -> None:
        with self.assertRaises(IntegrityError):
            DataYear.objects.create(year=2020)


class DataSourceTestCase(TestCase):
    def setUp(self) -> None:
        year = DataYear.objects.create(year=2020)
        DataSource.objects.create(
            title="Test title", url="http://test-url.com", year=year
        )

    def test_datasource_is_created(self) -> None:
        test_item = DataSource.objects.get(year__year=2020)
        self.assertEqual(test_item.title, "Test title")
        self.assertEqual(test_item.url, "http://test-url.com")

    def test_datasource_has_no_duplicate(self) -> None:
        with self.assertRaises(IntegrityError):
            year = DataYear.objects.create(year=2020)
            DataSource.objects.create(
                title="Test title", url="http://test-url.com", year=year
            )

    def test_datasource_has_title_as_public_label_by_default(self) -> None:
        test_item = DataSource.objects.get(year__year=2020)
        self.assertEqual(test_item.get_public_label(), "Test title (2020)")

    def test_datasource_public_label_can_be_set(self) -> None:
        test_item = DataSource.objects.get(year__year=2020)
        test_item.public_label = "Manually set public label"
        self.assertEqual(test_item.get_public_label(), "Manually set public label")


class DataMappingTestCase(TestCase):
    def setUp(self) -> None:
        test_item = DataMapping.objects.create(
            name="Test mapping",
            file_format="xlsx",
            mapping=json.loads(sample_commune_mapping),
        )

    def test_mapping_is_created(self) -> None:
        test_item = DataMapping.objects.get(name="Test mapping")
        self.assertEqual(str(test_item), "Test mapping")
        self.assertEqual(test_item.mapping["insee_key"], "CodeInsee")


@override_settings(MEDIA_ROOT="francedata/tests/testdata")
class DataSourceFileTestCase(TestCase):
    def setUp(self) -> None:
        mapping_excel = DataMapping.objects.create(
            name="Test mapping",
            file_format="excel",
            mapping=json.loads(sample_commune_mapping),
        )
        mapping_csv = DataMapping.objects.create(
            name="Test mapping",
            file_format="csv",
            mapping=json.loads(sample_commune_mapping),
        )

        year = DataYear.objects.create(year=2021)
        source_xlsx = DataSource.objects.create(title="Sample source - xlsx", year=year)
        source_csv = DataSource.objects.create(title="Sample source - csv", year=year)
        # Creating departements with 2-digit number, 3-digit number, numbers + letters, number with leading 0
        dept_01 = Departement.objects.create(insee="01", name="Ain")
        dept_2a = Departement.objects.create(insee="2A", name="Corse-du-Sud")
        dept_56 = Departement.objects.create(insee="56", name="Morbihan")
        dept_976 = Departement.objects.create(insee="976", name="Mayotte")

        dept_01.years.add(year)
        dept_2a.years.add(year)
        dept_56.years.add(year)
        dept_976.years.add(year)

        test_item_xlsx = DataSourceFile.objects.create(
            name="Test xlsx source file",
            data_file="sample_communes.xlsx",
            data_mapping=mapping_excel,
            source=source_xlsx,
        )

        test_item_csv = DataSourceFile.objects.create(
            name="Test csv source file",
            data_file="sample_communes.csv",
            data_mapping=mapping_csv,
            source=source_csv,
        )

    def test_source_file_is_created(self) -> None:
        test_item = DataSourceFile.objects.get(name="Test xlsx source file")
        self.assertEqual(str(test_item), "Test xlsx source file")

    def test_excel_source_file_can_be_imported(self) -> None:
        test_item = DataSourceFile.objects.get(name="Test xlsx source file")
        test_item.import_file_data()
        self.assertEqual(Commune.objects.all().count(), 12)
        self.assertEqual(CommuneData.objects.all().count(), 336)
        self.assertEqual(
            Commune.objects.get(insee="01001").name, "L'Abergement-Clémenciat"
        )
        self.assertEqual(
            CommuneData.objects.get(commune__insee="01001", datacode="pop_muni").value,
            "771",
        )
        self.assertEqual(
            CommuneData.objects.get(
                commune__insee="01001", datacode="pop_muni"
            ).datatype,
            "int",
        )

    def test_csv_source_file_can_be_imported(self) -> None:
        test_item = DataSourceFile.objects.get(name="Test csv source file")
        test_item.import_file_data()
        self.assertEqual(Commune.objects.all().count(), 12)
        self.assertEqual(CommuneData.objects.all().count(), 336)
        self.assertEqual(
            Commune.objects.get(insee="01001").name, "L'Abergement-Clémenciat"
        )
        self.assertEqual(
            CommuneData.objects.get(commune__insee="01001", datacode="pop_muni").value,
            "771",
        )
        self.assertEqual(
            CommuneData.objects.get(
                commune__insee="01001", datacode="pop_muni"
            ).datatype,
            "int",
        )

    def test_source_file_is_not_marked_as_imported_by_default(self) -> None:
        test_item = DataSourceFile.objects.get(name="Test xlsx source file")
        self.assertFalse(test_item.is_imported)
        self.assertIsNone(test_item.imported_at)

    def test_source_file_can_be_marked_as_imported(self) -> None:
        test_item = DataSourceFile.objects.get(name="Test xlsx source file")
        test_item.mark_imported()
        self.assertTrue(test_item.is_imported)
        self.assertIsNotNone(test_item.imported_at)


class RegionTestCase(TestCase):
    def setUp(self) -> None:
        test_item = Region.objects.create(insee=11, name="Test region")
        year1 = DataYear.objects.create(year=2020)
        year2 = DataYear.objects.create(year=2021)
        test_item.years.add(year1, year2)
        test_item.save()

        dept01 = Departement.objects.create(name="Dept 1", insee="01", region=test_item)
        dept02 = Departement.objects.create(name="Dept 2", insee="02", region=test_item)
        dept03 = Departement.objects.create(name="Dept 3", insee="03")

        Commune.objects.create(name="Commune 11", insee="01001", departement=dept01)
        Commune.objects.create(name="Commune 12", insee="01002", departement=dept01)
        Commune.objects.create(name="Commune 21", insee="02001", departement=dept02)
        Commune.objects.create(name="Commune 31", insee="03001", departement=dept03)

    def test_region_is_created(self) -> None:
        test_item = Region.objects.get(insee=11)
        self.assertEqual(test_item.name, "Test region")

    def test_region_has_years(self) -> None:
        test_item = Region.objects.get(insee=11)
        self.assertQuerysetEqual(
            test_item.years.values_list("year", flat=True), [2020, 2021], ordered=False
        )

    def test_region_has_no_duplicate(self) -> None:
        with self.assertRaises(ValidationError):
            Region.objects.create(insee=11, name="Test region")

    def test_region_cant_be_created_without_name(self) -> None:
        with self.assertRaises(ValidationError):
            Region.objects.create(insee=11, name="")

        with self.assertRaises(ValidationError):
            Region.objects.create(insee=11)

    def test_region_cant_be_created_without_insee(self) -> None:
        with self.assertRaises(ValidationError):
            Region.objects.create(name="Test region")

    def test_region_cant_be_created_with_invalid_insee(self) -> None:
        with self.assertRaises(ValidationError):
            Region.objects.create(name="Test region", insee="1")

        with self.assertRaises(ValidationError):
            Region.objects.create(name="Test region", insee="1A")

    def test_region_has_departements(self) -> None:
        test_region = Region.objects.get(insee=11)

        self.assertEqual(test_region.subdivisions_count()["departements"], 2)

    def test_region_has_communes(self) -> None:
        test_region = Region.objects.get(insee=11)

        self.assertEqual(test_region.subdivisions_count()["communes"], 3)

    def test_region_cant_have_invalid_siren(self) -> None:
        with self.assertRaises(ValidationError):
            test_region = Region.objects.get(insee=11)
            test_region.siren = "42"
            test_region.save()


class DepartementTestCase(TestCase):
    def setUp(self) -> None:
        region = Region.objects.create(insee="11", name="Test region")
        year1 = DataYear.objects.create(year=2020)
        year2 = DataYear.objects.create(year=2021)
        region.years.add(year1, year2)
        region.save()

        test_departement = Departement.objects.create(
            name="Test département", insee="01", region=region
        )
        test_departement.years.add(year1, year2)
        test_departement.save()

        epci1 = Epci.objects.create(name="EPCI 1", siren="200068989")

        epci2 = Epci.objects.create(name="EPCI 2", siren="200068989")

        Commune.objects.create(
            name="Commune 11", insee="01001", departement=test_departement, epci=epci1
        )
        Commune.objects.create(
            name="Commune 12", insee="01002", departement=test_departement, epci=epci2
        )

    def test_departement_is_created(self) -> None:
        test_item = Departement.objects.get(insee="01")
        self.assertEqual(test_item.name, "Test département")

    def test_departement_has_years(self) -> None:
        test_item = Departement.objects.get(insee="01")
        self.assertQuerysetEqual(
            test_item.years.values_list("year", flat=True), [2020, 2021], ordered=False
        )

    def test_departement_cant_be_created_without_name(self) -> None:
        with self.assertRaises(ValidationError):
            Departement.objects.create(insee="02", name="")

        with self.assertRaises(ValidationError):
            Departement.objects.create(insee="03")

    def test_departement_cant_be_created_without_insee(self) -> None:
        with self.assertRaises(ValidationError):
            Departement.objects.create(name="Test departement")

    def test_departement_cant_be_created_with_invalid_insee(self) -> None:
        with self.assertRaises(ValidationError):
            Departement.objects.create(name="Test departement", insee="1")

        with self.assertRaises(ValidationError):
            Departement.objects.create(name="Test departement", insee="20")

        with self.assertRaises(ValidationError):
            Departement.objects.create(name="Test departement", insee="113")

    def test_departement_has_communes(self) -> None:
        test_item = Departement.objects.get(insee="01")

        self.assertEqual(test_item.commune_set.count(), 2)

    def test_departement_has_epcis(self) -> None:
        test_item = Departement.objects.get(insee="01")
        self.assertEqual(test_item.list_epcis().count(), 2)

    def test_departement_cant_have_invalid_siren(self) -> None:
        with self.assertRaises(ValidationError):
            test_item = Departement.objects.get(insee="01")
            test_item.siren = "42"
            test_item.save()


class EpciTestCase(TestCase):
    def setUp(self) -> None:
        year1 = DataYear.objects.create(year=2020)
        year2 = DataYear.objects.create(year=2021)

        test_epci = Epci.objects.create(name="Test EPCI", siren="200068989")
        test_epci.years.add(year1, year2)
        test_epci.save()

        dept1 = Departement.objects.create(name="dept 1", insee="01")
        dept2 = Departement.objects.create(name="dept 2", insee="01")

        Commune.objects.create(
            name="Commune 11", insee="01001", departement=dept1, epci=test_epci
        )
        Commune.objects.create(
            name="Commune 12", insee="01002", departement=dept1, epci=test_epci
        )
        Commune.objects.create(
            name="Commune 21", insee="02001", departement=dept2, epci=test_epci
        )

    def test_epci_is_created(self) -> None:
        test_item = Epci.objects.get(siren="200068989")
        self.assertEqual(test_item.name, "Test EPCI")

    def test_epci_cant_be_created_without_name(self) -> None:
        with self.assertRaises(ValidationError):
            Epci.objects.create(siren="200068989")

    def test_epci_cant_be_created_without_siren(self) -> None:
        with self.assertRaises(ValidationError):
            Epci.objects.create(name="Test EPCI")

    def test_epci_cant_be_created_with_invalid_siren(self) -> None:
        with self.assertRaises(ValidationError):
            Epci.objects.create(name="Test EPCI", siren="42")

    def test_epci_has_years(self) -> None:
        test_item = Epci.objects.get(siren="200068989")
        self.assertQuerysetEqual(
            test_item.years.values_list("year", flat=True), [2020, 2021], ordered=False
        )

    def test_epci_has_communes(self) -> None:
        test_item = Epci.objects.get(siren="200068989")

        self.assertEqual(test_item.commune_set.count(), 3)


class CommuneTestCase(TestCase):
    def setUp(self) -> None:
        year1 = DataYear.objects.create(year=2020)
        year2 = DataYear.objects.create(year=2021)

        epci = Epci.objects.create(name="Test EPCI", siren="200068989")

        dept = Departement.objects.create(name="dept 1", insee="01")

        test_item = Commune.objects.create(
            name="Test commune", insee="01001", departement=dept, epci=epci
        )
        test_item.years.add(year1, year2)
        test_item.save()

    def test_commune_is_created(self) -> None:
        test_item = Commune.objects.get(insee="01001")
        self.assertEqual(test_item.name, "Test commune")

    def test_commune_cant_be_created_without_name(self) -> None:
        dept = Departement.objects.get(insee="01")

        with self.assertRaises(ValidationError):
            Commune.objects.create(insee="01001", departement=dept)

    def test_commune_cant_be_created_without_insee(self) -> None:
        dept = Departement.objects.get(insee="01")

        with self.assertRaises(ValidationError):
            Commune.objects.create(name="Test commune", departement=dept)

        with self.assertRaises(ValidationError):
            Commune.objects.create(name="Test commune", insee="", departement=dept)

    def test_commune_cant_be_created_with_invalid_insee(self) -> None:
        dept = Departement.objects.get(insee="01")

        with self.assertRaises(ValidationError):
            Commune.objects.create(name="Test commune", insee="1001", departement=dept)

        with self.assertRaises(ValidationError):
            Commune.objects.create(name="Test commune", insee="2C001", departement=dept)

    def test_commune_cant_be_created_without_departement(self) -> None:
        with self.assertRaises(ValidationError):
            Commune.objects.create(insee="01001")

    def test_commune_cant_have_invalid_siren(self) -> None:
        with self.assertRaises(ValidationError):
            test_item = Commune.objects.get(insee="01001")
            test_item.siren = "42"
            test_item.save()

    def test_commune_slug_has_proper_characters(self) -> None:
        dept = Departement.objects.get(insee="01")
        test_item = Commune.objects.create(
            name="Le Bœuf étoilé", insee="01010", departement=dept
        )
        self.assertEqual(test_item.slug, "le-boeuf-etoile-01010")


class RegionDataTestCase(TestCase):
    def setUp(self) -> None:
        region = Region.objects.create(insee="11", name="Test region")
        year = DataYear.objects.create(year=2020)
        source = DataSource.objects.create(
            title="Test title", url="http://test-url.com", year=year
        )

        RegionData.objects.create(
            region=region,
            year=year,
            datacode="property",
            value="Test data item",
            source=source,
        )

    def test_region_data_is_created(self) -> None:
        test_item = RegionData.objects.get(
            region__insee="11", year__year=2020, datacode="property"
        )
        self.assertEqual(test_item.value, "Test data item")

    def test_region_data_is_unique_per_year(self) -> None:
        region = Region.objects.get(insee="11", name="Test region")
        year = DataYear.objects.get(year=2020)
        source = DataSource.objects.get(
            title="Test title", url="http://test-url.com", year=year
        )

        with self.assertRaises(IntegrityError):
            RegionData.objects.create(
                region=region,
                year=year,
                datacode="property",
                value="Test data duplicate",
                source=source,
            )


class DepartementDataTestCase(TestCase):
    def setUp(self) -> None:
        dept = Departement.objects.create(insee="11", name="Test departement")
        year = DataYear.objects.create(year=2020)
        source = DataSource.objects.create(
            title="Test title", url="http://test-url.com", year=year
        )

        DepartementData.objects.create(
            departement=dept,
            year=year,
            datacode="property",
            value="Test data item",
            source=source,
        )

    def test_departement_data_is_created(self) -> None:
        test_item = DepartementData.objects.get(
            departement__insee="11", year__year=2020, datacode="property"
        )
        self.assertEqual(test_item.value, "Test data item")

    def test_departement_data_is_unique_per_year(self) -> None:
        dept = Departement.objects.get(insee="11")
        year = DataYear.objects.get(year=2020)
        source = DataSource.objects.get(
            title="Test title", url="http://test-url.com", year=year
        )

        with self.assertRaises(IntegrityError):
            DepartementData.objects.create(
                departement=dept,
                year=year,
                datacode="property",
                value="Test data duplicate",
                source=source,
            )


class EpciDataTestCase(TestCase):
    def setUp(self) -> None:
        epci = Epci.objects.create(name="Test EPCI", siren="200068989")
        year = DataYear.objects.create(year=2020)
        source = DataSource.objects.create(
            title="Test title", url="http://test-url.com", year=year
        )

        EpciData.objects.create(
            epci=epci,
            year=year,
            datacode="property",
            value="Test data item",
            source=source,
        )

    def test_epci_data_is_created(self) -> None:
        test_item = EpciData.objects.get(
            epci__siren="200068989", year__year=2020, datacode="property"
        )
        self.assertEqual(test_item.value, "Test data item")

    def test_epci_data_is_unique_per_year(self) -> None:
        epci = Epci.objects.get(siren="200068989")
        year = DataYear.objects.get(year=2020)
        source = DataSource.objects.get(
            title="Test title", url="http://test-url.com", year=year
        )

        with self.assertRaises(IntegrityError):
            EpciData.objects.create(
                epci=epci,
                year=year,
                datacode="property",
                value="Test data duplicate",
                source=source,
            )


class DepartementDataTestCase(TestCase):
    def setUp(self) -> None:
        dept = Departement.objects.create(insee="11", name="Test departement")
        year = DataYear.objects.create(year=2020)
        source = DataSource.objects.create(
            title="Test title", url="http://test-url.com", year=year
        )
        commune = Commune.objects.create(
            name="Commune 11", insee="01001", departement=dept
        )

        CommuneData.objects.create(
            commune=commune,
            year=year,
            datacode="property",
            value="Test data item",
            source=source,
        )

    def test_commune_data_is_created(self) -> None:
        test_item = CommuneData.objects.get(
            commune__insee="01001", year__year=2020, datacode="property"
        )
        self.assertEqual(test_item.value, "Test data item")

    def test_commune_data_is_unique_per_year(self) -> None:
        commune = Commune.objects.get(insee="01001")
        year = DataYear.objects.get(year=2020)
        source = DataSource.objects.get(
            title="Test title", url="http://test-url.com", year=year
        )

        with self.assertRaises(IntegrityError):
            CommuneData.objects.create(
                commune=commune,
                year=year,
                datacode="property",
                value="Test data duplicate",
                source=source,
            )
