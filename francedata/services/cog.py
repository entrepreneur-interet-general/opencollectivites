import re

from francedata.services.datagouv import get_datagouv_file
from francedata.services.utils import (
    get_zip_from_url,
    parse_csv_from_distant_zip,
    parse_csv_from_url,
)
from francedata.models import (
    Commune,
    CommuneData,
    DataSource,
    Departement,
    DepartementData,
    Region,
    DataYear,
    Metadata,
    RegionData,
)


COG_ID = "58c984b088ee386cdb1261f3"
COG_MIN_YEAR = 2019


def import_regions_from_cog(year: int = 0) -> dict:
    region_regex = re.compile(r"Millésime (?P<year>\d{4})\s: Liste des régions")
    region_files = get_datagouv_file(COG_ID, region_regex, COG_MIN_YEAR)

    if not year:
        year = max(region_files)
    year_entry, _year_created = DataYear.objects.get_or_create(year=year)

    import_region_file = region_files[year]

    source_entry, _source_created = DataSource.objects.get_or_create(
        title=f"COG {import_region_file['title']}",
        url=import_region_file["url"],
        year=year_entry,
    )

    if year >= 2021:
        column_names = {
            "insee": "REG",
            "name": "LIBELLE",
            "seat_insee": "CHEFLIEU",
            "tncc": "TNCC",
            "nccenr": "NCCENR",
        }
    else:
        column_names = {
            "insee": "reg",
            "name": "libelle",
            "seat_insee": "cheflieu",
            "tncc": "tncc",
            "nccenr": "nccenr",
        }

    file_url = import_region_file["url"]
    print(f"🗜️   Parsing archive {file_url}")
    if file_url[-4:] == ".zip":
        regions = parse_csv_from_distant_zip(
            file_url,
            get_zip_from_url,
            f"region{year}.csv",
            column_names,
        )
    else:
        regions = parse_csv_from_url(
            file_url,
            column_names,
        )

    for region in regions:
        print(import_region_from_cog(region, year_entry, source_entry))

    Metadata.objects.get_or_create(prop="cog_regions_year", value=year)

    return {"year_entry": year_entry}


def import_region_from_cog(
    region: dict, year_entry: DataYear, source_entry: DataSource
) -> str:
    # Create or update region item
    entry, return_code = Region.objects.get_or_create(
        name=region["name"], insee=region["insee"]
    )
    entry.save()
    if not year_entry in entry.years.all():
        new_year = True
    else:
        new_year = False
    entry.years.add(year_entry)

    if return_code:
        return_message = f"Région {entry} created."
    elif new_year:
        return_message = f"Région {entry} already in database, updated year."
    else:
        return_message = f"Région {entry} already in database, skipped."

    # Import metadata
    metadata_keys = ["seat_insee", "tncc", "nccenr"]
    for md_key in metadata_keys:
        metadata_entry, _md_entry_created = RegionData.objects.get_or_create(
            region=entry,
            year=year_entry,
            datacode=md_key,
            datatype="string",
            value=region[md_key],
            source=source_entry,
        )
        metadata_entry.save()

    return return_message


def import_departements_from_cog(year):
    depts_regex = re.compile(r"Millésime (?P<year>\d{4})\s: Liste des départements")
    depts_files = get_datagouv_file(COG_ID, depts_regex, COG_MIN_YEAR)

    if not year:
        year = max(depts_files)
    year_entry, _year_created = DataYear.objects.get_or_create(year=year)

    import_dept_file = depts_files[year]

    source_entry, _source_created = DataSource.objects.get_or_create(
        title=f"COG {import_dept_file['title']}",
        url=import_dept_file["url"],
        year=year_entry,
    )

    if year >= 2021:
        column_names = {
            "insee": "DEP",
            "name": "LIBELLE",
            "region": "REG",
            "seat_insee": "CHEFLIEU",
            "tncc": "TNCC",
            "nccenr": "NCCENR",
        }
    else:
        column_names = {
            "insee": "dep",
            "name": "libelle",
            "region": "reg",
            "seat_insee": "cheflieu",
            "tncc": "tncc",
            "nccenr": "nccenr",
        }

    file_url = import_dept_file['url']
    print(f"🗜️   Parsing archive {file_url}")
    if file_url[-4:] == ".zip":
        depts = parse_csv_from_distant_zip(
            import_dept_file["url"],
            get_zip_from_url,
            f"departement{year}.csv",
            column_names,
        )
    else:
        depts = parse_csv_from_url(
            file_url,
            column_names,
        )


    for dept in depts:
        print(import_departement_from_cog(dept, year_entry, source_entry))

    Metadata.objects.get_or_create(prop="cog_depts_year", value=year)

    return {"year_entry": year_entry}


def import_departement_from_cog(
    dept: dict, year_entry: DataYear, source_entry: DataSource
) -> str:
    region = Region.objects.get(years=year_entry, insee=dept["region"])

    entry, return_code = Departement.objects.get_or_create(
        name=dept["name"], insee=dept["insee"], region=region
    )
    entry.save()

    if not year_entry in entry.years.all():
        new_year = True
    else:
        new_year = False
    entry.years.add(year_entry)

    if return_code:
        return_message = f"Département {entry} created."
    elif new_year:
        return_message = f"Département {entry} already in database, updated year."
    else:
        return_message = f"Département {entry} already in database, skipped."

    # Import metadata
    metadata_keys = ["seat_insee", "tncc", "nccenr"]
    for md_key in metadata_keys:
        metadata_entry, _md_entry_created = DepartementData.objects.get_or_create(
            departement=entry,
            year=year_entry,
            datacode=md_key,
            datatype="string",
            value=dept[md_key],
            source=source_entry,
        )
    metadata_entry.save()

    return return_message


def import_communes_from_cog(year):

    communes_regex = re.compile(r"^Millésime (?P<year>\d{4})\s:\s+Liste des communes")
    communes_files = get_datagouv_file(COG_ID, communes_regex, COG_MIN_YEAR)

    if not year:
        year = max(communes_files)
    year_entry, year_created = DataYear.objects.get_or_create(year=year)

    import_communes_file = communes_files[year]

    if year == 2019:
        csv_filename = "communes-01012019.csv"
    elif year == 2021:
        csv_filename = "commune2021.csv"
    else:
        csv_filename = f"communes{year}.csv"

    source_entry, _source_created = DataSource.objects.get_or_create(
        title=f"COG {import_communes_file['title']}",
        url=import_communes_file["url"],
        year=year_entry,
    )

    if year >= 2021:
        column_names = {
            "insee": "COM",
            "name": "LIBELLE",
            "dept": "DEP",
            "tncc": "TNCC",
            "nccenr": "NCCENR",
        }
        typecheck = {"column": "TYPECOM", "value": "COM"}
    else:
        column_names = {
            "insee": "com",
            "name": "libelle",
            "dept": "dep",
            "tncc": "tncc",
            "nccenr": "nccenr",
        }
        typecheck = {"column": "typecom", "value": "COM"}

    file_url = import_communes_file['url']
    print(f"🗜️   Parsing archive {import_communes_file['url']}")
    if file_url[-4:] == ".zip":
        communes = parse_csv_from_distant_zip(
            import_communes_file["url"],
            get_zip_from_url,
            csv_filename,
            column_names,
            typecheck=typecheck,
        )
    else:
        communes = parse_csv_from_url(
            file_url,
            column_names,
            typecheck=typecheck,
        )

    for commune in communes:
        print(import_commune_from_cog(commune, year_entry, source_entry))

    md_entry, md_created = Metadata.objects.get_or_create(
        prop="cog_communes_year", value=year
    )


def import_commune_from_cog(
    commune: dict, year_entry: DataYear, source_entry: DataSource
) -> str:
    dept = Departement.objects.get(years=year_entry, insee=commune["dept"])
    entry, return_code = Commune.objects.get_or_create(
        name=commune["name"], insee=commune["insee"], departement=dept
    )
    entry.save()

    if not year_entry in entry.years.all():
        new_year = True
    else:
        new_year = False
    entry.years.add(year_entry)

    if return_code:
        return_message = f"Commune {entry} created."
    elif new_year:
        return_message = f"Commune {entry} already in database, updated year."
    else:
        return_message = f"Commune {entry} already in database, skipped."

    # Import metadata
    metadata_keys = ["tncc", "nccenr"]
    for md_key in metadata_keys:
        metadata_entry, _md_created = CommuneData.objects.get_or_create(
            commune=entry,
            year=year_entry,
            datacode=md_key,
            datatype="string",
            value=commune[md_key],
            source=source_entry,
        )
        metadata_entry.save()

    return return_message
