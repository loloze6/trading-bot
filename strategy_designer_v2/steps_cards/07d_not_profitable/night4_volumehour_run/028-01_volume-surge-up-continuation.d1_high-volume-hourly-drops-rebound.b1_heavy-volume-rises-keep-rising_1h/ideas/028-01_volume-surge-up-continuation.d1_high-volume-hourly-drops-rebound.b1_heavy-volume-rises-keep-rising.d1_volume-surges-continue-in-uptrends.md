---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.b1_heavy-volume-rises-keep-rising
line: 7.d not profitable
backtest: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.b1_heavy-volume-rises-keep-rising_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours, only while the coin's 7-day return is large against its hourly volatility over those 7 days. The further rise is larger the larger that scaled 7-day return, the heavier the hour's volume against its 30-day average and the larger its rise against its typical hourly move.
Consequence: A trader would buy a sharp high-volume hourly rise only inside a strong week and refuse it in a flat or falling week, where it is not followed by a rise that covers the cost.
Why:
- F1: Almost all of the book's gain comes from simply being long the coins, not from the idea's timing. The book is long on 80 % of bars (mean position 0.77, 0.96 when long). Of its mean daily return of 0.1035 %, 0.0977 % is the market's own rise. Its daily returns correlate 0.85 with holding. Its Sharpe of 0.58 is below holding's 0.64.
- F2: The idea's move per case is smaller than a trade. Over 4448 cases the unusual 24-hour move is +0.07 % (t 1.03, strength 0.016), against a cost of 0.11 % per trade. The 6-hour unusual move is −0.05 % (t −1.26, n 3319).
- F3: The move is not graded by the forecast. The unusual 24-hour move is +0.079 % in the lowest third of cases by forecast, +0.022 % in the middle third and +0.077 % in the top third (about 1485 cases each, all |t| < 0.8).
- F4: The effect sits only in cases where the coin's 7-day return is large against its hourly volatility. In that top fifth (n 664) the unusual 24-hour move is +0.53 % (t 3.25, strength 0.13, 4.8 times the cost). The other four fifths are between −0.14 % and +0.06 % (all t < 0.5 in absolute value or negative).
- F5: The same holds on the raw 7-day return and on each coin separately.
- F6: The Calmar fails because the book stays long through falling markets.
