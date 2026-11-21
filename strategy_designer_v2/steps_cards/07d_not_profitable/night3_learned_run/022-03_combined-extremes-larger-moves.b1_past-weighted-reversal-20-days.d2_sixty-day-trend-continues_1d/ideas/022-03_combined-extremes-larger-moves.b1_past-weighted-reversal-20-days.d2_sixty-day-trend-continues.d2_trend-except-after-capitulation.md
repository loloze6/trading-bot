---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues
line: 7.d not profitable
backtest: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 60-day return, the more the coin moves in that same direction over the next 20 days, except after a 60-day fall whose last 20 days fell steeply, where the deeper the 20-day fall, the more the coin rises over the next 20 days.
Consequence: A trader would refuse to short a falling coin after a steep 20-day fall, and would expect it to rebound more the deeper that fall.
Why:
- F5: After a 60-day fall whose last 20 days fell steeply, the coin rebounds. Shorts in the deepest 20-day-return quartile (mean −29 %) saw the coin rise 4.9 % above drift over the next 20 days (8.1 % total, t −2.74, 165 cases). Shorts after milder 20-day falls gained 4.7 % and 5.5 % (t 3.13 and 3.33). On days, coins in their lowest 60-day-return quintile rose 0.25 % a day afterwards, the second highest of the five quintiles.
- F3: The forecast is not graded. By forecast sextile, the unusual move in the forecast's direction is −0.45 % for the most negative sixth (mean forecast −16.5) and +1.4 % for the most positive (+18.6). Both are weaker than the moderate sixths (+2.5 % at −8.7, +3.2 % at +10.1). Within each side, the Spearman correlation of |forecast| with that move is −0.03 for longs (803 cases, p 0.42) and −0.06 for shorts (803 cases, p 0.10).
- F1: The book's shorts cost it most of holding's gain. Over 17,432 coin-days short, the shorts earned −0.069 % a day before fees. Of that, −0.078 % came from being short coins that drift up, and only +0.009 % from timing. Over 16,188 days long, the longs earned +0.122 % a day, with +0.032 % from timing. As a result the book makes 0.029 % a day against holding's 0.139 %, and fails the mean-return and Sharpe-against-holding measures.
