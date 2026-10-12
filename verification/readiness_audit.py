from pathlib import Path
import sys
root = Path(__file__).resolve().parents[1]
required = [
    "agent.yaml", "SOUL.md", "README.md", "RULES.md", "DUTIES.md", "AGENTS.md",
    "EXPLAINABILITY.md", "requirements.txt", "pytest.ini", "core/analysis.py",
    "tools/analyze-sql-query.yaml", "tools/recommend-indexes.yaml",
    "tools/create-optimization-plan.yaml", "skills/query-analysis/SKILL.md",
    "skills/index-planning/SKILL.md", "skills/safe-optimization/SKILL.md",
    "tests/test_analysis.py", "verification/readiness_audit.py"
]
missing = [p for p in required if not (root / p).is_file()]
if missing:
    print("FAIL: missing required files:", ", ".join(missing))
    sys.exit(1)
print(f"PASS: all {len(required)}/{len(required)} required files present")
