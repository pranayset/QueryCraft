# Architecture

1. **Question input** — user submits a natural-language question.
2. **Generator** — baseline placeholder now; later replace with Gemma 3 inference.
3. **Validation** — reject obvious write/admin clauses and malformed input. Lexical checks alone are not a security boundary.
4. **Optional execution layer** — if added, use a dedicated least-privilege Neo4j account, read-only transaction, query timeout, and development database.
5. **UI** — Gradio displays generated Cypher; the starter does not execute queries.

## Suggested next steps
- Define and document the graph schema.
- Build a small synthetic dataset and manually review every pair.
- Record baseline results before fine-tuning.
- Fine-tune in a suitable GPU environment; keep adapters and weights outside Git.
- Evaluate exact match, execution accuracy, invalid-query rate, and safety rejection rate.
