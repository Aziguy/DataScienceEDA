import { axis, chart, escapeHTML, legend, tooltipRow } from "../lib/charts.js";
import { DataTable, kpiTiles, showError } from "../lib/components.js";
import { loadJSON, rowsToObjects } from "../lib/data.js";
import { el, fmt } from "../lib/format.js";

const MAX_POINTS = 2500;
const state = { search: "", category: "", type: "", minRating: 1 };
const $ = (id) => document.getElementById(id);

const TYPE_LABEL = { free: "Gratuit", paid: "Payant" };
const CORR_LABELS = {
  rating: "Note",
  reviews: "Avis",
  size_mb: "Taille",
  installs: "Installs",
  price: "Prix",
  android_min: "Android",
};

function filterApps(apps) {
  const query = state.search.trim().toLowerCase();
  return apps.filter(
    (a) =>
      (!query || a.app.toLowerCase().includes(query)) &&
      (!state.category || a.category === state.category) &&
      (!state.type || (state.type === "paid") === a.price > 0) &&
      (state.minRating <= 1 || (a.rating ?? 0) >= state.minRating),
  );
}

function median(values) {
  if (!values.length) return NaN;
  const s = [...values].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
}

function renderKpis(rows) {
  const rated = rows.filter((r) => r.rating !== null).map((r) => r.rating);
  const avg = rated.reduce((a, b) => a + b, 0) / rated.length;
  kpiTiles($("explore-kpis"), [
    { label: "Applications", value: fmt.int(rows.length) },
    { label: "Note moyenne", value: fmt.orDash(avg, (v) => fmt.dec(v)) },
    { label: "Installations médianes", value: fmt.orDash(median(rows.map((r) => r.installs)), fmt.compact) },
    { label: "Payantes", value: rows.length ? fmt.pct(rows.filter((r) => r.price > 0).length / rows.length) : "–" },
  ]);
}

function renderScatter(rows) {
  const points = rows.filter((r) => r.rating !== null && r.size_mb > 0);
  const stride = Math.max(1, Math.ceil(points.length / MAX_POINTS));
  const sample = points.filter((_, i) => i % stride === 0);
  const series = (paid) =>
    sample.filter((r) => (r.price > 0) === paid).map((r) => [r.size_mb, r.rating, r.app, r.category]);

  chart("chart-scatter", (t) => ({
    legend: legend(t, { data: ["Gratuit", "Payant"] }),
    grid: { left: 8, right: 16, top: 36, bottom: 24, containLabel: true },
    tooltip: {
      trigger: "item",
      formatter: (p) =>
        `<strong>${escapeHTML(p.value[2])}</strong><br><span style="opacity:.7">${escapeHTML(p.value[3])}</span>` +
        tooltipRow(p.color, "Note", fmt.dec(p.value[1], 1)) +
        tooltipRow(p.color, "Taille", `${fmt.dec(p.value[0], 1)} Mo`),
    },
    xAxis: axis(t, { type: "log", name: "Mo", nameLocation: "end", min: 0.01, max: 1000 }),
    yAxis: axis(t, { type: "value", min: 1, max: 5 }),
    series: [
      { name: "Gratuit", data: series(false), color: t.series[0] },
      { name: "Payant", data: series(true), color: t.series[1] },
    ].map((s) => ({
      ...s,
      type: "scatter",
      symbolSize: 7,
      itemStyle: { color: s.color, opacity: 0.55, borderColor: t.surface, borderWidth: 1 },
      emphasis: { scale: 1.6, itemStyle: { opacity: 1 } },
    })),
  }));
}

function renderCorrelation({ columns, matrix }) {
  const labels = columns.map((c) => CORR_LABELS[c] ?? c);
  const data = matrix.flatMap((row, i) => row.map((v, j) => [j, i, v]));
  chart("chart-corr", (t) => ({
    tooltip: {
      formatter: (p) => `${labels[p.value[1]]} × ${labels[p.value[0]]}<br><strong>${fmt.dec(p.value[2])}</strong>`,
    },
    grid: { left: 8, right: 8, top: 8, bottom: 56, containLabel: true },
    xAxis: axis(t, {
      type: "category",
      data: labels,
      splitLine: { show: false },
      axisLine: { show: false },
      axisLabel: { color: t.muted, fontFamily: t.mono, fontSize: 11, interval: 0 },
    }),
    yAxis: axis(t, { type: "category", data: labels, inverse: true, splitLine: { show: false }, axisLine: { show: false } }),
    visualMap: {
      min: -1,
      max: 1,
      orient: "horizontal",
      left: "center",
      bottom: 0,
      itemWidth: 12,
      itemHeight: 160,
      calculable: false,
      text: ["+1", "−1"],
      textStyle: { color: t.muted, fontFamily: t.mono, fontSize: 11 },
      inRange: { color: t.diverging },
    },
    series: [
      {
        type: "heatmap",
        data,
        itemStyle: { borderColor: t.surface, borderWidth: 2, borderRadius: 4 },
        label: { show: true, color: t.text, fontFamily: t.mono, fontSize: 11, formatter: (p) => fmt.dec(p.value[2]) },
      },
    ],
  }));
}

function bindFilters(update) {
  $("f-search").addEventListener("input", (e) => {
    state.search = e.target.value;
    update();
  });
  $("f-category").addEventListener("change", (e) => {
    state.category = e.target.value;
    update();
  });
  $("f-rating").addEventListener("input", (e) => {
    state.minRating = Number(e.target.value);
    $("f-rating-out").textContent = state.minRating.toFixed(1);
    update();
  });
  const buttons = [...$("f-type").querySelectorAll("button")];
  for (const button of buttons) {
    button.addEventListener("click", () => {
      state.type = button.dataset.value;
      for (const b of buttons) b.setAttribute("aria-pressed", String(b === button));
      update();
    });
  }
}

async function init() {
  const [table, dashboard] = await Promise.all([loadJSON("apps"), loadJSON("dashboard")]);
  const apps = rowsToObjects(table);

  for (const c of [...new Set(apps.map((a) => a.category))].sort((a, b) => a.localeCompare(b, "fr"))) {
    $("f-category").append(el("option", { value: c, text: c }));
  }

  const appsTable = new DataTable(
    $("apps-table"),
    [
      { key: "app", label: "Application", class: "app-name", title: true, format: (r) => r.app },
      { key: "category", label: "Catégorie", format: (r) => r.category },
      { key: "rating", label: "Note", num: true, format: (r) => fmt.orDash(r.rating, (v) => fmt.dec(v, 1)) },
      { key: "reviews", label: "Avis", num: true, format: (r) => fmt.int(r.reviews) },
      { key: "installs", label: "Installs", num: true, format: (r) => `${fmt.compact(r.installs)}+` },
      { key: "size_mb", label: "Taille", num: true, format: (r) => fmt.orDash(r.size_mb, (v) => `${fmt.dec(v, 1)} Mo`) },
      { key: "price", label: "Prix", num: true, format: (r) => (r.price > 0 ? fmt.money(r.price) : TYPE_LABEL.free) },
      { key: "last_updated", label: "Mise à jour", format: (r) => r.last_updated },
    ],
    {
      pageSize: 15,
      sort: { key: "reviews", dir: "descending" },
      pager: { info: $("pager-info"), prev: $("prev"), next: $("next") },
    },
  );

  const categoryTable = new DataTable(
    $("category-table"),
    [
      { key: "category", label: "Catégorie", format: (r) => r.category },
      { key: "apps", label: "Apps", num: true, format: (r) => fmt.int(r.apps) },
      { key: "avg_rating", label: "Note moy.", num: true, format: (r) => fmt.orDash(r.avg_rating, (v) => fmt.dec(v)) },
      { key: "median_installs", label: "Installs méd.", num: true, format: (r) => fmt.compact(r.median_installs) },
      { key: "total_installs", label: "Installs total", num: true, format: (r) => fmt.compact(r.total_installs) },
      { key: "paid_share", label: "Payantes", num: true, format: (r) => fmt.pct(r.paid_share) },
      { key: "avg_price_paid", label: "Prix moy.", num: true, format: (r) => fmt.orDash(r.avg_price_paid, fmt.money) },
    ],
    { sort: { key: "apps", dir: "descending" } },
  );
  categoryTable.setRows(dashboard.categories);
  renderCorrelation(dashboard.correlation);

  let frame = 0;
  const update = () => {
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame(() => {
      const rows = filterApps(apps);
      appsTable.setRows(rows);
      renderKpis(rows);
      renderScatter(rows);
    });
  };
  bindFilters(update);
  update();
}

init().catch(showError);
