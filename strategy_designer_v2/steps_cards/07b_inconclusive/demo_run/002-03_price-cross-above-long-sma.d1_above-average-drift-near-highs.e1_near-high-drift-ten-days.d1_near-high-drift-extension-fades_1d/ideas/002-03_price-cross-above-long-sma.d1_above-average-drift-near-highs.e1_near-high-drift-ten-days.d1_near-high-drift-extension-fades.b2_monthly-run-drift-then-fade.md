---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the larger its 30-day return, the larger its rise over the next 10 days, except at its very largest 30-day returns, where the larger that return, the smaller the rise over the next 10 days.
Consequence: A trader would add to a coin's long as its month-long run grows above its long average, but trim it once the 30-day run becomes extreme.
Why:
- F5: The extension part only shows at the very top of the 30-day return. On trending bars the 10-day excess rises from -2.50% to +4.16% across the first four quintiles of the 30-day return (mean returns -17% to +26%), then drops to +0.02% in the top quintile (mean +71%).
