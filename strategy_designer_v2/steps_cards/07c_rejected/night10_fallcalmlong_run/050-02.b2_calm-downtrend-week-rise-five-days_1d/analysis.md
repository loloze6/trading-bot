---
line: 7.c no effect
backtest: 050-02.b2_calm-downtrend-week-rise-five-days_1d
idea tested: 050-02.b2_calm-downtrend-week-rise-five-days
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3734 USD
---
## Findings
- **F1:** Inside the falling calm profile, the tested long cases show no carry. The main measure is -0.16 % excess over 5 days (t -0.21, 264 cases on 146 days), and the slope on the forecast is -0.0008. On the explore half, the excess over 5 days for 7-day rises has a rank correlation with the scaled rise of only 0.08 (n 45, mean +0.64 %, t 0.37).
- **F2:** What the market did instead is continue its falls, not its rises. The two lowest quintiles of the scaled 7-day move (mean -1.56 and -0.70 swing units, n 23 and 22) were followed by -4.47 % (t -1.83) and -4.86 % (t -2.19) excess over 5 days. All 76 profile cases with a 7-day fall averaged -2.90 % (t -2.17). The whole-sample rank correlation of 0.26 at 5 and 10 days therefore comes from the fall side, which is short and outside this research's box.
- **F3:** On the long side, the rise carries further on a longer lookback and a longer horizon, and it grows with the rise's size. For 14-day scaled rises in the profile, the rank correlation with the later excess is 0.14 over 5 days, 0.32 over 10 days and 0.48 over 15 days. The upper half of those rises earned +3.3 % (t 1.63), +5.6 % (t 1.27) and +12.5 % (t 2.15, about 6 cases) excess over 5, 10 and 15 days. The 7-day lookback over 5 days earned only +2.4 % (t 1.26).
- **F4:** The 7-day rise carry is uneven. By coin, only BCH holds it: +6.35 % over 5 days (t 2.52, n 7), against -0.22 % for ETH, +1.50 % for XMR and -0.54 % for ZEC. By year, only 2021 holds it, at +6.7 % over 5 days (n 15), against -1.7 % in 2018 and -1.8 % in 2019.
- **F5:** Outside the profile, the 7-day scaled move shows no clean grading. The top quintile earns +2.30 % over 5 days (t 1.65), the bottom quintile +0.88 %, and the middle quintile -2.04 % (t -1.77). The carry is therefore not a general feature that the falling calm profile merely dilutes.

## Ideas
- `050-02.b2.c1_calm-downtrend-fortnight-rise-carries` (from F1, F3): In a falling, calm market, a coin that has risen over the last 14 days keeps rising over the next 15 days, and rises further the larger its 14-day rise is in units of its 30-day daily-return swing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
