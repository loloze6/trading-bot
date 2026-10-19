# Fold-confirm floors and the past_return direction bias: measurement report

Date: 2026-10-19. Asked by: operator ruling Q2 (2026-10-19), lane 2.
Base: origin/master 84173698. Status: a measurement report for the operator to rule on.

- No code change: nothing in `tools/` or `workflow/` is touched. `fold_confirm` stays as it is until the operator rules on this report.
- No record changed: `campaign_record/confirmations.yaml` and every run folder were only read, through copies in a scratch folder.
- No backtest was run. No market data was read: the simulator uses synthetic prices only, and the re-grade reads only the three child runs' saved outputs.
- D-090 stands. D-090 is the operator's rule that a claim measured on several folds is `confirmed` if any fold confirmed it. This report does not propose changing it.
- Every rate below gives its simulation count and a binomial standard error (SE). A statement I did not measure is labelled **hypothesis**.

## 0. Summary

**(i) Cause of the bias (measured).** On a pure random walk, a `past_return` reversal claim is confirmed about 5 times as often as the matching momentum claim:

- `less` after a rise: 0.230 (SE 0.009).
- `greater` after a rise: 0.041 (SE 0.004).
- Symmetric chance: about 0.11.

The cause is coupling between bars inside one window. A selected bar's own forward move, over bars t+1..t+h, is also part of the `past_return` of the bars that follow it. So a selected bar that is followed by a rise pulls more bars into the selection after it, and one followed by a fall ends its cluster early.

- The sum of the selected bars' forward moves is unbiased: 0.0018, SE 0.0046.
- Their mean is biased low, because the count it divides by grows with that sum: −0.00315, SE 0.00016, about 20 SE below zero. The correlation between the sum and the count is +0.61.
- A biased-low selected mean favours `less` after a rise. By the same mechanism it favours `greater` after a fall: 0.217 (SE 0.009) against 0.050 (SE 0.005).

The decisive control keeps the same paths and the same arithmetic return but removes the overlap: only bars spaced bars + h = 8 apart may be candidates. With that control:

- the per-window share with the claimed sign falls from 0.596 to 0.504 (SE 0.005);
- the sum-to-count correlation falls to 0.004.

Arithmetic versus log returns is not the cause: the log outcome gives 0.593 instead of 0.596. The hit rate statistic, the quantile cut-off and every horizon tested (1, 3, 6) all carry the bias. It grows with h and shrinks as the windows get longer.

**(ii) Re-grade of the three recorded confirmations: none changes under the claims' own floors.** All three claims carry the floor `min_events: 100, min_windows: 4`. `claim_measure` checks this floor on the fold's pooled counts at each horizon, and all three clear it with room:

| claim | events | windows with events |
|---|---|---|
| forecast_power-run_095-1 | 330 | 6 |
| trade_efficiency-run_066-2 | 2182 to 2195 | 6 |
| trade_efficiency-run_071-4 | 3361 | 6 |

The floor-applied verdict is `confirmed` for all three, the same as recorded.

- If `min_events` were read literally per window, forecast_power-run_095-1 (run_096) would fail. Each of its 6 windows has only 52 to 59 short lots, below 100.
- Under an "every window holds" rule, all three would fail: each has exactly one window against.

**(iii) Recommended floor rule: R5 (measured).** R5 has two parts:

1. The claim's own floor, applied as `claim_measure` applies it (pooled, at every horizon). If it is not met, the test is `not_measurable`, never `confirmed`.
2. The all-but-one count is taken over the fold's windows. A window with no value counts against.

Measured false-confirm rates under R5 (2000 sims per cell):

| null case | current rule | R5 |
|---|---|---|
| Symmetric null, 6 full windows | 0.115 to 0.117 | 0.115 to 0.117 (unchanged) |
| Thin selectors | 0.099 to 0.117 | 0.057 to 0.102 |
| Fold with 2 of its 6 windows empty | 0.272 to 0.292 | 0.000 |
| Fold with 1 of its 6 windows empty | 0.187 to 0.198 | 0.025 to 0.039 |

R5 has no power cost when the floor is met. The three recorded confirmations stay confirmed under R5.

No floor rule removes the direction bias of (i): under R5, a reversal claim on the random walk is still confirmed 0.230 of the time. That is a separate defect in how the measurement is taken, listed in section 5 for the operator.

## 1. The code (read before simulating; line numbers re-verified on 84173698)

**`tools/claim_tests.py`:**

- `past_return` (470-481) is `close[t]/close[t-n] - 1`, which reads rows t-n..t.
- `sel_event` (523-528) and `sel_quantile` (565-580): the quantile cut-off is taken over the trailing `lookback` bars t-L..t-1.
- `out_fwd_return` (599-604) is `close[t+h]/close[t] - 1`, which is arithmetic. It reads rows t..t+h of the same window.
- `base_complement` (666-667) is every valid, unselected bar of the window.
- `st_mean_diff` (728-733) is the mean of the selected bars minus the weighted mean of the baseline. It is oriented by direction.
- `st_hit_rate` (736-743).
- `_prepare` (1562-1576).
- `effect_sizes` computes the pooled value (1702-1703), the event count (1704, 1722) and the per-window values (1707-1710).
- The trade family: `trade_outcome` (1275-1291) and `trade_effect_sizes` (1432-1509).

**`tools/claim_measure.py`:**

- The floor is checked in `measure_test` at 213-216 against the POOLED horizon counts (`_FLOOR_KEY`, 74-75): `n_events`, `n_windows_with_events`, `n_blocks`, `n_eras_with_events`.
- A floor that is not met is only listed in `floor_not_met`; the status stays `measured` (217-220).

**`tools/fold_confirm.py`:**

- `MIN_WINDOWS = 4` (109) and `WINDOWS_ALLOWED_AGAINST = 1` (110).
- `grade_test` (131-190):
  - k and n are counted among the windows WITH a value (159-160);
  - the rule is `n >= 4 and k >= n - 1`, plus a positive pooled value (165-166);
  - horizons with at least 4 windows are judged first (173-179);
  - fewer than 4 windows gives `not_measurable` (180-185).
- `grade_test` never reads `floor` or `floor_not_met`: the word "floor" does not occur in fold_confirm.py.

Line drift against the specification (which cited c51026fb): the three files are byte-identical between c51026fb and 84173698. The specification's ":111" for `MIN_WINDOWS` is 109, and `grade_test` ends at 190, not 201. The claim_measure citation 211-221 contains the floor loop at 213-216.

## 2. (i) The past_return direction bias

### 2.1 Setup

Script: `fold_floor_sim.py` in this folder. The setup:

- **Paths:** 6 windows of 120 daily bars. Each window is its own iid Gaussian log-return walk with sd 0.035 per bar and zero drift, so there is no edge anywhere. The layout follows `claim_tests_calibration.simulate_windows`.
- **Blocks:** the selector, outcome, baseline and statistic are the UNCHANGED blocks of `claim_tests`.
- **Grading:** the noise rule is the UNCHANGED `fold_confirm.grade_test`.
- **Cross-check:** for the first 50 sims of every plain cell, the script also runs the full chain (`claim_measure.measure_test` and then `grade_test`) and asserts that every per-window value, the pooled value, `n_events` and the status are identical. No difference was found.
- **Pairing:** the two directions of one selector run on the same paths. Their per-window shares therefore add up to 1.
- **Counts:** 2000 sims per cell. That is 12000 window values for the per-window share; the fold confirm rate is out of 2000.

Base cell A:

- selector: `past_return`, bars 5, `>= +0.05` (absolute cut-off);
- outcome: `fwd_return` at h = 3;
- statistic: `mean_diff` against the complement;
- about 30 selected bars per window.

### 2.2 Reproduction

| cell | direction | per-window share with the claimed sign (SE) | fold confirmed, current rule R0 (SE) |
|---|---|---|---|
| A: past_return(5) >= +5% (rise, absolute) | less (reversal) | 0.596 (0.004) | **0.230 (0.009)** |
| | greater (momentum) | 0.404 (0.004) | **0.041 (0.004)** |
| quantile: past_return(5) in the top 20% of the last 20 bars | less | 0.525 (0.005) | 0.135 (0.008) |
| | greater | 0.475 (0.005) | 0.079 (0.006) |
| past_return(5) <= −5% (fall) | less (momentum) | 0.406 (0.004) | 0.050 (0.005) |
| | greater (reversal) | 0.594 (0.004) | **0.217 (0.009)** |
| trailing_vol(10) >= 0.035 | less | 0.508 (0.005) | 0.114 (0.007) |
| | greater | 0.491 (0.005) | 0.107 (0.007) |

This reproduces the PR-A2 review's asymmetry, which was 0.27 against 0.035 with its own cut-offs. `trailing_vol` is symmetric, at the documented chance of about 0.11. Two points the review had not seen:

- The bias favours **reversal in both directions**: `less` after a rise, and `greater` after a fall.
- For the quantile cut-off the per-window share leans the same way, 0.525, but the pooled sign leans slightly the other way: 0.486 positive for `less`. The fold rate still favours `less`: 0.135 against 0.079.

### 2.3 Controlled variants (one change each, on cell A; `less` / `greater`)

| change | per-window share, less (SE) | R0 less / greater (SE about 0.007-0.009 / 0.004-0.007) | removes the asymmetry? |
|---|---|---|---|
| none (cell A) | 0.596 (0.004) | 0.230 / 0.041 | |
| outcome from an INDEPENDENT second path (selection and outcome share nothing) | 0.498 (0.005) | 0.117 / 0.115 | **yes** |
| log outcome instead of arithmetic | 0.593 (0.004) | 0.215 / 0.045 | no: arithmetic is not the cause |
| candidates only every 8 bars (= bars + h: no outcome window overlaps another candidate's selector window), 120 bars | 0.502 (0.005) | 0.103 / 0.099 | **yes** (3.7 events per window) |
| same stride 8, 960-bar windows (31.7 events per window, the same count as cell A) | 0.504 (0.005) | 0.108 / 0.103 | **yes** |
| candidates every 4 bars (partial overlap) | 0.550 (0.004) | 0.164 / 0.065 | halved |
| selected mean against the exact expected outcome (no complement) | 0.561 (0.004) | 0.172 / 0.065 | no: the selected side carries most of it |
| exact expected outcome against the complement mean (no selected side) | 0.512 (0.005) | 0.121 / 0.089 | mostly: the complement carries a small part |
| hit_rate instead of mean_diff | 0.578 (0.004) | 0.181 / 0.039 | no |
| h = 1 | 0.561 (0.004) | 0.167 / 0.059 | no (smaller) |
| h = 6 | 0.622 (0.004) | 0.245 / 0.029 | no (larger) |
| past_return over 1 bar, >= +3% | 0.560 (0.004) | 0.174 / 0.062 | no |
| 480-bar windows (126 events per window) | 0.542 (0.004) | 0.153 / 0.075 | no (smaller) |
| sparse cut-off, >= +12% (8 events per window) | 0.610 (0.004) | 0.244 / 0.043 | no (larger) |
| 3 horizons 1, 3, 6 at once (all must hold) | 0.597 (0.003) | 0.068 / 0.007 | no |
| 4 windows per fold | 0.607 (0.005) | 0.411 / 0.162 | no; the 4-window rule is loose (section 4) |
| 8 windows per fold | 0.599 (0.004) | 0.106 / 0.010 | no |

### 2.4 The mechanism, and the decisive measurement

Per window, call S the sum of the selected bars' log forward returns over h = 3 bars, and N their count. These come from `mechanism` in the script: 2000 sims, 12000 windows, cell A.

| quantity | tool (every bar a candidate) | stride 8 (no overlap) |
|---|---|---|
| mean of S (the sum) | +0.0018 (SE 0.0046), zero | +0.0017 (SE 0.0011), zero |
| mean of S/N (what the rule reads) | **−0.00315 (SE 0.00016)** | +0.00055 (SE 0.00032), zero |
| share of windows with S/N < 0 (SE) | 0.550 (0.005) | 0.494 (0.005) |
| correlation of S and N | **+0.61** | +0.004 |
| selected bars among the next 8, after a selected bar whose own outcome rose | **4.36** | 0.25 |
| the same, after one whose own outcome fell | **1.77** | 0.25 |

The SE of the last two rows assumes independent events, which they are not. The gap between the rows is far larger than any plausible SE.

In plain words:

1. Each bar's forward move is independent of its OWN selection, because the selector reads only the past. So the sum over the selected bars is unbiased.
2. The same forward move (bars t+1..t+h) is part of the `past_return` of the next bars. After a selected bar whose move rises, the rise keeps `past_return` above the cut-off, and on average 4.4 of the next 8 bars are selected. After one whose move falls, only 1.8 are.
3. So the windows where the selected bars did well have more selected bars, each new one with a fresh, zero-mean move. The good move is divided by a larger count, and the bad move by a smaller one.
4. The selected-bar mean is therefore pulled below zero even though the sum is not. The complement is pulled the other way, less strongly, because it holds about 90 bars against 30.
5. Pull the selected mean down and push the complement mean up, and `mean_diff` leans negative. That is the claimed sign of `less` after a rise, and of `greater` after a fall: a **reversal** is confirmed by chance far more often than a momentum claim.
6. `trailing_vol` is symmetric because a forward move of either sign raises later volatility. Cluster length then depends on the size of the move, not its sign.

The decisive measurement is the stride control. It uses the same paths, the same arithmetic `fwd_return`, the same complement and the same rule, and changes only one thing: no outcome window may overlap another candidate's selector window. With that change, the share returns to 0.504 (SE 0.005) at the same 32 events per window, and the correlation of S and N goes to zero.

Why the 6-window rule amplifies the bias: the rule needs at least 5 of 6 windows with the claimed sign. A per-window share of 0.60 instead of 0.50 raises that chance from 7/64 = 0.11 to 6·0.6⁵·0.4 + 0.6⁶ = 0.23. That is what the simulation shows: 0.230.

**Hypothesis, not measured:** the same coupling may exist in the trade-level tests that the three recorded confirmations use.

- A lot's `trade_net_return` spans its own life, during which the same prices decide other lots' entries.
- A flip exit's `post_exit_return` overlaps the next lots' entries and exits.

Its direction and size there are unknown. Measuring them needs a trade-level null simulator, which this report does not build.

## 3. (ii) Re-grade of the three recorded confirmations

### 3.1 Source and method

**Source.** `campaign_record/confirmations.yaml` (`fold_confirmations`, status `confirmed`). Each row is the copy of its child run's `artifacts/fold_confirmation.yaml`. Its inputs are the vehicle variant `base` of that child run:

- `artifacts/variants/base/protocol_result.yaml`;
- `variants/base/results/<rid>/bars.csv` and `trades.json`;
- `variants/base/trade_diagnostics.json`.

All of these were copied read-only to a scratch folder. The claim and its floor come from the child's `artifacts/hypothesis_card.yaml`. Its test `spec_hash` equals the source claim's: this is the rule `confirm_on_fold` enforces, and the record lists the same hash.

**Method (`regrade.py`).**

1. Re-measure each test with the unchanged `claim_measure.measure_test`, trade family on, on the fold's windows.
2. **Assert** that every per-window value, the pooled value, `n_events` and the status equal the recorded row. All three matched to 1e-12.
3. Add what the record does not carry: the per-window count of selected lots with an outcome, and of baseline lots (`other_trades`) with an outcome.
4. Apply the claim's floor and the candidate rules.

No backtest was run. Only the strategy's saved trades and bars were read.

### 3.2 Results

Every row has the floor `min_events: 100, min_windows: 4`. `claim_measure`'s own `floor_not_met` is `[]` for all three.

**forecast_power-run_095-1, child run_096, fold C.** Test `shorts_earn_less_than_other_lots`: `mean_diff` of `trade_net_return`, direction `less`. Horizon 0, pooled oriented +0.0210, 330 events, 196 non-overlapping stretches.

| window | selected (short lots) | baseline | claimed sign |
|---|---|---|---|
| 2018-01 | 53 | 46 | yes |
| 2018-09 | 52 | 52 | **no** |
| 2019-05 | 55 | 37 | yes |
| 2020-01 | 58 | 47 | yes |
| 2020-09 | 59 | 40 | yes |
| 2021-05 | 53 | 48 | yes |

**trade_efficiency-run_066-2, child run_079, fold B.** Test `flip_closed_lots_continue`: `hit_rate` of `post_exit_return` at h 1, 6 and 24, direction `greater`. Pooled oriented: +0.0419 at h1, +0.0478 at h6, +0.0808 at h24. Events: 2195, 2194 and 2182. Stretches (`n_blocks`): 2195, 363 and 87.

| window | selected / baseline at h1 | h1 sign | h6 sign | h24 sign |
|---|---|---|---|---|
| 2018-05 | 321 / 695 | yes | yes | yes |
| 2019-01 | 363 / 713 | yes | yes | yes |
| 2019-09 | 365 / 717 | yes | yes | yes |
| 2020-05 | 380 / 744 | yes | yes | yes |
| 2021-01 | 380 / 756 | **no** | yes | yes |
| 2021-09 | 386 / 767 | yes | yes | yes |

The counts at h6 and h24 differ by at most 3 lots per window. They are in `results/regrade.yaml`.

**trade_efficiency-run_071-4, child run_078, fold B.** Test `strong_long_entries_earn_more`: `mean_diff` of `trade_net_return`, direction `greater`. Horizon 0, pooled oriented +0.00150, 3361 events, 1297 stretches.

| window | selected | baseline | claimed sign |
|---|---|---|---|
| 2018-05 | 502 | 1934 | **no** |
| 2019-01 | 556 | 1813 | yes |
| 2019-09 | 437 | 2002 | yes |
| 2020-05 | 606 | 1833 | yes |
| 2021-01 | 663 | 1729 | yes |
| 2021-09 | 597 | 1886 | yes |

### 3.3 Verdicts

| claim | original | floor applied as claim_measure reads it (pooled) = R1 | R5 (recommended) | min_events per window (literal, 100) | m = ceil(100/6) = 17 per window, below counts against | every window holds (R4) |
|---|---|---|---|---|---|---|
| forecast_power-run_095-1 | confirmed | **confirmed** | confirmed | not confirmed (all 6 windows have 52-59 < 100) | confirmed | not confirmed (2018-09 against) |
| trade_efficiency-run_066-2 | confirmed | **confirmed** | confirmed | confirmed | confirmed | not confirmed (2021-01 against at h1) |
| trade_efficiency-run_071-4 | confirmed | **confirmed** | confirmed | confirmed | confirmed | not confirmed (2018-05 against) |

**Floor-applied verdict: unchanged for all three.** The floor as the claims state it is met. Each claim's `pass_if` reads it as a fold total, for example "with at least 100 short lots". So is `claim_measure`. Only an invented per-window reading of `min_events: 100` would change one verdict (run_096).

**Information, not a floor of these claims:** each claim counts LOTS, which overlap. The non-overlapping stretches are fewer: run_096 has 196, run_078 has 1297, and run_079 has 87 at h24. None of the three claims sets `min_blocks`.

## 4. (iii) Floor rules for fold_confirm, measured

### 4.1 Candidate rules

All are evaluated on the same simulated folds as section 2, 2000 sims per cell, with the claim floor `min_events 100, min_windows 4`.

- **R0 (current).** `grade_test` as it is.
- **R1.** R0, plus the claim's floor at every horizon, read as `claim_measure` reads it (pooled counts). If the floor is not met: `not_measurable`.
- **R5.** R1, plus the count runs over the fold's windows: a window without a value counts against. The rule becomes "at most 1 of the fold's 6 windows against, whether by the wrong sign or by no value", instead of "at most 1 against among the windows with a value, at least 4 of them".
- **R2(m).** R5, plus a window with fewer than m selected or m baseline events counts against. Measured at m = 10 and m = 17 (= ceil(min_events / 6)).
- **R3(m = 17).** As R2, but a window below m is DROPPED and the all-but-one rule runs on the remaining windows (at least 4).
- **R4.** Every window with a value has the claimed sign, with at least 4 windows. No floor.

### 4.2 False-confirm rate (a confirmed claim on a walk with no edge)

The SE is about 0.007 at 0.11 and about 0.003 at 0.02.

| null case | R0 | R1 | **R5** | R2 m10 | R2 m17 | R3 m17 | R4 |
|---|---|---|---|---|---|---|---|
| symmetric (independent outcome), 30 events per window, less / greater | 0.117 / 0.115 | 0.117 / 0.115 | **0.117 / 0.115** | 0.117 / 0.111 | 0.096 / 0.092 | 0.141 / 0.139 | 0.015 / 0.015 |
| symmetric, thin (20 events per window, about 115 per fold) | 0.117 / 0.099 | 0.102 / 0.089 | **0.102 / 0.089** | 0.080 / 0.073 | 0.022 / 0.015 | 0.140 / 0.134 | 0.019 / 0.021 |
| trailing_vol, thin (18 events per window) | 0.114 / 0.109 | 0.066 / 0.065 | **0.060 / 0.057** | 0.028 / 0.024 | 0.003 / 0.004 | 0.082 / 0.082 | 0.015 / 0.015 |
| symmetric, 2 of 6 windows with no value | 0.292 / 0.272 | 0.254 / 0.237 | **0.000 / 0.000** | 0.000 / 0.000 | 0.000 / 0.000 | 0.220 / 0.197 | 0.059 / 0.059 |
| symmetric, 1 of 6 windows with no value | 0.198 / 0.187 | 0.197 / 0.186 | **0.039 / 0.025** | 0.038 / 0.025 | 0.034 / 0.019 | 0.209 / 0.200 | 0.039 / 0.025 |
| sparse, 8 events per window (about 50 per fold) | 0.244 / 0.043 | 0.000 / 0.000 | **0.000 / 0.000** | 0 / 0 | 0 / 0 | 0 / 0 | 0.051 / 0.004 |
| past_return reversal bias (cell A), less / greater | 0.230 / 0.041 | 0.230 / 0.041 | **0.230 / 0.041** | 0.226 / 0.040 | 0.172 / 0.036 | 0.241 / 0.064 | 0.048 / 0.002 |
| past_return bias, thin, less / greater | 0.213 / 0.043 | 0.184 / 0.040 | **0.184 / 0.040** | 0.142 / 0.032 | 0.024 / 0.009 | 0.187 / 0.097 | 0.048 / 0.005 |

### 4.3 Power (the confirm rate when a real effect is added to the selected bars)

The added effect is +δ in the claimed direction, on top of an independent outcome. The SE is about 0.011.

| real effect | R0 | **R5** | R2 m10 | R2 m17 | R3 m17 | R4 |
|---|---|---|---|---|---|---|
| δ = 1%, 30 events per window | 0.436 | **0.436** | 0.429 | 0.359 | 0.478 | 0.132 |
| δ = 1%, 20 events per window | 0.393 | **0.348** | 0.285 | 0.071 | 0.354 | 0.104 |
| δ = 2%, 30 events per window | 0.798 | **0.798** | 0.790 | 0.696 | 0.827 | 0.389 |
| δ = 2%, 20 events per window | 0.707 | **0.617** | 0.527 | 0.172 | 0.551 | 0.310 |

The table shows the `less` cell. The `greater` cell agrees within 0.02 in every column: see `results/sim.yaml`.

### 4.4 Reading of the tables

- **Dropping windows below a floor makes the rule looser, not stricter.** R3 is above R0 in every symmetric case, for example 0.141 against 0.117. Fewer windows means 3 of 4 or 4 of 5 is enough, and those happen by chance 31% and 19% of the time. Any floor that removes windows must count them **against**.
- **The current rule's real weak spot is windows without a value, not too few events.** With 1 or 2 of the 6 windows empty (a coin or a period with almost no data), R0 confirms a pure null 0.19 to 0.29 of the time. R5 takes this to 0.03 to 0.04 and 0.000, and costs nothing when all 6 windows have a value.
- **The pooled floor (R1) costs power only when a fold falls short of `min_events`.** On thin selectors it cuts both false confirms (0.114 to 0.066 on trailing_vol) and power (0.707 to 0.617 at δ = 2%, 20 events per window).
- **A per-window floor of min_events / 6 (R2 m17) cuts power hard on thin selectors** (0.707 to 0.172). It also gives a meaning to `min_events` that the claim cards do not give it: they read it as a fold total.
- **R4 (every window) brings the symmetric null to about 0.015 to 0.02 and the biased reversal to 0.048.** It halves power (0.80 to 0.39-0.41 at δ = 2%). It would also turn all three recorded confirmations to not confirmed.
- **No floor rule fixes the direction bias of (i).** Under R5 the reversal null still passes 0.230 against 0.041 for momentum. Only R2 m17 and R4 lower it, and only by lowering everything.

## 5. Recommendation

**Recommended: R5.** It changes `fold_confirm.grade_test` in two ways:

1. It reads the claim's own floor as `claim_measure` computes it, pooled per horizon over the fold's windows (for several coins, over the coins pooled per window, D-089). D-089 is the operator's 2026-10-08 decision to pool several coins into one value per window before the noise rule. A test whose floor is not met at any horizon is `not_measurable` with the reason "floor not met", never `confirmed`.
2. It counts "all but one" over the fold's windows (`fold_blocks`). A window without a value counts against, so at most one of the 6 windows may be against, by the wrong sign or by no value. `MIN_WINDOWS` then has no separate role on a 6-block fold.

Its measured false-confirm rates, from section 4.2:

| case | R5 | R0 |
|---|---|---|
| symmetric null, full windows | 0.115-0.117 | 0.115-0.117 |
| thin selectors | 0.057-0.102 | 0.099-0.117 |
| 1 empty window | 0.025-0.039 | 0.19-0.20 |
| 2 empty windows | 0.000 | 0.27-0.29 |

Its power cost is zero when the floor is met, and about 0.09 at δ = 2% when a fold has about 115 events against a floor of 100. The three recorded confirmations are unchanged.

**Alternative: R5 plus "every window" (R4-style), for the operator to weigh.** The false-confirm rate falls to about 0.015-0.02 on a symmetric null and 0.048 on the reversal bias. Power is halved, and all three recorded confirmations become not confirmed. This report does not recommend it, because its power cost lands on real effects as much as on noise.

**Separately, for the operator: the direction bias of (i) is not a floor problem.** Two remedies were measured here as controls, not proposed as code:

- Space candidate events at least bars + h apart. This removed the bias: 0.504 (SE 0.005) at the same event count. The cost is about 1/(bars + h) of the events.
- Grade against a selector-specific simulated null, not the fixed 11%. This was not built here.

**Hypothesis:** the bias may also affect the trade-level families that all three recorded confirmations use. That needs its own simulator.

**No code change is made before the operator's ruling.** D-090 stands: a claim confirmed on any fold stays confirmed. This report adds no DECISION_LOG row.

## 6. Limits

- The null is an iid Gaussian walk on daily bars. Real prices have fat tails and volatility clusters. The asymmetry's size will differ on them; its sign follows from the mechanism. **Hypothesis**: not measured on another model.
- All rule rates are per test, at one horizon unless stated. With 3 horizons that must all hold, R0 falls to 0.068 / 0.007 (cell A).
- The trade-level families (`trade_net_return`, `post_exit_return`) were not simulated (section 2.4).
- The per-window counts in section 3 are recomputed from the saved trades with the unchanged tool functions. They are not stored in the record, and the recomputation reproduces every recorded value exactly.

## 7. Reproduce

Shell: Git Bash on Windows. Interpreter: `C:\Users\alauz\venvs\trading-bot\Scripts\python.exe`. Run from the worktree root. Synthetic data only, except `regrade.py`, which needs the scratch copies described in its docstring. Wall-clock times are from this machine, each run holding the shared test lock.

```
# (i) and (iii): every cell, 2000 sims; the first 50 sims of each plain cell are cross-checked against the full tool chain. Run time 321 s.
python strategy-research/engineering/FOLD-FLOORS-2026-10-19/fold_floor_sim.py --sims 2000 --check 50 --out <scratch>/sim.yaml

# (i) mechanism (S, N, S/N, cluster continuation). About 3 s.
python strategy-research/engineering/FOLD-FLOORS-2026-10-19/fold_floor_sim.py --mechanism --sims 2000 --out <scratch>/mechanism.yaml

# (ii) re-grade from scratch copies of runs/run_096, run_079, run_078 (layout in the docstring). 2.5 s.
python strategy-research/engineering/FOLD-FLOORS-2026-10-19/regrade.py --runs <scratch>/runs --out <scratch>/regrade.yaml
```

Seeds: `numpy.random.default_rng([20261019, pair index])` per pair of cells, and `[20261019, 999]` for the mechanism. A second full run reproduced every earlier cell exactly.

The outputs of this report's runs are in `results/`: `sim.yaml`, `mechanism.yaml` and `regrade.yaml`.
