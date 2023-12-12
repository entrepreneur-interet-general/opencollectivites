from francedata.models import (
    Commune,
    CommuneData,
    DataSource,
    DataYear,
    Departement,
    DepartementData,
    Region,
    RegionData,
)
from django.test import TestCase
from francedata.services.cog import (
    import_commune_from_cog,
    import_departement_from_cog,
    import_region_from_cog,
)


class ImportRegionFromCogTestCase(TestCase):
    def setUp(self) -> None:
        year_entry = DataYear.objects.create(year=2021)
        source_entry = DataSource.objects.create(
            title=f"COG test", url="https://test.com/regions.csv", year=year_entry
        )

        test_row = {
            "insee": "01",
            "name": "Guadeloupe",
            "seat_insee": "97105",
            "tncc": "3",
            "nccenr": "Guadeloupe",
        }

        import_region_from_cog(test_row, year_entry, source_entry)

    def test_region_is_created(self) -> None:
        test_item = Region.objects.get(insee="01")
        self.assertEqual(test_item.name, "Guadeloupe")

    def test_metadata_is_inserted(self) -> None:
        test_item = Region.objects.get(insee="01")
        test_data_seat = RegionData.objects.get(region=test_item, datacode="seat_insee")
        test_data_tncc = RegionData.objects.get(region=test_item, datacode="tncc")
        self.assertEqual(test_data_seat.value, "97105")
        self.assertEqual(test_data_tncc.value, "3")


class ImportDepartementFromCogTestCase(TestCase):
    def setUp(self) -> None:
        year_entry = DataYear.objects.create(year=2021)
        source_entry = DataSource.objects.create(
            title=f"COG test", url="https://test.com/departements.csv", year=year_entry
        )
        region = Region.objects.create(insee="06", name="Mayotte")
        region.years.add(year_entry)
        region.save()

        test_row = {
            "insee": "976",
            "name": "Mayotte",
            "nccenr": "Mayotte",
            "region": "06",
            "seat_insee": "97608",
            "tncc": "0",
        }

        import_departement_from_cog(test_row, year_entry, source_entry)

    def test_departement_is_created(self) -> None:
        test_item = Departement.objects.get(insee="976")
        self.assertEqual(test_item.name, "Mayotte")

    def test_metadata_is_inserted(self) -> None:
        test_item = Departement.objects.get(insee="976")
        test_data_seat = DepartementData.objects.get(
            departement=test_item, datacode="seat_insee"
        )
        test_data_tncc = DepartementData.objects.get(
            departement=test_item, datacode="tncc"
        )
        self.assertEqual(test_data_seat.value, "97608")
        self.assertEqual(test_data_tncc.value, "0")


class ImportCommuneFromCogTestCase(TestCase):
    def setUp(self) -> None:
        year_entry = DataYear.objects.create(year=2021)
        source_entry = DataSource.objects.create(
            title=f"COG test", url="https://test.com/communes.csv", year=year_entry
        )

        region = Region.objects.create(insee="06", name="Mayotte")
        region.years.add(year_entry)
        region.save()
        departement = Departement.objects.create(
            name="Mayotte", insee="976", region=region
        )
        departement.years.add(year_entry)
        departement.save()

        test_row = {
            "dept": "976",
            "insee": "97616",
            "name": "Sada",
            "nccenr": "Sada",
            "tncc": "0",
        }

        import_commune_from_cog(test_row, year_entry, source_entry)

    def test_commune_is_created(self) -> None:
        test_item = Commune.objects.get(insee="97616")
        self.assertEqual(test_item.name, "Sada")

    def test_metadata_is_inserted(self) -> None:
        test_item = Commune.objects.get(insee="97616")
        test_data_nccenr = CommuneData.objects.get(commune=test_item, datacode="nccenr")
        test_data_tncc = CommuneData.objects.get(commune=test_item, datacode="tncc")
        self.assertEqual(test_data_nccenr.value, "Sada")
        self.assertEqual(test_data_tncc.value, "0")
