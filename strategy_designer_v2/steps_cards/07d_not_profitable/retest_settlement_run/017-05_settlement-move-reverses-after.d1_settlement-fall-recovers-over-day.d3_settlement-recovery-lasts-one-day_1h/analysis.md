---
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day_1h
idea tested: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4162 USD
---
## Findings
- **F1:** The book is a part-time copy of holding the coins rather than a timing book: it was in a position on 90 % of the coins' days, its daily returns correlate 0.75 with holding's (beta 0.34), it ran from −1.91 % a day in holding's worst fifth of days to +1.72 % in its best, and its deepest fall of −61 % over 309 days (w1 to w3) came while holding fell −66 % over the same days, so the Calmar of 0.14 is the market's fall carried through the book.
- **F2:** The effect pays only while the coin's 30-day return is positive. There, signal cases had an unusual 24-hour move of +0.20 % (t 2.45, 3221 cases) and a total move of +0.34 %, 1.8 times the 0.19 % cost. In a 30-day fall, signal cases had −0.07 % unusual (t −0.77, 3219 cases) and +0.08 % total, under the cost. The condition alone is not the effect: rising-trend settlements without a fall earned only +0.06 % unusual (t 0.75, 3395 cases). It belongs to the theory, because a crowded long side paying funding after a run up is exactly the brief's setting for pre-settlement selling that reverses.
- **F3:** The 7-day trend splits the same way. Signal cases in a 7-day rise had +0.23 % unusual (t 3.01, 3838 cases) and +0.38 % total, against +0.03 % unusual (t 0.45, 4386 cases) for 7-day-rise settlements without a fall. Signal cases in a 7-day fall had −0.12 % (t −1.39, 4195 cases).
- **F4:** The information lies in the deeper falls. The two lowest of the five forecast quintiles gave −0.08 % and −0.16 % unusual 24-hour moves (t −0.71, −1.36), against +0.41 % (t 3.23) and +0.19 % (t 1.39) in the two highest, around 1700 cases each. The deepest two quintiles in a rising 30-day trend gave +0.47 % unusual (t 3.41, 1241 cases) and +0.61 % total, 3.2 times the cost, against −0.05 % (t −0.32, 1333 cases) in a falling trend.
- **F5:** The recovery is larger when the coin's recent volatility is high. In the top third of the 7-day against 60-day volatility ratio, signal cases gave +0.26 % unusual (t 2.54, 2876 cases) and +0.42 % total. The same third without a signal gave −0.22 % (t −2.24, 2854 cases), so the condition alone does not earn. The lower two thirds gave −0.05 % and −0.01 % with a signal.
- **F6:** Trades last 34 to 54 hours on average, well beyond the 24-hour horizon. Net gains per trade are only +0.02 % to +0.09 % in the middle forecast quintiles, against +0.32 % to +0.35 % at the extremes, so the book's holding and middle-strength entries add exposure without adding effect.

## Ideas
- `017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day.d1_settlement-fall-recovers-in-uptrend` (from F1, F2, F4): The rise over the 24 hours after a 00:00 or 16:00 UTC funding settlement grows with the size of the fall over the 2 hours before it against the coin's usual 2-hour move, only while the coin's 30-day return is positive, and it is gone by the second day after settlement.
- `017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day.d2_settlement-fall-after-weekly-rise` (from F1, F3): The rise over the 24 hours after a 00:00 or 16:00 UTC funding settlement grows with the size of the fall over the 2 hours before it against the coin's usual 2-hour move, only while the coin's 7-day return is positive, and it is gone by the second day after settlement.
- `017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day.d3_settlement-fall-in-raised-volatility` (from F4, F5, F6): The rise over the 24 hours after a 00:00 or 16:00 UTC funding settlement grows with the size of the fall over the 2 hours before it against the coin's usual 2-hour move, and grows more the higher the coin's 7-day volatility stands against its 60-day volatility, and it is gone by the second day after settlement.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
