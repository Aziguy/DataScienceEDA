import { axis, barRadius, chart, tooltipRow } from "../lib/charts.js";
import { showError, simpleTable } from "../lib/components.js";
import { loadJSON } from "../lib/data.js";
import { el, fmt } from "../lib/format.js";

const $ = (id) => document.getElementById(id);
const STACK = ["Python 3.10+", "pandas", "scikit-learn", "Streamlit", "Plotly", "ECharts", "GitHub Actions", "GitHub Pages", "pytest", "Ruff", "Docker"];
const TEAM = [
  { name: "Esteban Bara", url: "https://www.linkedin.com/in/esteban-bara/" },
  { name: "Gervais Kituanga", url: "https://www.linkedin.com/in/gervais-kituanga-mitimiti/" },
  { name: "Thomas Touil", url: "https://www.linkedin.com/in/thomas-touil-b168a5144/" },
  { name: "Abdou Aziz Ziza", url: null },
  { name: "Hippolyte Kengni", url: "https://github.com/Aziguy" },
];
const COLUMN_LABELS = {
  rating: "Note",
  size_mb: "Taille",
  android_min: "Android min.",
  current_ver: "Version",
  android_ver: "Android (brut)",
};

function initials(name) {
  return name
    .split(" ")
    .map((p) => p[0])
    .slice(0, 2)
    .join("");
}

async function init() {
  $("stack").replaceChildren(...STACK.map((s) => el("span", { class: "chip", text: s })));
  $("team").replaceChildren(
    ...TEAM.map((m) =>
      el("article", { class: "card member" }, [
        el("div", { class: "avatar", text: initials(m.name), "aria-hidden": "true" }),
        el("div", {}, [
          el("h3", { text: m.name }),
          m.url
            ? el("a", { href: m.url, target: "_blank", rel: "noopener", text: "Voir le profil" })
            : el("span", { class: "muted", text: "Contributeur" }),
        ]),
      ]),
    ),
  );

  const { quality } = await loadJSON("dashboard");
  simpleTable(
    $("quality-table"),
    [
      { label: "Étape", format: (r) => r[0] },
      { label: "Lignes", num: true, format: (r) => fmt.int(r[1]) },
    ],
    [
      ["Lignes brutes", quality.raw_rows],
      ["Lignes corrompues écartées", quality.malformed_rows],
      ["Doublons exacts", quality.exact_duplicates],
      ["Doublons d'application", quality.app_duplicates],
      ["Applications retenues", quality.clean_rows],
    ],
  );

  const missing = Object.entries(quality.missing).sort((a, b) => b[1] - a[1]);
  chart("chart-missing", (t) => ({
    tooltip: {
      trigger: "item",
      formatter: (p) => tooltipRow(t.series[1], p.name, `${fmt.int(p.value)} (${fmt.pct(p.value / quality.clean_rows)})`),
    },
    grid: { left: 8, right: 64, top: 8, bottom: 8, containLabel: true },
    xAxis: axis(t, { type: "value", axisLabel: { show: false }, splitLine: { show: false } }),
    yAxis: axis(t, { type: "category", inverse: true, data: missing.map(([k]) => COLUMN_LABELS[k] ?? k), axisLabel: { color: t.text2, fontSize: 12, interval: 0 } }),
    series: [
      {
        type: "bar",
        barMaxWidth: 18,
        data: missing.map(([, v]) => v),
        itemStyle: { color: t.series[1], borderRadius: barRadius(true) },
        label: { show: true, position: "right", color: t.text2, fontFamily: t.mono, fontSize: 11, formatter: (p) => fmt.int(p.value) },
      },
    ],
  }));
}

init().catch(showError);
