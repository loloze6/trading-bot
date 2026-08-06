# STEP_05_FINDINGS.md — brief specificity investigation

**Date:** 2026-06-30
**Status:** Investigation complete. Gate design proposed. Implementation pending review.

---

## Evidence base

Runs surveyed: run_011 through run_038 (28 runs, with gaps for unused numbers).
Files read: backtest_spec.yaml, research_brief.yaml, expanded_hypothesis_card.yaml,
hypothesis_card.yaml, findings_carryover.yaml (all available runs).
Sample for brief diff: run_012, run_017, run_025, run_032, run_035.

---

## Finding 1 — Variant selection never exercised

**0 of 28 runs** executed any variant beyond V1.

All unique variant_id values ever written to backtest_spec.yaml:
```
V1 / "V1" / V1-Conservative / V1-Base-Conservative /
V1-RSI-14-MR-4H-TRENDING / KELTNER_SCOREMODE_4H_V1_BASE
```

Every label is a V1-equivalent (first/base/only variant). No V2, V3, V4, V5, or V6
ever reached a backtest_spec.yaml. innovation_expansion generated up to 6 variants per
run (4 for run_017, 6 for run_025); all non-V1 variants were discarded by
backtest_specification in 100% of observed cases.

---

## Finding 2 — hypothesis_generation is a schema reformatter

For complete briefs (runs 017, 025 verified):
- research_brief.yaml → hypothesis_card.yaml: same single hypothesis, same params,
  translated into thesis/rationale/assumptions schema. No new parameters, no
  alternative signal directions, no material changes.
- Line counts: run_017 brief=49 lines → hypothesis_card=34 lines (shorter, reformatted).
  run_025 brief=44 lines → hypothesis_card=59 lines (slightly longer, same content).

For exploratory briefs (early campaign, runs 011-015): hypothesis_generation may have
added framing value. Not verified from this sample.

---

## Finding 3 — innovation_expansion generates untested space that pollutes downstream reasoning

For runs where the brief was complete and explicitly single-parameter-change:

| Run | Brief constraint | Expansion output | Variants executed |
|-----|-----------------|-----------------|-------------------|
| run_012 | "one variant only" | 1 variant (correctly respected) | V1 only |
| run_017 | "change ONLY ATR multiplier" | 4 variants (V1=2.0, V2=1.8, V3=2.2, V4=confirmation) | V1 only |
| run_025 | explicit constraint list | 6 variants (V1-baseline through V6-vol-adaptive) | V1 only |
| run_032 | "NO parameter changes. Replication only." | 1 variant (correctly respected) | V1 only |
| run_035 | partial (regime component TBD) | 4 variants (legitimate exploration) | V1 only |

**False reasoning injection (confirmed):**
run_017/findings_carryover.yaml `what_not_to_try` contains:
> "Do NOT refine band width further (ATR 1.8, 2.2): one-dimension parameter search already exhausted."
> "Do NOT add confirmation filters (multi-bar logic)"

ATR=1.8 (V2) and ATR=2.2 (V3) were never tested. The LLM authoring findings_carryover
read the expanded_hypothesis_card, saw V2/V3 listed as considered variants, and inferred
they were executed. Parameter space was permanently marked exhausted based on untested
proposals. The same inference was copied verbatim into run_018/findings_carryover.yaml.

No exact expansion variant_id labels appear in downstream artifacts by name — the
discarded variants are not cited as "V1-PIVOT-A-sweep-1.8 failed." The harm is indirect:
the category of parameter adjustments they represent gets foreclosed as "already tried."

---

## Finding 4 — Brief completeness by campaign phase

Early phase (runs 011-022): **Exploratory** — briefs are research questions without
full parameter specs. hypothesis_generation and innovation_expansion had genuine scope
to contribute.

Mature phase (runs 023-037, post-campaign-review wiring): **Complete** — 13 of 14 runs
(93%) have fully-specified briefs: exact component name, all numeric params, exact regime
thresholds, explicit constraint language ("DO NOT CHANGE", "change ONLY X", "Replication only").
Single exception: run_035 (regime component explicitly left open).

---

## Proposed gate: dual-signal brief_specificity check

### Gate logic (pseudocode — NOT implemented)

```python
STRUCTURED_ORIGINS = {"refine", "pivot", "reframe", "replication_diagnostic"}

CONSTRAINT_MARKERS = [
    "DO NOT CHANGE", "one variant only", "NO parameter changes",
    "Replication only", "change ONLY", "IDENTICAL to", "unchanged from",
]

EXPLORATORY_MARKERS = [
    "to be defined", "TBD", "to be determined", "novel component",
    "explore", "investigate whether",
]

def skip_expansion_stages(run_context, brief):
    """
    Returns True → skip hypothesis_generation + innovation_expansion,
                    enter pipeline at validation.
    Returns False → full pipeline from hypothesis_generation.
    """
    return (
        origin_guarantees_complete_brief(run_context)
        or brief_params_are_complete(brief)
    )

def origin_guarantees_complete_brief(run_context):
    if run_context.origin_stage not in STRUCTURED_ORIGINS:
        return False
    # First instrument escalation with no prior findings_carryover:
    # campaign_review may leave component selection open.
    if run_context.origin_stage == "escalate_instrument":
        return run_context.prior_context_available
    return True

def brief_params_are_complete(brief):
    all_text = " ".join([
        brief.signal_concept or "",
        brief.regime_filter or "",
        brief.change_from_previous or "",
        " ".join(brief.constraints or []),
    ])
    has_required = (
        brief.asset and brief.timeframe
        and brief.signal_concept
        and any(char.isdigit() for char in brief.signal_concept)
        and not any(m in brief.signal_concept for m in EXPLORATORY_MARKERS)
        and not any(m in (brief.regime_filter or "") for m in EXPLORATORY_MARKERS)
    )
    has_constraint_language = any(m in all_text for m in CONSTRAINT_MARKERS)
    return has_required and has_constraint_language
```

### Routing change (pseudocode)

```
# In run_loop(), after loading research_brief.yaml:
if skip_expansion_stages(run_context, research_brief):
    next_stage = "validation"   # enter here directly
else:
    next_stage = "hypothesis_generation"  # full pipeline
```

### What still runs (gate does NOT skip these)

- **validation** (devil's advocate) — always runs. A complete brief can still be
  logically flawed, contradicted by prior findings, or specify a config the
  regime_validity evidence already rules out.
- **backtest_specification** — always runs. Translating brief → valid JSON config
  (with validate_config.py gating, STRATEGY_CONFIG_REFERENCE.md lookup) is a genuine
  transformation regardless of brief completeness.

### Files that must change on implementation

1. `workflow/run_phase1_research.py` — add `skip_expansion_stages()` check in
   `run_loop()` before setting `next_stage = "hypothesis_generation"`.

2. `skills/validation/SKILL.md` (or whichever handles the validation stage) — add
   note: when invoked after specificity gate, input is `research_brief.yaml` directly,
   not `expanded_hypothesis_card.yaml`.

3. `workflow/stages.yaml` — `validation` stage's `required_inputs` currently lists
   `expanded_hypothesis_card.yaml`. For gate-bypassed runs: either accept
   `research_brief.yaml` as alternative, or have routing create a minimal stub
   `expanded_hypothesis_card.yaml` that wraps the brief (preserves downstream file
   expectations without re-running the stage).

4. `workflow_artifacts/skills/verdict-interpreter/SKILL.md` findings_carryover output spec — add guard:
   "If expanded_hypothesis_card.yaml was produced and contained variants beyond V1,
   those variants are PROPOSED, NOT EXECUTED. Do not list them in `what_not_to_try`.
   Only reference configurations that appear in a protocol_result.yaml."
   This closes the false-reasoning-injection gap for any residual runs where expansion
   does execute (exploratory briefs).

### Estimated impact

- Runs affected retroactively: 13-14 of last 15 (93% of mature phase)
- Per-run savings: ~2 LLM calls × ~$0.05-0.08 = ~$0.10-0.16/run + ~3-4 min wall-clock
- Campaign total (run_023 onward): ~$1.50-$2.25 and ~45-60 min avoidable overhead
- False-reasoning eliminated: the false-exhaustion pattern (run_017 findings_carryover)
  does not occur — no expanded_hypothesis_card → no untested variants to misread

---

## Decision checkpoint

This is a STOP point. No pipeline code changed in STEP_05.

Implementation requires review of:
1. Whether the stub expanded_hypothesis_card approach is preferred over updating
   validation/stages.yaml to accept research_brief.yaml directly.
2. Whether the "escalate_instrument with prior_context_available" condition correctly
   handles the ENHANCE_04 escalation flow (run_context.yaml written by _route_escalate
   before the LLM runs — confirm prior_context_available field exists or must be added).
3. The findings_carryover guard in verdict-interpreter/SKILL.md is independently
   valuable and should be implemented regardless of whether the gate is approved.
