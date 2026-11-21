# Topic 41: is a paying book a new source of profit, or one we already have?

Status: open (designing: the definitions below, for the operator's review; nothing built)  
Where: research: a function of its own in `orchestration/` (next to `unseen_test`), read by step 7's line 7.f;
shared definitions in `common/measures.md`  
Opened: 2026-11-21, the designer session, from night 3 (`runs/NIGHT3_RUN.md`, the "Check" sections); designed the same
day with the operator ("keep it simple, standard, structured").

## Question
When a book pays, does it make its money on the same bars as a book we already have, or is its profit new?

## Seen
- Night 3: 19 ideas confirmed and profitable, from five different briefs. On 7 of them, the same book without the
  idea's own signal (its 30-day trend condition alone) paid on all six checks, with a Sharpe 0 to 0.15 lower, or higher
  (the 1h rebounds: 1.19 alone against 0.87 to 1.02). The others are momentum outright. Each brief "found" momentum again.
- Step 6 judges one book alone (pass or fail) and compares it with holding its coins; nothing compares it with the
  books already found.
- That night's check edited each config by hand: not one rule for every config shape.

## Why it matters
Without it, runs and briefs are spent rediscovering the same profit, and a book that adds nothing to what we have
looks like a discovery. Tomorrow, books will be combined in one live bot: two books that make money on the same bars
are one bet taken twice (operator, 2026-11-21).

## The business definitions (to go into `common/measures.md` on the operator's go)
1. **A paying book:** a backtest record whose idea step 5 confirmed and step 6 found profitable enough (the loop's
   "goal"), in any run. Only paying books are compared, and only with each other: the question is "do we already have
   this profit?", and only paying books are something we have.
2. **A book's bar returns:** its value at the close of each bar against the close of the bar before, from the record's
   own value series, all its coins together (as step 6 builds its daily returns).
3. **The common bar of two books:** the larger of their two bar sizes (1h with 1h: the hour; 1h with 4h: 4 hours; 1h
   or 4h with 1d: the day). Each book's returns are compounded over that common bar; a bar belongs to the common bar in
   which it closes (UTC blocks: hours, 4-hour blocks from 00:00, days from 00:00, as the data files are cut).
4. **The days compared:** only the common bars both books ran, inside the folds (never the unseen dates). Fewer than a
   minimum span in common (one setting, for the operator: proposed one year) gives "not comparable", not a number.
5. **How much one book explains another (the share explained):** the share of the new book's ups and downs, bar by
   common bar, that the other book's returns explain, reading the other book on the same bar, the bar before and the
   bar after together (the standard correction when two strategies do not act at the same moment). 0 to 100 %, the
   sign does not count: a book that does the opposite of another uses the same effect.
   Reported with it: the **sensitivity** (signed: +1 follows, −1 the opposite), **what is left** per bar (what the new
   book earns beyond the other) and its t, and **which one leads** (the same bar, one bar ahead, one bar behind).
6. **The nearest relative:** the paying book that explains the new one best. Holding the new book's coins is always
   compared too, as the market (what step 6 already compares).
No threshold decides anything: the numbers are reported (visibility, as the rules ask).

What the readings mean (examples, not rules):
| Readings | Meaning |
|---|---|
| nearest relative explains most of it, little left | a profit we already have, whatever its name or sign |
| same, but the new book leads by one bar | the same profit, caught earlier (for example a daily idea caught on the hour) |
| nearest relative explains most of it, something reliably left | a known profit, improved (timing, exit) |
| no paying book explains much, something reliably left | a new source of profit: what the research looks for |

## Where it runs and who reads it
- **A function, `orchestration/paying_books/`** (its card by `HOW_WE_DESIGN_A_CARD.md`), called by `run_idea` with the
  same trigger as the unseen test (confirmed and profitable). It adds the book to **the register of paying books**
  (each book's bar returns as one small committed file, its run, idea, bar size, coins, engine version) and writes the
  book's comparison with every other paying book and with holding.
- **Readers:** line 7.f (real and profitable: what next) reads the comparison; the operator; later the briefs, through
  the findings.
- **Step 6 is not changed.** The daily returns it builds for its own measures are built the same way here (one
  definition, `common/measures.md`), so the two cannot disagree.

## Before the first comparison
- The paying books found so far (about 40 in all runs) are rerun once on today's engine and costs (the holding rule, the
  measured slippage): otherwise a new book is compared with books charged other costs. Steps 4 and 6 only, no model
  call.
- The register then holds them, with their bar returns.

## Plan (for the operator's go)
| # | Change | Gain | Effort | Risk |
|---|---|---|---|---|
| 1 | Definitions 1 to 6 in `common/measures.md`; the function's card | one meaning before any code | small | none |
| 2 | The function, with tests on books whose answer is known by construction (a book equal to another: 100 % explained; the same book one bar later: 100 % with a lag; noise: about 0 %) | the comparison for every new paying book | medium (one helper, the register) | none to the steps: nothing they decide changes |
| 3 | The paying books so far rerun on today's engine (steps 4 and 6), then added to the register | references on equal terms | CPU only, about 40 backtests | some may no longer pay under today's costs: reported, not hidden |
| 4 | Proof: the comparisons read on night 3's 19 paying books against the hand controls already run (they should read "a profit we already have") and on step 7 A/B's 1-day reversal (it should read differently) | shows the measure says what the controls said, with one rule | small | if they disagree, the definition is wrong: rework it before use |
| 5 | `run_idea` calls it; line 7.f reads its file | every new paying book compared at once | small | none |

Not in this topic: grouping books into families (next, with the operator), the two measures of topic 42, combining
books in one live bot (it will use the register).

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-21 | Compare a paying book with the other paying books, one by one, not with a strategy invented as a reference | the operator ("why don't we use already tested profitable strategies, and why not all") | no setting invented; a new known effect enters by itself | a momentum reference (a setting of ours); one pooled portfolio of all paying books (it blurs the effects: a copy of a rare book would read as new) |
| 2026-11-21 | Paying books compared only with paying books, in every run | the operator, on the designer's proposal | the question is "do we already have this profit?" | every book run (hundreds; a failed twin answers another question) |
| 2026-11-21 | Its own function next to the unseen test, read by 7.f; step 6 unchanged | the operator ("is it really step 6 or 7.d? I do not think so") | it is about the set of what we found, not one book's pass or fail | inside step 6 or line 7.d |
| 2026-11-21 | Two books compared at the larger of their two bar sizes (1h with 1h: the hour; 1h with 4h: 4 hours; with 1d: the day) | the operator | one rule; and intraday books will be combined in one live bot | the day for every pair (it hides when, within the day, two intraday books hold) |
| 2026-11-21 | The other book read on the same bar, the bar before and the bar after; the sign does not count | the operator's remark (a book shorting momentum still uses momentum); the designer | the same profit caught one bar apart, or reversed, is the same profit | correlation alone |

## Status and next
Waiting for the operator's go on the definitions and the one setting (the minimum span in common: one year proposed),
then the plan in order.

## Links
`runs/NIGHT3_RUN.md`, `orchestration/unseen_test/card.md`, `07f_real_and_profitable/card.md`, `06_profitability/card.md`,
`common/measures.md`, topics 08 (books together), 42.
