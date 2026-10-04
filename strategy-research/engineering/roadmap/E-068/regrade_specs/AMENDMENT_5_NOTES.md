# Amendment 5: review notes (committed before the re-evaluated summary and before any grade)

Opus adversarial review of `AMENDMENT_5.md` (`f7a3b3ae`) and its code
(`073bdd4c`), 2026-10-03. **No blockers.** Verified true by the reviewer:
method B's code path and its period-20 seeds are unchanged since `bc4e67f4`;
N = 199 vs 1,000 figures; B was calibrated on Donchian(20) only; the B cells
carry no code hash; `variant_signal` on run_065 returns exactly
`donchian(20)` for `base` and `donchian_solusdt_crossasset` and period 14 for
`donchian_period_14_reactive`; B's range 0.0225-0.0575; the rule change is
disclosed as decided after the gate numbers; no code reads `claim_status` or
`calibration_status` outside the claim tool (information only).

## Fixed in code (this commit)

1. **A gate row could pass on fewer horizons.** `judge_calibration_row` now
   requires exactly horizons 1-5 (`CALIBRATION_HORIZONS`), and
   `calibration_for` refuses a spec whose horizons go beyond the gate's.
2. **Re-evaluation provenance was recorded, not checked.** `reevaluate` (CLI)
   now reads each cell from git at `--code-ref` and refuses if the working
   file differs (line endings aside); it refuses pre-hash cells that name a
   signal other than Donchian(20).
3. **Hashes depended on the checkout's line endings.** Cell hashes are now of
   git's stored bytes, as the code hash already was (`code_sha256_at`, the
   same form as amendment 4's stored hash). Recorded as
   `cell_files_sha256_source`.
4. **Two passed summaries for one scope** would let the order of
   `--calibration` pick the "conservative" label. Now refused.
5. Tests added: partial-horizon row, duplicate scope, horizons beyond the
   gate, non-Donchian(20) pre-hash cell, and the `reevaluate` CLI on the real
   committed cells at `bc4e67f4` (skipped where git history is absent, e.g. a
   shallow CI clone). 83 tests pass.

## Corrections to the amendment's wording (the amendment file is not edited)

- **Section 4, "changed only in the A8.5.1a family, the lock and the CLI"** is
  incomplete. Also changed since `bc4e67f4`: `combine([])` now returns
  `not_graded`, and `grade_claim_file` gained amendment 4's per-variant "not
  graded" aggregation; the calibration script's `METHODS` gained the timegap
  method (appended, so B's seed index is unchanged) and reads its gate
  constants from `claim_tests`. None of these touches B's fakes, statistic or
  p-value.
- **Section 3, "the other methods are not rescued"** also covers the retired
  analytic method `block_analytic_v1` (`calibration_block_analytic_v1.yaml`,
  up to 0.09 > 0.075).
- **Section 6, "a supported is not weakened"** rests on B being close to
  exactly valid at N = 1,000: the worst B value, 0.0575, plus the at most
  ~0.005 difference between N = 199 and N = 1,000 stays under 0.075. Block
  permutation is only approximately valid; the gate is the evidence for it.

## Not changed

- The gate's measurement, the spec, the verdict rule, the scope lock.
- `code_sha256()` for future cells still hashes working-tree bytes (a cell run
  on a CRLF checkout records a hash not reproducible from git). It does not
  affect this slice (no cell is run); noted for slice 2.
