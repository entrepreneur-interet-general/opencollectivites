from francesubdivisions.models import Epci
from aspic.models.t_aspic_intercommunalites import T311Groupements


def epci_data(siren_id):
    # Get the basic data
    response = T311Groupements.objects.get(siren=siren_id).__dict__
    response.pop("_state", None)

    return response