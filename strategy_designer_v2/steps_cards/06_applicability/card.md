# Step card 6: Applicability (2026-11-11)

## Business objective, one question
Is acting on this idea worth it?

**Establish whether acting on a real idea pays, after its costs and against its risk, consistently enough to be traded, by one rule fixed in advance and applied the same way to every idea.**

## Input
One real idea (its step 5 verdict is "confirmed"), its plan, and its backtest record. An idea whose verdict is anything else is not assessed; its index line says so.

## Output
One assessment per real idea: **worth acting on** or **not worth acting on**, with the evidence.

## What an assessment is
**An assessment is the answer, by one rule fixed before any idea is judged and the same for every idea, to whether trading the idea on its own, as the backtest traded it, pays after the backtest's own costs, against its risk, and steadily over time.**

- **"Acting on it" means trading the idea on its own, as tested.** Adding risk control, sizing or combining it with other ideas changes how it trades: that is a later question.
- **It calculates from the backtest's results; it rebuilds nothing.** The book's value after each rebalance and its fees, the trades and the prices are read from the record. No trade is rebuilt and no cost is computed: the costs are the backtest's own.
- **One rule for every idea.** Its values sit in one file, written before any idea is assessed, and never moved after seeing an assessment.
- **Inspired by the old pipeline's profit bars (branch 3), rebuilt.** The same idea of a single bar for all, and the same values, without its deflated Sharpe and its drawdown ceiling, and without its code.

## The fields of an assessment
**In `assessment.md`:**
1. **status** (header): worth acting on, or not worth acting on.
   - For: the answer.
   - Used by: the operator, to decide which ideas to take further.
   - Without it: no answer.
2. **plan, idea, fit and verdict** (header, copied by code).
   - For: tracing the assessment to the idea and its proof; an "adapted" test stays marked.
   - Used by: the operator.
   - Without it: an assessment cannot be traced to what was proven.
3. **The six bars:** for each, its value, the rule, and passed or not.
   - **Sharpe:** the book's gain against its ups and downs.
   - **Sharpe minus holding's Sharpe:** better than simply holding the same coins.
   - **Mean daily return:** large enough to matter.
   - **Lowest Sharpe with one window left out:** not carried by one period.
   - **Calmar:** the yearly return against the deepest fall.
   - **Trades per bar:** the idea acts often enough to be judged.
   - For: the evidence, bar by bar.
   - Used by: the rule, the operator.
   - Without it: a bare word nobody can check.
4. **Decided by:** every bar that passed, or the bars that failed.
   - For: the answer can be challenged.
   - Used by: the operator.
   - Without it: no way to see what to improve.
5. **The book in figures:** the coins, windows, days, years, trades and bars; holding's Sharpe, the yearly return, the deepest fall, and the window whose removal hurts the most.
   - For: reading the bars in context.
   - Used by: the operator.
   - Without it: the bars' values have no scale.

**Next to it:** `result.json` (the same numbers, for code), and the **index line** (`INDEX.md`): `<plan id>: worth acting on | not worth acting on [Sharpe; Sharpe minus holding's; Calmar]`, or `<plan id>: not assessed: the verdict is <status>`.

## The rule (`helper/rule.yaml`)
**Worth acting on** when all six bars pass; otherwise **not worth acting on**.

| Bar | Value (branch 3's) | Passes |
|---|---|---|
| Sharpe | 0 | strictly above |
| Sharpe minus holding's Sharpe | 0 | strictly above |
| Mean daily return | 0.05 % a day (about 20 % a year) | at least |
| Lowest Sharpe, one window left out | 0 | strictly above |
| Calmar | 0.75 | strictly above |
| Trades per bar | 1 % | at least |

Dropped from branch 3: the deflated Sharpe (one idea has one plan, fixed in advance) and the 20 % drawdown ceiling (it was advisory only; Calmar decides on risk).

**Definitions, the same for every idea:**
- **The book of one coin in one window:** the backtest's value after each rebalance and its fees, at the last bar of each day. Daily returns stay inside a window.
- **The idea's book:** all its coins together, equal weight: each day, the mean of the coins' daily returns. **Holding:** the same, from the coins' closing prices.
- **Sharpe:** the mean of all daily returns over their standard deviation, times √365.
- **Calmar:** the yearly return of the daily returns chained in window order, over the deepest fall of that chain.
- **Trades:** the backtest's trades, minus those closed on a window's last bar (forced closes), per bar of the record.

## Storage and naming
Aligned with the other steps.

```
06_applicability/
  card.md                      this card
  helper/
    rule.yaml                  the six bars' values
    make_assessment.py         reads a verdict and its backtest record, applies the rule, saves the assessment
    test_make_assessment.py    tests on hand-made records: numbers recomputed independently, both answers reached
  assessments/
    INDEX.md                   one line per idea
    REVIEW.md, run_log*.txt    once a real run has filled it
    <plan id>/                 assessment.md, result.json
  exercise_k/                  the exercises
```

## The AI
**None. The step is code only.** The rule is the same for every idea, so no judgement is needed per idea: plain code applies it the same way every time, at no cost.

**Checks in code:** an idea whose verdict is not "confirmed", or with no backtest record, is written as "not assessed". `--any-verdict` assesses it anyway, for exercises only, and the assessment says so.

## Quality criteria on the assessment
- **Every number recomputes** from the backtest record and the rule file. Nothing else is read.
- **Nothing is rebuilt:** no trade, no cost, no backtest.
- **The rule is applied as written,** and "decided by" names the bars.
- **The same input gives the same assessment,** always.

## Fixed inputs for the iterations
- **Hand-made records** (in the tests): books built to pass, to lose, to fail on one bad window, and to trade too little. The tests recompute every number independently.
- **Real records, in exercise mode:** the full-data run (6 ideas, 6 coins, 24 windows) and the hourly run (10 ideas). None is confirmed, so they also test "not assessed".

## Variants compared
None: there is no model to compare.

## Who judges the output
The operator: "given these numbers, would I trade this idea on its own?". The tests check the arithmetic.

## Done when
The tests pass, and on the real records every assessment's numbers are consistent with the record and every status follows the rule. Status: met by exercise 1 (`exercise_1/reading.md`).

## To observe
- **No real book has passed yet,** because no idea is confirmed. The "worth acting on" answer is reached only by the hand-made records. A fake market run through the real backtest would test it end to end; not built.
- **Calmar fails most books.** A trend book fell 83 % at its worst over 8 years. Whether 0.75 is right for crypto is to be seen on a real idea.

## What this step does not do
It does not rerun a backtest, rebuild trades or costs, measure the idea again, change how it trades, size positions, combine ideas, or decide on the holdout.
