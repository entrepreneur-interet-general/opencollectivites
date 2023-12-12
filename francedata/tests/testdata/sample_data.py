sample_commune_mapping = """
{
  "insee_key": "CodeInsee",
  "data_fields": [
    {
      "field_type": "str",
      "fieldname_database": "siren",
      "fieldname_sourcefile": "SIREN"
    },
    {
      "field_type": "int",
      "fieldname_database": "chef_lieu",
      "fieldname_sourcefile": "CHEFLIEU"
    },
    {
      "field_type": "int",
      "fieldname_database": "chef_lieu",
      "fieldname_sourcefile": "CHEFLIEU"
    },
    {
      "field_type": "string",
      "fieldname_database": "code_uu",
      "fieldname_sourcefile": "CodeUU"
    },
    {
      "field_type": "string",
      "fieldname_database": "uu",
      "fieldname_sourcefile": "UU"
    },
    {
      "field_type": "string",
      "fieldname_database": "code_au",
      "fieldname_sourcefile": "CodeAU"
    },
    {
      "field_type": "string",
      "fieldname_database": "au",
      "fieldname_sourcefile": "AU"
    },
    {
      "field_type": "string",
      "fieldname_database": "code_bv",
      "fieldname_sourcefile": "CodeBV"
    },
    {
      "field_type": "string",
      "fieldname_database": "bv",
      "fieldname_sourcefile": "BV"
    },
    {
      "field_type": "int",
      "fieldname_database": "pop_tot",
      "fieldname_sourcefile": "PopTot"
    },
    {
      "field_type": "int",
      "fieldname_database": "pop_muni",
      "fieldname_sourcefile": "PopMuni"
    },
    {
      "field_type": "int",
      "fieldname_database": "pop_tcam",
      "fieldname_sourcefile": "PopTCAM"
    },
    {
      "field_type": "float",
      "fieldname_database": "tcam",
      "fieldname_sourcefile": "TCAM"
    },
    {
      "field_type": "string",
      "fieldname_database": "adresse_1",
      "fieldname_sourcefile": "Adresse1"
    },
    {
      "field_type": "string",
      "fieldname_database": "adresse_2",
      "fieldname_sourcefile": "Adresse2"
    },
    {
      "field_type": "string",
      "fieldname_database": "adresse_3",
      "fieldname_sourcefile": "Adresse3"
    },
    {
      "field_type": "string",
      "fieldname_database": "CP",
      "fieldname_sourcefile": "cp"
    },
    {
      "field_type": "string",
      "fieldname_database": "ville",
      "fieldname_sourcefile": "Ville"
    },
    {
      "field_type": "string",
      "fieldname_database": "tel",
      "fieldname_sourcefile": "Tel"
    },
    {
      "field_type": "string",
      "fieldname_database": "courriel",
      "fieldname_sourcefile": "Courriel"
    },
    {
      "field_type": "string",
      "fieldname_database": "civ_maire",
      "fieldname_sourcefile": "CiviliteMaire"
    },
    {
      "field_type": "string",
      "fieldname_database": "nom_maire",
      "fieldname_sourcefile": "NomMaire"
    },
    {
      "field_type": "string",
      "fieldname_database": "prenom_maire",
      "fieldname_sourcefile": "PrenomMaire"
    },
    {
      "field_type": "int",
      "fieldname_database": "superficie",
      "fieldname_sourcefile": "Sup"
    },
    {
      "field_type": "bool",
      "fieldname_database": "montagne",
      "fieldname_sourcefile": "montagne"
    },
    {
      "field_type": "bool",
      "fieldname_database": "touristique",
      "fieldname_sourcefile": "Touristique"
    },
    {
      "field_type": "bool",
      "fieldname_database": "zrr",
      "fieldname_sourcefile": "ZRR"
    },
    {
      "field_type": "bool",
      "fieldname_database": "qpv",
      "fieldname_sourcefile": "QPV"
    },
    {
      "field_type": "float",
      "fieldname_database": "densite",
      "fieldname_sourcefile": "Densite"
    }
  ],
  "file_params": {
    "sheet_name": "CommuneASPIC{year}"
  },
  "collectivity_type": "commune",
  "collectivity_create": true,
  "collectivity_create_fields": {
    "dept": "dept",
    "name": "NomCom",
    "siren": "SIREN",
    "population": "PopMuni"
  }
}
"""
