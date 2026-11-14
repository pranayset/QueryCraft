# QueryCraft Architecture

## 1. Purpose

QueryCraft explores natural-language-to-Cypher generation for a Neo4j movie graph. The repository separates the graph schema, data preparation, model experimentation, query validation, and user interface.

## 2. Graph schema

The current project schema documents three node labels:

- `Movie`
- `Person`
- `Genre`

Relationship types:

- `(:Person)-[:ACTED_IN]->(:Movie)`
- `(:Person)-[:DIRECTED]->(:Movie)`
- `(:Movie)-[:IN_GENRE]->(:Genre)`

Confirm property names against the schema notebook and live development database; do not infer properties from labels alone.

## 3. Logical workflow

```text
Natural-language question
          |
          v
Question preprocessing
          |
          v
Gemma 3 inference (planned / optional integration)
          |
          v
Candidate Cypher query
          |
          v
Read-only validation and policy checks
          |
          v
Gradio query preview
          |
          v
Optional Neo4j read-only execution (not enabled in starter)
```

## 4. Repository components

| Component | Responsibility |
|---|---|
| `notebooks/` | Google Colab/Jupyter exploration and experiments |
| `configs/` | Non-secret configuration examples |
| `data/` | Publishable synthetic examples only |
| `src/querycraft/` | Reusable Python package |
| `tests/` | Unit tests for validation and application behavior |
| `app.py` | Gradio launcher |
| `docs/` | Supporting technical documentation |

## 5. Model lifecycle

The project has explored Gemma 3 instruction-tuned models and PEFT/LoRA. Training must be performed in a suitable runtime. Keep model weights, checkpoints, tokenizer caches, and trained adapters outside the public repository. Record model ID/revision, quantization, LoRA configuration, dataset version, random seed, hardware, and evaluation metrics in a reproducibility report.

## 6. Security model

Generated Cypher is untrusted. The included lexical validator is a convenience guardrail only; it is not a parser and cannot prove a query is safe. The current starter UI previews generated text and does not execute it against Neo4j.

If execution is implemented later:

1. Use a dedicated least-privilege database account.
2. Enforce read-only transactions on the server.
3. Parameterize user values.
4. Apply query timeouts and result limits.
5. Validate using a Cypher parser or equivalent structural policy.
6. Never connect a public demo to production data.

## 7. Current implementation status

The repository includes a Gradio starter and deterministic placeholder generator. It is not yet a verified end-to-end fine-tuned LLM application. Update this section when model-backed inference and evaluation are implemented and tested.
