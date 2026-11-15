"""Offline-batch generation, lexical checks, and live Neo4j evaluation."""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

from .database import execute_readonly_cypher
from .model import GemmaCypherGenerator
from .validation import validate_readonly_cypher

DEFAULT_CASES = Path(__file__).resolve().parents[2] / "data" / "evaluation" / "golden_questions.jsonl"


def evaluate_cases(
    cases_path: str | Path = DEFAULT_CASES,
    output_path: str | Path = "evaluation_results.csv",
) -> list[dict[str, Any]]:
    generator = GemmaCypherGenerator()
    results: list[dict[str, Any]] = []

    with Path(cases_path).open(encoding="utf-8") as handle:
        cases = [json.loads(line) for line in handle if line.strip()]

    for case in cases:
        row: dict[str, Any] = {
            "id": case["id"],
            "question": case["question"],
            "generated_cypher": "",
            "lexical_valid": False,
            "expected_pattern_match": None,
            "neo4j_execution": "NOT_RUN",
            "returned_rows": 0,
            "answer_match": None,
            "error": "",
        }
        try:
            query = generator.generate(case["question"])
            row["generated_cypher"] = query
            valid, reason = validate_readonly_cypher(query)
            row["lexical_valid"] = valid
            if not valid:
                row["error"] = reason
            else:
                pattern = case.get("expected_pattern")
                if pattern:
                    row["expected_pattern_match"] = bool(
                        re.search(pattern, query, flags=re.IGNORECASE)
                    )
                payload = execute_readonly_cypher(query)
                row["neo4j_execution"] = "SUCCESS"
                row["returned_rows"] = len(payload["rows"])
                expected = case.get("expected_answer")
                if expected is not None:
                    row["answer_match"] = expected in payload["rows"]
        except Exception as exc:
            row["error"] = f"{type(exc).__name__}: {exc}"
            if row["lexical_valid"]:
                row["neo4j_execution"] = "FAILED"
        results.append(row)

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", default=str(DEFAULT_CASES))
    parser.add_argument("--output", default="evaluation_results.csv")
    args = parser.parse_args()
    results = evaluate_cases(args.cases, args.output)
    total = len(results)
    lexical = sum(bool(x["lexical_valid"]) for x in results)
    executed = sum(x["neo4j_execution"] == "SUCCESS" for x in results)
    pattern = sum(x["expected_pattern_match"] is True for x in results)
    print(f"Cases: {total} | Lexically valid: {lexical} | Executed: {executed}")
    print(f"Expected-pattern matches: {pattern}")
    print(f"Detailed report: {args.output}")


if __name__ == "__main__":
    main()
