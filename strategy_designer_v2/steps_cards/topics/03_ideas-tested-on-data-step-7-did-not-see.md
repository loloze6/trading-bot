# Topic 03: Ideas tested on data step 7 did not see

Status: open (in part done)  
Where: research: orchestration  
Opened: 2026-11-13 (overnight run)

## Question
Does an idea step 7 found still hold on data it never saw?

## Seen
- Overnight run (2026-11-13): of 8 ideas confirmed on the 6 default coins, 4 did not hold on 9 other coins; step 7's
  own numbers are inflated by its search.
- 6 coins count as about 2 independent coins (books' correlation 0.40 to 0.46), so years, not coins, set what an idea
  can show.
- Unseen dates: standard since 2026-11-18 (topic 20).

## Why it matters
The more ideas are tried on one data set, the more a good result there can be luck.

## Options
| Option | Gain | Risk |
|---|---|---|
| Unseen coins: the same plan unchanged on coins step 7 never saw (the overnight tool `oos.py`, in git history) | a second out-of-sample axis | coins are correlated: a weak test |
| A count of ideas tried per data set, with a limit past which a result counts only with an unseen test | controls the search's luck | a limit is a gate: the operator prefers visibility |

Recommended: unseen dates first (done); the count as a visible number, not a limit.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-18 | Unseen dates made standard (topic 20) | operator | years, not coins, set what an idea can show | unseen coins first: coins are correlated |

## Status and next
The remaining part opens when the operator says so.

## Links
Topic 20; `orchestration/unseen_test/card.md`.
