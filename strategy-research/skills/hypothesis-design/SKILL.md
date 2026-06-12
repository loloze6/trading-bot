---
name: hypothesis-design
description: Produces a clear, testable trading strategy hypothesis from a research brief, including thesis, rationale, signal concept, assumptions, and expected failure modes.
---

# Hypothesis Design

## Mission
Create one explicit, testable strategy hypothesis.

## Required input
- `research_brief.yaml`

## Required output
- `hypothesis_card.yaml`

## Output requirements
The artifact must include:
- hypothesis_id
- thesis
- rationale
- signal_concept
- target_market
- timeframe
- assumptions
- expected_failure_modes

## Checklist
- State the idea in a way that can be tested.
- Keep the logic interpretable.
- Make the expected mechanism explicit.
- Include assumptions rather than hiding them.
- Include failure modes.
- Prefer hypotheses that can be integrated as a minimal change in the current strategy architecture.

## Forbidden
- Do not write code.
- Do not propose more than 3 variants unless explicitly requested.
- Do not use vague claims like "AI may detect patterns".
- Do not assume unavailable data.
- Do not propose ideas that require replacing the whole existing bot architecture.

## Context rule
Read only the research brief unless the handoff explicitly requires one more file.