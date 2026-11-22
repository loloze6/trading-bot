---
idea: 027-02_panic-fall-depth-rebound
brief: 027_panic-days-are-followed-by-a-premium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: a 24-hour stretch whose range is several times its 30-day average -> adapted: "after the stretch" made "while the stretch holds", as a regime: the mean 4h bar range over the last 6 bars is at least 3 times its 180-bar mean.
- Comparison: the deeper the coin's fall over that stretch -> kept: the 6-bar fall, graded, long only on falls.
- Outcome: a higher return over the next 14 days -> kept: each bet is held 84 bars, and its 84-bar return is judged against the coin's normal drift.
- Verdict transfer: yes: the test measures how the 84-bar excess return grows with the fall depth across the same high-range stretches the idea names.
Forecast: The regime detector compares the 30-day mean 4h bar range with the mean bar range of the last 6 bars (`MeanBarRangeRatioComponent`, long 180, short 6). When that ratio is 1/3 or less, the last 24 hours ran at least 3 times their usual bar range, and the bar is `mean_reversion`. On every other bar the regime is `unknown`, which is null, so the forecast is 0 and the book is flat. In the panic regime the forecast is the 6-bar price change in percent (`PriceEvolutionOnPeriodComponent`, comparison_period 6). It is standardised over its past 60 values (min 20), negated, then clipped at 0. So it is positive and grows with the depth of the 24h fall, about 10 at a usual-size fall and capped at 20. It is 0 when the stretch did not fall. It is never negative.
Config: 027-02_panic-fall-depth-rebound_4h_config.json
Criterion:
- Horizon: 84 bars
- Main measure: Each case is one bet in the panic regime, the first one per non-overlapping 84-bar grid cell of each window. - Fall depth: minus `fall.last_history_value`, read on the case's bar. - Excess return: close[t+84]/close[t]-1 minus the coin's mean 84-bar return over all its windows, divided by the coin's usual 84-bar move. - The measure is the slope of excess return on fall depth, pooled over the coins, with its t-statistic.
- Supporting check: The mean excess return of the cases is above 0.
- Confirm: The slope is positive with t ≥ 2, the supporting check passes, and there are at least 30 cases.
- Reject: The slope is negative with t ≤ -2, with at least 30 cases.
- Inconclusive: These results neither confirm nor reject: - a slope t between -2 and 2; - a slope t ≥ 2 while the mean excess return is not above 0; - fewer than 30 cases.
