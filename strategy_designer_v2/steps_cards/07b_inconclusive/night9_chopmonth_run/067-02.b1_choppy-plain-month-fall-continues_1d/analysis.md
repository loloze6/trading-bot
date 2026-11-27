---
line: 7.b inconclusive
backtest: 067-02.b1_choppy-plain-month-fall-continues_1d
idea tested: 067-02.b1_choppy-plain-month-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3949 USD
---
## Findings
- **F1:** Step 5's main measure appears to have the wrong sign. With forecast < 0, -(forecast/10) × (return − drift) is the long-side excess, not the short's gain. On folds B and C the correctly signed weighted short gain is +2.31 % per cell (t 1.34, 159 cells, 76 days), and the recorded −1.34 is its mirror. So the verdict's −0.0121 (t −1.55) points the idea's way, and the size agrees: unusual move +1.13 % in the short direction, t 2.08, 1024 cases, strength 0.071.
- **F2:** The config's standardised forecast hides the depth the idea is about. Its deepest quartile and its second quartile have the same plain 30-day return (−21.3 % and −21.8 %) but excess short moves of +7.0 % and −0.7 %, and its Spearman with the short move is only 0.11. Weighting each cell by the plain percent depth of the fall instead gives +12.0 % per weighted cell with t 3.84 (159 cells, 76 days).
- **F3:** The move grows with the plain depth of the 30-day fall. The mean short-direction excess move over 7 days is +10.2 % for falls beyond −20 % (37 cells, median +9.0 %), +3.6 % for −20 to −10 % (23), +4.3 % for −10 to −5 % (17) and +1.1 % for −5 to 0 % (34).
- **F4:** Falls deeper than −10 % carry +7.7 % per 7 days (t 2.86, 60 cells, 34 days), against +2.2 % for shallower falls (t 1.35, 51 cells, 32 days). The deep cases are positive in 8 of 11 windows, though w16 (+24.4 %, 7 cells) and a single −38 % cell in w10 weigh heavily.
- **F5:** The effect is about 7 days long. The raw short's move is +0.7 % over 3 days (t 0.96) and −2.6 % over 14 days (t −1.38). Over 30 days it is −6.6 % (t −2.20), because the coins' normal 7-day drift of +2.8 % in folds B and C works against a short. So only the unusual move pays: the total move per case is −0.01 %, against a cost of 0.22 % per trade.
- **F6:** No more data is available. The test already used all four folds and all 19 coins, so the answer is to grade the tested idea by plain percent depth, where the effect shows clearly (F2 to F4), rather than to rerun it unchanged.

## Ideas
- `067-02.b1.b1_choppy-deep-month-fall-continues` (from F1, F2, F3, F4, F5, F6): In a choppy market, the further a coin's close sits below its close of 30 days earlier, measured as a plain percent of that earlier close, the more it falls over the next 7 days, so that the deepest monthly falls are followed by the largest weekly declines.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
