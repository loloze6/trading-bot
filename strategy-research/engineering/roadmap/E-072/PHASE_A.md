# E-072 phase A: ideas are confirmed on data the proposer never saw

**Status:** built behind `orchestrator.explore_confirm.enabled` (off by default), D-080.
Written 2026-10-08, autonomously overnight; the operator reviews in the morning. No design
problem was found that makes the epic's goal unreachable, so the build went ahead. The
choices that are the operator's are listed under "Decisions for the operator", each with
the safe default taken and the alternative.

Plan: `engineering/delivery_plan_readers.md` (PR #339), item 1. Linear: E-072 (P-CUL-80).

## 1. What the readers see today (file:line on master `4d585c33`)

Every v3 reader input that carries a result is computed over **all** of the run's windows:

| Reader input | Built by | All-window content |
|---|---|---|
| `artifacts/reports/<cat>.yaml` | `tools/build_reports.py::build_reports` (called at `run_phase1_research.py:2429`) | `per_window` rows of every window; the `overall` slices of profitability (`build_reports.py:350-357`, `hypothesis_verdict.diagnostics`), trade_efficiency (`:456-462`, `trade_diagnostics_summary`) and forecast_power (`:501-506`) are run_protocol.py aggregates over every window |
| `artifacts/grid_evaluation.yaml` | `verdict_criteria_evaluator.evaluate_grid` (`run_phase1_research.py:2372`) | every cell; pooled cells read the all-window aggregate (`verdict_criteria_evaluator.py:1330-1338`); `idea_status` |
| `artifacts/claim_result_digest.yaml` | `reader_findings.claim_result_digest` (`reader_findings.py:221`) | each variant's `claim_test.yaml`, measured on every window (`claim_measure.py:224`, `measure_variant`) |
| `artifacts/findings_summary_for_readers.yaml` | `reader_findings.reader_findings_summary` (`:299`) | earlier runs' largest effect (`_largest`, `:285`), measured on their windows -- every run since run_065 uses the same six 2022-2023 windows, so these include this run's confirmation windows |
| `artifacts/registry_summary.yaml` | `block_registry.registry_summary` (`block_registry.py:541`) | `this_run.idea_status` (`:576`), this run's `correlation_to_composite` (`:586`), earlier blocks' residual IC |
| `artifacts/claim_measurement.yaml` (optional) | `_measure_claim_tests` (`run_phase1_research.py:16747`) | statuses only, but `no_events` vs `measured` is decided over every window |

The handoff that lists them is `_reader_handoff_v3` (`run_phase1_research.py:4332`); the
two code-written inputs are written by `_write_reader_v3_inputs` (`:5027`) at the stage
body (`_run_specialist_readers_stage`, `:5136`).

A side finding becomes a decide-next candidate (`decide_next.py:1557`) and its brief carries
`candidate.source.proposal_ref` (`decide_next.py:2134`), copied into the next run's
`artifacts/research_brief.yaml` (seen on run_072..074). That is the link a pending finding
is resolved through.

## 2. Design (as built)

One module, `tools/explore_confirm.py`; one flag; every orchestrator change sits behind
`_explore_confirm_enabled()`.

1. **Split, pre-registered before the backtests.** At protocol_execution entry
   (`run_tool_worker`'s preamble, next to the other protocol_execution clears),
   `_prepare_explore_confirm` writes `artifacts/explore_confirm.yaml`: the windows of the
   run protocol (`_resolve_protocol_path`) and of the variants' own protocol files, one row
   per label, in time order; first half = exploration, the rest = confirmation (rule
   `chronological_half`). For the current 6 x 4-month protocol: 2022-01/2022-05/2022-09 vs
   2023-01/2023-05/2023-09. A re-run keeps the file; a window in neither half raises; fewer
   than 2 windows raises (nothing has been spent yet). The previous attempt's
   `artifacts/exploration/` and `confirmation.yaml` are removed.
2. **Readers' copies, exploration windows only** (`artifacts/exploration/`):
   - `reports/<cat>.yaml`: `build_reports(..., only_windows=...)`, written right after the
     real reports in the variant loop. Sources are cut to the exploration windows
     (`restrict_sources`: a protocol_result keeps only its `results` entries for those
     windows; trades and bars likewise); the three pooled `overall` slices are
     `unavailable: withheld ...`; each report carries `windows_shown`.
   - `grid_evaluation.yaml`: each `window`-source criterion re-evaluated by the grid's own
     cell function (`_evaluate_grid_cell`) on the exploration results; every other source
     (pooled, profit bars) and the idea status are `withheld`.
   - `claim_result_digest.yaml`: the digest's descriptive part plus each variant's claim
     tests **measured again** on the exploration windows (`claim_measure.measure_test` on
     the variant's bars, cut to those windows).
   - `findings_summary_for_readers.yaml`: earlier findings with `largest_effect: withheld`
     (what was tested stays, so a reader still does not repeat a test).
   - `registry_summary.yaml`: this run's idea status and correlation, and earlier blocks'
     residual IC / correlation, withheld.
   A failure of the reports/grid copies fails protocol_execution (like the reports
   themselves under specialist_readers); a failure of the registry copy stops the stage;
   the digest/summary copies follow slice 5's rule (a gap, the reader runs without it). The
   readers never fall back to the all-window files.
3. **Handoff.** `_explore_confirm_handoff` swaps every result input for its exploration copy,
   drops `claim_measurement.yaml`, adds `readers_v3/EXPLORATION.md` (a flag-on-only input;
   the v3 SKILLs and READING_CONTRACT.md are untouched) and
   `injected_context.explore_confirm.exploration_windows`.
4. **Confirmation, after every reader** (`_record_confirmations`, information only, never
   raises). Per side finding (`finding_route`):
   - pure (claim kind not mapped to a forecast/regime block by `claim_card.KIND_BLOCK`):
     measured in this run on the **base variant's** bars, confirmation windows only;
   - block claim (forecast/regime), or a pure finding whose `config_change` alters the
     forecast/regime its tests read: `pending`;
   - no usable test (`tests: none`, refused claim): `not_measurable`, retained `null`.
   A pending finding is resolved when a run whose `research_brief.yaml` names it
   (`candidate.source.proposal_ref`) reaches its readers stage: that run's own card tests
   on that run's own confirmation windows (base variant). If those windows overlap the
   windows the proposer saw, it stays pending (the attempt is recorded).
5. **Sign rule.** A test held when at least one horizon has a value and every horizon with a
   value has the claimed sign (`oriented > 0`); no events on the confirmation windows =
   not held. A finding held when every test held. Recorded as
   `confirmation_sign_retained: true | false | pending` (`null` only for not_measurable or
   an error).
6. **Looks.** `campaign_record/confirmations.yaml` keeps every finding's latest record and
   every look (run, finding, spec_hash -- idempotent on a resume), with totals per
   confirmation set: `n_looks` (tests) and `n_comparisons` (test x horizon). Each measured
   record carries its position on the set. The campaign summary shows the counts. The bar
   text on every record: "the sign held (or not) on windows the proposer never saw, counted
   against the looks taken on that confirmation set; not proven".

Flag off: no split, no exploration copies, no confirmation, no ledger; the handoff, the
prompts, the proposals and the campaign summary are unchanged (tests prove it).

## 3. Decisions for the operator

Each was taken with the safe default so the build could continue.

1. **The split rule.** Default: time order, first half exploration, an odd count gives the
   extra window to confirmation. Alternative: explicit `exploration_windows` /
   `confirmation_windows` in the config or the protocol.
2. **The run's own grid and idea status stay all-window.** The run's pre-registered idea is
   still graded on every window (routing and decide-next unchanged); only what the readers
   see is cut. Alternative: grade the idea on exploration windows too (changes routing).
3. **Pooled numbers are withheld, not recomputed.** The pooled `overall` slices, pooled grid
   criteria and the registry correlation are `withheld` rather than recomputed on the
   exploration windows (recomputing would duplicate run_protocol.py's aggregation).
   Effect: the readers score `distance_to_profitable` without `max_abs` (READING_CONTRACT's
   "not measurable" default, 2). Alternative: recompute them on the exploration windows.
4. **Earlier runs' numbers are withheld in full.** Every run since run_065 used the same six
   windows, so an earlier effect mixes in this run's confirmation windows. Alternative:
   show an earlier run's numbers when its windows do not overlap this run's confirmation
   windows (needs each finding's windows).
5. **Which bars measure a pure finding.** Default: the base variant (`base`, else the first
   graded id). Alternative: every graded variant, retained only when all hold.
6. **The sign rule is strict.** Every horizon with a value must hold; no events = not held.
   Alternative: the majority of horizons, or the test's first horizon only.
7. **Confirmation results are information only.** decide-next does not read them (no
   ranking or eligibility change). Alternative: decide-next skips (or ranks down) a
   candidate whose sign was not retained -- a separate, explicit decision.
8. **Confirmation results are not shown to the readers.** A later run's readers do not see
   which earlier findings held (that is one bit of confirmation-window information per
   finding). Alternative: show it, counting it as a look.
9. **Prose is not filtered.** `hypothesis_card.yaml` (the claim and 1a's rationale) and an
   earlier finding's `statement` are given as written; step 1a may quote earlier runs'
   all-window numbers in prose (run_074's card does). Alternative: give the readers a card
   copy without `rationale`, or ask 1a not to quote numbers (a SKILL change).
10. **Variant loop required.** The flag requires `variant_loop` (the split and the
    measurement read the variants' protocol files and bars); a non-variant run is refused.

## 4. Residuals (outside this epic)

- Step 1a/1b and innovation_expansion are proposers too; they still see earlier runs'
  all-window results (campaign memory, findings summary, the brief's evidence). E-072 cuts
  the readers only, as the epic states.
- The confirmation set is the same for every run on the 2022-2023 protocol; each look spends
  it. The ledger counts the looks; more years come from E-066.
