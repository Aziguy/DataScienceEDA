import { axis, barRadius, chart, escapeHTML, tooltipRow } from "../lib/charts.js";
import { kpiTiles, showError, simpleTable } from "../lib/components.js";
import { loadJSON } from "../lib/data.js";
import { el, fmt } from "../lib/format.js";
import { deriveInput, toRow } from "../lib/features.js";
import { predictGradientBoosting } from "../lib/models.js";

const $ = (id) => document.getElementById(id);
const FINAL_MODEL = "Gradient Boosting";
const INSTALL_STEPS = [1, 5, 10, 50, 100, 500, 1e3, 5e3, 1e4, 5e4, 1e5, 5e5, 1e6, 5e6, 1e7, 5e7, 1e8, 5e8, 1e9];
const ANDROID = [1.6, 2.1, 2.2, 2.3, 3.0, 4.0, 4.1, 4.2, 4.3, 4.4, 5.0, 5.1, 6.0, 7.0, 8.0];
const DEFAULTS = {
  category: "Family",
  content_rating: "Everyone",
  installs: 1e5,
  reviews: 2000,
  size_mb: 15,
  price: 0,
  last_updated: "2018-07-01",
  android_min: 4.1,
  n_genres: 1,
};
const FEATURE_LABELS = {
  reviews_per_install: "Avis par installation",
  log_reviews: "Nombre d'avis",
  category: "Catégorie",
  days_since_update: "Ancienneté de la MAJ",
  size_mb: "Taille",
  android_min: "Android minimum",
  log_installs: "Installations",
  content_rating: "Public cible",
  price: "Prix",
  n_genres: "Nombre de genres",
};

function fillSelect(select, options) {
  select.replaceChildren(...options.map(([value, label]) => el("option", { value, text: label })));
}

function readForm(form) {
  const data = Object.fromEntries(new FormData(form));
  const num = (v) => (v === "" ? NaN : Number(v));
  return {
    category: data.category,
    content_rating: data.content_rating,
    installs: num(data.installs),
    reviews: num(data.reviews),
    size_mb: num(data.size_mb),
    price: num(data.price) || 0,
    last_updated: data.last_updated,
    android_min: num(data.android_min),
    n_genres: num(data.n_genres),
  };
}

function writeForm(form, values) {
  for (const [key, value] of Object.entries(values)) {
    const field = form.elements.namedItem(key);
    if (field) field.value = String(value);
  }
  $("p-genres-out").textContent = String(values.n_genres);
}

function renderScore(prediction, categoryAvg, globalAvg) {
  const clamped = Math.min(5, Math.max(1, prediction));
  $("score").textContent = fmt.dec(clamped, 2);
  $("stars").style.width = `${(clamped / 5) * 100}%`;
  $("meter").style.width = `${((clamped - 1) / 4) * 100}%`;
  $("meter-mark").style.left = `${((categoryAvg - 1) / 4) * 100}%`;
  const delta = clamped - categoryAvg;
  const deltaNode = el("span", {
    class: delta >= 0 ? "delta-up" : "delta-down",
    text: `${delta >= 0 ? "+" : "−"}${fmt.dec(Math.abs(delta), 2)}`,
  });
  $("compare").replaceChildren(
    el("span", { text: "Moyenne de la catégorie (repère)" }),
    el("span", { text: fmt.dec(categoryAvg, 2) }),
    el("span", { text: "Moyenne du store" }),
    el("span", { text: fmt.dec(globalAvg, 2) }),
    el("span", { text: "Écart à la catégorie" }),
    deltaNode,
  );
}

function renderComparison(rows) {
  const ordered = [...rows].sort((a, b) => a.mae - b.mae);
  chart("chart-compare", (t) => ({
    tooltip: {
      trigger: "item",
      formatter: (p) => {
        const r = ordered[p.dataIndex];
        return `<strong>${escapeHTML(r.model)}</strong>${tooltipRow(p.color, "MAE", fmt.dec(r.mae, 3))}${tooltipRow(p.color, "RMSE", fmt.dec(r.rmse, 3))}${tooltipRow(p.color, "R²", fmt.dec(r.r2, 3))}`;
      },
    },
    grid: { left: 8, right: 56, top: 8, bottom: 8, containLabel: true },
    xAxis: axis(t, { type: "value", min: 0.3, axisLabel: { show: false }, splitLine: { show: false } }),
    yAxis: axis(t, { type: "category", inverse: true, data: ordered.map((r) => r.model), axisLabel: { color: t.text2, fontSize: 12, interval: 0 } }),
    series: [
      {
        type: "bar",
        barMaxWidth: 18,
        data: ordered.map((r) => ({
          value: r.mae,
          itemStyle: { color: r.model === FINAL_MODEL ? t.series[0] : t.axis, borderRadius: barRadius(true) },
        })),
        label: { show: true, position: "right", color: t.text2, fontFamily: t.mono, fontSize: 11, formatter: (p) => fmt.dec(p.value, 3) },
      },
    ],
  }));
}

function renderImportance(rows) {
  chart("chart-importance", (t) => ({
    tooltip: { trigger: "item", formatter: (p) => tooltipRow(t.series[0], p.name, fmt.pct(p.value)) },
    grid: { left: 8, right: 56, top: 8, bottom: 8, containLabel: true },
    xAxis: axis(t, { type: "value", axisLabel: { show: false }, splitLine: { show: false } }),
    yAxis: axis(t, { type: "category", inverse: true, data: rows.map((r) => FEATURE_LABELS[r.feature] ?? r.feature), axisLabel: { color: t.text2, fontSize: 12, interval: 0 } }),
    series: [
      {
        type: "bar",
        barMaxWidth: 16,
        data: rows.map((r) => r.importance),
        itemStyle: { color: t.series[0], borderRadius: barRadius(true) },
        label: { show: true, position: "right", color: t.text2, fontFamily: t.mono, fontSize: 11, formatter: (p) => fmt.pct(p.value) },
      },
    ],
  }));
}

function renderPredictions(points) {
  chart("chart-pred", (t) => ({
    grid: { left: 8, right: 24, top: 16, bottom: 28, containLabel: true },
    tooltip: {
      trigger: "item",
      formatter: (p) =>
        p.seriesType === "scatter"
          ? `<strong>${escapeHTML(p.value[2])}</strong>${tooltipRow(t.series[0], "Observée", fmt.dec(p.value[1], 1))}${tooltipRow(t.series[0], "Prédite", fmt.dec(p.value[0], 2))}`
          : "Prédiction parfaite",
    },
    xAxis: axis(t, { type: "value", name: "Note prédite", nameLocation: "middle", nameGap: 28, min: 3, max: 5 }),
    yAxis: axis(t, { type: "value", name: "Note observée", min: 1, max: 5 }),
    series: [
      {
        type: "scatter",
        symbolSize: 8,
        data: points.map(([app, , actual, predicted]) => [predicted, actual, app]),
        itemStyle: { color: t.series[0], opacity: 0.6, borderColor: t.surface, borderWidth: 1 },
        emphasis: { scale: 1.5, itemStyle: { opacity: 1 } },
      },
      {
        type: "line",
        data: [[3, 3], [5, 5]],
        symbol: "none",
        silent: true,
        lineStyle: { color: t.muted, width: 1, type: "solid" },
      },
    ],
  }));
}

function renderCard(meta, holdout) {
  const items = [
    `Cible : note moyenne Play Store (1 à 5). ${fmt.int(meta.n_train)} apps d'entraînement, ${fmt.int(meta.n_test)} de test.`,
    `${meta.n_features} variables : volumétrie (log), ratio avis/installs, taille, prix, ancienneté de mise à jour, version Android, catégorie et public (one-hot).`,
    `${fmt.pct(holdout.within_half_star, 0)} des prédictions tombent à ±0,5 étoile de la note réelle.`,
    "Limite : la note dépend surtout de la qualité perçue, absente des métadonnées. Le R² reste modeste, le modèle capte des tendances, pas un verdict.",
    `Données figées au ${meta.reference_date} : l'ancienneté est calculée par rapport à cette date.`,
  ];
  $("model-card").replaceChildren(...items.map((text) => el("li", { text })));
}

async function init() {
  const [payload, metrics, dashboard, predictions] = await Promise.all([
    loadJSON("rating_model"),
    loadJSON("metrics"),
    loadJSON("dashboard"),
    loadJSON("predictions"),
  ]);
  const meta = payload.metadata;
  const form = $("predict-form");
  const categoryAvg = Object.fromEntries(dashboard.categories.map((c) => [c.category, c.avg_rating]));

  fillSelect($("p-category"), meta.categories.map((c) => [c, c]));
  fillSelect($("p-content"), meta.content_ratings.map((c) => [c, c]));
  fillSelect($("p-installs"), INSTALL_STEPS.map((v) => [v, `${fmt.int(v)}+`]));
  fillSelect($("p-android"), [["", "Variable selon l'appareil"], ...ANDROID.map((v) => [v.toFixed(1), `${v.toFixed(1)} et +`])]);
  writeForm(form, { ...DEFAULTS, android_min: DEFAULTS.android_min.toFixed(1) });
  $("model-tag").textContent = `GBM · ${payload.model.trees.length} arbres`;

  const update = () => {
    const input = readForm(form);
    $("p-genres-out").textContent = String(input.n_genres);
    const row = toRow(payload.features, deriveInput(input, meta.reference_date));
    const prediction = predictGradientBoosting(payload.model, row);
    renderScore(prediction, categoryAvg[input.category] ?? meta.rating_mean, dashboard.kpis.avg_rating);
  };
  form.addEventListener("input", update);
  $("reset").addEventListener("click", () => {
    writeForm(form, { ...DEFAULTS, android_min: DEFAULTS.android_min.toFixed(1) });
    update();
  });
  $("score-note").textContent = `Erreur absolue moyenne sur le jeu de test : ±${fmt.dec(metrics.rating.holdout.mae, 2)} étoile.`;
  update();

  const h = metrics.rating.holdout;
  kpiTiles($("model-kpis"), [
    { label: "MAE (test)", value: fmt.dec(h.mae, 3), note: "erreur absolue moyenne" },
    { label: "RMSE (test)", value: fmt.dec(h.rmse, 3) },
    { label: "R² (test)", value: fmt.dec(h.r2, 3) },
    { label: "±0,5 étoile", value: fmt.pct(h.within_half_star, 0), note: "des prédictions" },
  ]);
  renderComparison(metrics.rating.comparison);
  renderImportance(metrics.rating.importance);
  renderPredictions(predictions);
  renderCard(meta, h);
  simpleTable(
    $("compare-table"),
    [
      { label: "Modèle", format: (r) => (r.model === FINAL_MODEL ? `${r.model} (retenu)` : r.model) },
      { label: "MAE", num: true, format: (r) => fmt.dec(r.mae, 3) },
      { label: "RMSE", num: true, format: (r) => fmt.dec(r.rmse, 3) },
      { label: "R²", num: true, format: (r) => fmt.dec(r.r2, 3) },
      { label: "Écart-type R²", num: true, format: (r) => fmt.dec(r.r2_std, 3) },
    ],
    metrics.rating.comparison,
  );
}

init().catch(showError);
