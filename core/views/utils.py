from core.models import Topic

from babel.numbers import format_decimal

from aspic.models.t_aspic_other import T173DatesDonnees


def init_payload():
    # Returns the common payload passed to all pages

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

    return {"context": context}


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
