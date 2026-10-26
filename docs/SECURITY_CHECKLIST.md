# Pre-publication security checklist

- [ ] `.env` and credentials are ignored and not staged.
- [ ] No `*.pem`, `*.key`, `*pek*`, tokens, passwords, or connection strings.
- [ ] No private datasets or database exports.
- [ ] No trained LoRA adapters, checkpoints, or model weights.
- [ ] Notebook outputs inspected and cleared if they contain sensitive values.
- [ ] Synthetic data and licenses reviewed.
- [ ] Generated Cypher validated; execution is read-only and time-limited.
- [ ] Git status and staged diff reviewed before every push.
- [ ] If a secret was ever committed, revoke it and clean Git history as appropriate.
