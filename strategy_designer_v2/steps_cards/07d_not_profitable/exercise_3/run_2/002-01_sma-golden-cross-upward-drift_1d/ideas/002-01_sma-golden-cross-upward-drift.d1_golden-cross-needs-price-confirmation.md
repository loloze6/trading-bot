---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While the 50-day SMA is above the 200-day SMA, price keeps drifting upward, graded by the spread, only while price itself has been rising over the recent weeks. The more the recent price trend points down while the spread is still widening, the more price falls over the next days.
Consequence: A trader long on a golden cross would cut the position as the coin's own recent trend turns down, even though the averages still show an up-trend.
Why:
- F1: The book's daily chain fell 93.1% at its deepest. The fall stayed within 12–27% through w10, deepened to 71% in w13 and reached 93% by w21. Inside w11–w18 the book badly trailed holding: w13 −54.8% against −30.0%, w16 −35.4% against +35.8%, w18 −60.0% against −22.0%. This is what sinks Calmar (0.001).
- F2: On the book's worst 2% of active bars (n=200), it held a mean allocation of 1.78, against 0.94 over all active bars. Those bars also had 20-bar volatility of 0.078 against 0.045, and sat 18.4% below the 20-bar high against 10.9%. The largest positions sat in the most violent, already-falling markets.
- F3: When the 50/200 spread had risen over the last 10 bars but price had fallen over the last 20 bars, the position lost money. Its mean daily gain was −0.0019, with a Sharpe of −0.51 and summed gain of −2.46 over 1,292 bars. Its non-overlapping 10-bar excess return was −0.0248 (t −1.74, n=116). The same rising spread with price up over 20 bars earned +0.0291 (t 2.07, n=239), with a daily Sharpe of 1.06.
