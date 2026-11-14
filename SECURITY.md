# Security Policy

## Scope

QueryCraft is an educational/portfolio prototype for natural-language-to-Cypher experimentation. Reports are welcome for vulnerabilities in code and configuration maintained in this repository.

## Reporting a vulnerability

Please do not disclose credentials, personal information, private datasets, or exploit details in a public issue. Use GitHub's private vulnerability reporting feature for this repository if it is enabled. Otherwise, contact the repository maintainer through a verified private channel. Include a concise description, impact, reproduction steps, and suggested mitigation where possible.

## Secret and artifact handling

- Keep credentials in a local `.env` file or an approved secret manager.
- Never commit API tokens, passwords, private keys, `*.pem`, `*.pek`, certificates, database dumps, or cloud credentials.
- If a secret is exposed, revoke or rotate it immediately. Removing the file in a later commit does not remove it from Git history.
- Do not publish private datasets, model weights, checkpoints, or LoRA/PEFT adapters without explicit redistribution permission.
- Review notebook cells, outputs, metadata, screenshots, and commit diffs before pushing.

## Cypher and database safety

- Treat all model-generated Cypher as untrusted input.
- The included lexical validator is a basic prototype guardrail, not a complete parser and not a security boundary.
- Do not execute generated queries against production data.
- Any future execution feature must use a dedicated least-privilege Neo4j account, server-side read-only transactions, query timeouts, result limits, and parameterized values.
- Reject write and administrative operations at the database boundary; do not rely on prompt instructions or UI checks alone.
- Do not expose Neo4j credentials to a public Gradio client.

## Dependencies and deployment

- Install reviewed dependencies and monitor security advisories.
- Keep secrets in deployment secret settings, never in source code or notebook cells.
- Restrict public demos to synthetic or otherwise approved data.
- A passing test suite does not establish that the application is secure.

## Supported versions

This policy applies to the current public repository state on the default branch. Security fixes are handled as maintainers are able to review and validate them.
