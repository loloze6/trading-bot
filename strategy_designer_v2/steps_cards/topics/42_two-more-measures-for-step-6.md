# Topic 42: two more measures for step 6, the book's standard deviation and its total profit over the period

Status: open (parked)  
Where: research: step 6 (`06_profitability/`), `common/measures.md`  
Opened: 2026-11-21, the operator: "park two new metrics for step 6: standard deviation of the portfolio, global profit
over the period".

## Question
Should step 6 also report how much the book's value moves from day to day (its standard deviation) and how much it
made in all over the period tested?

## Seen
- Step 6 reports Sharpe, Sharpe minus holding's, the mean daily return, the lowest Sharpe with one window left out,
  Calmar and trades per day. The standard deviation is inside the Sharpe but not shown; the total profit is not shown.

## Why it matters
Two books with the same Sharpe can move very differently in size, and the total profit is what an investor reads first.

## Options
To be designed when opened (business definition first, in `common/measures.md`: over which dates, per window or over
the whole period, simple or compounded).

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-21 | Parked | the operator | - | - |

## Status and next
Parked.

## Links
`06_profitability/card.md`, `common/measures.md`, topic 41.
