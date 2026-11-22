---
line: 7.d not profitable
backtest: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse_1h
idea tested: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3886 USD
---
## Findings
- **F1:** The book trades every thin weekend, whatever the size of its move, and the small moves continue instead of reversing. On thin Sunday-23:00 cases, the two quintiles with the smallest absolute weekend move have an unusual 48 h move of -0.65 % (t -2.26, n 379) and -0.81 % (t -2.36, n 378). Only the largest-move quintile reverses, by +1.02 % (t 2.36, n 378), which is about 5 times the 0.19 % trade cost; pooled, the idea's size is 0.002 of a usual move.
- **F2:** The reversal on thin weekends is slow. The slope of the forward return on the weekend move (in usual moves) is -0.030 (t -1.51) at 12 h, -0.067 (t -1.72) at 48 h and -0.173 (t -3.27, n 1812) at 96 h. For the largest-move quintile the unusual move rises from +1.02 % at 48 h to +1.63 % at 96 h (t 2.30), about 8 times the trade cost, so the 48 h holding cuts the reversal short.
- **F3:** Weekends traded heavily against the week continue rather than reverse. The slope on the weekend move is +0.075 (t 3.13) at 12 h and +0.175 (t 2.85) at 96 h (n 432).
- **F4:** Inside the thin regime the reversal holds only on the thinnest weekends. By weekend-to-weekday log volume-ratio quartile, the 48 h reversal is +0.57 % on the thinnest quartile (mean -1.20) and -0.40 %, -0.14 % and -1.04 % on the other three.
- **F5:** The book's 3336 trades lose -0.36 % gross and -0.46 % net on average. Shorts carry the loss: 1797 shorts lose -0.80 % gross while 1539 longs gain +0.14 %. Trades at the capped forecast of 20 lose -0.65 % gross, because the standardised, capped forecast does not separate the large moves that reverse from the rest.
- **F6:** The weekend effect is unstable across years. The Sunday 48 h slope runs from -0.220 (t -3.78, reversal) in 2025 to +0.203 (t 2.01) in 2022 and +0.182 (t 2.00) in 2024 (continuation), which is why every window-left-out Sharpe stays negative (lowest -0.31).
- **F7:** The short reversal is not specific to weekends, and is in fact stronger mid-week. The 2-day move to Wednesday 23:00 reverses over 12 h with slope -0.050 (t -4.96) and over 24 h with slope -0.065 (t -4.11), against -0.030 (t -1.51) and -0.038 (t -1.31) after thin weekends.

## Ideas
- `026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse.d1_large-thin-weekends-reverse-slowly` (from F1, F2, F4, F5): A coin's Saturday-Sunday move is partly reversed over the next 96 hours (Monday to Thursday), only while its weekend volume is lower than its mean volume over the preceding five weekdays. The share reversed rises steeply with the size of the weekend move counted in the coin's usual 2-day moves, so the largest weekend moves carry most of the reversal, and it grows the lower the weekend volume is against the weekdays.
- `026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse.d2_heavy-weekends-keep-going` (from F3, F4): A coin's Saturday-Sunday move continues over the next 96 hours when its weekend volume is higher than its mean volume over the preceding five weekdays, and the continuation is larger the larger the move and the heavier the weekend volume against the weekdays.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
