# Topic 27: Dropped or solved in the review of 2026-11-19

Status: closed (2026-11-19)  
Where: research  
Opened: 2026-11-19 (clean-up 6)

## Question
Which parked items no longer need a decision?

## Seen
- **A cost limit per model call** (parked 2026-11-16): one 7.b call cost 3.77 USD once. Every call's tokens and time
  are logged since, so a repeat would show.
- **A component with no history step declares one bar fewer than it needs** (2026-11-16): no harm, the warm-up fetches
  twice the bars; the engine's design guide says so.
- **TAO has no data in fold D** (2026-11-17): solved, its daily bars load (120 bars, January to April 2025).

## Why it matters
A list of improvements holds only what still needs a decision.

## Options
| Option | Gain | Risk |
|---|---|---|
| Drop or close them | a shorter, true list | - |

Recommended: drop them.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-19 | Dropped: the cost limit | operator | only if it happens again; the logs show it | a limit (the operator: no default limits) |
| 2026-11-19 | Dropped: the one bar fewer | operator's go, on the design session's proposal | no harm, documented | - |
| 2026-11-19 | Closed: TAO | design session | its data loads | - |

## Status and next
Closed. The cost-limit item's condition ("if it happens again") was met the same day: reopened as topic 29.

## Links
Commit eaf5baaa.
