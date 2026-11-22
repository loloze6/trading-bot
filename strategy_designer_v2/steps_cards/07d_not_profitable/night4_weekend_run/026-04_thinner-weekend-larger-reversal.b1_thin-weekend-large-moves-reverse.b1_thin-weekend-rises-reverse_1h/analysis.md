---
line: 7.d not profitable
backtest: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse.b1_thin-weekend-rises-reverse_1h
idea tested: 026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse.b1_thin-weekend-rises-reverse
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5765 USD
---
## Findings
- **F1:** The move per case is too small to pay for a trade, and the coin's own rise works against the short: over the 48 hours after the 717 active weekends the short's total move is −0.18 % (t −0.75), and the step-5 size is +0.03 % total and +0.29 % unusual, against a 0.19 % cost per trade.
- **F2:** The book pays the cost about twice per weekend and loses on most trades: 1,796 short trades on about 952 active weekends (459 lasted under 1.5 h and 348 lasted 1.5–24 h), a mean of 42.6 allocation changes inside each 48-hour hold, a gross mean of −0.93 % and a net mean of −1.03 % per trade, and 26 % winners.
- **F3:** What happened on the weekdays before decides the sign, and the effect is larger over four days than over two: after a weekend rise that followed a weekday rise, the coin kept rising (the short's total is −0.65 % over 48 h, t −1.97, and −1.00 % over 96 h, t −2.20, 593 cases); after a weekend rise that followed a weekday fall, the short gained +0.11 % over 48 h (t 0.43) and +0.47 % over 96 h (t 1.24, 616 cases).
- **F4:** The continuation after a weekday rise is strongest when the weekend traded heavily: weekend rises after a weekday rise on volume at or above the weekday mean were followed by a further rise against the short of 1.68 % over 48 h (t −2.04, 168 cases), against +0.03 % (t 0.11, 434 cases) on thin weekends.
- **F5:** The result changes sign from year to year: the short's total over 48 h on active weekends was +0.20 % to +0.35 % in 2018–2020 and +0.86 % in 2025, but −1.56 % in 2021 (t −1.83) and −0.84 % in 2023 (t −1.79); the book's mean daily return was negative in every year from 2020 to 2024 while the coins' mean daily return was positive.
- **F6:** Weekend moves are not reversed more than weekday moves, and small and mid-sized weekend moves continue: the reversal of the 48-hour move ending at 23:00 is −0.29 % for Sunday (t −1.87) and −0.07 % to −0.24 % on weekdays; the Sunday terciles by size are −0.45 % (t −1.99), −0.58 % (t −2.32) and +0.16 % (t 0.49) for the largest.
- **F7:** The coin's 30-day return bends the result: active cases in the two outer quartiles of 30-day return gave the short +0.44 % and +0.42 %, while the two middle quartiles gave −0.85 % (t −2.08) and −0.75 % (t −1.69).

## Ideas
- `026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse.b1_thin-weekend-rises-reverse.d1_weekend-rise-extends-rising-week` (from F3, F4, F6, F1): A coin's Saturday-Sunday rise that follows a rise over the preceding five weekdays continues over the next four days; the larger the weekend rise and the heavier the weekend's volume against the weekdays' mean, the larger the further rise.
- `026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse.b1_thin-weekend-rises-reverse.d2_thin-bounce-in-falling-week` (from F3, F2, F1): A coin's Saturday-Sunday rise is partly reversed over the next four days, only while its preceding five weekdays fell and its weekend volume is lower than its mean volume over those weekdays; the larger the weekend rise and the lower the weekend volume against the weekdays, the larger the share reversed.
- `026-04_thinner-weekend-larger-reversal.b1_thin-weekend-large-moves-reverse.b1_thin-weekend-rises-reverse.d3_modest-weekend-moves-continue` (from F6, F5): A coin's Saturday-Sunday move continues in its own direction over the next 48 hours (Monday and Tuesday); the larger the move relative to the coin's usual 48-hour move, up to a usual move, the larger the continuation.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
