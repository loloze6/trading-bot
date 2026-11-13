---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-02_sma-death-cross-downward-drift
line: 7.b inconclusive
backtest: 002-02_sma-death-cross-downward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 50-day SMA is below its 200-day SMA, and price is in a moderate drawdown from its 60-day high (neither near the high nor at the deepest lows) and has bounced back above its 20-day SMA, the coin falls over the next 10 days by more than its average 10-day move.
Consequence: A trader would short a downtrending coin only on such a moderate relief bounce, and would refuse the short when price is near its high or already deeply sold off.
Why:
- F3: The short works where the coin is in a moderate drawdown from its 60-bar high. That middle tercile gives +0.028 (t 2.95, hit 58%, n 227). The deepest-drawdown tercile gives -0.011 (t -1.07) and the near-high tercile gives +0.001 (t 0.10).
- F4: Within the moderate-drawdown cases, the gain is concentrated where price has bounced back above its 20-bar SMA: +0.055 (t 3.39, hit 61%, n 95). The same drawdown with price below its 20-bar SMA gives +0.009 (t 0.80). Deep drawdown with price above its 20-bar SMA gives -0.033 (t -1.48).
- F1: The short's result is swamped by the market's own moves. The per-case excess gain has a standard deviation of 0.137 against a pooled weighted mean of 0.0022 (t 0.39, hit 52%, n 825), and it correlates 0.71 with BTC's own forward fall. When BTC's next 10 bars go down, the excess gain is +0.086 (t 13.5, hit 85%). When they go up, it is -0.076 (t -10.9, hit 22%).
