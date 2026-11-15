"""Neo4j read-only execution helpers."""
from __future__ import annotations

import os
from typing import Any


def execute_readonly_cypher(
    query: str,
    *,
    max_records: int = 100,
    timeout_seconds: float = 10.0,
) -> dict[str, Any]:
    """Run one query in a server-side read transaction and cap returned rows."""
    uri = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    if not all((uri, username, password)):
        raise RuntimeError(
            "Neo4j is not configured. Set NEO4J_URI, NEO4J_USERNAME, and "
            "NEO4J_PASSWORD in your local .env or Colab secrets."
        )

    try:
        from neo4j import GraphDatabase, Query
    except ImportError as exc:
        raise RuntimeError(
            "Neo4j driver is missing. Install the core requirements."
        ) from exc

    driver = GraphDatabase.driver(uri, auth=(username, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            def work(tx: Any) -> dict[str, Any]:
                result = tx.run(Query(query, timeout=timeout_seconds))
                keys = list(result.keys())
                rows = result.fetch(max_records + 1)
                truncated = len(rows) > max_records
                rows = rows[:max_records]
                return {
                    "columns": keys,
                    "rows": rows,
                    "truncated": truncated,
                }

            payload = session.execute_read(work)
            # Normalize Neo4j temporal/spatial values for JSON and Gradio.
            import json
            safe_rows = json.loads(json.dumps(payload["rows"], default=str))
            return {
                "columns": payload["columns"],
                "rows": safe_rows,
                "truncated": payload["truncated"],
            }
    finally:
        driver.close()
