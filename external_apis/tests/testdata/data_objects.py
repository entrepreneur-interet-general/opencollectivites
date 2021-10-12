from typing import OrderedDict
from external_apis.services.gallica_search_api import Record

get_records_result = {
    "bc6p0716f8m": Record(
        {
            "dc:creator": [
                "Guadeloupe. Service de l'information statistique et économique. Auteur du texte",
                "Guadeloupe. Direction départementale de l'agriculture et de la forêt. Auteur du texte",
            ],
            "dc:date": "2019",
            "dc:description": [
                "Comprend : Autres auteurs : Ducrot, Alexandre",
                "Appartient à l’ensemble documentaire : BnSP000",
            ],
            "dc:format": ["application/pdf", "Nombre total de vues : 1"],
            "dc:identifier": "https://gallica.bnf.fr/ark:/12148/bc6p0716f8m",
            "dc:language": "fre",
            "dc:publisher": "SRISE Guadeloupe (Paris)",
            "dc:relation": [
                "Périodique lié : Agreste GuadeloupeEn ligne(ISSN 2739-249X) (Notice : http://catalogue.bnf.fr/ark:/12148/cb46607763v)",
                "Notice du catalogue : http://catalogue.bnf.fr/ark:/12148/cb46804556n",
                "Première de couverture : 577537",
            ],
            "dc:rights": ["domaine public", "public domain"],
            "dc:source": "BNSP-SSP Agreste",
            "dc:subject": [
                "Agriculture",
                "Exploitations agricoles",
                "Résultats économiques",
            ],
            "dc:title": "RICA 2017. Un revenu moyen touché par le cyclone Maria",
            "dc:type": [
                "text",
                "monographie imprimée",
                "printed monograph",
                "Document électronique",
                "Digital document",
            ],
            "id": "bc6p0716f8m",
        }
    ),
    "bc6p0716f78": Record(
        {
            "dc:creator": [
                "Guadeloupe. Service de l'information statistique et économique. Auteur du texte",
                "Guadeloupe. Direction départementale de l'agriculture et de la forêt. Auteur du texte",
            ],
            "dc:date": "2019",
            "dc:description": [
                "Comprend : Autres auteurs : Ducrot, Alexandre",
                "Appartient à l’ensemble documentaire : BnSP000",
            ],
            "dc:format": ["application/pdf", "Nombre total de vues : 1"],
            "dc:identifier": "https://gallica.bnf.fr/ark:/12148/bc6p0716f78",
            "dc:language": "fre",
            "dc:publisher": "SRISE Guadeloupe (Paris)",
            "dc:relation": [
                "Périodique lié : Agreste GuadeloupeEn ligne(ISSN 2739-249X) (Notice : http://catalogue.bnf.fr/ark:/12148/cb46607763v)",
                "Notice du catalogue : http://catalogue.bnf.fr/ark:/12148/cb46804596w",
                "Première de couverture : 577576",
            ],
            "dc:rights": ["domaine public", "public domain"],
            "dc:source": "BNSP-SSP Agreste",
            "dc:subject": [
                "Agriculture",
                "Exploitations agricoles",
                "Résultats économiques",
            ],
            "dc:title": "RICA 2016",
            "dc:type": [
                "text",
                "monographie imprimée",
                "printed monograph",
                "Document électronique",
                "Digital document",
            ],
            "id": "bc6p0716f78",
        }
    ),
    "bc6p06wznwk": Record(
        {
            "dc:creator": [
                "Guadeloupe. Service de l'information statistique et économique. Auteur du texte",
                "Guadeloupe. Direction départementale de l'agriculture et de la forêt. Auteur du texte",
            ],
            "dc:date": "//invalid date//",
            "dc:description": "Appartient à l’ensemble documentaire : BnSP000",
            "dc:format": ["application/pdf", "Nombre total de vues : 1"],
            "dc:identifier": "https://gallica.bnf.fr/ark:/12148/bc6p06wznwk",
            "dc:language": "fre",
            "dc:publisher": "SRISE Guadeloupe (Paris)",
            "dc:relation": [
                "Périodique lié : Agreste Guadeloupe (En ligne)(ISSN 2739-249X) (Notice : http://catalogue.bnf.fr/ark:/12148/cb46607763v)",
                "Notice du catalogue : http://catalogue.bnf.fr/ark:/12148/cb467148090",
                "Première de couverture : 519513",
            ],
            "dc:rights": ["domaine public", "public domain"],
            "dc:source": "BNSP-SSP Agreste",
            "dc:subject": ["Produits agricoles", "Exploitations agricoles"],
            "dc:title": "La culture de la canne à sucre. Résultats de l'enquête statistique réalisée en 2014 auprès de 185 planteurs en Guadeloupe",
            "dc:type": [
                "text",
                "monographie imprimée",
                "printed monograph",
                "Document électronique",
                "Digital document",
            ],
            "id": "bc6p06wznwk",
        }
    ),
}

sample_raw_record = OrderedDict(
    [
        ("dc:creator", "Bally, Alice (1872-1938). Graveur"),
        ("dc:date", "1906"),
        ("dc:description", "Donateur : Musée national d'art moderne (Paris). Donateur"),
        (
            "dc:format",
            [
                "1 est. : gravure sur bois en couleur sur papier Japon ; 26 x 19 cm (tr. c.)",
                "image/jpeg",
                "Nombre total de vues : 1",
            ],
        ),
        ("dc:identifier", "https://gallica.bnf.fr/ark:/12148/btv1b10547034q"),
        ("dc:language", ["fre", "français"]),
        ("dc:publisher", "[s.n.][s.n.]"),
        (
            "dc:relation",
            [
                "Notice de recueil : http://catalogue.bnf.fr/ark:/12148/cb403863436",
                "Appartient à : [Recueil. Oeuvre de Alice Bailly]",
                "Notice du catalogue : http://catalogue.bnf.fr/ark:/12148/cb452780288",
            ],
        ),
        ("dc:rights", ["domaine public", "public domain"]),
        (
            "dc:source",
            "Bibliothèque nationale de France, département Estampes et photographie, FOL-CA20C-1 (BAILLY, Alice)",
        ),
        (
            "dc:subject",
            ["Hérens, Val d' (Suisse)", "Paysages de montagne -- 1870-1913"],
        ),
        (
            "dc:title",
            "[Le Mulet (Val d'Hérence)] : [estampe] ([Tirage en noir, jaune et bleu]) / A. Bally",
        ),
        ("dc:type", ["image fixe", "image", "still image", "estampe", "engraving"]),
        ("id", "btv1b10547034q"),
    ]
)

sample_raw_record_bad_ids = OrderedDict(
    [
        ("dc:creator", "Bally, Alice (1872-1938). Graveur"),
        ("dc:date", "1906"),
        ("dc:description", "Donateur : Musée national d'art moderne (Paris). Donateur"),
        (
            "dc:format",
            [
                "1 est. : gravure sur bois en couleur sur papier Japon ; 26 x 19 cm (tr. c.)",
                "image/jpeg",
                "Nombre total de vues : 1",
            ],
        ),
        ("dc:identifier", ["https://sample-site.fr/sample_id", "ISBN 9782111625242"]),
        ("dc:language", ["fre", "français"]),
        ("dc:publisher", "[s.n.][s.n.]"),
        (
            "dc:relation",
            [
                "Notice de recueil : http://catalogue.bnf.fr/ark:/12148/cb403863436",
                "Appartient à : [Recueil. Oeuvre de Alice Bailly]",
                "Notice du catalogue : http://catalogue.bnf.fr/ark:/12148/cb452780288",
            ],
        ),
        ("dc:rights", ["domaine public", "public domain"]),
        (
            "dc:source",
            "Bibliothèque nationale de France, département Estampes et photographie, FOL-CA20C-1 (BAILLY, Alice)",
        ),
        (
            "dc:subject",
            ["Hérens, Val d' (Suisse)", "Paysages de montagne -- 1870-1913"],
        ),
        (
            "dc:title",
            "[Le Mulet (Val d'Hérence)] : [estampe] ([Tirage en noir, jaune et bleu]) / A. Bally",
        ),
        ("dc:type", ["image fixe", "image", "still image", "estampe", "engraving"]),
        ("id", "btv1b10547034q"),
    ]
)
