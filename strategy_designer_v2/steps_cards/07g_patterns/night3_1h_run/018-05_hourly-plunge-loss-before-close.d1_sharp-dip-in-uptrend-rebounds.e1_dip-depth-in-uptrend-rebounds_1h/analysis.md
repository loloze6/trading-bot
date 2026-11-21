---
line: 7.g patterns
backtest: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e1_dip-depth-in-uptrend-rebounds_1h
idea tested: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e1_dip-depth-in-uptrend-rebounds
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4063 USD
---
## Findings
- **F1:** When a coin's 30-day return is negative, its 24-hour move reverses over the next day on both sides and in grades. Falls of more than 2 times its 30-day average absolute daily move were followed by +0.82 % above drift (t 2.56, 507 cases). Rises of more than 2 times were followed by −0.94 % (t −3.45, 307 cases). The slope is 27 bps per unit of scaled move (t 6.06, 6319 cases) at 1 day and 38 bps per unit (t 4.31, 3140 cases) at 2 days. It fades to 5 bps per unit (t 0.41) at 3 days.
- **F2:** This down-trend reversal is carried by the coin's most volatile third of bars. There the 1-day slope is 69 bps per unit (t 7.29, 2419 cases), against −3 bps (t −0.61) in its calmest third. It holds in both halves of the windows: w1–12 t 2.22, w13–24 t 5.81. It holds in every coin with the same sign, from t 1.21 (ZEC) to t 4.27 (XRP).
- **F3:** The tested dip-in-uptrend rebound over 3 days also grows with the coin's 30-day volatility. In the calm third of up-trend dips the rebound is +0.49 % (t 1.09, 116 cases). In the middle third it is +2.41 % (t 4.12, 127), and in the volatile third +2.57 % (t 1.75, 92). The slope rises from 23 bps per unit in the calm third to 197 bps (t 3.25) in the middle third.
- **F4:** The tested rebound does not outlast its 3 days. After up-trend falls beyond 2 times the usual daily move, the excess is +2.68 % at 3 days (t 3.65, 93 cases). It turns to −0.82 % at 6 days (t −0.63, 39) and −3.01 % at 10 days (t −1.56, 26).
- **F5:** In an up-trend, large 24-hour rises are not reversed over the next day: +0.00 % in the reversal direction (t 0.02, 959 cases). Large falls are reversed: +0.53 % (t 2.34, 547). Only the down-trend reverses both ways.
- **F6:** The book's gain rests on its tails. Its top 1 % of coin-days sum to 21.9, more than its whole sum of daily returns (16.5), while its bottom 1 % sum to −18.7. Its mean daily return is negative in 11 of 24 windows.
- **F7:** A coin's 7-day return in its top fifth, inside a positive 30-day return, was followed by +0.98 % above drift over 3 days (t 2.39, 634 cases). Given the many angles looked at, this is too weak to stand apart from chance.

## Ideas
- `018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e1_dip-depth-in-uptrend-rebounds.g1_downtrend-day-move-reverses` (from F1, F2, F5): When a coin's 30-day return is negative, the larger its 24-hour move in multiples of its 30-day average absolute daily return, the more the coin moves back the opposite way relative to its normal drift over the next 2 days.
- `018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e1_dip-depth-in-uptrend-rebounds.g2_volatile-downtrends-reverse-harder` (from F1, F2): When a coin's 30-day return is negative, the reversal over the next 2 days after its 24-hour move, in multiples of its 30-day average absolute daily return, is larger the higher its hourly volatility over the last 30 days.
- `018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e1_dip-depth-in-uptrend-rebounds.g3_dip-rebound-scales-with-volatility` (from F3, F4): When a coin's 30-day return is positive, the rebound above its normal drift over the next 3 days after a 24-hour fall, in multiples of its 30-day average absolute daily return, is larger the higher its hourly volatility over the last 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
