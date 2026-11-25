---
line: 7.g patterns
backtest: 032-03.b2.b2_deep-calm-decline-five-days_1d
idea tested: 032-03.b2.b2_deep-calm-decline-five-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3948 USD
---
## Findings
- **F1:** Inside the low-volume regime (28-day mean volume below the 90 days before it), the next 5-day unusual move rises with the past return rather than falling with it. By 28-day return quintile, the move in units of the coin's usual move goes from −0.130 (t −1.61, n 114) and −0.153 (t −2.26, n 166) in the two lowest quintiles to +0.158 (t 2.18, n 160) and +0.197 (t 1.87, n 96) in the two highest, a spread of about 4 % per 5 days (−1.5 % against +2.8 %).
- **F2:** The same continuation is clearer on the 14-day return. In the low-volume regime, the slope of the 5-day standardised unusual move on the standardised 14-day return is +0.123 (OLS t 3.97, day-clustered t 2.23, 806 cases on 211 days). Outside that regime it is −0.044 (t_day −0.60, 688 cases).
- **F3:** The 28-day slope inside the low-volume regime is positive on every coin. The values are 0.065 (BTC), 0.145 (ETH), 0.106 (LTC), 0.139 (XMR), 0.073 (XRP) and 0.210 (ZEC), about 100–137 cases each. Outside the regime the 28-day slope is −0.054 (t_day −0.71), so the low-volume regime is where past moves carry on.
- **F4:** Inside the low-volume regime, only the part of the 28-day slope that comes from falls carries it. Among falls the slope is +0.241 (OLS t 2.10, t_day 1.46, 372 cases), so deeper calm falls do fall further. Among rises it is −0.001 (t_day −0.02, 347 cases).
- **F5:** The short-only book cannot capture this, because falls in the regime are mostly shallow. Over the tested cases the coin's normal drift in the short direction is −0.59 % per 5 days, which leaves a total move of −0.29 % against a 0.19 % trade cost. The 933 short trades lose −0.63 % on average, and every |entry forecast| quartile has a negative median, from −2.47 % to −1.12 %.
- **F6:** Over all bars, the 5-day move falls as the coin's recent quiet deepens. Its correlation with the 28-day/90-day range ratio is −0.141 (t −2.90, n 414), and with the 28-day/90-day volume ratio it is −0.118 (t −2.42, n 414). The lowest volume-ratio quintile is followed by +0.368 usual moves (t 2.86, n 84, +5.0 %). These cases were not clustered by day and come from a small sample.
- **F7:** Most other angles showed nothing beyond chance, given how many were tried:

## Ideas
- `032-03.b2.b2.g1_thin-volume-two-week-momentum` (from F1, F2, F3, F5): In a coin whose volume over the past 28 days is below its usual volume, the higher its 14-day return, the higher its return over the next 5 days, so recent gains and recent losses both continue more the larger they were.
- `032-03.b2.b2.g2_deep-quiet-precedes-rise` (from F6): The more a coin's daily high-low ranges over the past 28 days have shrunk compared with its ranges over the past 90 days, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
