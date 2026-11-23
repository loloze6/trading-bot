---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b2_two-hour-settlement-snapback_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 2-hour move into a funding settlement ran against its 24-hour trend, the coin moves back with the trend over the next 8 hours. The move is larger the larger the product of the 24-hour trend's and the 2-hour counter-move's sizes, each measured against the coin's hourly volatility over the past 7 days.
Consequence: A trader should trade only the settlements where both the trend and the counter-move are unusually large for the coin, and hold for about 8 hours, rather than trading every counter-trend settlement for 2 hours.
Why:
- F1: The tested signal's move is smaller than a trade costs. Across all counter-trend settlement cases it moves +0.059 % over 2 hours (t 6.0, n 20934) against a cost of 0.19 % per trade. The book's 26603 trades lose about 0.10 % each in fees (LONG +0.14 % before fees and +0.04 % after; SHORT −0.25 % before and −0.35 % after), which is how a real effect becomes a Sharpe of −2.31 and a mean of −0.068 % a day on days in a position.
- F2: The effect grows with both parts of the idea's own situation, measured against the coin's 7-day hourly volatility. In the top decile of (24h trend strength × 2h counter-move strength) the move is +0.21 % over 2 hours (t 4.8) and +0.21 % over 8 hours (t 2.8, n 1996), while deciles 0 to 3 give −0.04 % to +0.01 %. Cases in the top 40 % of both give +0.186 % at 2h (t 6.3) and +0.156 % at 8h (t 3.0, n 3448), against +0.035 % for the rest.
- F3: Strength alone is not the effect. Strong 24h trends whose 2h pre-move ran with the trend (no counter-move) give −0.03 % at 2h on the short side and +0.05 % at 2h on the long side (t −0.8 and 1.5). The whole non-counter-trend set gives −0.025 % (t −2.8, n 30235). The gain needs the counter-trend pre-move the theory describes.
- F6: Both sides carry the effect in the cases, so the short trades lose because of how the book trades them, not because the signal is wrong. Strong short cases give +0.24 % at 2h (t 5.3, n 1585) and strong long cases +0.11 % at 2h and +0.19 % at 8h (t 2.5). Yet the book's SHORT trades lose −0.25 % before fees, and it holds a position on 14 % of bars where the forecast is 0, out of 18 % of bars in a position.
