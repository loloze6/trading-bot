---
idea: 017-04_postsettle-decline-after-downtrend.c1_post-settlement-decline-four-hours
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: a coin with a strong 3-day run down, at a funding settlement (00:00, 08:00, 16:00 UTC) -> adapted: "strong" fall made graded (the 72-bar fall's size), and "after settlement" made "while in the 4 bars after settlement".
- Comparison: none -> kept
- Outcome: the 4-hour return after settlement is negative, and more negative the stronger the 3-day fall -> kept
- Verdict transfer: yes: the short is held only over the 4 post-settlement bars and is sized by the 3-day fall, so its gain is the idea's claimed decline.
Forecast: The regime detector reads `HoursToSettlementComponent`. The idea's window is open when the coming bar starts 0 to 3 hours after a settlement (values 8, 7, 6, 5, rule between 4.5 and 8.5). Those bars go to the active regime; every other bar is flat. In the active regime, the forecast is the 72-bar (3-day) price change from `PriceEvolutionComponent` with period 72. It is standardised over 72 past values (min_periods 20) and clipped at a maximum of 0. It is negative (short) only after a 3-day fall, and its size grows with the size of that fall. It is 0 after a 3-day rise.
Config: 017-04_postsettle-decline-after-downtrend.c1_post-settlement-decline-four-hours_1h_config.json
Criterion:
- Horizon: 4 bars
- Main measure: One case per settlement episode where the forecast is below 0. The entry bar is the bar whose close is the settlement (stamped 23:00, 07:00 or 15:00). Each case takes the forecast at that entry bar divided by 10, times the coin's 4-bar return from that close minus the coin's mean 4-bar return over all windows. The measure is the mean of these products and its t across episodes. Episodes are disjoint 4-bar spans inside each window, and the count of cases is given.
- Supporting check: Among the same episodes, take the mean excess 4-bar return of the third with the largest |forecast| and subtract the mean of the third with the smallest |forecast|. The difference must be below 0.
- Confirm: The mean product is above 0 with t >= 2, and the supporting check passes.
- Reject: The mean product is below 0 with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t >= 2 with the supporting check failing is also inconclusive. The test needs at least 300 episodes with a negative forecast, pooled over coins and windows.
