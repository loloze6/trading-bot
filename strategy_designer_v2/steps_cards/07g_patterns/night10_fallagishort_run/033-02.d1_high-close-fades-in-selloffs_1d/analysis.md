---
line: 7.g patterns
backtest: 033-02.d1_high-close-fades-in-selloffs_1d
idea tested: 033-02.d1_high-close-fades-in-selloffs
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4108 USD
---
## Findings
- **F1:** Inside the falling agitated profile, the close's position in the range does sort the next day: the top fifth minus the bottom fifth is +3.47 % in short-direction excess (Welch t 3.03, 383 cases), but almost all of it is the bottom fifth. Closes at the low are followed by a rise (short excess -2.81 %), while closes at the high are followed by only a small fall (+0.65 %). The short side the idea bets on is therefore thin, which matches its verdict (t 0.33).
- **F2:** Inside the profile, the next day is graded more strongly by the day's own return scaled by its 20-day swing (day-clustered graded t 3.40, 367 cases on 214 days) than by close location (t 2.09). The top half minus the bottom half by that scaled return is positive in every coin (+2.8 % BCH, +3.5 % LTC, +3.0 % XMR) and every year (+2.4 % to +4.4 %). This effect is again carried by down days rebounding (bottom fifth -2.95 %), a long effect outside this run's box.
- **F3:** Among up days inside the profile, the size of the rise does not grade a fall; it runs the other way. By tercile of the scaled rise, the short excess over the next day is +1.70 %, +1.36 % and +0.10 %, from 61, 60 and 61 cases.
- **F4:** An up day that closes in the lower half of its range (a rally that gave back its gains intraday) is followed by a fall. Its short excess is +2.56 % the next day (t 3.75) and +4.27 % over two days (t 3.20), but on only 27 cases. Among all up days, the lowest tercile of close location gives +1.92 % against +0.41 % and +0.81 % for the two higher terciles (about 60 cases each), so the grading is not monotone.
- **F5:** Over three days, the 7-day return scaled by swing grades a fall (day-clustered t 2.22, 117 cases on 67 days). The top half minus the bottom half is +3.4 % to +6.7 % in all three coins and in three of four years (2019: -0.2 %). This is a bounce fade in a falling market, which the profile map already holds in falling agitated short (the 074-01 family).
- **F6:** Several angles showed no pattern inside the profile. Range width scaled by swing (q5-q1 -0.9 %, t -0.71) and volume against its 20-day mean (-0.6 %, t -0.53) sort nothing. No weekday stands out (|t| ≤ 1.57 across 7 days), and the unconditional short excess in the profile is -0.46 % a day (t -1.43, 383 cases).

## Ideas
- `033-02.d1.g1_failed-rally-close-fades` (from F4, F1, F3): In a falling, agitated market, on a day the coin rises, the lower its close sits within that day's high-low range, the larger its fall over the next one to two days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
