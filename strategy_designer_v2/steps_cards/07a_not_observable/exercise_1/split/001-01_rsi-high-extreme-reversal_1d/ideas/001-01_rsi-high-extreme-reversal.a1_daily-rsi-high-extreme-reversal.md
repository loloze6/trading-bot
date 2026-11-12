---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal
line: 7.a not observable
backtest: 001-01_rsi-high-extreme-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: 2019 to 2024, several windows (w1, w2, ...) per coin
---
Idea: In BTC, ETH and BNB daily bars, when RSI(14) is in the top of its own past-60-bar range (high-extreme reading), the coin's return over the next 5 bars is lower than its average 5-bar return over the same coin and window.
Consequence: A trader would refuse new longs, or lean short, in a coin whose daily RSI sits at the top of its recent range, expecting the next week to underperform simply holding it.
Why:
- F1: The backtest holds only BTCUSD, in one window (w1) of 120 daily bars spanning 119 days, all in 2022. ETH and BNB from the plan's three instruments are absent. So 120 bars is the whole sample, against a plan that pools 3 coins and several windows.
- F2: With a 5-bar horizon on non-overlapping grid bars, the single 120-bar window yields only 23 usable blocks in total. That is below the plan's minimum of 30 extreme cases even if every block were extreme.
- F3: The extreme situation was reached on 15 of 120 bars (forecast ≤ −10). These bars fell in only 3 episodes of 2, 1 and 12 bars, so the 5-bar grid kept just 3 non-overlapping cases against the required 30.
- F6: The direction measured so far matches the reversal claim, though the counts are tiny:
- F7: The case-to-case spread is large relative to the effect. The 5-bar forward return has an sd of 7.3% across all bars and the excess return 5.7% on extreme bars. At an effect of −2.3%, about 23 independent cases are needed for |t| = 2. A sample with that many extreme cases needs roughly 8–10 times the current extreme frequency in bar-count terms: several coins, several windows or years, or a shorter bar size where 14-bar RSI runs recur more often.
