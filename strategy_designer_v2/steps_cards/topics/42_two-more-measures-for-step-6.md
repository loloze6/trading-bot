# Topic 42: two more measures for step 6, the book's standard deviation and its total profit over the period

Status: built 2026-11-22 (two informative measures in step 6)  
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
| 2026-11-22 | The daily standard deviation, and the yearly return instead of a total over the period; both informative measures (shown, in no rule), a category defined in `common/measures.md` | the operator, on the designer's challenge of the total | per year, books tested over different lengths compare; the total grows with the period's length and with the size step 3 chose; the yearly return is Calmar's numerator, so it cannot disagree with it | the total over the period; the share of windows that made money, the worst window, the costs' share of the profit before costs (not needed for now) |

## Status and next
Built (2026-11-22): `common/measures.md` (an informative measure; the two definitions), step 6's card, `check_profitability.py` (`check.md`: an informative-measure table; `result.json`: `informative`), a test. Proof: step 6 rerun on the 317 records whose bars are on this machine: no status changed; 302 of 303 index lines identical; the differences are the 2026-11-18 label "trades per day" on 149 older checks and one old-engine hourly record whose local bars are not its record's (left as recorded).

## Links
`06_profitability/card.md`, `common/measures.md`, topic 41.
