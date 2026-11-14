# QueryCraft Graph Schema

## Purpose

QueryCraft's example domain is a movie graph. The schema is used to ground natural-language questions and candidate Cypher queries.

## Node labels

| Label | Meaning |
|---|---|
| `Movie` | A movie entity |
| `Person` | A person associated with a movie |
| `Genre` | A movie genre |

## Relationship types

| Relationship | Direction | Meaning |
|---|---|---|
| `ACTED_IN` | `Person -> Movie` | A person acted in a movie |
| `DIRECTED` | `Person -> Movie` | A person directed a movie |
| `IN_GENRE` | `Movie -> Genre` | A movie belongs to a genre |

## Illustrative patterns

```cypher
MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
RETURN p, m
```

```cypher
MATCH (p:Person)-[:DIRECTED]->(m:Movie)
RETURN p, m
```

```cypher
MATCH (m:Movie)-[:IN_GENRE]->(g:Genre)
RETURN m, g
```

## Property names

Property names and constraints must be confirmed from the schema notebook and the target Neo4j database. This document intentionally does not invent a complete property schema.

## Safety

Use only a development graph with synthetic or otherwise approved data. Any application that executes generated Cypher must enforce read-only access on the database server, use least-privilege credentials, and apply timeouts and result limits.
