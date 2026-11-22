---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise
line: 7.d not profitable
backtest: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is positive, the higher its close sits in its 30-day closing range, the more it rises over the next 5 days, and the more so the larger its 30-day net move relative to that range.
Consequence: A trader would buy a coin near the top of a trending month during a 90-day rise, and sell one near the bottom, instead of fading the move.
Why:
- F2: Inside the 90-day-rise regime the close's place in its 30-day range predicts continuation, not reversion. The 5-day unusual move was +1.14 % at the top of the range (t 1.99, n 495) and +0.77 % in the upper part (t 1.30, n 246). It was -1.44 % in the lower part (t -2.39, n 186) and -1.48 % at the bottom (t -1.57, n 182). Grading the deviation by the cube of the flatness gives the same pattern: the lowest two quintiles had -1.26 % (t -2.07) and -2.39 % (t -3.25), and the fourth had +1.19 % (t 2.08).
- F4: In the 90-day-rise regime, the shorts that lose most are closes above the middle in the most trending fifth of months: -1.68 % per case (t -1.93, n 238). Closes above the middle in the flattest fifth earn +0.54 % (t 0.64, n 90). At the very top of the flattest fifth the coin fell 3.34 % against drift (t -2.84, n 38), against +1.68 % at the top of the most trending fifth.
- F5: In the 90-day-rise regime and the two most trending fifths of months, a close far from the middle kept going its own way. The far third moved +2.32 % per 5 days after drift (t 2.05, n 183), +2.75 % in total, about 14 times the cost of a trade. The middle third moved +1.85 % (t 1.71, n 160) and the near third +0.13 % (t 0.18, n 180).
- F6: That continuation in trending months during a 90-day rise held in 6 of 8 years: 2019 +2.3 %, 2020 +4.1 %, 2021 +1.3 %, 2022 +0.4 %, 2024 +1.5 % and 2025 +0.9 %. The exceptions were 2018 (-6.3 %, n 25) and 2023 (-1.0 %).
