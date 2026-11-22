---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-02_panic-fall-depth-rebound
line: 7.g patterns
backtest: 027-02_panic-fall-depth-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: Among 24-hour stretches where a coin's range is several times its 30-day average and its price fell, the smaller that fall measured in the coin's usual 24-hour moves, the higher its return over the next 3 days.
Consequence: Panic bars with a modest fall are where the short rebound is worth buying, and the steepest falls are where it is not.
Why:
- F1: After a 4h panic-fall bar (mean 6-bar range at least 3 times its 180-bar mean, 6-bar return negative; the first such bar per 18-bar grid cell), the coin beats its normal drift over the next 1 to 3 days and not over 14 days: +1.68 % over 6 bars (t 2.41), +1.87 % over 12 bars (t 2.57) and +2.47 % over 18 bars (t 2.85, median +1.45 %, 61 % positive, strength 0.21, 141 cases), but −0.21 % over 42 bars (t −0.17) and +0.61 % over 84 bars (t 0.33, median −1.49 %).
- F2: The 3-day rebound after a panic fall is not driven by a few outliers: with the 5 % tails cut it is still +1.83 % (t 3.28). It holds in both halves of the windows: w1–w12 +1.59 % (t 1.56, 56 cases) and w13–w24 +3.04 % (t 2.39, 85 cases). Its mean excess return over 3 days is 13 times the 0.19 % cost of a trade.
- F3: Inside panic falls, the grading runs opposite to the tested idea: the deeper the 24h fall measured in the coin's usual 24h moves, the lower what follows. The slope of the standardised excess return on fall depth is −0.15 over 18 bars (t −2.92), −0.20 over 42 bars (t −4.02) and −0.15 over 84 bars (t −2.91), with 132 to 141 cases.
- F4: By quartile of fall depth (mean depths of 0.7, 2.5, 3.7 and 5.1 usual moves), the 3-day excess return falls from +6.2 % to +3.4 %, +0.6 % and −0.5 %. The 14-day excess return of the deepest quartile is −4.7 %, against +7.2 % for the shallowest.
