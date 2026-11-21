---
line: 7.e profitable but not proven
backtest: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs_1d
idea tested: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4246 USD
---
## Findings
- **F1:** The book earns on its long side. Long bars give 10.54 bps per day of the book's 10.47 gross, and short bars give −0.08. By trade, long trades sum to +16,726 % (1,792 trades) and short trades to −1,486 % (1,238). Short trades entered more than 30 % below the 60-day high lose −1,906 % (mean −5.0 %, 33 % winners).
- **F2:** The gain comes from a few long trends. The top 5 % of the 3,030 trades make 110 % of the net sum, and 45 % of trades win. The top 30 long trades make 59 % of the long sum and fall in only 5 windows. Of those 30, 25 are XRP (14) or ZEC (11), and their median hold is 42 days.
- **F3:** The market's own rise is a minor part of the gain: 2.73 of the 10.47 bps per day gross, with 7.74 bps of timing. Timing is spread over the years but turns negative in 2022 (−0.41) and 2023 (−1.21). By window, gross gain runs from −0.43 to +1.99 bps, and 8 of 24 windows lose.
- **F4:** The book earns where the coin is near its 60-day high, and the 10-day move falls in step with the distance below it. Long contribution is 3.24, 2.84, 2.08, 0.60 and 0.45 bps per day from "at the high" to "more than 30 % below". Over the next 10 days, on the non-overlapping grid, the excess return is +2.08 % (n 122), +1.67 % (194), +0.39 % (399), −0.96 % (376) and −0.70 % (312). Nearness alone has a slope t of 1.63 (n 1,403).
- **F5:** The test measured a standardised forecast, and that hides the idea. On the 10-day grid, the forecast has a slope t of 1.01 and the recorded component, standardised against its own past 60 values, 1.04. The plain level of the 28-day return times (1/(1+D))² has a slope t of 2.69 (n 1,259), above the 28-day return alone (t 2.29).
- **F6:** Among coins whose 28-day return is positive, nearness to the 60-day high grades the next 10-day move (t 1.69, n 644). The largest cell is the top quarter of 28-day returns at the high: +4.36 % excess over 10 days (n 79).
- **F7:** At shorter horizons the forecast predicts better than at the plan's 10 days, and the move fades beyond it. Slope t is 2.17 at 1 day (n 17,380), 2.12 at 3 days (n 5,723) and 1.09 at 10 days (n 1,691). It is near zero at 20 and 30 days (0.01 and 0.61). The 3-day signed excess return is 0.23 %, barely above the 0.19 % cost of a round trip, while the 10-day unusual move of 1.37 % is 7.1 times that cost.

## Ideas
- `022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs.e1_momentum-level-near-highs` (from F1, F4, F5, F6): The higher a coin's 28-day return multiplied by its nearness to its 60-day closing high (the closer to the high, the larger the weight), the higher its return over the next 10 days.
- `022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs.e2_nearness-to-60-day-high` (from F1, F3, F4): The closer a coin's close is to its highest close of the last 60 days, the higher its return over the next 10 days.
- `022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs.e3_rising-coins-near-highs` (from F1, F2, F6): While a coin's 28-day return is positive, the closer its close is to its 60-day closing high, the larger its return over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
