from external_apis.services.opendatasoft_api import OpenDataSoftSearch
import logging


def check_values(metadata: dict, key: str, output: dict) -> None:
    """
    Count the number of time each value appears for a given field
    """
    try:
        for i in metadata[key]:
            if i not in output:
                output[i] = 1
            else:
                output[i] += 1
    except:
        pass


def analyse_endpoint(endpoint: str) -> None:
    """
    Analyse the catalog of a OpenDataSoft by retrieving and counting the values
    for a set of fields.
    """
    logging.info(f"Checking endpoint {endpoint}:")

    ods = OpenDataSoftSearch(endpoint)

    results = ods.catalog_datasets(
        where="""modified >= date'2016-01-01'""", exclude="theme:INTERNE"
    )
    logging.info(f"{len(results)} results found")

    all_geographic_references = {}
    all_keywords = {}
    all_territories = {}
    all_themes = {}
    for result in results:
        metadata = result["dataset"]["metas"]["default"]

        check_values(metadata, "geographic_reference", all_geographic_references)
        check_values(metadata, "keyword", all_keywords)
        check_values(metadata, "territory", all_territories)
        check_values(metadata, "theme", all_themes)

    logging.info("geographic_reference:")
    logging.info(
        dict(
            sorted(all_geographic_references.items(), key=lambda x: x[1], reverse=True)
        )
    )
    logging.info("keyword:")
    logging.info(dict(sorted(all_keywords.items(), key=lambda x: x[1], reverse=True)))
    logging.info("territory:")
    logging.info(
        dict(sorted(all_territories.items(), key=lambda x: x[1], reverse=True))
    )
    logging.info("theme:")
    logging.info(dict(sorted(all_themes.items(), key=lambda x: x[1], reverse=True)))
