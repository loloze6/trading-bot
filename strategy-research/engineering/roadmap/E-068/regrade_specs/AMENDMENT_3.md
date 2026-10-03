# Amendment 3: narrower scope, operator rules, two candidate methods, one gate

Written and committed 2026-10-03, **before any calibration of the methods below
and before any re-grade result**. Operator decisions of 2026-10-03. This
amendment replaces the parts of amendments 1-2 that it names.

## 1. Scope

- **This slice re-grades run_065 only.**
- **run_066 moves to its own follow-up ticket under E-068.** Its pre-registered
  spec (`run_066_momentum_direction.yaml`) stays unchanged and is not graded
  here. That ticket starts from the signal mismatch found today:
  - With 500 warm-up bars, the Keltner signal recomputed on the real prices
    differs from the saved forecast by 0.007 to 0.39 (on a +-20 scale) in most
    run_066 windows.
  - The cause is the engine's own history rules: it prefetches 2 x
    `required_bars` (`core/launcher.py`) and keeps a buffer of
    `required_bars + 100` (`strategies/main_strategy.py`).
  - The tool does **not** copy those rules (operator decision).
- run_065 passes the same check: within 5e-7 on all 18 windows, which is the
  6-decimal rounding of bars.csv.

## 2. Operator rules

These carry the lesson of the deleted signal prescreen (E-039: a homemade
significance calculation killed 7 runs before their backtest and was removed
on 2026-09-12).

1. **After the backtest only.** The claim test only ever runs after a completed
   backtest, on its saved bars. It never gates, skips or kills a backtest.
2. **Information only.** `claim_status` never changes `idea_status`, never
   routes and never bans (D-055).
3. **No verdict without a passed calibration gate.** If no method passes, the
   tool reports effect sizes and "verdict: method not calibrated". There is
   never a best guess.
4. **Existing or standard methods first.** New statistics code is kept to the
   minimum.

## 3. Verdict rule (replaces amendment 1, section C)

The floor must be met at every horizon, otherwise the result is
**inconclusive**. Then:

| Status | When |
|---|---|
| **refuted** | At any horizon, the effect in the opposite direction is itself significant (`p_value_opposite < 0.05`) |
| **supported** | At every horizon the effect points the claimed way with `p < 0.05`, and the window-sign rule is met |
| **inconclusive** | Everything else, including a wrong-way wobble that is not significant |

Combining tests and variants is unchanged: refuted dominates inconclusive (D-014).

**Why:** on no-edge data, the earlier rule called run_065's claim "refuted" in
83 of 100 simulations (review finding, 2026-10-03).

## 4. Two candidate significance methods

### A. `a851a_episode_v1`: the existing A8.5.1a method, unchanged

This calls `tools/episode_significance.py::compute_a851a_significance` as it
is, the way `tools/run_protocol.py::_a851a_episode_significance` feeds it.

**Inputs, per variant:**
- All windows are pooled in window order.
- One record per bar with a defined forward return at horizon h:
  `forecast` = the saved forecast; `next_return_bps` = the h-bar forward return
  x 1e4; `active` = the test's event selector; `timestamp`; `symbol`.
- `era_of` = (symbol, era_id), as in run_protocol.
- `expected_step` = 1 day.
- Settings from `config/campaign_config.yaml: episode_significance`: gap_bars
  48, density fallback 50%, min_n_episodes 8, n_resamples 2000.
- `block_size` = `bars_per_day("1d")` = 1. Seed 20261003.

**Its statistic is not the spec's.** A8.5.1a measures the **pooled rank IC
between the forecast and the forward return among the event bars**: do
stronger breakouts give bigger follow-through? run_065's spec measures the
**mean difference against other days**.

- If A is chosen, the verdict is about that IC, and the report says so
  plainly.
- The claimed direction is IC > 0 for both sides: a more extreme breakout gives
  a larger move in the breakout's direction.
- One-sided p = `p2 / 2` if the IC points the claimed way, else `1 - p2 / 2`.
- Where the method itself returns no p (fewer than 8 episodes), the p is
  undefined.

### B. `block_permutation_v1`: the shuffle method, fixed (replaces `bootstrap_null_v1`)

Same as amendment 2 B2, with one change: **chunks are drawn without
replacement.**
- Each window's bar units are rotated by a random phase, cut into consecutive
  blocks of B bars (5 for daily; the last block may be shorter), and the blocks
  are put in random order.
- Each unit is used exactly once.
- The signal is recomputed on real warm-up rows (30 daily bars from the cache,
  read only) plus the fake window.
- N = 1,000 for the grade.

## 5. Calibration gate (replaces amendment 1 B and amendment 2 B3, daily only)

- **Signal:** the real `DonchianBreakoutComponent(period=20)`.
- **Layout:** 6 windows x 120 daily bars, plus 30 warm-up bars from the same
  simulated path.
- **Price models, both zero-mean with no edge:**
  1. iid normal log returns (sd 0.035);
  2. persistent two-state volatility: calm sd 0.02, wild sd 0.06, switching
     with probability 0.01 per bar (about 100-bar spells). This replaces the
     GARCH model.
  - In both models the intrabar high/low scale with the current bar's sd.
- **Cells:** model (2) x side (`forecast >= 12`, `forecast <= -12`) x direction
  (claimed, opposite) = 8 rows per method, with horizons 1-5.
- **Size:** 400 simulations per cell. Inside each simulation, B uses N = 199
  fakes and A uses its own 2,000 resamples.
- **Pass for a row:**
  - undefined p in no more than 5% of simulations; and
  - among defined p, the share below 0.05 within [0.025, 0.075] at every horizon.
- A method passes if all 8 rows pass.
- Undefined p are counted and reported, never hidden as "no rejection".
- Each cell runs as its own job and writes its own result file.

## 6. Choosing the method

- If A passes, use A (prefer the existing method). This holds even if B also
  passes.
- If only B passes, use B.
- If neither passes, **do not grade**. The tool ships with effect sizes and
  "verdict: method not calibrated", the PR opens, and the calibration evidence
  goes to the operator.
- In code, a verdict needs the method's calibration result file with
  `all_pass: true`. Otherwise the status is `method_not_calibrated`.

## 7. Small fixes (operator-approved)

- Undefined calibration cases are counted honestly (section 5).
- The holdout guard checks every final cache file path that is opened, not
  just the folder.
- A strategy config with settings the tool does not copy is refused.
  - Allowed: top level {regime_detector, strategies}.
  - The regime detector must have no components and no rules.
  - Exactly one non-null regime, containing only `components`.
  - Component keys only {id, class, params, weight, transforms}.
- The calibration's fake prices have longer calm and wild periods (section 5).
