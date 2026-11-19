# Topic 07: Two loops calling the components step at the same time

Status: open  
Where: research: components  
Opened: 2026-11-19 (night 1h)

## Question
Can two loops run at once without building into the same files?

## Seen
- Two loops on the same working tree would build into the same shared files (`strategy_components.py`, the catalogue,
  the specs) at the same time. The briefs have run one after the other since.
- A build cut by a restart is undone at the step's next start since 2026-11-19 (topic 24).

## Why it matters
Parallel runs would be faster; today they are not safe on one working tree.

## Options
| Option | Gain | Risk |
|---|---|---|
| Keep one loop at a time per working tree | safe, no work | slower |
| A lock around a build | parallel loops | a loop waits for another's build |

Recommended: one loop at a time, until parallel runs are needed.

## Decisions
None yet.

## Status and next
Opens when parallel runs are wanted.

## Links
`components/card.md`, topic 24.
