---
line: 7.d confirmed, not profitable
backtest: 032-01.b1.b1.e2.d2.d2_strong-case-chop-continuation_1d
idea tested: 032-01.b1.b1.e2.d2.d2_strong-case-chop-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4369 USD
---
## Findings
- **F1:** The long side carries the book: in folds B and C, long bars (2541) earned a mean 0.29 % per bar (summed 7.41) against 0.04 % for short bars (2746, summed 1.12); my rebuild of the short-only book has a Sharpe of 0.27 and a Calmar of 0.17, against 1.37 and 2.04 for the long-only book.
- **F2:** The shorts' weakness is not a missing effect but the coin's drift: signal cases after down-weeks still had an unusual move of +3.6 % (t 3.46, 165 grid cases), close to up-weeks' +3.9 % (t 3.52, 178 cases), while down-weeks without the signal rose a raw +1.8 % over the next 7 days (t 2.00, 257 cases), so in these years a short pays its unusual move back to the coin's rise.
- **F3:** Up-weeks alone are not the effect: up-weeks without the chop-agreement signal were followed by a raw +0.37 % (t 0.37, 259 cases) and an unusual move of −0.95 % (t −0.95), against +3.9 % for signal up-weeks, so keeping only the long side keeps the idea's own situation and adds no separate effect.
- **F4:** The deepest falls come from the losing side of each window: in w12 (−17.0 % while the coins fell 4.4 %) and in w9 (−16.4 %) the longs lost (−0.33 and −0.42 summed) while the shorts gained; in w17 (−14.4 %) the shorts lost (−0.51) while the longs gained 1.28.
- **F5:** Dropping the shorts lowers the deepest fall only a little in my rebuild (−16.1 % long-only against −16.8 % for both sides, −15.4 % long-only without the highest-volatility third), so the side change mainly removes a side that adds falls for almost no gain (short-only deepest fall −18.9 % for +3.3 % a year).
- **F6:** High 30-day volatility does not spoil the signal, so it is no repair: signal cases in the highest volatility third had an unusual move of +4.5 % (t 2.74, 100 cases) against +3.5 % (t 4.11, 243 cases) in the rest; their low gain per bar (0.07 %, t 1.1, against 0.31 % in the lowest third) comes from the volatility-target sizing, and high-volatility bars without the signal reverse instead (−2.6 %, t −2.10).
- **F7:** The gain grows with the forecast's strength: bars in the top third by |forecast| earned a mean 0.28 % (t 3.24, 1763 bars) against 0.07 % (t 1.28) in the bottom third.

## Ideas
- `032-01.b1.b1.e2.d2.d2.d1_long-only-chop-continuation` (from F1, F2, F3, F4, F5, F7): When a coin's past 30 days have gone back and forth with little net progress compared with the sum of its daily moves, and both its 7-day and 30-day net moves are up, its 7-day rise counted in 30-day daily swings tends to be followed by a further rise over the next 7 days, a rise that is larger after the largest scaled 7-day rises and grows faster than in proportion to their size.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
