---
line: 7.b inconclusive
backtest: 067-02.b1_raw-swing-stretch-keeps-falling_1d
idea tested: 067-02.b1_raw-swing-stretch-keeps-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3181 USD
---
## Findings
- **F1:** The tested measure is essentially zero. On the short side, the slope of the 10-day excess return on the stretch is 0.00155 with a day-clustered t of 0.18 (200 cases, 114 days). On the visible folds B and C it is the same: below-average cases give a slope of 0.0054 with a clustered t of 0.25 (77 cases, 45 days). Being deeper below the average does not grade the following fall.
- **F2:** The grading appears only when both sides of the average are taken together. On folds B and C, the 10-day excess return rises across the stretch quintiles: -3.9 %, -4.8 %, -1.2 %, -0.4 %, +2.8 % (mean stretch -2.8 to +3.8 usual moves, about 28 cases each). The pooled slope is 0.0113 with a clustered t of 1.53 (143 cases, 73 days).
- **F3:** The both-sides carry is clearer over 5 days than over 10. At 5 days the pooled slope is 0.0082 with a clustered t of 1.74 (287 cases, 150 days). The directional excess is +1.26 % (t 1.49), a strength of 0.10 of a usual move. The 5-day quintiles also rise: -4.1 %, -2.1 %, -2.3 %, +0.1 %, +1.1 %.
- **F4:** The short side has a direction but no grade. Below-average cases show a directional excess of +2.7 % at 5 days (t 2.11, 91 days) and +3.3 % at 10 days (t 1.31), with a strength of about 0.22. Their slopes within the side have clustered t of only 0.76 and 0.25. Over the full data, the size is an unusual move of only +0.32 % (t 0.44, 324 days), against a normal drift of -1.15 % in the short direction.
- **F5:** The effect changes sign between years, so it is mixed. The 10-day pooled slope is -0.034 (clustered t -3.60) in 2018, -0.003 (t -0.33) in 2019, +0.022 (t 1.35) in 2020 and +0.007 (t 0.54) in 2021. The 5-day slope in 2018 is also negative (t -1.85).
- **F6:** By coin, the both-sides 5-day carry is positive on BTC, XMR, XRP and ZEC (strength 0.12 to 0.16; XRP slope t 1.99) and absent on ETH and LTC (strength -0.02 and -0.03).

## Ideas
- `067-02.b1.b1_two-sided-swing-stretch-five-days` (from F1, F2, F3, F6): In a choppy market, the further a coin's close stands from its 20-day average, above or below, counted in units of its current 20-day standard deviation of daily returns as it stands that day, the more the coin keeps moving the same way over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
