"""Gradio interface for Gemma 3 LoRA Cypher generation and optional Neo4j reads."""
from __future__ import annotations

import json
import gradio as gr

from .generator import generate_cypher
from .validation import validate_readonly_cypher


def run_question(question: str, execute: bool = False) -> tuple[str, str, str]:
    """Generate, validate, and optionally execute a read-only graph query."""
    try:
        candidate = generate_cypher(question)
        accepted, reason = validate_readonly_cypher(candidate)
        if not accepted:
            return candidate, f"Rejected: {reason}", "Not executed."
        status = f"Accepted by lexical checks: {reason}"
        if not execute:
            return candidate, status, "Execution disabled. Enable the explicit execution option to query Neo4j."
        from .database import execute_readonly_cypher
        payload = execute_readonly_cypher(candidate)
        preview = {
            "columns": payload["columns"],
            "rows": payload["rows"],
            "truncated": payload["truncated"],
        }
        return candidate, status + "\nNeo4j read transaction: SUCCESS", json.dumps(preview, indent=2, ensure_ascii=False)
    except Exception as exc:
        return "", f"Unable to complete request: {type(exc).__name__}: {exc}", "No database result."


def main() -> None:
    with gr.Blocks(title="QueryCraft | Gemma 3 to Cypher") as demo:
        gr.Markdown(
            "# QueryCraft\n"
            "### Gemma 3 4B + LoRA → validated Cypher → optional Neo4j read transaction\n"
            "**Model loading is lazy:** the first question loads the private adapter. "
            "Set ADAPTER_PATH and the Neo4j environment variables before use."
        )
        question = gr.Textbox(
            label="Natural-language question",
            placeholder="Which people acted in The Matrix?",
            lines=2,
        )
        execute = gr.Checkbox(
            label="Execute accepted query against configured Neo4j read-only database",
            value=False,
        )
        generate = gr.Button("Generate Cypher", variant="primary")
        query = gr.Code(label="Generated Cypher", language="sql")
        validation = gr.Textbox(label="Validation and execution status", lines=3, interactive=False)
        results = gr.Code(label="Neo4j result preview (JSON)", language="json")
        generate.click(run_question, inputs=[question, execute], outputs=[query, validation, results])
        gr.Markdown(
            "**Safety:** lexical validation is not a Cypher parser or security boundary. "
            "Use a dedicated least-privilege Neo4j read-only account. Do not connect this "
            "demo to a production database or expose it publicly with credentials."
        )
    demo.launch()


if __name__ == "__main__":
    main()
