# Topic 41: is a paying book a new source of profit, or one we already have?

Status: open (designing: definitions and outputs agreed with the operator, 2026-11-21; nothing built)  
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
   "goal"), in any run. Paying books are compared only with each other: the question is "do we already have this
   profit?", and only paying books are something we have. An idea rerun in several runs counts once (its latest record).
2. **A book's bar returns:** its value at the close of each bar against the close of the bar before, read from the
   record's own value series, all its coins together (built the way step 6 builds its daily returns).
3. **The comparison timeframe of two books:** the larger of their two bar sizes (1h with 1h: the hour; 1h with 4h: 4
   hours; 1h or 4h with 1d: the day). Each book's returns are compounded over that timeframe; a bar belongs to the bar
   of the comparison timeframe in which it closes (UTC: hours, 4-hour blocks from 00:00, days from 00:00, as the data
   files are cut).
4. **The window in common:** the bars of the comparison timeframe both books ran, inside the folds (never the unseen
   dates). Every output uses these bars only: a period only one book ran cannot move any number. Under one year in
   common (the operator, 2026-11-21), the pair is "not comparable".

## The outputs, for a new paying book against one other paying book
How it is computed, once: the share of the new book's returns explained by the other book's returns (a one-variable
regression over the window in common), read three times: the other book on the same bar, one bar earlier, one bar
later. The largest of the three gives the share explained and who leads.
| Output | Definition | Business meaning |
|---|---|---|
| **Comparison timeframe** | the larger of the two bar sizes | the precision of the comparison: the hour, 4 hours or the day |
| **Window in common** | the span both books ran inside the folds, with its length | how much evidence the result rests on; under one year: not comparable |
| **Share explained** | the share (0 to 100 %) of the new book's gains and losses, bar by bar, that the other book's gains and losses account for; the largest of the three readings | how much of this profit we already have: 90 % is almost the same book, 5 % is unrelated |
| **Direction** | whether the new book moves with the other (+) or against it (−), in that reading | "−" with a large share explained: the same effect used the other way round, still not new |
| **Who leads** | the reading the share explained came from: the same bar, the new book one bar ahead, or one bar behind | "one bar ahead": the same profit caught earlier (for example a daily idea caught on the hour) |
| **What is left** | the new book's mean return per bar that the other book does not explain, and its t | what the new book really adds: about 0, nothing new; reliably above 0, a profit of its own |

And, for each new paying book:
| Output | Definition | Business meaning |
|---|---|---|
| **Nearest relative** | the paying book with the largest share explained, with its outputs above | "mostly a copy of X", or "no book we have explains it" |
| **Against holding** | the same outputs against holding the book's own coins | how much of the profit is the market rising (what step 6's "Sharpe minus holding's" already looks at) |

No threshold decides anything: the numbers are reported (visibility, as the rules ask).

What the outputs mean together (examples, not rules):
| Outputs | Meaning |
|---|---|
| nearest relative: large share explained, little left | a profit we already have, whatever its name or sign |
| same, the new book one bar ahead | the same profit, caught earlier |
| large share explained, something reliably left | a known profit, improved (timing, exit) |
| no paying book explains much, something reliably left | a new source of profit: what the research looks for |

**Limit, stated in the card:** a lead of more than one bar of the comparison timeframe does not show (between two 1h
books, a lead of 3 hours). Widened only if a run shows it is needed.

## Where it runs and who reads it
- **A function, `orchestration/paying_books/`** (its card by `HOW_WE_DESIGN_A_CARD.md`), called by `run_idea` with the
  same trigger as the unseen test (confirmed and profitable). It adds the book to **the register of paying books**
  (each book's bar returns as one small committed file, its run, idea, bar size, coins, engine version) and writes the
  book's comparison with every other paying book and with holding.
- **Readers:** line 7.f (real and profitable: what next) reads the comparison; the operator; later the briefs, through
  the findings.
- **Step 6 is not changed.** The daily returns it builds for its own measures are built the same way here (one
  definition, `common/measures.md`), so the two cannot disagree.

## Before the first comparison: the older paying books rerun, before and after
41 paying records, made under three engines (counted from their manifests, 2026-11-21):
| Made on | Records | Holding rule (each bet held for the idea's horizon) | Trading cost |
|---|---|---|---|
| 14 to 19 November | 14 | none: re-sized every bar | the old guessed slippage (7.5 bps default) |
| 20 November, before 10:30 Paris | 6 | an earlier version, with the 3 defects found case by case | the old guess |
| 21 November | 21 | the corrected rule | the measured slippage (topic 38) |
The speed changes A to D change no result (proven). The holding rule changes when a book is in a position, so two
books with the same idea, one with it and one without, would look less alike than they are.
- The 20 older records are rerun once on today's engine and costs (steps 4 and 6, no model call); the register holds
  the rerun books.
- **Before and after, for each of them:** step 6's six measures and its verdict, as recorded and as rerun, in one
  table: what the holding rule and the measured costs changed on books already trusted, and which, if any, no longer
  pays. A proof of those two changes on real books (the operator, 2026-11-21).

## Plan (for the operator's go)
| # | Change | Gain | Effort | Risk |
|---|---|---|---|---|
| 1 | The definitions and the outputs above in `common/measures.md`; the function's card | one meaning before any code | small | none |
| 2 | The function, with tests on books whose answer is known by construction (a book equal to another: 100 % explained, same bar; the same book one bar later: 100 %, one bar behind; the opposite book: 100 %, direction −; noise: about 0 %; no window in common: not comparable) | the comparison for every new paying book | medium (one helper, the register) | none to the steps: nothing they decide changes |
| 3 | The 20 older paying records rerun on today's engine (steps 4 and 6), the before and after table, then every paying book added to the register | references on equal terms; the holding rule and the measured costs proven on real books | CPU only, 20 backtests | some may no longer pay: reported, not hidden |
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
| 2026-11-21 | Three readings (same bar, one bar ahead, one bar behind), reported as one share explained (the largest) and who leads; the sign does not count | the operator's remarks (a book shorting momentum still uses momentum; "would we still see that A is a bit sooner?"), the designer | the same profit caught one bar apart, or reversed, is the same profit, and which one is sooner shows | correlation alone; the three shares all reported (more reading for little gain) |
| 2026-11-21 | Names: comparison timeframe, window in common; only the bars in common are used; one year minimum | the operator | - | - |
| 2026-11-21 | The 20 older paying records rerun on today's engine, with a before and after table | the operator | references on equal terms; a proof of the holding rule and the measured costs on real books | keeping them as recorded (biased: other holding, other costs) |

## Status and next
The definitions agreed with the operator (2026-11-21); next: the plan in order, step 1 first (the definitions in
`common/measures.md` and the function's card), on the operator's go to build.

## Links
`runs/NIGHT3_RUN.md`, `orchestration/unseen_test/card.md`, `07f_real_and_profitable/card.md`, `06_profitability/card.md`,
`common/measures.md`, topics 08 (books together), 42.
