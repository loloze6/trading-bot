---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample
line: 7.c rejected
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 14-day return, the more its price rises above its usual move over the next 5 days.
Consequence: A strong recent two-week run is a reason to lean long on the coin for the following week, rather than fading it.
Why:
- F3: The coin's own 14-day return predicts continuation: over 5 bars the top two quintiles beat the average (q5 +0.0106, t 1.97; q4 +0.0080, t 2.01; about 597 cases each) while q2 lagged it (-0.0155, t -3.76), with Spearman rho 0.047 (p 0.010); over 10 bars rho was 0.053 (p 0.046), and q5 beat the average by +0.0221 (t 1.83).
- F1: The idea was rejected because the market did the opposite of the forecast: at the extreme high-RSI cases (forecast ≤ -5), the 5-bar return beat the coin's average by +0.0129 (t 2.26, 523 non-overlapping cases), and the 10-bar return beat it by +0.0318 (t 2.36, 254 cases); the verdict's own count was +0.0144 (t 2.58, 595 cases), with only 1 of 6 coins negative.
