# Function card: ideas_similarities_check (orchestration, 2026-11-21; named by the operator)

## Business objective, one question
Is a book that pays a new source of profit, or one we already have? And is a real idea whose book does not pay a profit we already earn, or a variation (operator, 2026-11-22)?

**Establish, for every paying book (step 5 confirmed, step 6 profitable enough), how much of its gains and losses the
books we already have account for, which of them is its nearest relative, who of the two acts first, and what it earns
that they do not, so that a profit already found is not counted again as a discovery** (operator, 2026-11-21; topic 41).
**And the same for every confirmed book whose book does not pay, against the paying books, so that the real ideas that
differ from what we earn stay visible; for a repair (line 7.d), also against the idea it repairs, so that a repair that
drifted to another effect shows** (operator, 2026-11-22; topic 45: the idea's verdict had been forgotten, and 7.d's
ideas drifted to momentum).
Why: on night 3, 19 ideas paid from five different briefs; checked against their own trend condition alone, the 7
checked added 0 to 0.15 of Sharpe or less (`runs/NIGHT3_RUN.md`). Tomorrow, books will be combined in one live bot: two
books that make money on the same bars are one bet taken twice.

## Input
- One paying or confirmed book: its backtest record (`04_backtest/<run>/backtests/<id>/`, with each window's `bars.csv.gz`, or
  its committed `chart_bars.csv.gz` when the bars are not on this machine) and its
  step 5 and step 6 results (`05_verification/<run>/verdicts/<id>/result.json`, `06_profitability/<run>/checks/<id>/result.json`).
- The register (below): the paying and confirmed books already there.

## Output
- The book added to the register: its bar returns (one small file; committed for a paying book, local for a confirmed one) and its line, with its kind.
- Its comparison with every paying book of the register (and, for a repair, with its parent) and with holding its coins:
  `<id>.json` and `<id>.md`, one line in the register's `COMPARISONS.md` (its paying books, then its confirmed books from
  the least explained).
- **The similarity matrix of the paying books** (operator, 2026-11-22; `../../common/measures.md`), rewritten with every
  summary: `register/MATRIX.md` (the numbered books, then one row and one column per book, the share explained in
  hundredths, "-" under one year in common; similar books together, so families show as blocks) and
  `register/matrix.csv` (one line per ordered pair: book, other, comparison timeframe, share explained, direction, who
  leads), for code. Business meaning: which paying books are one bet and which are different, the map for combining
  books in one bot (topic 44).

## What a comparison is
**The new book's returns set against another paying book's, period by period, on the comparison timeframe and the window
in common, read on the same period, the period before and the period after; the definitions are in `common/measures.md`
("A paying book, and what it shares with the books we have").**
- **It records; it decides nothing.** No threshold, no gate: the numbers are reported; the operator reads them (who else reads them is open: topic 41).
- **It compares paying books with paying books only:** the question is whether we already have this profit, and only
  paying books are something we have.
- **One rule for every pair**, whatever the bar sizes, coins or configs: the larger bar size, the periods in common.

## The fields of a comparison (`<id>.json`, one entry per other book, and one for holding)
1. **other:** the other book (run and id), its bar size and its coins.
   - For: which book this is about. Used by: the operator. Without it: a number with no book.
2. **comparison_timeframe:** the larger of the two bar sizes.
   - For: the precision of the comparison. Used by: the reader. Without it: an hour and a day read alike.
3. **window_in_common:** the first and last period in common, their count, and the span in days; "not comparable" under
   one year.
   - For: how much evidence the result rests on. Used by: the reader. Without it: a result on a few weeks reads as sure.
4. **share_explained** (0 to 1): the largest of the three readings.
   - For: how much of this profit we already have. Used by: the operator. Without it: a copy reads as new.
5. **who_leads:** the reading it came from: `same period`, `new one period ahead`, `new one period behind`.
   - For: the same profit caught earlier shows. Used by: the operator (which version to keep). Without it: a book
     one period apart reads as unrelated.
6. **direction:** `+` (moves with) or `−` (against).
   - For: the same effect used the other way round is still the same effect. Used by: the reader. Without it: a reversed
     copy reads as a new, opposite profit.
7. **what_is_left:** the mean return per period the other book does not explain, and its t.
   - For: what the new book really adds. Used by: the operator. Without it: "explained" says nothing of what remains.
8. **readings:** the three shares (same period, period before, period after), for checking.
   - For: auditing who leads. Used by: the operator. Without it: who leads cannot be checked.

And for the book: **nearest_relative** (the other paying book with the largest share explained, among those comparable)
and **against_holding** (fields 2 to 8 against holding its own coins).

## Storage and naming
```
orchestration/ideas_similarities_check/
  card.md                      this card
  helper/
    ideas_similarities_check.py            add a book to the register and compare it; --all compares every book again
    book_returns.py            a record's bar returns, per window (the definition in common/measures.md)
    test_ideas_similarities_check.py       its tests, on books whose answer is known by construction (no backtest, no model call)
  register/
    INDEX.md                   one line per paying book: run, id, bar size, coins, engine (git sha), made on
    books.json                 the same, for code
    returns/<run>__<id>.csv.gz one book's bar returns: window, period start (UTC), return; and holding's return
    comparisons/<run>__<id>.json and .md   its comparison with every other book and with holding
    COMPARISONS.md             one line per book: its nearest relative, share explained, who leads, what is left (t)
```
The bar returns are committed (about 1.3 MB per hourly book, 7 significant digits): the records' bars are kept local only, and a
new session must find the register whole.

## Who calls it, and when
- **`run_idea`** (operator, 2026-11-22; topic 41), after step 6 and the chart files, for every idea step 5 confirmed, its
  book paying or not: the book added and compared (code only, no model call). `select_next` reads the register to order
  the next ideas (the parent's difference). A failure is recorded in the run's journal and the run goes on.
- **Parallel sessions** each add their run's books on their own branch. When their branches are merged, `books.json`,
  `INDEX.md` and `COMPARISONS.md` conflict: `books.json` is resolved as the union of both sides' rows (keys are unique,
  `<run>__<id>`), then `--all` compares every book again and rewrites `INDEX.md` and `COMPARISONS.md`, so a book added on
  one branch is compared with those added on the other.
- **The operator** (or the designer, on the operator's go), with `--all`, to compare every book again (after the
  register is first filled, or a book is rerun).

## How to call it
```
python3 orchestration/ideas_similarities_check/helper/ideas_similarities_check.py RECORD --run NAME_run      # one book
python3 orchestration/ideas_similarities_check/helper/ideas_similarities_check.py --all                       # every book again
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
- The register's files above, committed. (A journal line in `run_idea` comes with its call, if decided: topic 41.)

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
Code: the numbers. The operator: what a book adds, which to keep.

## Done when
The tests pass; daily returns equal step 6's on 3 records; the register holds every paying book on today's engine; the
comparisons on night 3's books agree with the hand checks.
Status: **met** (`validation/reading.md`, 2026-11-22): 35 paying books in the register; the comparisons agree with night 3's
hand checks.

## What it changes elsewhere (each in its own card)
- None yet (`run_idea`'s call is open: topic 41).

## What this function does not do
It does not judge whether a book pays (step 6), choose ideas, gate anything, group books into families, or combine books
in a live bot.
