---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d1_wide-days-in-uptrends-rise
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 69ac1b38a672
---
Fidelity:
- Situation: the day's high-low range exceeds its 30-day average range, more strongly the wider, only while the 30-day return is positive -> kept: today's range over its 30-day mean bar range, graded above 1, inside a regime that is on only while the 30-day return is above 0.
- Comparison: the coin's average daily range over the past 30 days -> kept: the 30-bar mean of high minus low, today included.
- Outcome: return over the next 3 days above the usual drift, long -> kept: 3-bar forward return minus the coin's mean 3-bar return, long side only.
- Verdict transfer: yes: every part is measured as stated, so a confirm or a reject on this forecast is a confirm or a reject of the idea.
Forecast: The regime detector reads the 30-day return (`PriceEvolutionOnPeriodComponent`, 30 bars). When it is above 0, the bar is `trending`; otherwise it is `unknown`, which is flat. In `trending`, `RangeCompressionRatioComponent` (short 1 bar, long 30 bars, base mean bar range, form compression) gives 1 minus today's range over the 30-day mean bar range. This is negative when today is wider than average. It is standardised over its past 60 values, then negated, then clipped at 0. The forecast is therefore 0 when today's range is at or below its 30-day average. Above that, it is positive and grows in proportion to how far today's range exceeds the average, capped at 20. It is never negative.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d1_wide-days-in-uptrends-rise_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: The sample is the bars of each window's non-overlapping 3-bar grid where the forecast is above 0. For each such bar, take the forecast times the coin's excess 3-bar return. The excess return is close[t+3]/close[t]-1 minus the coin's mean 3-bar return over all windows. The measure is the mean of these products and its ordinary t, pooled over coins and windows.
- Supporting check: Split the same cases at their median forecast. The mean excess 3-bar return of the upper half minus that of the lower half must be above 0.
- Confirm: The main measure's t is 2 or more and the supporting check is above 0, with at least 100 cases.
- Reject: The main measure's t is -2 or less, with at least 100 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a t of 2 or more when the supporting check is at or below 0. So is any result with fewer than 100 grid cases that have a positive forecast.
