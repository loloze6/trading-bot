---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday
line: 7.b inconclusive
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin, Sunday's daily return, measured in its 20-day daily standard deviations, is reversed over the next 1 day: the larger Sunday's move, the larger Monday's move against it.
Consequence: After a Sunday move, lean against it into Monday, harder the larger the move, and do not count on Sunday volume to strengthen the trade.
Why:
- F1: The main measure leans clearly toward the idea, with a slope of 0.000338 per forecast unit and t 3.16 over 2489 Sunday cases. The result is inconclusive only because of the volume clause: the high-volume minus low-volume slope difference has t −0.0001. My per-coin volume terciles agree, with slopes of 2.9, 4.2 and 3.4 bp per forecast unit (t 1.04, 1.95, 1.86, n ≈ 690 each), so there is no gradient with volume.
- F4: The reversal works by direction more than by size. After down Sundays the next-day excess mean is +60 bp, and after up Sundays it is −56 bp. Within the up side the slope runs the wrong way, at −5.8 bp (t −2.24, n 1099). Across forecast quintiles the next day reads −15, −96, −37, +74 and +66 bp, so the most extreme quintiles reverse less than the moderate ones.
