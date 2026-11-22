---
line: 7.g patterns
backtest: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks_1h
idea tested: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4578 USD
---
## Findings
- **F1:** Weekend moves continue rather than reverse. On the 00:00 UTC grid, Monday's next 48-hour return rises with the weekend's 48-hour return, each standardised by the coin's 30-day hourly volatility: slope +0.119, t 3.65, 2228 cases. After a weekend rise, Monday and Tuesday returned +0.39 %; after a weekend fall, −0.26 %. The same slope at the other weekday points is between +0.006 and +0.058.
- **F2:** The continuation sits in calm weeks. In the lowest tercile of each coin's 30-day hourly volatility, a weekend rise was followed by +0.84 % over Monday and Tuesday (t 2.93, 426 cases) and a weekend fall by −0.70 % (t −2.14, 317 cases), with a slope of +0.34. In the highest tercile, a weekend rise was followed by only −0.27 % (t −0.59, 385 cases) and the slope was +0.125, still not a reversal. This fits step 5's failed size check: the larger half minus the smaller half was −0.0008.
- **F3:** The weekend continuation is not monotone in the weekend's size. By quintile of the standardised weekend move, the next 48-hour return was +0.43 %, −0.60 %, −0.30 %, +0.39 % and +0.53 % (about 445 cases each), so it shows mainly in the top quintile of weekend rises.
- **F4:** The continuation is strongest in XRP and BTC. Their Monday slopes were +0.285 (t 3.47, 381 cases) and +0.202 (t 2.05, 380 cases), against 0.004 to 0.144 for XMR, LTC, ZEC and ETH.
- **F5:** The book lost on its trades. All 894 trades were shorts, with a mean of −1.13 % before fees and −1.23 % after, every coin negative (−0.41 % for LTC to −2.14 % for ETH). The median holding was 48 hours, but 25 % of trades lasted at most 1 hour and one was held 2880 hours, so the book was not the clean 48-hour fade whose per-case total move was +0.57 %.
- **F6:** A large 1-hour fall partly rebounds the next hour, and the effect is graded. By decile of the 1-hour return standardised by 30-day volatility, the next hour returned +0.070 % (t 9.1), +0.029 % (t 5.3) and +0.013 % (t 2.8) in the three lowest deciles, about 38,800 hours each. This is far below the 0.19 % cost of a trade.
- **F7:** Hourly returns have strong clock patterns, read across many angles and with coins pooled, so the t values are inflated. Saturday hours averaged +0.027 % per hour (t 7.2, against −0.004 % to +0.015 % on the other days). The hours closing at 22:00 and 23:00 UTC averaged +0.055 % (t 6.9) and +0.044 % (t 5.8), about 17,400 hours each.

## Ideas
- `026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.g1_calm-weekend-moves-carry-on` (from F1, F2, F3, F4): A coin's move from Saturday 00:00 to Monday 00:00 UTC carries on in the same direction over the next two days (Monday and Tuesday) while the coin's 30-day hourly volatility is low against its own last 6 months. The larger the weekend move, measured against that volatility, the larger the move that follows in its direction.
- `026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.g2_strong-weekend-rally-extends` (from F1, F3): The larger a coin's weekend rise from Saturday 00:00 to Monday 00:00 UTC, measured against its 30-day hourly volatility, the larger its rise over the next two days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
