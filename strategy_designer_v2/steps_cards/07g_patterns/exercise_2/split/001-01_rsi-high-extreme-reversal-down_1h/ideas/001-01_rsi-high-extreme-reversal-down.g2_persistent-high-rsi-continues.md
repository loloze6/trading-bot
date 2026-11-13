---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal-down
line: 7.g patterns
backtest: 001-01_rsi-high-extreme-reversal-down_1h
instruments: BTC, ETH, BNB
bar: 1h
period: fold A
---
Idea: Once a coin's 14-hour RSI has stayed above 50 for many hours in a row, the price keeps rising over the following 12 hours more than its usual drift.
Consequence: A trader should exit or refuse a give-back short once the high reading has lasted, rather than holding it while it waits for a reversal.
Why:
- F2: Trade results depend strongly on how long the trade is held. Trades of 3 hours or less earned +0.33% gross (n=3452). Trades of 6–17 hours lost -0.70% (n=1562), and trades longer than 17 hours lost -2.85% (n=1464).
- F4: The weakest entries are held longest. Trades entered at the smallest forecasts (-5.9 to -2.0) last 19.9 hours on average, against 8.9 hours for the strongest (≤ -11.3), and they have the lowest win rate (57% vs 60%).
- F7: The book lost in all 12 coin-windows, whether the coin fell or rose. It lost most in the rising windows w4 and w6 (coin +0.32 to +0.57, book -0.69 to -1.12), where it was short on 69–76% of bars. Even in falling windows it lost (for example ETH w2: coin -0.57, book -0.60).
- F3: The trade P&L is heavily negatively skewed. Shorts win 58–62% of the time with a median of +0.08%. But the 5th percentile is -5.06% against a 95th percentile of +1.34%, and the worst 10% of trades account for 125% of the total gross loss.
