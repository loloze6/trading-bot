---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.g1_volatile-coin-short-horizon-dip-rebound
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after.g1_volatile-coin-short-horizon-dip-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's 7-day mean absolute hourly move ranks against its own last 30 days, the larger its rise over the next 2 hours after a 2-hour fall measured in its usual 2-hour moves, with the rebound largest after the deepest falls in the most volatile stretches.
Consequence: A dip-rebound trade is worth paying fees for only when the coin is unusually volatile for itself, and its expected size should scale with both the fall and that volatility rank.
Why:
- F3: Only the strongest forecasts pay their fees. Bars held with forecast 15–20 earn 14.38 gross against 8.46 in fees, while forecasts 0–5 earn 0.76 against 6.87 and forecasts 5–10 earn 1.42 against 7.35; at entry, every forecast quintile loses after fees (-0.23% to -0.30% per trade).
- F4: The rebound is too small at 2 hours for most signals. The 2-hour excess return is only 2.1 bp in the lowest positive-forecast quintile and 4.4–6.6 bp in the middle ones, against about 20 bp of fees for a round trip; only the top quintile reaches 21 bp.
- F6: The rebound is graded by the coin's volatility rank, not switched on by it:
