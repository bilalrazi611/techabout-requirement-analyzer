"""
Evaluate the analyzer on every brief in data/sample_briefs.json and write a
Markdown report to docs/EVALUATION_<mode>.md.

Usage (from the project root):
    python tests/run_eval.py --mode none    # keyword fallback, free
    python tests/run_eval.py --mode groq    # real LLM (needs key in .env)
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

parser = argparse.ArgumentParser()
parser.add_argument("--mode", default="none", help="none | groq | openai | ollama")
args = parser.parse_args()

# Must be set BEFORE importing the app (it reads the env at import time).
os.environ["LLM_PROVIDER"] = args.mode

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.services_catalog import ALL_SERVICES  # noqa: E402

client = TestClient(app)

# Service IDs a reasonable analyst would expect for each brief (any of these
# counts as a hit). Empty list = edge case with no sensible expectation.
EXPECTED = {
    1: ["enterprise-mobile", "saas-platforms", "enterprise-software", "cybersecurity"],
    2: ["ai-ml"],
    3: ["express-web-migration"],
    4: ["express-ecommerce"],
    5: ["digital-transformation", "enterprise-software"],
    6: ["ai-ml", "iot"],
    7: ["cloud-devops"],
    8: ["cybersecurity"],
    9: ["enterprise-mobile", "web-mobile"],
    10: ["data-analytics"],
    11: ["blockchain"],
    12: ["express-security"],
    13: ["saas-platforms", "web-mobile"],
    14: ["iot"],
    15: ["qa-automation"],
    16: [],
    17: [],
    18: ["express-ecommerce"],
    19: ["enterprise-software", "web-mobile", "cybersecurity"],
    20: ["express-seo"],
    21: ["digital-transformation"],
    22: ["web-mobile", "saas-platforms"],
    23: ["cloud-devops"],
    24: ["ai-ml"],
    25: [],
    26: ["ai-ml", "data-analytics", "cybersecurity", "enterprise-mobile"],
    27: ["web-mobile", "express-wordpress"],
}

ID_BY_NAME = {s["name"].lower(): s["id"] for s in ALL_SERVICES}
VALID_IDS = {s["id"] for s in ALL_SERVICES}


def to_service_id(item):
    """Turn one suggestion (string or dict) into a catalog id, or None."""
    candidates = []
    if isinstance(item, str):
        candidates.append(item)
    elif isinstance(item, dict):
        for key in ("id", "service_id", "name", "service", "service_name"):
            if isinstance(item.get(key), str):
                candidates.append(item[key])
    for c in candidates:
        if c in VALID_IDS:
            return c
        if c.lower() in ID_BY_NAME:
            return ID_BY_NAME[c.lower()]
    return None


briefs = json.loads((ROOT / "data" / "sample_briefs.json").read_text(encoding="utf-8"))

rows = []
scored = hits = 0
recall_sum = 0.0
modes_seen = set()

for case in briefs:
    expected = EXPECTED.get(case["id"], [])
    r = client.post("/analyze", json={"brief": case["brief"]})

    if r.status_code != 200:
        rows.append((case["id"], case["title"], expected, [], f"rejected ({r.status_code})"))
        continue

    data = r.json()
    modes_seen.add(data.get("mode", "?"))
    suggested = []
    unknown = 0
    for item in data.get("suggested_services", []):
        sid = to_service_id(item)
        if sid:
            suggested.append(sid)
        else:
            unknown += 1

    if expected:
        found = [e for e in expected if e in suggested]
        hit = bool(found)
        scored += 1
        hits += hit
        recall_sum += len(found) / len(expected)
        verdict = "PASS" if hit else "MISS"
    else:
        verdict = "n/a (edge case)"
    if unknown:
        verdict += f" ({unknown} unrecognised service)"

    rows.append((case["id"], case["title"], expected, suggested, verdict))
    if args.mode != "none":
        time.sleep(1.5)  # be gentle with provider rate limits

hit_rate = hits / scored * 100 if scored else 0
avg_recall = recall_sum / scored * 100 if scored else 0

lines = [
    f"# Evaluation report (LLM_PROVIDER={args.mode})",
    "",
    f"- Briefs run: {len(briefs)}",
    f"- Briefs with an expected service area: {scored}",
    f"- **Hit rate** (at least one expected service suggested): {hits}/{scored} = {hit_rate:.0f}%",
    f"- **Average recall** (share of expected services found): {avg_recall:.0f}%",
    f"- Analyzer modes seen: {', '.join(sorted(modes_seen)) or 'none'}",
    "",
    "Expected services are my own judgement of what a TechAbout analyst would pick; "
    "they are a rough benchmark, not ground truth.",
    "",
    "| # | Brief | Expected | Suggested | Result |",
    "|---|-------|----------|-----------|--------|",
]
for bid, title, exp, sug, verdict in rows:
    lines.append(
        f"| {bid} | {title} | {', '.join(exp) or '-'} | {', '.join(sug) or '-'} | {verdict} |"
    )

out = ROOT / "docs" / f"EVALUATION_{args.mode}.md"
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Hit rate {hits}/{scored} ({hit_rate:.0f}%), recall {avg_recall:.0f}%. Wrote {out}")