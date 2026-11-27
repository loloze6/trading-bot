---
line: 7.b inconclusive
backtest: 072-02.b1_choppy-deep-up-day-fade-more-coins_1d
idea tested: 072-02.b1_choppy-deep-up-day-fade-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3912 USD
---
## Findings
- **F1:** On the active bars of folds B and C (choppy up-days, 803 bars), the deepest third's excess return grows with the horizon while the shallowest third's stays near 0. The deepest third gives -0.85 % over 1 day, -1.39 % over 2, -1.78 % over 3 and -2.73 % over 5 days. The shallowest gives -0.07 %, -0.52 %, -0.90 % and -0.13 %. The Welch t of deep minus shallow is -1.80 over 1 day and -2.21 over 5 days (overlapping returns).
- **F2:** On non-overlapping 5-day cases the same active bars give deep -8.0 % against shallow +1.4 %, t -3.01 on 77 cases. All choppy up-days give deep -7.3 % against shallow +15.6 %, t -1.90 on 100 cases. The test's 1-day horizon catches only the first part of a move that keeps building over the next days.
- **F3:** The 1-day effect is weak and uneven. The rank correlation of depth with the next day's excess return on choppy days is -0.024 (p 0.46, 959 days). The depth quintiles do not fall evenly: +0.07 %, +0.57 %, -0.65 %, -0.54 %, -1.07 %. On up-days the deep-minus-shallow t is -0.10 in 2019 and +0.03 in 2020, against -1.00 in 2018 and -1.60 in 2021.
- **F4:** The coins split. Over 1 day on choppy days, deep minus shallow has t -1.96 for BTC and -1.69 for ETH. It points the other way for LINK (t +1.88) and ZEC (t +0.81). On the full test the 1-day result is -0.14 % with t -0.82, weaker than the -1.80 seen in folds B and C, so folds A and D dilute it further.
- **F5:** Dropping the up-close condition, all choppy days give a 3-day deep-minus-shallow t of -2.93 (322 non-overlapping cases; deep -3.4 % against shallow +0.3 %). Down-days alone give t -3.83 (158 cases).
- **F6:** Over 1 day the idea's total move per case (+0.11 %) is half the 0.22 % cost of a trade. A longer horizon, where the deep cases' move is several times larger (F1, F2), is the only way this effect can cover the cost.

## Ideas
- `072-02.b1.b1_choppy-deep-up-day-five-day-fade` (from F1, F2, F3, F6): In a choppy market, on a day that closed up, the further the close sits below the coin's 20-day high, in units of its 20-day daily-return standard deviation, the larger its fall over the next five days.
- `072-02.b1.b2_choppy-deep-close-three-day-fall` (from F5, F1, F6): In a choppy market, the further a coin's close sits below its 20-day high, in units of its 20-day daily-return standard deviation, the larger its fall over the next three days, whether that day closed up or down.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
