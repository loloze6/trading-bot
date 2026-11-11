# Step card 6: Profitability (2026-11-11)

## Business objective, one question
Is this backtest's book profitable enough?

**Establish whether the book a backtest traded pays, after the backtest's own costs, against its risk and steadily over time, by one rule fixed in advance and applied the same way to every backtest.**

## Input
One backtest record.

## Output
One profitability check per backtest: **profitable enough** or **not profitable enough**, with the evidence.

## What a profitability check is
**A profitability check is the answer, by one rule fixed before any backtest is checked and the same for every backtest, to whether the book the backtest traded pays after the backtest's own costs, against its risk, and steadily over time.**

- **The book is what the backtest traded:** its value after each rebalance and its fees, on every coin and window it ran. Nothing is added to it, such as sizing or risk control.
- **It calculates; it rebuilds nothing.** The book's value, the trades and the prices are read from the record. No trade is rebuilt and no cost is computed: the costs are the backtest's own.
- **One rule for every backtest,** in one file, written before any check and never moved after seeing one.

## The fields of a check
**In `check.md`:**
1. **status** (header): profitable enough, or not profitable enough.
   - For: the answer.
   - Used by: the operator.
   - Without it: no answer.
2. **backtest and data** (header, copied by code): the record's name, its coins, bar size and period.
   - For: what was checked.
   - Used by: the operator.
   - Without it: a check cannot be traced to its backtest.
3. **The six measures:** for each, its value, the rule, and passed or not.
   - **Sharpe:** the book's gain against its ups and downs.
   - **Sharpe minus holding's Sharpe:** better than simply holding the same coins.
   - **Mean daily return:** large enough to matter.
   - **Lowest Sharpe with one window left out:** not carried by one period.
   - **Calmar:** the yearly return against the deepest fall.
   - **Trades per bar:** the book trades often enough to be judged.
   - For: the evidence, measure by measure.
   - Used by: the rule, the operator.
   - Without it: a bare word nobody can check.
4. **Decided by:** "every measure passed", or the measures that failed.
   - For: the answer can be challenged.
   - Used by: the operator.
   - Without it: no way to see what failed.
5. **The book in figures:** coins, windows, days, years, trades and bars; holding's Sharpe, the yearly return, the deepest fall, and the window whose removal lowers the Sharpe most.
   - For: reading the measures in context.
   - Used by: the operator.
   - Without it: the measures have no scale.

**Next to it:** `result.json` (the same numbers, for code), and the **index line** (`INDEX.md`): `<backtest>: profitable enough | not profitable enough [Sharpe; Sharpe minus holding's; Calmar]`, or `<backtest>: not checked: the record holds no window that ran`.

## The rule (`helper/rule.yaml`)
**Profitable enough** when all six measures pass; otherwise **not profitable enough**. The values are those of the old pipeline's profit bars, without its deflated Sharpe and its drawdown ceiling.

| Measure | Value | Passes |
|---|---|---|
| Sharpe | 0 | strictly above |
| Sharpe minus holding's Sharpe | 0 | strictly above |
| Mean daily return | 0.05 % a day (about 20 % a year) | at least |
| Lowest Sharpe, one window left out | 0 | strictly above |
| Calmar | 0.75 | strictly above |
| Trades per bar | 1 % | at least |

**Definitions, the same for every backtest:**
- **The book of one coin in one window:** the backtest's value after each rebalance and its fees, at the last bar of each day. Daily returns stay inside a window.
- **The backtest's book:** all its coins together, equal weight: each day, the mean of the coins' daily returns. **Holding:** the same, from the coins' closing prices.
- **Sharpe:** the mean of all daily returns over their standard deviation, times √365.
- **Calmar:** the yearly return of the daily returns chained in window order, over the deepest fall of that chain.
- **Trades:** the backtest's trades, minus those closed on a window's last bar (forced closes), per bar of the record.

## Storage and naming
```
06_profitability/
  card.md                        this card
  helper/
    rule.yaml                    the six measures' values
    check_profitability.py       one backtest record -> its check; adds the index line
    test_check_profitability.py  tests on hand-made records: numbers recomputed independently, both answers reached
  checks/
    INDEX.md                     one line per backtest
    REVIEW.md, run_log*.txt      once a real run has filled it
    <backtest>/                  check.md, result.json
  exercise_k/                    the exercises
```

## The AI
**None. The step is code only.** The rule is the same for every backtest, so no judgement is needed: plain code applies it the same way every time, at no cost.

**Checks in code:** a record with no window that ran is written as "not checked".

## Quality criteria on the check
- **Every number recomputes** from the backtest record and the rule file. Nothing else is read.
- **Nothing is rebuilt:** no trade, no cost, no backtest.
- **The rule is applied as written,** and "decided by" names the measures.
- **The same record gives the same check,** always.

## Fixed inputs for the iterations
- **Hand-made records** (in the tests): books built to pass, to lose, to fail on one bad window, and to trade too little.
- **Real records:** the full-data run (6 backtests: 6 coins, 24 windows) and the hourly run (10 backtests).

## Variants compared
None: there is no model to compare. Exercises 1 and 2 ran an earlier form of this step (an applicability gate, then the same rule on every backtest); exercise 3 runs this form, with the same numbers.

## Who judges the output
The operator: "given these numbers, would I trade this book?". The tests check the arithmetic.

## Done when
The tests pass, and on the real records every check's numbers are consistent with the record and every status follows the rule. Status: met by exercise 3 (`exercise_3/reading.md`).

## To observe
- **No real book has passed yet.** "Profitable enough" is reached only by the hand-made records.
- **Calmar fails most books.** A trend book fell 83 % at its worst over 8 years. Whether 0.75 is right for crypto is to be seen on more books.

## What this step does not do
It does not rerun a backtest, rebuild trades or costs, change how the book trades, or judge the idea behind the book.
