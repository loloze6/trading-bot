---
line: 7.c no effect
backtest: 089-04_calm-decline-up-volume-lasting_1d
idea tested: 089-04_calm-decline-up-volume-lasting
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3810 USD
---
## Findings
- **F1:** Inside the falling calm profile the tested relation is flat to reversed at every horizon of 10 days or more. The slope of the 10-day excess return on the 20-day up-day volume share is -0.143 (t -0.77, 57 non-overlapping cases), and over 20 days it is -0.447 (t -1.35, 28 cases), matching step 5's -0.0017 (t -1.08, 138 cases) with a negative second half (-0.56 %).
- **F2:** The market fell more than usual in this profile regardless of the lean, and the highest-share quintile did not rise. The 10-day excess return averaged -3.96 % over the 57 falling calm cases, and the highest share quintile (mean share 0.62) still lost -2.2 % against -0.4 % for the lowest (0.34), with no ordering between them.
- **F3:** The share relation appears outside the brief's profile, the opposite of the brief's claim that it lives only in calm declines. Off the falling calm profile, the 10-day slope on the share is +0.156 (t 2.20, 286 cases) and +0.259 (t 2.84, 161 cases with complete volume history).
- **F4:** Inside falling calm, the amount of up-day volume against the coin's usual volume predicts the next 5 days, while the share does not. The up-day volume of the last 20 days over 20 times the 60-day mean volume has a slope of +0.186 (t 2.80, 88 cases) against +0.113 (t 1.13) for the share. Its top tercile gained +2.4 % excess (t 1.61), against -3.7 % (t -1.96) and -3.9 % (t -2.04) for the lower two.
- **F5:** Much of that up-day-volume reading is total volume swelling, not a lean. The 20-day/60-day volume ratio predicts the 5-day excess return in falling calm with slope +0.111 (t 2.64, 88 cases), and it keeps t 2.67 when the share is added (share t 1.24). Up-day volume correlates 0.74 with that ratio, and down-day volume also has a positive sign (t 1.25 at 5 days, 1.73 at 10 days).
- **F6:** The lean only paid when volume was also heavy. At 10 days in falling calm, cases with an above-median share and above-median volume ratio averaged +2.5 % excess (12 cases). Above-median share with below-median volume averaged -9.8 % (9 cases).
- **F7:** The up-day volume effect is uneven across coins and years. Over 5 days in falling calm, its t is 2.85 on ETH (38 cases), 1.21 on XMR, 0.64 on ZEC and -0.24 on BCH, and 2.88 in 2018, 2.11 in 2019 and -0.12 in 2021.
- **F8:** The book cannot pay as it stands. The total move per case is +0.28 % against a 0.31 % trade cost (0.9 times), and the unusual move is -0.86 % (t -0.95, 232 days).

## Ideas
- `089-04.c1_heavy-up-day-volume-rebounds` (from F4, F6, F1, F7): In a falling, calm market, the heavier a coin's volume on its up days over the last 20 days, measured against its usual daily volume over the last 60 days, the more the coin rises over the next 5 days.
- `089-04.c2_swelling-volume-in-calm-decline` (from F5, F4, F2): In a falling, calm market, the more a coin's average daily volume over the last 20 days exceeds its average over the last 60 days, the more the coin rises over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
