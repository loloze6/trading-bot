---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b1_settlement-fall-rebound-more-coins
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b1_settlement-fall-rebound-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's recent volatility is high against its own longer-run volatility, its fall over the past 24 hours is followed by a rise over the next 24 hours. The deeper the fall against its usual 24-hour move, and the higher that volatility, the larger the rise.
Consequence: A trader buys deep 24-hour falls only when the coin is in an unusually volatile stretch, where the rebound per case is several times the cost of a trade, and refuses them in calm stretches.
Why:
- F1: Among the coins' most volatile thirds of days (recent 7-day hourly volatility over its 60-day level), a 24-hour fall is followed by a graded 24-hour rebound. The unusual move is +1.47 % (t 4.9, 807 non-overlapping cases) after a fall of more than 2 usual 24-hour moves and +0.98 % (t 6.1, 1387 cases) after a fall of 1 to 2. Small moves are followed by +0.16 % and +0.08 %, and rises of 1 to 2 usual moves by −0.49 % (t −3.3).
- F2: That high-volatility rebound after 24-hour falls held in 7 of 8 years, with 2022 flat at +0.18 % (t 0.3) and the others between +0.61 % and +2.90 %. It was positive in 83 % of windows. At +1.47 % per case it is 6.7 times the 0.22 % cost of a trade, against +0.08 % (0.3 times) for the tested settlement idea.
- F4: Across all coins, the strength of the 24-hour reversal on the 24-hour grid is graded. It is +0.122 of a usual move (t 4.0, 1953 cases) after falls of more than 2 usual moves and +0.059 (t 4.0, 4337 cases) after falls of 1 to 2. Between −1 and +2 usual moves it is −0.012 to −0.034.
- F5: The settlement clock adds nothing to the 2-hour-fall rebound. After a fall of more than 3 usual 2-hour moves, the next 24 hours' unusual move is +0.40 % (t 3.0) at the 00:00/16:00 settlement bars against +1.04 % (t 15.6) at all other hours. Falls of more than 1 usual move rebound at almost every hour of the day, with hour-23 bars (+0.33 %, t 4.3) no different from hours 8, 11 or 12 (+0.44 % to +0.48 %).
