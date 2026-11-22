---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows.b1_bounce-fade-all-coins
line: 7.g patterns
backtest: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows.b1_bounce-fade-all-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, a one-day rise that is large relative to its 20-day standard deviation of daily returns is given back mostly over the next 1 to 3 days. The larger the rise in usual moves, the larger the fall over those days.
Consequence: A trader shorting bounces in falling coins would bet on the next 1 to 3 days, not hold the short for weeks.
Why:
- F3: In falling coins, rises do fade, as the tested idea says, but unevenly over time. Five days after rises of more than 2 usual moves the unusual move is -3.76 % (t -2.71, n 79), and the slope of strength on rise size is -0.094 (t -2.49, n 1409). After rises above 1 usual move, the move is -2.4 % in <date> (t -3.22, n 285) but +2.4 % in <date> (t 1.77, n 90). Only 32 % of coins show a positive move after such rises, so the fade holds in most coins, but not in every period.
- F4: The fade in falling coins shows fastest. After rises of 1 to 2 usual moves, strength is -0.058 at 1 day (t -2.58, n 1522) and -0.112 at 3 days (t -3.17, n 517).
- F5: The book holds its shorts far longer than the 5-day horizon and loses on them. There are 4260 short trades, held 11.1 days on average, with a mean gross result of -3.69 % and only 33 % winners. On the book's worst 2 % of days (58 days), the coins rose +8.1 % on average.
