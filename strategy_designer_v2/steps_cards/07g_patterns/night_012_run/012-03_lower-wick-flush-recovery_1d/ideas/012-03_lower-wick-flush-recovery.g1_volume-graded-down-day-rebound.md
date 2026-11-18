---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-03_lower-wick-flush-recovery
line: 7.g patterns
backtest: 012-03_lower-wick-flush-recovery_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a day a coin closes lower, the larger that day's volume relative to its prior 20-day mean volume, the larger the coin's rise over the next 3 days.
Consequence: A down day on heavy volume relative to the coin's recent norm is a reason to buy for a few days, sized by how extreme the volume is, rather than to wait for a long lower wick.
Why:
- F1: Across all falling days (z ≤ -1, thinned to one case per 3 days), the 3-day excess return rises with the day's volume ratio: OLS slope on log volume ratio 0.0096, t 2.53, n 1419. The volume-ratio 2–3 bucket gains +2.12% (t 3.29, n 174), while ratios below 1.5 sit near zero (+0.21% t 0.54 n 489; -0.33% t -0.93 n 448).
- F2: The rebound after volume-burst falls holds in both halves of the sample, at +1.68% (t 1.94, n 141) up to 2021 and +1.86% (t 2.86, n 118) after. Sharp falls without the burst show no rebound: z in (-3,-2] with volume ratio below 2 gives -0.85% over 3 days (t -0.95, n 75), against +2.12% (t 1.80, n 39) with the burst.
- F3: The wick, which the tested idea relied on, does not grade the rebound. The verdict's slope t was 0.77 on 223 flush bars. Among volume-burst sharp falls, closes nearest the low (close location 0–0.2) had the largest 3-day excess, +1.87% (t 2.21, n 83, not thinned), against +0.62% (t 0.57, n 77) for 0.2–0.4 and +0.88% (t 0.76, n 32) for above 0.4.
