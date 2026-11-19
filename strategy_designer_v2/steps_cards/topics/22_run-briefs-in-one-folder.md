# Topic 22: Run briefs in one folder

Status: closed (2026-11-19)  
Where: research: repository  
Opened: 2026-11-19 (clean-up 2)

## Question
Where do the run briefs live?

## Seen
- The 10 run briefs (`*_RUN.md`) lay at the root of `steps_cards/`. Moved to `steps_cards/runs/`; 18 cards, the run viewer and its test updated.

## Why it matters
One place for each thing.

## Options
| Option | Gain | Risk |
|---|---|---|
| One folder `runs/` | clean root; the viewer finds them | references to update |

Recommended: as done.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-19 | Moved to `runs/` | operator's go, on the design session's proposal | a clean, structured repository: one place for each thing | - |

## Status and next
Closed.

## Links
Commit 004488fa.
