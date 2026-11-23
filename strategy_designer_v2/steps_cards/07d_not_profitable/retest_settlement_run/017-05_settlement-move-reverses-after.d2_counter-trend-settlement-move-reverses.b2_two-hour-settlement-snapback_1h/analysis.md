---
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback_1h
idea tested: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3970 USD
---
## Findings
- **F1:** The tested signal's move is smaller than a trade costs. Across all counter-trend settlement cases it moves +0.059 % over 2 hours (t 6.0, n 20934) against a cost of 0.19 % per trade. The book's 26603 trades lose about 0.10 % each in fees (LONG +0.14 % before fees and +0.04 % after; SHORT −0.25 % before and −0.35 % after), which is how a real effect becomes a Sharpe of −2.31 and a mean of −0.068 % a day on days in a position.
- **F2:** The effect grows with both parts of the idea's own situation, measured against the coin's 7-day hourly volatility. In the top decile of (24h trend strength × 2h counter-move strength) the move is +0.21 % over 2 hours (t 4.8) and +0.21 % over 8 hours (t 2.8, n 1996), while deciles 0 to 3 give −0.04 % to +0.01 %. Cases in the top 40 % of both give +0.186 % at 2h (t 6.3) and +0.156 % at 8h (t 3.0, n 3448), against +0.035 % for the rest.
- **F3:** Strength alone is not the effect. Strong 24h trends whose 2h pre-move ran with the trend (no counter-move) give −0.03 % at 2h on the short side and +0.05 % at 2h on the long side (t −0.8 and 1.5). The whole non-counter-trend set gives −0.025 % (t −2.8, n 30235). The gain needs the counter-trend pre-move the theory describes.
- **F4:** The 08:00 UTC settlement (bar opening 07h) does not carry the effect, and it turns against the trade later. Counter-trend cases there give −0.012 % at 2h and −0.146 % at 8h (t −4.4, n 7405); among strong cases, +0.03 % at 2h and −0.26 % at 8h (t −2.9, n 1111).
- **F5:** At the 00:00 and 16:00 UTC settlements the strong counter-trend cases clear the cost, and more so over 8 hours. They give +0.29 % (00h) and +0.23 % (16h) over 2 hours (t 4.9 and 4.1, n 981 and 971), and +0.40 % and +0.29 % over 8 hours (t 4.4 and 2.5). All counter-trend cases at these two times give +0.082 % and +0.115 % at 2h, and +0.090 % and +0.166 % at 8h.
- **F6:** Both sides carry the effect in the cases, so the short trades lose because of how the book trades them, not because the signal is wrong. Strong short cases give +0.24 % at 2h (t 5.3, n 1585) and strong long cases +0.11 % at 2h and +0.19 % at 8h (t 2.5). Yet the book's SHORT trades lose −0.25 % before fees, and it holds a position on 14 % of bars where the forecast is 0, out of 18 % of bars in a position.

## Ideas
- `017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback.d1_strong-snapback-two-settlements` (from F1, F2, F3, F4, F5): At the 00:00 and 16:00 UTC funding settlements, when a coin's 2-hour move into settlement ran against its 24-hour trend, the coin moves back with the 24-hour trend over the next 8 hours. The move is larger the larger both the 24-hour trend and the 2-hour counter-move are against the coin's hourly volatility over the past 7 days.
- `017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback.d2_volatility-scaled-settlement-stretch-reversal` (from F1, F2, F3, F6): When a coin's 2-hour move into a funding settlement ran against its 24-hour trend, the coin moves back with the trend over the next 8 hours. The move is larger the larger the product of the 24-hour trend's and the 2-hour counter-move's sizes, each measured against the coin's hourly volatility over the past 7 days.
- `017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback.d3_08-00-settlement-counter-move-continues` (from F4): At the 08:00 UTC funding settlement, when a coin's 2-hour move into settlement ran against its 24-hour trend, the coin keeps moving against its 24-hour trend over the next 8 hours. The move is larger the stronger the 24-hour trend.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
