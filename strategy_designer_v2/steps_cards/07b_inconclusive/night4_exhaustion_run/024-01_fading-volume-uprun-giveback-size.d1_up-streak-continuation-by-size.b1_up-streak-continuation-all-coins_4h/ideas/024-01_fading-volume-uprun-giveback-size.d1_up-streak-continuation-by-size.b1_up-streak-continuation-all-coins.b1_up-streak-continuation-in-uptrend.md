---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins
line: 7.b inconclusive
backtest: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size.b1_up-streak-continuation-all-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just risen in an unbroken streak of four-hour periods, it keeps rising over the next three days, only while its 30-day return is positive; the larger the streak's gain relative to the coin's typical four-hour move over the past 30 days, the larger the further rise.
Consequence: A strong 4-hour up-run is a reason to join it for three days when the coin is up over the past month, and not otherwise.
Why:
- F2: The zero is two opposite effects that cancel, split by the coin's 30-day return at the signal bar. When the 30-day return is positive, the up-streak is followed by a further rise above drift: +0.26 % per case (t 1.76, 4545 cases), positive in 79 % of the coins. When it is negative, the streak is followed by a give-back: -0.46 % (t -3.64, 4557 cases).
- F3: Inside the 30-day up-trend, the effect grows with the streak's size, as the idea says. The top quartile of forecast (mean 19.3) gains +0.77 % (t 1.99, 1136 cases), against +0.21 % for the bottom quartile (mean 3.5). Inside the down-trend, the largest streaks are near zero (-0.22 %, t -0.82) and the smallest give back most (-0.67 %, t -2.69).
- F4: The 30-day return grades the result fairly steadily across its deciles. Deciles 1 to 5 (30-day returns from -23 % to +3 %) give unusual moves between -0.30 % and -1.19 %, with t down to -4.47. Deciles 6 to 9 (+9 % to +87 %) give between +0.25 % and +0.73 %. Only the deepest-fall decile (-37 %) breaks the pattern, at +0.99 % (t 2.88), which looks like a capitulation bounce. The 10-day return shows the same shape.
- F5: The up-trend continuation depends on the regime year to year. It is strong in 2020 (+0.97 %, t 2.48), 2021 (+2.66 %, t 3.97) and 2023 (+0.63 %, t 2.60), and reverses in 2018 (-4.82 %, t -5.73), 2022 (-1.41 %, t -3.62) and 2025 (-0.96 %, t -2.32). The down-trend give-back is negative in 7 of 8 years.
