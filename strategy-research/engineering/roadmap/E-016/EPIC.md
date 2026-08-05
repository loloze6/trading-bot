# E-016 — Fee-reduction autopsy field

**State:** in-progress
**Owner:** Jeremy
**Updated:** 2026-08-05

## Why

Source: `docs/ROADMAP.md` §1.4, verbatim: "**Fee-reduction autopsy field
(your addition, adopted).** Objective: cost-kills must generate ideas, not
just tombstones. Deliverable: whenever a kill's root cause is cost-dominated,
the autopsy must answer one mandatory question — *'is there a system that
reduces these fees?'* (maker-only execution, lower-frequency variant of the
same signal, different product, venue tier, batching) — and, if yes, register
the cheap variant as a new idea."

**UNPARKED (dispatch W38, tree audit) — the recorded blocker was false.** The
prior text blocked this on E-010 (fee/slippage attribution) and E-017
(autopsy standard v1 / cost decomposition), reasoning that a cost-dominated
kill "cannot be identified" before either exists. That's wrong: cost-dominance
is already identified today via the pre-existing
`root_cause.mechanism_failure == "signal_real_but_subscale_vs_costs"` enum
value (`schemas/verdict_interpretation.schema.json`, Improvement 01) — no
fee/slippage split from E-010 and no cost-decomposition metric from E-017 is
needed to reach that classification; it's an LLM verdict-stage judgment call,
already in the schema, already usable as a trigger. The mechanism works
today.

**VERIFIED shipped implementation:**
- `schemas/verdict_interpretation.schema.json:115-136` —
  `root_cause.fee_reduction_assessment`, mandatory whenever
  `mechanism_failure == "signal_real_but_subscale_vs_costs"`, with
  `has_fee_reduction_system` (bool), `candidate_system` (enum: the five named
  options), and `registered_as` (the cheap variant's brief filename, if any).
- `workflow/run_phase1_research.py:4416-4436` — `determine_post_verdict_route()`
  checks for a cost-dominated kill missing `fee_reduction_assessment` and
  prints a warning nudge.
- 3 tests: `tests/test_fee_reduction_assessment.py`.

## Done when

1. The autopsy process includes a mandatory field, triggered whenever a
   kill's root cause is cost-dominated: "is there a system that reduces these
   fees?" — evaluated against the named options (maker-only execution,
   lower-frequency variant of the same signal, different product, venue
   tier, batching). **MET** — see shipped implementation above.
2. When the answer is yes, the cheap variant is registered as a new idea,
   observable as a new registration entry that references the parent kill.
   **Schema-level MET** (`registered_as` field exists); no end-to-end example
   observed in `campaign_knowledge_base.yaml` yet.
3. NEW, the real gap: the source text says a cost-dominated kill **MUST**
   answer the fee-reduction question — but enforcement
   (`run_phase1_research.py:4428-4436`) is a non-blocking `print()` warning,
   while its two siblings in the same function
   (`component_execution_error` at :4386-4395, `regime_misattribution` at
   :4405-4414) both call `update_state(status="paused_for_human")` and
   `return "human_pause"`. A missing `fee_reduction_assessment` today does
   not stop the pipeline, so "mandatory" is not actually enforced.
   **IMPORTANT:** `run_phase1_research.py:4419-4427`'s own comment documents
   this as a *deliberate* choice — "this does not pause the pipeline -- it's
   a completeness gap in the autopsy, not evidence the verdict itself is
   untrustworthy," and notes `regime_attribution` (a different field) is
   similarly enforced only at the prompt/skill level with no code-side pause.
   The story below must read that reasoning first; it may conclude the
   *requirement* ("MUST") should be softened to match the deliberate design,
   rather than that the *code* should be changed to pause.

## Stories

- [x] S1 — Add the mandatory fee-reduction question to the autopsy template,
      gated on cost-dominated root cause. DONE — schema + wiring above
      (shipped before this epic was unparked; not tracked here at the time).
- [ ] S2 — Wire the "yes" branch to brief registration of the cheap variant
      end-to-end (schema field exists; no observed registration flowing from
      it yet).
- [ ] S3 — Resolve Done-when #3: read `run_phase1_research.py:4419-4427`'s
      stated rationale for the non-pausing design, then either (a) make the
      check blocking to match its `component_execution_error`/
      `regime_misattribution` siblings, or (b) formally soften the source
      text's "MUST" to a non-blocking nudge, recording why the deliberate
      choice stands. Do not change the code without first addressing the
      documented reasoning.

## Log

- 2026-08-05 — `new` → `parked`. Created from E-013 S1's audit of
  `docs/ROADMAP.md` §1.4 (dispatch W35). Parked: cannot proceed until E-010
  and E-017 exist. Resumes when both land.
- 2026-08-05 — `parked` → `in-progress` (dispatch W38). Tree audit found the
  blocking condition was false — the mechanism the epic needs
  (cost-dominated-kill identification) already existed via the pre-existing
  `signal_real_but_subscale_vs_costs` enum, and S1 had already shipped on
  that basis. Unparked; sharpened Done-when to the real gap (non-blocking
  enforcement vs. its two pausing siblings), noting the non-pausing choice is
  documented as deliberate in the code itself.
