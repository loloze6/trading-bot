---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound
line: 7.g patterns
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: In a coin whose 30-day hourly volatility is high against its own past, the larger its 24-hour drop in multiples of its 30-day average absolute daily return, the more the coin rises over the next 2 days above its usual 2-day drift.
Consequence: In turbulent conditions, buying a multi-day plunge and holding it for two days captures a move many times the cost of a trade.
Why:
- F1: When a coin's 30-day hourly volatility was in its own top third, a 24-hour drop of more than 2 times its 30-day mean absolute 24-hour return was followed by a large rise: +327 bps of unusual move over the next 24 hours (t 5.8, 296 independent cases, strength 0.64, total move +342 bps, about 18 times the 0.19 % round-trip cost), and +468 bps over the next 48 hours (t 5.3, 141 cases, strength 0.67).
- F2: The same drop sizes in the coin's low and middle volatility thirds were followed by nothing that paid: −13 bps (t −0.6, 516 cases) and −23 bps (t −0.8, 507 cases) over 48 hours for drops above 1 multiple, against +157 bps (t 3.8, 482 cases) in the high third. So the tested idea's small average (+0.18 %, strength 0.024, t 1.98) is a strong high-volatility effect diluted by calm regimes.
- F3: Inside the high-volatility third the rebound grows with the size of the drop. The Spearman correlation between drop size and the excess return is 0.147 over 24 hours (p 1e-14, 2726 cases) and 0.158 over 48 hours (p 6e-9, 1337 cases), against 0.01 to 0.08 in the lower thirds. The drop-size times volatility-rank product correlates at 0.077 (p 1e-6) over 48 hours.
- F4: The high-volatility rebound is broad. Over 48 hours it is positive on all 6 coins (+80 to +242 bps, t 0.7 to 2.1). Over 24 hours it is positive in every year (2018 +186 bps t 3.6, 2019 +121 t 2.7, 2021 +204 t 3.6). Only 2022 is flat (+0.5 bps, 123 cases) and 2023 has almost no cases.
- F7: The book earned 5.7 bps a day against the coins' 11.9 bps, with a Calmar of 0.21. It sizes the same drop alike in every volatility regime, so it buys the calm-regime drops (F2) that do not rebound.
