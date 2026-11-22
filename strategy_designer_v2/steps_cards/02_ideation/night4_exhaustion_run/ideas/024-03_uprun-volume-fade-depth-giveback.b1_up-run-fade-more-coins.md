---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-03_uprun-volume-fade-depth-giveback
line: 7.b inconclusive
backtest: 024-03_uprun-volume-fade-depth-giveback_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: After an unbroken streak of rising four-hour periods whose gain is large relative to the coin's typical four-hour move over the past 30 days, the coin falls over the next three days. The more the volume declined from the start of the streak to its end, the larger the fall.
Consequence: For up-runs of the same size, the give-back grows the more the volume behind the run has faded, because only fragile late buyers remain.
Why:
- F1: The tested short after up-runs sits on the predicted side but is too small to show: step 5 measured +0.13 % per case (t 1.15, 5709 cases, strength 0.014), below the 0.19 % cost of a trade, and my recomputation finds no horizon that does better (6 bars +0.01 % t 0.11, 12 bars +0.11 % t 1.20, 18 bars +0.14 % t 1.28, 36 bars +0.05 % t 0.29, about 5,600 to 5,800 cases each).
- F3: The up-side effect is mixed across periods and weak everywhere. By year it is +1.52 % in 2018 (t 3.83), +0.89 % in 2022 (t 3.02) and −0.82 % in 2020 (t −2.38), and it is near zero in 2023 to 2025. Every coin is positive, but no t exceeds 1.13 (LTC +0.30 %, BTC +0.04 %).
- F4: Volume fade adds little to the up side. Among the two largest run-size quintiles, the highest-fade tercile gives +0.56 % (t 1.56, 585 cases) against −0.15 % and −0.30 % for the other two. Cases in the top half of both run gain and fade give −0.46 % (t −1.31, 799 cases).
