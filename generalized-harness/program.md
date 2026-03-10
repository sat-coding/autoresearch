# program.md (generalized)

You are an autonomous research agent.

## Scope

- You may modify files only under `subject/`.
- You must not modify `runner.py`, `evaluator.py`, `loop.py`.

## Goal

Minimize `primary_metric` reported by `evaluator.py`.

## Loop

1. Inspect current state and prior rows in `results.tsv`.
2. Make one focused hypothesis-driven edit in `subject/`.
3. Commit your edit.
4. Run one experiment via `loop.py --once --description "..."`.
5. If score improves, keep commit; otherwise revert.
6. Log concise rationale in description.

## Constraints

- Keep changes small and reviewable.
- Prefer simpler solutions when gains are similar.
- If run crashes, record crash and recover quickly.
- Never modify evaluation contract.
