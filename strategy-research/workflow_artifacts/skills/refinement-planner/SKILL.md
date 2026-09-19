---
name: refinement-planner
description: Converts validation blockers into a structured refinement plan without redesigning the strategy.
---

# Refinement Planner

## Mission
Turn validation blockers into a concrete refinement artifact.

## Required inputs
- `validation_protocol.yaml`
- `validation_decision.yaml`
- `expanded_hypothesis_card.yaml`
- `innovation_notes.yaml`
- `DATA_AVAILABILITY.md` (`strategy-research/docs/DATA_AVAILABILITY.md` — read only if a
  blocker is about data/timeframe availability; it is short by design to fit this skill's
  minimal-context rule)

## Required output
- `refinement_notes.yaml`

## Output requirements
The artifact must include:
- hypothesis_id
- stage
- blocker_responses
- decision

Each blocker response must include:
- issue
- action
- status

## Checklist
- Address each blocker explicitly.
- Keep the scope limited to refinement, not redesign.
- Distinguish data audit tasks from strategy changes.
- Pre-commit any threshold or execution assumption that validation flagged.
- If the blocker is about data availability, define the audit or fallback plan.

## Forbidden
- Do not write code.
- Do not redesign the strategy.
- Do not approve the hypothesis.
- Do not skip unresolved blockers.

## Context rule
Read only the validation artifacts and the current hypothesis context. Use minimal context.