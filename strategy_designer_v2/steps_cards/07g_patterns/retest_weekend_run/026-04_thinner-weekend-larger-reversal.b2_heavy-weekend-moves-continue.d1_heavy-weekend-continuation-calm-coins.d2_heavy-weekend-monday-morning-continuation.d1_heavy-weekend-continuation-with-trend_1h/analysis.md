---
line: 7.g patterns
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d1_heavy-weekend-continuation-with-trend_1h
idea tested: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d1_heavy-weekend-continuation-with-trend
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4406 USD
---
## Findings
- **F1:** Over all coins and windows, a coin's weekend move continues over Monday's first 12 hours only when weekend volume is heaviest. In the top fifth of the weekend-to-prior-weekday volume ratio, the move continues by +0.75 % beyond drift in its own direction (t 3.36, 363 cases), and by +0.79 % (t 2.29) over 24 hours. The four lower fifths give between −0.14 % and −0.01 % over 12 hours (all |t| < 0.9).
- **F2:** The continuation is also concentrated in the largest weekend moves, and the shape is not monotonic. The top fifth of |weekend return in usual 48-hour moves| continues +0.83 % over 12 hours (t 3.69, 363 cases), while the middle three fifths give −0.13 % to −0.19 % (|t| ≤ 1.1).
- **F3:** The 30-day-trend gate of the tested idea adds only part of the effect. Heavy-volume weekends with the trend continue +0.77 % over 12 hours (t 2.71, 226 cases), heavy-volume weekends against the trend continue +0.44 % (t 1.11, 119 cases), and light-volume weekends give −0.06 % to −0.03 % whatever the trend.
- **F4:** The weekend effect is not steady across years. Over 12 hours it is −0.35 % (t −1.27) in 2018 and −0.39 % (t −2.17) in 2019, against +0.51 % (t 2.24) in 2022 and +0.23 % to +0.37 % in 2023–2025. This fits the book's Calmar of 0.50 and its Sharpe falling short of holding's.
- **F5:** The strongest pattern in the bars is time of day. Hours opening at 21:00 and 22:00 UTC return +5.5 bp (t 6.87) and +4.4 bp (t 5.76) on average, over about 17,400 coin-hours each. These are the only two hours of 24 with |t| above 4; the next are 14:00 at −3.5 bp (t −3.77) and 03:00 at −2.8 bp (t −3.89). The t's pool six correlated coins, so they overstate independence.
- **F6:** Saturdays are quieter and drift up. The mean absolute hourly return is 53.5 bp on Saturday and 56.6 bp on Sunday, against 66.5–68.0 bp on weekdays. Saturday's mean hourly return is +2.1 bp (t 5.57, 59,082 coin-hours), against −0.8 to +1.5 bp on weekdays.
- **F7:** Among the 48-hour moves measured at every midnight, only the move ending Monday night reverses over the next 48 hours, by −0.33 % (t −2.20, 1,813 cases); the Sunday-night (weekend) move does not (+0.15 %, t 0.90). After seven weekdays and three horizons were tested, this does not stand out from chance.

## Ideas
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d1_heavy-weekend-continuation-with-trend.g1_heavy-weekend-volume-drives-continuation` (from F1, F3): A coin's Saturday–Sunday move continues in its own direction over the next 12 hours, whatever its 30-day trend. The continuation is larger the heavier the weekend's volume relative to the mean of the five weekdays before it.
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d1_heavy-weekend-continuation-with-trend.g2_extreme-weekend-moves-continue` (from F2, F1): A coin's Saturday–Sunday move, measured in its usual 48-hour moves, continues in its own direction over the next 12 hours. The continuation is larger the larger that move is, and grows fastest among the largest moves.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
