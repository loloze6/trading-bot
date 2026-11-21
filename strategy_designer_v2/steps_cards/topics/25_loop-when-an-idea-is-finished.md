# Topic 25: Loop: when an idea is finished

Status: closed (2026-11-19)  
Where: research: loop  
Opened: 2026-11-19 (the run session, 017-02)

## Question
When the loop resumes, which ideas did it leave unfinished?

## Seen
- 017-02 (intraday_1h_run): refused at 00:13 (a row), unblocked, re-planned at 08:55, cut before its backtest. On
  resume the loop read it as finished from its old row; nothing would ever run its backtest. Finished by hand.
- Built: `run_idea` stamps each row with `finished_at`; an idea is finished when its row was written after its latest
  turn started. Old rows (no time) count as finished, as before. Proof: all 12 runs' unfinished ideas identical, old
  rule against new.

## Why it matters
An idea silently never backtested is a lost result.

## Options
| Option | Gain | Risk |
|---|---|---|
| Compare the row's time with the turn's | one rule, any cause | old rows keep the old rule |
| Special-case refusals that were unblocked | - | a patch for one case |

Recommended: compare the times.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-19 | Finished = the row written after the latest turn started | operator's go, on the design session's proposal | the fix is general, not a case | a special case for unblocked refusals |

## Status and next
Closed. Lives in `orchestration/loop/` and `run_idea/`.

## Links
Commit 1551066f.
