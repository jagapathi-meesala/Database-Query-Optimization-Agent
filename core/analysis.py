"""Offline heuristic analysis for SQL query optimization."""
import re

def analyze_query(sql: str, engine: str = "unspecified", schema_context: str = "") -> dict:
    if not isinstance(sql, str) or not sql.strip():
        raise ValueError("sql must be a non-empty string")
    normalized = re.sub(r"\s+", " ", sql.strip())
    findings = []
    if re.search(r"SELECT\s+\*", normalized, re.I):
        findings.append({"issue": "select-star", "confidence": "medium",
                         "reason": "SELECT * may retrieve unnecessary columns.",
                         "suggestion": "Select only columns required by the caller."})
    if re.search(r"WHERE\s+LOWER\s*\(", normalized, re.I) or re.search(r"WHERE\s+UPPER\s*\(", normalized, re.I):
        findings.append({"issue": "function-on-filter-column", "confidence": "medium",
                         "reason": "A function applied to a filtered column may prevent use of a conventional index.",
                         "suggestion": "Check the plan; consider a matching expression index or a sargable predicate if supported."})
    if re.search(r"LIKE\s+['\"]%", normalized, re.I):
        findings.append({"issue": "leading-wildcard-like", "confidence": "medium",
                         "reason": "A leading wildcard often prevents a conventional B-tree index from supporting the search.",
                         "suggestion": "Consider engine-specific full-text or trigram search if appropriate."})
    if re.search(r"ORDER BY", normalized, re.I) and not schema_context:
        findings.append({"issue": "ordering-needs-plan-review", "confidence": "low",
                         "reason": "Ordering can require a sort, but schema and plan context were not supplied.",
                         "suggestion": "Inspect the execution plan and available indexes before proposing changes."})
    return {"engine": engine or "unspecified", "findings": findings,
            "evidence_type": "static heuristic; not benchmarked",
            "missing_context": [x for x, present in [
                ("database engine and version", engine not in ("", None, "unspecified")),
                ("schema and existing indexes", bool(schema_context))
            ] if not present]}

def candidate_index_guidance(columns: list[str], reason: str = "filter/join") -> dict:
    clean = [c.strip() for c in columns if isinstance(c, str) and c.strip()]
    if not clean:
        return {"candidates": [], "note": "Supply relevant columns and schema context before suggesting an index."}
    return {"candidates": [{"columns": clean, "reason": reason,
                            "status": "candidate for review",
                            "tradeoffs": ["additional storage", "write and maintenance overhead"]}],
            "note": "Confirm column order and usefulness using the engine-specific plan and representative workload."}
