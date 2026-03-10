# Generalized AutoResearch Harness

Domain-agnostic autonomous improvement loop inspired by `autoresearch`, without LLM training coupling.

## Core idea

Keep the same evolutionary loop:

1. Agent proposes a small change in `subject/`
2. Harness runs a fixed-budget experiment
3. Evaluator emits standardized score JSON
4. Loop decides keep/revert
5. Log every run to `results.tsv`

## Layout

- `program.md` — policy/instructions for the agent
- `subject/target.py` — the only mutable surface
- `runner.py` — deterministic execution wrapper (timeout/budget)
- `evaluator.py` — fixed scoring contract
- `loop.py` — keep/revert orchestration
- `results.tsv` — append-only run ledger
- `artifacts/` — per-run outputs

## Scoring contract

`evaluator.py` writes JSON with this shape:

```json
{
  "primary_metric": 0.123,
  "secondary": {
    "runtime_ms": 120,
    "complexity_penalty": 0.0
  },
  "status": "ok",
  "notes": "optional"
}
```

Lower `primary_metric` is better by default.

## Quick start

```bash
cd generalized-harness
python3 loop.py --init-baseline
python3 loop.py --once --description "example iteration"
```

## Why this structure

- Preserves autoresearch's high-velocity selection loop
- Separates mutable vs immutable surfaces clearly
- Makes it portable to any task with measurable outputs
