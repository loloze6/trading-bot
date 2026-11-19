---
line: 7.d not profitable
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift_1h
idea tested: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3394 USD
---
## Findings
- **F1:** The book loses because fees take about five times what the position earns. Summed over all bars, the position's gain before fees is 3.79 and the fees are 18.22. Fees run at 0.107% of the share of the book turned over, and there is about one round trip per day at about 0.5 allocation. So the daily book return is negative for every coin (-0.00061 to -0.00109), while holding the coins returns +0.00067 to +0.00155 a day.
- **F2:** The rise the idea bets on is real but small against the fee. The 20:00–22:00 return averages only 0.017% to 0.087% per coin (n ≈ 2750 per coin). The trades' own record makes it worse: 17075 trades average -0.064% before fees (t -5.9) and -0.164% after a fee of about 0.100% per trade.
- **F3:** Almost all of the 2-hour rise sits in the coin's most volatile weeks. In the top decile of 7-day hourly volatility the return is +0.290% (t 4.0, n 1528) and in the ninth it is +0.124% (t 2.5). Deciles 0–7 range from -0.028% to +0.047%, with no t above 1.5. In volatility units it is still the top two deciles that carry it: 0.12 (t 3.6) and 0.09 (t 2.5), against at most 0.05 below.
- **F4:** Volatility measured against the coin's own recent past tells the same story. In the top quintile of 7-day volatility relative to its 30-day average, the return is +0.145% (t 3.7, n 3050). The other four quintiles range from 0.009% to 0.036%.
- **F5:** The vol-target sizing puts the smallest position exactly where the gain is. The mean allocation is 0.34 in the top volatility decile and 0.64 in the bottom one. Most of the turnover, and so most of the fees, falls in the calm weeks that earn nothing.
- **F6:** The gain is uneven across years. By year the 2-hour return is +0.138% (t 4.4) in 2020, +0.145% (t 3.8) in 2021 and +0.088% (t 3.0) in 2024. It is -0.053% (t -2.2) in 2023 and about zero in 2018, 2019 and 2025. This fits a gain that shows up only in turbulent periods.

## Ideas
- `016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_evening-drift-in-turbulent-weeks` (from F1, F3, F4, F6): Each day, the coin rises over the two hours after 20:00 UTC by more than in its other hours, only while its realised hourly volatility over the past 7 days is high against its own level over the past 30 days. Inside that state, the rise is larger the higher that 7-day volatility stands above its 30-day level.
- `016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_evening-drift-outpaces-volatility` (from F3, F5): Over the two hours after 20:00 UTC, the coin's rise measured in units of its 7-day hourly volatility is larger the higher that volatility is. So the rise grows faster than the coin's volatility, not just in proportion to it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
