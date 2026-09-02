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
the epic itself closes when both remaining items are done:

1. **STAGE_CONFIGS/skill_map merge:** `grep -n "skill_map = {" workflow/run_phase1_research.py`
   returns zero matches — a single `STAGE_CONFIGS`-derived lookup drives
   both call sites.
2. **sample_split override:** a documented merge/narrowing mechanism exists
   and a test exercises overriding `baseline_v1.json`'s `sample_split` via
   validation config.
3. ~~Protocol auto-run~~ — **split out to E-030, 2026-08-21.** See Log.
4. ~~Auto-repair loop~~ — **split out to E-030, 2026-08-21.** See Log.

## Stories

- [ ] S1 — Merge `STAGE_CONFIGS` and `skill_map` into one source of truth.
- [ ] S2 — Build the `sample_split` override/narrowing merge onto
      `baseline_v1.json`.
- ~~S3~~ — moved to `E-030` S1/S2.
- ~~S4~~ — moved to `E-030` S1/S3.

## Relationship to other epics

- **E-030** (halt recovery + a loop-health instrument) owns what were this
  epic's S3/S4. A `research-system-evolution` review (2026-08-21) measured
  that halt downtime — not auto-run/auto-repair in the abstract — is the
  binding constraint on the research loop (127 h of downtime across a 310.5 h
  campaign span, 84% of it plumbing, 67% still unfixed), which is a bigger and
  more urgent scope than either S3 or S4 as originally written. Both stories'
  own Done-when already admitted "or re-scope once the true gap is
  determined" — this is that re-scope. This epic keeps only the two
  mechanical refactors (S1, S2), which remain real and unstarted.

## Log

- 2026-08-03 — `new`. Written up in E-001 S4 (dispatch W24), carrying 4 of
  `BACKLOG_DEFERRED.md`'s 5 items forward (1 dropped as stale — see Why).
  Not started.
- 2026-08-21 — S3/S4 split out to **E-030**, on measurement from a
  `research-system-evolution` review (operator-approved same day). Neither
  story had been dispatched since filing; the split re-scopes them to their
  measured priority rather than leaving them as an under-sized pair of items
  inside a lower-urgency epic. Done-when and Stories updated to reflect the
  two remaining items (S1, S2).
