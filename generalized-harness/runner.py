import importlib.util
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET_FILE = ROOT / "subject" / "target.py"


def load_candidate():
    spec = importlib.util.spec_from_file_location("target", TARGET_FILE)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.candidate_solution


def run_once():
    t0 = time.time()
    fn = load_candidate()
    xs = [0.0, 0.5, 1.0, 2.0, 3.0]
    outputs = [float(fn(x)) for x in xs]
    runtime_ms = int((time.time() - t0) * 1000)
    return {"xs": xs, "outputs": outputs, "runtime_ms": runtime_ms}


if __name__ == "__main__":
    print(json.dumps(run_once(), indent=2))
