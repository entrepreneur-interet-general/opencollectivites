from francedata.models import Commune, DataYear, Departement, Epci
from django.test import TestCase
from unittest import mock
import re
from datetime import datetime

from francedata.services.banatic import (
    first_day_of_quarter,
    import_commune_row_from_banatic,
    import_epci_row_from_banatic,
    match_filenames_in_zip,
)


class ZipTestCase(TestCase):
    MOCK_LISTING = [
        "Banatic_SirenInsee2011.xlsx",
        "Banatic_SirenInsee2014.xlsx",
        "Banatic_SirenInsee2015.xlsx",
        "Banatic_SirenInsee2021.xlsx",
    ]

    def test_match_filenames_in_zip(self) -> None:
        title_regex = re.compile(r"Banatic_SirenInsee(?P<year>\d{4})\.xlsx")
        with mock.patch("francedata.services.banatic.ZipFile") as MockZipFile:
            MockZipFile.return_value.namelist.return_value = self.MOCK_LISTING
            zip_file = MockZipFile()

            annual_files = match_filenames_in_zip(
                zip_file, title_regex, starting_year=2014
            )
            self.assertEqual(
                annual_files,
                {
                    2014: "Banatic_SirenInsee2014.xlsx",
                    2015: "Banatic_SirenInsee2015.xlsx",
                    2021: "Banatic_SirenInsee2021.xlsx",
                },
            )


class FirstDayOfQuarterTestCase(TestCase):
    def test_returns_first_day_of_current_quarter(self) -> None:
        with mock.patch("francedata.services.banatic.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2021, 7, 8, 16, 2, 56, 943674)
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

            self.assertEqual(first_day_of_quarter(), "2021-07-01")

    def test_returns_first_day_of_specified_quarter(self) -> None:
        test_date = datetime(2020, 5, 28, 16, 2, 56, 943674)
        self.assertEqual(first_day_of_quarter(test_date), "2020-04-01")

    def test_returns_formatted_date(self) -> None:
        test_date = datetime(2020, 11, 28, 16, 2, 56, 943674)
        self.assertEqual(
            first_day_of_quarter(test_date, format="%d/%m/%Y"), "01/10/2020"
        )


class ImportCommuneRowFromBanaticTestCase(TestCase):
    def setUp(self) -> None:
        year = DataYear.objects.create(year=2021)
        dept = Departement.objects.create(name="Mayotte", insee="976")

        commune = Commune.objects.create(name="Sada", insee="97616", departement=dept)

        commune.years.add(year)
        commune.save()

    def test_insert_commune_row_passes_if_commune_exists(self) -> None:
        year_entry = DataYear.objects.get(year=2021)

        test_row = {
            "insee": "97616",
            "nom_com": "Sada",
            "ptot_2021": 11619,
            "siren": 200008878,
        }

        import_commune_row_from_banatic(row=test_row, year_entry=year_entry)

        commune = Commune.objects.get(insee="97616", years=year_entry)
        self.assertEqual(commune.siren, "200008878")
        self.assertEqual(commune.population, 11619)

    def test_insert_commune_row_fails_if_commune_does_not_exist(self) -> None:
        with self.assertRaises(ValueError):

            year_entry = DataYear.objects.get(year=2021)

            test_row = {
                "insee": "97617",
                "nom_com": "Mauvaise commune",
                "ptot_2021": 11619,
                "siren": 200008878,
            }

            import_commune_row_from_banatic(row=test_row, year_entry=year_entry)


class ImportCommuneRowFromBanaticTestCase(TestCase):
    def setUp(self) -> None:
        year_entry = DataYear.objects.create(year=2021)
        dept = Departement.objects.create(name="Lot-et-Garonne", insee="47")

        commune = Commune.objects.create(
            name="Sainte-Colombe-de-Villeneuve",
            insee="47237",
            departement=dept,
            siren="214702375",
        )

        commune.years.add(year_entry)
        commune.save()

        test_row = {
            "Nom du groupement": "CA du Grand Villeneuvois",
            "Nature juridique": "CA",
            "N° SIREN": "200023307",
            "Siren membre": "214702375",
        }
        column_keys = {
            "epci_name": "Nom du groupement",
            "epci_type": "Nature juridique",
            "epci_siren": "N° SIREN",
            "member_siren": "Siren membre",
        }

        import_epci_row_from_banatic(
            row=test_row, year_entry=year_entry, column_keys=column_keys
        )

    def test_epci_is_created(self) -> None:
        year_entry = DataYear.objects.get(year=2021)
        test_item = Epci.objects.get(siren="200023307", years=year_entry)
        self.assertEqual(test_item.name, "CA du Grand Villeneuvois")

    def test_epci_is_added_to_commune(self) -> None:
        year_entry = DataYear.objects.get(year=2021)
        test_commune = Commune.objects.get(insee="47237", years=year_entry)
        test_epci = Epci.objects.get(siren="200023307", years=year_entry)
        self.assertEqual(test_commune.epci, test_epci)
