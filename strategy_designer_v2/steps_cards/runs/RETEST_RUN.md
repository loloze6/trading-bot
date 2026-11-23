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
| 5 (added 2026-11-23, about 00:40 Paris; the operator: quota to use) | `retest_monday_run` | 011 weekend rise reverses on Monday, 1d | 011-01.b2.b1 Sunday move reverses both ways (0.06); 011-01.b2.b2 weekend fall rebounds Monday-Tuesday (0.06) | 35 USD |

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

**Read (2026-11-23, about 00:30 Paris; 0 USD):**
| Book | Nearest paying book (share) | Unseen 2016-17 | Unseen 2026 |
|---|---|---|---|
| 011-01.g2 heavy-volume falls reverse | 005-02...g2 volatile reversal completes quickly (0.25) | holds (Sharpe 1.11; step 5 inconclusive, t 2.37) | does not hold (Sharpe −0.86, t −0.38) |
| 013-01.d2 nearness with rising month | 001-01...c1 high-RSI continuation (0.74) | holds | holds |
Not a second family: the reversal book fails 2026, as the daily reversal book of `runs/COMBINE_TEST_RUN.md` did; the
book that holds is momentum (0.74 explained). Their in-sample checks stay as recorded (written under step 6 before
2026-11-22).

## During the night
- **About 02:00 Paris, an idea's id too long for a file name** (sessions 2 and 4; topic 46): ids grow with every
  generation; at generation 5 to 6 a plan's file (255-byte limit) or the similarity register's (`<run>__<id>_<bar>`,
  longer) cannot be written; step 3, or `run_idea` after step 6 (`Path.exists()` raises on such a name), fails. Failures
  before the fix: 9 (030), 6 in step 7 (026), 2 (011), 1 (022), 0 (017). **Fixed for tonight** (commits 01b1f5ffe0 and
  2d18f5ad6e): `select_next` does not offer an idea whose longest file name would pass the limit; the ids themselves are
  topic 46, for the operator. All five sessions stopped, took the fix, restarted (about 02:10 to 02:16 Paris).
  Correction: 01b1f5ffe0's message says failed ideas were retried; they were not (0 of 13, session 4).
- **A stop by hand leaves the loop's children running** (session 5): an idea stopped inside step 4 failed on resume
  ("Directory not empty": an orphan backtest still writing into its folder); re-admitted with a retry line once the
  orphans were stopped. Stopping a loop: stop its whole process group, not loop.py alone.
  **Fixed** (about 02:30 Paris, `common/lib.py` `end_with_parent`): a helper started by another helper now ends when
  that helper ends, whatever stopped it; a helper started from a shell (the loop) is unaffected. Test: a child outlives
  a killed parent without it, ends with it. Proof: step 4 rerun on 029-01 (1d, 6 coins, 144 windows) through the new
  path: metrics, forecasts and trade diagnostics identical in all 144; only run ids, times, commit id and temporary
  paths differ. Not covered: the engine's own `run_protocol.py` (shared code) still runs to its end after its step 4
  is stopped; it writes only into step 4's temporary folder, not the record. Sessions take it at their next restart.

## Session 4 (brief 030, absorption): ended on budget, 02:28 Paris (35.31 USD, 2 h 24; branch night5-brief-absorption, 26561df6d6)
| Measure | Count |
|---|---|
| Ideas written (step 2 / step 7) | 107 (4 / 103) |
| Tested / duplicates / not testable, id too long / left | 38 / 9 / 38 / 31 |
| Components built (wishes 12) | 9 (7 components), 3 existed; 5.85 USD |
| Step 5: confirmed / inconclusive / mismatch (of 29 plans) | 22 / 6 / 1, all 22 from 030-03 (heavy volume, low close, next-day rise) |
| Step 6 profitable enough | 3 (two are 7.d repairs) |
| Unseen tests: hold on both periods | 0 of 2 |
| 7.d: analyses / ideas / closures | 14 / 31 / 0; all 31 repairs by the session's reading; a trend condition in 9, each measured alone |
| Failed on file names over 255 bytes | 13 (1.45 USD), none after the second fix |

The session's reading: none of A1 to A4 as written; nearest A2 (a real effect, 22 of 29 confirmed; 3 books pay in
sample, none holds on both unseen periods). Its shares are against this run's books only (the other runs' return files
are not in its container): to be redone at the morning merge. One paying book (030-03...d2.d2.d2.d1) has no comparison:
its register file name is too long (topic 46); the merge's `--all` will fail on it the same way. 38 of 107 ideas not
testable for their id's length: topic 46's count for the operator.

## The register's periods under pandas 3 (session 2, about 03:40 Paris)
`run_idea` runs the similarity check under the python that runs it (here the system's, pandas 3), not the backtest's
(`--python`, pandas 2). The register wrote a period as `astype("int64") // 10**9`, which assumes nanoseconds; pandas 3
stores microseconds, so tonight's sessions wrote periods 1000 times too small (and truncated: 1641081 for 1641081600).
Effect: no night-5 book had a date in common with another run's book; its nearest relative was none, or a book of its
own run; `select_next`'s w had no evidence for most night-5 parents (0.5 by its rule). The register on this branch is
not affected (215 files, 0 bad: built with pandas 2). **Fixed** (`utc_seconds`, whatever unit pandas stores; test
under three units; checked under pandas 3.0.5). Not repairable by multiplying by 1000 (the truncation loses the
minutes): at the morning merge, each night-5 book is added again from its record (`add` rewrites its returns file),
then `--all`.

## Session 2 (brief 022 retest, 1d): ended on budget, 03:39 Paris (35.14 USD, 3.7 h; branch night5-retest-learned, 85c5a2c3d2)
| Measure | Count |
|---|---|
| Ideas written by step 7 (7.b / 7.d / 7.e / 7.g) | 63 (12 / 20 / 2 / 29) |
| Tested (plans) | 27 (26, 1 missing components) |
| Components built / existing | 2 / 1 (every check passed) |
| Step 5: confirmed / inconclusive / mismatch | 12 / 13 / 1 |
| Step 6 profitable enough / of them confirmed | 4 / 2 |
| Unseen: the 2 confirmed and paying books hold on both periods | 2 of 2 |
| 7.d: runs on confirmed not-paying ideas / ideas / closures | 10 (2 failed on names) / 20 / 0; 20 of 20 keep the signal; a trend condition in 13, measured alone in 9 |
| Failed on file names over 255 bytes | 11 (3.6 USD): 4 at step 3; 7 step 7 runs whose children's names were too long |

The two confirmed and paying books, nearest paying book measured again by the session in scratch with pandas 2:
| Book | Line | Holds unseen | Nearest paying book | Share |
|---|---|---|---|---|
| ...g1_range-expansion-precedes-rises.d1...b1_range-expansion-uptrend-more-coins | 7.b | both | 020-03 resistance breakout (paying_rerun_run) | 0.853 |
| ...d2_wide-range-days-lead-rises.b1...d1_wide-days-in-uptrends-rise | 7.d repair | both | 013-01 nearness to high (momentum) | 0.789 (its parent: 0.356) |

The session's reading: **R2, pays but drifted**: both hold on unseen dates, both mostly explained by a paying momentum
or breakout book; no paying book under 0.25. Group 2: 7 of 27 tested; with correct shares, five more parents would
have been group 2 (w 0.60 to 0.96). A cause found: `select_next`'s length rule guards the names of an idea's plan and
register files, not the names of the ideas step 7 writes from it; at generation 6, its children's names pass the limit
(topic 46).
