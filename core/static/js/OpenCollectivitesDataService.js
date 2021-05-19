const apiCall = axios.create({
  baseURL: "/api",
  headers: {
    "Content-type": "application/json"
  }
});

class OpenCollectivitesDataService {
  listByName(name) {
    return apiCall.get('/france/subdivisions/' + name);
  }
  communeBySiren(siren) {
    return apiCall.get('/france/communes/siren/' + siren);
  }
  aspicFicheCommune(siren) {
    return apiCall.get('/aspic/fiche-commune/' + siren);
  }
  publicationFilters() {
    return apiCall.get('/core/filters');
  }
  getPublications(filters) {
    return apiCall.get('/core/documents', { params: filters });
  }
}