"""Conservative lexical screening before a server-side read transaction.

This is not a complete Cypher parser. Neo4j least-privilege credentials and
server-side read transactions remain mandatory.
"""
import re

FORBIDDEN = re.compile(
    r"\b(CREATE|MERGE|DELETE|DETACH|SET|REMOVE|DROP|ALTER|GRANT|DENY|REVOKE|"
    r"LOAD\s+CSV|CALL|FOREACH|APOC)\b",
    re.IGNORECASE,
)
ALLOWED_START = re.compile(
    r"^(MATCH|OPTIONAL\s+MATCH|WITH|UNWIND|RETURN)\b", re.IGNORECASE
)


def validate_readonly_cypher(query: str) -> tuple[bool, str]:
    if not query or not query.strip():
        return False, "Query is empty."
    q = query.strip()
    if len(q) > 4000:
        return False, "Query exceeds the configured length limit."
    statement = q[:-1].rstrip() if q.endswith(";") else q
    if ";" in statement:
        return False, "Multiple statements are not allowed."
    if FORBIDDEN.search(statement):
        return False, "Potential write, procedure, or administrative clause detected."
    if not ALLOWED_START.match(statement):
        return False, "Query must begin with an allowed read clause."
    if statement.count("/*") != statement.count("*/"):
        return False, "Unbalanced block comment delimiters."
    if statement.count("/*") or re.search(r"(^|\s)//", statement):
        return False, "Cypher comments are not allowed in generated queries."
    return True, "Accepted by basic lexical checks only; server-side read-only access is still required."
