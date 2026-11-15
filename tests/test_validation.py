from querycraft.validation import validate_readonly_cypher


def test_accepts_read_query():
    ok, _ = validate_readonly_cypher("MATCH (m:Movie) RETURN count(m) AS answer")
    assert ok


def test_rejects_write_query():
    ok, message = validate_readonly_cypher("MATCH (m:Movie) SET m.title = 'x' RETURN m")
    assert not ok
    assert "write" in message.lower()


def test_rejects_multiple_statements():
    ok, _ = validate_readonly_cypher("MATCH (m) RETURN m; MATCH (n) RETURN n")
    assert not ok


def test_rejects_empty_query():
    ok, _ = validate_readonly_cypher("   ")
    assert not ok


def test_rejects_call_procedure():
    ok, _ = validate_readonly_cypher("CALL db.labels() YIELD label RETURN label")
    assert not ok


def test_rejects_comments():
    ok, _ = validate_readonly_cypher("MATCH (m) // bypass\n RETURN m")
    assert not ok


def test_accepts_optional_match():
    ok, _ = validate_readonly_cypher(
        "MATCH (p:Person) OPTIONAL MATCH (p)-[:ACTED_IN]->(m:Movie) RETURN p, m"
    )
    assert ok
