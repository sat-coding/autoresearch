import json
import sys
from pathlib import Path


def evaluate(run_artifact: dict) -> dict:
    top = run_artifact.get("top", [])
    if not top:
        return {
            "primary_metric": 1.0,
            "secondary": {"reason": "no_candidates"},
            "status": "bad",
            "notes": "lower is better",
        }

    # Real policy objective: maximize executable + high-priority picks at top ranks.
    # Convert to minimization metric.
    reward = 0.0
    for i, t in enumerate(top[:5]):
        rank_weight = 1.0 / (i + 1)
        priority_bonus = {"high": 1.0, "medium": 0.6, "low": 0.3}.get(str(t.get("priority", "")).lower(), 0.4)
        blocked_penalty = 1.0 if (t.get("blocked_count", 0) > 0) else 0.0
        executable_bonus = 1.0 if str(t.get("column")) in {"Inbox", "Planned"} else 0.0
        reward += rank_weight * (priority_bonus + 0.5 * executable_bonus - 1.2 * blocked_penalty)

    # Normalize roughly to [0,1+] and convert to minimization.
    normalized = max(0.0, min(2.0, reward / 3.0))
    primary_metric = round(1.0 - normalized, 6)

    return {
        "primary_metric": primary_metric,
        "secondary": {
            "reward": round(reward, 6),
            "top5": top[:5],
            "candidate_count": run_artifact.get("candidate_count", 0),
        },
        "status": "ok",
        "notes": "lower is better (more executable high-priority top picks)",
    }


if __name__ == "__main__":
    run_json = Path(sys.argv[1])
    run_data = json.loads(run_json.read_text())
    print(json.dumps(evaluate(run_data), indent=2))
