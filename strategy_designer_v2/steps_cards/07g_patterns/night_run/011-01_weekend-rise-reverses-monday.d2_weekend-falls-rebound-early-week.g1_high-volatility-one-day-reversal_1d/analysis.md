---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g1_high-volatility-one-day-reversal_1d
idea tested: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g1_high-volatility-one-day-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3342 USD
---
## Findings
- **F1:** The reversal is almost all on falls. In the top third of 20-day volatility against its 60-bar history, the largest third of down days were followed by a next-day market-adjusted return of +0.0100 (t 5.74, n 1056). The largest third of up days in the same tercile were followed by only −0.0028 (t −1.76, n 1138). In the middle volatility tercile the large down days gave +0.0041 (t 2.17, n 740) and the large up days −0.0006 (t −0.34, n 791).
- **F2:** Across deciles of the scaled 1-day move, only the two most negative deciles were followed by clearly positive next-day returns: +0.0070 (t 4.68, n 1436) and +0.0030 (t 2.35, n 1436). The top decile gave −0.0015 (t −1.10, n 1436), so the up-side fade the book trades adds little.
- **F3:** The rebound after large high-volatility falls is stable over time: +0.0053 (t 4.15, n 1115) in windows w1–w12 and +0.0057 (t 3.13, n 1180) in w13–w24.
- **F4:** Large moves made on weekend days reverse more than weekday ones. The largest third of down days on Saturday or Sunday were followed by +0.0118 (t 3.87, n 432), against +0.0039 (t 3.34, n 1920) on weekdays. The largest third of weekend up days were followed by −0.0056 (t −2.38, n 557), against +0.0003 (t 0.28, n 1877) on weekdays.
- **F5:** By weekday, the fade of the top 30% of scaled moves earned most on Saturday (+0.0073, t 2.78, n 367) and Sunday (+0.0089, t 2.94, n 500). It earned nothing on Monday (−0.0004, t −0.25, n 773) and Friday (−0.0018, t −0.93, n 637). The book's gain per bar follows the same pattern: Sunday +0.0018 (t 2.78) and Saturday +0.0010 (t 2.32), against Monday −0.0001 and Friday −0.0005.
- **F6:** Against the brief, the fade of large moves is weakest when the day's volume is low against its 20-day mean. It earned +0.0010 (t 0.50, n 645) in the lowest volume tercile and +0.0037 (t 3.42, n 2724) in the highest.

## Ideas
- `011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g1_high-volatility-one-day-reversal.g1_turbulent-falls-rebound-next-day` (from F1, F2, F3): A coin whose last day's fall was large relative to its usual daily move over the past 60 days rises over the next 1 day. The rise is larger the larger that scaled fall and the higher the coin's 20-day volatility stands against its own 60-day history.
- `011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g1_high-volatility-one-day-reversal.g2_weekend-day-moves-reverse-next-day` (from F4, F5): A coin's move on a Saturday or Sunday that was large relative to its usual daily move over the past 60 days is followed by a move the opposite way over the next 1 day. The reversal is larger the larger that scaled weekend-day move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
