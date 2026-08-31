# CLAUDE.md

Start with `DOC_INDEX.md` — it maps every doc in this directory by the
question you're arriving with, not by file location.

## Project
Research-only trading strategy factory.

## Objective
Generate, expand, validate, backtest, analyze, and decide on strategy hypotheses.

## Global rules
- Use structured artifacts for all handoffs.
- Never pass full transcript/history by default.
- Load only the files needed for the current task.
- Innovation happens before validation.
- Validation is falsification-first.
- Promising ideas must pass screening, then walk-forward, then holdout.
- Large outputs must be written to files, not kept inline.
- After each stage, write a short summary artifact.

> **Schemas are declared but not enforced.** This file previously said
> *"Validate outputs against schemas before moving to the next stage."* That is
> false: no schema under `workflow_artifacts/schemas/` is loaded by any code —
> verified by grep across `workflow/` and `tools/`, where the only hits are
> source comments. Where enforcement genuinely exists it is written in code at
> the seam that reads the value. See `docs/USER_GUIDE.md` §3's preamble
> (corrected 2026-08-27) and E-037 [E037-09](engineering/roadmap/E-037/FINDINGS.md#e037-09).

## Workflow stages

**`docs/USER_GUIDE.md` §2.2 is authoritative.** Read it there rather than
here — this list is a pointer, kept short deliberately so it cannot drift out
of step again.

The pipeline is 13 numbered stages:

`research_brief` → `hypothesis_generation` → `innovation_expansion` →
`validation_gate` → `refinement_planner` → `backtest_specification` →
`signal_prescreen` → `protocol_execution` → `regime_detector_validation` →
`regime_auditor` → `verdict_interpreter` → `campaign_review` →
`holdout_evaluation`

Two caveats the guide explains in full:

- The engine's own registry, `STAGE_CONFIGS`
  (`workflow/run_phase1_research.py:88`), holds **10** entries. `research_brief`
  is a human input; `regime_detector_validation` is a helper function; and
  `regime_auditor` is not dispatched by the orchestrator at all.
- Stage 4 is `validation_gate` in the docs and **`validation`** in the code —
  the latter is the key you would grep for.

> **Superseded names.** This file previously listed five stages that do not
> exist in the pipeline: `screening_backtest`, `walk_forward_validation`,
> `final_holdout_test`, `robustness_analysis` and `research_decision`. Recorded
> rather than deleted because they document an intended design — and
> `workflow_artifacts/schemas/robustness_report.schema.json` still exists,
> though nothing produces it. The nearest real equivalents are
> `signal_prescreen`, `protocol_execution`, `holdout_evaluation`, and
> `verdict_interpreter` / `campaign_review`. See E-037
> [E037-09](engineering/roadmap/E-037/FINDINGS.md#e037-09).

## Context policy
- Default to minimal context.
- Maximum required reads per stage: 3 files unless explicitly justified.
- Prefer YAML/JSON artifacts over prose.
