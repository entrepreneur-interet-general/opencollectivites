from aspic.models.t_aspic_other import T173DatesDonnees


def data_vintage():
    # Get the vintage ("Millésime") of Aspic data
    vintages = {}

    vintages_data = T173DatesDonnees.objects.all()
    for v in vintages_data:
        vintages[v.code] = v.libelle

    return vintages


def clean_civility(civility: str):
    """
    Cleans up the civility that is present in the database. As it can return html,
    it has to be invoked with |safe in a Django template

    Values that are actually present in Aspic:
    #>>> set(T311DeleguesCom.objects.all().values_list('civilite', flat=True)).union(
        set(T312DeleguesGrp.objects.all().values_list('civilite', flat=True))).union(
        set(T313DeleguesAut.objects.all().values_list('civilite', flat=True)).union(
        set(T050Communes.objects.all().values_list('civ_maire', flat=True))))
    {'', None, 'M.', 'MME', 'Mme ', 'M', 'M. ', 'Mme', 'Melle'}
    """
    civility = civility.strip().lower()
    if civility in ["mme", "melle"]:
        return "M<sup>me</sup>"
    elif civility in ["m", "m."]:
        return "M."
    else:
        return ""
