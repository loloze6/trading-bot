# Night 4 (2026-11-22): five briefs aimed at the days momentum does not trade or loses, and one short-horizon brief (written before the runs)

**The operator's go (2026-11-22, about 01:00 Paris):** "go for tonight's briefs", as on night 3: several sessions,
several briefs across 1h, 4h and 1d. **Why these briefs:** on night 3 and in the similarity register, 33 of 35 paying
books are momentum variants (`orchestration/ideas_similarities_check/validation/reading.md`); combining pays only with
books unrelated to each other that each hold on the unseen dates (`runs/COMBINE_TEST_RUN.md`, topic 44). So each brief
aims at a market state where a long momentum book is flat or loses: no trend, the end of an overextended run, a falling
market, the thin weekend, a panic.

**Engine and workflow:** master as merged on 2026-11-22 (PR 577) and the working branch after it: the holding period,
the measured costs, the loop's fixes (a refused model call stops the loop and marks nothing failed; the budget holds on
resume), line 7.f deleted, the findings register removed.

| Session | Brief | Bar | Run | Budget (model calls) |
|---|---|---|---|---|
| 1 | 023, range reversion when there is no trend | 1d | `night4_range_run` | 35 USD |
| 2 | 024, exhaustion after an extended run with fading volume | 4h | `night4_exhaustion_run` | 35 USD |
| 3 | 025, bounces fade in falling markets (long and short) | 1d | `night4_fallingbounce_run` | 35 USD |
| 4 | 026, weekend moves reverse in the week | 1h | `night4_weekend_run` | 35 USD |
| 5 | 027, panic stretches are followed by a premium | 4h | `night4_panic_run` | 35 USD |
| 6 (added 01:15 Paris, the operator: "try also a brief at short horizon") | 028, volume-confirmed hourly moves continue over 2 to 6 hours; BTC and ETH only (a buy and a sell about 0.10 %) | 1h | `night4_volumehour_run` | 35 USD |
| designer | the morning: merges, the similarity check on the new paying books, the reading | - | - | 25 USD |

Each session: `run_brief` with its brief and budget on its own branch (`night4-<name>`). A background task cut by the
2-hour limit or a restart is resumed with `loop.py --run` without asking (topic 37, the operator 2026-11-21). If the
loop stops on "not run: the model service refused a call" (the account's usage limit), the session resumes it after the
limit's reset time. Start nothing after 07:00 UTC (09:00 UTC at most if the limit cost time). Sessions do not touch the
similarity register: the designer adds the night's paying books to it in the morning, after the merges.

**Measures, per brief:** ideas written; plans; missing components and those built; confirmed; profitable enough;
holding on the unseen dates; and, for each paying book, its nearest relative in the similarity register and the share
of it that relative explains.

**Expected outcomes:**
| Outcome | What the counts would show | Meaning |
|---|---|---|
| M1. A second family | a paying book that holds on the unseen dates and whose nearest relative explains less than half of it | a candidate to combine with momentum (topic 44) |
| M2. Momentum again | paying books whose nearest relative is a momentum book explaining most of them | the brief's theory did not lead away from momentum: read what the ideas became |
| M3. Real but not paying | confirmed ideas, no profitable book | the effect exists, too small or too rare to pay its costs |
| M4. Not real, or blocked | few confirmed, or ideas waiting for components that cannot be built | recorded, not pursued |

**Risk noted:** the account's 7-day usage limit showed a warning on 2026-11-21; five sessions at once can reach the
5-hour limit again (it stopped every session on night 3).

## The operator's authorization, and the lessons of night 3 applied (2026-11-22, 01:20 Paris)
**The operator:** "You have all rights to fix and restart if needed. From last nights, take the lesson about what went
wrong."

| Night 3 | What went wrong | Applied tonight |
|---|---|---|
| The account's 5-hour usage limit stopped every session at once (03:56 to 06:10 Paris) | 2.3 hours lost; every session waited for a message | each session schedules its own wake-up at the reset time and resumes; the designer checks at 04:30 Paris |
| A refused model call failed ideas for good; one idea turned about 4,000 times | 177 untested ideas excluded; MBs of repeated lines | fixed in the loop and `run_idea` (refused call: the loop stops, nothing marked failed; a failed step ends the idea's run) |
| The designer's fix (retry lines) let resumed ideas run past their budget | about 29 USD over two budgets | fixed (the budget holds before every `run_idea` call). Rule for tonight: a fix sent to a running session is tested first on the state that session is in (its loop file), budget and resume paths included, before it is merged into its branch |
| A session refused a budget raise sent by another session | 26 ideas left unrun | budgets are set in each session's first message and not changed during the night |
| Background tasks cut by the 2-hour limit, and a machine restart | runs paused until relaunched | relaunched at once without asking (topic 37); each session commits along the way, so a restart loses nothing finished |
| Branches touching the same shared files (components) | conflicts at every merge | resolved the tested way in the morning (ours plus each branch's additions, then both test suites) |
| Paying ideas that were momentum again | counted as discoveries | each paying book goes through the similarity check in the morning before it is called new |

## During the night
- **01:09 Paris, a blocking defect, found by session 3:** every step 3 call failed with "OSError: Argument list too
  long". Step 3's system prompt (its instructions 8 KB, the config guide 40 KB, the component catalogue 99 KB) reached
  about 147 KB with the night-3 builds; `common/lib.py` passed it as one command-line argument, capped at 128 KiB on
  Linux. The loop counted it as a failed step (as it should: the call never reached the model) and stopped on "no
  candidate left" after 0.04 USD.
- **01:25 Paris, fixed** (commit 2df2b7da): the system prompt goes through a file (`--system-prompt-file`), the same
  text. Proof: a tiny call with a prompt file; step 3 on a real idea with the full prompt (its plan written, 0.55 USD);
  workflow tests 116 pass. The resume tested first on session 3's own state (clean merge; 3 retry lines re-admit its
  ideas; the budget checked), then sent to the six sessions: merge, one retry line per idea failed this way, resume
  with the budget unchanged.
- **To watch (for the operator):** the catalogue grows with every component built (99 KB today), and with it the cost of
  each step 3 call: 64,000 tokens written to the cache, 0.55 USD per plan.
- **01:16 Paris, a second fix on one branch:** session 1 had already fixed the defect its own way (the prompt split into
  `--system-prompt` and `--append-system-prompt` above 120 KB; it fails above about 240 KB) and objected to the file:
  on haiku-4-5, its probe saw the file's text treated as the user's. Checked by the designer on the models the steps
  use: the probe "reply PONG-7731" gives PONG-7731 through the file 3 of 3 times (claude-haiku-5-5), as through the
  argument; a conflict probe (system: always APPLE; user: BANANA) gives APPLE through the file 2 of 2 (claude-opus-5-5,
  step 3's model), as through the argument. Kept: the file, one rule with no size limit; session 1 asked to take it.

## Reading (2026-11-22, about 08:20 Paris)
All six sessions ended (five on their 35 USD budget, session 4 at 07:00 UTC); every branch merged into the working
branch; the night's 14 paying books added to the similarity register and compared. Model calls: about 212 USD
(36.3 + 39.3 + 36.0 + 28.7 + 35.6 + 35.9; the overruns are the idea already started and the components step, as the
cards allow).

| Brief | Bar | Ideas tested | Confirmed | Profitable enough | Confirmed and profitable | Holding on the unseen dates | Components built | Outcome |
|---|---|---|---|---|---|---|---|---|
| 023 range reversion | 1d | 30 | 16 | 7 | 6 | 6 of 6, both periods | 6 | M2 |
| 024 exhaustion after a run | 4h | 27 | 6 | 8 | 6 | 6 of 6 on 2016-17 (no 2026 data at 4h) | 3 | M2 |
| 025 bounces fade in falling markets | 1d | 23 | 7 | 1 | 1 | 1 of 1, both periods | 1 | M1 at the line (below) |
| 026 weekend moves reverse | 1h | 21 | 9 | 0 | 0 | - | 4 | M3 |
| 027 panic premium | 4h | 18 | 1 | 0 | 0 | - | 5 | M3 (mostly inconclusive) |
| 028 volume-confirmed hourly moves | 1h | 26 | 7 | 1 | 1 | 0 of 1 (fails 2016-17) | 1 | M3 |

**No brief's own theory paid.** The reversion, exhaustion, weekend-reversal and panic ideas were inconclusive, rejected
or too small; the step 7 lines moved each brief back to continuation (trends, dips in uptrends) and those books pay.

**The similarity check on the 14 paying books** (share explained by the nearest paying book; what is left, and its t):
| Book | Nearest relative | Share explained | Left (t) | Explained by holding its coins |
|---|---|---|---|---|
| 023, six books | momentum books (022-01, 022-02, 019-03), and each other | 0.61 to 0.98 | none reliable (t −1.79 to 1.51) | 0.00 to 0.52 |
| 024, four books | 019-03, 018-06 (dips in uptrends), and each other | 0.79 to 0.99 | none reliable (t −0.23 to 1.00) | 0.42 to 0.58 |
| 024-02.d3.e1 thirty-day trend, graded | 022-03 strong monthly rises | 0.91 | +0.019 % a day (2.09) | 0.42 |
| 024-03.d2 stretch above average continues | 001-01 high-RSI trend continuation | 0.90 | +0.025 % a day (2.57) | 0.39 |
| 025-03.d2 sharp rises follow the monthly trend (long and short) | 018-02 hourly breakout continuation | **0.50** | +0.020 % a day (1.88) | **0.08** |
| 028-04.b1 quiet dip in an uptrend recovers | 005-02 five-day rise keeps going | 0.49 | none (0.53) | 0.22 |

- **M2 for 12 of 14:** the night's paying books are momentum we already have; two of them add a little on top of
  their relative (t above 2 with 0.90 explained: a known profit, improved timing).
- **025-03.d2 is the only candidate for M1, exactly at its line** (M1 asks for less than half explained; 0.50): it
  holds on both unseen periods, holding its coins explains 8 % of it, every other paying book explains at most 0.50,
  and the night's other books explain 0.20 to 0.41 of it. It is the only long-and-short book of the night; what it
  adds is probably the short side in falling coins. Not called a second family: half of it is momentum.
- **028-04.b1** reads unrelated (0.49) but adds nothing reliable and fails the unseen dates.

**Incidents:** step 3 blocked at the start for every session ("Argument list too long", fixed 2df2b7da, above); the
account's 5-hour limit stopped sessions 1 and 5 at 02:16 to 02:17 UTC, the 2-hour task limit cut sessions 2, 3, 4 and 6
at about the same time; all resumed at 03:32 UTC after the designer's check-in: about 1.3 h lost per session.
Session 6 sat idle about 75 minutes: a session whose loop the 2-hour limit cuts does not always restart it alone.
Session 4's stop at 07:00 UTC ended its last idea mid-way (026-03...d3, step 3 done): a later resume finishes it.

**Merges and shared code (the operator's go for master):** 18 new components built (6 + 3 + 1 + 3 + 5) and three earlier components given a
setting in place (`DonchianBreakout` forms, `VolumeRatio` lag, `MeanAbsScaledFallTimesRise` rise_lag). Each in-place
change proven by old against new on real bars (4 coins, 1h, 4h and 1d, the earlier settings): 82,409, 137,980 and
82,788 bars, 0 differ; the 14 paying books' step 4 reruns here (on the merged engine) reproduce their records file by
file. Tests: the cards' 116 and the bot's 1,635 pass.

**What a practitioner would do next:** stop writing briefs that aim at reversal on these coins and bars: four nights of
briefs found momentum, and the reversal effects that are real do not pay their costs. Two readings are worth one test
each: (1) 025-03.d2, the long-and-short book, against momentum held long only: is the short side the profit of its own
(the similarity check on its two legs)? (2) If it is, topic 44's portfolio layer has its two books: momentum and
025-03.d2's short side. Recommended: (1), at no model cost.

## The operator's decisions on the reading (2026-11-22, morning)
| # | Proposal | Decision |
|---|---|---|
| 1 | Test 025-03.d2's short side: the book split into its buying and its selling part, each through the similarity check (no model cost) | go |
| 2 | Stop writing reversal briefs on these coins and bars | **no**: reversal briefs stay allowed |
| 3 | Merge the night's shared code (18 new components, 3 in-place settings, with their build records and proofs) into master | go |
| 4 | Delete the merged GitHub branches (refused to the designer, 403) | go, done by the operator |

## Test 1: 025-03.d2 split into its long leg and its short leg (2026-11-22, morning; 0 USD)
**Purpose:** is the short side (selling coins whose month fell) a profit of its own, unrelated to momentum? If so, it is
the second book topic 44 waits for. **Expected:** either the short leg earns reliably (t of 2 or more) and no paying book
explains it, or it does not. **Rule:** per coin, each bar's return goes to the side held coming into the bar; a bar
entered from flat goes to the side entered (its cost). The legs sum to the book on 17,522 of 17,524 bars (the other 2:
a position opened and closed within the bar, 0.002 % of the book's movement). Script `topics/44_review/split_legs.py`
(the similarity check's own functions; folds only).

| | Book | Long leg | Short leg |
|---|---|---|---|
| Mean return a day | +0.052 % | +0.047 % | +0.006 % |
| t (2 or more: reliable) | 3.50 | 3.20 | 1.25 |
| Sharpe | 1.24 | 1.14 | 0.44 |
| Share of the book's total return | 1.00 | 0.89 | 0.11 |
| Days in a position | - | 54 % | 31 % |
| Nearest paying book, share explained | 0.50 | 0.58 (018-02, momentum) | 0.10 (024-01) |
| Holding its coins, share explained | 0.08 | 0.15 | 0.10 (against) |

**Found:** the second outcome. The short leg is unrelated to every paying book and to the long leg (0.01), but small and
not reliable (t 1.25 over 8 years). The book read as half new because it mixes a momentum long leg with a small
unrelated short leg. Topic 44 stays waiting for a second unrelated book that pays on its own.

## The seal gate made to follow the policy (2026-11-22, the operator's go)
CI's "Holdout seal gate" failed on PR 578 and on master: `strategy-research/tools/holdout_date_gate.sh` wrote the old
sealed half-year into its pattern, while `holdout_range` had moved on the operator's go for the unseen run
(`runs/UNSEEN_RUN.md`). The gate now builds its pattern and its four self-test dates from `holdout_range` (as
`data/data_manager.py` does) and blocks when it cannot read it. Proof: the gate passes on the branch and on master; its
15 tests pass (13 before, the fixtures given a policy file; 2 new: a made-up window moves the gate, a missing policy
blocks), the 2 new ones fail on the old script; no unseen-2026 window's data overlaps `holdout_range` (1,011 checked).

## Test 2: 025-03.d2 combined with momentum (2026-11-22, written before the run; the operator's "yes"; 0 USD)
**Purpose:** what combining the night's most distinct paying book with momentum gives, measured rather than estimated
from the similarity check. **Method:** A of `runs/COMBINE_TEST_RUN.md` (side by side, half the capital each: each day the
mean of the two books' daily returns; step 6's measures), on the folds and on both unseen periods (step 4 rerun on
each plan with `04_backtest/windows/unseen_*.json`). Script `topics/44_review/combine_night4.py`.

| Pair | Books | Share explained | Expected (from the share explained) |
|---|---|---|---|
| 1 | 025-03.d2 with 022-03.d1 strong monthly rises continue (1d, the momentum book of the earlier test) | 0.41 | correlation about 0.64; daily swings about 10 % below the two books' average; Sharpe about 1.35 against about 1.25 alone; deepest fall at or below the smaller one |
| 2 | 025-03.d2 with 018-02 hourly breakout continuation (1h, its nearest relative; compared by the day) | 0.50 | correlation about 0.71; about 8 % smaller swings; a smaller Sharpe gain |
**If not:** a combination clearly worse than either book alone, or a correlation far from the square root of the share
explained, means the similarity check does not say how two books combine: read why.
