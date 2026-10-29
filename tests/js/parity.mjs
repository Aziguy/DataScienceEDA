// Reads {rating, rows, sentiment, texts} JSON on stdin, prints browser-runtime predictions.
import { createTextClassifier, predictGradientBoosting } from "../../web/assets/js/lib/models.js";
import { deriveInput, toRow } from "../../web/assets/js/lib/features.js";

const chunks = [];
for await (const chunk of process.stdin) chunks.push(chunk);
const input = JSON.parse(Buffer.concat(chunks).toString("utf-8"));

const rating = input.records.map((record) => {
  const row = toRow(input.rating.features, deriveInput(record, input.reference_date));
  return predictGradientBoosting(input.rating.model, row);
});
const classifier = createTextClassifier(input.sentiment);
const sentiment = input.texts.map((text) => classifier.predict(text).proba);
process.stdout.write(JSON.stringify({ rating, sentiment }));
