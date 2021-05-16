from django.apps import apps
from django.db.models import Max

from .utils import format_number
from aspic.utils import data_vintage


class ContextData:
    # These properties must be set by defining classes
    # inheriting this one
    context_properties = []
    aspic_data_model_name = ""
    fs_base_model_name = ""

    def __init__(
        self,
        sirens: list,
    ) -> None:

        # Instanciate variables
        self.sirens = []
        self.context_data = {}
        self.max_year = None
        self.place_names = []
        self.formated_tables = {}
        self.vintages = []

        if len(sirens):
            # We want to keep the list of Sirens in order
            self.sirens = sirens
            for siren_id in sirens:
                self.context_data[siren_id] = {}
                self.fetch_collectivity_name(siren_id)
        else:
            raise ValueError("The list of siren IDs is empty")

        self.vintages = data_vintage()

    def list_context_fields(self) -> list:
        return set([cp_dict["field"] for cp_dict in self.context_properties])

    def list_context_tables(self) -> list:
        return set([cp_dict["table"] for cp_dict in self.context_properties])

    def get_context_properties_for_table(self, table: list) -> list:
        return [
            cp_dict for cp_dict in self.context_properties if cp_dict["table"] == table
        ]

    def list_sirens(self) -> list:
        return self.sirens

    def fetch_collectivity_name(self, siren_id):
        fs_base_model = apps.get_model("francesubdivisions", self.fs_base_model_name)
        self.place_names.append(fs_base_model.objects.get(siren=siren_id).name)

    def fetch_collectivities_context_data(self):
        for siren_id in self.list_sirens():
            self.fetch_collectivity_context_data(siren_id)

    def fetch_collectivity_context_data(
        self,
        siren_id: str,
    ):
        """
        Returns the raw context data for a collectivity
        """
        context_data = {}

        data_model = apps.get_model("aspic", self.aspic_data_model_name)

        context_data_unsorted = data_model.objects.filter(siren=siren_id)

        # get the most recent year
        if not self.max_year:
            most_recent = context_data_unsorted.aggregate(Max("annee"))
            self.max_year = most_recent["annee__max"]

        context_data_recent = context_data_unsorted.filter(annee=self.max_year)

        for data in context_data_recent:
            datacode = data.code_donnee
            value = data.valeur
            if isinstance(value, float) and value.is_integer():
                value = int(value)
            context_data[datacode] = value

        # make sure the keys exist
        for field in self.list_context_fields():
            if field not in context_data:
                context_data[field] = ""

        self.context_data[siren_id] = context_data
        return self

    def format_tables(self):
        if not len(self.context_properties):
            raise ValueError("The context_properties list is empty.")

        for table in self.list_context_tables():
            self.format_table(table)

        self.formated_tables["places_names"] = self.place_names

    def format_table(self, table):
        formated_table = []
        for prop in self.get_context_properties_for_table(table):
            field = prop["field"]
            row = []
            label = prop["label"].format(**self.vintages)

            if "tooltip" in prop:
                label += f' <span class="fr-fi-question-line oc-tooltip" aria-hidden="true" title="{prop["tooltip"]}"></span>'

            row.append(label)
            for siren_id in self.list_sirens():
                if prop["type"] == "numeric":
                    row.append(format_number(self.context_data[siren_id][field]))
                elif prop["type"] == "boolean":
                    if "value_true" in prop:
                        value_true = prop["value_true"]
                    else:
                        value_true = "Vrai"

                    if "value_false" in prop:
                        value_false = prop["value_false"]
                    else:
                        value_false = "Faux"

                    row.append(
                        value_true
                        if self.context_data[siren_id][field]
                        else value_false
                    )
                else:
                    row.append(self.context_data[siren_id][field])

            formated_table.append(row)
        self.formated_tables[table] = formated_table
