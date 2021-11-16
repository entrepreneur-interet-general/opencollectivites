from francedata.apps import FrancedataConfig

# Subclassing Francedata to rename it in the Admin panel
class CollDataConfig(FrancedataConfig):
    verbose_name = "Données collectivités"
