# `packedscan_beat382840_mask32` — 100% recovery at static read cost 382840

## Task

`cybertronai/sutro-problems`, `sparse-parity/` (Challenge #3, sparse parity on
the grid). Instance: `n = 32` bits, `k = 5` secret positions, `m = 18` training
rows. Inputs: 18×32 training bits (row-major) then 18 parity bits; outputs: 32
cells, `cell c = 1` iff bit `c` is secret. Score = static read cost: every
operand read of address `a` costs `ceil(sqrt(a))`, plus one final read per
declared output cell. Recovery = fraction of instances with an exact 32-cell
match.

## Result

| artifact | cost | dev 1024 recovery | held-out |
|---|---|---|---|
| `ir/packedscan_beat382840_mask32.ir` (this record) | **382840** | **1.0** | 4/4 fresh suites × 1.0 |
| upstream `submissions/packedscan5_mask32.ir` (baseline) | 392666 | 1.0 | — |

Delta: **−9826 (−2.5024 %)**. Baseline authors @jurajselep + @b0nce,
2026-09-02, `generate_packed_scan(5)`.

IR: 58530 lines. SHA256 (raw bytes):
`08757dccc081ed85fb3ada23b6fe95a10f8857335acac0c18dd131146e576280`.
SHA256 (LF-normalized):
`91089d94694ff71d8598d4a0333187ca01737a4e6867689c41078b145189ab86`.

## Method

The record is produced by the upstream generator with the two layout-compaction
flags enabled:

```python
packed_sparse_parity.generate_packed_scan(
    5, compact_predicates=True, compact_flow=True, walk_order_bias=1.0
)
```

- `compact_flow` packs the flow so chunk addresses are allocated densely
  (`allocate(chunks-1)` and the chunk-address rows that follow it).
- `compact_predicates` packs the exact-zero/one predicate branches.

Both flags default to OFF in the shipped generator, i.e. the upstream 80 % and
100 % records were submitted without them. `weight_cap=5` covers the full
bounded-weight ball of coefficient masks, so every instance is covered by
construction rather than by search — the circuit reproduces the mask exactly iff
its coefficient mask lies in the visited set, and with cap 5 the visited set is
the whole ball. This is the reason recovery is 1.0 with no suite-dependent
dispersion, unlike the partial bands.

Regeneration is byte-identical to the frozen file after LF normalization
(`eval/reproduce.py` / `src/generator_beat382840.py` verify this).

## Verification (own runs, official oracle)

Oracle: `mask_sparse_parity.evaluate_mask`, upstream commit
`aa6c51e6ad661089cbf71a39c95c577c216b627f`, `engine="vector"`,
Python 3.14.6 / numpy 2.5.3.

- Dev suite (`suite_key="mask-dev"`, 1024 instances): `cost=382840`,
  `recovery=1.0`, identical across repeats.
- Adjudication (fresh random 2048-instance suites, `suite_key=None`):
  4/4 suites at 2048/2048 exact matches, min = max = 1.0, this run; 8/8
  including earlier runs. Fresh suites cannot be keyed, so they are recorded as
  observed with no re-rolling.

Exact numbers and hashes: `eval/audit_beat382840.json`.

## What is NOT claimed

- No claim of global optimum, optimality, or proof of optimality. The claim is
  limited to: lowest known cost on the stated suites at the pinned upstream
  commit, under the same scorer.
- The 20 / 40 / 60 / 80 % bands are **not** claimed. Their candidates do not
  pass the held-out gate (or cost more than the shipped record); see
  `benchmarks/results.md` and the README table.
