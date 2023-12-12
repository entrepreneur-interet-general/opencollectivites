from francedata.models.collectivity import (
    Commune,
    CommuneData,
    Departement,
    DepartementData,
    Epci,
    EpciData,
)
from francedata.services.django_admin import TimeStampModel
from django.db import models

from simple_history.models import HistoricalRecords
from typing import Union

from francedata.services.banatic import import_epci_row_from_banatic
from francedata.services.utils import fieldfile_to_dictreader

import logging
from django.contrib import messages
from django.db import models
from django.utils import timezone

from francedata.services.django_admin import TimeStampModel


class DataSource(TimeStampModel):
    """
    The source file for the data stored
    """

    title = models.CharField("titre", max_length=255)
    url = models.CharField("URL", max_length=255, null=True, blank=True)
    year = models.ForeignKey(
        "DataYear", on_delete=models.RESTRICT, verbose_name="millésime"
    )
    public_label = models.CharField(
        "libellé public", max_length=1000, null=True, blank=True
    )

    def __str__(self):
        return f"{self.title} ({self.year})"

    def get_public_label(self) -> str:
        if self.public_label:
            return self.public_label
        else:
            return self.__str__()

    class Meta:
        verbose_name = "source"
        unique_together = (("title", "url", "year"),)


class DataMapping(TimeStampModel):
    FILE_FORMATS = [
        ("csv", "csv"),
        ("excel", "excel"),
    ]

    name = models.CharField("nom", max_length=100)
    file_format = models.CharField(
        "format du fichier", max_length=5, choices=FILE_FORMATS
    )
    mapping = models.JSONField("données")
    history = HistoricalRecords()

    class Meta:
        verbose_name = "table de correspondance"
        verbose_name_plural = "tables de correspondance"
        ordering = ["name"]

    def __str__(self):
        return self.name


class DataSourceFile(TimeStampModel):
    name = models.CharField("Nom", max_length=100, blank=True, null=True)
    data_file = models.FileField("Fichier de données")
    data_mapping = models.ForeignKey(
        DataMapping, on_delete=models.PROTECT, verbose_name="Table de correspondance"
    )
    source = models.ForeignKey(
        DataSource,
        on_delete=models.CASCADE,
        verbose_name="source",
    )
    is_imported = models.BooleanField("import effectué", default=False)
    imported_at = models.DateTimeField("date d’import", null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "fichier source"
        verbose_name_plural = "Sources - fichiers"

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.data_file.name[:100]

        super().save(*args, **kwargs)

    def mark_imported(self) -> None:
        self.is_imported = True
        self.imported_at = timezone.now()
        self.save()

    def import_file_data_command(self, request) -> None:
        """
        The command actioned on click from the admin interface
        """
        if self.data_file.size > 1048576:
            messages.info(
                request,
                "Compte-tenu de la taille importante de ce fichier, il sera importé automatiquement durant la nuit.",
            )
        else:
            response = self.import_file_data()
            result = response["success"]
            if result:
                self.mark_imported()
                messages.success(request, "L’import a été effectué avec succès.")
            else:
                messages.error(request, "Erreur lors de l’import.")
                for message in response["messages"]:
                    messages.error(request, message)

    def import_file_data(self) -> dict:
        response = {"success": False, messages: []}
        # Step 1: get the data in a dictReader
        file_format = self.data_mapping.file_format
        year = self.source.year.year

        mapping = self.data_mapping.mapping
        if "file_params" in mapping:
            file_params = mapping["file_params"]
        else:
            file_params = {}

        reader = fieldfile_to_dictreader(self.data_file, file_format, file_params, year)

        # Step 2: process the data
        for row in reader:
            coll_type = mapping["collectivity_type"]
            if coll_type == "departement":
                self.import_departement_data(row)
            elif coll_type == "commune":
                self.import_commune_data(row)
            elif coll_type == "epci":
                self.import_epci_data(row)
            else:
                response["messages"].append("Type de collectivité non reconnu")
                return response

        # Return True if everything went well
        response["success"] = True
        return response

    def import_departement_data(self, row: dict) -> None:
        try:
            insee = self.get_mapping_value("insee_key", "insee")
            fields = self.get_mapping_value("data_fields", [])
            force_year = self.get_mapping_value("force_year", False)

            if force_year:
                dept = Departement.objects.get(insee=row[insee], years=self.source.year)
            else:
                dept = Departement.objects.get(insee=row[insee])
            for field in fields:
                values_dict = self.process_field(field, row)
                fieldname_db = field["fieldname_database"]

                md, md_created = DepartementData.objects.get_or_create(
                    departement=dept,
                    year=self.source.year,
                    datacode=fieldname_db,
                    defaults=values_dict,
                )
                md.save()
        except Departement.DoesNotExist:
            logging.warning(f"Departement with insee code {row[insee]} not found")

    def import_epci_data(self, row: dict) -> None:
        try:
            siren = self.get_mapping_value("siren_key", "siren")
            fields = self.get_mapping_value("data_fields", [])
            coll_create = self.get_mapping_value("collectivity_create", False)

            if coll_create:
                field_names = self.get_mapping_value("collectivity_create_fields", {})
                column_keys = {
                    "epci_name": field_names["epci_name"],
                    "epci_type": field_names["epci_type"],
                    "epci_siren": field_names["epci_siren"],
                    "member_siren": field_names["member_siren"],
                }
                year = self.source.year
                import_epci_row_from_banatic(row, year, column_keys)

            epci = Epci.objects.get(siren=row[siren], years=self.source.year)

            logging.debug(f"Importing data for epci {epci}")
            for field in fields:
                values_dict = self.process_field(field, row)
                fieldname_db = field["fieldname_database"]

                md, md_created = EpciData.objects.get_or_create(
                    epci=epci,
                    year=self.source.year,
                    datacode=fieldname_db,
                    defaults=values_dict,
                )
                md.save()

        except Epci.DoesNotExist:
            logging.warning(f"Departement with siren code {row[siren]} not found")

    def import_commune_data(self, row: dict) -> None:
        try:
            insee = self.get_mapping_value("insee_key", "insee")
            fields = self.get_mapping_value("data_fields", [])
            coll_create = self.get_mapping_value("collectivity_create", False)

            if coll_create:
                field_names = self.get_mapping_value("collectivity_create_fields", {})
                name_field = field_names["name"]
                siren_field = field_names["siren"]
                pop_field = field_names["population"]
                dept_field = field_names["dept"]
                year = self.source.year

                departement = Departement.objects.get(insee=row[dept_field], years=year)

                values_dict = {
                    "name": row[name_field],
                    "departement": departement,
                    "population": row[pop_field],
                }

                # The Siren/Insee combinaison should be unique: if there is a merger a new Siren is created
                # The name isn’t used here because of variations between the COG and Aspic files
                commune, commune_created = Commune.objects.get_or_create(
                    insee=row[insee],
                    siren=row[siren_field],
                    defaults=values_dict,
                )

                if commune_created:
                    logging.info(f"Created commune {row[name_field]}")

                commune.save()
                commune.years.add(year)
            else:
                commune = Commune.objects.get(insee=row[insee], years=self.source.year)

            logging.debug(f"Importing data for commune {commune}")
            for field in fields:
                values_dict = self.process_field(field, row)
                fieldname_db = field["fieldname_database"]

                md, md_created = CommuneData.objects.get_or_create(
                    commune=commune,
                    year=self.source.year,
                    datacode=fieldname_db,
                    defaults=values_dict,
                )
                md.save()
        except Commune.DoesNotExist:
            logging.warning(f"Commune with insee code {row[insee]} not found")

    def get_mapping_value(self, key: str, default=None) -> Union[str, int, bool, None]:
        """
        Gets a value from the mapping JSON object.
        Allows to define a default value if the key is not present in the mapping.
        """
        mapping = self.data_mapping.mapping
        if key in mapping:
            return mapping[key]
        else:
            return default

    def process_field(self, field: dict, row: dict) -> dict:
        """
        Returns a dictionary of parameters for a collectivity metadata entry according to the field values.
        """
        field_type = field["field_type"]
        fieldname_source = field["fieldname_sourcefile"]
        return {
            "datatype": field_type,
            "value": row[fieldname_source],
            "source": self.source,
        }
