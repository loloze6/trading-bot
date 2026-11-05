# CLAUDE.md (strategy-research)

The root `CLAUDE.md` hard rules (secrets, no lookahead, trial ledger, sealed
holdout) and working rules apply here too and are not repeated.

## 1. Objective and overview

A research-only trading strategy factory: it generates, expands, validates,
backtests, analyses and decides on strategy hypotheses, using the
`trading-bot/` engine as its backtester. Nothing here trades live.

Where to read:
- `docs/USER_GUIDE.md`: what the system is, its stages, artifacts, skills and tools.
- `docs/RUNBOOK.md`: how to operate a campaign (preflight, launch, status, pauses, resume, stop).
- `docs/CAMPAIGN_PROGRAM.md` (phase plan) and `config/campaign_queue.yaml` (queue state).
- `engineering/roadmap/EPICS.md` (engineering work) and `engineering/DECISION_LOG.md` (operator decisions).

### Workflow stages

The code is the source of truth: the stage registry
`workflow/run_phase1_research.py::STAGE_CONFIGS` and the `determine_post_*`
routing functions; `docs/USER_GUIDE.md` §2 describes them. The registry holds
12 stages: `hypothesis_generation`, `strategy_config_authoring`,
`innovation_expansion`, `validation`, `backtest_specification`,
`data_availability_gate`, `protocol_execution`, `verdict_interpreter`,
`analyst`, `regroup_record`, `campaign_review`, `holdout_evaluation`.
`research_brief` is the input, not a stage. Which stages a run reaches depends
on the `orchestrator.*` flags in `config/campaign_config.yaml`; for example,
with `orchestrator.verdict_routing_retired.enabled` on, a run ends after
`regroup_record` and decide-next picks the next run. Stage 4 is called
`validation_gate` in the docs and `validation` in the code.

## 2. Behaviour rules

- Default to minimal context: load only the files the current task needs, and
  never pass a full transcript or history by default (hand over files and paths).
- Write large outputs to files, not inline.
- Runtime records (operator decision 2026-10-17, Option C):
  - `runs/` is ignored (repo `.gitignore`): never stage a run file. Back run
    folders up outside git (copy only, junctions excluded). run_0001..run_060
    stay tracked on master as history; an ignore rule never untracks a file.
  - `campaign_record/` is committed once per session, as a docs PR from master.
    Its `composite/` folder is ignored: a backtest cache that
    `tools/composite_cache.py` rebuilds.
  - Nothing stays staged between sessions. Never run `git clean` in the main
    checkout: it would delete the ignored run folders, which exist nowhere else.

## 3. Development and test process

- Prefer structured YAML/JSON artifacts over prose for anything a stage or tool
  reads. A stage requires at most 3 file reads unless explicitly justified.
- A new stage is registered in `STAGE_CONFIGS` unconditionally and routed to
  only when its flag is on (the precedent of `data_availability_gate`,
  `strategy_config_authoring`, `analyst` and `regroup_record`).
- Artifact schemas warn, they do not stop: a violation of
  `workflow_artifacts/schemas/<stem>.schema.json` is only logged (blocking only
  under `WORKFLOW_ARTIFACT_VALIDATION=raise`; see
  `tools/workflow_artifact_validation.py`). A rule that must stop a run is
  written in code at the seam that reads the value.
- Tests (operator decisions 2026-10-03 and 2026-10-17; the full suite is too
  slow to run after every edit):
  - Interpreter: `../venv/Scripts/python.exe` on Windows (`../.venv/bin/python`
    on Mac/Linux); run strategy-research tests from `strategy-research/` (the
    workflow resolves the venv from the CWD). When `TBOT_PYTHON` holds an
    absolute interpreter path it is used first, so a worktree needs no venv of
    its own: `& $env:TBOT_PYTHON -m pytest <files>`. Never junction a venv into
    a worktree: checking out a commit from before 2026-09-09 (which tracked
    `venv/`) and moving away deletes the linked venv's files.
  - While developing, run only the test files the change touches and their
    direct neighbours.
  - CI runs the fast suite (`-m "not slow"`: trading-bot and strategy-research,
    including `tools/recorder/tests/`) on every push
    (`.github/workflows/tests.yml` -> `run_tests.py`, Ubuntu and Windows). Push,
    read `gh pr checks <n>`, fix what CI reports; do not also run it locally
    before every push.
  - Slow tests (marked `slow`: live market data, network) never run in CI. Run
    them on purpose when a change touches data fetching or the regression
    backtests: `python run_tests.py --slow` from the repo root.
  - Run the fast suite locally only when CI cannot be used, or for a large
    refactor, from the repo root: `venv/Scripts/python.exe run_tests.py -- -q -n 4`
    (4 workers, not 8: 8 crashed workers on memory on the 16 GB machine).
  - Never re-run a full suite for a test-only or doc-only follow-up fix; re-run
    the touched files and say so in the PR.
  - One test process at a time on this machine.
