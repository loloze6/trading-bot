# Night 6 (2026-11-23): four new daily briefs for portfolio candidates, under today's rules (written before the runs)

**The operator (2026-11-24, about 00:50 Paris):** "What is the best use of this night's working capacity that could be
launched in autonomy? New research workflow could be launched, learning from what we learnt today. See previous night
rules and work so that we apply the same." Same setup and rules as nights 4 and 5 (`runs/NIGHT4_RUN.md`,
`runs/RETEST_RUN.md`).

## What today changed, and how tonight uses it
| Learnt today | Tonight |
|---|---|
| A real book rarely pays alone (market timing on correlated coins, topic 47); unrelated books that each earn a little combine well: in sample Calmar 1.37 for 20 books against 0.24 for the median book; on the unseen dates the 13 daily ones are nearly uncorrelated (mean correlation 0.03 and 0.00) (topic 44, P2-P4) | The aim shifts from "one book that pays" to **more portfolio candidates**: real books that earn on their own (step 6's Sharpe above 0), from families the portfolio lacks, unrelated to its 20 books |
| Books built before N3 graded the idea's situation away; step 3 now builds the situation as stated (N3) | Every plan tonight is built under N3: the first run of whole briefs under it |
| Hourly books lose to turnover (topic 48); hourly 2026 bars exist only for 6 coins | Daily bars only |
| The strongest in-sample results hold least (1d-11) | Nothing is ranked or kept by in-sample strength; counts only |
| The current families (portfolio P1): 30 briefs, mostly one coin's price patterns (RSI, averages, ranges, volume, weekends, breakouts) | Four themes no brief has covered, within the rule "one coin's own bars" (`common/idea_definition.md`) |

## Sessions
| Session | Run | Theme (step 1 writes the brief) | Bar | Budget (model calls) |
|---|---|---|---|---|
| 1 | `night6_streak_run` | After a coin closes up, or down, several days in a row, does it give back part of the run over the next days, or carry on? The longer the streak against the coin's usual, the larger the move that follows. | 1d | 35 USD |
| 2 | `night6_longreversal_run` | A coin that has fallen, or risen, far more than its usual over the past two to three months moves the other way over the following weeks, as the overreaction fades. | 1d | 35 USD |
| 3 | `night6_indecision_run` | After a run of several days, a day with a wide range but a close near its open marks the end of the run: the coin moves back over the next days. | 1d | 35 USD |
| 4 | `night6_yearlow_run` | Near its lowest price of the past year, does a coin keep falling as holders give up, or bounce as sellers run out; and does a close below that low continue or reverse? | 1d | 35 USD |
| designer | P4 finished (the 7 hourly books once the 2026 hourly bars are fetched, about 07:30 Paris), the morning reading | - | - | 0 USD |

Each session: `run_brief --theme` with its theme and budget, on its own branch (`night6-<name>`) from the working
branch. Night 4 and 5's rules: the loop runs detached (`setsid nohup`) so the 2-hour limit of a background task does
not cut it; if it stops all the same, it is resumed with `loop.py --run` without asking; a stop on "the model service
refused a call" (the usage limit) is resumed after the limit's reset (the session schedules its own wake-up); commits
and pushes along the way; no new idea after 07:00 UTC (09:00 at most if the limit cost time); budgets set in the first
message and not changed; the similarity register is written by `run_idea` on the session's branch (merged in the
morning: the union of `books.json`, then `--all`). A stop by hand stops the loop's whole process group.

## Measures, per brief
Ideas, plans, confirmed, profitable enough, holding on the unseen dates (as before); and, new tonight, **portfolio
candidates**: books confirmed, size above 0, step 6's Sharpe above 0, whose daily returns correlate under 0.5 with
every book of the fixed portfolio (`topics/44_review/p1_candidates_earning.csv`), computed by the designer in the
morning (no model cost).

## Expected outcomes
| Outcome | What the counts would show | Meaning |
|---|---|---|
| N1. New candidates | at least one portfolio candidate per brief | the research adds families to combine |
| N2. A second family | a paying book holding on both unseen periods, its nearest paying book under 0.25 | topic 44's long-awaited second family |
| N3. Real, losing | confirmed ideas whose books lose after costs (Sharpe below 0) | the effect exists; its book does not keep it |
| N4. Not real | few confirmed | the theme is not in the daily bars |
The designer's guess, for the record: N1 on two or three briefs (streaks and long-horizon reversal are the most studied
effects of the four); N2 on none.

## During the night
- 00:50 Paris: the four sessions launched (session 1 `session_012maTgWeD1GH4TXz9VJSiU1`, 2 `session_012maTgTihYXqVbsfcvKL5za`,
  3 `session_012maTgU5GYo9zM36Fb7Euy4`, 4 `session_012maTgWBE2Ln9BPLKqXM7jV`), from the working branch at 072b469688.
  The designer checks them at 04:30 Paris (usage limit) and runs P4's hourly part from about 06:45 Paris.
- **04:58 Paris, session 4 (yearly low) ended on budget** (35.48 USD, 3.1 h; branch night6-yearlow, f5a28f805d): 65 ideas
  (4 from the brief, 61 from step 7), 32 plans and backtests; step 5: 14 confirmed, 14 inconclusive, 4 not observable;
  step 6: 9 profitable enough (5 of them confirmed); unseen, the 5 confirmed and profitable: 2016-17 holds 2 of 5,
  2026 holds 3 of 5, both 1 (volatile down day, next-day rebound: t 1.16 and 0.08; its nearest paying book explains
  0.39). The theme itself: 0 of 8 yearly-low ideas confirmed (falling near the low t +1.70, the bounce t -1.70, a break
  below the low too rare: 12 to 18 cases). All 14 confirmed come from step 7's pattern line on 031-01: one family, a
  week's or month's trend carrying into Thursday to Saturday; all 14 have step 6's Sharpe above 0 (0.57 to 1.31), 9
  fail step 6 on Calmar only. One container restart (about 01:43 Paris) killed the loop mid-idea; resumed at once,
  the idea finished from its outputs. The session's reading: N4 for the theme, N1 likely (to check against the
  portfolio: one family, so about one candidate), N2 not.
- **Brief numbers collide across branches:** sessions 1 and 4 both wrote brief 031 (each branch numbers from the
  briefs it has). At the morning merge, the briefs and their ideas' family codes must be renumbered (031, 032, ...),
  or P7 would take two briefs for one family. A rule for parallel sessions (a brief number range per session, or
  numbers given at the merge) is a next step.
- **About 04:00 Paris, the designer's container restarted:** the hourly download (P4) had stopped logging after 1,000
  BTC calls (about 00:48 Paris) and its progress, held in memory, was lost; the hourly files were untouched (checked
  against their checksums). The tool now saves its progress every 200 calls and resumes after a stop, logs the time,
  and never appends an hour a file already has (tests; ce60e63798, d3a7855cd8). Relaunched at 04:07 Paris, smallest
  coins first; watchdog check-ins at 05:30 and 07:30 Paris relaunch it if another restart stops it. P4's hourly part
  moves later (about 09:00 to 10:00 Paris).
- **04:31 Paris check-in:** sessions 1 to 3 working (updated within the last 5 minutes); session 4 done. The designer's
  container restarted again (up 0 min at 04:31): the cause is the cloud reclaiming an idle session's container; a
  process launched detached (setsid nohup) dies with it (03:12 UTC, 20 minutes after the designer's turn ended). The
  saved progress survived (XMR, 200 calls). The download now runs as a background task the session tracks, with a
  monitor, and resumes from its saved progress.

## Reading
(in the morning)
