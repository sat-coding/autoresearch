import csv
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ART = ROOT / "artifacts"
RESULTS = ROOT / "results.tsv"


def run(cmd):
    return subprocess.check_output(cmd, cwd=ROOT).decode()


def ensure_header():
    if not RESULTS.exists():
        RESULTS.write_text("timestamp\trun_id\tprimary_metric\tstatus\tdescription\n")


def best_keep():
    if not RESULTS.exists():
        return None
    rows = RESULTS.read_text().strip().splitlines()[1:]
    vals = [float(r.split("\t")[2]) for r in rows if len(r.split("\t")) >= 4 and r.split("\t")[3] == "keep"]
    return min(vals) if vals else None


def append_row(run_id, metric, status, desc):
    with RESULTS.open("a", newline="") as f:
        csv.writer(f, delimiter="\t").writerow([
            time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            run_id,
            metric,
            status,
            desc,
        ])


def run_once(desc="manual_test"):
    ensure_header()
    ART.mkdir(exist_ok=True)
    run_id = time.strftime("run-%Y%m%d-%H%M%S", time.gmtime())
    run_json = ART / f"{run_id}.run.json"
    eval_json = ART / f"{run_id}.eval.json"

    run_json.write_text(run(["python3", "runner.py"]))
    eval_json.write_text(run(["python3", "evaluator.py", str(run_json)]))

    metric = json.loads(eval_json.read_text())["primary_metric"]
    best = best_keep()
    status = "keep" if (best is None or metric < best) else "discard"
    append_row(run_id, metric, status, desc)
    return run_id, metric, status, best


if __name__ == "__main__":
    rid, metric, status, best = run_once("manual_test")
    print(json.dumps({"run_id": rid, "primary_metric": metric, "status": status, "prev_best": best}, indent=2))
