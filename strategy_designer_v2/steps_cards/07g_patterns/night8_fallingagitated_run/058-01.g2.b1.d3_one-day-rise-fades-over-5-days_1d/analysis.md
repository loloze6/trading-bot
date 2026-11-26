---
line: 7.g patterns
backtest: 058-01.g2.b1.d3_one-day-rise-fades-over-5-days_1d
idea tested: 058-01.g2.b1.d3_one-day-rise-fades-over-5-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6171 USD
---
## Findings
- **F1:** Outside the falling, agitated profile, a large one-day rise is followed by a further rise, not a give-back. On up days the 5-day unusual move grows with the rise in 30-day standard deviations (clustered slope +0.022 per unit, t 2.02, 643 cases), and after rises above 2 deviations it averages +7.9 % (t 2.35, 41 cases on 30 days).
- **F2:** The continuation lives in calm markets, and it is graded there. On calm up days the 5-day unusual move climbs from +2.6 % for rises of 0 to 1 deviation, to +6.2 % for 1 to 1.5 (t 1.74, 18 days), and to +8.1 % above 2 (t 4.00, 13 days). Calm rises above 1 deviation have a mean strength of 0.51 of a usual 5-day move (t 3.26, 71 cases on 23 days), far above the cost of 0.22 % a trade.
- **F3:** Within calm markets the gradient is strongest in choppy ones and absent in rising ones. The slope on z1 is +0.094 in choppy calm (t 3.27, 35 cases), +0.012 in falling calm (t 0.78) and -0.009 in rising calm (t -0.45). Rises above 1 deviation are followed by +10.1 % in choppy calm (t 2.15, 13 days) against +1.7 % in rising calm (t 0.79).
- **F4:** The calm-market continuation points the same way in every year of folds B and C. The slope is +0.016, +0.013, +0.023 and +0.009 in 2018, 2019, 2020 and 2021, and rises above 1 deviation are followed by +2.4 %, +10.9 % and +8.1 % in 2019, 2020 and 2021. The cases are few (23 days in all), so the size is uncertain.
- **F5:** In agitated markets up days show no reliable gradient. The 5-day unusual move after rises of 0.5 to 1 deviation is -4.2 % (t -2.70, 15 days), but after 1.5 to 2 deviations it is +4.5 % (t 0.57). The 2-day slope on up days is -0.0005 (t -0.06). The tested give-back is therefore not graded in the bars, matching its inconclusive t of 1.16.
- **F6:** The tested book's losses are spread across coins rather than concentrated in one. Mean trade results after fees are negative on 7 of 10 coins: XRP -10.6 % over 53 trades, DOGE -9.3 % over 10, ADA -4.6 % over 30 and BTC -2.7 % over 81. The positive coins, LINK (+9.4 %, 10 trades) and TRX (+8.6 %, 11 trades), have few trades.
- **F7:** No weekday pattern survives grouping cases by day. Tuesday in the profile reads +1.25 % next day with t 3.13 unclustered, but only t 1.66 over 73 days, and no weekday over all bars exceeds |t| 1.44. It is not a finding.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `058-01.g2.b1.d3.g1_calm-chop-rise-continues` (from F1, F2, F3, F4): In a choppy, calm market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the larger its further rise over the next 5 days.
- `058-01.g2.b1.d3.g2_calm-market-rise-continuation` (from F1, F2, F4): In a calm market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
