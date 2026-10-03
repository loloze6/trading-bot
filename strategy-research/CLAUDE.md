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

> **Schemas are checked at write time, warn-only by default.** This file
> once said *"Validate outputs against schemas before moving to the next
> stage"*, and a later correction said no schema was loaded by any code. Neither
> is right now: `save_yaml` (and the standalone tools that write artifacts) call
> `tools/workflow_artifact_validation.py`, which checks an artifact against
> `workflow_artifacts/schemas/<file stem>.schema.json` when one exists. A
> violation is logged and swallowed (a bug in the check must never crash a write
> path); only `WORKFLOW_ARTIFACT_VALIDATION=raise` makes it block the write. So a
> schema is a checked contract, but a warning is not a stop: where a rule must
> stop a run it is still written in code at the seam that reads the value. See
> E-037 [E037-09](engineering/roadmap/E-037/FINDINGS.md#e037-09) for the
> original correction and the C5.7a schemas (`grid_evaluation`, `idea_status`,
> `variant_patches`, ...).

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
  (`workflow/run_phase1_research.py::STAGE_CONFIGS`), holds **12** entries as
  of E-058 S2a (2026-09-23). The 11th, `specialist_readers` (E-046a Slice
  5b-ii-B), is registered unconditionally but routed to only when
  `orchestrator.specialist_readers.enabled` is on (off by default), replacing
  `verdict_interpreter` after `protocol_execution` (see `docs/USER_GUIDE.md`
  stage 16). The 12th, `regroup_record`, is registered the same way and routed
  to only when `orchestrator.regroup_record.enabled` is on (off by default;
  requires `specialist_readers`): it sits between `specialist_readers` and its
  route and writes `campaign_record/campaign_memory.yaml` (`docs/USER_GUIDE.md`
  stage 17). With `orchestrator.verdict_routing_retired.enabled` also on
  (E-059 S3 / slice 6c S2a, off by default; requires `decide_next` and
  `profit_bars_every_backtest`), that route ends the run at
  `completed_<idea_status>` and decide-next picks the next run: refine /
  pivot / escalate / kill, the circuit breaker, continuation children and the
  route to `holdout_evaluation` are unreachable (code kept, marked
  `# legacy routing (v26 card G)`). `data_availability_gate` (E-054 Layer 2)
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

## Running the tests (operator decision 2026-10-03: the full suite is too slow to run after every edit)
- Always from `strategy-research/`: `../venv/Scripts/python.exe -m pytest ...` (the workflow resolves `../venv` from the CWD).
- **While developing:** run only the test files the change touches (and their direct neighbours). Seconds to a minute.
- **The full suite is CI's job.** Every push runs it on Ubuntu and Windows (`.github/workflows/tests.yml` -> `run_tests.py`, ~8 / ~14 min). Push, then read `gh pr checks <n>`; fix what CI reports. Do not also run it locally before every push.
- **Locally, only when CI cannot be used** (or a large refactor): `../venv/Scripts/python.exe -m pytest tests -q -n 4` (pytest-xdist). Measured 2026-10-03: serial ~20 min; `-n 4` 12.2 min, 0 failures; `-n 8` 15.6 min with 2 crashed workers (memory, 16 GB machine) -- use 4, not 8.
- Never re-run a full suite for a test-only or doc-only follow-up fix; re-run the touched files and say so in the PR.
- One test process at a time on this machine.
