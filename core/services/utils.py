from core.models import Topic, Scope, DocumentType

from babel.numbers import format_decimal

from aspic.models.t_aspic_other import T173DatesDonnees


def init_payload(page_title: str, links: list = []):
    # Returns the common payload passed to all pages:
    # title: the page title
    # breadcrumb_data: a dictionary used by the page's breadcrumb
    # context: a dictionary used for content for the base template

    ## Topics
    context = {}
    context["topics"] = []
    topics = Topic.objects.all()

    for topic in topics:
        context["topics"].append(
            {
                "title": topic.name,
                "url": f"/publications?topic={topic.id}",
                "image_path": f"/static{topic.icon_path}",
            }
        )

    breadcrumb_data = {"current": page_title, "links": links}

    return {"context": context, "title": page_title, "breadcrumb_data": breadcrumb_data}


def formatNumber(n):
    """
    Format the number with French locale and rounds to one decimal place if needed
    """
    if type(n) in [int, float]:
        return format_decimal(n, locale="fr_FR", format="#,##0.#")
    elif n is None:
        return ""
    else:
        return n


def data_vintage():
    # Get the vintage ("Millésime") of Aspic data
    vintages = {}

    vintages_data = T173DatesDonnees.objects.all()
    for v in vintages_data:
        vintages[v.code] = v.libelle

    return vintages


def list_pages(page_obj):
    """
    Gets a paginator page item and returns it with a list of pages to display like:
    [1, 2, "…", 17, 18, 19, "…" 41, 42]
    """
    last_page_number = page_obj.paginator.num_pages
    pages_list = [1, 2]
    if page_obj.number > 1:
        pages_list.append(page_obj.number - 1)
    pages_list.append(page_obj.number)
    if page_obj.number < last_page_number:
        pages_list.append(page_obj.number + 1)
    pages_list.append(last_page_number - 1)
    pages_list.append(last_page_number)

    # Keep only one of each
    unique_pages_items = list(set(pages_list))

    list_with_separators = [unique_pages_items[0]]

    for i in range(1, len(unique_pages_items)):
        difference = unique_pages_items[i] - unique_pages_items[i - 1]
        # If "…" would replace only one value, show it instead
        if difference == 2:
            list_with_separators.append(unique_pages_items[i - 1] + 1)
        elif difference > 1:
            list_with_separators.append("…")
        list_with_separators.append(unique_pages_items[i])

    page_obj.pages_list = list_with_separators
    return page_obj


def publication_filters(request):
    models = [
        {"name": "Thématique", "model": Topic, "key": "topic"},
        {"name": "Portée", "model": Scope, "key": "scope"},
        {"name": "Type de ressource", "model": DocumentType, "key": "document_type"},
    ]
    response = {}
    for m in models:
        values = []

        entries = m["model"].objects.all()
        for entry in entries:
            values.append({"value": str(entry.id), "text": entry.name})

        model_key = m["key"]
        response[model_key] = {
            "label": m["name"],
            "id": m["key"],
            "options": values,
            "selected": request.GET.get(m["key"]),
            "onchange": f"setUrlParam({m['key']})",
            "default": {"text": f"- {m['name']} -", "disabled": False, "hidden": False},
        }
    return response
