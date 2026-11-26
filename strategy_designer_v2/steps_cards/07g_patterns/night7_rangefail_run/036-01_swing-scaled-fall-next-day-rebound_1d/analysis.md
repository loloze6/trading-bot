---
line: 7.g patterns
backtest: 036-01_swing-scaled-fall-next-day-rebound_1d
idea tested: 036-01_swing-scaled-fall-next-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4365 USD
---
## Findings
- **F1:** In folds B and C, the tested idea holds as a graded effect. Across 10,785 coin-days on 1,269 days, the next-day excess return rises with the swing-scaled one-day fall (fall = max(0, -return / 20-day std)): slope +1.04 % per swing, t 3.16. With returns winsorized at 1 %/99 % the slope is +0.84 %, t 3.31.
- **F2:** The rebound rises in steps with the fall's size, and up days get nothing:
- **F3:** The rebound lasts one day only:
- **F4:** The rebound after a fall is about twice as steep in an agitated market as in a calm one. Agitated here means 20-day swing above 60-day swing.
- **F5:** The 60-day trend adds no clear difference. The winsorized fall slope is +0.69 % (t 1.56) in falling markets, +0.80 % (t 1.90) in choppy ones and +0.57 % (t 1.40) in rising ones.
- **F6:** Where a falling day closes in its range adds little once the fall's size is known.
- **F7:** The idea's move is too small to pay for trading. Its unusual move per case is +0.09 % (t 0.66) against a cost of 0.22 % per trade.
- **F8:** Among the other angles, nothing stood out from chance across the number of splits looked at:

## Ideas
- `036-01.g1_agitated-sharp-fall-rebound` (from F4, F1, F2, F7): In an agitated market, the more of its own daily swings (the standard deviation of its daily returns over the past 20 days) a coin's one-day fall spans, the more the coin rises over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
