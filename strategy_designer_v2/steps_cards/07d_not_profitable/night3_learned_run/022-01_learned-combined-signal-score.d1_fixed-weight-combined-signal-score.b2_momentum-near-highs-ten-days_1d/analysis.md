---
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days_1d
idea tested: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4486 USD
---
## Findings
- **F1:** Only the long side pays. On 8,544 long bars the book earns +8.2 bps a day (t 4.7), of which +4.7 is timing. On 8,640 short bars it earns −0.7 bps (t −0.58): their +1.9 bps of timing is more than eaten by −2.7 bps of the coins' own rise. Counting the long bars alone gives 4.0 bps a day per coin-bar, against 3.65 for the whole book.
- **F2:** Almost all the gain comes from the strongest forecasts. The top forecast quintile (mean forecast 8.2) earns +17.6 bps a day (t 4.5), while the other four earn between −1.7 and +2.2 bps. On the 10-day grid, the top three deciles end +1.5 % to +2.1 % above drift (169 cases each). The middle is not graded: decile 6 ends −1.27 % and decile 0 ends −0.39 %.
- **F3:** Two of the book's deepest falls came while the coins rose.
- **F4:** Shorts taken deep below the 90-day high lose. The deepest quartile (mean −54 % below the high) earns −4.3 bps a day (t −1.48). The quartile at −23 % earns +3.2 bps.
- **F5:** Shorts taken after a rise over the last week lose. The quartile with the highest 7-day return (mean +11.8 %) earns −4.0 bps a day (t −2.07, 2,039 bars). The quartile at −4.5 % earns +3.1 bps.
- **F6:** Longs are graded by nearness to the high and by the 4-week rise.
- **F7:** Costs are not the cause. Allocation turnover is 272 bps a day per coin. The gain before costs (3.65 bps) is barely above the book's 3.43 bps. The move per case is 7.9 times the 0.19 % cost of a trade.
- **F8:** The book lags holding in bull windows. It earns in 15 of 24 windows, but in w11 it made +7.4 % against holding's +281 %, and in w21 +19 % against +87 %.

## Ideas
- `022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days.d1_momentum-near-highs-upside-only` (from F1, F2, F6, F8): The higher a coin's 28-day return plus its closeness to its 90-day high, the higher its return over the next 10 days, the rise above the coin's usual drift growing with how far both stand above their usual level.
- `022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days.d2_momentum-near-highs-rebound-exception` (from F3, F4, F5): The higher a coin's 28-day return plus its closeness to its 90-day high, the higher its return over the next 10 days, except when the coin stands far below its 90-day high after rising over its last 7 days: there, the deeper it stands below that high and the larger its 7-day rise, the higher its return over the next 10 days.
- `022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days.d3_rebound-from-deep-drawdown` (from F3, F4, F5): The deeper a coin stands below its 90-day high and the larger its 7-day return, the higher its return over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
