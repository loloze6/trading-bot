# CLAUDE.md

## Project
Research-only trading strategy factory.

## Objective
Generate, expand, validate, backtest, analyze, and decide on strategy hypotheses.

## Global rules
- Use structured artifacts for all handoffs.
- Never pass full transcript/history by default.
- Load only the files needed for the current task.
- Validate outputs against schemas before moving to the next stage.
- Innovation happens before validation.
- Validation is falsification-first.
- Promising ideas must pass screening, then walk-forward, then holdout.
- Large outputs must be written to files, not kept inline.
- After each stage, write a short summary artifact.

## Workflow stages
1. research_brief
2. hypothesis_generation
3. innovation_expansion
4. validation_gate
5. backtest_specification
6. screening_backtest
7. walk_forward_validation
8. final_holdout_test
9. robustness_analysis
10. research_decision

## Context policy
- Default to minimal context.
- Maximum required reads per stage: 3 files unless explicitly justified.
- Prefer YAML/JSON artifacts over prose.