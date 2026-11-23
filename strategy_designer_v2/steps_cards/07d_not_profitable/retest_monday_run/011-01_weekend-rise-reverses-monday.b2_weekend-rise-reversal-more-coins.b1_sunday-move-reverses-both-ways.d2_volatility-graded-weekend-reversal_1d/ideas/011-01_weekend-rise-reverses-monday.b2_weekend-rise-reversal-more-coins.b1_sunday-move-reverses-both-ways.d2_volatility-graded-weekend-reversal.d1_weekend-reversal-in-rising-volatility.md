---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d2_volatility-graded-weekend-reversal
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d2_volatility-graded-weekend-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Saturday-to-Sunday close-to-close return reverses over the next 2 days (Monday and Tuesday), only while its 20-day daily volatility is above its 60-day daily volatility. Within that state, the move back is larger the further 20-day volatility exceeds 60-day volatility.
Consequence: A trader would take the Sunday-close bet against the weekend move only when recent volatility has risen above its longer norm, and stay out otherwise, where the reversal is too small to pay for its falls.
Why:
- F1: The book fails on its falls, not its gain. Its deepest fall is −23.7 % and lasts 903 days, against a yearly return of +12.3 %, so Calmar is 0.51. Inside that fall, the Sunday cases in the three lowest quintiles of s20/s60 lost −0.60, −0.55 and −1.18 (summed bar gains after costs), while the top two quintiles earned +0.32 and +0.78.
- F2: The reversal sits in the high-volatility-ratio cases. By quintile of s20/s60, the signed 2-day return is +0.76 % (t 2.6), +0.13 % (t 0.4), −0.18 % (t −0.5), +0.80 % (t 2.4) and +2.10 % (t 5.0), over about 520 cases each. The book's gain per case after costs is negative in the first three quintiles (−0.01 %, −0.06 %, −0.14 %) and +0.43 % and +1.25 % in the top two.
- F3: A rebuilt book that trades the Sunday bets only when s20/s60 is at or above its 60th percentile raises Calmar from 0.51 to 0.84. It does this by cutting the deepest fall from −23.7 % to −10.0 %, with Sharpe 0.90 against 0.74 and a yearly return of +8.3 %. At the 80th percentile, Calmar is 0.93 (fall −7.1 %, Sharpe 0.99, yearly return +6.7 %).
- F4: The volatility condition is not an effect of its own. On non-Sunday bars, betting against the 1-day move over the next 2 days earns −0.25 % (t −1.5, n 1490) in the lowest s20/s60 quintile and +0.20 % (t 1.0, n 1646) in the top one. Sunday cases in the top quintile earn +2.10 % (t 5.0). The weekend situation carries the effect, and the condition fits the theory: thin weekend books push price furthest when volatility has just risen.
- F6: Both sides lose in the deepest fall: short bets after weekend rises −0.88 and long bets after weekend falls −1.44. Both sides are positive over all cases (+0.79 %, t 5.1 and +0.56 %, t 3.8). Leaving out one side does not repair the falls.
