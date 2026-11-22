---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins
line: 7.d not profitable
backtest: 025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin, the 5-day return after a one-day rise of several usual daily moves is lower when its 90-day return is negative than when its 90-day return is positive. The gap widens as the rise gets larger, only while its 30-day return is still negative, and it grows the deeper that 30-day fall is.
Consequence: A trader would short a sharp bounce in a falling coin only while the past month is still a fall, and more strongly the deeper that fall. A bounce in a coin that has already recovered over the past month is not a reason to short.
Why:
- F1: The Calmar failure comes from the short side. Chained alone, the short positions return −7.1 % a year with a deepest fall of −65 % (Sharpe −0.23). The long positions return +34 % a year with a deepest fall of only −25 % (Sharpe 1.35). The whole book returns 21 % a year with a −59 % fall, so its Calmar is 0.36.
- F2: The book's deepest fall ran −59 % over 1014 days, across w15 to w23. Over that stretch the short positions lost −0.70 in summed daily gain and the long positions only −0.06, so the shorts carried almost all of it.
- F3: Inside the book's six deepest falls the book was short more often than elsewhere (41 % of bars against 32 %). Its shorts lost there (−0.075 % per bar against +0.19 % elsewhere). The coins were also far less extended over 90 days (mean 90-day return +14 % against +66 %).
- F4: On the 5-day grid, the short signals made in the falling regime fade only while the coin is still deep in its fall. In the most negative quarter of 30-day returns (mean −28 %) the unusual 5-day move is −3.9 % (t −3.29, 135 cases). In the quarter whose 30-day return is already positive (mean +21 %) it is +1.3 % (t +1.15, 134 cases). The grading is monotone across the four quarters (−3.9, −1.5, −0.1, +1.3 %).
