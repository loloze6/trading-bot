---
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week_4h
idea tested: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.5039 USD
---
## Findings
- **F1:** When a 4h bar closes below the low of the prior 2 days (12 bars), the coin rises more than usual over the next 3 days. The strength is 0.168 (t 4.44, 753 independent cases), an unusual move of +1.60 % and a total move of +2.13 %, which is 7.3 and 9.7 times the 0.22 % round-trip cost. Over 12 days the strength is 0.284 (t 4.70, 173 cases), with an unusual move of +5.01 % and a total of +7.27 %. Over 1 day there is no effect (−0.008, t −0.32, 2132 cases).
- **F2:** The rebound after a downward break grows with how far the close sits below the 2-day low, measured in the coin's recent 7-day bar volatility. By depth tercile, the 3-day strength is 0.057 (t 0.88), 0.169 (t 2.57) and 0.242 (t 3.34), with about 237 cases each. It is positive in 18 of 19 coins, positive in 2020 and 2022 to 2025, flat in 2019 and negative in 2018 (−0.36, t −2.29, 55 cases).
- **F3:** An upward break above the 2-day high, which is the tested idea's situation, does not stand out. Its strength is 0.023 over 3 days (t 0.63, 831 cases) and 0.077 over 12 days (t 0.92, 185 cases). This matches the inconclusive verdict (0.017, t 0.85); the book's profit comes with holding's own rise of +2.18 % per 12 days.
- **F4:** The larger a coin's 1-day fall, measured in its recent volatility, the larger its rise over the next 3 days. The bottom decile of 1-day returns gives a strength of 0.133 (t 4.64, 1135 cases), and among falling days the slope of strength on the 1-day z-return is −0.106 (t −4.55, 4596 cases). The rebound is concentrated in high volatility: 0.282 (t 6.22, 464 cases) when 7-day volatility is above its usual level for the coin, against 0.047 (t 1.11, 485 cases) below it. It is positive in 5 of 8 years.
- **F5:** A strong 7-day rise is followed by a rise over 12 days only in rising years, so it is not a stable effect. The top quintile's strength is 0.166 overall (t 3.28, 539 cases), but it is −0.62 in 2018, −0.59 in 2022 (t −5.53) and −0.21 in 2025 (t −2.43), against +0.34 to +0.53 in 2020, 2021, 2023 and 2024.
- **F6:** Narrow 2-day ranges are not followed by larger 3-day moves, which goes against the brief. The mean absolute strength rises from 0.645 in the narrowest width quintile to 0.757 in the widest, with about 1950 cases each. The first break out of a wide range reverses rather than continues: the 3-day strength signed by the break's direction is −0.133 (t −2.70, 572 cases).
- **F7:** 3-day stretches starting on Sunday are weaker than usual: strength −0.129 (t −5.54, 1732 cases), negative in 6 of 8 years. This is one of many angles examined and is not graded, so it proposes no idea.

## Ideas
- `019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week.g1_downside-break-snaps-back` (from F1, F2, F3): When a coin's four-hour bar closes below the low of its preceding two days, the coin rises more than usual over the next 3 days. The further that close lies below the two-day low, measured against the coin's 7-day volatility, the larger the rise.
- `019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week.g2_volatile-one-day-fall-rebounds` (from F4, F1): When a coin's 7-day volatility is above its usual level, the larger its 1-day fall measured against that volatility, the more the coin rises over the next 3 days.
- `019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week.g3_downside-break-longer-rebound` (from F1, F2): When a coin's four-hour bar closes below the low of its preceding two days, the coin rises more than usual over the next 12 days. The further that close lies below the two-day low, measured against the coin's 7-day volatility, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
