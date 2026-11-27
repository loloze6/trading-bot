---
line: 7.c no effect
backtest: 086-02_volume-weighted-up-move-continuation_1d
idea tested: 086-02_volume-weighted-up-move-continuation
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4289 USD
---
## Findings
- **F1:** The test found no volume effect in falling, calm markets. Volume does not grade what follows an up day: the tested product gave an unusual 5-day move of +0.27 % (t 0.51, 578 cases on 360 days). On the 5-day grid, light-volume up days were followed by +3.6 % (15 cases), middle-volume ones by +0.6 % (15) and heavy-volume ones by +2.1 % (16). Over 3 days light-volume up days did better than heavy ones (+2.0 % against +0.7 %, 25 and 26 cases). The rank correlation of volume with the next 5 days on up days changed sign across the five grid offsets (−0.18 to +0.25, and −0.003 on the plan's grid).
- **F2:** What the market did instead was carry on the last few days' move. On all five grid offsets, the coin's past 5-day return (in usual daily moves) ranked positively with its unusual move over the next 5 days (rank correlation +0.08 to +0.20, about 93 to 109 cases each). The lowest fifth of past 5-day returns fell a further −4.5 % unusual on average, negative on every offset (−2.3 % to −6.4 %; t −2.57 with 21 cases on the plan's grid). The middle fifths rose +1.0 % to +2.6 %.
- **F3:** Over 10 days the carry-on is steadier. The past 10-day return ranked positively with the next 10 days' unusual move on 9 of 10 grid offsets (+0.10 to +0.46, about 40 to 55 cases each; −0.001 on the tenth). The past 5-day return over the next 10 days was positive on 8 of 10 offsets.
- **F4:** A single day's up move, without its volume, does not grade the next 5 days reliably. Its rank correlation ran from −0.19 to +0.21 across the offsets. The top fifth of day moves gained +4.9 % (t 2.22, 20 cases) on the plan's grid but only +1.2 % averaged over all offsets (−3.3 % on one).
- **F5:** Up days against down days, over the next 5 days, flipped with the grid. On the plan's grid, up days were followed by +2.1 % unusual (t 1.75, 46 cases) and down days by −2.2 % (t −1.77, 55 cases). Across the five offsets the difference was +4.3, +0.9, +2.4, −4.8 and +2.6 points.
- **F6:** Falling, calm markets as a whole did worse than the rest of the data. Over 5 days the unusual move was −0.25 % inside them (101 cases) and +0.39 % outside (513 cases); over 10 days it was −0.10 % inside against +0.73 % outside.
- **F7:** The tested idea is too small to pay for its trades. Per case it moved +0.59 % in total and +0.27 % unusual, against a trade cost of 0.33 %. The book's Sharpe of 0.53 was 0.26 below holding the coins, with a Calmar of 0.25.

## Ideas
- `086-02.c1_calm-decline-five-day-continuation` (from F2, F1, F4, F6): In a falling, calm market, a coin's return over the last 5 days, measured in its usual daily moves, predicts its move over the next 5 days: the stronger the recent rise, the more the coin rises further.
- `086-02.c2_calm-decline-ten-day-continuation` (from F3, F2, F7): In a falling, calm market, a coin's return over the last 10 days, measured in its usual daily moves, predicts its move over the next 10 days: the stronger the recent rise, the larger the further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
