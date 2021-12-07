from typing import Union
from francedata.models import DataYear
from django.apps import apps
from django.db.models import Max
from francedata.models.collectivity import CollectivityModel
from stdnum.fr import siren
from collectivity_pages.models import CollectivityMessage, DataRow, DataTable, Vintage

from core.services.utils import format_number
from collectivity_pages.services.utils import format_boolean


class ContextData:
    # These properties must be set by defining classes
    # inheriting this one
    base_model_name = ""
    data_model_name = ""
    data_model_key = ""
    tables_page_type = ""

    def __init__(self, collectivities: list, datayear: DataYear = None) -> None:
        # Instantiate variables
        self.collectivities = []
        self.sirens = []
        self.context_data = {}
        self.max_year = None
        self.collectivities_names = []
        self.formated_tables = {}
        self.vintages = []

        # sirens/insee codes are normally unique per year
        if datayear:
            self.datayear = datayear
        else:
            self.datayear = DataYear.objects.latest()

        # We want to keep the list of Sirens in order
        if len(collectivities):
            self.collectivities = collectivities
            for coll in collectivities:
                self.sirens.append(coll.siren)
                self.context_data[coll.siren] = {}
                self.collectivities_names.append(coll.name)
        else:
            raise ValueError("The list of siren IDs is empty")

        self.vintages = {item.key: item.value for item in Vintage.objects.all()}

        self.context_tables = DataTable.objects.filter(page_type=self.tables_page_type)

    def list_context_fields(self) -> list:
        return DataRow.objects.filter(
            table__page_type=self.tables_page_type
        ).values_list("key", flat=True)

    def list_context_tables(self) -> list:
        return self.context_tables.values_list("slug", flat=True)

    def list_sirens(self) -> list:
        return self.sirens

    def list_collectivities(self) -> list:
        return self.collectivities

    def fetch_collectivity_name(self, siren_id: str):
        base_model = apps.get_model("francedata", self.base_model_name)
        self.place_names.append(
            base_model.objects.get(siren=siren_id, years=self.datayear).name
        )

    def fetch_collectivities_context_data(self):
        for coll in self.collectivities:
            self.fetch_collectivity_context_data(coll)

    def fetch_collectivity_context_data(self, collectivity: CollectivityModel):
        """
        Returns the raw context data for a collectivity
        """

        data_model = apps.get_model("francedata", self.data_model_name)
        params = {self.data_model_key: collectivity}
        context_data_unsorted = data_model.objects.filter(**params)

        # get the most recent year
        if not self.max_year:
            max_year = data_model.objects.latest("year__year").year
            self.max_year = max_year

        context_data_recent = context_data_unsorted.filter(year=self.max_year)

        self.context_data[collectivity.siren] = {
            item.datacode: item for item in context_data_recent
        }
        return self

    def format_tables(self, format_for_web: bool = True) -> None:
        for table in self.context_tables:
            self.format_table(table, format_for_web)

        self.formated_tables["places_names"] = self.collectivities_names

    def format_table(self, table: DataTable, format_for_web: bool = True) -> None:
        formated_table_rows = []
        sources = []
        for datarow in table.datarow_set.all():
            row = []
            datacode = datarow.key
            label = datarow.label.format(**self.vintages)

            if datarow.tooltip and format_for_web:
                label += f' <span class="fr-fi-question-line oc-tooltip" role="tooltip" title="{datarow.tooltip}"></span>'

            row.append(label)

            for siren_id in self.list_sirens():
                if datacode in self.context_data[siren_id]:
                    raw_data = self.context_data[siren_id][datacode]

                    if raw_data.source not in sources:
                        sources.append(raw_data.source)

                    # Managing empty strings, then casting according to the proper datatype
                    if raw_data.value == "":
                        row.append(raw_data.value)
                    elif raw_data.datatype == "int":
                        row.append(format_number(int(raw_data.value), format_for_web))
                    elif raw_data.datatype == "float":
                        row.append(format_number(float(raw_data.value), format_for_web))
                    elif raw_data.datatype == "bool":
                        row.append(format_boolean(raw_data.value))
                    else:
                        row.append(raw_data.value)
                else:
                    row.append("")

            formated_table_rows.append(row)

        # Templates can't use kebab-case
        table_id = table.slug.replace("-", "_")
        self.formated_tables[table_id] = {
            "rows": formated_table_rows,
            "sources": sources,
        }
