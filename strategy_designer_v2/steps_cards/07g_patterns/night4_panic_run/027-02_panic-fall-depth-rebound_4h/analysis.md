---
line: 7.g patterns
backtest: 027-02_panic-fall-depth-rebound_4h
idea tested: 027-02_panic-fall-depth-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3804 USD
---
## Findings
- **F1:** After a 4h panic-fall bar (mean 6-bar range at least 3 times its 180-bar mean, 6-bar return negative; the first such bar per 18-bar grid cell), the coin beats its normal drift over the next 1 to 3 days and not over 14 days: +1.68 % over 6 bars (t 2.41), +1.87 % over 12 bars (t 2.57) and +2.47 % over 18 bars (t 2.85, median +1.45 %, 61 % positive, strength 0.21, 141 cases), but −0.21 % over 42 bars (t −0.17) and +0.61 % over 84 bars (t 0.33, median −1.49 %).
- **F2:** The 3-day rebound after a panic fall is not driven by a few outliers: with the 5 % tails cut it is still +1.83 % (t 3.28). It holds in both halves of the windows: w1–w12 +1.59 % (t 1.56, 56 cases) and w13–w24 +3.04 % (t 2.39, 85 cases). Its mean excess return over 3 days is 13 times the 0.19 % cost of a trade.
- **F3:** Inside panic falls, the grading runs opposite to the tested idea: the deeper the 24h fall measured in the coin's usual 24h moves, the lower what follows. The slope of the standardised excess return on fall depth is −0.15 over 18 bars (t −2.92), −0.20 over 42 bars (t −4.02) and −0.15 over 84 bars (t −2.91), with 132 to 141 cases.
- **F4:** By quartile of fall depth (mean depths of 0.7, 2.5, 3.7 and 5.1 usual moves), the 3-day excess return falls from +6.2 % to +3.4 %, +0.6 % and −0.5 %. The 14-day excess return of the deepest quartile is −4.7 %, against +7.2 % for the shallowest.
- **F5:** The rebound does not grow with the size of the range: by quartile of the range ratio (3.1, 3.3, 3.7, 5.1), the 3-day excess return is +2.8 %, +3.9 %, +3.0 % and +0.2 %.
- **F6:** Neither high-range rises nor low-range falls are followed by a premium. After panic rises, the excess return is −0.01 % over 1 day (t −0.01) and −0.08 % over 3 days (t −0.05), on 76 cases. After falls of more than 5 % in calm stretches, it is +0.09 % over 3 days (t 0.25), on 580 cases.
- **F7:** The premium is carried by the smaller coins. The 3-day excess after panic falls is −0.40 % for BTC (22 cases) and −0.05 % for ETH (24 cases), against +1.2 % for LTC, +2.5 % for XMR, +3.2 % for ZEC and +6.5 % for XRP. The book follows this split: its mean daily return is 0.00014 for BTC against 0.00094 for XRP.
- **F8:** The tested book holds each bet for 84 bars, past the point where the rebound fades. Its trades entered on the lowest third of forecasts average +20.5 % net (median +3.7 %), against +3.4 % (median +1.1 %) for the highest third.

## Ideas
- `027-02_panic-fall-depth-rebound.g1_mild-panic-fall-rebound` (from F1, F2, F3, F4): Among 24-hour stretches where a coin's range is several times its 30-day average and its price fell, the smaller that fall measured in the coin's usual 24-hour moves, the higher its return over the next 3 days.
- `027-02_panic-fall-depth-rebound.g2_deep-panic-fall-continuation` (from F3, F4, F8): Among 24-hour stretches where a coin's range is several times its 30-day average and its price fell, the deeper that fall measured in the coin's usual 24-hour moves, the lower its return over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
