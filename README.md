# QueryCraft — Natural Language to Cypher Graph Queries

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Gradio-demo-orange)](https://www.gradio.app/)
[![Graph DB](https://img.shields.io/badge/Graph-Neo4j-018BFF)](https://neo4j.com/)
[![Model](https://img.shields.io/badge/Model-Gemma%203-8E75B2)](https://ai.google.dev/gemma)

QueryCraft is a portfolio project exploring natural-language-to-Cypher generation for a small Neo4j movie graph. The project separates graph-schema design, dataset preparation, model experimentation, query validation, and a Gradio interface.

> **Project status:** The repository currently provides a runnable Gradio starter and basic lexical read-only checks. The checked-in generator is a deterministic placeholder, not the fine-tuned Gemma model. Model training, adapter loading, and end-to-end execution must be configured and evaluated separately before describing them as production-ready.

## Project goals

- Translate natural-language questions into Cypher for a documented graph schema.
- Explore Gemma 3 instruction-tuned models and PEFT/LoRA fine-tuning.
- Validate generated queries before any optional database interaction.
- Keep private datasets, credentials, model weights, and adapters outside Git.
- Provide reproducible notebooks, configuration examples, tests, and documentation.

## Graph schema

The project schema uses these node labels: `Movie`, `Person`, and `Genre`. The documented relationship types are `ACTED_IN`, `DIRECTED`, and `IN_GENRE`. See the [schema notebook](notebooks/QueryCraft_AI_Graph_Schema_Based_on_Google_Deepmind_Course.ipynb) and [architecture](ARCHITECTURE.md).

## Repository layout

```text
QueryCraft/
├── app.py                         # Convenience launcher for Gradio
├── README.md
├── ARCHITECTURE.md
├── CONTRIBUTING.md
├── SECURITY.md
├── CITATION.cff
├── requirements.txt
├── pyproject.toml
├── .env.example
├── .gitignore
├── configs/                        # Safe YAML examples; no secrets
├── data/                           # Public, reviewed synthetic samples only
├── docs/                            # Design notes and project guidance
├── notebooks/                       # Google Colab/Jupyter notebooks
├── src/querycraft/                  # Reusable Python package
└── tests/                           # Automated tests
```

## Google Colab notebook

Open the existing [QueryCraft AI Graph Schema notebook](notebooks/QueryCraft_AI_Graph_Schema_Based_on_Google_Deepmind_Course.ipynb) in GitHub and select **Open in Colab**. Before publishing notebook changes, clear outputs that may contain tokens, local paths, private records, or credentials.

## Quick start

### Windows PowerShell

```powershell
git clone https://github.com/pranayset/QueryCraft.git
cd QueryCraft

py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

# Run the Gradio starter
python app.py

# Run tests
python -m pytest
```

### Linux / macOS

```bash
git clone https://github.com/pranayset/QueryCraft.git
cd QueryCraft
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
python app.py
python -m pytest
```

## Configuration

Copy `.env.example` to `.env` for local configuration. Populate secrets only in the local file or an approved secret manager. Never commit `.env`.

The checked-in YAML example is at `configs/config.example.yaml`. Model IDs and optional local adapter paths must be reviewed against the actual runtime. Do not put adapter files, weights, or credentials in the repository.

## Model development

The project has previously explored Gemma 3 4B IT with LoRA/PEFT and a Neo4j AuraDB movie-graph schema. Training artifacts and private reviewed datasets are intentionally not distributed in this repository. Use the notebooks and documentation as the reproducibility entry point; record the exact model revision, dataset version, configuration, hardware, and evaluation results when publishing future experiments.

## Safety boundary

- Treat generated Cypher as untrusted input.
- The included validator is a basic lexical filter, not a Cypher parser or security boundary.
- Do not execute model output against a production database.
- If database execution is added, use a dedicated least-privilege Neo4j account, server-side read-only transactions, parameterized values, and query timeouts.
- Never rely on prompt instructions or client-side checks as the only protection.

See [SECURITY.md](SECURITY.md) for the reporting and security policy.

## What is excluded from Git

The repository excludes private/raw datasets, environment files, API keys, `*.pem` and related key material, model weights, checkpoints, LoRA/PEFT adapters, local database dumps, and notebook checkpoints. Review `.gitignore` before every push. If a secret was committed, revoke it; deleting it in a later commit does not remove it from Git history.

## Contributing and citation

- Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.
- See [CITATION.cff](CITATION.cff) for citation metadata.
- See [docs/ROADMAP.md](docs/ROADMAP.md) for planned work.

## License

No license has been selected for this repository yet. Until a license is added, do not assume that the code or included materials may be reused, modified, or redistributed.
