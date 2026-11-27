---
line: 7.b inconclusive
backtest: 067-02.b1.b1.d3_calm-choppy-month-rise-continues_1d
idea tested: 067-02.b1.b1.d3_calm-choppy-month-rise-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3831 USD
---
## Findings
- **F1:** Step 5's main measure is on the side the idea predicts but short of the bar: slope t 1.35 over 776 cases on 229 days, and the long-minus-short check passes (+0.79 %). The test already used every fold and every coin, so no further data is available. In the shown folds B and C alone, the same day-clustered regression has t 2.92 (143 cases, 61 days), so folds A and D must carry a weaker effect.
- **F2:** The effect lives in the larger monthly moves. In the choppy calm profile, the half of cases with the larger |30-day return| has slope t 2.76 (71 cases, 40 days), with mean 7-day excess +5.2 % after rises and −4.7 % after falls. The smaller half has t 0.76 (72 cases), with excesses of −0.1 % and −0.3 %, which is no effect at all.
- **F3:** Graded by the plain 30-day percent return, the 7-day excess rises almost monotonically across sextiles: −4.7 %, −2.5 %, −0.1 %, −0.2 %, +4.5 % and +6.8 %. Graded by the plan's standardised forecast, the sextiles are not ordered: the 1.3 to 6.7 sextile shows −2.0 % and the top one +4.6 % against +5.0 % below it. The move is graded by its plain size, and the middle of the range is flat.
- **F4:** The continuation shows on both sides and only inside the profile. Inside it, the cases after falls have t 2.18 (64 cases, 35 days) and the cases after rises have t 1.70 (79 cases, 38 days). Outside it, the regression gives t 0.22 when not choppy (544 cases) and t 0.59 over all bars (981 cases).
- **F5:** The effect is uneven across periods. By year, the clustered t is −0.24 (2018), 0.31 (2019), 0.35 (2020) and 2.75 (2021). By window, w10 has t 2.30 and w12 has t 2.21, while w14, w17 and w18 are negative (−1.38, −0.93, −1.94). The market's own swings drown the small cases.
- **F6:** The plan's 7-day horizon is where the effect shows best. The naive t is 2.46 at 7 days against 1.58 at 3 days and 1.79 at 14 days. Per case, the size is +0.94 % against a trade cost of 0.22 %, so cost is not what blocks the idea.

## Ideas
- `067-02.b1.b1.d3.b1_large-calm-choppy-month-continues` (from F1, F2, F3, F4, F6): In a choppy, calm market, the further a coin's close has moved from its close of 30 days earlier, measured as a plain percent of that earlier close, the further it moves the same way over the next 7 days. This continuation is carried by the month's large rises and falls, and grows with their size.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
