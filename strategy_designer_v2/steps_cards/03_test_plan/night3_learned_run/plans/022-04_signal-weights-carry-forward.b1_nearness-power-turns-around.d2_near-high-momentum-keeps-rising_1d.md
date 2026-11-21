---
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.d2_near-high-momentum-keeps-rising
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: the close is near its 90-day high and the 20-day return is large -> adapted: each part is a graded level, and the two are added so the forecast rises with each.
- Comparison: none -> kept
- Outcome: a higher return over the next 5 days -> kept
- Verdict transfer: yes: the forecast rises with nearness to the 90-day high and with the 20-day return, and it is judged on the next 5 days' returns, so a confirm or a reject carries over to the idea.
Forecast: The forecast is the equal-weight mean of three parts. The first is the close's percent distance below its 90-bar closing high, standardised over 90 bars: it is 0 at the high and about -10 at its usual depth. The second is a constant +10 offset, so the nearness term (distance + 10) is positive when the close sits nearer its high than usual and negative when it sits further away. The third is the 20-bar percent return, standardised over 60 bars, which is positive after a rise and negative after a fall. The forecast is (distance + 10 + return) / 3. It is positive and larger the nearer the close is to its 90-day high and the stronger the 20-day rise. It is negative far below the high after a fall. It is near zero when the two terms cancel. It is graded on every bar, with no regime and no dead zone, and it is not long-only, because the header sets no side.
Config: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.d2_near-high-momentum-keeps-rising_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The slope of the next 5-bar return on the forecast, pooled over all coins and windows. The return is close[t+5]/close[t] - 1 minus the coin's mean 5-bar return over all its windows. The samples are non-overlapping grid bars (positions 0, 5, 10, ... of each window). The slope's t is reported with its number of cases.
- Supporting check: The book's timing gain is above 0. This is its mean daily return before costs minus the gain from the market's own rise.
- Confirm: The slope's t is 2 or more and the timing gain is above 0.
- Reject: The slope's t is -2 or less.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is a t of 2 or more when the timing gain is 0 or below. The test needs at least 200 grid cases with a non-zero forecast; with fewer, the result is inconclusive.
