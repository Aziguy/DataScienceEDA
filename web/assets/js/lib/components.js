// Small DOM components shared across pages.

import { el, fmt } from "./format.js";

export function kpiTiles(container, items) {
  container.replaceChildren(
    ...items.map(({ label, value, note }) =>
      el("article", { class: "card kpi" }, [
        el("div", { class: "kpi-label", text: label }),
        el("div", { class: "kpi-value num", text: value }),
        note ? el("div", { class: "kpi-note", text: note }) : null,
      ]),
    ),
  );
}

export function simpleTable(table, columns, rows) {
  const head = el(
    "tr",
    {},
    columns.map((c) => el("th", { class: c.num ? "num" : "", scope: "col", text: c.label })),
  );
  const body = rows.map((row) =>
    el(
      "tr",
      {},
      columns.map((c) => el("td", { class: c.num ? "num" : "", text: c.format(row) })),
    ),
  );
  table.replaceChildren(el("thead", {}, head), el("tbody", {}, body));
}

export function showError(error) {
  const main = document.getElementById("main");
  main.prepend(
    el("div", { class: "card section", role: "alert" }, [
      el("h3", { text: "Données indisponibles" }),
      el("p", {
        class: "muted",
        text: `${error.message}. Lancez « make site » puis servez le dossier build/site.`,
      }),
    ]),
  );
}

export class DataTable {
  constructor(table, columns, { pageSize = Infinity, sort = null, pager = null } = {}) {
    Object.assign(this, { table, columns, pageSize, sort, pager, rows: [], page: 0 });
    pager?.prev.addEventListener("click", () => this.go(this.page - 1));
    pager?.next.addEventListener("click", () => this.go(this.page + 1));
  }

  setRows(rows) {
    this.rows = rows;
    this.page = 0;
    this.render();
  }

  go(page) {
    this.page = Math.max(0, Math.min(page, this.pages() - 1));
    this.render();
  }

  pages() {
    return Math.max(1, Math.ceil(this.rows.length / this.pageSize));
  }

  sorted() {
    if (!this.sort) return this.rows;
    const { key, dir } = this.sort;
    const factor = dir === "ascending" ? 1 : -1;
    return [...this.rows].sort((a, b) => {
      const x = a[key];
      const y = b[key];
      if (x === null || x === undefined) return 1;
      if (y === null || y === undefined) return -1;
      return (typeof x === "string" ? x.localeCompare(y, "fr") : x - y) * factor;
    });
  }

  toggle(key) {
    const dir = this.sort?.key === key && this.sort.dir === "descending" ? "ascending" : "descending";
    this.sort = { key, dir };
    this.page = 0;
    this.render();
  }

  render() {
    const head = el(
      "tr",
      {},
      this.columns.map((c) => {
        const th = el("th", { class: c.num ? "num" : "", scope: "col" });
        if (this.sort?.key === c.key) th.setAttribute("aria-sort", this.sort.dir);
        th.append(el("button", { type: "button", text: c.label, onclick: () => this.toggle(c.key) }));
        return th;
      }),
    );
    const start = Number.isFinite(this.pageSize) ? this.page * this.pageSize : 0;
    const visible = this.sorted().slice(start, start + this.pageSize);
    const body = visible.map((row) =>
      el(
        "tr",
        {},
        this.columns.map((c) =>
          el("td", { class: [c.num ? "num" : "", c.class ?? ""].join(" ").trim(), text: c.format(row), title: c.title ? c.format(row) : "" }),
        ),
      ),
    );
    this.table.replaceChildren(el("thead", {}, head), el("tbody", {}, body));
    if (this.pager) {
      const end = Math.min(start + this.pageSize, this.rows.length);
      this.pager.info.textContent = this.rows.length
        ? `${fmt.int(start + 1)}–${fmt.int(end)} sur ${fmt.int(this.rows.length)}`
        : "Aucun résultat";
      this.pager.prev.disabled = this.page === 0;
      this.pager.next.disabled = this.page >= this.pages() - 1;
    }
  }
}
