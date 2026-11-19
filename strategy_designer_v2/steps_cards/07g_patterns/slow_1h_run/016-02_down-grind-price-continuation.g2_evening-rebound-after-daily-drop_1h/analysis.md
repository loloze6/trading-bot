---
line: 7.g patterns
backtest: 016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop_1h
idea tested: 016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3767 USD
---
## Findings
- **F1:** Every coin rises in the evening whatever the forecast says. The hourly bars stamped 20:00 and 21:00 UTC return +5.45 bp (t 6.75) and +4.36 bp (t 5.66), the largest of all 24 hours. The 2-hour excess return from the 21:00 close is positive in all six coins (+7.2 to +9.6 bp, t 2.7 to 4.1), in 7 of 8 years (2022 is the exception at −5.5 bp), and in 74% of coin-windows. It is +5.13 bp (t 3.66, n 8790) even on days with a zero forecast, against +11.87 bp (t 7.39, n 8613) with a positive one.
- **F2:** The idea's edge is real but too small to pay for trading. Trades earn 11.2 bp gross (t 3.81, n 11475) but only 1.2 bp after fees (t 0.41). The book's mean daily return is −2.4 bp (t −5.3 across coins). The book is in a position only 6.6% of bars, with a mean size of 0.31.
- **F3:** Short moves partly reverse over the next 2 to 4 hours. The 2-hour return regressed on the 6-hour volatility-scaled return gives a slope of −2.39 bp (t −6.99, n 206550 non-overlapping cases), negative in 7 of 8 years. It is strongest in XMR (−5.14, t −6.21) and ZEC (−5.36, t −4.96) and absent in BTC (+0.38, t 0.67) and ETH (+0.16, t 0.22). On 4-hour returns, the two lowest 6-hour-return quintiles gain +5.06 bp (t 3.16) and +5.62 bp (t 3.96), while the top quintile gains −0.04 bp (t −0.03).
- **F4:** Whether the 24-hour move reverses or continues over the next 2 hours depends on the hour, with |t| above 6 even after scanning 24 hours. After the 13:00 UTC close (bar stamped 12:00) and the 20:00 close (stamped 19:00), the slope on the 24-hour volatility-scaled return is −9.24 bp (t −6.88) and −7.87 bp (t −6.50), so the move reverses. After the 15:00 close (stamped 14:00) and the 23:00 close (stamped 22:00), it is +8.89 bp (t 6.44) and +8.23 bp (t 6.42), so the move continues.
- **F5:** How a move was built adds nothing to its size. The interaction of the 24-hour volatility-scaled return with path efficiency (net move over summed absolute hourly moves) has t 0.32 at 24 hours (n 17102) and −0.21 at 72 hours (n 5539). Next-day return signed by the past day's direction shows no ordered pattern across volume quintiles (−18.9, −10.7, +10.3, −28.6, −7.5 bp).

## Ideas
- `016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop.g1_six-hour-move-partly-reverses` (from F3, F5): The more a coin has fallen over its past 6 hours relative to its own hourly volatility, the more it rises over the next 4 hours, and the more it has risen the more it falls.
- `016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop.g2_midday-reversal-of-daily-move` (from F4): The more a coin has risen over its past 24 hours relative to its own volatility, as read at the 13:00 UTC close, the more it falls over the two hours to 15:00 UTC.
- `016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop.g3_afternoon-continuation-of-daily-move` (from F4): The more a coin has risen over its past 24 hours relative to its own volatility, as read at the 15:00 UTC close, the more it keeps rising over the two hours to 17:00 UTC.
- `016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop.g4_evening-fade-of-daily-rise` (from F4, F1): The more a coin has risen over its past 24 hours relative to its own volatility, as read at the 20:00 UTC close, the more it falls over the two hours to 22:00 UTC.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
