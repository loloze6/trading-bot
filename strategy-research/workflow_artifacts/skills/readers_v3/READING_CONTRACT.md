# Reading contract (readers v3, E-068 slice 5)

You read ONE report of a finished run and do two things: **explain** the measured result
through your report's lens, and **propose** what to test next. You never judge the claim. The
grid and the claim measurement already measured it; there is no field for a judgement, and
nothing you write grades the claim: you explain its numbers.

## Output: one fenced ```yaml block holding one mapping

```yaml
schema_version: 3
reading_id: <category>-<run_id>          # exactly as in your handoff's objective
model_id: <your model name>
rubric_version: <category>-reading-v1    # exactly as your SKILL says
explanation: >
  Why the result came out this way, in your report's terms, with numbers.
evidence:
  - "variants.base.slices.overall.<field>=<value>"   # field paths from your input files
side_findings:                           # 0, 1 or 2 -- `[]` when nothing else stands out
  - proposal_id: <reading_id>-1
    claim:                               # a FULL claim block, exactly as CLAIM_TESTS.md section 1
      statement: "..."
      kind: <one of CLAIM_TESTS.md's kinds>
      tests: [ ... ]                     # or `tests: none` with `missing_block: "..."`
      pass_if: "..."                     # pass_if / fail_if: what the claim predicts, in words
      fail_if: "..."
      rationale: "..."
    evidence: ["..."]
    scores: {confidence_real: 0-3, distance_to_profitable: 0-3, mechanism_plausibility: 0-3}
patch: null                              # or ONE patch:
#  proposal_id: <reading_id>-<n>
#  patch: [{component_id: <id in the base config>, field: <path inside it>, before: <current>, after: <new>}]
#  evidence: ["..."]
#  scores: {confidence_real: .., distance_to_profitable: .., mechanism_plausibility: ..}
```

Exactly these keys. Every `proposal_id` is the `reading_id`, a dash and a number, each used once.
A side finding or the patch may carry `requires_feed: {feed, reason}` when its test needs data
the run does not have (names: your handoff's `feed_names`).

## Rules

1. **Explain first.** Read `claim_result_digest.yaml` (the claim's tests and their effect sizes
   per variant: measured, not proven) with your report. If its `block_visibility` is `blind`,
   say so: the tests could not see the block, so base and variants measure the same.
   A statement about the claim cites the digest's numbers and names the statistic exactly as
   its `statistic_label` says (a rank IC is not the reports' Pearson `forecast_return_corr`).
2. **A side finding is something else the evidence shows.** Write its tests exactly as
   CLAIM_TESTS.md tells step 1a: only its blocks, never approximate, `tests: none` plus
   `missing_block` when no block expresses it. Code runs the same check as on step 1a's card.
   - If its `kind` names a block (`direction_forecast`, `volatility_forecast`: forecast;
     `regime_classifier`, `regime_transition`: regime), at least one test must read that block's
     output (CLAIM_TESTS.md's first rule).
   - Any other kind is a pure finding; its tests may read price only.
3. **Do not repeat.** A test already listed in `findings_summary_for_readers.yaml` or in this
   run's own claim (same selector, outcome, baseline, statistic and direction) teaches nothing
   new.
4. **No hindsight.** A proposal may act only on data at or before a bar's close. "Entering
   earlier" because the move is now known is hindsight, not a setting.
5. **A patch** names a component `id` that exists in the base config, a `field` inside it, and
   its current value as `before`. Code resolves it against that file and refuses anything else.
   Never patch a path `block_manifest.yaml` lists as scaffolding: scaffolding is not part of
   the idea.
6. **Never invent** a component class, transform, setting or regime name absent from
   COMPONENT_CATALOG.md, in any field, prose included.
7. **Nothing worth proposing:** `side_findings: []` and `patch: null`. The explanation is still
   required.

## Scores (they only rank candidates; 0-3)

- `confidence_real`: 0 = one cell of the report; 1 = base only; 2 = two or more windows;
  3 = most windows and every variant.
- `distance_to_profitable` (read `registry_summary.yaml`; the lower score wins when two apply):
  0 = the same block type as a registered block (`this_run.type_already_registered`, a
  `same_type` relation), or a patch on a registered block; 1 = the same component classes with
  another timeframe category or kind, or `this_run.correlation_to_composite.max_abs` >= 0.6;
  2 = a type not in the registry with `max_abs` 0.3-0.6 or not measurable (the default for a
  side finding); 3 = a type not in the registry with `max_abs` < 0.3, or no composite exists.
  Cite the registry field you used.
- `mechanism_plausibility`: 0 = no mechanism; 1 = a pattern only; 2 = a mechanism consistent
  with the evidence; 3 = a mechanism that names who is on the other side and why it persists.
