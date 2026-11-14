# 7.d exercise 3: the final rules, twice on the fixed inputs (2026-11-14)

Inputs: the card's fixed inputs, 002-01 (golden cross) and 002-03 (close above the 200-day average), both not
profitable (they fail the gain against holding and Calmar). Two runs each (`run_1/`, `run_2/`), with the final shared
rules (`../../common/`) and 7.d's prompt "start from what failed". Cost 1.34 USD.

| Criterion | 002-01 run 1 | 002-01 run 2 | 002-03 run 1 | 002-03 run 2 |
|---|---|---|---|---|
| Starts from what failed (F1 on the falls and the gap to holding) | yes | yes | yes | yes |
| Findings measured as the workflow measures (book's daily returns; returns counted once, n given) | yes | yes | yes | yes |
| Repairs written as the tested idea amended, in full; a new idea marked as such | yes (1 new) | yes | yes (1 new) | yes |
| Ideas graded or a regime, one coin, no dates | yes | yes | yes | yes |

**The same repair in both runs, on both inputs:** 002-01: the golden cross loses while the spread still widens but
price has turned down over 20 bars; idea: "only while the coin's recent return is positive" (run 1 d1, run 2 d1).
002-03: long days after a negative 60-day return lose; idea: "only while the coin's own recent return is positive"
(run 1 d1, run 2 d2). The second run adds other angles (a rising average, a narrow spread), not a different answer.

**What the exercise revealed:** the fixed inputs were backtested before the sizing rule (2 % a day by each coin's
volatility). Several findings are about large positions in violent markets (002-01 run 2 F2; 002-03 run 2 F4), which
the sizing now handles. The inputs should be backtested again with the current steps 3 and 4.
