# Night 4 (2026-11-22): five briefs aimed at the days momentum does not trade or loses (written before the runs)

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
