# QueryCraft: Natural Language to Cypher with Gemma 3

QueryCraft is a learning project for translating natural-language questions into read-only Cypher queries for a Neo4j movie graph. It is designed as a GitHub-ready starter structure.

> **Security note:** This repository intentionally excludes secrets, private datasets, trained LoRA adapters, model weights, checkpoints, and local environment files. Add only synthetic or properly licensed data that you are authorized to publish.

## Features
- Prompt-based baseline and optional Gemma 3 / PEFT LoRA workflow
- Neo4j read-only query execution pattern
- Gradio UI starter
- Validation tests and evaluation scaffolding
- Security-first repository hygiene

## Repository layout

```text
QueryCraft/
├── configs/                 # Safe, non-secret configuration examples
├── data/
│   ├── README.md            # Dataset policy and safe placement instructions
│   └── synthetic/           # Publishable synthetic examples only
├── docs/                    # Architecture, roadmap, and security notes
├── notebooks/               # Exploration and training notebooks
├── src/querycraft/          # Reusable application code
├── tests/                   # Unit tests
├── .env.example             # Placeholder variables only
├── .gitignore
├── requirements.txt
├── SECURITY.md
└── README.md
```

## Quick start (Windows PowerShell)

```powershell
# 1. Extract the ZIP and enter the project folder
cd .\QueryCraft_GitHub_Starter

# 2. Create and activate a virtual environment
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Create your local environment file
Copy-Item .env.example .env
# Edit .env locally with your own credentials. Never commit it.

# 5. Run tests
python -m pytest

# 6. Start the starter Gradio app
python -m querycraft.app
```

If PowerShell blocks activation, use `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that PowerShell session only, then activate the environment.

## Configuration

Set the following in your local `.env` file:
- `NEO4J_URI`
- `NEO4J_USERNAME`
- `NEO4J_PASSWORD`
- `NEO4J_DATABASE` (usually `neo4j` for AuraDB)
- `MODEL_ID` (default example: `google/gemma-3-1b-it`)

Never paste API keys, passwords, access tokens, private keys, or production connection strings into notebooks, source files, screenshots, or Git history.

## Model and training files

Do **not** commit:
- `*.pem`, `*.key`, `*.p12`, `*.pfx`, `*pek*`
- `.env` files and credentials
- private or non-redistributable datasets
- model weights, checkpoints, and trained LoRA/PEFT adapters
- Hugging Face cache and other downloaded model files

Store large or sensitive artifacts outside the repository, or in an approved private artifact store. Review model and dataset licenses before use.

## Development status

This starter is a safe scaffold, not a trained or production-ready model. Add your reviewed synthetic dataset, implement your model inference/training workflow, validate every generated query, and test it against a disposable development database before deployment.

## License

Choose a license only after confirming that every included source file and dataset may be distributed under it. No license is provided by this starter.
