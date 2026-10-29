// Pure inference runtime for the exported models (no DOM, runs in browsers and Node).

export function predictGradientBoosting(model, row) {
  const x = row.map(Math.fround);
  let total = 0;
  for (const tree of model.trees) {
    let node = 0;
    while (tree.f[node] !== -1) {
      node = x[tree.f[node]] <= tree.t[node] ? tree.l[node] : tree.r[node];
    }
    total += tree.v[node];
  }
  return model.init + model.learning_rate * total;
}

const TOKEN = /[\p{L}\p{N}_]{2,}/gu;

export function tokenize(text) {
  return text.toLowerCase().match(TOKEN) ?? [];
}

export function ngrams(tokens, [min, max]) {
  const out = [];
  for (let n = min; n <= max; n += 1) {
    for (let i = 0; i + n <= tokens.length; i += 1) out.push(tokens.slice(i, i + n).join(" "));
  }
  return out;
}

export function createTextClassifier(payload) {
  const index = new Map(payload.vocabulary.map((term, i) => [term, i]));

  function vectorize(text) {
    const counts = new Map();
    for (const term of ngrams(tokenize(text), payload.ngram_range)) {
      const i = index.get(term);
      if (i !== undefined) counts.set(i, (counts.get(i) ?? 0) + 1);
    }
    const weights = new Map();
    let norm = 0;
    for (const [i, tf] of counts) {
      const w = (payload.sublinear_tf ? 1 + Math.log(tf) : tf) * payload.idf[i];
      weights.set(i, w);
      norm += w * w;
    }
    norm = Math.sqrt(norm) || 1;
    for (const [i, w] of weights) weights.set(i, w / norm);
    return weights;
  }

  function predict(text) {
    const x = vectorize(text);
    const scores = payload.coef.map((row, k) => {
      let s = payload.intercept[k];
      for (const [i, w] of x) s += row[i] * w;
      return s;
    });
    const max = Math.max(...scores);
    const exp = scores.map((s) => Math.exp(s - max));
    const sum = exp.reduce((a, b) => a + b, 0);
    const proba = exp.map((e) => e / sum);
    const best = proba.indexOf(Math.max(...proba));
    const contributions = [...x].map(([i, w]) => ({
      term: payload.vocabulary[i],
      weight: payload.coef[best][i] * w,
    }));
    return { label: payload.classes[best], classes: payload.classes, proba, contributions };
  }

  return { predict, vectorize };
}
