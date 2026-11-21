---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-02_support-retest-bounces-up.d2_support-retest-fails-downtrend
line: 7.b inconclusive
backtest: 020-02_support-retest-bounces-up.d2_support-retest-fails-downtrend_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's price falls back to a price where it turned up several times in the past 90 days while its 90-day return is negative, it tends to fall further over the next 5 days, and the deeper that 90-day fall, the larger the further fall.
Consequence: In a coin that has fallen over the past 90 days, a retest of old lows would be a reason to sell or stay out rather than to buy.
Why:
- F1: The result points the way the idea predicts but is too small for this data to show: step 5's mean signed excess 5-day fall is +0.60 % per case with t 1.13 over 271 cases. Across every active grid bar it is +0.74 % (t 1.80, 449 cases), against -0.11 % (t -0.53, 2,970 cases) on inactive bars. Measured from the next day's close it is +0.82 % (t 2.25, 448 cases).
- F2: The effect is spread thinly across coins, not carried by one. At 5 days the mean excess fall is positive on 5 of 6 coins: XMR +1.43 % (t 1.59), ETH +1.33 % (t 1.13), LTC +0.91 % (t 0.82), ZEC +0.59 %, XRP +0.45 %. BTC is about zero (-0.11 %, t -0.12). No coin reaches t 2 with 51 to 90 cases each, so the shortfall is too few cases rather than one coin driving it.
- F3: The effect is mixed across periods, and one sharp rebound year weighs heavily against it. At 5 days the excess fall is +2.4 % (t 2.03) in 2018 and +2.6 % (t 2.95) in 2019. In 2020 it is -5.2 % (t -3.54, 24 cases), and in 2025 -1.8 % (t -1.50). The same pattern holds at 10 days: +5.6 % and +5.2 % in 2018 and 2019, -9.4 % in 2020.
