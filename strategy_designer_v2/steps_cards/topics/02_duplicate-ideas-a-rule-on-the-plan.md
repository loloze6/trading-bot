# Topic 02: Duplicate ideas: a rule on the plan

Status: open  
Where: research: select_next  
Opened: 2026-11-17 (night_run)

## Question
How do we avoid paying twice for the same test written in other words?

## Seen
- `select_next` finds a duplicate only when two ideas have the same text and data.
- Two ideas from different parents (`...d1_weekend-moves-reverse-both-ways` and
  `...b1_weekend-fall-reverses-monday.d1_weekend-moves-reverse-both-ways`, night_run) gave the same t (+2.75) and the
  same failures, about 1 USD each.
- Step 2's 002-01 (after the cross) and 002-05 (from cross to cross) became the same config in step 3.

## Why it matters
Each duplicate costs a run (about 1 USD) and counts twice in the results.

## Options
| Option | Gain | Risk |
|---|---|---|
| A rule on the plan: same config and same data = a duplicate | catches both cases seen | a config can differ by a detail and still be the same test |
| A rule on the text (as today) | no work | misses both cases seen |

Recommended: a rule on the plan, when the operator opens it.

## Decisions
None yet.

## Status and next
Opens when the operator says so.

## Links
`orchestration/select_next/card.md`.
