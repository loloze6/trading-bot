---
brief: 023_range-reversion-when-no-trend
source-idea: 023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up
line: 7.g patterns
backtest: 023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin, the larger its rise over the 5 days up to Friday's close, the more it rises over the following day (Saturday), while after a fall over those 5 days Saturday tends to fall.
Consequence: A trader leans long into the weekend after a strong week and refuses Friday longs after a weak one.
Why:
- F1: Saturday is the strongest pattern in the bars, and it does not come from the idea. Saturday's daily return averages +0.45 % (t 5.53, n 2484), or +0.092 of the coin's 20-day volatility (t 5.37, n 2093). That is well above every other weekday: Sunday is +0.060 (t 3.14), Friday +0.048 (t 2.17), and Thursday is the only clearly negative day at −0.079 (t −3.38).
- F2: The Saturday rise holds up across coins and years. Its mean is positive in all 6 coins, from +0.06 % in BTC (t 0.50) to +0.53 % in XRP (t 1.76), with XMR at +0.44 % (t 2.39). It is positive in 6 of 8 years, for example 2020 at +1.00 % (t 3.30) and 2025 at +0.71 % (t 3.20). The exceptions are 2018 at −0.35 % (t −1.33) and 2023 at −0.02 % (t −0.13).
- F3: The Saturday return grows with the coin's rise over the 5 days up to Friday's close. Split into quarters of that rise, scaled by volatility, Saturday averages:
- F4: Daily moves in general do not continue the next day. After a 1-day move of more than 2 volatilities, the next day averages +0.05 of a volatility (n 481); after a move below −2 volatilities, +0.03 (n 411). This says the Friday-to-Saturday continuation in F3 is specific to the weekend.
