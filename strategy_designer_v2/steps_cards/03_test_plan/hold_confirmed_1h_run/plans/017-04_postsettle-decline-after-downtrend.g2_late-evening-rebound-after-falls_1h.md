---
idea: 017-04_postsettle-decline-after-downtrend.g2_late-evening-rebound-after-falls
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: a1c2ac068edc
---
Fidelity:
- Situation: a coin whose price fell over the last 3 days, at 21:00 UTC -> adapted: the 72-bar fall is made graded by depth (zero without a fall), and "at 21:00" is made "while the coming bar starts at 21:00 or 22:00".
- Comparison: a deeper 3-day fall is compared with a larger rise -> kept: the position grows with the depth of the fall.
- Outcome: the return over the 2 hours from 21:00 UTC is positive -> kept: the long is held from the 21:00 close to the 23:00 close, then the position is closed.
- Verdict transfer: yes: the test bets long, sized by the 3-day fall, over exactly the 21:00 to 23:00 UTC hours, which is the idea as stated.
Forecast: A clock regime is active only on decisions whose coming bar starts at 21:00 or 22:00 UTC (HourOfDayComponent between 20.5 and 22.5). Every other hour is flat. In that regime, the forecast is the 72-bar price change (PriceEvolutionComponent, period 72), standardised against its own past 72 values, negated so that a fall reads positive, and clipped at 0. It is zero when the coin did not fall over 3 days. It is positive and grows with the depth of the fall, up to the cap of 20. It is never negative.
Config: 017-04_postsettle-decline-after-downtrend.g2_late-evening-rebound-after-falls_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: The cases are the bars where the coming bar starts at 21:00 UTC and the forecast is above 0, one per day, so they do not overlap. For each case, take the 2-bar return close[t+2]/close[t]-1 and subtract the coin's mean 2-bar return over all its windows. Multiply that excess return by the forecast. Report the mean of this product over all coins pooled, with its ordinary t.
- Supporting check: Split the same cases at the forecast's tercile cut points. Compute the mean excess 2-bar return of the top tercile minus that of the bottom tercile, with its Welch t.
- Confirm: The main measure has t ≥ +2 AND the top-minus-bottom difference is above 0.
- Reject: The main measure has t ≤ -2, OR the top-minus-bottom difference has Welch t ≤ -2.
- Inconclusive: Any result between these is inconclusive, including a main t between -2 and +2 or a confirm-level main t with a top-minus-bottom difference at or below 0 that is not ≤ -2. At least 200 cases are needed overall, and at least 60 per tercile; with fewer, the test is inconclusive.
