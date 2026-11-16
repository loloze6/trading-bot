---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the stronger its rise toward its 20-day high, the larger its rise over the next 5 days. The rise is larger the longer the close has stayed above its 200-day average, counted in days.
Consequence: A trader would lean on near-high pushes in long-established uptrends and stay lighter on them shortly after the coin regains its 200-day average, where the deepest falls built up.
Why:
- F3: The deepest fall is -25.4 %, running from w4 to w10 over 782 days. In those windows the active bars earned 0.00088 against 0.00217 elsewhere, and the next-day return was 0.00076 against 0.00303, while allocation was higher (0.73 against 0.54). Middle-tercile forecasts in those windows lost money: next-day return -0.00051, gain -0.00015, from 494 bars.
- F6: How long the coin has been above its 200-day average matters. Bars about 24 days into the trending regime show a next-day return of -0.00003 and a gain of -0.0006 (1040 bars). Bars about 86 days in show 0.0051 and 0.0040 (1018 bars).
