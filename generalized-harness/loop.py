import argparse
import csv
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ART = ROOT / "artifacts"
RESULTS = ROOT / "results.tsv"


def ensure_results_header():
    if RESULTS.exists():
        return
    RESULTS.write_text("timestamp\trun_id\tprimary_metric\tstatus\tdescription\n")


def git(cmd):
    return subprocess.check_output(["git", *cmd], cwd=ROOT.parent).decode().strip()


def run_cmd(cmd):
    return subprocess.check_output(cmd, cwd=ROOT).decode()


def run_experiment(run_id: str):
    ART.mkdir(parents=True, exist_ok=True)
    run_json = ART / f"{run_id}.run.json"
    eval_json = ART / f"{run_id}.eval.json"

    out = run_cmd(["python3", "runner.py"])
    run_json.write_text(out)

    ev = run_cmd(["python3", "evaluator.py", str(run_json)])
    eval_json.write_text(ev)
    return json.loads(ev)


def last_best_metric():
    if not RESULTS.exists():
        return None
    rows = RESULTS.read_text().strip().splitlines()[1:]
    vals = []
    for r in rows:
        cols = r.split("\t")
        if len(cols) >= 4 and cols[3] == "keep":
            vals.append(float(cols[2]))
    return min(vals) if vals else None


def append_result(run_id, metric, status, description):
    with RESULTS.open("a", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow([time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), run_id, metric, status, description])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--init-baseline", action="store_true")
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--description", default="iteration")
    args = ap.parse_args()

    ensure_results_header()

    run_id = time.strftime("run-%Y%m%d-%H%M%S", time.gmtime())
    before = git(["rev-parse", "--short", "HEAD"])
    ev = run_experiment(run_id)
    metric = ev["primary_metric"]

    best = last_best_metric()
    if args.init_baseline and best is None:
        append_result(run_id, metric, "keep", "baseline")
        print(f"Baseline set: {metric}")
        return

    keep = best is None or metric < best
    if keep:
        append_result(run_id, metric, "keep", args.description)
        print(f"KEEP {metric} (prev best={best})")
    else:
        subprocess.check_call(["git", "reset", "--hard", before], cwd=ROOT.parent)
        append_result(run_id, metric, "discard", args.description)
        print(f"DISCARD {metric} (prev best={best})")


if __name__ == "__main__":
    main()
