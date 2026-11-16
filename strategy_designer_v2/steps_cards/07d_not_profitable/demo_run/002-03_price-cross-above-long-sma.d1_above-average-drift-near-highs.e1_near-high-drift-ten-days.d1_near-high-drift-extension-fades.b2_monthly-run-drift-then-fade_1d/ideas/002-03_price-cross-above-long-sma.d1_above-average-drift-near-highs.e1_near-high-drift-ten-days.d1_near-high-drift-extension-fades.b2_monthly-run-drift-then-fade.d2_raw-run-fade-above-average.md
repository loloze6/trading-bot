---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b2_monthly-run-drift-then-fade_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the larger its 30-day percent gain, the larger its rise over the next 10 days, except where that gain is largest as a share of the price itself, where the larger the 30-day percent gain, the smaller the rise over the next 10 days.
Consequence: A trader would cut the long as the raw month-long gain becomes very large, rather than judging the run only against its own recent range, which keeps him fully long into the falls.
Why:
- F4: The fade at extreme runs is real in the raw 30-day return but missed by the standardised forecast. On trending grid cases with a positive 30-day return, the 10-day excess return is +0.044 (t 1.84) in the 26–45% quintile and −0.006 (t −0.24) above 45%. Long bars with a 30-day return above 40% gain 0.000189 per bar against 0.001998 for 7–40%, yet they still hold an allocation of 0.38 against 0.50. Meanwhile the standardised s ≥ 14 bucket shows no fade (s≥14 minus 8≤s<14: −0.0095, t −0.38).
- F5: The book's worst days come from large longs held after big runs. On the worst 5% of book days, the book is long on 68% of coin-bars (32% on other days), with mean allocation 0.26 (0.09), mean 30-day return 0.23 (0.04) and mean s 9.4 (6.3).
