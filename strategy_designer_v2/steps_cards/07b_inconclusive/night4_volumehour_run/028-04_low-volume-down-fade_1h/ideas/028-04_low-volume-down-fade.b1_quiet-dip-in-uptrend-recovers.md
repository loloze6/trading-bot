---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-04_low-volume-down-fade
line: 7.b inconclusive
backtest: 028-04_low-volume-down-fade_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin falls far more than its typical hourly move over the past 30 days while its volume stays near its average hourly volume over the past 30 days, the price recovers part of that fall over the next six hours, only while the coin's 7-day return is positive. The larger that 7-day rise, the larger the recovery.
Consequence: Buy a quiet-volume hourly drop when the coin is in a 7-day rise, more so the stronger the rise, and refuse the same drop when the coin is in a 7-day decline.
Why:
- F1: The tested recovery appears only when the coin has risen over the past 7 days. With volume at 2/3 to 1.5 times its 30-day mean and a fall of at least half a usual move, the 6-hour unusual move is +0.100 % (t 3.62, 4601 cases) after a 7-day rise, against −0.053 % (t −1.62, 4801 cases) after a 7-day fall. At 24 hours the gap widens to +0.175 % (t 3.08) against −0.303 % (t −4.66). Pooling the two regimes leaves the plan's small t of 1.40.
- F2: The 7-day-rise split holds on both coins and in most years, so it is not one coin or one period. BTC is +0.082 % (t 2.40, 2352 cases) and ETH +0.119 % (t 2.72, 2249 cases). The mean is positive in 6 of 8 years (2019 +0.184 % t 2.06, 2020 +0.147 % t 2.18, 2023 +0.095 % t 2.05, 2024 +0.137 % t 2.18), with 2022 at −0.004 % and 2025 at −0.020 %.
- F3: Within a 7-day rise, the recovery grows with the size of that rise, so the effect is graded by the trend. By 7-day-return quartile the 6-hour unusual move is −0.030 % (t −0.62), +0.113 % (t 2.35), +0.104 % (t 1.95) and +0.213 % (t 3.13), about 1150 cases each.
- F5: The same split shows over other trend lengths. A 3-day rise gives +0.105 % (t 3.95, 4663 cases) against −0.059 % (t −1.77) after a 3-day fall. A 30-day rise gives +0.106 % (t 3.69, 3938 cases) against −0.038 % (t −1.26).
- F6: The pooled result is dragged down by falls inside declines, most of all in 2022. Quiet-volume falls after a 7-day fall averaged −0.298 % (t −3.50, 686 cases) that year. Across all such downtrend cases, small falls of 0.5–1 usual moves gave −0.142 % (t −2.78, 1899 cases).
- F7: The strongest trend quartile's move (+0.213 % over 6 hours) is about twice the 0.11 % cost of a trade. The tested idea's pooled total move was +0.07 %, 0.7 times that cost. Restricting to rises could make a book pay where the pooled idea cannot. This is a reading of F3 against the stated cost; I did not test whether the higher 6-hour moves after rises are just the coin's ongoing drift.
