---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins.d1_broken-support-without-collapse
line: 7.g patterns
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins.d1_broken-support-without-collapse_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's fall over its last day, measured against its usual daily move over the past 20 days, the more the coin rises over the next 10 days.
Consequence: A daily close after an unusually large one-day drop is a reason to be long for about ten days and to refuse a fresh short there.
Why:
- F3: The day just before is what most predicts the next 10 days in these bars, and the sign is a rebound after a fall.
- F4: The rebound after a large down day holds in both halves of the 30-day trend. The lowest last-day fifth gave +1.84 % unusual when the 30-day return was in its lower half (n 284) and +3.02 % in its upper half (n 217); every other fifth in the lower half was negative.
- F5: The rebound comes after the first days. The lowest decile of the volatility-scaled last day returns -0.24 % over the next 3 days but +2.18 % unusual over 10 days, about 10 times the 0.22 % cost of a trade.
- F6: The rebound is not steady across coins or years. The rank correlation of the volatility-scaled last day with the following 10-day move is -0.069 overall (n 2928), negative in 15 of 19 coins (median -0.081). But the top-minus-bottom difference was positive in 2018, 2019 and 2023 and negative in 2020-2022, 2024 and 2025 (2025 t -3.67).
- F1: The book loses because it is short against coins that rise. Coins rose 0.142 % a day on average, the book lost 0.085 % a day, and all 5797 trades were shorts (mean net -3.03 %, median -2.90 %, negative on every one of 19 coins). The idea's unusual fall (+0.48 % per case, 2.2 times the 0.22 % cost) is smaller than the coin's drift against it (-1.38 %), so the total move per case is -0.90 %.
