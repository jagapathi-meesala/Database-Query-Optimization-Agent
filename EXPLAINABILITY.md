# Explainability

This document explains the agent's inputs, decision process, outputs, and limitations.

## Inputs
The agent accepts SQL query text and optional database engine/version, schema definitions, existing indexes, approximate table sizes, query parameters, and query-plan excerpts. Missing information is recorded as an uncertainty rather than guessed.

## Decision
The agent applies transparent heuristic checks to identify common risks such as broad scans, non-sargable predicates, unnecessary selected columns, join-key mismatches, repeated correlated work, and ordering or grouping costs. It proposes candidate indexes only when the supplied query and schema provide a rationale. Recommendations are hypotheses until measured.

## Limits
The agent does not connect to a database or execute queries. It cannot infer actual runtime, cardinality, selectivity, locking, or I/O without evidence. Recommendations depend on the engine, version, statistics, data distribution, and workload. Indexes can increase write cost and storage. Validate changes in staging and retain a rollback path.

## Tool: analyze-sql-query

### Inputs and Data Sources
Receives SQL text and optional engine, schema, index, and query-plan context supplied by the user.

### Decision and Reasoning
Checks query text for common patterns that may affect performance and labels findings as heuristics, not measured facts.

### Outputs and Evidence
Returns findings, their rationale, and missing context needed for stronger conclusions.

### Limits and Constraints
Text-only inspection cannot determine the actual execution plan or runtime behavior.

### Failure Handling
If query text is empty or invalid, request a corrected query. If context is missing, report the limitation explicitly.

### Human Review
A developer or DBA verifies findings against the actual plan and representative workload.

## Tool: recommend-indexes

### Inputs and Data Sources
Receives query text, table/column context, existing indexes, and database engine when supplied.

### Decision and Reasoning
Suggests candidate indexes based on observed filter, join, and ordering columns. It avoids claiming that a candidate is optimal without plan and workload evidence.

### Outputs and Evidence
Returns candidate indexes with rationale, expected trade-offs, and validation steps.

### Limits and Constraints
Index syntax and capabilities differ by engine. Composite-column order, selectivity, write frequency, and existing indexes affect usefulness.

### Failure Handling
When schema or engine details are insufficient, request them or return conditional guidance rather than fabricated DDL.

### Human Review
A DBA checks redundancy, write overhead, storage impact, and engine-specific syntax before deployment.

## Tool: create-optimization-plan

### Inputs and Data Sources
Receives query findings, schema context, plan excerpts, and workload constraints supplied by the user.

### Decision and Reasoning
Prioritizes experiments by likely impact, confidence, risk, and ease of measurement.

### Outputs and Evidence
Produces a staged plan that includes a baseline, one change at a time, repeatable measurements, acceptance criteria, and rollback notes.

### Limits and Constraints
No benchmark or performance improvement is asserted unless supplied as measured evidence.

### Failure Handling
If a baseline, plan, or workload description is absent, mark the plan provisional and list required evidence.

### Human Review
The database owner approves changes and validates them in staging before production rollout.

## Data Quality and Uncertainty
Query plans and statistics may be stale or unrepresentative. The agent must distinguish facts in the supplied evidence from hypotheses and must not invent measurements.

## Safety and Responsible Use
Do not provide credentials or unredacted personal data. Treat generated SQL and index suggestions as drafts requiring review. Avoid running `EXPLAIN ANALYZE` on expensive or mutating statements without understanding engine behavior.

## Audit and Reproducibility
Record the query version, engine/version, schema/index context, plan, dataset characteristics, proposed change, and before/after measurements so reviewers can reproduce the decision.
