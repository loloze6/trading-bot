---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d2_volatility-graded-weekend-reversal
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d2_volatility-graded-weekend-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Saturday-to-Sunday close-to-close return reverses over the next 2 days (Monday and Tuesday). The move back grows steeply, more than in proportion, with how far the coin's 20-day daily volatility sits above its 60-day daily volatility, so the largest reversals come in the cases where recent volatility is furthest above its norm.
Consequence: A trader would concentrate the Sunday-close reversal bet in the coins whose recent volatility has jumped furthest above their longer norm, rather than spreading it across all weekend moves.
Why:
- F2: The reversal sits in the high-volatility-ratio cases. By quintile of s20/s60, the signed 2-day return is +0.76 % (t 2.6), +0.13 % (t 0.4), −0.18 % (t −0.5), +0.80 % (t 2.4) and +2.10 % (t 5.0), over about 520 cases each. The book's gain per case after costs is negative in the first three quintiles (−0.01 %, −0.06 %, −0.14 %) and +0.43 % and +1.25 % in the top two.
- F3: A rebuilt book that trades the Sunday bets only when s20/s60 is at or above its 60th percentile raises Calmar from 0.51 to 0.84. It does this by cutting the deepest fall from −23.7 % to −10.0 %, with Sharpe 0.90 against 0.74 and a yearly return of +8.3 %. At the 80th percentile, Calmar is 0.93 (fall −7.1 %, Sharpe 0.99, yearly return +6.7 %).
- F5: The book's gain is concentrated in its strongest forecasts. The top quintile of |forecast| has a mean signed return of +1.36 % (t 4.9) and carries a summed gain of 10.0 out of about 14.8. The lowest quintile earns −0.12 at a mean allocation of 0.02.
