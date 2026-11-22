---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 30-day return measured against its own 20-day daily volatility, the larger its rise over the next 5 days.
Consequence: A trader ranks monthly strength by how unusual it is for that coin's own volatility, and leans long hardest on steady rises rather than large but noisy ones.
Why:
- F2: The 30-day return divided by the coin's 20-day daily volatility (times the square root of 30) predicts the next 5 days better than the raw 30-day return: t 4.22 against 3.45 on the same 5,363 non-overlapping cases. The vol-scaled t also stays higher inside each own-volatility tercile: 3.30, 3.00 and 1.42 against 2.86, 2.91 and 1.39.
- F1: The tested monthly momentum works mainly in calm coins. Split by each coin's own 20-day volatility into terciles, the slope of the 5-day demeaned move (in units of the usual move) on the 30-day return is 0.32 (t 2.86) in the calmest third, 0.25 (t 2.91) in the middle third and 0.08 (t 1.39) in the most volatile third, about 1,790 grid cases each. Split by volatility pooled across coins, the same falloff shows: 0.50 (t 4.01), 0.19 (t 2.07), 0.04 (t 1.04).
