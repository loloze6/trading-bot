---
line: 7.b inconclusive
backtest: 068-02_falling-agitated-run-break-fade_1d
idea tested: 068-02_falling-agitated-run-break-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 3.6359 USD
---
## Findings
- **F1:** The test's result points the way the idea predicts but falls short of the bar: the slope of the next-day move on the run length is -0.0023 with day-clustered t -1.00 over 759 cases on 387 days. On folds B and C the same slope within the active cases is -0.0040 with clustered t -1.22 (353 cases, 160 days).
- **F2:** The level of the effect is clear even though its gradient is not: the mean short-side unusual move is +0.94 % per case (t 3.26, 387 days), 0.204 of a usual move, and the total move is 4.2 times the 0.19 % cost of a trade.
- **F3:** The effect is present on every coin and in every year shown. On folds B and C the active mean short move per coin is 1.38 % to 1.54 % (t 1.92 to 2.72, 45 to 78 cases). By year it is 2018 +2.09 %, 2019 +1.44 %, 2020 +1.35 %, 2021 +0.82 %. It is not confined to one part of the data.
- **F4:** The grading is noisy rather than absent: the mean next-day short move by run length is 1 day +0.94 % (201 cases, t 1.60), 2 days +2.93 % (92, t 3.03), 3 days -0.61 % (39, t -0.54) and 4+ days +3.46 % (27, t 3.00). The long runs that carry the slope number only 66 cases, too few to fix it.
- **F5:** When up days after rises (run 0) are included as the baseline, the gradient does show:
- **F6:** The plan's standardised forecast mostly separates 1-day runs from longer ones, because most past values are 0 and runs of 2 days or more sit at the -20 cap. Its book earns its gain from that level (Sharpe 0.74, +6.7 % a year, 9 % of coin-days in a position) and fails only on Calmar (0.36). The direction is right; what is missing is cases in the long-run tail.

## Ideas
- `068-02.b1_run-break-fade-more-coins` (from F1, F3, F4, F5): In a falling, agitated market, on a day that closes up, the longer the unbroken run of down days that ends just before it, the larger the coin's fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
