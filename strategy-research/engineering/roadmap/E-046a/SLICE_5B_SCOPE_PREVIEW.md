# Slice 5b (specialist readers) — scope preview, not a full S1

Deliberately lightweight: a quick, direct grep-and-read pass done under a tight token
budget (quota nearly exhausted for the session), not the full characterize-and-STOP rigor
every other slice this session got. Purpose: give the operator a real, honest sense of
Slice 5b's actual size before deciding whether to greenlight a full S1/S2 dispatch cycle
for it — not a build-ready spec.

## Headline finding: the delivery plan undersells this slice's real scope

`delivery_plan_v26.md`'s own Slice 5 text names exactly 6 functions that read
`verdict_interpretation.yaml` and would need re-pointing/retiring once `verdict_interpreter`
is removed from `STAGE_CONFIGS`: `_inject_regime_context_into_handoff`,
`_auto_generate_findings_carryover`, `_write_kb_findings_entry`,
`_check_kb_reactivation_conformance`, `campaign-review/SKILL.md`'s required-input list, and
`tools/near_miss_scoreboard.py`'s schema-diversity reader.

A direct grep of every real reference to the literal string `verdict_interpretation.yaml`
across `strategy-research/workflow/run_phase1_research.py` alone finds roughly 13 distinct
call sites, not 4. `run_campaign.py` adds at least one more real reader
(`workflow/run_campaign.py:1487`). Some of these may collapse to the same 4 named functions
once traced (a function can reference the file more than once), but the raw count strongly
suggests the real caller surface is larger than the plan's own text implies. This needs a
full, real trace before Slice 5b is dispatched — not assumed from the plan's own list.

## Spot-checked, not exhaustively traced

- **`tools/near_miss_scoreboard.py`** — confirmed real, in-scope: reads
  `verdict_interpretation.yaml` directly (`:408`) and does schema-diversity analysis across
  the corpus (matches the plan's own naming).
- **`tools/killed_run_gate.py`** — writes a synthetic `verdict_interpretation.yaml` inside a
  TEST fixture helper (`_pipeline_N`), not production code. Not in scope for re-pointing.
- **`tools/anti_adjacency_gate.py`**, **`tools/lint_verdict_provenance.py`**,
  **`tools/record_schema.py`**, **`tools/verdict_criteria_evaluator.py`** — each has a
  comment *referencing* one of the named functions or the file, but none of the four reads
  `verdict_interpretation.yaml` directly themselves (confirmed by grep, not deeply read).
- **`workflow_artifacts/skills/campaign-review/SKILL.md`** — the delivery plan's own text
  says this skill's required-input list references `verdict_interpretation.yaml`. A direct
  grep for that literal string in the file found zero hits. Either the plan's claim is
  stale, or the skill references it under different wording (e.g. without the `.yaml`
  suffix, or via a variable name) — **not resolved here, needs a real check before Slice 5b
  is dispatched.**

## Not done at all (out of scope for this pass)

- No attempt to enumerate the ~13 `run_phase1_research.py` call sites individually or
  classify which are read-only consumers vs. ones that would need real logic changes.
- No read of `_validate_retune_firewall` (the regime reader's own firewall, per the plan's
  own text) or what re-pointing it at the new reader's output would actually require.
- No read of the five specialist-reader skill files' own current non-existence confirmed
  (i.e., verified none of them exist yet) but their target shape (per delivery_plan_v26.md's
  own text: `proposal_id`, `kind`, `patch`/`block sketch`, `evidence`, `scores`) not
  cross-checked against anything real.

## Recommendation

Treat this as a signal to budget MORE investigation time for Slice 5b's own S1 than the
other slices got, not less — the plan's own "6 functions" framing looks optimistic. A
proper characterize-and-STOP pass (matching Slice 3's or Slice 4's own rigor) is still the
right next step before any build; this note is not a substitute for that, only evidence
that it's worth doing carefully rather than assuming the plan's existing scope estimate.
