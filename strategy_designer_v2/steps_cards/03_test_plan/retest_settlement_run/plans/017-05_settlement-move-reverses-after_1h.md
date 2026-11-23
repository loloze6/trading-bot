---
idea: 017-05_settlement-move-reverses-after
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the 2-hour return just before each funding settlement time -> kept: a 2-bar return read at the close of the bar that ends at 00:00, 08:00 or 16:00 UTC, selected by a settlement-clock regime.
- Comparison: none -> kept
- Outcome: the 2 hours after settlement run opposite to the pre-move, larger after a larger pre-move -> kept: a contrarian position sized by the pre-move, held 2 bars.
- Verdict transfer: yes: the test bets exactly against the pre-settlement 2-hour move, in proportion to its size, over the 2 hours after settlement.
Forecast: The forecast is active only on the bar whose close is a funding settlement time, where the coming bar starts at 00:00, 08:00 or 16:00 UTC (HoursToSettlement reads 8). On other bars the forecast is 0. On the settlement bar, the indicator is the 2-bar percent return (PriceEvolution, period 2), which covers the 2 hours before settlement. It is standardised against its own last 60 hourly values and then negated. The forecast is short after a rise into settlement and long after a fall. It is zero when the pre-move is zero, and its size grows linearly with the pre-move against the coin's usual 2-hour move, capped at ±20. Each bet is held for 2 bars.
Config: 017-05_settlement-move-reverses-after_1h_config.json
Criterion:
- Horizon: 2 bars
- Main measure: A case is a settlement bar with a nonzero forecast. These bars are 8 hours apart, so the cases do not overlap. For each case, take the forecast/10 × (close[t+2]/close[t] − 1 − the coin's normal 2-bar drift), computed inside each window. The main measure is the mean of this over all cases and coins, with its ordinary t.
- Supporting check: Sort the cases by |forecast| into thirds. The mean drift-removed 2-bar return in the forecast's direction is larger in the top third than in the bottom third, by Welch t ≥ 2.
- Confirm: The main measure has t ≥ 2 and the supporting check passes.
- Reject: The main measure has t ≤ −2.
- Inconclusive: Any result with t between −2 and 2 is inconclusive, and so is a main t ≥ 2 without the check passing. At least 1000 cases in total are required; with fewer, the result is inconclusive.
