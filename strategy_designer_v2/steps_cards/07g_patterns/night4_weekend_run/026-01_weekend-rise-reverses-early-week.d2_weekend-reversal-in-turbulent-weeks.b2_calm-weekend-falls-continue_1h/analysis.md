---
line: 7.g patterns
backtest: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b2_calm-weekend-falls-continue_1h
idea tested: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b2_calm-weekend-falls-continue
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5055 USD
---
## Findings
- **F1:** The two hours from 21:00 to 23:00 UTC (the close of the 20:00 bar to the close of the 22:00 bar) end higher in every coin. The mean rise is +0.08 % to +0.13 % per coin, with t from 2.83 to 4.73 (1,804 to 2,878 days per coin). It is positive in 7 of 8 years, with 2022 the exception at −0.04 % (t −1.16), on every weekday (t 1.70 to 4.34), and in 76 % of 144 coin-windows. The bars starting at 21:00 and 22:00 are the strongest of all 24 hours (t 6.87 and 5.76), clear of what testing 24 hours would produce by chance.
- **F2:** That 21:00–23:00 rise is largest after a 24-hour fall. In the lowest quintile of the prior 24-hour return (mean −5.97 %) it is +0.22 %, against +0.06 %, +0.06 % and +0.01 % in the next three quintiles and +0.13 % in the highest. It also grows with volatility: +0.05 %, +0.04 %, +0.09 % and +0.18 % by quartile of 30-day volatility. Only the largest-fall and highest-volatility cells exceed the 0.19 % cost of a trade.
- **F3:** The book's 884 trades, all shorts entered on Sunday, lost −0.46 % gross and −0.56 % net on average. This is against the +0.63 % total move per case measured for the idea. Entries with forecast between −5 and −2 were held 154 hours on average and lost −0.77 % gross. ZEC alone lost −1.55 % gross per trade. So the book does not capture the confirmed move: it takes weak signals below the band and holds them far past the 48-hour horizon.
- **F4:** The continuation after a weekend move is not confined to calm weeks. The slope of the next 48 hours on the standardised weekend return is t 3.26 in the lowest volatility-rank tercile (634 Mondays), t −0.38 in the middle tercile (248) and t 2.43 in the highest (489). It is unstable across years: t 3.55, 2.37, 2.33 and 3.19 in 2020 and 2022–2024, but negative in 2021 (−0.72) and 2025 (−1.55).
- **F5:** The largest weekend falls are followed by a rise, not a continuation. In the lowest quintile of the standardised weekend return (mean z −0.86), Monday gains +0.69 % and the 48 hours +0.44 % beyond drift. The second quintile falls a further −0.93 % and −0.86 %. Likewise, falls in the highest volatility tercile are followed by +0.45 % over 48 hours, against −1.09 % in the lowest tercile.
- **F6:** Coins rise on Saturday and Friday (UTC days). Saturday averages +0.45 % (t 5.53, 2,484 coin-days) and is positive in all six coins (t 1.40 to 2.92). Friday averages +0.33 % (t 3.51). In 2022 and 2023 the Saturday rise is near zero (t 0.42 and −0.01).

## Ideas
- `026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b2_calm-weekend-falls-continue.g1_late-evening-rebound-after-falls` (from F1, F2): The larger a coin's fall over the 24 hours to 21:00 UTC, the larger its rise over the next 2 hours, from 21:00 to 23:00 UTC.
- `026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b2_calm-weekend-falls-continue.g2_evening-rise-grows-with-volatility` (from F1, F2): The higher a coin's 30-day hourly volatility, the larger its rise over the 2 hours from 21:00 to 23:00 UTC.
- `026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b2_calm-weekend-falls-continue.g3_outsized-weekend-falls-rebound-monday` (from F5, F4): The larger a coin's fall from Saturday 00:00 to Monday 00:00 UTC, measured against its 30-day hourly volatility, the larger its rise over Monday (the next 24 hours), once that fall is large against its usual weekend move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
