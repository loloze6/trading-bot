---
idea: 017-04_postsettle-decline-after-downtrend
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a coin with a strong 3-day run down, at each funding settlement (00:00, 08:00, 16:00 UTC) -> adapted: the strong fall is graded by the 72-bar return; the "after settlement" timing is held "while" the two hours after it run.
- Comparison: the stronger the 3-day fall, the larger the decline -> kept: the short position grows with the size of the 72-bar fall.
- Outcome: the return over the 2 hours after settlement is negative -> kept: a short is held over the two 1h bars starting at each settlement, a 2-bar horizon.
- Verdict transfer: yes: the test is short only after settlements, sized by the 3-day fall, and measured on the 2-bar return that follows.
Forecast: A regime rule uses HoursToSettlementComponent and selects only the bars whose coming bar starts at a settlement hour or one hour after it (value 7 to 8). The position is therefore held from the 00:00, 08:00 and 16:00 UTC closes until two hours later. All other bars are flat. In the selected regime the forecast is built in four steps: 1. Take the 72-bar (3-day) percent price change. 2. Standardise it against its last 73 values. 3. Clip it at a maximum of 0, so only runs down count and the forecast is never positive. 4. Damp it with signed_power (exponent 2), so mild falls give a small short and strong falls a large one. The forecast is 0 after a 3-day rise and grows more negative, smoothly, the deeper the 3-day fall.
Config: 017-04_postsettle-decline-after-downtrend_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: - Events: the settlement bars, those whose close falls at 00:00, 08:00 or 16:00 UTC (the coming bar starts on the settlement). Each event is one non-overlapping case. - For each event, take the 2-bar forward return within its window, minus the coin's mean 2-bar return over all windows (from the non-overlapping 2-bar grid). - Compute the per-event gain: -(forecast / 10) × that excess return. - Report the ordinary t of the mean gain over events with forecast below 0, before costs.
- Supporting check: Among events with forecast below 0, split by |forecast| into thirds. The mean excess 2-bar return of the largest third minus that of the smallest third must be below 0.
- Confirm: The mean gain is positive with t ≥ 2, and the supporting check passes (the largest-third minus smallest-third difference is below 0).
- Reject: The mean gain is negative with t ≤ -2, meaning the coin rises more than usual after settlements in proportion to the 3-day fall.
- Inconclusive: Any t between -2 and 2, or t ≥ 2 with the supporting check failing. At least 300 events with forecast below 0 are required; fewer is inconclusive.
