---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins
line: 7.g patterns
backtest: 027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: The more a coin's volatility over the last 5 days exceeds its volatility over the last 30 days, the higher its return over the next 14 days, both when its 30-day return was rising and when it was falling.
Consequence: A trader would lean long on coins whose recent volatility is expanding against its month-long norm and avoid coins whose volatility is contracting, for a two-week hold.
Why:
- F1: The ratio of a coin's 5-day to its 30-day volatility of 4h returns grades its 14-day return over its normal drift: the top quintile earns +4.99 % (t 3.64, 298 non-overlapping cases) and the bottom quintile −4.40 % (t −3.93, 298), rising steadily through −1.34 %, +0.34 % and +1.24 % in between. The per-coin Spearman correlation is positive in all 19 coins (mean 0.215, minimum 0.058), and top minus bottom is positive in 6 of 8 years (+0.13 to +0.23 in 2020, 2021, 2023, 2024 and 2025).
- F2: The F1 effect holds whatever the coin's prior trend. With a positive 30-day return, the 14-day excess goes from −3.99 % (t −2.68, 129) to +6.83 % (t 3.34, 147). With a negative one, it goes from −4.94 % (t −3.14, 177) to +3.68 % (t 2.05, 159). At 3 days the top quintile alone earns +1.72 % (t 4.99, 981) when the prior return is positive.
