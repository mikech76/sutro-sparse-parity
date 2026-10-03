# Benchmarks

All numbers are own runs of the official oracle
`mask_sparse_parity.evaluate_mask` (upstream commit
`aa6c51e6ad661089cbf71a39c95c577c216b627f`, `engine="vector"`) on Python 3.14.6 /
numpy 2.5.3. Machine-local, not a performance claim.

## 100 % record (bankable)

`ir/packedscan_beat382840_mask32.ir`, 58530 lines.

| suite | instances | exact 32-cell matches | recovery | cost | seconds |
|---|---|---|---|---|---|
| dev (`suite_key="mask-dev"`) run 1 | 1024 | 1024 | 1.0 | 382840 | 20.98 |
| dev run 2 | 1024 | 1024 | 1.0 | 382840 | 0.82 |
| fresh 0 (`suite_key=None`) | 2048 | 2048 | 1.0 | 382840 | 40.51 |
| fresh 1 | 2048 | 2048 | 1.0 | 382840 | 39.35 |
| fresh 2 | 2048 | 2048 | 1.0 | 382840 | 39.82 |
| fresh 3 | 2048 | 2048 | 1.0 | 382840 | 40.12 |

Totals this run: 8192/8192 exact matches on held-out suites; 8/8 fresh suites at
1.0 including earlier runs. First-run cost is the suite build (dev suite is
`lru_cache`d; repeats drop to <1 s).

Regeneration: `generate_packed_scan(5, compact_predicates=True, compact_flow=True,
walk_order_bias=1.0)` → 1.27 s, 58529 lines + trailing newline, byte-identical to
the frozen file after LF normalization.

## Baseline comparison

| artifact | cost | dev recovery |
|---|---|---|
| upstream `packedscan5_mask32.ir` | 392666 | 1.0 |
| this record | 382840 | 1.0 |
| delta | −9826 (−2.5024 %) | — |

## Other bands (HOLD — research only, not claimed)

| level | candidate cost | record cost | dev recovery | held-out | verdict |
|---|---|---|---|---|---|
| 20 % | 78607 | 86753 | 0.2139 | min 0.1553 over 4 suites, 4/4 < 0.20 | HOLD (does not generalize) |
| 40 % | 141531 | 141218 | 0.4131 | min 0.4624 ≥ 0.40 | HOLD (cost NO-GO) |
| 60 % | 149936 | 149665 | 0.6084 | min 0.6406 ≥ 0.60 | HOLD (cost NO-GO) |
| 80 % | 180760 | 182744 | 0.8262 | min 0.7715 over 20 suites, 2 < 0.80 | HOLD (held-out gate) |

Acceptance rule: bankable = held-out min ≥ target on every final suite. Dev
suite alone is not acceptance. Only 100 % passes. No claim of global optimum or
optimality is made.
