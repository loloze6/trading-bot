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

The pipeline is 12 numbered stages:

`research_brief` → `hypothesis_generation` → `innovation_expansion` →
`validation_gate` → `backtest_specification` →
`data_availability_gate` → `protocol_execution` → `regime_detector_validation` →
`regime_auditor` → `verdict_interpreter` → `campaign_review` →
`holdout_evaluation`

Two caveats the guide explains in full:

- The engine's own registry, `STAGE_CONFIGS`
  (`workflow/run_phase1_research.py::STAGE_CONFIGS`), holds **10** entries as
  of E-056 Slice 3b (2026-09-21). `data_availability_gate` (E-054 Layer 2)
  sits between `backtest_specification` and `protocol_execution`.
  **CORRECTED 2026-09-20** (delivery_plan_v26.md s:0.4 item 14): it is now ON
  BY DEFAULT, gated by `orchestrator.data_availability_gate.enabled` in
  `config/campaign_config.yaml` (default `true` — the one flag in this
  project that defaults on; see `feature_flag_register.yaml`), not the old
  `E054_DATA_AVAILABILITY_GATE` env var, which this change removed. So it
  now DOES appear in a default run's stage list. Only an explicit
  `enabled: false` reproduces the old skip-it behavior. There is no
  pre-backtest signal-prescreen stage — every run always executes a full
  backtest. `research_brief` is a human input; `regime_detector_validation`
  is a helper function; `regime_auditor` is not dispatched by the
  orchestrator at all; and there is no separate `refinement_planner` stage
  (E-039 S4, 2026-09-12) — a "refine" verdict from `validation_gate` produces
  its own refinement plan in the same call and loops back to
  `innovation_expansion` directly. **The 10th entry, `strategy_config_authoring`**
  (E-056 Slice 3b, 2026-09-21), is registered UNCONDITIONALLY — same
  documentation convention as `data_availability_gate`'s own addition — but
  only ROUTED to when `orchestrator.config_direct_authoring.enabled` is true
  (off by default). When on, it sits between `hypothesis_generation` and
  `innovation_expansion`, authors the single BASE strategy config, and the
  `validation` stage becomes naturally unreached (not deleted — its registry
  entry and code path stay intact for flag-off runs); `backtest_specification`
  becomes a deterministic tool stage instead of an LLM call, applying
  `innovation_expansion`'s `variant_patches.yaml` patches to that base config.
  See `docs/USER_GUIDE.md` §2.1/§2.2 for the full diagram.
- Stage 4 is `validation_gate` in the docs and **`validation`** in the code —
  the latter is the key you would grep for.

## Context policy
- Default to minimal context.
- Maximum required reads per stage: 3 files unless explicitly justified.
- Prefer YAML/JSON artifacts over prose.
