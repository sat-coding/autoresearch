import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "eval_set.json"


def _contains(text: str, needle: str) -> bool:
    return re.search(r"\b" + re.escape(needle.lower()) + r"\b", text.lower()) is not None


def evaluate(run_artifact: dict) -> dict:
    cases = {c["id"]: c for c in json.loads(DATA.read_text())}
    per_case = []
    score_sum = 0.0

    for row in run_artifact["outputs"]:
        c = cases[row["id"]]
        text = row["response"]
        req_hits = sum(1 for k in c["required"] if _contains(text, k))
        req_score = req_hits / max(1, len(c["required"]))

        forbidden_hits = sum(1 for w in c["forbidden"] if _contains(text, w))
        forbid_penalty = 0.25 * forbidden_hits

        length_penalty = 0.15 if len(text) > c["max_chars"] else 0.0

        case_score = max(0.0, req_score - forbid_penalty - length_penalty)
        score_sum += case_score
        per_case.append({
            "id": c["id"],
            "score": round(case_score, 4),
            "required_hit": req_hits,
            "required_total": len(c["required"]),
            "forbidden_hits": forbidden_hits,
            "chars": len(text),
        })

    avg_score = score_sum / max(1, len(per_case))
    return {
        "primary_metric": round(1.0 - avg_score, 6),
        "secondary": {
            "avg_score": round(avg_score, 6),
            "cases": per_case,
        },
        "status": "ok",
        "notes": "primary_metric lower is better",
    }


if __name__ == "__main__":
    run_json = Path(sys.argv[1])
    run_data = json.loads(run_json.read_text())
    print(json.dumps(evaluate(run_data), indent=2))
