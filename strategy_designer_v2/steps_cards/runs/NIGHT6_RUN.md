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
(notes)

## Reading
(in the morning)
