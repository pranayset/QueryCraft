"""Basic guardrails for generated Cypher.

This is intentionally conservative starter validation, not a complete Cypher parser.
Use a parser and server-side read-only transaction for stronger enforcement.
"""
import re

FORBIDDEN = re.compile(
    r"\b(CREATE|MERGE|DELETE|DETACH|SET|REMOVE|DROP|ALTER|GRANT|DENY|REVOKE|LOAD\s+CSV|CALL\s+DBMS)\b",
    re.IGNORECASE,
)

def validate_readonly_cypher(query: str) -> tuple[bool, str]:
    if not query or not query.strip():
        return False, "Query is empty."
    q = query.strip()
    if len(q) > 4000:
        return False, "Query exceeds the configured length limit."
    # Permit one optional trailing semicolon, but reject embedded/multiple statements.
    without_trailing = q[:-1] if q.endswith(";") else q
    if ";" in without_trailing:
        return False, "Multiple statements are not allowed."
    if FORBIDDEN.search(q):
        return False, "Potential write or administrative clause detected."
    if not re.match(r"^(MATCH|OPTIONAL\s+MATCH|WITH|UNWIND|RETURN)\b", q, re.IGNORECASE):
        return False, "Query must begin with an allowed read clause."
    return True, "Accepted by basic lexical checks; execute only in a read-only transaction."
