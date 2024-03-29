import csv
from django.http.response import HttpResponse
from babel.numbers import format_decimal


def init_payload(page_title: str, links: list = []):
    # Returns the common payload passed to most pages:
    # title: the page title
    # breadcrumb_data: a dictionary used by the page's breadcrumb
    # context: a dictionary used for content for the base template

    context = {}

    breadcrumb_data = {"current": page_title, "links": links}

    skiplinks = [
        {"link": "#content", "label": "Contenu"},
    ]

    return {
        "context": context,
        "title": page_title,
        "breadcrumb_data": breadcrumb_data,
        "skiplinks": skiplinks,
    }


def format_number(n, format_for_web):
    """
    Rounds a number to one decimal place if needed.

    If format_for_web is True, then it also applies French locale (comma
    for decimal separator, narrow no-break space for thousands separator)
    """

    if format_for_web:
        locale = "fr_FR"
        number_format = "#,##0.#"
    else:
        # Useful for csv export
        locale = "en_US"
        number_format = "###0.#"

    if type(n) in [int, float]:
        return format_decimal(n, locale=locale, format=number_format)
    elif n is None:
        return ""
    else:
        return n


def generate_csv(
    filename: str = "output",
    title_row: list = [],
    table: list = None,
    tables_dict: dict = None,
) -> HttpResponse:
    """
    Generates a csv file, taking either a list of lists,
    or a dictionary whose values are lists of lists, for the content.
    If both are provided, "table" is managed first
    """
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}.csv"'},
    )

    writer = csv.writer(response)

    if title_row:
        writer.writerow(title_row)

    if table:
        for row in table:
            writer.writerow(row)

    if tables_dict:
        for _, table in tables_dict.items():
            for row in table["rows"]:
                writer.writerow(row)

    return response
