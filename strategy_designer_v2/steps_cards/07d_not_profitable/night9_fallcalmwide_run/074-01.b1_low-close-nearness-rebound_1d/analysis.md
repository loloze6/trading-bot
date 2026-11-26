---
line: 7.d confirmed, not profitable
backtest: 074-01.b1_low-close-nearness-rebound_1d
idea tested: 074-01.b1_low-close-nearness-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4117 USD
---
## Findings
- **F1:** The check failed only on how often the book trades: 0.00945 trades per day against the 0.01 required, with positions on 2 % of the coins' days. Every gain and fall measure passed (Sharpe 1.05, Calmar 1.16, +0.47 % a day in a position). On folds B and C the tested situation (range ≥ 2 of the 30-day swing, close in the bottom quarter, rising calm) gave only 75 cases on 44 days and 87 active bars among 9,986 coin-bars, so the book is rare, not losing.
- **F2:** A broader case of the same situation carries the same effect at about three times the count. In the rising calm profile, a range of at least 1.5 swings with a close in the lower 40 % of the range gave 221 cases on 122 days, with a next-day unusual move of +1.49 % (t 3.14). The 146 of those cases outside the tested thresholds still gave +1.19 % (t 2.43). That case rate (about 2.9 × 0.0095 ≈ 0.027 trades per day) would clear the 0.01 rule.
- **F3:** The profile is not an effect of its own. Rising calm bars without the signal earn +0.23 % the next day (t 1.06, 1,921 bars), against +1.49 % where both hold. Rising agitated bars with the broad signal earn only +0.26 % (t 0.31, 141 cases). This fits the brief's theory that dip-buyers repay the overshoot only in a calm uptrend.
- **F4:** The effect switches on once the close is in the lower ~40 % of the range, and it is not graded by nearness to the low beyond that point. For days of at least 1.5 swings in profile, the next-day move was:
- **F5:** The day's width grades the rebound better than the close does, up to about 3 swings. Among in-profile days closing in the lower 40 %:
- **F6:** The broad case is not one period's effect:

## Ideas
- `074-01.b1.d1_wide-lower-close-calm-rebound` (from F1, F2, F3, F4, F5, F6): In a rising, calm market, a day whose high-to-low range is wide against the coin's 30-day swing of daily returns and that closes in the lower part of its range is followed by a rise over the next day; the wider the day against that swing, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
