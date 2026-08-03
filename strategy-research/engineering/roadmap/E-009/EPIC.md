# E-009 — Pipeline harmonization

**State:** new
**Owner:** Jeremy
**Updated:** 2026-08-03

## Why

Carries forward 4 of the 5 items from the deleted `BACKLOG_DEFERRED.md`
(`workflow/LATER.md`, out-of-scope-for-`STEP6_ITER1_v2` items). The 5th —
"stages 6-10 skeletons (research-analysis, research-decision present but
empty)" — was checked this dispatch and is **stale**: neither
`skills/research-analysis/` nor `skills/research-decision/` exists anywhere
on master. It does not carry forward. The remaining 4 are still real,
verified-unchanged gaps in the pipeline machinery:

- **STAGE_CONFIGS/skill_map merge** — verified still separate:
  `STAGE_CONFIGS` (`workflow/run_phase1_research.py:87`) and two independent
  `skill_map` dict literals (lines 678, 862) duplicate the same stage→skill
  mapping in parallel, a standing source-of-truth-drift risk.
- **Override/narrowing merge of validation `sample_split` onto
  `baseline_v1.json`** — verified unbuilt: zero references to `sample_split`
  anywhere in `.py` files.
- **Auto-running the protocol from the pipeline** (`run_tool_worker`
  integration) — partially present (`run_tool_worker` is referenced in
  `run_phase1_research.py` and `tests/test_k3_protocol_pinning.py`) but
  whether it constitutes full pipeline auto-run wasn't established this
  dispatch.
- **Auto-repair loop** feeding `spec_validation_report.txt` VIOLATION lines
  back to the agent — `spec_validation_report` is referenced in
  `run_phase1_research.py`, but whether it already loops back or is a
  one-way report wasn't established this dispatch.

## Done when

Each sub-item closes independently and is checked off here as it does;
the epic itself closes when all four are done:

1. **STAGE_CONFIGS/skill_map merge:** `grep -n "skill_map = {" workflow/run_phase1_research.py`
   returns zero matches — a single `STAGE_CONFIGS`-derived lookup drives
   both call sites.
2. **sample_split override:** a documented merge/narrowing mechanism exists
   and a test exercises overriding `baseline_v1.json`'s `sample_split` via
   validation config.
3. **Protocol auto-run:** a test or documented run demonstrates the pipeline
   invoking `run_tool_worker` end-to-end without a manual intermediate step,
   or this sub-item is re-scoped once S3 below determines the true gap.
4. **Auto-repair loop:** a test demonstrates a VIOLATION line in
   `spec_validation_report.txt` triggering an automatic re-dispatch to the
   agent, or this sub-item is re-scoped once S4 below determines the true gap.

## Stories

- [ ] S1 — Merge `STAGE_CONFIGS` and `skill_map` into one source of truth.
- [ ] S2 — Build the `sample_split` override/narrowing merge onto
      `baseline_v1.json`.
- [ ] S3 — Establish exactly what's missing in `run_tool_worker` integration
      (read the current call sites first — this dispatch didn't), then close
      the gap or re-scope.
- [ ] S4 — Establish exactly what's missing in the auto-repair loop (read
      `spec_validation_report` consumers first), then build it or re-scope.

## Log

- 2026-08-03 — `new`. Written up in E-001 S4 (dispatch W24), carrying 4 of
  `BACKLOG_DEFERRED.md`'s 5 items forward (1 dropped as stale — see Why).
  Not started.
