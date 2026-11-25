---
line: 7.g patterns
backtest: 032-02.b2.g2.d3_rebound-scaled-by-range-widening_1d
idea tested: 032-02.b2.g2.d3_rebound-scaled-by-range-widening
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3914 USD
---
## Findings
- **F1:** The day after a fall that is large against the coin's own past 30-day daily volatility, the coin rises more than its normal drift, and the rise grows with the size of the fall. By decile of that standardised return, lowest first, the next-day excess return is +0.82 % (646 cases, 203 days, t 1.85), +0.42 % (t 1.42), +0.21 %, +0.09 %, then about 0 or negative from the fifth decile on.
- **F2:** That rebound after a large standardised fall points the same way on every coin: BTC +0.27 % (t 0.89), ETH +0.65 % (t 1.85), LTC +0.48 % (t 1.22), XMR +1.17 % (t 3.29), XRP +0.49 % (t 1.20) and ZEC +0.67 % (t 1.80). It also points the same way in 11 of the 12 windows (only w15 is negative, −0.52 %) and in every year from 2018 to 2021.
- **F3:** The rebound after the bottom-quintile standardised falls roughly doubles when the past 20 days' ranges are wide against the past 60 days': +0.97 % (462 cases, 181 days, t 1.98) against +0.43 % (830 cases, 296 days, t 1.30) when they are not. In both cases the mean move per case is above the 0.19 % cost of a trade.
- **F4:** The rebound after a down day does not need the tested idea's wide-range regime. In the bottom quintile of the previous day's return, the next-day excess return is +0.67 % outside the regime (799 bars, bar-level t 4.02) and +0.75 % inside it (925 bars, t 3.00). The tested idea's close near the day's low is part of this down-day effect: +0.85 % in the regime, t 3.43.
- **F5:** The book's best and worst days both come at high long forecasts (mean forecast 17.6 in the top gain decile, 16.6 in the bottom one). What separates them is the day before: a standardised return of −0.86 before the best decile against −0.40 before the worst. The book wins when its long follows a larger fall in volatility terms.
- **F6:** When the past 30 days' ranges are narrowest against the past 90 days' (the bottom quintile of the ratio), the next-day excess return is +1.42 % (457 cases, 141 days, t 2.96). The other four quintiles lie between −0.33 % and +0.06 %. The effect is concentrated in w11, w13, w16 and w18, and is negative in w7 and w15.

## Ideas
- `032-02.b2.g2.d3.g1_volatility-scaled-down-day-rebound` (from F1, F2, F3, F4, F5): The larger a coin's last 1-day fall compared with its own typical daily move over the past 30 days, the larger its rise over the next 1 day. The rebound is larger still when the coin's daily high-low ranges over the past 20 days are wide against those of the past 60 days.
- `032-02.b2.g2.d3.g2_calm-after-turbulence-daily-drift` (from F6): The narrower a coin's daily high-low ranges over the past 30 days compared with those of the past 90 days, the larger its rise over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
