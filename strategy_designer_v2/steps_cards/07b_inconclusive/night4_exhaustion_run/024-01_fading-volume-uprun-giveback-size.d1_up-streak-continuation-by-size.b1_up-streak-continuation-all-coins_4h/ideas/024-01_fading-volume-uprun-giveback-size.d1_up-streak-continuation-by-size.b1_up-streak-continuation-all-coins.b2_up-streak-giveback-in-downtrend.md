---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins
line: 7.b inconclusive
backtest: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just risen in an unbroken streak of four-hour periods while its 30-day return is negative, it gives back part of the streak over the next three days; the deeper the 30-day fall, the larger the give-back.
Consequence: A 4-hour up-run inside a falling month is a reason to fade it, or to refuse a long, for three days.
Why:
- F2: The zero is two opposite effects that cancel, split by the coin's 30-day return at the signal bar. When the 30-day return is positive, the up-streak is followed by a further rise above drift: +0.26 % per case (t 1.76, 4545 cases), positive in 79 % of the coins. When it is negative, the streak is followed by a give-back: -0.46 % (t -3.64, 4557 cases).
- F4: The 30-day return grades the result fairly steadily across its deciles. Deciles 1 to 5 (30-day returns from -23 % to +3 %) give unusual moves between -0.30 % and -1.19 %, with t down to -4.47. Deciles 6 to 9 (+9 % to +87 %) give between +0.25 % and +0.73 %. Only the deepest-fall decile (-37 %) breaks the pattern, at +0.99 % (t 2.88), which looks like a capitulation bounce. The 10-day return shows the same shape.
