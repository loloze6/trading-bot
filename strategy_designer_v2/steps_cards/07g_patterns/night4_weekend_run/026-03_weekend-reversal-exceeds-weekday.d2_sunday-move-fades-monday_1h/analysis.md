---
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday_1h
idea tested: 026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3945 USD
---
## Findings
- **F1:** On a 24-hour grid covering every start hour and every day, the next 24 hours reverse the past 24-hour return (slope −0.101 of a usual move per usual move, t −11.6, 13030 non-overlapping cases), and the reversal is the same size whether the past 24 hours cover the weekend or not (−0.105, t −5.4, 3764 cases, against −0.100, t −10.3, 9266 cases); the brief's own falsifier, that weekday moves of the same size are reversed just as much, is what the bars show.
- **F2:** The 24-hour reversal sits almost entirely in the coin's most volatile third of 7-day volatility (slope −0.151, t −10.9, 4344 cases), with none in the middle third (+0.006, t 0.4, 4341) or the calmest third (+0.027, t 1.3, 4345); inside the most volatile third it is the same on weekend and weekday cases (−0.151, t −4.8, 1245, against −0.152, t −9.8, 3099).
- **F3:** The 24-hour reversal holds on every coin (slopes −0.077 to −0.151, t −3.5 to −6.8) and in all 8 years (slopes −0.005 to −0.181), with t ≤ −2 in 6 of them (weakest 2024, t −0.2; 2022, t −1.2).
- **F4:** On the tested Monday 00:00 cases alone, the reversal also appears only in the most volatile third (slope −0.192, t −4.0, 676 cases; fade mean +0.257 of a usual move), against +0.011 (t 0.2) and +0.046 (t 0.8) in the other two thirds; its slope was positive in only 11 of 24 windows.
- **F5:** Hourly returns from 20:00 and 21:00 UTC are positive (+0.053 and +0.043 of an hourly standard deviation, t 6.9 and 5.9, about 17400 bars each; Welch t 8.3 against all other hours). The pattern holds on all 6 coins (t 3.0 to 4.4), on every weekday (t 2.4 to 4.0), in 7 of 8 years (2022: −0.021, t −1.5) and in 110 of 144 coin-windows. With 24 hours examined, it still clears any reasonable bar for chance.
- **F6:** The 20:00–22:00 UTC rise is graded by the coin's prior 24-hour return on the falling side: +0.113 (t 6.8) after the lowest fifth, then +0.041, +0.022 and +0.010 through the fourth fifth. The highest fifth breaks the pattern (+0.055, t 4.0).
- **F7:** Over 48 hours there is no reversal of the past 48-hour return on any start day (slopes −0.021 to +0.053), and the 48-hour reversal of the 24-hour return is significant only from Monday (−0.179, t −4.6); otherwise the effect is spent within the first day.
- **F8:** The book earns on Mondays (mean daily return 0.000718), close to zero on Tuesday to Saturday (−0.00007 to +0.00009) and loses on Sundays (−0.000418). Its whole gain is the one Monday bet, while holding the coins earned up to 0.0045 a day on other weekdays.

## Ideas
- `026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday.g1_volatile-one-day-moves-reverse` (from F1, F2, F3, F4, F7): A coin's 24-hour return is followed by an opposite move over the next 24 hours on any day of the week, and the higher the coin's 7-day volatility and the larger that 24-hour move, the larger the reversal.
- `026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday.g2_evening-rebound-after-falls` (from F5, F6): A coin rises over the two hours from 20:00 to 22:00 UTC, and the more it fell over the preceding 24 hours, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
