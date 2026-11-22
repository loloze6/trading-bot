# Night 5 (2026-11-22): the new chain retested on briefs that had real non-momentum ideas (written before the runs)

**The operator's go (2026-11-22, evening):** "testing the decide-next and the ideas generation ... on briefs that had
potential but drifted to momentum, then backtest, and see if we finally find an idea profitable and with no
similarities". Same setup and rules as night 4 (`runs/NIGHT4_RUN.md`).

**What changed since those briefs ran (topic 45):** line 7.d runs only on a confirmed idea whose book does not pay and
writes repairs that keep the idea (the self-check measured; a closure only when no version of the effect can be
traded); `select_next` puts first the ideas written from a confirmed idea unlike what we earn (priority = score x w, w
the parent's difference); `run_idea` adds every confirmed book to the similarity register; step 6 counts the mean daily
return on days in a position; step 3 enforces the brief's side.

| Session | Run | Brief, bar | Starting ideas (confirmed, not paying; share explained by the nearest paying book; Sharpe) | Budget |
|---|---|---|---|---|
| 1 | `retest_weekend_run` | 026 weekend moves, 1h | 026-03.d3 Saturday move continues early week (0.05; 1.08); 026-04.b2 heavy weekend moves continue (0.07; 0.89) | 35 USD |
| 2 | `retest_learned_run` | 022 learned combination, 1d | 022-04.b1 nearness power turns around (0.03; 0.92); 022-04.b2 volatility power turns around (0.01; 0.68) | 35 USD |

Each session: `run_idea` on its two starting ideas (retested under today's rules), then the loop on the run with the
budget. Night 4's rules: a loop the 2-hour limit cuts is restarted at once; a usage-limit stop resumed after its reset;
commits along the way; no new idea after 07:00 UTC (09:00 at most); the similarity register is written by `run_idea`
on the session's branch (merged in the morning: the union of `books.json`, then `--all`).

**Measures:** ideas, plans, confirmed, profitable enough, holding on the unseen dates; the share of tested ideas from
`select_next`'s group 2; 7.d's ideas that are repairs, and the trend conditions they add (measured alone?); for each
paying book, its nearest paying book and its share, and for a repair its share explained by its parent.

| Outcome | What the counts would show | Meaning |
|---|---|---|
| R1. Found | a book confirmed, profitable, holding on the unseen dates, whose nearest paying book explains under 0.25 | the second family topic 44 waits for |
| R2. Pays but drifted | a repair that pays but that a paying book explains 0.5 or more, more than its parent does | 7.d's self-check let momentum through |
| R3. Real, still not paying | repairs confirmed, none profitable | the effect is real; no version tested pays yet |
| R4. Not real | the repairs not confirmed | the repair changed the idea too much |

**Limits:** the hourly run has no 2026 data for the unseen test (2016-17 only); the account's 7-day usage limit is at its
warning level.
