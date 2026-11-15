"""Lazy Gemma 3 4B + PEFT adapter inference for QueryCraft.

The model and adapter stay outside Git. The loader follows the training notebook's
Gemma3ForConditionalGeneration + AutoTokenizer + PeftModel architecture.
"""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

SYSTEM_PROMPT = """You generate Cypher queries for the QueryCraft graph database.
Use only the supplied schema. Do not invent labels, properties, or relationship
types. Return only one read-only Cypher query. Never generate CREATE, MERGE, SET,
DELETE, REMOVE, DROP, CALL, LOAD CSV, FOREACH, or write procedures.

GRAPH SCHEMA:
Nodes:
- Movie(title, released)
- Person
- Genre

Relationships:
- (Person)-[:ACTED_IN]->(Movie)
- (Person)-[:DIRECTED]->(Movie)
- (Movie)-[:IN_GENRE]->(Genre)
"""


class GemmaCypherGenerator:
    """Loads the private adapter only when first needed."""

    def __init__(self) -> None:
        self.model: Any = None
        self.tokenizer: Any = None
        self.device: str | None = None

    def load(self) -> None:
        if self.model is not None:
            return

        adapter_dir = Path(os.getenv(
            "ADAPTER_PATH",
            "/content/drive/MyDrive/QueryCraft_Gemma3_4B/final_adapter",
        )).expanduser()
        model_id = os.getenv("MODEL_ID", "google/gemma-3-4b-it")
        if not (adapter_dir / "adapter_config.json").is_file():
            raise FileNotFoundError(
                f"LoRA adapter_config.json not found in {adapter_dir}. "
                "Mount Google Drive and set ADAPTER_PATH to the folder containing "
                "adapter_config.json and adapter_model.safetensors."
            )
        if not (adapter_dir / "adapter_model.safetensors").is_file():
            raise FileNotFoundError(
                f"adapter_model.safetensors not found in {adapter_dir}."
            )

        try:
            import torch
            from transformers import AutoTokenizer, BitsAndBytesConfig, Gemma3ForConditionalGeneration
            from peft import PeftModel
        except ImportError as exc:
            raise RuntimeError(
                "Model dependencies are missing. Install the model extras listed "
                "in requirements-model.txt in a compatible Colab GPU runtime."
            ) from exc

        if not torch.cuda.is_available():
            raise RuntimeError(
                "Gemma 3 4B is configured for 4-bit GPU inference. Select a CUDA "
                "GPU runtime in Colab before loading the model."
            )

        token = os.getenv("HF_TOKEN") or None
        self.tokenizer = AutoTokenizer.from_pretrained(
            str(adapter_dir), token=token, use_fast=True
        )
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        load_in_4bit = os.getenv("LOAD_IN_4BIT", "true").lower() in {
            "1", "true", "yes", "on"
        }
        kwargs: dict[str, Any] = {
            "torch_dtype": torch.float16,
            "device_map": "auto",
            "attn_implementation": os.getenv("ATTENTION_IMPLEMENTATION", "eager"),
            "token": token,
        }
        if load_in_4bit:
            kwargs["quantization_config"] = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
            )

        base = Gemma3ForConditionalGeneration.from_pretrained(model_id, **kwargs)
        self.model = PeftModel.from_pretrained(
            base, str(adapter_dir), is_trainable=False
        )
        self.model.eval()
        if hasattr(self.model.config, "use_cache"):
            self.model.config.use_cache = True
        self.device = str(self.model.device)

    @staticmethod
    def _clean_output(text: str) -> str:
        text = re.sub(r"```(?:cypher)?", "", text, flags=re.IGNORECASE)
        text = text.replace("```", "").strip()
        # If the model emits a short preamble, keep the first Cypher clause.
        match = re.search(
            r"\b(?:OPTIONAL\s+MATCH|MATCH|WITH|UNWIND|RETURN)\b",
            text,
            flags=re.IGNORECASE,
        )
        if match:
            text = text[match.start():]
        return text.strip()

    def generate(self, question: str, max_new_tokens: int = 128) -> str:
        if not question or not question.strip():
            raise ValueError("Enter a natural-language question.")
        self.load()

        import torch

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": "Translate this question into Cypher:\n" + question.strip(),
            },
        ]
        prompt = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        eos_ids = [self.tokenizer.eos_token_id]
        end_turn_id = self.tokenizer.convert_tokens_to_ids("<end_of_turn>")
        if (
            end_turn_id is not None
            and end_turn_id != self.tokenizer.unk_token_id
            and end_turn_id not in eos_ids
        ):
            eos_ids.append(end_turn_id)

        with torch.inference_mode():
            output = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                eos_token_id=eos_ids,
                pad_token_id=self.tokenizer.pad_token_id,
            )
        new_tokens = output[0, inputs["input_ids"].shape[1]:]
        decoded = self.tokenizer.decode(new_tokens, skip_special_tokens=True)
        return self._clean_output(decoded)
