# sutro-sparse-parity

Personal research repo for Challenge #3 «Sparse parity on the grid»
(`cybertronai/sutro-problems`, directory `sparse-parity/`).
Instance: n=32 bits, k=5 secret positions, m=18 rows. Metric: static read
cost (`ceil(sqrt(a))` per operand read + one final read per declared output),
secret recovery rate = fraction of instances with exact 32-cell match.

No affiliation with NumFast (GPU-numerics). Solution environment is only
Python + numpy (+ pytest). No `numfast`/`wgpu` dependencies.

## Bankable result (only this)

| artifact | cost | recovery (dev 1024) | baseline | delta |
|---|---|---|---|---|
| `ir/packedscan_beat382840_mask32.ir` | **382840** | **1.0** | `packedscan5_mask32.ir` 392666 (`generate_packed_scan(5)`, @jurajselep + @b0nce, 2026-09-02) | **−9826 (−2.5024%)** |

- Dev: `suite_key="mask-dev"`, 1024 instances, `cost==382840`, `recovery==1.0`, identical across repeats (own runs, official oracle `mask_sparse_parity.evaluate_mask`, upstream commit `aa6c51e6ad661089cbf71a39c95c577c216b627f`).
- Adjudication (fresh random 2048-suites, `suite_key=None`): **8/8 × 1.0** (2048/2048 each), min 1.0. 4/4 of these were re-run in this repo and are stored as raw records in `eval/audit_beat382840.fresh.json` (8192/8192 exact matches). Fresh suites draw a hidden random key, so they are recorded as observed with no re-rolling; aggregated audit in `eval/audit_beat382840.json`.
- Mechanism (independently regenerated): upstream `generate_packed_scan(5, compact_predicates=True, compact_flow=True, walk_order_bias=1.0)` regenerates the frozen file byte-identically after LF normalization (verified with `src/generator_beat382840.py`). Defaults in the shipped generator are OFF; both records 80%/100% were submitted with defaults, i.e. with these optimizations disabled.
- Frozen IR: `ir/packedscan_beat382840_mask32.ir`, 58530 lines. SHA256 (raw file): `08757dccc081ed85fb3ada23b6fe95a10f8857335acac0c18dd131146e576280`. SHA256 (LF-normalized): `91089d94694ff71d8598d4a0333187ca01737a4e6867689c41078b145189ab86`.

## Explicitly NOT claimed (HOLD)

Only 100% is bankable. All other bands are research-only and are NOT
submitted as records here:

| level | candidate cost vs record | dev | held-out (own fresh 2048-suites) | verdict |
|---|---|---|---|---|
| 20% | 78607 vs 86753 (−9.39%) | 0.2139 | min 0.1553, 4/4 below 0.20 | HOLD (does not generalize) |
| 40% | 141531 vs 141218 (+0.22%) | 0.4131 | min 0.4624 ≥ 0.40 ok | HOLD (cost NO-GO) |
| 60% | 149936 vs 149665 (+0.18%) | 0.6084 | min 0.6406 ≥ 0.60 ok | HOLD (cost NO-GO) |
| 80% | 180760 vs 182744 (−1.09%) | 0.8262 | min 0.7715 over 20 suites, 2 below 0.80 | HOLD (held-out gate) |

Acceptance rule used: bankable = held-out min ≥ target on ALL final
suites. Dev suite alone is not acceptance. Only 100% passes.

No claim of global optimum / optimality / proof of optimality is made.
Claim is only: lowest known cost on the stated dev + adjudication suites at
the pinned upstream commit, beating the 392666 baseline under the same
scorer.

## Upstream pin

- Upstream: `https://github.com/cybertronai/sutro-problems`, commit
  `aa6c51e6ad661089cbf71a39c95c577c216b627f` (2026-10-03 checkout).
- Oracle/generator: `sparse-parity/mask_sparse_parity.py`,
  `sparse-parity/packed_sparse_parity.py` (NOT vendored here; see
  `vendor/README_vendor.md`). Scoring only on that commit.
- Env scored: Python 3.14.6, numpy 2.5.3.
- Upstream repo contains NO `LICENSE` file at the pinned commit (checked:
  root and `sparse-parity/`). Own files in this repo are MIT (see
  `LICENSE`); upstream code is NOT copied here, only referenced + attributed.

## Reproduce

Run from the repository root; `--upstream-dir` points at the `sparse-parity/`
directory of the pinned upstream checkout. Requires `numpy` (and `pytest` only
if you run the upstream tests); nothing else.

```bash
# 1. dev suite (1024 instances): prints cost/recovery, exits non-zero on mismatch
python eval/reproduce.py \
  --ir ir/packedscan_beat382840_mask32.ir \
  --upstream-dir /path/to/sutro-problems/sparse-parity \
  --repeats 2

# 2. adjudication: fresh random 2048-suites, prints successes/denominator
python eval/adjudicate.py \
  --ir ir/packedscan_beat382840_mask32.ir \
  --upstream-dir /path/to/sutro-problems/sparse-parity \
  --n-fresh 4

# 3. mechanism: regenerate the IR and compare with the frozen file
python src/generator_beat382840.py \
  --upstream-dir /path/to/sutro-problems/sparse-parity \
  --out /tmp/regen.ir \
  --compare ir/packedscan_beat382840_mask32.ir
```

## Layout

```
README.md
LICENSE                            # MIT for own files in this repo
requirements.txt / environment.yml
.python-version
ir/packedscan_beat382840_mask32.ir # frozen record, only this file counts
src/generator_beat382840.py        # regenerate byte-identical IR via upstream flags
eval/reproduce.py                  # dev 1024: cost/recovery
eval/adjudicate.py                 # fresh 2048 suite(s): successes/denominator
eval/audit_beat382840.json         # hashes, integer successes, denominators, pins
eval/audit_beat382840.fresh.json   # raw output of the last adjudication run
reports/packedscan_beat382840_mask32.md
reports/HISTORY.md
benchmarks/results.md
vendor/README_vendor.md            # upstream pin, no vendored evaluator
```
