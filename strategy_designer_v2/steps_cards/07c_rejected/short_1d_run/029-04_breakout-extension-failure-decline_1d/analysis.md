---
line: 7.c rejected
backtest: 029-04_breakout-extension-failure-decline_1d
idea tested: 029-04_breakout-extension-failure-decline
step 5: rejected
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4062 USD
---
## Findings
- **F1:** The test found the opposite of the idea. Higher peak excursions were followed by higher 5-day returns, not larger falls: slope +0.0027 per excursion point, t 3.3 over 751 non-overlapping cases. The positive slope held at every horizon: t 4.3 at 1 day (1402 cases), 4.3 at 3 days (908), 4.4 at 10 days (578) and 2.1 at 20 days (422).
- **F2:** The positive excursion slope is carried partly by its tail. At 5 days its rank correlation is only 0.019 (p 0.60), and the slope falls to t 1.7 once the excursion is cut at its 95th percentile. At 1 day the effect survives on ranks (Spearman 0.081, p 0.002, winsorised t 3.9), and at 10 days it is weaker (Spearman 0.083, p 0.046, winsorised t 2.5).
- **F3:** Failed breakouts were followed on average by a small rise, not a fall. The long-signed unusual move was +0.19 % at 5 days (t 0.52, 751 cases) and +0.94 % at 10 days (t 1.29, 578 cases). This was not stable across years: 2019 was −2.8 % (t −2.7, 83 cases) and 2020 was +2.5 % (t 3.2, 117 cases).
- **F4:** Among failed breakouts, the further the close sat below its highest close of the prior 20 days, the higher the return that followed. The slope on that depth was −0.15 at 1 day (t −5.0, Spearman −0.12, p 0.00003, 1190 cases) and −0.39 at 3 days (t −5.5, Spearman −0.11, p 0.002, 766 cases). It faded at 5 and 10 days (Spearman p 0.39–0.40).
- **F5:** Plain closes above the prior 20-day closing high were followed by rises well above the coin's drift. The unusual move was +0.93 % at 3 days (t 3.4, 1018 cases), +1.34 % at 5 days (t 3.1, 799 cases) and +2.99 % at 10 days (t 3.6, 558 cases). The 10-day total move was +4.2 %, about 22 times the 0.19 % cost of a trade.
- **F6:** Those breakout rises grew with how far the close cleared the old high, measured in units of the coin's 20-day daily volatility. At 5 days the quintiles went from +0.23 % (lowest) to +2.1 % and +2.2 % (top two, t 2.4 and 2.0, about 160 cases each). The linear slope was t 1.9 at 5 days and t 2.5 at 10 days, but ranks are weaker (Spearman 0.04–0.05, p about 0.28).
- **F7:** The failed-breakout 5-day result splits by coin. ETH (+1.28 %, t 1.3, 127 cases) and ZEC (+1.06 %, t 0.8, 113 cases) rose after failures, while BTC fell (−0.70 %, t −1.2, 143 cases). Failures in the highest third of 20-day volatility rose +1.46 % (t 1.6, 211 cases) against −0.69 % in the lowest third (t −1.4, 211 cases).

## Ideas
- `029-04_breakout-extension-failure-decline.c1_breakout-extension-carries-higher` (from F5, F6, F3): When a coin closes above its highest close of the prior 20 days, it rises more than its normal drift over the next 10 days, and the further the close clears that old high, measured in units of the coin's 20-day daily volatility, the larger the rise.
- `029-04_breakout-extension-failure-decline.c2_failed-breakout-dip-rebounds` (from F4, F3, F1): When a coin has closed above its prior 20-day closing high within the last 4 days and now closes back below that old high, it rises over the next 3 days, and the further its close sits below its highest close of the prior 20 days, the larger the rise.
- `029-04_breakout-extension-failure-decline.c3_big-excursion-failure-bounces` (from F1, F2): When a coin closes above its prior 20-day closing high, reaches further above it within the next 3 days, and then closes back below the old high, the coin rises over the next day, and the larger the peak excursion above the old high was, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
