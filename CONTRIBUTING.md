# Contributing to QueryCraft

Thank you for your interest in improving QueryCraft. Contributions should be reproducible, documented, and safe to publish.

## Before contributing

1. Read `README.md` and `SECURITY.md`.
2. Open an issue to discuss substantial changes.
3. Do not upload private datasets, database exports, credentials, model weights, checkpoints, or adapters.
4. Keep the existing graph schema and reviewed dataset unchanged unless a change is explicitly proposed and reviewed.

## Development setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

## Quality checks

Run the test suite before submitting:

```bash
python -m pytest
```

For notebook contributions:

- Restart the kernel and run all cells where practical.
- Remove outputs containing credentials, private records, or machine-specific paths.
- Do not embed access tokens or secrets in notebook metadata or outputs.
- Explain required runtime/GPU dependencies.

## Dataset contributions

- Submit only synthetic, licensed, and non-sensitive examples.
- Keep private and reviewed training/evaluation datasets outside Git unless explicit redistribution permission exists.
- Preserve train/evaluation separation and document the schema version.
- Include provenance and licensing information for any public dataset.

## Cypher and database safety

- Treat generated queries as untrusted.
- Add tests for rejected write/admin clauses and malformed input.
- Do not add unrestricted database execution.
- Any execution feature must use server-side read-only transactions, least privilege, parameterized values, and timeouts.

## Pull request checklist

- [ ] The change has a clear purpose and description.
- [ ] Tests pass locally.
- [ ] Documentation/configuration examples are updated.
- [ ] No credentials, private data, model artifacts, or local paths are included.
- [ ] Notebook outputs have been reviewed.
- [ ] Security implications are documented.
