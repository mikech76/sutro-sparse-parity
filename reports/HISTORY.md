# History

## Baseline

- 2026-09-02 — upstream record `submissions/packedscan5_mask32.ir`, cost
  **392666**, authors @jurajselep + @b0nce, produced by
  `generate_packed_scan(5)` with shipped defaults
  (`compact_predicates=False, compact_flow=False`). Checked against the pinned
  upstream commit `aa6c51e6ad661089cbf71a39c95c577c216b627f`.

## This record

- Frozen artifact: `ir/packedscan_beat382840_mask32.ir`, cost **382840**
  (58530 lines).
- Change relative to the baseline: the same `generate_packed_scan(5)` scan with
  `compact_predicates=True, compact_flow=True, walk_order_bias=1.0`.
  `walk_states` is left at the generator default (its own bounded-weight BRGC
  order), which upstream `doc/packed_scan_lower_bound.md` shows to be
  transition-optimal for this vertex set; re-ordering with 2-opt+reverse was
  measured worse (414058).
- Effect: −9826 (−2.5024 %) cost, identical 1.0 recovery. Mechanism confirmed
  by byte-identical regeneration from the upstream generator.
- Verification: dev 1024 → `cost=382840`, `recovery=1.0`; held-out fresh
  2048-suites → 4/4 × 1.0 in this run, 8/8 × 1.0 in total.

## Other bands (research only, not claimed)

- 20 % candidate 78607 vs record 86753: held-out min 0.1553 over 4 fresh suites,
  4/4 below the 0.20 target — does not generalize.
- 40 % candidate 141531 vs record 141218: cost above the record (NO-GO).
- 60 % candidate 149936 vs record 149665: cost above the record (NO-GO).
- 80 % candidate 180760 vs record 182744: dev 0.8262, but held-out min 0.7715
  over 20 fresh suites, 2 of them below 0.80 — held-out gate fails.

Acceptance rule used: a level is bankable only if held-out min ≥ target on every
final suite. Only 100 % passes.
