---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.g2_down-day-close-near-high
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 69ac1b38a672
---
Fidelity:
- Situation: a day the coin closes lower, with its close location in the day's high-low range -> kept: a regime for close below the prior close, and close location as a graded measure.
- Comparison: return above the coin's usual drift -> kept: the 3-day return minus the coin's mean 3-day return over all windows.
- Outcome: a higher return over the next 3 days, the nearer the close is to the high -> kept: a long position sized by close location, held 3 bars.
- Verdict transfer: yes: the test measures the idea's own condition, its own graded measure and its own horizon, so a confirm or a reject applies to the idea.
Forecast: The regime detector reads the 1-day price change (`PriceEvolutionComponent`, period 1). On a down day (change below 0) the bar is `mean_reversion`. Every other bar is `unknown`, which is flat. On down days the forecast is the day's close location, (close − low) / (high − low), from `CloseLocationInRangeComponent` with reference "low". It is standardised against its past 60 values, so it averages about +10. It is 0 when the close sits at the day's low and grows linearly as the close nears the high, up to the cap of 20. It is never negative, so the strategy is long only. The position appears only on down days and is sized by nearness to the high.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.g2_down-day-close-near-high_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: Sample each window on a non-overlapping 3-bar grid and keep the down-day bars (regime `mean_reversion`). Regress the excess return on the forecast and read the slope's t. The excess return is close[t+3] / close[t] − 1 minus the coin's mean 3-bar return over all windows.
- Supporting check: The book's timing gain must be above 0. This is its mean daily return minus the gain from the market's own rise (position × the coin's mean daily return).
- Confirm: The slope's t is 2 or more and the timing gain is above 0.
- Reject: The slope's t is −2 or less.
- Inconclusive: Any t between −2 and 2, or a t of 2 or more with a timing gain at or below 0, is inconclusive. Fewer than 200 down-day grid cases across all coins and windows is also inconclusive.
