---
idea: 036-01_fall-vs-swing-next-day-rebound
brief: 036_outsized-daily-fall-rebounds
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 59f1baae24fe
---
Fidelity:
- Situation: a one-day close-to-close fall beyond the coin's 30-day standard deviation of daily returns -> adapted: the fall beyond one usual move is a regime; inside it the position is graded by the fall's size in usual moves.
- Comparison: the fall against the standard deviation of daily returns over the past 30 days -> kept
- Outcome: a rise over the next day that is larger the larger the relative fall -> kept
- Verdict transfer: yes: the test holds positions only on days whose fall exceeds the 30-day swing, sized by that relative fall, and judges the next day's return.
Forecast: The forecast uses one quantity: the day's close-to-close return divided by the standard deviation of the last 30 daily returns. This is VolatilityScaledReturnComponent with period 1 and vol_period 30. When that value is -1 or lower (the day fell by at least one usual move), the bar is in the active regime. There the same quantity is standardised over 60 bars, negated and clipped at 0. The forecast is then positive, and it grows with the depth of the fall in usual moves: about 12 at a one-usual-move fall, rising to the cap of 20 for falls near two usual moves or more. On every other day the forecast is 0. It never goes short.
Config: 036-01_fall-vs-swing-next-day-rebound_1d_config.json
Side: long only (the brief): each component's forecast capped at 0 by step 3's code
Criterion:
- Horizon: 1 bar
- Main measure: A case is a bar with forecast > 0. For each case, take the coin's next-day return minus the coin's mean daily return over all windows. Measure the mean of these values, with its t, clustering cases on the same day together.
- Supporting check: Split the cases by forecast size. The mean next-day excess return of the top third must be above the mean of the bottom third (Welch difference, top minus bottom, greater than 0).
- Confirm: The main measure is above 0 with t ≥ 2, and the supporting check passes.
- Reject: The main measure is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2, or a confirming main measure whose supporting check fails. At least 300 cases are required, on at least 200 distinct days.
