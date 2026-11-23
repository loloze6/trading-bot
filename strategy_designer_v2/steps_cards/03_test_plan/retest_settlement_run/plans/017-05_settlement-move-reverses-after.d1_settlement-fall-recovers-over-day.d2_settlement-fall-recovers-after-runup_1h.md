---
idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a fall over the 2 hours before a 00:00 or 16:00 UTC settlement, with a positive 7-day return before it -> adapted: "after the settlement" becomes "on the settlement bar", using the fall times the 7-day rise.
- Comparison: the fall against the coin's usual 2-hour move; a flat or falling coin gives no reason -> kept: the fall is divided by the 30-day mean absolute 2-hour return, and a 7-day return at or below 0 gives 0.
- Outcome: the price rises over the next 24 hours, more for a larger scaled fall and a larger run-up -> kept: long, held 24 bars.
- Verdict transfer: yes: the forecast is the idea's own interaction, taken only on settlement bars and held for its 24-hour horizon.
Forecast: The forecast is set only on the bar whose close is 00:00 or 16:00 UTC (the coming bar starts at hour 0 or 16). On every other bar it is 0, but each bet is held for 24 bars. - Indicator: MeanAbsScaledFallTimesRiseComponent with fall_period 2, window 720 and rise_period 168, ending at the settlement. - What it computes: the 2-hour fall into the settlement in usual 2-hour moves, times the 7-day percent return ending at the settlement. - Sign: it is 0 when the last 2 hours did not fall or the 7-day return is not positive, and positive otherwise. It is never negative, so the book is long or flat. - Size: it grows with the depth of the fall and with the size of the run-up. - Scale: it is standardised over its last 500 values (min_periods 120), so a typical active value is about 10, capped at 20.
Config: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Cases are bets on settlement bars, one per 24-bar grid cell of each window. For each case, take the coin's 24-bar return from the case bar minus the coin's mean 24-bar return over all windows, multiplied by forecast/10. Test the mean of this product with the t of the mean.
- Supporting check: Split the cases at the median forecast. The mean excess 24-bar return of the upper half minus that of the lower half must be above 0.
- Confirm: The main measure's t is 2 or more, and the supporting check passes (upper half minus lower half above 0), on at least 100 cases.
- Reject: The main measure's t is -2 or less, on at least 100 cases.
- Inconclusive: A t between -2 and 2, a t of 2 or more with the supporting check failing, or fewer than 100 cases.
