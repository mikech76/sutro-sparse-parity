"""Adjudication run: fresh random 2048-instance suites (suite_key=None).

Official oracle only: ``mask_sparse_parity.evaluate_mask`` from the pinned
upstream checkout. Each call with ``suite_key=None`` draws a fresh random
suite; keys are recorded as observed (no re-rolling for a nicer number).

Usage (Git Bash):
    python eval/adjudicate.py \
        --ir ir/packedscan_beat382840_mask32.ir \
        --upstream-dir /path/to/sutro-problems/sparse-parity \
        --n-fresh 4 [--json-out eval/audit_beat382840.fresh.json]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ir", required=True, type=Path)
    ap.add_argument("--upstream-dir", required=True, type=Path)
    ap.add_argument("--n-fresh", type=int, default=4)
    ap.add_argument("--json-out", type=Path, default=None)
    args = ap.parse_args()

    sys.path.insert(0, str(args.upstream_dir.resolve()))
    import mask_sparse_parity as mp  # noqa: E402

    with args.ir.open("r", encoding="utf-8", newline="") as fh:
        ir = fh.read()
    lf = ir.replace("\r\n", "\n")
    ir_sha = hashlib.sha256(lf.encode()).hexdigest()

    suites = []
    for i in range(args.n_fresh):
        t0 = time.perf_counter()
        res = mp.evaluate_mask(ir, suite_key=None)
        dt = round(time.perf_counter() - t0, 3)
        rec = {
            "index": i,
            "suite_key": None,
            "n_instances": res.n_instances,
            "successes_exact32": int(round(res.recovery * res.n_instances)),
            "denominator": res.n_instances,
            "recovery": res.recovery,
            "cost": res.cost,
            "seconds": dt,
        }
        suites.append(rec)
        print(
            f"fresh[{i}]: recovery={res.recovery!r} "
            f"({rec['successes_exact32']}/{rec['denominator']}) cost={res.cost} ({dt}s)",
            flush=True,
        )

    recs = [s["recovery"] for s in suites]
    out = {
        "ir_file": str(args.ir),
        "ir_lines": lf.count("\n"),
        "ir_sha256_lf_normalized": ir_sha,
        "suite_version": mp.SUITE_VERSION,
        "upstream_dir": str(args.upstream_dir.resolve()),
        "engine": "vector",
        "n_fresh_suites": len(suites),
        "suites": suites,
        "recovery_min": min(recs),
        "recovery_max": max(recs),
        "all_exact_1": all(r == 1.0 for r in recs),
    }
    print(json.dumps(out, indent=2))
    if args.json_out:
        args.json_out.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print("ADJUDICATE:", "OK" if out["all_exact_1"] else "MISMATCH")
    return 0 if out["all_exact_1"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
