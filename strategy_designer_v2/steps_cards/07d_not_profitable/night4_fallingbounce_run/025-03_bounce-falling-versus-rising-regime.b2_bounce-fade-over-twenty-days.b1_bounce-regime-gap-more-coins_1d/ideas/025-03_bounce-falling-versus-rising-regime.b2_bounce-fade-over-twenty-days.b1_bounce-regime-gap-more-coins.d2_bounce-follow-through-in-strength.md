---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days.b1_bounce-regime-gap-more-coins
line: 7.d not profitable
backtest: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days.b1_bounce-regime-gap-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin, the 20-day return after a one-day rise of several usual daily moves (its day's return over the standard deviation of its last 20 daily returns) is lower when its 90-day return is negative than when it is positive, and the gap widens as the rise gets larger. In a coin up over 90 days, the rise over the next 20 days after such a rise is larger the larger the coin's 20-day return before it.
Consequence: A trader would weight longs on sharp up days most heavily in coins already strongest over the past 20 days.
Why:
- F5: The long side is graded by the coin's recent strength. Long cases in the top quartile of the 20-day return (mean +47.8 %) end 9.25 % above drift (t 2.57, 164 cases, raw +12.4 %), against 1.7 % to 4.2 % in the other quartiles. Longs in the top quartile of the 60-day return gain 10.25 % above drift (t 1.83, 86 cases).
- F1: The book fails because its shorts lose. Bars held short sum to -17.37 of gain over 17,339 bars, while bars held long sum to +29.00 over 17,632 bars. The 1,913 SHORT trades average -15.4 % net (median -10.0 %, 30.4 % won), against +12.8 % for the 1,417 LONG trades. The book's Sharpe is 0.43 against holding's 0.60, and its deepest fall is -88.7 % against holding's -82.0 %.
