import csv
import re
import requests
from zipfile import ZipFile
from io import BytesIO, StringIO
import openpyxl_dictreader
from datetime import datetime
from typing import Pattern

from francedata.models import Epci, Commune, DataYear, Metadata

from francedata.services.datagouv import get_datagouv_file

BANATIC_ID = "5e1f20058b4c414d3f94460d"


def import_commune_data_from_banatic(year: int = 0) -> None:
    # Imports the Siren <-> Insee table for Communes
    # Communes must have been imported beforehand from COG

    zip_url = "https://www.banatic.interieur.gouv.fr/V5/ressources/documents/document_reference/TableCorrespondanceSirenInsee.zip"
    print(f"🗜️   Parsing archive {zip_url}")

    zip_name = requests.get(zip_url).content

    with ZipFile(BytesIO(zip_name)) as zip_file:
        title_regex = re.compile(r"Banatic_SirenInsee(?P<year>\d{4})\.xlsx")
        annual_files = match_filenames_in_zip(zip_file, title_regex, starting_year=2014)

        if not year:
            year = max(annual_files)
        year_entry, _year_created = DataYear.objects.get_or_create(year=year)
        print(f"Importing data for year {year_entry}")

        with zip_file.open(annual_files[year]) as xlsx_file:
            reader = openpyxl_dictreader.DictReader(xlsx_file, "insee_siren")
            for row in reader:
                print(f"Importing row data for {row['nom_com']} ({row['insee']})")
                import_commune_row_from_banatic(row, year_entry)

        Metadata.objects.get_or_create(prop="banatic_communes_year", value=year)


def import_commune_row_from_banatic(row: dict, year_entry: DataYear) -> None:
    name = row["nom_com"]
    insee = row["insee"]
    try:
        commune = Commune.objects.get(years=year_entry, insee=insee)
        if commune.name != name:
            print(
                f"Commune name {name} ({insee}) doesn't match with database entry {commune}"
            )
        commune.siren = row["siren"]
        pop_col = f"ptot_{year_entry.year}"
        commune.population = row[pop_col]
        commune.save()
    except:
        raise ValueError(f"Commune {name} ({insee}) not found")


def import_epci_data_from_banatic(year: int) -> None:
    # Imports the EPCIs and EPCI <=> communes relations
    # Communes must have been imported beforehand from COG

    epci_regex = re.compile(
        r"Périmètre des EPCI à fiscalité propre - année (?P<year>\d{4})"
    )
    epci_files = get_datagouv_file(BANATIC_ID, epci_regex)

    if not year:
        year = max(epci_files)

    epci_filename = epci_files[year]["url"]

    year_entry, _year_created = DataYear.objects.get_or_create(year=year)

    print(f"🧮   Parsing spreadsheet {epci_filename}")

    # Despite its .xls extension, it is actually a tsv.
    tsv_bytes = requests.get(epci_filename).content
    str_file = StringIO(tsv_bytes.decode("cp1252"), newline="\n")
    reader = csv.DictReader(str_file, delimiter="\t")

    list_reader = list(reader)

    rows_count = len(list_reader)

    if rows_count:
        print(f"Importing {rows_count} entries.")
        epci_sirens = []

        column_keys = {
            "epci_name": "Nom du groupement",
            "epci_type": "Nature juridique",
            "epci_siren": "N° SIREN",
            "member_siren": "Siren membre",
        }
        
        for row in list_reader:
            siren = row["N° SIREN"]
            if siren not in epci_sirens:
                print(import_epci_row_from_banatic(row, year_entry, column_keys))
                epci_sirens.append(siren)

        Metadata.objects.get_or_create(prop="banatic_epci_year", value=year)
    else:
        raise ValueError("The spreadsheet is empty")


def import_epci_row_from_banatic(row, year_entry, column_keys) -> str:
    epci_name_key = column_keys["epci_name"]
    epci_name = row[epci_name_key]

    epci_type_key = column_keys["epci_type"]
    epci_type = row[epci_type_key]

    epci_siren_key = column_keys["epci_siren"]
    epci_siren = row[epci_siren_key]

    member_siren_key = column_keys["member_siren"]
    member_siren = row[member_siren_key]
    member_commune = Commune.objects.get(siren=member_siren, years=year_entry)

    # Get or create the EPCI
    epci_entry, return_code = Epci.objects.get_or_create(
        siren=epci_siren,
        defaults={
            "name": epci_name,
            "epci_type": epci_type,
        },
    )
    epci_entry.save()

    if not year_entry in epci_entry.years.all():
        new_year = True
    else:
        new_year = False
    epci_entry.years.add(year_entry)

    if return_code:
        return_message = f"EPCI {epci_entry} created."
    elif new_year:
        return_message = f"EPCI {epci_entry} already in database, updated year."
    else:
        return_message = f"EPCI {epci_entry} already in database, skipped."

    # Adds the membership data on the communes entries
    member_commune.epci = epci_entry
    member_commune.save()

    return return_message


def first_day_of_quarter(dt: datetime = None, format: str = "%Y-%m-%d") -> str:
    # Returns the first day of the quarter the provided date belongs to
    # If no date is specified, use the current one
    if dt is None:
        dt = datetime.now()
    first_day_of_quarter = datetime(dt.year, 3 * ((dt.month - 1) // 3) + 1, 1)
    return first_day_of_quarter.strftime(format)


def match_filenames_in_zip(
    zip_file: ZipFile, title_regex: Pattern[str], starting_year: int = 0
) -> dict:
    files_in_zip = zip_file.namelist()
    annual_files = {}

    for f in files_in_zip:
        m = title_regex.match(f)
        if m:
            matched_year = int(m.group("year"))
            if matched_year >= starting_year:
                annual_files[matched_year] = f

    return annual_files
