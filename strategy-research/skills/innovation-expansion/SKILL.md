---
name: innovation-expansion
description: Expands a base trading hypothesis into novel but testable variants using alternative data, reverse thinking, behavioral indicators, and regime-specific adaptations.
---

# Innovation Expansion

## Mission
Expand the hypothesis space before strict validation.

## Required inputs
- `research_brief.yaml`
- `hypothesis_card.yaml`

## Required outputs
- `expanded_hypothesis_card.yaml`
- `innovation_notes.yaml`

## Output requirements
The expanded artifact must include:
- base_hypothesis_id
- expanded_variants
- alternative_data_candidates
- reverse_hypothesis
- behavioral_features
- regime_specific_variants

## Checklist
- Add novelty without destroying testability.
- Suggest alternative data only if plausible.
- Consider the reverse version of the thesis.
- Add behavioral or positioning proxies where meaningful.
- Keep at least one conservative variant.
- Prefer variants that can fit the current strategy/regime/component framework.
- Check research_brief.yaml constraints field first. If variant count is constrained, honor it before applying expansion logic.

## Forbidden
- Do not skip interpretability.
- Do not require expensive or unavailable data by default.
- Do not output generic brainstorming prose only.
- Do not propose ideas that require rebuilding execution, portfolio, or backtest infrastructure unless explicitly requested.
- If `research_brief.yaml` contains "one variant only", "single variant", or "no variants" in its `constraints` field, do NOT expand into multiple variants. Pass the base hypothesis through to a single variant (V1 only) matching the brief's signal_concept exactly. Expansion is only appropriate when the brief does not constrain variant count.

## Context rule
Use only the brief and the current hypothesis unless more is explicitly required.