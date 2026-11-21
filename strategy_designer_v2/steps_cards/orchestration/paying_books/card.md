# Function card: paying_books (orchestration, 2026-11-21)

## Business objective, one question
Is a book that pays a new source of profit, or one we already have?

**Establish, for every paying book (step 5 confirmed, step 6 profitable enough), how much of its gains and losses the
books we already have account for, which of them is its nearest relative, who of the two acts first, and what it earns
that they do not, so that a profit already found is not counted again as a discovery** (operator, 2026-11-21; topic 41).
Why: on night 3, 19 ideas paid from five different briefs; checked against their own trend condition alone, the 7
checked added 0 to 0.15 of Sharpe or less (`runs/NIGHT3_RUN.md`). Tomorrow, books will be combined in one live bot: two
books that make money on the same bars are one bet taken twice.

## Input
- One paying book: its backtest record (`04_backtest/<run>/backtests/<id>/`, with each window's `bars.csv.gz`) and its
  step 5 and step 6 results (`05_verification/<run>/verdicts/<id>/result.json`, `06_profitability/<run>/checks/<id>/result.json`).
- The register of paying books (below): the books already there.

## Output
- The book added to the register: its bar returns (one small file) and its line.
- Its comparison with every book of the register and with holding its coins: `<id>.json` and `<id>.md`, one line in the
  register's `COMPARISONS.md`.

## What a comparison is
**The new book's returns set against another paying book's, period by period, on the comparison timeframe and the window
in common, read on the same period, the period before and the period after; the definitions are in `common/measures.md`
("A paying book, and what it shares with the books we have").**
- **It records; it decides nothing.** No threshold, no gate: the numbers are reported; line 7.f and the operator read them.
- **It compares paying books with paying books only:** the question is whether we already have this profit, and only
  paying books are something we have.
- **One rule for every pair**, whatever the bar sizes, coins or configs: the larger bar size, the periods in common.

## The fields of a comparison (`<id>.json`, one entry per other book, and one for holding)
1. **other:** the other book (run and id), its bar size and its coins.
   - For: which book this is about. Used by: the operator, 7.f. Without it: a number with no book.
2. **comparison_timeframe:** the larger of the two bar sizes.
   - For: the precision of the comparison. Used by: the reader. Without it: an hour and a day read alike.
3. **window_in_common:** the first and last period in common, their count, and the span in days; "not comparable" under
   one year.
   - For: how much evidence the result rests on. Used by: the reader. Without it: a result on a few weeks reads as sure.
4. **share_explained** (0 to 1): the largest of the three readings.
   - For: how much of this profit we already have. Used by: 7.f, the operator. Without it: a copy reads as new.
5. **who_leads:** the reading it came from: `same period`, `new one period ahead`, `new one period behind`.
   - For: the same profit caught earlier shows. Used by: 7.f, the operator (which version to keep). Without it: a book
     one period apart reads as unrelated.
6. **direction:** `+` (moves with) or `−` (against).
   - For: the same effect used the other way round is still the same effect. Used by: the reader. Without it: a reversed
     copy reads as a new, opposite profit.
7. **what_is_left:** the mean return per period the other book does not explain, and its t.
   - For: what the new book really adds. Used by: 7.f, the operator. Without it: "explained" says nothing of what remains.
8. **readings:** the three shares (same period, period before, period after), for checking.
   - For: auditing who leads. Used by: the operator. Without it: who leads cannot be checked.

And for the book: **nearest_relative** (the other paying book with the largest share explained, among those comparable)
and **against_holding** (fields 2 to 8 against holding its own coins).

## Storage and naming
```
orchestration/paying_books/
  card.md                      this card
  helper/
    paying_books.py            add a book to the register and compare it; --all compares every book again
    book_returns.py            a record's bar returns, per window (the definition in common/measures.md)
    test_paying_books.py       its tests, on books whose answer is known by construction (no backtest, no model call)
  register/
    INDEX.md                   one line per paying book: run, id, bar size, coins, engine (git sha), made on
    books.json                 the same, for code
    returns/<run>__<id>.csv.gz one book's bar returns: window, period start (UTC), return; and holding's return
    comparisons/<run>__<id>.json and .md   its comparison with every other book and with holding
    COMPARISONS.md             one line per book: its nearest relative, share explained, who leads, what is left (t)
```
The bar returns are committed (a few hundred kilobytes per hourly book): the records' bars are kept local only, and a
new session must find the register whole.

## Who calls it, and when
- **`run_idea`**, after the unseen test, for an idea step 5 confirmed and step 6 found profitable enough (the same rule
  and the same place as the unseen test, so no step 7 line of that idea reads it before it ran).
- **The operator** (or the designer, on the operator's go), with `--all`, to compare every book again (after the
  register is first filled, or a book is rerun).

## How to call it
```
python3 orchestration/paying_books/helper/paying_books.py RECORD --run NAME_run      # one book
python3 orchestration/paying_books/helper/paying_books.py --all                       # every book again
```

## When something fails
- **The record is not a paying book** (no confirmed verdict, or no profitable check): refused (exit 1, its message).
- **A window's bars are missing** (kept local only, not on this machine): refused with the message "bars not found:
  rerun step 4 on the plan"; nothing is written.
- **A pair with under one year in common:** written as "not comparable", not left out.

## Checks in code
- The book is paying (step 5 and step 6 files read, never assumed).
- Returns are computed inside each window only; a period is kept only where both books have a return.
- Each comparison's three readings use the same periods' lagged pairs only (no period across a window gap).

## Visibility
- `run_idea`'s journal: one line `paying_books` (called or skipped, seconds, 0 USD).
- The register's files above, committed.

## The AI
None: code only. Cost: 0 USD; seconds per book.

## Quality criteria
- **Known answers by construction:** a book equal to another reads share 1, same period, +; the same book one period
  later reads share 1, one period behind; its opposite, share 1, −; noise, about 0; no window in common, not comparable.
- **The same as step 6 on the day:** a book's daily returns from `book_returns.py` equal step 6's daily book returns on
  the same record (one definition).
- **On night 3's books, the comparisons say what the hand checks said:** the 7 checked ideas read "a profit we already
  have" (their nearest relative explains most of them, little left).

## Fixed inputs for the iterations
Night 3's paying books (`runs/NIGHT3_RUN.md`) and the step 7 A/B set B's 1-day reversal, against the hand checks.

## Variants compared
None.

## Who judges the output
Code: the numbers. Line 7.f and the operator: what a book adds, which to keep.

## Done when
The tests pass; daily returns equal step 6's on 3 records; the register holds every paying book on today's engine; the
comparisons on night 3's books agree with the hand checks.
Status: **designed, not built.**

## What it changes elsewhere (each in its own card)
- `run_idea`: the call after the unseen test (a journal line).
- Line 7.f: reads the book's comparison (`<id>.md`) with the step 6 check.

## What this function does not do
It does not judge whether a book pays (step 6), choose ideas, gate anything, group books into families, or combine books
in a live bot.
