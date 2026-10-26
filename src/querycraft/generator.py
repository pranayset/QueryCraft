"""Replace this baseline with your validated Gemma 3 inference pipeline."""
from .validation import validate_readonly_cypher

def generate_cypher(question: str) -> str:
    """Return a safe placeholder query until model inference is implemented."""
    if not question or not question.strip():
        raise ValueError("Please enter a natural-language question.")
    # This deterministic placeholder keeps the starter runnable.
    # Replace with model inference and validate its output before execution.
    candidate = "MATCH (m:Movie) RETURN count(m) AS answer"
    ok, reason = validate_readonly_cypher(candidate)
    if not ok:
        raise ValueError(f"Generated query rejected: {reason}")
    return candidate
