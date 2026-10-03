# Re-grade of run_065: not graded, no significance method passed calibration

E-068 slice 1 · CUL-386 · 2026-10-03 · branches `feat/cul-386-claim-tests`
(PR #315, merged) and `feat/cul-386-a851a-daily-gap` (amendment 4)

## The answer in five lines

- **Verdict: none. Method not calibrated.** Three candidate methods were
  tried, and none passed the pre-registered calibration gate. run_065 was
  **not graded** (operator rule 3: no verdict without a passed gate, and never
  a best guess). The third was the operator's one bounded try (amendment 4):
  A8.5.1a with its gap in time. **The method search is now stopped**
  (operator).
- **N tests run: 0** of 2 pre-registered for run_065 (`upper_breakout`,
  `lower_breakout`). run_066's test is moved to CUL-387.
- **run_065's effect sizes were NOT computed either.** Seeing them before the
  method is chosen would contaminate the pre-registered test. The inputs are
  frozen by their sha256 below instead.
- The tool ships: `tools/claim_tests.py` (17 blocks, effect sizes, verdict only
  with a passed gate) and `tools/claim_tests_calibration.py` (the gate).
- **One gate is needed per method x signal (with its parameters) x
  timeframe.** It is not needed per coin, because the gate uses simulated
  prices.

## Operator rules (written into the tool's docstring too)

1. The claim test only ever runs **after a completed backtest**, on its saved
   bars. It never gates, skips or kills a backtest.
2. `claim_status` is **information only**. It never changes `idea_status`,
   never routes and never bans (D-055).
3. **No verdict without a passed calibration gate.** Otherwise the tool reports
   effect sizes and "verdict: method not calibrated".
4. **Existing or standard methods first**; new statistics code is kept minimal.

These rules carry the lesson of the deleted signal prescreen (E-039): a
homemade significance calculation killed 7 runs before their backtest and was
removed on 2026-09-12.

## Scope, honestly

| | Claim card | Actually available |
|---|---|---|
| Coins | "BTC/ETH" | BTCUSD (variants `base`, `donchian_period_14_reactive`) and SOLUSD (`donchian_solusdt_crossasset`). **No ETH anywhere.** |
| Variants | | All 3 run_065 variants have results. `xrp_payment` (no `protocol_result`) is a run_066 variant: **not graded**, and out of this slice's scope. |
| Windows | | 6 per variant (2022-01 to 2023-09, about 120 daily bars each), all in one policy era (`era_2019_2023_full_feed`) |
| Data | | The saved `bars.csv` of each window, Kraken daily. No new backtest, no AI call, no new data. |

### Inputs frozen for the future grade (sha256 of each bars.csv, read only)

| Variant | Symbol | Window | run_id | sha256 |
|---|---|---|---|---|
| base | BTCUSD | 2022-01 | `20261002T164130Z_1f4decf7` | `984bbf142f5919e236541d47cea12d831ad2ee6dbfa3b1b452111eb2e4d4cfb9` |
| base | BTCUSD | 2022-05 | `20261002T164134Z_1f4decf7` | `eb12507f04f186e1d415fe63b30334a69362bd3edb09120d5e20eb16a94fca3d` |
| base | BTCUSD | 2022-09 | `20261002T164137Z_1f4decf7` | `6b5fdecdc9f5ce9fc30a9c650bbeacef3f331a54b1fb4fa8c5d7f554c797d6bd` |
| base | BTCUSD | 2023-01 | `20261002T164139Z_1f4decf7` | `6a29d1327a04986cafd8cbe62ee527e0c4da28dafc32b3de702b568fc08b0339` |
| base | BTCUSD | 2023-05 | `20261002T164142Z_1f4decf7` | `69410cbad0b7c8fec6f184d15a5a593a4798fd386cf648f0d5519f7bee1050b4` |
| base | BTCUSD | 2023-09 | `20261002T164145Z_1f4decf7` | `7ba64afbb29f3d188e97582002768dd6642cf5f26261ca976102632b3f436aa2` |
| donchian_period_14_reactive | BTCUSD | 2022-01 | `20261002T164154Z_00ab1b3a` | `b74076f81bed241113e621ed9aa02af7f5523a65146204b74e1a3caa2be0ae6a` |
| donchian_period_14_reactive | BTCUSD | 2022-05 | `20261002T164157Z_00ab1b3a` | `9f9113cf5d6d094504556d01be1b27e75576f33ba196ec4ded4324d6a59340df` |
| donchian_period_14_reactive | BTCUSD | 2022-09 | `20261002T164200Z_00ab1b3a` | `a2d7028b101546e2a20d5f059e0746fa3b14d517e2e887a7558624c4c4984c1a` |
| donchian_period_14_reactive | BTCUSD | 2023-01 | `20261002T164203Z_00ab1b3a` | `15c3bf31c92d314d11cf6f59cdbb13f51c12be0783180c0fd063823bc333ecae` |
| donchian_period_14_reactive | BTCUSD | 2023-05 | `20261002T164206Z_00ab1b3a` | `991589351deeee912eb5341c56d4e767efeeecd8c4994d9a8e49d68e71ff26ef` |
| donchian_period_14_reactive | BTCUSD | 2023-09 | `20261002T164209Z_00ab1b3a` | `20191ef23fada3b306b29cfd758a69d03c19d680eabe5c97e638f575f1184783` |
| donchian_solusdt_crossasset | SOLUSD | 2022-01 | `20261002T164218Z_1f4decf7` | `ebe872b1c32efbb74a6e585b75d1acd661a1fe312aa71fb58606b17304e2e2fb` |
| donchian_solusdt_crossasset | SOLUSD | 2022-05 | `20261002T164221Z_1f4decf7` | `cb3caefc71db479383d9ab413ce30082c0006752aa3f357633c422352b71f4bc` |
| donchian_solusdt_crossasset | SOLUSD | 2022-09 | `20261002T164223Z_1f4decf7` | `214ea557b9d12f765fa66e2e40f255c94ca324a4bec0899242377dd3eca51a20` |
| donchian_solusdt_crossasset | SOLUSD | 2023-01 | `20261002T164226Z_1f4decf7` | `8a836b48a9fbdb3e0e5ddce6db63578091df64dd3d87b9047f54f2604d4665b9` |
| donchian_solusdt_crossasset | SOLUSD | 2023-05 | `20261002T164230Z_1f4decf7` | `3470f2ab290b3a16b524bd24ee9e28ba0284d780e6ce3119ae3e3d3de94b075f` |
| donchian_solusdt_crossasset | SOLUSD | 2023-09 | `20261002T164233Z_1f4decf7` | `90212c444dc2f854d75beb7427532c25e599a48aae9b67bf6e84f455b6de456c` |

**Pre-grade check (prices and forecasts only, no outcome):** Donchian
recomputed on the real prices matches the saved forecast within 5e-7 on all
18 windows. That is the 6-decimal rounding of bars.csv.

## Calibration gate: both methods failed

**Setup** (pre-registered, amendment 3 section 5):
- Simulated prices with no edge: iid, and a "switching" model with long calm
  and wild spells.
- The real Donchian(20) signal, on run_065's layout: 6 windows x 120 daily
  bars. Their timestamps abut; each window is its own independent price path
  with its own warm-up.
- No eras are passed. All dates fall in one era, as run_065's do; the review
  checked that episode counts are identical with an era list.
- 400 simulations per cell.
- **Pass:** "no answer" in at most 5% of simulations, AND the share of
  p < 0.05 within [0.025, 0.075] at every horizon. Target 0.05.

Evidence: `engineering/roadmap/E-068/calibration/` (one file per cell plus a
summary per method).

### Method A: `a851a_episode_v1`, the existing A8.5.1a (`tools/episode_significance.py`), unchanged

| Row (model, side, direction) | Share of p < 0.05, h = 1..5 | No answer | Result |
|---|---|---|---|
| iid, upper, claimed | n/a | 100% | FAIL |
| iid, upper, opposite | n/a | 100% | FAIL |
| iid, lower, claimed | n/a | 100% | FAIL |
| iid, lower, opposite | n/a | 100% | FAIL |
| switching, upper, claimed | n/a | 100% | FAIL |
| switching, upper, opposite | n/a | 100% | FAIL |
| switching, lower, claimed | n/a | 100% | FAIL |
| switching, lower, opposite | n/a | 100% | FAIL |

**Why no answer:** its episode gap is 48 *bars*
(`config/campaign_config.yaml`, "48 bars @ 1h ~= 2 days"). On daily bars that
is 48 *days*.
- The breakout days of 6 abutting 120-day windows merge into 1-5 episodes
  (the review measured 1-4 over 40 simulations), below its own minimum of 8.
- So the method declines by its own rule. It is not broken; it does not fit
  this layout.
- It also measures a different quantity: the rank IC between forecast and
  return among the event days, not the spec's mean difference against other
  days.

### Method B: `block_permutation_v1`, chunks shuffled without replacement, signal recomputed

| Row (model, side, direction) | Share of p < 0.05 at h = 1, 2, 3, 4, 5 | No answer | Result |
|---|---|---|---|
| iid, upper, claimed | 0.025 **0.022** 0.028 0.030 0.025 | 0% | FAIL (too strict) |
| iid, upper, opposite | 0.045 0.033 0.045 0.045 0.058 | 0% | pass |
| iid, lower, claimed | 0.043 0.033 0.040 0.040 0.033 | 0% | pass |
| iid, lower, opposite | **0.022** 0.043 0.030 0.037 0.040 | 0% | FAIL (too strict) |
| switching, upper, claimed | 0.035 0.035 0.037 0.035 0.043 | 0% | pass |
| switching, upper, opposite | 0.028 **0.022** 0.028 0.028 0.035 | 0% | FAIL (too strict) |
| switching, lower, claimed | 0.052 0.050 0.045 0.050 0.055 | 0% | pass |
| switching, lower, opposite | 0.030 0.030 0.028 **0.022** 0.028 | 0% | FAIL (too strict) |

**Reading it:**
- B never flatters: the highest value is 0.058.
- It is slightly too strict in 4 rows. The lowest value is 0.022, that is 9
  rejections in 400 against a floor of 10.
- Its average across all 40 cells is 0.036, so it really is somewhat
  conservative. Suspected reason (not a bug): the order inside each 5-bar block
  is kept from the real path, so the fakes stay a little correlated with the
  real data.
- **Context for the method decision** (final review): the gate counts
  p < 0.05 with N = 199 fakes. With that N, p moves in steps of 1/200, so even
  a perfectly valid method rejects at most 9/200 = 0.045 of the time, not 0.05.
  At the grade's N = 1,000 the ceiling is 0.04995. The gate therefore measured
  B under a slightly stricter rule than the grade would apply. Under a valid
  test, the chance of 9 or fewer rejections in 400 is 0.014 at a true rate of
  0.045, against 0.004 at 0.05.
- Under the pre-registered rule, it is still a fail. No exception was made
  after seeing it; this context is for the operator's decision on the method.
- Values are the tool's 3-decimal printout; the exact shares are in the YAML
  files. 0.0375 prints as 0.037 and 0.0275 as 0.028, a floating-point rounding
  quirk.

### Amendment 4, the bounded try: `a851a_episode_timegap_v1` (A8.5.1a with gap = 2 days)

**What it was:**
- The existing A8.5.1a with only its episode gap expressed in time, as its
  pre-registration states it ("48 bars @ 1h ≈ 2 days"). On daily bars the gap
  is 2 bars instead of 48. Everything else is unchanged.
- The amendment (`regrade_specs/AMENDMENT_4.md`), the method code (`4bf18c6b`)
  and the review notes (`AMENDMENT_4_NOTES.md`) were each committed before any
  gate result.
- The gate results carry `code_sha256` `de156087…`, which was checked equal to
  the method code at `4bf18c6b`.
- The gate is unchanged, run once per signal that traded:
  - Donchian(20): variants `base` and `donchian_solusdt_crossasset`;
  - Donchian(14): variant `donchian_period_14_reactive`.

**Results** (share of p < 0.05 at h = 1..5; **bold** = outside [0.025, 0.075]):

Donchian(20), `calibration_a4/summary_timegap_p20.yaml`, **FAIL**:

| Row (model, side, direction) | h = 1, 2, 3, 4, 5 | No answer | Result |
|---|---|---|---|
| iid, lower, claimed | 0.0575 0.0475 0.0525 0.0400 0.0400 | 0% | pass |
| iid, lower, opposite | **0.0875** **0.0925** **0.0950** **0.0775** **0.1150** | 0% | FAIL |
| iid, upper, claimed | 0.0400 0.0625 0.0625 0.0325 0.0375 | 0% | pass |
| iid, upper, opposite | 0.0600 0.0475 0.0675 0.0650 0.0650 | 0% | pass |
| switching, lower, claimed | 0.0400 0.0300 **0.0225** **0.0200** 0.0250 | 0% | FAIL |
| switching, lower, opposite | **0.0800** 0.0750 0.0675 **0.1000** **0.0800** | 0% | FAIL |
| switching, upper, claimed | 0.0400 0.0400 0.0300 0.0350 0.0300 | 0% | pass |
| switching, upper, opposite | **0.0875** **0.0800** **0.0825** **0.0900** **0.1075** | 0% | FAIL |

Donchian(14), `calibration_a4/summary_timegap_p14.yaml`, **FAIL**:

| Row (model, side, direction) | h = 1, 2, 3, 4, 5 | No answer | Result |
|---|---|---|---|
| iid, lower, claimed | 0.0475 0.0325 0.0350 0.0325 0.0300 | 0% | pass |
| iid, lower, opposite | 0.0575 **0.0775** **0.0875** **0.1175** **0.1250** | 0% | FAIL |
| iid, upper, claimed | 0.0500 0.0425 0.0275 0.0350 0.0325 | 0% | pass |
| iid, upper, opposite | 0.0625 **0.0900** **0.1000** **0.0925** **0.0850** | 0% | FAIL |
| switching, lower, claimed | 0.0400 0.0450 0.0525 0.0525 0.0325 | 0% | pass |
| switching, lower, opposite | 0.0600 **0.0800** **0.0875** **0.0900** **0.0875** | 0% | FAIL |
| switching, upper, claimed | 0.0300 0.0450 0.0400 0.0400 0.0400 | 0% | pass |
| switching, upper, opposite | 0.0550 0.0650 0.0650 0.0650 0.0700 | 0% | pass |

**Reading it:**
- **The 2-day gap fixes the "no answer" problem:** 0% undefined, and roughly
  19-41 episodes per simulation (the review's small probes, not the gate run).
- **But the method flatters in the opposite direction:** up to 0.125 false
  edges against a 0.075 ceiling, in 6 of the 8 opposite-direction rows. The
  error grows with the horizon (h = 1 is mostly fine; h = 3-5 is not).
- This matches the review's warning (AMENDMENT_4_NOTES.md, point 2):
  - the forward returns (3-5 days) are longer than the 2-day gap, so
    neighbouring episodes share return days;
  - the episode bootstrap then treats them as independent and is
    overconfident;
  - suspected, not measured: a small finite-sample bias may also push the
    null IC slightly negative, which falls on the opposite side.
- One claimed-direction row is slightly too strict (Donchian(20), switching,
  lower: 0.020-0.025).
- **Decision (operator's rule): not graded, no other method tried.** The tool
  keeps reporting effect sizes only.

### The methods tried before amendment 3 (all retired)

| Method | Evidence | Result |
|---|---|---|
| Circular shift of the signal against the outcome | Probe, 100-200 sims per case: continuation claims 0.00-0.01, reversal claims 0.10-0.12; hourly rank IC 0.00 / 0.33 | Invalid: the signal is built from past prices |
| Block-adjusted analytic p (`block_analytic_v1`) | `calibration_block_analytic_v1.yaml`, 400 sims: hourly rank IC 0.000 in every cell; daily 0.005-0.090 | Failed the gate |
| Chunks drawn WITH replacement (`bootstrap_null_v1`) | Review probe: continuation 0.000-0.007 (finite-sample depletion bias) | Retired by amendment 3, before its own gate run finished |

## What the tool is now

- `run_test(windows, spec, eras, calibrated)` always reports effect sizes: per
  horizon, per window and per era, plus the sample counts.
- A verdict appears only when `calibrated=True`. The CLI sets it only when a
  calibration summary passes every check:
  - `all_pass` is true, with the exact gate and all 8 rows passing;
  - it carries a code hash;
  - its scope matches the test exactly: method, signal class and parameters,
    bar size, and statistic.
  - So a Donchian(20) daily gate does not unlock `donchian_period_14_reactive`
    (Donchian 14) or any hourly run.
  - A run with nothing graded is `not_graded`, never a verdict-shaped status.
- **Verdict rule** (amendment 3), with the floor met at every horizon:
  - **refuted** when the opposite-direction effect is itself significant;
  - **supported** when the effect is the right way with p < 0.05 at every
    horizon and the window-sign rule is met;
  - **inconclusive** otherwise.
  - On no-edge data, the earlier rule called the claim "refuted" 83 times out
    of 100.
- **No lookahead:**
  - selectors read bar t only;
  - quantile is trailing;
  - outcomes are matched by timestamp within a window;
  - the warm-up reader stops at the window start and refuses a holdout path,
    checked on the final file path.
- **Tests:** 70 in `tests/test_e068_claim_tests.py`, all passing (targeted,
  run locally; earlier also run together with `test_a851a_episode_bootstrap.py`
  and `test_campaign_config_sync.py`; CI runs the full suite).
  - Every block has a planted-effect case and a no-effect case.
  - Every selector has a lookahead test.
  - The vectorized signals equal the components' `update()`.
  - The A8.5.1a wrapper equals a direct call to the existing function.
- **Mutation checks (deliberate breakages the tests must catch):**
  - 25/25 on the pre-amendment-3 code (selectors, outcomes, verdict and the
    with-replacement fakes, some lines since rewritten);
  - 8/8 on the amendment-3 additions: chunks without replacement, the
    calibration lock, the refuted rule, not-calibrated dominating
    `combine()`, A8.5.1a's one-sided p, the holdout path guard, the strict
    config check and failed-gate files.
- **Exercised on real runs:** none of the 17 blocks yet; all are on synthetic
  data only. `EXERCISED_ON_REAL_RUNS` in the tool still lists the six blocks
  the re-grade was going to use. It becomes true only once run_065 is graded.

## Open questions

1. **Method for run_065: closed for now.** Option (a), A8.5.1a with a daily
   gap, was tried as amendment 4 and failed: it flatters at horizons longer
   than its gap. The operator stopped the method search after this bounded
   try. Not tried: (b) method B with a gate re-stated at the grade's N, and
   (c) a standard event-study method for overlapping returns.
2. **`block_adjusted_pvalue` and the live `residual_ic` criterion.** The
   function `signal_statistics.block_adjusted_pvalue` is what the live
   residual_ic grid criterion uses (`tools/residual_ic.py`, block = bars per
   day). The same function, fed rank IC with block = the horizon, failed our
   gate: 0.000 false-edge rate in every hourly cell (should be about 0.05),
   i.e. far too strict (`calibration_block_analytic_v1.yaml`).
   - The block size differs from residual_ic's, so this is evidence about the
     family, not a measurement of residual_ic itself.
   - The operator is opening a ticket to calibrate residual_ic.
3. **A8.5.1a on daily runs in the pipeline (CUL-388).**
   `tools/run_protocol.py` passes gap_bars = 48 to A8.5.1a for every
   timeframe. On run_065's daily layout that gave no p-value in 100% of
   simulations.
   - With a 2-day gap it does give answers, but it flatters at horizons longer
     than the gap (up to 0.125).
   - So A8.5.1a is not calibrated for daily data with multi-day horizons
     either way.
   - Whether the pipeline's daily runs ever use horizons longer than 1 bar has
     not been measured here.
5. **Gate cost when the claim test is wired in (slice 2-3).** The lock needs
   one passed gate per method x signal (with its parameters) x timeframe,
   about 1 hour each with A8.5.1a. It is not needed per coin, because the gate
   uses simulated prices. A coin with very different behaviour (e.g. bigger
   jumps) is not specifically tested.
   - A new timeframe also needs code support: the tool accepts daily and
     hourly bars only.
   - Possible ways to bound the cost: calibrate per signal family, or make the
     gate cheaper.
4. **run_066** (CUL-387): the Keltner signal recomputed with 500 warm-up bars
   does not match the traded one (0.007-0.39 on a ±20 scale). The engine's
   history rules were deliberately not copied into the tool.

## Commits (pre-registration order)

1. `53705062` specs pre-registered.
2. `9d0f595f` the first tool.
3. `d3bb10ea` amendment 1.
4. `36cffa31` amendment 2, with the analytic method's failed gate.
5. `1b600061` the bootstrap method.
6. `4bf8b326` amendment 3.
7. `bc4e67f4` the amendment-3 code and the gate results.

8. `f6b44bc2` amendment 4.
9. `4bf18c6b` the amendment-4 method code (before its gate).
10. `e5ab927c` its tests.
11. `1feff947` the review notes (before any gate result).
12. `5813689b` the gate results and the review fixes:
    - uncalibrated variants are not graded and mask nothing;
    - N tests run counts each graded variant;
    - the lock requires 8 distinct rows of 400 simulations.
    These were applied after the cells finished, so the code hash stays true.

Each amendment was committed before any result it governs.

**Audit-trail caveat (final review):** the amendment-3 method code and its gate
results were committed together, in `bc4e67f4`, 15 minutes after the amendment.
No commit proves the code was frozen before its results, and those result
files carry no code hash. Calibration results now record a `code_sha256` of the
two files that produce them, and a summary refuses to mix code versions.

**Also for the method decision:** the run_065 spec names no `significance`
method, so it defaults to B (N = 1,000, seed 20261003). Choosing A, or a
re-stated B, needs a written amendment naming the method before any grade.
