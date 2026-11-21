---
idea: 017-05_settlement-move-reverses-after
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the 2-hour return into each funding settlement (00, 08, 16 UTC) -> kept: a regime selects the bar closing at settlement, and the 2-bar return is measured at that close.
- Comparison: none -> kept
- Outcome: the 2 hours after settlement run opposite to the pre-settlement move, more so after a larger move -> adapted: the 2-hour hold is dropped, so the position lasts one bar while the criterion scores the 2-bar return.
- Verdict transfer: yes: the forecast is the negated pre-settlement move on settlement bars only, so its link to the next 2 bars' return is the idea's claim.
Forecast: A `HoursToSettlementComponent` in the regime detector selects `mean_reversion` only on the bar whose close is a settlement time. That is a reading of 8, meaning the coming bar starts at 00, 08 or 16 UTC. Every other bar is `unknown`, which is null, so the forecast there is 0 (flat). On a settlement bar the forecast is minus the 2-bar return (`PriceEvolutionComponent`, period 2), close at settlement over the close 2 bars earlier. That return is standardised against the mean absolute 2-bar return of the previous 60 bars, scaled to target 10 and capped at ±20, then negated. The forecast is positive (long) after a pre-settlement fall and negative (short) after a rise. Its size grows in proportion to the size of the move against its usual size. It is near 0 when the move was negligible.
Config: 017-05_settlement-move-reverses-after_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: The cases are the settlement bars (regime `mean_reversion`, forecast not 0). These bars are 8 apart, so their 2-bar forward returns do not overlap. The measure is the mean of forecast/10 × (close[t+2]/close[t] − 1 − the coin's mean 2-bar return over all its windows). It is pooled over coins and windows, with its ordinary t.
- Supporting check: The same forecast-signed excess 2-bar return is compared between two groups: the top third of settlement bars by |forecast| minus the bottom third. Its Welch t must be ≥ 2, since a larger pre-move must give a larger reversal.
- Confirm: The main mean is positive with t ≥ 2, and the supporting check passes.
- Reject: The main mean is negative with t ≤ −2.
- Inconclusive: Any other result is inconclusive. This includes a main t between −2 and 2, and a main t ≥ 2 with a failed supporting check. The test needs at least 1000 settlement bars in total, and at least 300 in each third.
