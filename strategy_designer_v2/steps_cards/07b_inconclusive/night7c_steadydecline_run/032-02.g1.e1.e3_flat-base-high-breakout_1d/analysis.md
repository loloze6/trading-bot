---
line: 7.b inconclusive
backtest: 032-02.g1.e1.e3_flat-base-high-breakout_1d
idea tested: 032-02.g1.e1.e3_flat-base-high-breakout
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3639 USD
---
## Findings
- **F1:** Closes at the 28-day closing high are followed by a clear rise, whatever the run-up before them: on the 5-day grid in folds B and C, the 113 at-high cases had a mean excess 5-day return of +4.84 % (t 3.12), against −0.42 % (t −1.30) for the 1,165 other cases; the 151 "trending" cases had +3.79 % (t 2.84); step 5's size is +1.51 % per case (t 2.53, 370 days), 7.8 times the 0.19 % cost of a trade.
- **F2:** The predicted grading by a flat base is not linear but a cliff at the steepest run-ups: by 28-day-return quartile, the at-high cases earned +4.48 % (t 2.19), +8.62 % (t 2.44) and +9.03 % (t 2.29), then −2.77 % (t −1.32) in the top quartile (mean 28-day return +70 %); by forecast quartile, −1.18 % at forecast 0, then a flat +5.15 %, +5.33 % and +5.92 %, so the slope on the forecast has a t of only 1.11 (n 151), as step 5's 0.79.
- **F3:** The plan's standardised run-up hides the effect that the plain 28-day return shows: the excess 5-day return falls with the raw 28-day return at a slope t of −2.20 (n 113), but only at t −0.53 with the 60-bar standardised return the forecast uses (n 83) and t −1.02 with the vol-scaled return; the forecast's correlation with the raw return is only −0.63.
- **F4:** How close the close is to its 28-day high grades the next 5 days on all bars: by decile of distance from the high, the closest decile earned +4.23 % (t 3.06) and the next +1.75 % (t 2.04), while the deciles 14–24 % below the high earned −1.90 % to −3.90 % (t down to −3.96); the slope of the excess return on the distance has a t of 2.31 on all 1,278 cases and 2.20 within 10 % of the high (n 586).
- **F5:** The continuation after a high holds at longer horizons too: over 10 days the at-high cases earned +9.18 % excess (t 2.89, n 62) against −0.87 % for the others, and the raw 28-day return's slope reached t −2.00 over 20 days (n 26).
- **F6:** The at-high rise is broad and not one coin's: the mean excess over 5 days was positive in 5 of 6 coins (XRP +18.8 % t 2.30, ETH +3.7 % t 2.14, BTC +3.0 % t 1.62; only LTC −0.8 %) and in 7 of 11 windows. The steep run-up losses are spread too: LTC −4.9 % (t −1.96, 10 cases), w8 −9.2 % (t −3.12) and w17 −2.4 %.

## Ideas
- `032-02.g1.e1.e3.b1_flat-base-high-more-coins` (from F2, F3, F6): Among coins closing near their highest close of the last 28 days, the smaller the coin's 28-day return, the larger its rise over the next 5 days, so a new high reached from a flat base is followed by more rise than one reached after a steep climb.
- `032-02.g1.e1.e3.b2_nearness-to-28-day-high` (from F1, F4, F5, F6): The closer a coin closes to its highest close of the last 28 days, the larger its rise over the next 5 days, with closes at the high followed by the largest rise.
- `032-02.g1.e1.e3.b3_steep-run-up-high-fades` (from F2, F3, F6): Among coins closing at their highest close of the last 28 days, the larger the coin's 28-day return, the smaller its rise over the next 5 days, so the steepest run-ups to a new high are followed by the weakest moves.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
