---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-02_sma-death-cross-downward-drift
line: 7.d not profitable
backtest: 002-02_sma-death-cross-downward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin, while the 50-day SMA is below the 200-day SMA and the gap between them has widened over the last 10 bars, a close below the 50-day SMA in high 20-day volatility is followed by a 10-bar rise larger than the coin's usual 10-bar move. An extended, accelerating decline exhausts itself and rebounds.
Consequence: A trader would refuse new shorts, or cut them, when a death-cross decline is still deepening in volatile conditions.
Why:
- F7: Shorting a deepening decline loses: with price below its 50-day SMA and the spread still widening, the short's 10-bar excess gain is -0.0102 non-overlapping (n=247, t -1.14), and -0.0147 (t -3.29) in the volatile tercile.
- F5: Short losses come from volatile bars: short bars in the calm volatility tercile earn +0.000051 a day gross, against -0.001138 in the middle tercile and -0.001446 in the volatile tercile, where coins rise 0.001786 a day.
- F3: A larger forecast loses more because it adds size without adding edge: the top |forecast| tercile loses -0.002588 a day gross at a mean allocation of -1.52, against -0.000487 for the bottom tercile at -0.27, even though forward 10-bar coin returns are similar (0.0150 vs 0.0199).
