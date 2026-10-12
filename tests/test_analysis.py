import pytest
from core.analysis import analyze_query, candidate_index_guidance

def test_select_star_flagged():
    result = analyze_query("SELECT * FROM users")
    assert any(x["issue"] == "select-star" for x in result["findings"])

def test_empty_query_rejected():
    with pytest.raises(ValueError):
        analyze_query(" ")

def test_function_predicate_flagged():
    result = analyze_query("SELECT id FROM users WHERE LOWER(email) = 'a'")
    assert any(x["issue"] == "function-on-filter-column" for x in result["findings"])

def test_leading_wildcard_flagged():
    result = analyze_query("SELECT id FROM items WHERE name LIKE '%gear'")
    assert any(x["issue"] == "leading-wildcard-like" for x in result["findings"])

def test_missing_context_disclosed():
    result = analyze_query("SELECT id FROM t")
    assert "schema and existing indexes" in result["missing_context"]

def test_candidate_index_empty():
    assert candidate_index_guidance([])["candidates"] == []

def test_candidate_index_tradeoffs():
    result = candidate_index_guidance(["customer_id"])
    assert "write and maintenance overhead" in result["candidates"][0]["tradeoffs"]

def test_findings_are_unbenchmarked():
    result = analyze_query("SELECT id FROM t")
    assert "not benchmarked" in result["evidence_type"]
