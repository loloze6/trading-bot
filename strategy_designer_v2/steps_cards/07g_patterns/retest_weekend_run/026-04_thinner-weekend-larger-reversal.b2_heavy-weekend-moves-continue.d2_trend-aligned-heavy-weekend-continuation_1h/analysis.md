---
line: 7.g patterns
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d2_trend-aligned-heavy-weekend-continuation_1h
idea tested: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d2_trend-aligned-heavy-weekend-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4277 USD
---
## Findings
- **F1:** The two hours from 20:00 to 22:00 UTC carry the strongest clock pattern in the bars, and it is a rebound: the mean hourly return is +5.45 bp at 20:00 (t 6.75) and +4.36 bp at 21:00 (t 5.66), against roughly ±1 to 3 bp at the other hours. Over the 20:00–22:00 stretch, the coin's 24-hour return before 20:00 (in usual moves) predicts the stretch with slope −0.067 (t −5.45, n 15966), from +19.2 bp (t 4.96) in the lowest fifth of prior returns down to −0.8 bp (t −0.30) in the highest.
- **F2:** The same 20:00–22:00 rebound is concentrated in volatile conditions, at +16.1 bp (t 4.71) in each coin's top quarter of 30-day hourly volatility against −0.6 to +2.5 bp in the other three quarters. It appears in every coin (+1.6 to +8.0 bp, t 0.55 to 2.28) and is strongest on Sundays (+12.2 bp, t 3.75) and Mondays (+10.5 bp, t 3.29). Its sign is not stable across years: it is negative in 2018 (−5.6 bp) and 2023 (−3.6 bp). Even its best fifth is only about the size of one trade's cost (0.19 %).
- **F3:** On a non-overlapping 48-hour grid on every day of the week, a 48-hour move that goes the same way as the coin's 30-day return before it continues: +0.053 usual moves over the next 48 hours (t 2.69, n 3191 cases), against −0.008 (t −0.42, n 3228) when it goes against the trend. The tested weekend version (+0.150 of a usual move, t 1.76, 252 cases) is thus a small subset of a broader pattern. The broader pattern is unstable by year, strong in 2020 (t 3.06), 2021 (t 2.29) and 2024 (t 3.61) and negative in 2019, 2022, 2023 and 2025.
- **F4:** The idea's own grading fails in the bars: among Sunday-23:00 cases, the smallest quarter of weekend moves continues the most (+0.082 usual moves, t 1.92) and the largest quarter reverses (−0.060, t −1.05). The weekend continuation also flips sign by year, positive in 2023 (t 2.73) and 2024 (t 1.97) and negative in 2025 (−0.116, t −1.96).
- **F5:** The reversal the brief expected appears one day later than its weekend: the 48-hour move ending Monday 23:00 reverses over the next 48 hours (slope −0.074, t −3.21, n 1814), as does the move ending Tuesday 23:00 (slope −0.066, t −2.84). The move ending Sunday 23:00 does not (slope −0.015, t −0.47). The Monday slope swings from +0.22 (t 2.86) in 2018 to −0.24 (t −4.29) in 2025, so after the many angles looked at it does not stand apart from a regime effect.

## Ideas
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d2_trend-aligned-heavy-weekend-continuation.g1_evening-rebound-after-daily-falls` (from F1, F2): A coin's return from 20:00 to 22:00 UTC is higher the more the coin fell over the preceding 24 hours, measured in its usual 24-hour moves. The rebound is larger the higher the coin's volatility over the past 30 days.
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d2_trend-aligned-heavy-weekend-continuation.g2_trend-aligned-two-day-continuation` (from F3, F4): A coin's 48-hour move continues over the next 48 hours, on any day of the week, the more it goes the same way as the coin's 30-day return before it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
