---
idea: N2-05_shock-up-continuation
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a coin closes up on the day by an outsized amount -> adapted: the one-day rise is graded, and a strong dead zone keeps small days near flat.
- Comparison: more than about 2.5 times the trailing 20-day volatility -> kept: the day's rise is divided by the mean absolute daily return of the prior 20 bars, a 20-day volatility scale.
- Outcome: keeps rising over the following five days, with no gain the very next day -> kept: read from the recorded closes over 5 bars after each signal bar, not from the one-bar position.
- Verdict transfer: yes: the test measures the 5-day rise after big up days against holding, and checks that the next day is flat.
Forecast: One component, the one-day percent rise of the close (PriceEvolutionComponent, period 1). It is divided by the mean absolute daily return of the previous 20 bars (standardise, window 20, min_periods 20). The standardise target is 6.4, so a rise of 2.5 standard deviations (about 3.13 mean absolute returns) gives 20. Down days are clipped to 0, so the forecast is long-only, as the idea is. Then signed_power with exponent 3 and pivot 20 is the strongest graded dead zone allowed. Typical values from a 1σ day give about 1.3, which is below the 2-point rebalance minimum, so the position stays near flat. A 2σ day gives about 10 (100 percent long). A day at or above 2.5σ gives 20. The forecast is never negative and is zero on down days.
Config: N2-05_shock-up-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: For each event, take the close-to-close return from the event bar to 5 bars later. An event is a bar with forecast ≥ 10 (a rise of about 2σ or more). Subtract 5 times the coin's mean daily return, pooled over all its windows. Events within 5 bars of an earlier counted event are merged and counted once. Results are pooled across coins.
- Supporting check: Mean next-bar (t to t+1) return after the same events, minus the coin's pooled mean daily return. The idea expects |t| < 2 here.
- Confirm: The mean 5-bar excess return after events is above 0, with t ≥ 2 over at least 30 independent events.
- Reject: The mean 5-bar excess return after events is below 0, with t ≤ -2 over at least 30 independent events (big up days reverse).
- Inconclusive: Any result with -2 < t < 2 is inconclusive, including an estimate near zero. Fewer than 30 independent events is also inconclusive, whatever the t.
