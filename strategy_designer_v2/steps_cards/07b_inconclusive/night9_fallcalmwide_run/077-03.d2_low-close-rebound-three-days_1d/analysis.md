---
line: 7.b inconclusive
backtest: 077-03.d2_low-close-rebound-three-days_1d
idea tested: 077-03.d2_low-close-rebound-three-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2245 USD
---
## Findings
- **F1:** The test measured the rebound over three days, but in folds B and C it is spent after one day. On the 122 replicated cases (89 days), the mean excess return was +0.88 % (t 1.23) over the next day, -0.11 % (t -0.09) over two days and +0.28 % (t 0.23) over three days, so days two and three give back the first day's rise. This dilution is why step 5's three-day mean (-0.39 %, t -1.07, 419 days) is negative and unclear.
- **F2:** The one-day rebound grows with the forecast and shows in its strongest cases. By forecast quartile, the next-day excess return rises from -2.31 % (t -1.83) to +0.33 %, +1.63 % and then +3.85 % (t 2.46, 31 cases, 26 days). Over three days the same quartiles give -3.61 %, -0.59 %, +4.55 % and +0.89 %, which is not monotonic.
- **F3:** Across every profile day (one-day grid, 397 days), the next day's excess return falls steadily as the close moves up the range. The quintile of closes nearest the low (mean close position -0.75) is followed by +1.65 % (t 2.40, 56 days), the middle quintile by -0.37 % and the top two by -1.18 % and -0.90 %. The rank correlation between the idea's product (close position × width) and the next-day return is -0.15, against -0.10 for the three-day return on its grid.
- **F4:** The rebound is larger on wide days, as the idea grades it. On days wider than the median against their 30-day swing, the lowest-close quintile is followed by +2.39 % the next day (t 2.42, 37 days), compared with +1.65 % for all widths.
- **F5:** The three-day result is mixed across periods, which fits a horizon too long for the effect. By year it was +3.9 %, -2.2 %, -3.1 % and +3.0 % in 2018 to 2021. By window it was positive in w11 to w14 (for example w12 +6.5 %, t 1.95) and negative in w15 to w17. No coin stands out: ZEC +1.1 % and XMR +0.7 %, against ETH -3.2 % and BTC -1.8 %.

## Ideas
- `077-03.d2.b1_low-close-rebound-next-day` (from F1, F2, F3, F4, F5): In a choppy, agitated market, a day closing below the middle of its range is followed by a rise over the next day, larger the further the close sits below the middle, multiplied by the day's range against its 30-day swing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
