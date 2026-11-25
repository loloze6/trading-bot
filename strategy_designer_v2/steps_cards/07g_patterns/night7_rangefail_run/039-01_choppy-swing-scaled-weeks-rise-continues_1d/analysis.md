---
line: 7.g patterns
backtest: 039-01_choppy-swing-scaled-weeks-rise-continues_1d
idea tested: 039-01_choppy-swing-scaled-weeks-rise-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6792 USD
---
## Findings
- **F1:** In the choppy profile, a coin's one-day return measured in its own 20-day daily swings predicts its excess return over the next 5 days far better than the tested 20-day move. Day-pooled slope 0.1125, t 3.63 on 134 days; with the tails clipped, slope 0.0229, t 2.47. Fitted alongside the 20-day swing-scaled move, the one-day move keeps t 3.21 while the 20-day move drops to t 1.18.
- **F2:** This carry from the one-day move belongs to the choppy profile. Outside it, the same 5-day slope is 0.0079 with t 1.04 on 241 days.
- **F3:** The carry builds with the horizon and is not there the next day or two.
- **F4:** The one-day carry has the same sign on every coin with choppy cases: 9 of 9 coin slopes are positive. The largest t are DOGE 2.16, XRP 1.61 and ADA 1.52.
- **F5:** The one-day carry is uneven and should be read with caution.
- **F6:** Over the next single day, a large swing-scaled one-day move partly reverses in every profile. One-day slope is -0.0045 (t -2.52, 714 days) in the choppy profile and -0.0034 (t -2.52, 1197 days) outside it.
- **F7:** The tested 20-day swing-scaled move is weak and lopsided in the choppy profile.
- **F8:** Despite that, the book's gain came from longs after 20-day rises.
- **F9:** The other angles I looked at stand out from nothing, given how many were examined.

## Ideas
- `039-01.g3_choppy-few-day-move-carries` (from F3, F1, F2): In a choppy market, the larger a coin's 3-day return in units of its own 20-day daily swing, the further it moves the same way over the next 10 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `039-01.g1_choppy-one-day-jump-carries` (from F1, F2, F3, F4, F5): In a choppy market, the larger a coin's one-day return in units of its own 20-day daily swing, the further it moves the same way over the next 5 days.
- `039-01.g2_next-day-giveback-after-jumps` (from F6): The larger a coin's one-day return in units of its own 20-day daily swing, the more it moves back the other way over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
