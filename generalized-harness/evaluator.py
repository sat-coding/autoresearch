import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def evaluate(run_artifact: dict) -> dict:
    # Fixed hidden target behavior for scoring.
    target = [1.0, 1.2, 1.8, 3.2, 4.9]
    outputs = run_artifact["outputs"]
    mse = sum((a - b) ** 2 for a, b in zip(outputs, target)) / len(target)

    complexity_penalty = 0.0
    status = "ok"

    return {
        "primary_metric": round(mse + complexity_penalty, 8),
        "secondary": {
            "mse": round(mse, 8),
            "runtime_ms": run_artifact.get("runtime_ms", 0),
            "complexity_penalty": complexity_penalty,
        },
        "status": status,
        "notes": "lower is better",
    }


if __name__ == "__main__":
    import sys

    in_path = Path(sys.argv[1])
    data = json.loads(in_path.read_text())
    print(json.dumps(evaluate(data), indent=2))
