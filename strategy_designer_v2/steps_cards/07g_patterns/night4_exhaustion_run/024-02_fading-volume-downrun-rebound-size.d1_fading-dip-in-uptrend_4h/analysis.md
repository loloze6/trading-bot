---
line: 7.g patterns
backtest: 024-02_fading-volume-downrun-rebound-size.d1_fading-dip-in-uptrend_4h
idea tested: 024-02_fading-volume-downrun-rebound-size.d1_fading-dip-in-uptrend
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4193 USD
---
## Findings
- **F1:** The 4-hour bar opening at 16:00 UTC is the strongest pattern in these bars: its mean return is +9.9 bp (t 6.64, 17,506 bars), and it is positive in each of the six coins (t from 1.94 for XRP to 3.59 for ETH) and in each of the eight years. It is significant (t > 2) in five of those years; it is weakest in 2022 (+2.6 bp, t 0.62) and 2025 (+4.4 bp, t 1.13).
- **F2:** The 16:00 UTC bar is graded by the size of the bar before it, in either direction. Split by the 12:00 bar's move in usual one-bar moves, the 16:00 bar returns +17.0 bp (t 3.99) after the largest falls and +14.6 bp (t 3.87) after the largest rises. In the middle three fifths it returns only +2.1 to +7.3 bp, with about 3,213 bars per fifth.
- **F3:** Large 24-hour moves, in either direction, are followed by a larger-than-usual rise over the next 3 days, on the 18-bar grid. By size of the absolute 6-bar move in usual moves, the top three deciles show strengths of +0.088 (t 2.02), +0.098 (t 2.33) and +0.140 (t 2.75), about 515 cases each. Six of the seven lower deciles are between -0.02 and -0.06, and one is -0.11 (t -2.37).
- **F4:** The direction of a large 24-hour move does not decide what follows; both extremes rise more than usual over 3 days.
- **F5:** Fading volume does the opposite of what the brief expects. Among streaks of at least 3 falling bars, those with fading volume have strength -0.011 (t -0.16, 232 cases), against +0.080 (t 1.32, 263 cases) with rising volume. Rising streaks show the same order: fading +0.016, rising volume +0.114 (t 1.55). None of these differences is significant.
- **F6:** The book's forecast is graded where it is active. Its terciles of positive forecast give strengths of -0.066, +0.167 and +0.233 (t -0.83, 1.70, 1.91; about 99 cases each). The flat bars give -0.006 (t -0.45, 5,428 cases).
- **F7:** Friday's bars have a mean return of +10.1 bp (t 6.20), positive in all six coins, with Friday 20:00 UTC at +22.3 bp (t 6.27). By year it is not stable: 2022 is -5.7 bp (t -1.47) and 2025 is -0.3 bp. The 20:00 UTC bar's mean of -4.9 bp (t -3.18) reverses sign after 2022 (2018 -28.0 bp, 2024 +9.5 bp).

## Ideas
- `024-02_fading-volume-downrun-rebound-size.d1_fading-dip-in-uptrend.g1_big-daily-moves-precede-rises` (from F3, F4, F5): When a coin has made a large move over the past 24 hours, measured against its usual move, it rises over the next 3 days by more than its normal drift. The larger the absolute 24-hour move, whether up or down, the larger the rise.
- `024-02_fading-volume-downrun-rebound-size.d1_fading-dip-in-uptrend.g2_sharp-dip-in-uptrend-rebounds` (from F4, F5, F6): When a coin has fallen far over the past 24 hours against its usual move while it has risen over the past 30 days, it rises over the next 3 days by more than its normal drift. The rise is larger the deeper the 24-hour fall and the larger the 30-day rise, whatever the volume behind the fall.
- `024-02_fading-volume-downrun-rebound-size.d1_fading-dip-in-uptrend.g3_us-afternoon-rise-after-activity` (from F1, F2): Over the four hours from 16:00 UTC, a coin rises, and the rise is larger the larger the coin's move over the previous four hours, in either direction, measured against its usual four-hour move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
