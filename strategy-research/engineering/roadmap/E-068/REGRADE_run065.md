# Re-grade of run_065: not graded, no significance method passed calibration

E-068 slice 1 · CUL-386 · 2026-10-03 · branch `feat/cul-386-claim-tests`

## The answer in four lines

- **Verdict: none. Method not calibrated.** Neither candidate method passed
  the pre-registered calibration gate, so run_065 was **not graded** (operator
  rule 3: no verdict without a passed gate, and never a best guess).
- **N tests run: 0** of 2 pre-registered for run_065 (`upper_breakout`,
  `lower_breakout`). run_066's test is moved to CUL-387.
- **run_065's effect sizes were NOT computed either.** Seeing them before the
  method is chosen would contaminate the pre-registered test. The inputs are
  frozen by their sha256 below instead.
- The tool ships: `tools/claim_tests.py` (17 blocks, effect sizes, verdict only
  with a passed gate) and `tools/claim_tests_calibration.py` (the gate).

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
- The real Donchian(20) signal, on run_065's layout: 6 abutting windows x 120
  daily bars.
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
- The breakout days of 6 abutting 120-day windows merge into 3-5 episodes,
  below its own minimum of 8.
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
- Under the pre-registered rule, that is a fail. No exception was made after
  seeing it.

### The methods tried before amendment 3 (all retired)

| Method | Evidence | Result |
|---|---|---|
| Circular shift of the signal against the outcome | Probe, 100-200 sims per case: continuation claims 0.00-0.01, reversal claims 0.10-0.12; hourly rank IC 0.00 / 0.33 | Invalid: the signal is built from past prices |
| Block-adjusted analytic p (`block_analytic_v1`) | `calibration_block_analytic_v1.yaml`, 400 sims: hourly rank IC 0.000 in every cell; daily 0.005-0.090 | Failed the gate |
| Chunks drawn WITH replacement (`bootstrap_null_v1`) | Review probe: continuation 0.000-0.007 (finite-sample depletion bias) | Retired by amendment 3, before its own gate run finished |

## What the tool is now

- `run_test(windows, spec, eras, calibrated)` always reports effect sizes: per
  horizon, per window and per era, plus the sample counts.
- A verdict appears only when `calibrated=True`. The CLI sets it only from a
  calibration file with `all_pass: true` for the spec's method.
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
- **Tests:** 69 in `tests/test_e068_claim_tests.py` (targeted, run locally
  together with `test_a851a_episode_bootstrap.py` and
  `test_campaign_config_sync.py`: 85 passed; CI runs the full suite).
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

1. **Which method for run_065?** This is for the operator. Options seen today,
   none recommended over the others without new evidence:
   - (a) A8.5.1a with a daily episode gap, for example 2 days instead of 48
     bars. That changes a pre-registered project setting (CUL-265 uses 48 for
     every timeframe).
   - (b) Method B with more simulations or a re-stated gate. The 4 failures sit
     1 rejection under the floor.
   - (c) A standard method from the literature for event studies with
     overlapping returns.
2. **`block_adjusted_pvalue` and the live `residual_ic` criterion.** The
   function `signal_statistics.block_adjusted_pvalue` is what the live
   residual_ic grid criterion uses (`tools/residual_ic.py`, block = bars per
   day). The same function, fed rank IC with block = the horizon, failed our
   gate: 0.000 false-edge rate in every hourly cell (should be about 0.05),
   i.e. far too strict (`calibration_block_analytic_v1.yaml`).
   - The block size differs from residual_ic's, so this is evidence about the
     family, not a measurement of residual_ic itself.
   - The operator is opening a ticket to calibrate residual_ic.
3. **A8.5.1a on daily runs in the pipeline.** `tools/run_protocol.py` passes
   gap_bars = 48 to A8.5.1a for every timeframe. On daily runs that probably
   leaves too few episodes to give any p-value. This has not been measured on
   real runs here.
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

Each amendment was committed before any result it governs.
