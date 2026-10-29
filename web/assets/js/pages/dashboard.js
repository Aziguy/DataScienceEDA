import { axis, barRadius, chart, tooltipRow, valueAxis } from "../lib/charts.js";
import { kpiTiles, showError, simpleTable } from "../lib/components.js";
import { loadJSON } from "../lib/data.js";
import { el, fmt } from "../lib/format.js";

function renderKpis(k) {
  kpiTiles(document.getElementById("kpis"), [
    { label: "Applications", value: fmt.int(k.apps), note: `${k.categories} catégories` },
    { label: "Note moyenne", value: fmt.dec(k.avg_rating), note: "sur 5 étoiles" },
    { label: "Gratuites", value: fmt.pct(k.free_share), note: "du catalogue" },
    { label: "Installations", value: fmt.compact(k.total_installs), note: "cumulées (bornes basses)" },
    { label: "Avis analysés", value: fmt.int(k.labelled_reviews), note: `${fmt.pct(k.positive_share, 0)} positifs` },
  ]);
}

function renderInsights(d) {
  const ranked = d.categories.filter((c) => c.apps >= 50).sort((a, b) => b.avg_rating - a.avg_rating);
  const best = ranked[0];
  const worst = ranked.at(-1);
  const tiers = d.installs_tiers;
  const top = tiers.avg_rating.at(-1);
  const mid = tiers.avg_rating[1];
  const [free, paid] = ["Free", "Paid"].map((t) => d.free_vs_paid.find((r) => r.type === t));
  const sent = d.sentiment_by_category;
  const items = [
    {
      icon: "01",
      title: "La popularité va avec la satisfaction",
      text: `Les applications à plus de 100 M d'installations ont une note moyenne de ${fmt.dec(top)} contre ${fmt.dec(mid)} pour celles entre 1k et 100k.`,
    },
    {
      icon: "02",
      title: `${best.category} en tête`,
      text: `Meilleure note moyenne (${fmt.dec(best.avg_rating)}) parmi les catégories d'au moins 50 apps. ${worst.category} ferme la marche (${fmt.dec(worst.avg_rating)}).`,
    },
    {
      icon: "03",
      title: "Payer pour mieux noter",
      text: `Les apps payantes sont légèrement mieux notées (${fmt.dec(paid.avg_rating)} contre ${fmt.dec(free.avg_rating)}) mais visent des audiences ${fmt.int(free.median_installs / paid.median_installs)} fois plus petites.`,
    },
    {
      icon: "04",
      title: "Les avis confirment la note",
      text: `La polarité moyenne des avis est corrélée à la note (Spearman ${fmt.dec(d.polarity_vs_rating.spearman)}). ${sent.categories[0]} reçoit la plus forte part d'avis positifs.`,
    },
  ];
  document.getElementById("insights").replaceChildren(
    ...items.map((i) =>
      el("article", { class: "card insight span-3" }, [
        el("div", { class: "insight-icon", text: i.icon }),
        el("div", {}, [el("h3", { text: i.title }), el("p", { text: i.text })]),
      ]),
    ),
  );
}

function horizontalBars(id, labels, values, format, colorIndex = 0) {
  chart(id, (t) => ({
    tooltip: {
      trigger: "item",
      formatter: (p) => tooltipRow(t.series[colorIndex], p.name, format(p.value)),
    },
    xAxis: axis(t, { type: "value", axisLabel: { show: false }, splitLine: { show: false } }),
    yAxis: axis(t, {
      type: "category",
      data: labels,
      inverse: true,
      axisLabel: { color: t.text2, fontSize: 12 },
    }),
    series: [
      {
        type: "bar",
        data: values,
        barMaxWidth: 18,
        itemStyle: { color: t.series[colorIndex], borderRadius: barRadius(true) },
        label: {
          show: true,
          position: "right",
          color: t.text2,
          fontFamily: t.mono,
          fontSize: 11,
          formatter: (p) => format(p.value),
        },
        emphasis: { itemStyle: { opacity: 0.85 } },
      },
    ],
    grid: { left: 8, right: 56, top: 8, bottom: 8, containLabel: true },
  }));
}

function columns(id, labels, values, { format, xName, colorIndex = 0, labelTop = false }) {
  chart(id, (t) => ({
    tooltip: {
      trigger: "axis",
      axisPointer: { type: "shadow" },
      formatter: ([p]) => `${p.name}${tooltipRow(t.series[colorIndex], xName, format(p.value))}`,
    },
    xAxis: axis(t, { type: "category", data: labels, splitLine: { show: false } }),
    yAxis: valueAxis(t),
    series: [
      {
        type: "bar",
        data: values,
        barMaxWidth: 24,
        barCategoryGap: "20%",
        itemStyle: { color: t.series[colorIndex], borderRadius: barRadius(false) },
        label: labelTop
          ? { show: true, position: "top", color: t.text2, fontFamily: t.mono, fontSize: 11, formatter: (p) => format(p.value) }
          : { show: false },
      },
    ],
  }));
}

function renderCharts(d) {
  const cats = d.categories.slice(0, 15);
  horizontalBars("chart-categories", cats.map((c) => c.category), cats.map((c) => c.apps), fmt.int);

  const dist = d.rating_distribution;
  columns("chart-ratings", dist.bins.map((b) => b.toFixed(1)), dist.counts, {
    format: fmt.int,
    xName: "Applications",
  });

  const tiers = d.installs_tiers;
  columns("chart-tiers", tiers.labels, tiers.apps, {
    format: fmt.int,
    xName: "Applications",
    labelTop: true,
  });

  chart("chart-tier-rating", (t) => ({
    tooltip: {
      trigger: "axis",
      formatter: ([p]) => `${p.name}${tooltipRow(t.series[0], "Note moyenne", fmt.dec(p.value))}`,
    },
    xAxis: axis(t, { type: "category", data: tiers.labels, boundaryGap: false, splitLine: { show: false } }),
    yAxis: valueAxis(t, { min: 3.9, max: 4.5, interval: 0.1, axisLabel: { formatter: (v) => fmt.dec(v, 1) } }),
    series: [
      {
        type: "line",
        data: tiers.avg_rating,
        smooth: false,
        symbol: "circle",
        symbolSize: 9,
        lineStyle: { width: 2, color: t.series[0] },
        itemStyle: { color: t.series[0], borderColor: t.surface, borderWidth: 2 },
        areaStyle: { color: t.series[0], opacity: 0.1 },
        label: {
          show: true,
          position: "top",
          color: t.text2,
          fontFamily: t.mono,
          fontSize: 11,
          formatter: (p) => fmt.dec(p.value),
        },
      },
    ],
  }));

  const years = d.updates_by_year;
  columns("chart-years", years.years.map(String), years.apps, {
    format: fmt.int,
    xName: "Applications",
    labelTop: true,
  });

  horizontalBars(
    "chart-content",
    d.content_rating.map((c) => c.label),
    d.content_rating.map((c) => c.apps),
    fmt.int,
  );
}

function renderTypeTable(rows) {
  const label = { Free: "Gratuit", Paid: "Payant" };
  simpleTable(
    document.getElementById("table-type"),
    [
      { label: "Modèle", format: (r) => label[r.type] },
      { label: "Applications", num: true, format: (r) => fmt.int(r.apps) },
      { label: "Note moyenne", num: true, format: (r) => fmt.dec(r.avg_rating) },
      { label: "Installations médianes", num: true, format: (r) => fmt.int(r.median_installs) },
      { label: "Avis médians", num: true, format: (r) => fmt.int(r.median_reviews) },
    ],
    rows,
  );
}

loadJSON("dashboard")
  .then((d) => {
    renderKpis(d.kpis);
    renderInsights(d);
    renderCharts(d);
    renderTypeTable(d.free_vs_paid);
  })
  .catch(showError);
