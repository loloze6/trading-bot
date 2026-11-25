---
line: 7.g patterns
backtest: 039-02_range-scaled-fall-rebound_1d
idea tested: 039-02_range-scaled-fall-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4246 USD
---
## Findings
- **F1:** Across all days, the drop from the day's high to its close, divided by the coin's 30-day mean daily high-to-low range, predicts the next-day excess return better than the tested close-to-close fall. The pooled slope is +0.0097 with a day-clustered t of 2.84 (7,321 cases on 1,221 days). Using the high-to-close drop minus the low-to-close recovery, the slope is +0.0070 with t 3.12.
- **F2:** The gain sits in the largest drops from the high. Ranking all days by the scaled high-to-close drop, the top quintile earns +0.78 % next-day excess (t 2.58, 468 days), while quintiles 0 to 3 earn -0.20 % to -0.25 % (t -0.9 to -1.4). On down days alone the top quintile earns +1.16 % (t 2.77, 236 days) against +0.06 % in the bottom quintile.
- **F3:** On the same down days, the scaled high-to-close drop has a slope of 0.0118 with t 2.68. The tested close-to-close scaled fall has a slope of 0.0105 with t 1.85 (3,624 cases, 885 days). Among the largest scaled falls, closing near the low rebounds +1.32 % (t 2.07, lowest close-location tercile), but closing near the high rebounds only +0.38 % (t 0.67).
- **F4:** The high-to-close slope is positive in all 12 windows w7 to w18, ranging from +0.0022 to +0.0230; w10 has t 4.27 and w16 has t 2.68. The pattern is not carried by one period.
- **F5:** The rebound is concentrated when the coin is agitated. On down days with the 30-day swing above its recent median, the high-to-close slope is 0.0162 (t 2.23, 332 days), against 0.0048 (t 1.21, 434 days) when calm. The tested scaled fall gives 0.0170 (t 1.54) agitated against 0.0021 (t 0.44) calm. The largest scaled falls on high-range coins rebound +1.50 % (t 2.32), against +0.38 % (t 0.89) on low-range coins.
- **F6:** Other angles showed nothing that stands out once the number of angles looked at is counted:

## Ideas
- `039-02.g1_intraday-high-to-close-selloff-rebound` (from F1, F2, F3, F4): After a day on which a coin closes well below that day's high, the coin rises over the next day, more so the larger the drop from the day's high to its close measured in units of its 30-day average daily high-to-low range.
- `039-02.g2_agitated-high-to-close-selloff-rebound` (from F5, F1, F2): In an agitated market, after a day on which a coin closes well below that day's high, the coin rises over the next day, more so the larger the drop from the day's high to its close measured in units of its 30-day average daily high-to-low range.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
