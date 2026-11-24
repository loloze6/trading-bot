---
line: 7.g patterns
backtest: 031-03.g1.b1.d2.e2_volume-swell-predicts-rise_1d
idea tested: 031-03.g1.b1.d2.e2_volume-swell-predicts-rise
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6768 USD
---
## Findings
- **F1:** The one clear pattern the tested idea does not explain is in XMR alone: a large daily move is followed by a move back the next day. The slope of the next day's return on the day's return in units of its 30-day volatility is −0.0046 (t −4.17, 2153 days). That is about 0.46 % back per unit of volatility, twice the 0.22 % cost of a trade. The slope is negative in 7 of 8 years (2020: −0.011, t −4.17; 2018: t −2.13; 2024: t −1.95; 2025 the only exception at +0.0002).
- **F2:** XMR's reversal is stronger after falls than after rises (slope −0.0075, t −2.65, 1006 down days, against −0.0021, t −1.09, 1145 up days). It is gone over 3 days (slope −0.0020, t −0.67, 686 cases). It is not a market-wide effect: pooled over all 19 coins the slope is −0.0007 (t −0.79, 27462 cases). After XMR, the most negative coins are ETH (t −2.25), BTC (t −1.82) and LTC (t −1.76), and DOGE leans the other way (t +2.57). With 19 coins looked at, only XMR's t of −4.2 stands clear of chance.
- **F3:** The volume swell's lean does not come from price momentum, a drawdown or the volatility level. After removing the 14-day return, the distance from the 30-day high and 30-day volatility from the ratio, its slope is unchanged (0.145 to 0.145 usual moves per standard deviation, t 2.89 to 2.90, 1530 cases, 131 days). Its correlation with the 14-day return is only 0.27.
- **F4:** The volume swell's lean is specific to its 14-day against 30-day form and its 14-day horizon. At 14 days its slope is 0.145 (t 2.89), against 0.069 (t 2.03) at 7 days and 0.080 (t 1.63) at 28 days. Other volume ratios read weaker: 7 against 30 days t 1.77, 7 against 60 days t 0.29, 14 against 60 days t 1.23.
- **F5:** The volume swell's lean is carried by 2023 and 2024 (slopes 0.217, t 2.71, and 0.378, t 2.95). It is flat or negative in 2018, 2019 and 2022 (t −0.47, −0.04, −0.16). The forecast's quintiles move only at the ends (top +3.4 %, t 1.58; bottom −2.8 %, t −1.92; middle three within ±0.7 %). This matches its size: +0.66 % per case with a t of 1.02.
- **F6:** The volume swell's lean looks larger in calm coins (lowest volatility tercile slope 0.183, t 3.76, against 0.131, t 1.61, in the highest). But the interaction itself cannot be told from 0 (slope −0.053, t −1.21, 1530 cases), so it is not a finding to build on.
- **F7:** The brief's own reversal is absent from these bars. Forward 14-day returns show no lean against the 60-day return (slope 0.011, t 0.18, 918 cases) or the 30-day return (t 0.52). The 14-day return leans slightly the same way (0.083, t 1.99).
- **F8:** The other angles show nothing that stands out once day-clustered and set against the number of angles looked at:

## Ideas
- `031-03.g1.b1.d2.e2.g1_xmr-next-day-move-reversal` (from F1, F2): The larger XMR's one-day return against its own 30-day daily volatility, the more its price moves back the other way over the next day, more so after a fall than after a rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
