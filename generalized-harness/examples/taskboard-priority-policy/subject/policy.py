"""Mutable policy surface: rank candidate tasks for auto-start.

Agent should tune weights/logic in this file only.
"""

from datetime import datetime, timezone


WEIGHTS = {
    "priority": 1.0,
    "age": 0.25,
    "todo_ready": 0.35,
    "blocked_penalty": 2.0,
    "failed_penalty": 1.2,
}


def _priority_score(p: str) -> float:
    return {"high": 1.0, "medium": 0.6, "low": 0.3}.get(str(p or "").lower(), 0.4)


def _age_days(created_at: str) -> float:
    if not created_at:
        return 0.0
    try:
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        return max(0.0, (now - dt).total_seconds() / 86400.0)
    except Exception:
        return 0.0


def task_score(task: dict) -> float:
    priority = _priority_score(task.get("priority"))
    age = min(_age_days(task.get("createdAt")), 30.0) / 30.0

    todos = task.get("todos") or []
    pending = sum(1 for t in todos if (t.get("status") or "pending") == "pending")
    todo_ready = 1.0 if pending > 0 else 0.4

    blocked = 1.0 if (task.get("blockedBy") or []) else 0.0

    runs = task.get("runs") or []
    last_failed = 1.0 if runs and (runs[0].get("status") == "failed") else 0.0

    score = (
        WEIGHTS["priority"] * priority
        + WEIGHTS["age"] * age
        + WEIGHTS["todo_ready"] * todo_ready
        - WEIGHTS["blocked_penalty"] * blocked
        - WEIGHTS["failed_penalty"] * last_failed
    )
    return float(score)


def rank_tasks(tasks: list[dict]) -> list[dict]:
    candidates = [
        t for t in tasks
        if (t.get("column") in {"Inbox", "Planned"})
    ]
    return sorted(candidates, key=task_score, reverse=True)
