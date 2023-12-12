import requests

API_BASE = "https://www.data.gouv.fr/api/1/"


def get_datagouv_file(dataset_id, title_regex, min_year=0):
    """
    dataset_id: the id of the dataset
    title_regex: the regex to find the searched file title
    min_year: if the formatting of the file changed over time, the first managed year
    """
    dataset_url = f"{API_BASE}datasets/{dataset_id}/"

    response = requests.get(dataset_url).json()

    matching_files = {}
    for r in response["resources"]:
        m = title_regex.match(r["title"])
        if m:
            year = int(m.group("year"))
            if year >= min_year:
                matching_files[year] = {
                    "title": r["title"],
                    "url": r["url"],
                    "year": year,
                }

    return matching_files
