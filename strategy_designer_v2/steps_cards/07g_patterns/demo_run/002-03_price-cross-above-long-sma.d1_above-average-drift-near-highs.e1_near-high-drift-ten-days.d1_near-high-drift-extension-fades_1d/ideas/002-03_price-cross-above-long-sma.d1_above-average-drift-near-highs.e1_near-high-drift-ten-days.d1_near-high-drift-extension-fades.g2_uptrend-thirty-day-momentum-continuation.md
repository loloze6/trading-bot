---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the larger its 30-day return, the larger its rise over the next 10 days.
Consequence: A trader would add to a long as the coin's 30-day run grows inside an uptrend, rather than cutting it back as the tested idea proposed.
Why:
- F3: Above the 200-day average, the next 10 days rise with the past 30-day return rather than fading after it: the lowest two quintiles give -0.028 (t -1.27, n 43) and -0.029 (t -2.53, n 88), and the highest two give +0.018 (t 1.54, n 168) and +0.022 (t 1.53, n 222). This is the opposite of the plan's extension penalty.
- F4: The recorded forecast itself barely sorts the next 10 days on trending bars: its top quintile gives +0.014 (t 0.97) and its bottom quintile +0.004 (t 0.45). The 60-bar standardisation and the cubic penalty appear to have blurred the plain range and momentum effects in F1 and F3.
- F5: The book loses most when it is positioned against strong moves: on its worst 2% of days (348) it lost 10.5% on average while the coin rose 7.9%, and on its best 2% it gained 9.4% while the coin fell 4.8%.
