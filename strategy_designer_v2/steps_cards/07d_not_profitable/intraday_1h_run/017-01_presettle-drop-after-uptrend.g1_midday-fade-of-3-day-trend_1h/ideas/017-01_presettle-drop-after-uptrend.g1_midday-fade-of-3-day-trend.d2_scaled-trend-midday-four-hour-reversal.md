---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend
line: 7.d not profitable
backtest: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 3-day return relative to its 3-day volatility, the more its return over the 4 hours following 12:00 UTC runs against that 3-day return, so a strong 3-day rise is followed by a larger decline and a strong 3-day fall by a larger rebound over those 4 hours.
Consequence: A trader would refuse the midday fade when the 3-day trend is weak against its volatility, and hold it through the afternoon only when that scaled trend is large.
Why:
- F3: The fade of the 3-day trend from the 12:00 UTC close builds over the following hours: 3.7 bp over 2 h (t = 3.09), 5.8 bp over 3 h (t = 4.01) and 7.4 bp over 4 h (t = 4.23, n = 16,932). It is gone by 6 h (-0.6 bp) and reversed by 12 h (-6.1 bp, t = -2.17).
- F4: The 4-hour fade is graded by the 3-day return scaled by its own 3-day volatility: -1.4 bp in the weakest |z| quintile (t = -0.40) against 18.4 bp in the strongest (t = 3.73, n = 3,387).
- F5: The 4-hour fade is positive in all 6 coins (2.2 bp BTC to 16.8 bp XMR) and in 7 of 8 years (2020 at -1.2 bp; 2022 and 2025 at about 15 bp), so it does not rest on one period.
