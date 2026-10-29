const locale = "fr-FR";

export const fmt = {
  int: (v) => new Intl.NumberFormat(locale).format(Math.round(v)),
  dec: (v, d = 2) =>
    new Intl.NumberFormat(locale, { minimumFractionDigits: d, maximumFractionDigits: d }).format(v),
  pct: (v, d = 1) =>
    new Intl.NumberFormat(locale, { style: "percent", maximumFractionDigits: d }).format(v),
  compact: (v) =>
    new Intl.NumberFormat(locale, { notation: "compact", maximumFractionDigits: 1 }).format(v),
  money: (v) => new Intl.NumberFormat(locale, { style: "currency", currency: "USD" }).format(v),
  orDash: (v, f) => (v === null || v === undefined || Number.isNaN(v) ? "–" : f(v)),
};

export function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "text") node.textContent = v;
    else if (k === "class") node.className = v;
    else if (k.startsWith("on")) node.addEventListener(k.slice(2), v);
    else node.setAttribute(k, v);
  }
  for (const child of [].concat(children)) if (child) node.append(child);
  return node;
}

export function setText(id, value) {
  const node = document.getElementById(id);
  if (node) node.textContent = value;
}
