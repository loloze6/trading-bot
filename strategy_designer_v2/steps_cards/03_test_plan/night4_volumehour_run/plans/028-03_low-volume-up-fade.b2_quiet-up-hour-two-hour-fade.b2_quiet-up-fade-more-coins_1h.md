---
idea: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b2_quiet-up-fade-more-coins
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: an hour rising far more than its typical 30-day hourly move, on volume near its 30-day average -> adapted: the rise is graded in usual moves (dead zone), and the volume band is kept as a regime condition.
- Comparison: the rise against the mean absolute hourly move over 720 bars, and volume against its 720-bar mean -> kept
- Outcome: the price gives back part of the rise over the next two hours, more after a larger rise -> kept
- Verdict transfer: yes: the forecast is short only after quiet-volume rises, sized by the rise, and is judged over the next 2 bars.
Forecast: The volume ratio is this hour's volume over its 720-bar mean. While it sits between 0.8 and 1.25, the mean_reversion regime is active. In every other volume state the book is flat. Inside that regime the forecast starts from the 1-bar return divided by the mean absolute 1-bar return over 720 bars. That value is standardised over 500 bars and clipped at 0, so only rises count. A cubic signed_power then pushes ordinary rises close to zero and enlarges large ones. A final negate makes the forecast short. It is zero on falls and on small rises, and the short grows quickly as the hour's rise grows in usual moves. It is never long.
Config: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b2_quiet-up-fade-more-coins_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: A case is a short bet: the forecast falls by at least 2 points on its short side, read once per non-overlapping 2-bar grid cell of each window. For each case, take the coin's return over the next 2 bars in the short direction and subtract the coin's normal 2-bar drift taken over all windows. The measure is the mean of these values over all coins, before costs, with its t.
- Supporting check: Across the cases, regress each case's short-direction excess return on the size of the forecast at the signal's bar. The slope must be positive.
- Confirm: The mean short-direction excess return has t ≥ 2 over at least 30 cases, and the supporting slope is above 0.
- Reject: The mean short-direction excess return has t ≤ -2 over at least 30 cases, meaning such rises extend rather than give back.
- Inconclusive: Any t between -2 and 2 is inconclusive. A positive t of 2 or more with a slope at or below 0 is also inconclusive. So is any result from fewer than 30 cases.
