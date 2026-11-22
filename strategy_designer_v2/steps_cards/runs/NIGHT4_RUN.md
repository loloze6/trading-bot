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
