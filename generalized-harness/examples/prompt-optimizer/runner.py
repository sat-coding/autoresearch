import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "eval_set.json"
POLICY = ROOT / "subject" / "prompt_policy.py"


def load_policy():
    spec = importlib.util.spec_from_file_location("prompt_policy", POLICY)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.compose_response


def run_once():
    compose = load_policy()
    cases = json.loads(DATA.read_text())
    outputs = []
    for c in cases:
        resp = compose(c["input"])
        outputs.append({"id": c["id"], "input": c["input"], "response": resp})
    return {"outputs": outputs}


if __name__ == "__main__":
    print(json.dumps(run_once(), indent=2))
