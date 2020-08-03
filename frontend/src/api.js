export function performQuery(query, onsuccess, onfailure) {
  let url = new URL(process.env.API_LOCATION + "/search");
  Object.keys(query).map(key => {
    url.searchParams.set(key, query[key]);
  });
  fetch(url, {
    mode: "cors"
  })
    .then(resp => resp.json())
    .then(onsuccess)
    .catch(onfailure);
}

export function getStats(onsuccess, onfailure) {
  let url = new URL(process.env.API_LOCATION);
  fetch(url, {
    mode: "cors"
  })
    .then(resp => resp.json())
    .then(onsuccess)
    .catch(onfailure);
}

export default performQuery;
