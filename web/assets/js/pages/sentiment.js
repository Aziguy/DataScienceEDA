import { axis, barRadius, chart, escapeHTML, legend, tokens, tooltipRow } from "../lib/charts.js";
import { kpiTiles, showError } from "../lib/components.js";
import { loadJSON } from "../lib/data.js";
import { el, fmt } from "../lib/format.js";
import { createTextClassifier } from "../lib/models.js";

const $ = (id) => document.getElementById(id);
const LABELS = { Positive: "Positif", Neutral: "Neutre", Negative: "Négatif" };
const COLOR_SLOT = { Neutral: 0, Negative: 1, Positive: 2 };
const EXAMPLES = [
  "Best app ever, simple and beautiful. Highly recommend!",
  "It keeps crashing after the last update, waste of money.",
  "The app opens and shows the weather.",
  "Too many ads, I uninstalled it.",
  "Great content but the login is slow sometimes.",
];
const WORDCLOUDS = [
  ["general", "Tous les avis"],
  ["free_app", "Apps gratuites"],
  ["free_app_pos", "Gratuites, positifs"],
  ["free_app_neg", "Gratuites, négatifs"],
  ["paid_app", "Apps payantes"],
  ["paid_app_pos", "Payantes, positifs"],
  ["paid_app_neg", "Payantes, négatifs"],
];

const color = (label, t = tokens()) => t.series[COLOR_SLOT[label]];

function renderPrediction(classifier, text) {
  const result = classifier.predict(text);
  const t = tokens();
  $("verdict").replaceChildren(
    el("span", { class: "swatch", style: `background:${color(result.label, t)}` }),
    el("span", { text: text.trim() ? LABELS[result.label] : "–" }),
  );
  $("proba").replaceChildren(
    ...result.classes.map((label, i) =>
      el("div", { class: "proba-row" }, [
        el("span", { text: LABELS[label] }),
        el("div", { class: "proba-track" }, [
          el("div", {
            class: "proba-bar",
            style: `width:${(result.proba[i] * 100).toFixed(1)}%;background:${color(label, t)}`,
          }),
        ]),
        el("span", { class: "mono num", style: "text-align:right", text: fmt.pct(result.proba[i], 0) }),
      ]),
    ),
  );
  const top = result.contributions
    .filter((c) => Math.abs(c.weight) > 0.01)
    .sort((a, b) => Math.abs(b.weight) - Math.abs(a.weight))
    .slice(0, 8);
  $("tokens").replaceChildren(
    el("div", { class: "label muted mono", style: "font-size:11px", text: "TERMES DÉCISIFS" }),
    ...top.map((c) =>
      el("span", {
        class: "token mono",
        title: `${c.weight > 0 ? "+" : ""}${c.weight.toFixed(2)}`,
        style: `border-color:${c.weight > 0 ? color(result.label, t) : t.border}`,
        text: `${c.term} ${c.weight > 0 ? "+" : "−"}${Math.abs(c.weight).toFixed(2)}`,
      }),
    ),
  );
}

function renderByCategory(data) {
  const order = ["Positive", "Neutral", "Negative"];
  chart("chart-sent-cat", (t) => ({
    legend: legend(t, { data: order.map((k) => LABELS[k]) }),
    grid: { left: 8, right: 16, top: 36, bottom: 8, containLabel: true },
    tooltip: {
      trigger: "axis",
      axisPointer: { type: "shadow" },
      formatter: (params) =>
        `<strong>${escapeHTML(params[0].name)}</strong>` +
        params.map((p) => tooltipRow(p.color, p.seriesName, fmt.pct(p.value))).join(""),
    },
    xAxis: axis(t, { type: "value", max: 1, axisLabel: { color: t.muted, fontFamily: t.mono, fontSize: 11, formatter: (v) => fmt.pct(v, 0) } }),
    yAxis: axis(t, { type: "category", data: data.categories, inverse: true, axisLabel: { color: t.text2, fontSize: 12, interval: 0 } }),
    series: order.map((key, i) => ({
      name: LABELS[key],
      type: "bar",
      stack: "share",
      barMaxWidth: 16,
      data: data.series[key],
      itemStyle: {
        color: color(key, t),
        borderColor: t.surface,
        borderWidth: 1,
        borderRadius: i === order.length - 1 ? barRadius(true) : 0,
      },
      label: {
        show: key === "Positive",
        position: "insideLeft",
        color: "#ffffff",
        fontFamily: t.mono,
        fontSize: 11,
        formatter: (p) => fmt.pct(p.value, 0),
      },
    })),
  }));
}

function renderTerms(id, terms, label) {
  const sorted = terms.slice(0, 12);
  chart(id, (t) => ({
    tooltip: { trigger: "item", formatter: (p) => tooltipRow(color(label, t), p.name, fmt.dec(p.value)) },
    grid: { left: 8, right: 48, top: 8, bottom: 8, containLabel: true },
    xAxis: axis(t, { type: "value", axisLabel: { show: false }, splitLine: { show: false } }),
    yAxis: axis(t, { type: "category", inverse: true, data: sorted.map((x) => x.term), axisLabel: { color: t.text2, fontFamily: t.mono, fontSize: 12, interval: 0 } }),
    series: [
      {
        type: "bar",
        barMaxWidth: 14,
        data: sorted.map((x) => x.weight),
        itemStyle: { color: color(label, t), borderRadius: barRadius(true) },
        label: { show: true, position: "right", color: t.text2, fontFamily: t.mono, fontSize: 11, formatter: (p) => fmt.dec(p.value, 1) },
      },
    ],
  }));
}

function renderPolarity(data) {
  $("polarity-caption").textContent =
    `${fmt.int(data.points.length)} applications avec au moins 20 avis · Spearman ${fmt.dec(data.spearman)}`;
  chart("chart-polarity", (t) => ({
    grid: { left: 8, right: 24, top: 16, bottom: 24, containLabel: true },
    tooltip: {
      trigger: "item",
      formatter: (p) =>
        `<strong>${escapeHTML(p.value[3])}</strong>` +
        tooltipRow(t.series[0], "Polarité", fmt.dec(p.value[0])) +
        tooltipRow(t.series[0], "Note", fmt.dec(p.value[1], 1)) +
        tooltipRow(t.series[0], "Avis", fmt.int(p.value[2])),
    },
    xAxis: axis(t, { type: "value", name: "Polarité moyenne", nameLocation: "middle", nameGap: 28, min: -0.5, max: 1, interval: 0.25 }),
    yAxis: axis(t, { type: "value", name: "Note", min: 2.5, max: 5 }),
    series: [
      {
        type: "scatter",
        data: data.points,
        symbolSize: 9,
        itemStyle: { color: t.series[0], opacity: 0.75, borderColor: t.surface, borderWidth: 2 },
        emphasis: { scale: 1.5 },
      },
    ],
  }));
}

function renderConfusion({ labels, confusion }) {
  const names = labels.map((l) => LABELS[l]);
  const data = confusion.flatMap((row, i) => {
    const total = row.reduce((a, b) => a + b, 0);
    return row.map((v, j) => [j, i, v / total, v]);
  });
  chart("chart-confusion", (t) => ({
    grid: { left: 8, right: 8, top: 8, bottom: 40, containLabel: true },
    tooltip: {
      formatter: (p) =>
        `Réel ${names[p.value[1]]}, prédit ${names[p.value[0]]}<br><strong>${fmt.int(p.value[3])}</strong> avis (${fmt.pct(p.value[2])})`,
    },
    xAxis: axis(t, { type: "category", data: names, name: "Prédit", nameLocation: "middle", nameGap: 24, splitLine: { show: false }, axisLine: { show: false } }),
    yAxis: axis(t, { type: "category", data: names, inverse: true, splitLine: { show: false }, axisLine: { show: false } }),
    visualMap: { show: false, min: 0, max: 1, dimension: 2, inRange: { color: t.seq } },
    series: [
      {
        type: "heatmap",
        data: data.map((d) => ({
          value: d,
          label: { color: d[2] > 0.5 ? (t.dark ? "#04121a" : "#ffffff") : t.text },
        })),
        itemStyle: { borderColor: t.surface, borderWidth: 2, borderRadius: 4 },
        label: {
          show: true,
          fontFamily: t.mono,
          fontSize: 12,
          formatter: (p) => `${fmt.pct(p.value[2], 0)}\n${fmt.int(p.value[3])}`,
        },
      },
    ],
  }));
}

function renderGallery() {
  $("gallery").replaceChildren(
    ...WORDCLOUDS.map(([file, caption]) =>
      el("figure", {}, [
        el("img", { src: `assets/img/wordcloud/${file}.png`, alt: `Nuage de mots : ${caption}`, loading: "lazy" }),
        el("figcaption", { text: caption }),
      ]),
    ),
  );
}

async function init() {
  const [dashboard, metrics, payload] = await Promise.all([
    loadJSON("dashboard"),
    loadJSON("metrics"),
    loadJSON("sentiment_model"),
  ]);
  const m = metrics.sentiment.metrics;
  kpiTiles($("sentiment-kpis"), [
    { label: "Avis étiquetés", value: fmt.int(dashboard.kpis.labelled_reviews) },
    { label: "Part positive", value: fmt.pct(dashboard.kpis.positive_share) },
    { label: "Accuracy", value: fmt.pct(m.accuracy), note: `sur ${fmt.int(m.n_test)} avis de test` },
    { label: "F1 macro", value: fmt.dec(m.f1_macro), note: `${fmt.int(m.vocabulary_size)} termes` },
  ]);

  const classifier = createTextClassifier(payload);
  const input = $("review-input");
  const update = () => renderPrediction(classifier, input.value);
  input.addEventListener("input", update);
  document.addEventListener("themechange", update);
  $("examples").replaceChildren(
    ...EXAMPLES.map((text) =>
      el("button", {
        class: "chip",
        type: "button",
        text,
        onclick: () => {
          input.value = text;
          update();
        },
      }),
    ),
  );
  update();

  renderByCategory(dashboard.sentiment_by_category);
  renderTerms("chart-terms-pos", metrics.sentiment.top_terms.Positive, "Positive");
  renderTerms("chart-terms-neg", metrics.sentiment.top_terms.Negative, "Negative");
  renderPolarity(dashboard.polarity_vs_rating);
  renderConfusion(m);
  renderGallery();
}

init().catch(showError);
