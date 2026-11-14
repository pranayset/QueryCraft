"""Gradio starter interface for QueryCraft.

The current generator is a deterministic placeholder. It previews Cypher and
does not connect to or execute queries against Neo4j.
"""

import gradio as gr

from .generator import generate_cypher
from .validation import validate_readonly_cypher


def run_question(question: str) -> tuple[str, str]:
    """Generate a preview and return the basic validator result."""
    try:
        candidate = generate_cypher(question)
        accepted, reason = validate_readonly_cypher(candidate)
        status = ("Accepted by basic checks: " if accepted else "Rejected: ") + reason
        return candidate, status
    except Exception as exc:
        return "", f"Unable to generate a preview: {exc}"


def main() -> None:
    with gr.Blocks(title="QueryCraft | Natural Language to Cypher") as demo:
        gr.Markdown(
            "# QueryCraft\n"
            "### Natural-language questions to read-only Cypher previews\n"
            "**Prototype status:** this public starter uses a deterministic placeholder "
            "generator. It does not load the fine-tuned Gemma adapter or execute queries."
        )
        question = gr.Textbox(
            label="Natural-language question",
            placeholder="How many movies are in the graph?",
            lines=2,
        )
        generate = gr.Button("Generate Cypher preview", variant="primary")
        query = gr.Code(label="Cypher preview", language="sql")
        validation = gr.Textbox(label="Basic validation result", interactive=False)
        generate.click(run_question, inputs=question, outputs=[query, validation])
        gr.Markdown(
            "Do not treat lexical validation as a security boundary. "
            "Never execute generated queries against a production database."
        )
    demo.launch()


if __name__ == "__main__":
    main()
