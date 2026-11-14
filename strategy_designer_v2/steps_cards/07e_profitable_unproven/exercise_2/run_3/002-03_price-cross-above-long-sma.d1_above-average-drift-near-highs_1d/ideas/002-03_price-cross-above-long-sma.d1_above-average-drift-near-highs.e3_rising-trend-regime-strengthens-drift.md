---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs
line: 7.e profitable but not proven
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The drift that follows a close near its recent high above the long average is larger when the coin's own long average is rising than when it is flat or falling.
Consequence: A trader should lean harder into strength near highs when the coin's long-term trend slopes up and trim it when the long average is turning down.
Why:
- F7: The book earns in rising-market years and loses in falling ones. Its mean daily return is 0.00193 in 2020 and 0.00118 in 2024, against -0.00017 in 2018 and -0.00019 in 2022, years when holding returned -0.0035 and -0.0018 a day.
- F6: The gain is not carried by one coin. Leaving any coin out keeps the book's mean daily return between 0.000476 and 0.000678. LTC (-0.000005) and XMR (0.000073) earn almost nothing.
