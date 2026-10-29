// Shared chrome: navigation, theme toggle and footer injected on every page.

import { loadJSON } from "./data.js";

const PAGES = [
  { href: "index.html", label: "Tableau de bord" },
  { href: "explore.html", label: "Exploration" },
  { href: "sentiment.html", label: "Sentiment" },
  { href: "model.html", label: "Modèle" },
  { href: "about.html", label: "Méthodologie" },
];
const REPO = "https://github.com/Aziguy/DataScienceEDA";
const STORAGE_KEY = "psi-theme";

const ICONS = {
  sun: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
  moon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
  github: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 .5a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2.1c-3.3.7-4-1.6-4-1.6-.6-1.4-1.4-1.8-1.4-1.8-1.1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1.1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.8-1.6-2.7-.3-5.5-1.3-5.5-6 0-1.3.5-2.4 1.2-3.2-.1-.3-.5-1.5.1-3.2 0 0 1-.3 3.3 1.2a11.5 11.5 0 0 1 6 0C17.3 4.6 18.3 5 18.3 5c.7 1.7.3 2.9.1 3.2.8.8 1.2 1.9 1.2 3.2 0 4.6-2.8 5.6-5.5 6 .4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A12 12 0 0 0 12 .5z"/></svg>',
  menu: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
};

function storedTheme() {
  try {
    return localStorage.getItem(STORAGE_KEY);
  } catch {
    return null;
  }
}

function currentTheme() {
  const forced = document.documentElement.dataset.theme;
  if (forced) return forced;
  return matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  try {
    localStorage.setItem(STORAGE_KEY, theme);
  } catch {
    /* storage unavailable */
  }
  document.dispatchEvent(new CustomEvent("themechange", { detail: theme }));
}

function nav() {
  const current = location.pathname.split("/").pop() || "index.html";
  const links = PAGES.map(
    (p) =>
      `<li><a href="${p.href}"${p.href === current ? ' aria-current="page"' : ""}>${p.label}</a></li>`,
  ).join("");
  const header = document.createElement("header");
  header.className = "nav";
  header.innerHTML = `
    <div class="container">
      <a class="brand" href="index.html"><img src="assets/img/logo.svg" alt="" width="28" height="28">Playstore Insights<small>v2</small></a>
      <ul class="nav-links" id="nav-links">${links}</ul>
      <div class="nav-actions">
        <button class="icon-btn" id="theme-toggle" type="button" aria-label="Changer de thème"></button>
        <a class="icon-btn" href="${REPO}" aria-label="Code source sur GitHub" target="_blank" rel="noopener">${ICONS.github}</a>
        <button class="icon-btn menu-btn" id="menu-toggle" type="button" aria-label="Menu" aria-controls="nav-links" aria-expanded="false">${ICONS.menu}</button>
      </div>
    </div>`;
  document.body.prepend(header);

  const toggle = header.querySelector("#theme-toggle");
  const paint = () => {
    toggle.innerHTML = currentTheme() === "dark" ? ICONS.sun : ICONS.moon;
  };
  paint();
  toggle.addEventListener("click", () => {
    applyTheme(currentTheme() === "dark" ? "light" : "dark");
    paint();
  });

  const menu = header.querySelector("#menu-toggle");
  menu.addEventListener("click", () => {
    const open = header.dataset.open !== "true";
    header.dataset.open = String(open);
    menu.setAttribute("aria-expanded", String(open));
  });
}

function skipLink() {
  const link = document.createElement("a");
  link.className = "skip-link";
  link.href = "#main";
  link.textContent = "Aller au contenu";
  document.body.prepend(link);
}

async function footer() {
  const node = document.createElement("footer");
  node.className = "footer";
  node.innerHTML = `
    <div class="container">
      <span>Playstore Insights · Team Data Analytics · Licence MIT</span>
      <span class="mono" id="build-meta"></span>
    </div>`;
  document.body.append(node);
  try {
    const meta = await loadJSON("meta");
    node.querySelector("#build-meta").textContent =
      `v${meta.version} · ${meta.commit} · ${meta.built_at.slice(0, 10)}`;
  } catch {
    /* meta is optional */
  }
}

const saved = storedTheme();
if (saved) document.documentElement.dataset.theme = saved;
nav();
skipLink();
footer();
