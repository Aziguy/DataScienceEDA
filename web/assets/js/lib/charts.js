// ECharts wrapper: reads design tokens from CSS and re-renders on theme or size change.

const registry = new Map();

export function tokens() {
  const css = getComputedStyle(document.documentElement);
  const v = (name) => css.getPropertyValue(`--${name}`).trim();
  return {
    text: v("text"),
    text2: v("text-2"),
    muted: v("muted"),
    surface: v("surface-solid"),
    border: v("border-strong"),
    grid: v("chart-grid"),
    axis: v("chart-axis"),
    series: [v("series-1"), v("series-2"), v("series-3"), v("series-4")],
    seq: [v("seq-0"), v("seq-1"), v("seq-2"), v("seq-3"), v("seq-4")],
    diverging: [v("div-neg"), v("div-mid"), v("div-pos")],
    dark: css.colorScheme === "dark" || v("color-scheme") === "dark",
    mono: v("font-mono"),
    sans: v("font-sans"),
  };
}

function base(t) {
  return {
    backgroundColor: "transparent",
    textStyle: { fontFamily: t.sans, color: t.text2 },
    animationDuration: 500,
    grid: { left: 8, right: 16, top: 16, bottom: 8, containLabel: true },
    tooltip: {
      backgroundColor: t.surface,
      borderColor: t.border,
      borderWidth: 1,
      padding: [8, 12],
      textStyle: { color: t.text, fontSize: 13 },
      extraCssText: "border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,.18);",
    },
  };
}

export function axis(t, extra = {}) {
  return {
    axisLine: { lineStyle: { color: t.axis } },
    axisTick: { show: false },
    axisLabel: { color: t.muted, fontFamily: t.mono, fontSize: 11 },
    splitLine: { lineStyle: { color: t.grid } },
    nameTextStyle: { color: t.muted, fontFamily: t.mono, fontSize: 11 },
    ...extra,
  };
}

export function valueAxis(t, extra = {}) {
  const compact = new Intl.NumberFormat("fr-FR", { notation: "compact", maximumFractionDigits: 1 });
  return axis(t, {
    type: "value",
    ...extra,
    axisLabel: {
      color: t.muted,
      fontFamily: t.mono,
      fontSize: 11,
      formatter: (v) => compact.format(v),
      ...extra.axisLabel,
    },
  });
}

export function legend(t, extra = {}) {
  return {
    top: 0,
    left: 0,
    icon: "roundRect",
    itemWidth: 10,
    itemHeight: 10,
    textStyle: { color: t.text2, fontSize: 12 },
    ...extra,
  };
}

export const barRadius = (horizontal) => (horizontal ? [0, 4, 4, 0] : [4, 4, 0, 0]);

export function tooltipRow(color, label, value) {
  const key = `<span style="display:inline-block;width:12px;height:2px;margin-right:8px;vertical-align:middle;background:${color}"></span>`;
  return `<div style="display:flex;justify-content:space-between;gap:16px"><span>${key}${escapeHTML(label)}</span><strong>${escapeHTML(value)}</strong></div>`;
}

export function escapeHTML(value) {
  return String(value).replace(/[&<>"']/g, (c) => `&#${c.charCodeAt(0)};`);
}

function render(id) {
  const entry = registry.get(id);
  const t = tokens();
  entry.instance.setOption({ ...base(t), ...entry.build(t) }, true);
}

export function chart(id, build) {
  const node = document.getElementById(id);
  if (!node || !window.echarts) return null;
  let entry = registry.get(id);
  if (!entry) {
    entry = { instance: window.echarts.init(node, null, { renderer: "canvas" }), build };
    registry.set(id, entry);
    new ResizeObserver(() => entry.instance.resize()).observe(node);
  }
  entry.build = build;
  render(id);
  return entry.instance;
}

export function rerenderAll() {
  for (const id of registry.keys()) render(id);
}

document.addEventListener("themechange", rerenderAll);
