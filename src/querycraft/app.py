"""Minimal Gradio starter UI."""
import gradio as gr
from .generator import generate_cypher

def run_question(question: str) -> str:
    try:
        return generate_cypher(question)
    except Exception as exc:
        return f"Error: {exc}"

def main() -> None:
    with gr.Blocks(title="QueryCraft") as demo:
        gr.Markdown("# QueryCraft\nNatural language to read-only Cypher — starter UI")
        question = gr.Textbox(label="Question", placeholder="How many movies are in the database?")
        output = gr.Code(label="Generated Cypher", language="sql")
        submit = gr.Button("Generate")
        submit.click(run_question, inputs=question, outputs=output)
        gr.Markdown("**Important:** This starter does not execute queries against Neo4j.")
    demo.launch()

if __name__ == "__main__":
    main()
