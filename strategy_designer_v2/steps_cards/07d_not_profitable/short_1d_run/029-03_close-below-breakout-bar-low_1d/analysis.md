---
line: 7.d not profitable
backtest: 029-03_close-below-breakout-bar-low_1d
idea tested: 029-03_close-below-breakout-bar-low
step 5: not observable
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3170 USD
---
## Findings
- **F1:** The book trades far too rarely to pay. Its forecast was short on only 63 bars, and it held a position on only 1.76 % of days (257 position-bars across 6 coins × 24 windows). That gives 0.005 trades a day against the required 0.01, and a mean daily return of 0.0052 % against the coins' 0.119 %. That gap is why both the mean-return check and the check against holding fail.
- **F2:** The 91 short trades lost 0.49 % each after fees and 0.39 % before, won 36 % of the time, and lasted 3.6 days on average. Yet the 50 recorded episodes were followed by mean coin returns of +0.03 % over 1 day, −0.83 % over 3 days, −2.24 % over 5 days and −1.53 % over 10 days. The episodes' fall comes on days 3–5, and the trades do not capture it.
- **F3:** Recomputed from prices, the tested situation is a 20-day high, a 3-day failure and a close below the breakout day's low. It gave 46 non-overlapping 5-day cases with an unusual move of +0.09 % (t 0.06). All twelve variants of lookback (10 or 20 days), failure window (3, 5 or 10 days) and reference level (breakout low or old high) stay between −0.31 % and +0.62 %, with |t| ≤ 0.81 on 46 to 656 cases. The depth's Spearman with the outcome sits between −0.13 and +0.08 in every variant.
- **F4:** On the broader situation, 256 cases of a close back below the old 20-day high within 10 days of a breakout, the 5-day short outcome depends on the 20-day run-up into the breakout. The low run-up tercile gained +0.78 % (t 0.71, 87 cases), the middle −0.35 % and the high tercile −2.28 % (t −2.30, 86 cases). The overall Spearman is −0.149: after a big run-up, the failure is followed by a fresh rise.
- **F5:** In those same 256 cases, the coin's 20-day volatility grades the outcome the same way. The calm tercile gained +1.01 % (t 1.14), the middle −1.33 % and the volatile tercile −1.55 % (Spearman −0.11). The depth below the old high does not grade it at all: the terciles gave −0.48 %, −0.79 % and −0.59 %, with Spearman −0.007.
- **F6:** The book's falls and weak Calmar (0.21) follow from shorting into rising coins. Over 60 days, the strongest tercile of prior returns gave the short −1.16 % per case and the weakest −0.03 %. The losing shorts sit where the coin was already trending up.

## Ideas
- `029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up` (from F4, F6, F3): When a failed breakout above the prior 20-day high ends with a daily close below the low of the breakout day, the coin falls over the next 5 days, and the smaller the coin's 20-day rise into the breakout day, the larger the fall.
- `029-03_close-below-breakout-bar-low.d2_return-below-old-high-unstretched` (from F1, F4, F5): When a coin closes back below its prior 20-day high within 10 days of first closing above it, the coin falls over the next 5 days, and the smaller its 20-day return into the breakout day, the larger the fall.
- `029-03_close-below-breakout-bar-low.d3_failed-breakout-in-calm-coin` (from F5, F1): When a coin closes back below its prior 20-day high within 10 days of first closing above it, the coin falls over the next 5 days, and the lower the coin's 20-day volatility of daily returns, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
