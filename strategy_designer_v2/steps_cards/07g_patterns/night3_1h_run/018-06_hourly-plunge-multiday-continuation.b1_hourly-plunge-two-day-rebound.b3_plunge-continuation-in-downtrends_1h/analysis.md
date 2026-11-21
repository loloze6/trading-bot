---
line: 7.g patterns
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b3_plunge-continuation-in-downtrends_1h
idea tested: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b3_plunge-continuation-in-downtrends
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5789 USD
---
## Findings
- **F1:** Large 24-hour plunges rebound instead of continuing. When the 24-hour return is at or below -2.5 times its 30-day mean absolute 24-hour return, the next 24 hours show a strength of +0.295 (t 4.67, 459 independent cases), an unusual move of +1.50 % and a total move of +1.64 %. Over the next 48 hours the strength is +0.344 (t 3.87, 222 cases), the unusual move +2.27 % and the total move +2.55 %, about 12 and 13 times the 0.19 % cost of a trade. The rebound holds whether the 30-day return is negative (24 h: +0.302, t 3.57, 314 cases) or positive (+0.279, t 3.51, 145 cases).
- **F2:** The rebound is graded, and it is gone by 4 days. Over all falls, the slope of the next-day strength on the size of the fall is -0.077 (t -5.9, 6327 cases), and the same over the next 2 days (-0.077, t -4.16, 3131 cases). The slope over falls is negative on all 6 coins (XRP -0.126, t -4.0; ZEC -0.121, t -3.6; ETH -0.084, t -2.5; XMR -0.075, t -2.4; BTC -0.043; LTC -0.037). At the tested 96-hour horizon the plunge cases have a strength of -0.027 (t -0.18, 106 cases), so the tested horizon sits after the rebound has ended.
- **F3:** The next-day plunge rebound spreads across windows and coins, but not across all years:
- **F4:** The tested short book lost because it shorted into the rebound. Its trades lost before fees on 5 of 6 coins (mean gross -0.48 % to -2.28 %, only BTC +0.37 %), won only 29 % to 37 % of the time, and its deepest-forecast quartile lost -1.03 % gross per trade.
- **F5:** When the 30-day return is negative, large 24-hour rises are followed by a further fall over the next day:
- **F6:** Fridays stand out but are not stable. The next day after a Friday bar has a strength of +0.105 (t 5.47, 2459 cases), positive on all 6 coins (0.086 to 0.172). But it is +0.218 (t 6.35) in the earlier half of the windows and 0.000 in the later half, so it is not a stable pattern. The 7-day and 30-day return deciles (best t 2.3 to 3.2, no graded order) and volatility terciles show nothing that stands out across the many angles looked at.

## Ideas
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b3_plunge-continuation-in-downtrends.g1_one-day-plunge-two-day-rebound` (from F1, F2, F3, F4): When a coin's 24-hour return, read at an hourly close, falls by a large multiple of its 30-day average absolute daily return, the price rises over the next 2 days by more than the coin's usual 2-day drift, and the larger the fall relative to that average, the larger the rebound.
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b3_plunge-continuation-in-downtrends.g2_downtrend-rally-next-day-fade` (from F5, F2): When a coin's 30-day return is negative and its 24-hour return, read at an hourly close, rises by a large multiple of its 30-day average absolute daily return, the price falls over the next day by more than the coin's usual one-day drift, and the larger the rise relative to that average, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
