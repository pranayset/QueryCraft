# Gemma 3 4B + Neo4j integration

This branch adds the runnable inference and evaluation path. It does not include
model weights, LoRA adapter files, datasets, or Neo4j credentials.

## Runtime prerequisites

- A Colab GPU runtime with a supported CUDA/PyTorch/bitsandbytes combination.
- Google Drive mounted and the private adapter folder accessible.
- Hugging Face access to `google/gemma-3-4b-it` if the base model is not cached.
- A Neo4j movie graph containing `Movie(title, released)`, `Person`, and
  `Genre`, with `ACTED_IN`, `DIRECTED`, and `IN_GENRE` relationships.
- A dedicated Neo4j account with read-only privileges.

## Configure Colab

Mount Drive, then install the repository and dependencies:

```python
from google.colab import drive
drive.mount("/content/drive")

%cd /content/QueryCraft
!pip install -r requirements.txt
!pip install -r requirements-model.txt
!pip install -e .
```

Set environment variables without writing secrets into notebook cells or Git:

```python
import os
from getpass import getpass

os.environ["MODEL_ID"] = "google/gemma-3-4b-it"
os.environ["ADAPTER_PATH"] = (
    "/content/drive/MyDrive/QueryCraft_Gemma3_4B/final_adapter"
)
os.environ["LOAD_IN_4BIT"] = "true"
os.environ["HF_TOKEN"] = getpass("Hugging Face token: ")
os.environ["NEO4J_URI"] = getpass("Neo4j URI: ")
os.environ["NEO4J_USERNAME"] = "querycraft_readonly"
os.environ["NEO4J_PASSWORD"] = getpass("Neo4j read-only password: ")
os.environ["NEO4J_DATABASE"] = "neo4j"
```

If your final adapter is in a different folder, change only `ADAPTER_PATH`.
The directory must contain `adapter_config.json` and
`adapter_model.safetensors`. Do not upload that folder to GitHub.

## Launch Gradio

```python
!python app.py
```

The first model request loads the 4-bit NF4 base model and attaches the LoRA
adapter. First load may take several minutes. Keep the Colab runtime alive while
using the Gradio URL. A CPU-only runtime is not supported by this 4B/4-bit
configuration.

The interface displays generated Cypher, lexical validation, and the bounded
Neo4j result preview. It never executes a query rejected by the validator.

## Run evaluation

```bash
python -m querycraft.evaluation --output reports/querycraft_evaluation.csv
```

The starter evaluation file contains eight questions retained from the project
notebook. It reports generation, lexical validation, expected-pattern matching,
and actual read-transaction execution. Pattern matching is a heuristic, not a
semantic correctness metric. The optional `expected_answer` field can be added
to a case after independently verifying the expected record against your graph;
only then is exact answer matching reported.

## Important safety notes

- The Python validator is a conservative lexical screen, not a complete Cypher
  parser. A query passing it is not proven semantically correct or safe.
- Queries run inside Neo4j's server-side read transaction, but the database
  credential must also be a least-privilege read-only account.
- The app caps displayed results at 100 rows and applies a query timeout.
- Do not expose the Gradio app publicly with database credentials in an
  untrusted environment. Use an authenticated/private deployment.
- Do not use production databases for model-generated queries.

## Results and reproducibility

Save the generated CSV report locally or as a private artifact. Publish only
aggregate metrics after checking that rows, database values, credentials, and
private test records are not present. Record the adapter revision, base model,
runtime GPU, package versions, evaluation date, and graph snapshot/version.
