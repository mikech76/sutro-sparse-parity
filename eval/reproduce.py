"""Reproduce the bankable record: dev-suite cost/recovery of the frozen IR.

Official oracle only: ``mask_sparse_parity.evaluate_mask`` from the pinned
upstream checkout ``cybertronai/sutro-problems``.

Usage (Git Bash):
    python eval/reproduce.py \
        --ir ir/packedscan_beat382840_mask32.ir \
        --upstream-dir /path/to/sutro-problems/sparse-parity \
        [--repeats 3]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path


def load_ir(path: Path) -> str:
    with path.open("r", newline="") as f:
        return f.read()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ir", required=True, type=Path)
    ap.add_argument(
        "--upstream-dir",
        required=True,
        type=Path,
        help=".../sutro-problems/sparse-parity (contains mask_sparse_parity.py)",
    )
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--json-out", type=Path, default=None)
    args = ap.parse_args()

    sys.path.insert(0, str(args.upstream_dir.resolve()))
    import mask_sparse_parity as mp  # noqa: E402

    ir = load_ir(args.ir)
    raw = args.ir.read_bytes()
    lf = ir.replace("\r\n", "\n")

    runs = []
    for _ in range(args.repeats):
        t0 = time.perf_counter()
        res = mp.evaluate_mask(ir, suite_key=mp.DEV_SUITE_KEY)
        runs.append(
            {
                "cost": res.cost,
                "recovery": res.recovery,
                "n_instances": res.n_instances,
                "seconds": round(time.perf_counter() - t0, 3),
            }
        )
        print(
            f"dev: cost={res.cost} recovery={res.recovery!r} "
            f"n={res.n_instances} ({runs[-1]['seconds']}s)",
            flush=True,
        )

    costs = {r["cost"] for r in runs}
    recs = {r["recovery"] for r in runs}
    summary = {
        "ir_file": str(args.ir),
        "ir_lines": lf.count("\n"),
        "sha256_raw": hashlib.sha256(raw).hexdigest(),
        "sha256_lf_normalized": hashlib.sha256(lf.encode()).hexdigest(),
        "suite_key": mp.DEV_SUITE_KEY,
        "suite_version": mp.SUITE_VERSION,
        "upstream_dir": str(args.upstream_dir.resolve()),
        "dev_runs": runs,
        "deterministic": len(costs) == 1 and len(recs) == 1,
        "cost": runs[0]["cost"],
        "recovery": runs[0]["recovery"],
        "expected_cost": 382840,
        "cost_matches_expected": runs[0]["cost"] == 382840,
        "recovery_is_1": runs[0]["recovery"] == 1.0,
    }
    print(json.dumps(summary, indent=2))
    if args.json_out:
        args.json_out.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    ok = summary["cost_matches_expected"] and summary["recovery_is_1"]
    print("REPRODUCE:", "OK" if ok else "MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
