// Mirror of `playstore_insights.features`: builds the model row from a form input.

const MISSING = -1;
const TRANSFORMS = { log1p: Math.log1p, identity: (v) => v };
const DAY_MS = 86_400_000;

export function deriveInput(input, referenceDate) {
  const ref = Date.parse(referenceDate);
  const updated = Date.parse(input.last_updated);
  const days = Number.isFinite(updated) ? Math.max(0, Math.round((ref - updated) / DAY_MS)) : NaN;
  return {
    ...input,
    days_since_update: days,
    reviews_per_install: input.reviews / Math.max(1, input.installs),
  };
}

export function toRow(spec, input) {
  return spec.map((feat) => {
    if (feat.kind === "onehot") return input[feat.source] === feat.value ? 1 : 0;
    const raw = input[feat.source];
    const value = raw === null || raw === undefined || raw === "" ? NaN : Number(raw);
    const out = TRANSFORMS[feat.transform](value);
    return Number.isFinite(out) ? out : MISSING;
  });
}
