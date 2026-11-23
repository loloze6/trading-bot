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
Proof on real books (session 2): its 12 books re-added with the fix under pandas 3.0.5 give the same shares as a
rebuild under pandas 2.3.3 (book 1: 0.853; book 2: 0.789, parent 0.356), each compared with 50 of 50 paying books.

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

## The usage limit (about 03:50 to 06:54 Paris)
The 5-hour usage limit stopped sessions 1, 3 and 5 between about 03:23 and 04:15 Paris (reset 05:30 Paris). Nothing
woke them at the reset: their own waits and my check-in at 04:46 Paris fired during the limit, and the workers of
several sessions, mine included, were restarted. My check-in at 06:51 Paris woke them; all three restarted at about
06:53 Paris, with both fixes (fddb0558b9, 86b9f9fa9f), no orphans found, the cut idea resumed or retried.
| Session | Stopped (Paris) | Time lost | State at 06:55 Paris |
|---|---|---|---|
| 1, weekend (020) | 03:23, machine restarted mid step 7 | 3 h 30 | 17 ideas run, 9 confirmed, 2 profitable (1 confirmed), 21.20 USD |
| 3, settlement (017) | 03:57, cut at step 5 | 2 h 55 | 21 turns, 25.80 USD |
| 5, Monday (011) | 03:52, refused at step 7 | 3 h 00 | 18 run, 14 confirmed, 2 profitable, 33.59 USD |
For a next night: a check-in timed just after the limit's reset (the refusal names it) would have saved about 3 hours
per session.

## Session 5 (brief 011 retest, Monday, 1d): ended on budget, 06:57 Paris (36.99 USD, 6 h 41 of which 3 h 01 stopped; branch night5-retest-monday, adb1e28e5b)
| Measure | Count |
|---|---|
| Ideas written by step 7 (7.d / others) | 73 (24 / 49) |
| Run to a result | 20 (2 starting, 18 from the loop) |
| Components built | 1 (VolatilityWeightedFallComponent; every check passed, bot suite 1635 passed) |
| Step 5 confirmed / inconclusive | 14 / 6 |
| Step 6 profitable enough | 2; the other 18 fail Calmar (12 on Calmar alone) |
| Unseen: hold on both periods | 0 of 2 |
| 7.d: analyses / ideas / closures | 14 / 24 / 0; all 24 keep the weekend move; trend condition in 9 (5 tested: all confirmed, none paying) |
| Failed | 3 on file names (before the fixes); 1 lost to an orphan, retried; 1 cut by the limit, resumed |

The two paying books: b1.d1 weekend reversal in rising volatility (7.d repair, +5.46, holds on neither unseen
period; its parent explains 0.76) and b2.b1.d3.b1 turbulent weekend fall rebound (+4.83, holds 2016-17, not 2026).
Both add volatility, not trend. Their shares against other runs wait for the rebuild. The session's reading: **R3**
(real, still not paying on unseen dates); R2 cannot be read before the rebuild.

## Session 3 (brief 017 retest, settlement, 1h): ended on budget, 07:55 Paris (35.97 USD, 7 h 51 of which 2 h 56 stopped; branch night5-retest-settlement, 25dd56449a)
| Measure | Count |
|---|---|
| Ideas written by step 7 (7.d / 7.g / 7.b / 7.c) | 154 (55 / 83 / 14 / 2) |
| Tested through step 6 | 31 (3 starting, 28 loop turns); 0 file-name failures |
| Step 5 confirmed / inconclusive / rejected | 22 / 8 / 1 |
| Step 6 profitable enough | 0 of 31; 6 confirmed failed Calmar alone (statistics up to +9.48) |
| 7.d: analyses / ideas / repairs / closures | 22 / 55 / 52 (3 replace the signal) / 0; a trend condition in 10, 9 measured alone (none significant) |
| Group 2 tested | 7 (turns 22-28, after the register fix; before it, no parent had evidence) |

The session's reading: **R3** (real, still not paying). The confirmed books are unlike any paying book (nearest
explains 0.008 to 0.17), but the effect's move per case is below the round trip (017-05: +0.05 % per case against
0.19 % per trade).

## Session 1 (brief 020 retest, weekend, 1h): ended at the time rule, 10:06 Paris (28.78 USD, 10 h 09 of which 3 h 31 stopped; branch night5-retest-weekend, 3eeaf4c8f5)
| Measure | Count |
|---|---|
| Ideas run | 22 (2 starting, 20 from the loop); a 23rd stopped after 11 s (started after the time rule) |
| Components built | 3 (every check passed); 1 wish answered "exists"; 2 ideas still missing components |
| Step 5 confirmed / rejected / inconclusive | 13 / 1 / 6 |
| Step 6 profitable enough / of them confirmed | 4 / 3 |
| Unseen: hold 2016-17 (no 2026 data on 1h) | 2 of 3 |
| 7.d: runs / ideas / closures | 11 (2 failed on names) / 23 / 0; all repairs; a trend condition in 6, 2 measured alone |
| Failed on file names | 6 step 7 runs |

The three confirmed and paying books: 026-03.d3.d1.d1 Saturday continuation with weekly trend (+5.86, holds 2016-17);
026-04.b2.d1.d1 heavy weekend extends week (+3.11, holds 2016-17; nearest paying book 018-02 hourly breakout, 0.10;
holding explains 0.01); 026-04.b2.d1.d2.d2 heavy weekend falls continue (+3.87, does not hold 2016-17). Shares to be
read from the rebuilt register. The session's reading: **R1 on the counts** (book 2: confirmed, paying, holds the one
unseen period with data, nearest paying book under 0.25).
Found: `trading-bot/performance/signal_statistics.py` (shared code) scans every segment for every block; on 2016-17
hourly BTC (17k bars) one coin's unseen test took about 75 min. Not changed (shared code: the operator's go).
