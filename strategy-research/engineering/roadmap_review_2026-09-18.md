# Engineering Roadmap — Review and Redesign Record (2026-09-16 → 2026-09-18)

Companion to `engineering_roadmap.html` v26 (v25 was the first rewrite; Part 4 below records the second). The board is the source of truth; this file is the
record of what was found, what was decided, and why the board changed shape. It supersedes
`roadmap_review_2026-09-16.md` (that pass's finding 2 introduced an error corrected here).

## Part 1 — Code-verified review of v24 (2026-09-16)

Every "today" claim was checked against the real files. Findings that did not survive:

| # | v24 claim | What the code says | Evidence |
|---|---|---|---|
| 1 | Walkthrough covers every step | The `validation` stage (approve / refine with budget 2 / reject) is absent from it | `run_phase1_research.py::determine_post_validation_route` (≈L2257), `quant-validation/SKILL.md` |
| 2 | Acceptance criteria are authored at Step 1 | `pass_rule` is copied from the brief at run creation, or from the previous run's LLM-written `proposed_brief.yaml` | `run_campaign.py` L304-324 (fresh), L484 (refinement child) |
| 3 | A run includes cost-stress and era-stability checks | No cost multiplier exists in `tools/` or `workflow/`; generated protocol = symbols, timeframe, monthly windows, holdout, promotion | `_ensure_protocol_from_constraints` (≈L2825-2836); era tag only at `run_protocol.py` ≈L855 |
| 4 | "Objective 1 is solid" | 60 run dirs; 10 `pre_registration.yaml`; 3 dict-shaped `pass_rule`; **1** `pass_rule_evaluation.yaml` in the corpus. Holdout gate never reached (code comment ≈L5104) | measured 2026-09-16 |
| 5 | The resolver only consumes symbol/timeframe, never chooses | `_route_escalate` → `_next_instrument_from_universe` / `_next_timeframe_from_universe` → `_create_escalation_protocol` | ≈L3681-3760, L3908-3955 |
| 6 | Step 3 data check "built and working" | E-054 gate is behind env var `E054_DATA_AVAILABILITY_GATE` (L98), never set by `run_campaign.py`, absent from `config/feature_flag_register.yaml` | verified |
| 7 | Registration function called once | Two `REGISTER:` lines in `campaign_record/campaign_log.md` (2026-07-18, 2026-08-27) | verified |
| 8 | "Skip re-deriving" is a small skill fix | Every refine child restarts at `hypothesis_generation` (`setup_run.py` L68; `_materialize_refinement_run` docstring) | verified |
| 9 | One "decide what's next" | Three: verdict routes scaffold the child immediately (`_route_refine` ≈L3805, followed by `run_campaign.py` L2255-2260); campaign review on 2+ failed families or every 6 runs; E-031's queue | verified |

Also verified and accurate: E-036's rejection account; CUL-267's premise (but the binding evaluator is
`tools/verdict_criteria_evaluator.py`, not the keyword matcher the ticket names); E-031 S3 unbuilt;
all board statuses vs Linear; E-018 firewall test removed; E-039's ~3m45s figure.

Per-window vs per-variant metrics, measured on `runs/run_059/artifacts/protocol_result.yaml`:
98 windows × 14 core metrics per window; 4 addressable per-variant fields; 9 diagnostic medians.

## Part 2 — Target-design decisions with the operator (2026-09-17/18)

Recorded on the board as cards A–J. Summary:

- **A. Building blocks.** One idea = one candidate block; validated blocks enter a registry; a block must hold information (residual IC vs the current composite). Old runs' verdicts are legacy.
- **B. Two pass bars.** Idea criteria per hypothesis from an anchored menu; profitability bars campaign-wide, in one manual file.
- **C. The grid.** Criteria × variants, cells mechanical; windows aggregated within a variant per the criterion's own reducer; unanimity across variants; sample floors → inconclusive; one symbol per variant by default, symbol reducer only for cross-sectional universes.
- **D. Three variants, cap four** (base + design diff + asset diff on a different coin category). Retires "no cap" (09-15) and "parameter X default 2" (09-01).
- **E. Protocol = time + cost only.** Symbol, universe, timeframe are design fields.
- **F. Composition runs** are their own run, code-triggered when the registry changes; variants = weighting schemes. Regime ideas = composite variants, gated vs ungated; A2.3 rule lifted.
- **G. Verdict routing retired.** Idea status validated / refuted / inconclusive; next-run choice is a separate step.
- **H. Order:** branches 1–3 in parallel → record memory → decide → park → holdout only after a manual stop.
- **I. Selection:** mechanical gates (novelty, feasibility, registry-changed rule) → LLM scores on anchored 0–3 rubrics (confidence real; distance to profitable; mechanism plausibility) → trivial rank, ties to cheapest.
- **J. Component gap** detected at spec time by code; gapped variant = not tested; fewer than three left → inconclusive.

Challenges raised and settled along the way: LLM verdict rejected (not pre-registrable); averaging
across variants rejected (hides setup dependence); "requires new data" flag rejected as duplicate
of E-054; one-symbol-per-variant kept as default, not a hard rule (would ban cross-sectional lane).

## Part 3 — Board changes applied in v25

Ordered plan: 16 items. New: profit-bars file (2), cost-stress axis (3), E-033.1 as a real item (6),
block registry + composition re-scoping E-044 (9), regroup-and-record (10), verdict retirement (11),
E-054 switch-on (14), validation-stage decision card (16). Merged: CUL-298 → E-046b; shared-queue
item → E-031; E-054.1 → item 14; skip-re-deriving → item 11. Superseded: E-040 → E-046a regime
reader + criterion menu. Moved into plan: E-035 (+ feed lane). Backlog: 20 entries, 8 categories.
Walkthrough: 15 steps (0, 1a, 1b, 2, 2b, 3, 4, 5a, 5b, 6–12) + two notes (composition, regime).

## Still open after v25 (superseded by Part 4 — kept for the record)

- Plan item 16 / Step 2b: settled in Part 4 — the validation stage is deleted.
- Linear reconciliation (needs the connector re-authorised): create the new issues/epics, move
  CUL-298 under E-046b, close E-040 as superseded, re-scope E-044/E-031/E-035, add decisions A–J to
  the relevant project descriptions.

## Part 4 — Operator's remarks on v25 and the resulting v26 (2026-09-18)

Seventeen remarks on the concept cards and the walkthrough, all applied. Net design changes:

| Point | Decision |
|---|---|
| Criteria vs variants | Criteria are scale-free; type + threshold fixed at 1a; only the sample is measured per variant; non-scale-free criteria refused (CUL-267) |
| Cost stress | Not a protocol axis. Cost survival is a criterion from the trade records (fees + funding + slippage per E-010, done; E-053 sub-daily funding still open). Protocol owns windows only |
| Criterion menu owner | E-046b (item 7) |
| Regime rules | A second kind of building block (regime block), stored as its detector rule; validated as composition variants |
| Component gap | No build backlog. Variant not tested; idea parked "waiting for component" with a request file; loop continues |
| Human cases | Runbook rows for every case: what to read, decide, which artifact to update, resume command (into Step 10). Deliverable of item 11 |
| Briefs with several hypotheses | Extras to the queue with the brief as source; brief status open/exhausted; Step 10 asks open briefs before stopping. Tracked as an E-031 sub-issue |
| Entry point | Every candidate enters at Step 1a; pass-through for already-formed ones (E-056 scope). The "skip re-deriving" rule is needed after all, at 1a |
| Validation stage | Deleted outright, nothing parked; plan item 16 (decision) removed |
| Repeat check | Exact match on config hash + instrument + timeframe + window set; neighbours are information (E-036 shrinks) |
| 1b output | **The real bot config**, written by an LLM under a design guide, plus manifest + rationale. No separate design doc, no translator. Variants = patches. 5a = validate + apply, no LLM |
| Auditor's checks | "Label beats ignoring it" → regime-block criterion; lag + health → regime-power report metrics; firewall → reader rule. No judgment stage |
| Restart after stop | Resume command re-enters Step 10; runbook row |
| Composition | Triggered by code (registry changed); brief written by Step 10; **config assembled by the LLM at 1b** (blocks live at different levels: component / sub-strategy / regime rule — not a merge); checked at 5a; E-048 is a prerequisite and moves into the plan (item 16) |

Board: 16 items (7 not yet created, 0 decisions open); backlog 19 entries / 8 categories; walkthrough
14 steps + 3 notes (composition, regime blocks, runbook); source section gained a third verbatim block
of the operator's own words.

## Next pass (agreed)

1. Delivery sequence, on paper: the ordered slices to reach the target state, with the run budget per slice.
2. Missing Linear artifacts: issues for items 2, 3, 6, 9, 10, 11, 14; E-031 sub-issue (brief-sourced
   entries + brief status); CUL-298 under E-046b; E-040 superseded; E-044 re-scoped; E-056/E-057/E-036
   re-scoped; E-048 promoted; decisions A–N pasted into the relevant project descriptions.

## Part 5 — Delivery-plan review corrections (2026-09-19/20)

The operator tried to review `delivery_plan_v26.md` directly and found it too implementation-
dense to review line by line — the right outcome, since it is written for agents, not for
operator review. Four genuine guesses (design choices I made without ever asking) surfaced
while checking the plan's own coherence against the agreed cards, and were put to the operator
as plain questions rather than buried in the document:

1. **Composition epic identity.** I had reused E-044 ("run several proven strategies at once,"
   a live-portfolio idea) for the new block-composition capability. Operator: these are
   different concepts; composition gets its own new epic (**E-060**). E-044 is untouched.
2. **E-048 as a gate.** I had made ensemble-standardisation (E-048) a hard prerequisite of the
   first composition run. Operator corrected this: the strategy config already has a transform
   pipeline per component, so the design guide should simply apply the existing standardisation
   op when assembling a composite; E-048 is only promoted into real work if a specialist
   reader's finding from a real composite result says the existing transforms are not enough —
   an ordinary queue proposal, not upfront engineering. E-048 stays in the backlog.
3. **`verdict_interpreter`'s fate.** I had left this open ("keeps the explanation role" vs.
   "folded into the readers"). Operator: delete it. The five specialist readers are the whole
   explanation layer.
4. **Cross-coin eligibility for composition.** I had marked this an open characterisation
   question. Operator: any validated block is usable in a composite for any instrument, not
   only the coins it was tested on — the composite's own grading against the profit bars is
   the real check, not an upfront filter.

Applied to both `engineering_roadmap.html` (now **v27** — card F, item 9 renamed and its text
corrected, the E-048 plan item removed and returned to backlog, tallies fixed, a new gaps-list
entry added) and `delivery_plan_v26.md` (slice 7 rewritten, slice 5b's verdict_interpreter
framing corrected, the Linear table's E-044/E-048 rows corrected and an E-060 row added).
Both files re-verified for tag balance / stray references after the edits.

**Process note for next time:** an implementation-facing document like the delivery plan should
ship with its own short "guesses" section up front — the handful of design calls made to fill a
gap that were never explicitly discussed — so the operator can confirm those in plain language
without having to review the whole document. This review is adopted as the standing practice.
