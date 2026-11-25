---
line: 7.b inconclusive
backtest: 036-01_agitated-scaled-fall-three-day-rebound_1d
idea tested: 036-01_agitated-scaled-fall-three-day-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3565 USD
---
## Findings
- **F1:** The forecast does not grade the move in any part of the data. Among the 577 cases in folds B and C, the forecast quartiles give 3-bar excess returns of +0.87 %, +0.18 %, +1.15 % and +0.53 %, which do not rise with the forecast. The case slope of excess on forecast is flat in every trend: falling t -0.25 (116 cases), choppy t -0.06 (353), rising t 0.76 (108). This matches step 5's slope t of 0.72 on 1192 cases.
- **F2:** The step-5 result is on the idea's side but nowhere near the bar. A slope t of 0.72 on 1192 cases (479 days) would need roughly eight times the cases to reach 2. The only more data for these coins' bars is other coins in folds A and D, which is far less than that.
- **F3:** Agitation does not set the recovery apart. On the raw scaled fall, the 3-day excess slope has t 1.29 in agitated bars (452 falls) and t 1.73 in calm bars (633 falls). By trend, calm-rising has t 1.81 and calm-choppy t 1.75, while agitated-falling has t 0.06 and agitated-rising t 0.75. The brief itself names this outcome as one that makes the theory wrong.
- **F4:** Where a rebound exists, it comes on the next day and is not built over the following two days. In calm markets the next-day excess slope on the fall has t 4.01, against t -0.43 for days 2 to 3. In agitated falling markets the next day has t 2.02 and days 2 to 3 have t -1.56. That is the "confined to the next day and given back" pattern the brief rejects.
- **F5:** The mean rebound after falls in an agitated, falling market (+2.48 % excess over 3 days, 116 cases) rests on 44 days with t 1.30. It comes mostly from one window, w16, at +7.39 % on 38 cases. The year 2019 is at -1.02 % and 2021 at -2.33 %, and the larger half of those falls by forecast earns its gain on the next day (+3.29 %), not on days 2 to 3 (-0.46 %).

## Ideas
- No ideas: The theme's effect is not in the data. The three-day rise does not grow with the scaled fall in any trend (F1). It is not larger in agitated than in calm markets (F3). What rebound exists lands on the next day and is not built over the two days after (F4, F5). More data could not lift a t of 0.72 (F2).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
