---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise.b1_volume-surge-more-coins
line: 7.b inconclusive
backtest: 024-01_fading-volume-uprun-giveback-size.g3_volume-surge-precedes-rise.b1_volume-surge-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin trades a four-hour volume far above its 30-day average, it rises over the next three days, only while its 30-day return is positive. The higher the volume against that average, the larger the rise.
Consequence: Lean long after a volume surge when the coin's last 30 days are up, and refuse the same long after a falling month.
Why:
- F1: The volume surge is followed by a rise only while the coin's 30-day return is positive: those cases end +0.72 % above the coin's normal 18-bar drift (t 4.35, 3,856 cases, strength 0.075), while cases after a falling 30 days end −0.54 % (t −3.92, 3,747 cases, strength −0.056), and the plan's pooled measure (+0.20 %, t 1.81) averages the two together.
- F2: Inside a rising 30 days the move grows with the surge, from +0.16 % (t 0.52) in the lowest volume-ratio fifth to +0.74 %, +0.53 %, +0.99 % (t 2.68) and +1.14 % (t 2.38) in the highest, about 800 cases each, strength up to 0.10. Inside a falling 30 days no fifth is positive with a t above 0.63. The rank correlation of volume ratio with the 18-bar move is weak in both groups (Spearman 0.010 up, 0.041 down).
- F3: The same split shows by year: the bear years 2018 (−1.87 %, t −4.10) and 2022 (−1.24 % weighted, t −4.58) are strongly negative, while 2020, 2021, 2023 and 2024 are positive with t from 2.78 to 3.93. The pooled result is drowned by the market's regime, not weak everywhere.
- F4: The supporting check could not pass by construction: 55.8 % of the cases sit at the forecast cap of 20 (median 20), so the upper half held 0 cases. Graded by the raw volume ratio instead, the top two fifths gain +0.70 % (t 2.87) and +0.43 % (t 1.62), against −0.18 % and −0.26 % in the lowest two.
- F6: The pooled effect is on the predicted side but small: 0.14 % per case, a strength of 0.013, which is 0.6 times the 0.22 % cost of a trade. The test already used every coin and fold the 4h bars allow, because hourly bars end in 2025. Inside a rising 30 days the unusual move of 0.72 % to 1.14 % is 3 to 5 times that cost.
