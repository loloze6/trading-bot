---
idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 42e48552438e
---
Fidelity:
- Situation: a 4h close above the high of the preceding two days, sized by the prior 7-day return -> adapted: the breakout is a regime rule, close above the max high of the prior 12 bars; "after" becomes "while"; size grows with the 42-bar return.
- Comparison: rises more than usual, against the coin's normal drift -> kept
- Outcome: the coin rises over the next 12 days (72 bars), more after a stronger week -> kept
- Verdict transfer: yes: the rule is exactly the breakout, the size is exactly the 7-day return, and each bet is held for the 12-day horizon.
Forecast: On bars where the close is above the highest high of the prior 12 bars (a regime rule on DistanceFromHighComponent with period 12, source high and current bar excluded, value above 0), the forecast is the 42-bar return (PriceEvolutionComponent, period 42), standardised over its past 60 values (min 20). It is clipped at 0, so it is long only and grows with the strength of the week before the breakout. Because a breakout bar sits at a 2-day high, its 7-day return is mostly positive, so the clip rarely binds. On every other bar the forecast is 0. Each bet is held for 72 bars.
Config: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week_4h_config.json
Criterion:
- Horizon: 72 bars
- Main measure: The unusual move per case: the 72-bar return from the signal bar minus the coin's normal drift, averaged over the cases. Cases are forecast rises of at least 2 points, one per non-overlapping 72-bar grid cell in each window. The test is the t of that mean.
- Supporting check: Across cases, the slope of the unusual move on the case's forecast is positive (t ≥ 1).
- Confirm: The mean unusual move has t ≥ 2 over at least 100 independent cases, and the supporting check passes.
- Reject: The mean unusual move has t ≤ -2 over at least 100 independent cases.
- Inconclusive: These results neither confirm nor reject: a t between -2 and 2, a t of 2 or more with a failed slope check, or fewer than 100 independent cases.
