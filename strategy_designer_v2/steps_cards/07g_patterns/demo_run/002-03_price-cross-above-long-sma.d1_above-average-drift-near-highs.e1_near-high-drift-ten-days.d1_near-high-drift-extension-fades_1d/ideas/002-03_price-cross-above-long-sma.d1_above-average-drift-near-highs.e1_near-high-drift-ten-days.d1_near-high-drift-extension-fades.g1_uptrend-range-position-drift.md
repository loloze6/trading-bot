---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the higher its close sits in its 20-day close range, the larger its rise over the next 10 days.
Consequence: A trader would size a long in an uptrending coin by how close it sits to its 20-day high, without a cut for extension, and would avoid such longs when the close sits near its 20-day low.
Why:
- F1: Above the 200-day average, the 10-day return minus the coin's mean rises with the close's place in its 20-day close range: +0.0335 in the top fifth of the range (t 2.56, 268 non-overlapping cases) against -0.0312 in the bottom fifth (t -2.86, 123 cases).
- F2: Below the 200-day average the same range position shows no gradient: the five bins run from -0.023 to +0.001, every |t| ≤ 1.3, so the range effect appears only in the uptrend regime.
- F4: The recorded forecast itself barely sorts the next 10 days on trending bars: its top quintile gives +0.014 (t 0.97) and its bottom quintile +0.004 (t 0.45). The 60-bar standardisation and the cubic penalty appear to have blurred the plain range and momentum effects in F1 and F3.
