# Database Query Optimization Agent

A planning-oriented agent for reviewing SQL query text, schema context, indexes, and query-plan excerpts. It highlights likely bottlenecks and proposes measurable, reversible optimization experiments.

## Capabilities
- Review query structure and identify common performance risks.
- Suggest candidate indexes based on supplied predicates, joins, and ordering.
- Produce a staged optimization plan with measurement and rollback guidance.
- Explain assumptions, evidence, and uncertainty.

## Quick start
Requires Python 3.10+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python3 verification/readiness_audit.py
```

## Input guidance
Provide database engine/version, query text, relevant schema and existing indexes, representative row counts, parameter patterns, and `EXPLAIN` / `EXPLAIN ANALYZE` output where appropriate. Redact secrets and personal data. `EXPLAIN ANALYZE` executes the query on many engines; use caution with expensive or mutating statements.

## Limitations
Recommendations are heuristics and are not a substitute for testing against representative data in a staging environment. Indexes can slow writes and consume storage. Query plans and behavior vary by engine/version and data distribution. The agent does not connect to databases or execute SQL.
