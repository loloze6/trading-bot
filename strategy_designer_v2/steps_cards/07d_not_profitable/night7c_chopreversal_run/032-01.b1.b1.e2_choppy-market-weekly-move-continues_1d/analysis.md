---
line: 7.d confirmed, not profitable
backtest: 032-01.b1.b1.e2_choppy-market-weekly-move-continues_1d
idea tested: 032-01.b1.b1.e2_choppy-market-weekly-move-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5684 USD
---
## Findings
- **F1:** The book's standardised forecast often points the other way from the idea's own signal. Its sign differs from the raw 7-day move counted in 30-day swings on 32 % of cases (share agreeing 0.68). On choppy bars where the two signs disagree, the drift-removed gain per bar is -0.053 % for shorts and +0.057 % for longs (977 and 773 bars). Where they agree it is +0.095 % and +0.158 % (2333 and 2423 bars). Signed by the raw scaled move, the choppy grid cases move +2.20 % beyond drift over 7 days (t 3.79, 612 cases), against the +0.50 % size of the book's forecast cases.
- **F2:** The effect is graded and large in its strong cases, far above the cost of a trade. Choppy cases with an absolute scaled 7-day move of at least 1 move +4.35 % beyond drift (total +4.53 %, strength 0.29, t 3.74, 162 cases), about 23 times the 0.19 % cost of a trade. Cases below 1 move +1.42 % (strength 0.085, t 2.14, 450 cases). The top quartile of the absolute scaled move earns +4.30 % (t 3.63, 153 cases).
- **F3:** The chop condition belongs to the idea and is not an effect of its own. Inside chop, the drift-removed 7-day return without a direction is near zero in every efficiency-ratio band: +0.41 % (t 0.43), -1.63 % (t -1.65) and +0.77 % (t 0.70). The same raw signal outside chop gives -1.69 % (t -1.62, 247 cases), against +2.20 % (t 3.79) in chop.
- **F4:** The continuation comes almost entirely from weekly moves that point the same way as the coin's 30-day net move. Those cases move +3.77 % beyond drift over 7 days (t 4.92, 344 cases). Weekly moves against the 30-day move give +0.18 % (t 0.21, 268 cases). This condition's effect on its own, without the weekly signal, was not measured.
- **F5:** The deepest fall shows the book shorting against a rising coin. It is a -27.7 % fall over 68 days across w16–w17, while holding the coins summed +8.6 % (correlation with holding 0.58). In those windows, choppy-regime shorts lost -0.150 % per bar (430 bars) while the coins' 30-day return averaged +7.1 %. Shorts held into the non-choppy regime lost -0.258 % per bar (83 bars).
- **F6:** The book's gross gain sits on the long side, which earns +0.195 % per bar (3703 bars). Shorts earn -0.007 % per bar (3926 bars). The fee is about 0.009 % per bar. The weak part is the shorts against the drift, not the trading costs.

## Ideas
- `032-01.b1.b1.e2.d1_raw-scaled-weekly-continuation` (from F1, F2, F3): When a coin's past 30 days have gone back and forth with little net progress compared with the sum of its daily moves, its 7-day move counted in 30-day daily swings, taken at its own size rather than against its recent values, tends to be followed by a move the same way over the next 7 days. The larger that scaled 7-day move, the larger the following move.
- `032-01.b1.b1.e2.d2_chop-continuation-with-month` (from F4, F5, F6, F3): When a coin's past 30 days have gone back and forth with little net progress compared with the sum of its daily moves, its 7-day move counted in 30-day daily swings tends to be followed by a move the same way over the next 7 days, only while that 7-day move points the same way as the coin's 30-day net move. The larger that scaled 7-day move, the larger the following move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
