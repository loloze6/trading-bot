# Topic 46: an idea's id grows with every generation, past the limit of a file name

Status: open (found 2026-11-23, night 5; for the operator's decision)  
Where: research: the id convention (`common/idea_created_from.md`), every step that names a file after an idea or a
plan, `select_next` (it reads the track from the id)  
Opened: 2026-11-23, session 2 of `runs/RETEST_RUN.md` (`retest_learned_run`).

## Question
How should an idea's id carry its track back to its brief without its file names growing past the system's limit?

## Seen
- An id is its parent's id, a dot, the line's letter and number, and a short name (`common/idea_created_from.md`): each
  generation adds about 30 to 50 characters. A plan's file adds the bar and `_config.json`.
- At generation 6, step 3 failed with "OSError: [Errno 36] File name too long" (a file name is limited to 255 bytes on
  Linux) on `022-04...b1_nearness-reversal-after-rises.e1_short-volatility-scaled-momentum`; the idea is lost and every
  deeper idea of that lineage fails the same way. The loop marks it failed and goes on (no spin).
- Night 5, all sessions (2026-11-23, about 02:10 Paris): step 3 failures before the `select_next` rule: 9 (brief 030), 2
  (011), 1 (022), 0 (017); step 7 failures (a line on a generation-5 idea could not write its generation-6 children, 257
  to 269 bytes): 6 (026: 7.b 1, 7.d 2, 7.g 3). The `select_next` rule stops the step 3 failures, not the step 7 ones (the
  generation-5 idea's own test is kept: only its children are lost, about 0.4 USD per line).
- Correction (session 4, 2026-11-23): no failed idea was picked again (0 of 13); commit 01b1f5ffe0's message says
  "retried": wrong (an idea stopped on missing components was retested once they were built, the normal path). Its 13
  failures: 5 at step 3, 4 at the similarity register after step 6 (`<run>__<id>_<bar>` is longer than a plan's names;
  in Python 3.13 `Path.exists()` raises on a name over the limit, so `run_idea` stopped there and step 7 did not run), 4
  on other paths. The `select_next` rule now counts the register's names too (commit after 01b1f5ffe0).
- Deep ideas rank low (score / (1 + generation)), so the loss is small today; the new order (`select_next`, 2026-11-22)
  follows real lineages further, so it will grow.

## Options
| Option | Gain | Risk |
|---|---|---|
| A. Ancestors by letter and number only: `022-04.b1.d2.e1_<short name>` (the last short name kept); the full names in the idea file's header (`source-idea:`) | the track stays in the id; a name stays short at any depth | `id_parts` in `select_next` and every reader of ids change (one convention, read in several places); old ids stay as they are |
| B. Short names capped (a few words) | small change | the id still grows; it only delays the limit |
| C. A number per idea (a register of ids) | short names at any depth | the track leaves the id; a register to keep |

Recommended: A, with the readers of ids changed together and old ids still read.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-23 | Until the ids are shortened, `select_next` does not offer an idea whose plan's files cannot be written | the designer, on the night's rights to fix (session 4 of `runs/RETEST_RUN.md`: 9 failures, failed ideas retried, each a step 3 call; the new order follows real lineages deep) | stops the waste with one rule; the convention is the operator's decision | changing the id convention at night with five loops running |

## Links
`common/idea_created_from.md`, `orchestration/select_next/`, `runs/RETEST_RUN.md`.
