import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "tasks_snapshot.json"
POLICY = ROOT / "subject" / "policy.py"


def load_policy():
    spec = importlib.util.spec_from_file_location("policy", POLICY)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.rank_tasks, mod.task_score


def run_once():
    payload = json.loads(DATA.read_text())
    tasks = payload.get("tasks", [])

    rank_tasks, task_score = load_policy()
    ranked = rank_tasks(tasks)

    top = []
    for t in ranked[:10]:
        top.append({
            "id": t.get("id"),
            "title": t.get("title"),
            "project": t.get("project"),
            "priority": t.get("priority"),
            "column": t.get("column"),
            "score": round(float(task_score(t)), 6),
            "blocked_count": len(t.get("blockedBy") or []),
        })

    return {
        "candidate_count": len(ranked),
        "top": top,
    }


if __name__ == "__main__":
    print(json.dumps(run_once(), indent=2))
