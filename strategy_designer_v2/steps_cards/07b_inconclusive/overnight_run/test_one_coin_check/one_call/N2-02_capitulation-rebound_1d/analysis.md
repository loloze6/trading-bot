---
line: 7.b inconclusive
backtest: N2-02_capitulation-rebound_1d
idea tested: N2-02_capitulation-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4327 USD
---
## Findings
- **F1:** The 69 non-overlapping cases with forecast >= 10 have a mean 10-bar excess return of +2.06% (t 0.90) but a median of -1.60% and a hit rate of 48%; their spread (std 0.19) is larger than that of all bars (0.16), so a few large rebounds (XRP mean +11.9% on 11 cases, median -1.9%) carry a mean that most cases do not share.
- **F2:** The market's own move dominates the outcome: the top cases where BTC rose over the same 10 bars average +11.6% excess (t 3.39, n 37, 81% hits), while those where BTC fell average -8.9% (t -6.12, n 32, 9% hits); the coin's and BTC's forward returns correlate at 0.59.
- **F3:** The cases are clustered in time, and one window weighs on the result: the 69 cases fall on only 46 distinct dates (date-clustered t 0.75), and w2 (2022) alone holds 28 cases averaging -1.4% (t -0.53); without w2 the 41 remaining cases average +4.4% (t 1.29, median +0.9%).
- **F4:** The effect sits on bars whose close is still falling: forecast >= 10 cases with a negative 5-bar return average +3.6% (t 1.26, n 50, hit 52%), against -1.9% (n 19, hit 37%) after a positive 5-bar return; at forecast >= 5 the same split gives +2.9% (t 1.36, n 74) against -1.5% (n 38).
- **F5:** The rebound is strongest when the close is at its 10-bar low: such top cases average +6.9% (median +3.2%, hit 58%, n 19), against +0.3% (median -2.4%) for the 45 cases that are not at the low.
- **F6:** Depth itself does not order the outcome: within the top cases, terciles of the distance below the 200-day SMA give +5.5%, -3.4% and +4.1%, and the in-regime buckets rise only weakly (from -2.2% at forecast 2 to 5 up to +1.6% at 15 to 20, none with |t| > 1.6).

## Ideas
- `N2-02_capitulation-rebound.b1_capitulation-at-fresh-low` (from F4, F5, F1): When a coin's close is far below its 200-day average during high volatility, and that close is also its lowest close of the last 10 days after a falling 5-day return, the coin's price rises over the next 10 days by more than its normal drift.
- `N2-02_capitulation-rebound.b2_first-deep-plunge-only` (from F3, F1): When a coin's close is far below its 200-day average during high volatility, the coin's rise over the next 10 days is larger in a period whose deep-drawdown signals do not keep recurring on consecutive checks, that is when the coin was not already this deep below its average 10 days earlier.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
