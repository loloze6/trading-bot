# Topic 23: Built components not merged afterwards

Status: closed (2026-11-19)  
Where: research: components  
Opened: 2026-11-19 (clean-up 3)

## Question
Should components built as near-duplicates be merged into one after the fact?

## Seen
- Brief 016's night built four components on one theme (how much of a move its k largest bars make):
  `RiseBeyondLargestMoves`, `LossShareBeyondLargest`, `TopGainsShareOfRise`, `TopLossesShareOfFall`.
- They are not exact variants: log returns, price units, the sum of losses as base, a sign; an exact merge needed 5
  switches (one per old formula). Two plans (016-02, 016-04) would change.
- The merge would remove 3 rows of 68 in the catalogue.

## Why it matters
Fewer, standard components; but a merge after the fact rewrites shared code and finished plans.

## Options
| Option | Gain | Risk |
|---|---|---|
| Merge into one component with settings | 3 fewer catalogue rows | shared code, two plans' configs, a proof, a conflict with the run session |
| Keep them; apply the rule when a component is built | no rework | - |

Recommended: keep them.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-19 | Not merged; one measure, one component is applied when a component is built | operator | the merge only slightly reduces the list and asks quite an effort | merging with 5 switches; merging with changed outputs |

## Status and next
Closed. The ruling is in `components/card.md` (rule 1).

## Links
Commit ac0092c8.
