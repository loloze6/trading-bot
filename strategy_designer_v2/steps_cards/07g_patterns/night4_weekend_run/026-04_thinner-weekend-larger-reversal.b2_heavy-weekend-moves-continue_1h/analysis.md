---
line: 7.g patterns
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h
idea tested: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3941 USD
---
## Findings
- **F1:** A large move over the past 24 hours, read at 23:00 UTC on any day, is partly reversed over the next 24 hours, and more so the larger the move. In the top fifth of each coin's absolute 24-hour moves the signed next-24-hour return minus drift is −0.50 % (t −4.53, 3208 cases). In the fourth fifth it is −0.20 % (t −2.28). The three smaller fifths sit between −0.02 % and +0.03 % (|t| < 0.4). The top-fifth reversal is about 2.6 times the 0.19 % cost of a trade.
- **F2:** The reversal of large 24-hour moves (top two fifths) holds broadly but fades in the last two years. It is negative in every window group: w1-8 −0.56 % (t −5.14), w9-16 −0.29 % (t −2.35), w17-24 −0.25 % (t −1.92). It is negative in every year from 2018 to 2023 (t −1.81 to −3.38), and positive in 2024 (+0.11 %, t 0.58) and 2025 (+0.10 %, t 0.54). It is clear in BTC, ETH, LTC and XMR (t −2.04 to −4.48) and absent in XRP (t −0.37) and ZEC (t −0.73).
- **F3:** A 48-hour move made on heavy volume continues over the next 48 hours on any day of the week, not only after weekends. On non-overlapping 23:00 anchors over all days, the top fifth of last-48-hour volume over the prior 120 hours gives a signed next-48-hour return minus drift of +0.64 % (t 3.29, 1593 cases), while the other four fifths range from −0.20 % to +0.09 % (|t| ≤ 1.28). Pooled over all days, the quintiles rise steadily from +0.05 % to +0.36 % (top t 2.69).
- **F4:** The heavy-volume continuation is strongest after the weekend. At Sunday 23:00 the top quarter of volume ratio gives +1.20 % (t 3.16, 572 cases), and the bottom quarter is reversed at −0.59 % (t −2.17). On Monday-to-Thursday anchors the top quarter gives only +0.24 % (t 1.54).
- **F5:** The tested Sunday effect rests mostly on one coin. Signed next-48-hour returns after all Sunday 23:00 anchors are significant only for XRP (+1.14 %, t 2.49). BTC (t 0.99), ZEC (t 1.09) and XMR (t 0.21) are positive but weak, and ETH (t −0.17) and LTC (t −0.50) are negative.
- **F6:** The book earns its money on Monday and Tuesday, as designed. Its mean daily return is +0.093 % on Mondays (t 2.67) and +0.076 % on Tuesdays (t 2.57), against −0.008 % to +0.015 % on the other days (Sunday −0.006 %, t −2.27).
- **F7:** The hours 20:00 and 21:00 UTC rise more than the coin's average hour.

## Ideas
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.g1_large-daily-moves-reverse` (from F1, F2): After a coin's 24-hour move, its price moves back against that move over the next 24 hours, and the larger the 24-hour move is against the coin's usual daily move, the larger the reversal.
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.g2_heavy-volume-moves-continue-any-day` (from F3, F4, F6): A coin's 48-hour move made on volume heavier than its mean over the preceding five days continues in the same direction over the next 48 hours, whatever the weekday. The heavier the last 48 hours' volume against the preceding five days, the larger the continuation.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
