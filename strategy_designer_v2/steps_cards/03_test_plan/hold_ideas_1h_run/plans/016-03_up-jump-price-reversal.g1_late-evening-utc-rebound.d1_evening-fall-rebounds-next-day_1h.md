---
idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin has fallen over the 24 hours up to the 20:00 UTC close -> kept: the 24-bar return at the bar closing at 20:00 UTC, graded by the size of the fall.
- Comparison: none
- Outcome: the deeper the fall, the more the price rises over the next 24 hours -> kept: a long sized by the fall, held 24 bars.
- Verdict transfer: yes: the test measures exactly the stated fall, at the stated time, against the stated next-24-hour rise.
Forecast: The forecast is active only on the hourly bar that closes at 20:00 UTC. That is the bar stamped 19:00, after which the coming bar starts at 20:00. A regime rule on HourOfDayComponent selects it, and every other hour is flat. On that bar the forecast takes the 24-bar percent return and standardises it over its own past 60 hourly values. It then negates the result, so a fall reads positive, and clips it at 0, so the book is long only. The forecast is 0 after a rise and grows in step with the depth of the 24-hour fall, up to the cap of 20. The 24-bar hold keeps the long through the following day.
Config: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The sample is the 20:00 UTC bars, one per day, so they do not overlap. On these bars, regress the next-24-bar return minus the coin's mean 24-bar return over all windows on the forecast (`post_pipeline_value` of fall24). Pool all coins and windows, and report the slope's t.
- Supporting check: On the 20:00 bars with forecast > 0, the mean next-24-bar excess return (as above) is positive.
- Confirm: The slope's t is +2 or more, and the supporting check passes.
- Reject: The slope's t is -2 or less.
- Inconclusive: Any slope t between -2 and +2 is inconclusive, including a t of +2 or more when the supporting check fails. The test needs at least 300 bars at 20:00 with forecast > 0, or it is inconclusive.
