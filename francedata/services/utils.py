from typing import Callable, Union
import requests
import pandas
from zipfile import ZipFile
from io import BytesIO, TextIOWrapper, StringIO
from importlib import resources

from django.db.models.fields.files import FieldFile

# Caution, we import two different types of DictReader here
from csv import DictReader


def parse_csv_from_distant_zip(
    zip_url: str,
    get_zip_method: Callable[[str], ZipFile],
    csv_name: str,
    column_names: dict,
    typecheck: dict = False,
) -> list:
    with get_zip_method(zip_url) as zip_file:
        with zip_file.open(csv_name) as csv_file:
            stream = TextIOWrapper(csv_file, encoding="utf-8-sig")
            return parse_csv_from_stream(stream, column_names, typecheck)


def parse_csv_from_url(
    file_url: str,
    column_names: dict,
    typecheck: dict = False,
    ):
    response = requests.get(file_url)
    response.encoding = response.apparent_encoding
    stream = StringIO(response.text)
    return parse_csv_from_stream(stream, column_names, typecheck)

def parse_csv_from_stream(
    stream,
    column_names: dict,
    typecheck: dict = False,
):
    reader = DictReader(stream)
    entries = []
    if typecheck:
        tc_col = typecheck["column"]
        tc_val = typecheck["value"]

    for row in reader:
        if typecheck:
            if row[tc_col] != tc_val:
                continue
        entry = {}
        # Parse all the columns
        for key, val in column_names.items():
            entry[key] = row[val]
        entries.append(entry)
    return entries


def add_sirens_and_categories(input_file, model_name, year_entry):
    with resources.open_text("francedata.resources", input_file) as input_csv:
        reader = DictReader(input_csv)
        for row in reader:
            insee = row["Insee"]
            siren = row["Siren"]
            category = row["CATEG"]

            if category != "ML":
                # The Métropole de Lyon is managed only at the EPCI level
                try:
                    collectivity_entry = model_name.objects.get(
                        insee=insee, years=year_entry
                    )
                    collectivity_entry.siren = siren
                    collectivity_entry.category = category
                    collectivity_entry.save()
                except:
                    print(f"{model_name} {insee} not found")


def file_exists_at_url(url: str) -> bool:
    r = requests.head(url)
    return r.status_code == requests.codes.ok


def get_zip_from_url(zip_url: str) -> ZipFile:
    zip_name = requests.get(zip_url).content
    zip_file = ZipFile(BytesIO(zip_name))
    return zip_file


def fieldfile_to_dictreader(
    data_file: FieldFile, file_format: str, file_params: dict = {}, year: int = 0
) -> DictReader:
    """
    Returns the data from the provided file as a DictReader.
    """
    if file_format == "csv":
        csv_data = data_file.read()
        if "newline" in file_params:
            newline = file_params["newline"]
        else:
            newline = "\n"

        if "encoding" in file_params:
            encoding = file_params["encoding"]
        else:
            encoding = "utf-8"

        str_file = StringIO(csv_data.decode(encoding), newline=newline)
        return DictReader(str_file)
    elif file_format == "excel":
        if "sheet_name" in file_params:
            sheet = file_params["sheet_name"]
        else:
            sheet = ""

        sheet = sheet.format(year=year)
        return excel_fieldfile_to_dictreader(data_file, sheet)
    else:
        raise ValueError("File format is not valid")


def excel_fieldfile_to_dictreader(
    data_file: FieldFile, sheet: Union[str, int] = 0
) -> DictReader:
    """
    Takes an excel file and return a DictReader object
    """
    dataframe = pandas.read_excel(data_file.read(), sheet, dtype="object")
    csv_string = dataframe.to_csv(index=False)
    return DictReader(csv_string.splitlines())
