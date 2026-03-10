# Taskboard Priority Policy (Real Example)

A real, operations-flavored harness example built on a live snapshot from your dashboard.

## What is optimized?

- Mutable surface: `subject/policy.py`
- Problem: rank **Inbox/Planned** tasks for auto-start (which should be started next)

## Data source

- `data/tasks_snapshot.json`
- Generated from live dashboard API (`/api/tasks`) at capture time

## Objective

`evaluator.py` rewards top-ranked tasks that are:
- higher priority
- executable now (Inbox/Planned)
- not blocked

`primary_metric` is minimized (lower is better).

## Run test

```bash
cd generalized-harness/examples/taskboard-priority-policy
python3 loop.py
cat results.tsv
```

## Iterate with an agent

Allow edits only in `subject/policy.py`, then loop experiments and keep/revert by metric.
