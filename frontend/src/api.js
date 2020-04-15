export function performQuery(query, onsuccess, onfailure) {
  let url = new URL("http://localhost:5000/search");
  Object.keys(query).map((key) => {
    url.searchParams.set(key, query[key]);
  });
  console.log(url);
  fetch(url, {
    mode: "cors",
  })
    .then((resp) => resp.json())
    .then(onsuccess)
    .catch(onfailure);
}

export function getStats(onsuccess, onfailure) {
  let url = new URL("http://localhost:5000/");
  fetch(url, {
    mode: "cors",
  })
    .then((resp) => resp.json())
    .then(onsuccess)
    .catch(onfailure);
}

export default performQuery;
