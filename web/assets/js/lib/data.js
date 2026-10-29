const cache = new Map();

export function loadJSON(name) {
  if (!cache.has(name)) {
    cache.set(
      name,
      fetch(`data/${name}.json`).then((res) => {
        if (!res.ok) throw new Error(`${name}.json: HTTP ${res.status}`);
        return res.json();
      }),
    );
  }
  return cache.get(name);
}

export function rowsToObjects({ columns, rows }) {
  return rows.map((row) => Object.fromEntries(columns.map((c, i) => [c, row[i]])));
}
