---
brief: 010_rsi-midline-regime-direction
source-idea: 010-02_rsi-below-midpoint-continues-down
line: 7.d not profitable
backtest: 010-02_rsi-below-midpoint-continues-down_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger the share of the past 14 days that a coin's 14-day RSI has spent below its midpoint, the larger the coin's fall over the next 7 days, only while the coin's 28-day return is negative, and the deeper that 28-day fall, the larger the continuation.
Consequence: A trader would take the RSI-below-midpoint short only when the coin's own 28-day move is already down, and would refuse it when that move is up, where the short was squeezed.
Why:
- F1: The Calmar failed because of one long fall: the book chained in window order fell -61.8% against a yearly return of +28.8%, and its deepest fall ran 414 days through windows w2 to w6 (2022–2023), where the book lost -60.8% while the coins rose +63.0%.
- F2: The book lost most when its side ran against the coin's 28-day move. Shorts held after a 28-day rise of 5–15% lost -1.14% a day (138 coin-days), and after a rise above 15% lost -1.05% a day (35). Longs held after a 28-day fall of 5–15% lost -0.61% a day (93), and after a fall above 15% lost -2.35% a day (15). Shorts in a 28-day fall above 15% earned +0.43% a day (844).
- F3: Pooled, the forecast's slope on the 7-day excess return had t 1.79 with signed excess +0.81% when the forecast's sign matched the 28-day return (511 non-overlapping cases), but t -1.03 with signed excess -0.82% when it did not (112 cases). The forecast's sign matched the 28-day return in most cases because the forecast correlates 0.76 with that return.
- F4: Daily book gain rose with how far the 28-day move went in the position's direction: the lowest alignment quintile lost -0.081% a day, against +0.026%, +0.331%, +0.121% and +0.111% for the other quintiles (890 coin-days each). With a 60-day move the lowest quintile was also negative (-0.043% against +0.13% to +0.29%).
- F5: The short side carried the falls. Shorts earned +0.002% a day (2,784 coin-days) against +0.190% for longs (2,801). In windows w2–w6 shorts lost -0.21 on BTC and -0.15 on ETH in summed daily gain, while longs gained +0.24 and +0.27.
