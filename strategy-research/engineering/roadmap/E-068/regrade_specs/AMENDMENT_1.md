# Amendment 1 to the run_065 / run_066 re-grade specs (E-068 slice 1, CUL-386)

Written and committed 2026-10-03, **before any re-grade result was computed**,
and before the calibration below was run. Operator decisions of 2026-10-03.
The two spec files are unchanged; this amendment changes how their p-values
and verdicts are computed.

## Why

An Opus review found that the first significance method (`circular_shift_v1`)
is invalid for signals built from past prices, which covers both runs. It was
reproduced on random walks with no edge:

| Case | Share of p < 0.05 (should be about 0.05) |
|---|---|
| Daily, Donchian-like signal, continuation claim | 0.00-0.01 |
| Daily, Donchian-like signal, reversal claim | 0.10-0.12 |
| Hourly, momentum-like signal, rank IC, `greater` | 0.00 |
| Hourly, momentum-like signal, rank IC, `less` | 0.33 |
| The same with backward shifts that overlap the signal's lookback removed | 0.06-0.13 |

Cause: a backward shift pairs a bar with a signal that was computed from that
bar's own future returns.

## A. Significance method: `block_analytic_v1` (replaces `circular_shift_v1`)

The saved forecast and outcomes are used as they are, with no shifting.
Overlapping outcomes are handled by counting independent blocks of `h` bars,
gap-aware (`signal_statistics.gap_aware_active_block_count`, block size = the
horizon `h`).

- **rank_ic:** `signal_statistics.block_adjusted_pvalue(ic, n, h,
  placeable_blocks=n_eff)`. This is the function `tools/residual_ic.py` uses.
- **mean_diff, decay_curve, hit_rate:** the same block adjustment applied to the
  difference. `z = diff / sqrt(var_sel / neff_sel + var_ref / neff_ref)`, where
  `neff` is the gap-aware block count of each side. Two-sided normal p.
- **One-sided p:** `p2 / 2` if the effect points the claimed way, else
  `1 - p2 / 2`.

## B. Calibration gate (mandatory, whichever method is used)

The tool runs on simulated prices with **no edge**, using the real signals:

- `DonchianBreakoutComponent(period=20)` on daily bars;
- `KeltnerBreakoutComponent(ema_period=20, atr_period=20, atr_multiplier=2.0)`
  on hourly bars.

Each signal is a vectorized copy, proven equal to the component's own
`update()` by a test.

| Cell | Setup |
|---|---|
| Daily | 6 windows x 120 bars (plus 20 warm-up bars). `event forecast >= 12` and `event forecast <= -12`, each tested `greater` and `less`. `mean_diff` vs `complement`, horizons 1-5 |
| Hourly | 6 windows x 2,900 bars (plus warm-up). `all`, `rank_ic`, `greater` and `less`, horizons 72/168/336 |

- **Price models:** (1) iid normal log returns; (2) GARCH(1,1) volatility
  clustering (alpha 0.08, beta 0.90), with zero mean.
- **Simulations:** 400 per cell. The fixed seed is in `tools/claim_tests_calibration.py`.
- **Pass rule:** for every cell and every horizon, the share of one-sided
  p < 0.05 is within [0.025, 0.075]. That is about 0.05 plus or minus 2.3
  standard errors at 400 simulations.
  - Above 0.075 means flattering.
  - Below 0.025 means so conservative that a true effect would rarely show.
- **If any cell fails:** switch to the fallback the operator chose. Shuffle the
  returns in chunks, recompute the signal with the strategy's own component
  code 1,000 times, and load warm-up history from the data cache. The fallback
  must pass the same gate.
- The table is reported in the PR and in the re-grade report.

## C. Verdict rule (Decision 2, replaces "not significant = refuted")

At every horizon, with the floor met:

| Status | When |
|---|---|
| **refuted** | The effect is in the wrong direction or exactly zero at any horizon |
| **inconclusive** | Below the floor; or the right direction at every horizon but p >= 0.05 at some horizon; or the window-sign rule not met; or a statistic undefined |
| **supported** | The right direction and p < 0.05 at every horizon, and the window-sign rule met |

**Reason:** a weak but true finding must not be stored as false. "Not
significant" means "not shown on this sample", not "shown wrong". A real power
check stays for a later slice.

Unchanged: refuted dominates inconclusive when tests and variants are combined
(D-014). The claim is supported only if every test is supported on every
graded variant.
