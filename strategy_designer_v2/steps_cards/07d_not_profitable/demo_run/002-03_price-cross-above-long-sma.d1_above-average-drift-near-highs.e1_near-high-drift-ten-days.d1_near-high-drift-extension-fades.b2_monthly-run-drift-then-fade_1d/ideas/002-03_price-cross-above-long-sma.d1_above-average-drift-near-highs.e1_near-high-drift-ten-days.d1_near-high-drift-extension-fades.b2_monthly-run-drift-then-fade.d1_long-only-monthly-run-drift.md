---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average and its 30-day return is positive, the larger that 30-day return, the larger its rise over the next 10 days, except at its very largest 30-day returns, where the larger that return, the smaller the rise over the next 10 days.
Consequence: A trader would hold only longs above the long average, sized up with the month-long run, and would stop shorting the uptrend's pullbacks, since those shorts add falls and no gain.
Why:
- F1: The short side earns nothing and the long side carries the whole book. In the trending regime, short bars average a gain of 0.000174 per bar (t 0.53, n 2535, mean allocation −0.27), while long bars average 0.001244 (t 4.71, n 5918, mean allocation 0.41). Across all bars, shorts summed 0.43 against 7.38 for longs.
- F2: Shorts deepen the falls that sink Calmar. The deepest fall is in w5 (−24.5%, the worst 20-day book sum −0.124). There shorts lost −0.58 against −0.29 for longs, and XRP alone lost −0.67 while its price rose 0.33. In 2023, shorts lost −0.639 while the coins' mean daily return was +0.0015 and the book's was −0.000192.
- F3: The coins do drift down after a negative 30-day run above the 200-day average, but only against their own average. Trending grid cases with a 30-day return ≤ 0 have a 10-day excess return of −0.024 (t −2.39, n 175). Shorting them still yields almost nothing (F1), because the coins' mean rise offsets the shortfall.
