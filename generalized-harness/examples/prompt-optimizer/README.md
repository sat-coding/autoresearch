# Prompt Optimizer Example

A concrete, CPU-safe demo for the generalized harness.

## What is optimized?

- Mutable file: `subject/prompt_policy.py`
- Goal: improve response quality over fixed eval cases.

## How scoring works

`evaluator.py` checks each response against:
- required keywords (coverage)
- forbidden words (penalty)
- max length (penalty)

Final metric:
- `primary_metric = 1 - avg_case_score`
- **lower is better**

## Run a test

```bash
cd generalized-harness/examples/prompt-optimizer
python3 loop.py
cat results.tsv
```

Artifacts are written under `artifacts/`.
