---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the next 24 hours runs opposite to a fall over the coin's past 24 hours: the larger that 24-hour fall against the coin's usual 24-hour move, the larger the rise that follows. The rise is larger still when the coin's hourly volatility over the past 3 days is high against its past 30 days.
Consequence: A trader buys a coin after a large 24-hour fall, most of all in a volatile spell, and holds for a day, where the rebound is several times a trade's cost; after a small fall, or in a calm spell, the trader refuses the trade.
Why:
- F1: Over the whole day, the coin's 24-hour fall is followed by a 24-hour rebound that is graded and far larger than a trade's cost. Measured on 14942 non-overlapping cases, the slope of the next-24h excess return on the 24h move (scaled by the usual 24h move) has t −7.78. The bottom quintile of 24h moves (2991 cases) is followed by an excess return of +0.54 % (t 5.1) and a total move of +0.68 %. That total is 3.6 times the 0.19 % cost of a trade, against 0.9 times for the tested 8-hour settlement case.
- F2: The 24h-fall rebound holds in every coin and across time. The per-coin slope t runs from −2.60 (LTC) to −4.47 (XMR). The slope is negative in 7 of 8 years, from t −0.84 (2022) to −5.66 (2021), and positive only in 2024 (t +0.93). Averaged across coins at each time, its signal profit still has t 3.90 over 6691 independent times.
- F3: The rebound is concentrated where volatility is high. By the coin's 30-day hourly volatility tercile, the slope t is +0.24, −2.66 and −9.28. In the high-volatility tercile, the bottom quintile of 24h moves (933 cases) is followed by an excess of +1.45 % (t 5.7) and a total of +1.59 %, about 8 times the cost.
- F4: Recent volatility against usual volatility sharpens the rebound further. When the 3-day hourly volatility over the 30-day one is in its top tercile, the slope t is −7.67 and the bottom-quintile excess is +1.11 %. In the bottom tercile the slope t is +0.33 and the bottom-quintile excess is −0.03 %.
- F6: The tested 2h-fall rebound is not specific to the funding settlements, which meets the brief's third rejection condition. The slope t of the 8h excess return on the 2h fall is 4.97 at close hour 00 and −0.13 at close hour 16. At the non-settlement close hours 02, 12 and 13 it is larger, at 10.73, 8.96 and 8.71.
