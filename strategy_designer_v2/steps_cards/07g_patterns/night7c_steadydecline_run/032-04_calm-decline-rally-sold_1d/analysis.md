---
line: 7.g patterns
backtest: 032-04_calm-decline-rally-sold_1d
idea tested: 032-04_calm-decline-rally-sold
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3661 USD
---
## Findings
- **F1:** In a calm 28-day uptrend (28-day return above 0, 28-day mean daily range no wider than its 120-day mean), the 5-day unusual move rises with the size of the day's return measured against its 60-day daily standard deviation. The slope is 0.022 per standard unit (t 3.47, 398 non-overlapping cases). By quintile of that day's move, the unusual move climbs steadily: -2.32 % (t_day -1.63, 41 days), -0.85 %, +1.81 %, +2.26 %, +3.24 % (t_day 2.21, 39 days).
- **F2:** The same calm-uptrend split holds on its own. Up days in a calm uptrend are followed by a 5-day unusual move of +2.88 % (t 3.36, 209 cases), down days by -1.44 % (t -2.07, 189 cases). The other three trend and range cells all have |t| under 1.
- **F3:** The continuation in calm uptrends also holds with the 3-day return. Its lowest quintile is followed by -3.85 % (t_day -2.48, 42 days) and its fourth quintile by +2.52 % (t_day 2.53, 49 days). The direction-signed move is positive on all 6 coins (+0.8 % BTC to +3.9 % XRP), in all 4 years (+0.3 % to +3.4 %) and in 9 of 12 windows.
- **F4:** The continuation is weaker when daily ranges are wide. In a wide-range 28-day uptrend the slope of the 5-day unusual move on the day's standardised move is 0.014 (t 1.54, 182 cases), against 0.022 (t 3.47) in the calm case.
- **F5:** The tested grading is absent in this data:
- **F6:** The book mostly carried a short on the coin and earned little:

## Ideas
- `032-04.g1_calm-uptrend-day-follow-through` (from F1, F2, F3, F4): When a coin is in a calm 28-day rise, with its daily ranges no wider than usual, a day's move continues in the same direction over the next 5 days. The larger that day's move relative to the coin's typical daily move over the past 60 days, the larger the follow-through.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
