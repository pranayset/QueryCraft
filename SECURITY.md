# Security Policy

## Supported scope
This is a learning starter project. Security reports should focus on vulnerabilities in code included in this repository.

## Reporting a concern
Do not publish credentials, private keys, personal data, private datasets, or exploit details in a public issue. Remove sensitive values and report the issue privately to the repository maintainer using GitHub's private vulnerability reporting feature, if enabled. If private reporting is unavailable, contact the maintainer through a verified private channel.

## Secret handling
- Keep credentials in a local `.env` file or an approved secret manager.
- Never commit `.env`, cloud credentials, `*.pem`, `*.key`, `*.p12`, `*.pfx`, tokens, or database dumps.
- If a secret is committed, revoke/rotate it immediately. Deleting the file in a later commit does not remove it from Git history.
- Use least-privilege Neo4j credentials and a dedicated development database.

## Cypher safety
- Treat model-generated Cypher as untrusted input.
- Allow only an explicit read-only query policy; reject write clauses and multiple statements.
- Use server-side read-only transactions and query timeouts where supported.
- Validate query structure and parameters before execution. Do not rely on prompt instructions alone.
- Never connect a public demo to a production database.

## Data and model artifacts
- Publish only synthetic or appropriately licensed datasets.
- Do not commit private datasets, model weights, checkpoints, or trained LoRA/PEFT adapters unless distribution is explicitly authorized.
- Inspect notebooks for outputs containing secrets before publishing.

## Dependency hygiene
- Install from a reviewed dependency list, keep packages updated, and investigate security advisories.
- Do not treat a successful test run as proof that the application is secure.
