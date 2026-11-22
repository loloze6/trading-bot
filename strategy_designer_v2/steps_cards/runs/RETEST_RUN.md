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
| 3 (added 2026-11-23, about 00:15 Paris) | `retest_settlement_run` | 017 settlement-hour moves, 1h | 017-05 settlement move reverses after (0.01); 017-02.g2 hourly reversal in volatile periods (0.01); 017-01.g2 hourly move reversal by volatility (0.01) | 35 USD |

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

## Session 4: a new category, brief 030 (added 2026-11-23, about 00:15 Paris; the operator: "one suggested brief you would select")
`brief_absorption_run`, `run_brief` with `01_brief/briefs/030_absorption-day-close-location.md` (1d; step 1 wrote it
from the theme "a day of very heavy volume with little net price change, where a large order is absorbed: does where
the price closes in the day's range show which side absorbed it and which way the coin moves next?"), 35 USD. Chosen
over calendar and session flows (1h: no 2026 hourly data for the unseen test) and volatility timing (long the market
most of the time: likely what we earn). The same rules; the same measures.
| Outcome | What the counts would show | Meaning |
|---|---|---|
| A1. A new family | a book confirmed, profitable, holding on the unseen dates, its nearest paying book under 0.25 | absorption pays on its own |
| A2. Real, not yet paying | confirmed ideas, none profitable; their repairs (line 7.d) tested | the chain at work on a new effect |
| A3. Momentum again | the paying books explained 0.5 or more by a paying book | the brief drifted despite the changes |
| A4. Not real | few confirmed | absorption is not in the daily bars |

## In the designer session, no model cost: the books the new step 6 now passes
Step 6 counted on days in a position (2026-11-22) turned two confirmed books profitable enough: `volume_run`'s
011-01.g2 heavy-volume falls reverse (in a position 16 % of days; its nearest paying book explains 0.25) and
`night_013_run`'s 013-01.d2 nearness with rising month (57 %). Neither went through the unseen test. Expected: if
011-01.g2 holds on both unseen periods, it is a candidate for the second family (R1's measure: under 0.25 is not met,
0.25 exactly: read with its parent and its family).
