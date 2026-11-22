---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 30-day return, the larger its rise over the next 5 days, the more so the lower the coin's 20-day volatility stands against its own past.
Consequence: A trader trusts monthly momentum in a coin while it trades calmly for itself, and discounts the same monthly move when the coin is in a turbulent stretch.
Why:
- F1: The tested monthly momentum works mainly in calm coins. Split by each coin's own 20-day volatility into terciles, the slope of the 5-day demeaned move (in units of the usual move) on the 30-day return is 0.32 (t 2.86) in the calmest third, 0.25 (t 2.91) in the middle third and 0.08 (t 1.39) in the most volatile third, about 1,790 grid cases each. Split by volatility pooled across coins, the same falloff shows: 0.50 (t 4.01), 0.19 (t 2.07), 0.04 (t 1.04).
- F3: The book's gain comes from the long side alone. Long bars earn +0.168 % per bar over 20,837 bars and short bars lose 0.021 % over 11,013. Long trades average +10.9 % net with a median of −1.0 %; short trades average −0.70 %.
