# Implementation roadmap

- [ ] Verify Neo4j development database and graph schema.
- [ ] Create synthetic examples and manually review Cypher.
- [ ] Implement prompt-based baseline inference.
- [ ] Evaluate baseline on held-out examples.
- [ ] Fine-tune Gemma 3 with LoRA/PEFT only after dataset review.
- [ ] Save adapters outside the public repository.
- [ ] Compare baseline and fine-tuned model.
- [ ] Add parser-based validation and read-only Neo4j execution.
- [ ] Test timeouts, empty prompts, invalid Cypher, write clauses, and schema mismatch.
- [ ] Review notebook outputs and Git diff for secrets before publication.
- [ ] Deploy only against a disposable or explicitly approved read-only database.
