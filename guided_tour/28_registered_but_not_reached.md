# Stop 28: Registered but not reached

## Speech (verbatim)

**Stop 28 of 29: Registered but not reached.** Open on the side: `run_phase1_research.py`, `run_campaign.py`, `campaign_config.yaml` (the top and the bottom), `workflow_artifacts/skills/` (five folders), `workflow_artifacts/templates/`, `workflow_artifacts/schemas/`.

**In one sentence.**
This stop lists what the process still carries but does not run today: whole steps, AI role sheets, the old routes after a verdict, queue branches, and settings of removed steps.

**Why it exists.**
The process changed step by step, each change behind a switch (a yes/no setting in the campaign config). The rule was "bypass, not delete": a replaced step stays registered, so a run under the old switches still works and a switch can be turned back (decision D-008, a row of the decision log).
So the code holds pieces that look live and are not. Without this list, someone could fix or trust a piece no run uses, or believe a check protects a run when it never fires.

**What comes in, what goes out.**
- In: the current switches, read at every step.
- Out: nothing. These pieces write no file on a run today. A guard stops a run that lands on one by accident, before any spend.
- Example: run_102 went through eight steps, none of those below (stop 05b; run_102's own files are not in this checkout).

**What happens here, step by step.**
1. Validation (an AI devil's advocate that judged the idea before any config existed). With config-first authoring on (an AI writes one base config, then small variants), step 2 goes straight to variant building. Validation, its refine loop and its route are skipped.
2. AI backtest engineering (an AI that wrote the config after validation). Code now builds the variants. The AI path, its route and its variant-choice record are skipped.
3. The verdict interpreter (an AI that chose refine, pivot, escalate, kill or promote after the backtest). With the pass/fail grid on, the backtests lead to the analyst, the record, then the grid's own route. Skipped with it: the old verdict routes, the circuit breaker (a cap on repeated refines), the old review trigger, the promotion audit, the regime-detector check.
4. The regime auditor (a role sheet judging the market-regime detector) is never called by the loop; a person runs it by hand.
5. The campaign review is reached only by its cadence; the holdout step (the one-time test on sealed months) only through the profit-bars stop and an operator unlock. Any other arrival pauses, nothing spent.
6. A second AI engine (Gemini) has a worker; no step template names it.
7. The launcher (the program that runs the queue) refuses an operator follow-up brief on an existing line, never follows a run minted by the old routes, queues extra idea cards instead of spawning sibling runs, and refuses the fold re-run (same config on another fold, a fixed set of test months) while the variant loop is on.
8. Switched off: the deviation pause after step 1b; extra cards queued as soon as step 1a ends; quarantine (going past four kinds of halt).
9. Five config sections belong to removed or bypassed steps: the old prescreen (removed), episode significance, the regime-detector check, the verdict thresholds, the BTC-ETH correlation. No running code reads them.

**What it costs and how long it takes.**
No cost: none of these pieces runs.
12 registered steps: 2 never reached, 1 run as code instead of AI, 2 reached only by a trigger (`run_phase1_research.py:156-256`).
5 role sheets never loaded by a run: 207, 230, 787, 117 and 548 lines (`workflow_artifacts/skills/`, counted with wc).
14 code blocks carry the code's marker for the old verdict routing; 13 are not called today, the 14th runs only its first line (`run_phase1_research.py`, grep).

**What is switched off or not used here.**
- The research-system-evolution role sheet is for a person; no code loads it.
- Validation's two output templates are empty files.
- Shape checks (schemas) exist for eight files no run writes today.
- 4 of the 9 step templates copied into every run serve skipped steps.
- The old stage list sits archived under epic E-033 (an E-number is an engineering epic); no code reads it.
- The wishlist-status writer has no workflow caller; a test and the review's role sheet name it.
- Beside the run: `protocols/` (15 fixed files; a brief may name one), `archive/`, `tools/recorder/` (a separate recorder, data reserved), `quarantine/` (named only, never opened).
- The tools README rates 20 of the 81 tracked entries of `tools/`; two of its 20 files are gone.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Registry | `run_phase1_research.py:156-256` | 12 entries; `validation :184-196` (next: validation's own route), `backtest_specification :197-201`, `verdict_interpreter :216-220`, `campaign_review :246-250`, `holdout_evaluation :252-255` |
| Skill map | `run_phase1_research.py:1019-1027` | `quant-validation`, `backtest-engineering`, `verdict-interpreter`, `campaign-review` mapped |
| Validation skipped | `run_phase1_research.py:20233-20234` | Step 2 → `backtest_specification` when `config_direct_authoring` is on; not reached under the current flags |
| Validation route | `run_phase1_research.py:20189-20197`; `:9749-9765` (`determine_post_refinement_route`); `:9766` (`determine_post_validation_route`) | Not reached under the current flags, skipped at `:20233` |
| Validation inputs | `run_phase1_research.py:3173-3184` (closed-book inputs); `:1730-1742` | Validation inputs; with config-direct on and no validation protocol, backtests get `--diagnostics-only` |
| 5a as a tool | `run_phase1_research.py:9671-9680` | `backtest_specification` joins the tool stages when `config_direct_authoring` is on |
| AI 5a route | `run_phase1_research.py:20257-20328`; `:19564` (`determine_post_spec_route`); `:9220` (`_record_variant_selection`); `:9464` (`_route_post_variant_selection`) | Not reached under the current flags, skipped at `:20246` (the config-direct 5a branch is taken first) |
| Verdict skipped | `run_phase1_research.py:20177-20179` | Backtests → analyst / regroup / grid route when `grid_evaluation` is on; not reached, skipped there |
| Verdict guard | `run_phase1_research.py:19972-19977` | A run found at `verdict_interpreter` raises before the call |
| Verdict prep and route | `run_phase1_research.py:20013-20050` (regime report `:20026` → `_ensure_regime_detector_report :10143`); `:20555-20571` (`determine_post_verdict_route`) | Not reached, skipped at `:20177` |
| Old verdict routes | `run_phase1_research.py:11739-12060` (escalation and timeframe protocols, `_route_refine :11785`, `_route_pivot :11844`, `_route_escalate :11906`, `_route_kill :11993`, `_route_campaign_terminate :12029`); `:12977` (`_should_trigger_campaign_review`); `:15820` (`_apply_circuit_breaker`); `:15866` (status map); `:15888` (`_resolve_verdict_fields`); `:15999` (`_dispatch_verdict_route`, promotion audit call `:16054` → `_write_promotion_audit :13411`); `:16117` (`determine_post_verdict_route`) | 13 marker comments: not called under `verdict_routing_retired` |
| Campaign review route | `run_phase1_research.py:16290-16297` | 14th marker; under the flag only the first line runs (`_route_retired_campaign_review`) |
| Regime auditor | `run_phase1_research.py:16162-16172`; `tests/test_guide_covers_the_code.py:47` | Named in a pause message on the old route; "never dispatched; a human runs the skill" |
| Campaign review entry | `run_phase1_research.py:20611` → `_retired_review_route :7867`; guards `:19911-19936` | Reached only by the cadence; any other arrival pauses (`campaign_review_refused`) or fails |
| Holdout entry | `run_phase1_research.py:7515` (`_holdout_unlock_route`); refusal `:19856-19909`; branch `:20626` | Reached only by the profit-bars stop plus an unlock (stop 27) |
| Gemini | `run_phase1_research.py:1576` (`run_gemini_worker`), choice `:9741-9747` | No handoff template sets `assigned_engine: gemini` |
| Deviation gate | `run_phase1_research.py:16884`; call `:18919-18920` | Flag `deviation_gate` off |
| Sibling split | `run_phase1_research.py:11616`, skipped at `:11651-11652` | With `decide_next` on, extra cards go to the queue |
| Refinement brief | `run_campaign.py:4546-4554` (halt); `:4555-4591`; `:1037-1166`; `:4400-4404` | Not reached under the current flags, refused at `:4546` (`verdict_routing_retired` on) |
| Old continuations | `run_campaign.py:122`; blocker `:268-292`, used `:4625-4631`, `:4794-4803`; append `:4832-4845` | A continuation minted by the old routing halts; the append is not reached |
| Split children | `run_campaign.py:4294-4303`; `:2931`; `:4337`, `:4488` | Fed only by sibling splits, which `decide_next` replaces |
| Extra cards at 1a | `run_campaign.py:4319-4334`; holder `:4646-4647`; `:4463-4466` | Flag `extra_cards_at_1a` off |
| Quarantine | `run_campaign.py:4683-4769` | `halt_policy.quarantine_enabled: false`, read `:1993-2007` |
| Decide-next off | `run_campaign.py:4869-4871` | The flag-off outcome; `decide_next` is on |
| Fold re-run | `run_campaign.py:5633-5762`; refusal `:5680-5688`, applied `:5767-5774` | Refused while `variant_loop` is on |
| Wishlist status | `run_campaign.py:1380-1455` | Single writer; no caller in `workflow/`; `tests/test_d198_kept_clarity.py:175` |
| Wishlist check | `run_campaign.py:1458-1487`, used `:1744` | Runs only when a campaign review wrote its file |
| Config sections | `campaign_config.yaml:18-43` (`prescreen`), `:51-61` (`episode_significance`), `:67-82` (`regime_detector`), `:1117-1126` (`verdict_interpreter`), `:1132-1145` (`symbol_correlation`) | No reader in `workflow/` or `tools/` by grep; `run_campaign.py:1999` names an absent reader |
| Skills | `workflow_artifacts/skills/quant-validation/SKILL.md` (207), `backtest-engineering/` (230), `verdict-interpreter/` (787), `regime-auditor/` (117), `research-system-evolution/` (548) | Not loaded by a run under the current flags |
| Templates | `workflow_artifacts/templates/validation_protocol.yaml`, `validation_decision.yaml` (0 bytes); `templates/handoffs/innovation_expansion_to_validation.yaml`, `validation_to_backtest_specification.yaml`, `protocol_to_verdict_interpreter.yaml`, `backtest_spec_to_protocol_execution.yaml` | Copied at launch by `workflow/setup_run.py:115-118` |
| Schemas | `workflow_artifacts/schemas/{validation_protocol,validation_decision,refinement_notes,verdict_interpretation,regime_audit_decision,promotion_audit,variant_selection,variants_not_pursued}.schema.json` | Applied by stem (`tools/workflow_artifact_validation.py:102-110`) |
| Old stage list | `engineering/roadmap/E-033/artifacts/stages_yaml_ARCHIVED_not_authoritative.yaml:1-25` | "Does not drive the pipeline"; no code reader |
| Tools README | `tools/README.md:6-16`, entries `:20-545` | STATUS column; `power_check.py` (`:287`) and `prescreen_signal.py` (`:316`) absent from `tools/` |
| Folders | `protocols/` (read by name `run_campaign.py:505`, `:4134`); `archive/`; `tools/recorder/` (`RUNBOOK.md:19-20` reserved data); `quarantine/` | Not part of a run; `quarantine/` not opened |

Remarks: send them as "stop 28: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

Lot of legacy stuff. 
Here again we are weighting ourself and the engineering process keeping those
I am even at the step of wondering if we should not even recreate a workflow from scratch knowing the amount of legacy stuff / comment / extra cleaning necessary identified over the stops..

## Inspector notes

(Checkout note: the committed switchboard has 6 of 34 flags on, so in this checkout "not reached" and "reached" trade places for most of the list; the notes judge the tour's flag set, as the speech does. `quarantine/` does not exist in this checkout.)

### (1) Design and mechanism

1. The inventory is right, and its cause is one rule: "bypass, not delete" (D-008). Every lead marked legacy in stops 00 to 27 traces to it: a switchboard that describes one path with 34 switches (03a note 1.1); a registry whose `default_next` is the flag-off route (00 note 1.3, 05a note 1.2); a 440-line routing chain of which the live run takes six branches (05b note 1.2); nine templates copied per run with four to six unused (05b lead 2.2); 1,889 lines of role sheets no run loads; 17 marker comments `legacy routing (v26 card G)` (grep; the speech's 14 count the function-level ones); schemas for eight unwritten files; config sections for removed stages (03b). None of it changes what a run does today. All of it raises the cost of changing what a run does, because every branch has a flag-off test pinning the old shape, and the working rule "build only what a run asked for" makes that cost the binding one. For the goal, bypass-not-delete is not a correctness risk; it is a velocity tax on a loop that still needs changes (the significance gate of stop 19, the lineage rule of stop 06, the memory's "why" of stop 22a).
2. The guards hold where it counts: a run found at an unreached stage stops loudly before any spend (`verdict_interpreter :19972-19977`, `campaign_review :19911-19937`, `holdout_evaluation :19856-19910`, `analyst`/`regroup_record` flag-off refusals, stop 21a and 22a). So the risk the speech names, trusting a check that never fires, is bounded in code. It is not bounded in prose: the role sheets, the config comments, the register's `blocked_on` texts, the README's STATUS column and the summary's retired labels (stop 29) all describe the flag-off pipeline as current.
3. One unreached branch matters to the operator's own method: the fold re-run (`refold`, D-122) is refused while `variant_loop` is on (`RC:5680-5688`, `_refold_flag_refusal`), and `variant_loop` is on in the tour's flag set. Stops 06, 19, 23 and 24 all name "the operator's refold command" as the one way to re-test a strategy on another fold without a config change (D-201 makes decide-next refuse it). Under the live flags that command refuses before any spend. The operator has no confirmation tool that runs.
4. The three real choices in the switchboard are the off ones (03a note 1.2): the deviation pause (`:16884`), extra cards at 1a (`RC:4319-4334`), quarantine (`:4683-4769`). Each has a design argument: the deviation pause duplicates nearest-build's policy (stop 10 note 1.6); extra cards at 1a would fill the queue before decide-next ranks (stop 07 note 1.5); quarantine is the one that bears on running continuously (stop 23 note 2). The operator's rulings on these three are the only switch decisions left; the other 31 are history.
5. The archived stage list (`E-033/artifacts/...:1-25`) says its fate is "E-033 S2's decision (revive as the real registry or delete)", pending since 2026-08; the registry it would replace still carries `# required_outputs` as comments (`RP:186-189`). The decision not taken is itself a line in this inventory.
6. The Gemini worker and its vendor import (`RP:1576`, `:62-63`, stop 05a lead 2.1) are the one piece here that costs at import time on every run; everything else costs only at read time.

### (2) Legacy or simplifiable (leads)

The speech's reading map is the list; the pointers below add what earlier stops found about each row and are leads for the post-tour search, not facts.
1. Registry and prompt: `validation`, `backtest_specification` (AI), `verdict_interpreter`, `holdout_evaluation` entries (`RP:184-201`, `:216-220`, `:252-255`), `_SKILL_MAP` duplicate (05a lead 2.2), `_B7_MANDATORY_INPUT_PATHS` and `_CLOSED_BOOK_STAGE_INPUTS` entries for unreached stages (05a leads 2.4, 2.5), `_validation_protocol_args` flag-off pair (`:1730-1742`).
2. Routing: the 17 marked blocks (`:11739-16290`), `determine_post_specialist_readers_route`'s non-retired half (stop 23 lead 2.1), `_route_refine`/`_route_pivot`/`_route_escalate`/`_route_kill`/`_route_campaign_terminate`, `_apply_circuit_breaker`, `_resolve_verdict_fields`, `_dispatch_verdict_route`, `_write_promotion_audit`, `_ensure_regime_detector_report` (`:10143`), `_handle_hypothesis_generation_multi_card_split` (`:11616`), `_route_deviation_gate` (`:16884`), the loop-side list of stop 05b lead 2.4.
3. Launcher: refinement brief (`RC:4546-4591`, `:1037-1166`), legacy continuation (`:4792-4805`), split children (`:4294-4303`), extra cards hook (`:4319-4334`), quarantine (`:4683-4769`), decide-next-off outcome (`:4869-4871`), `refold`'s `variant_loop off` requirement (`:5680-5688`; note 3: fix or accept), wishlist status writer (`:1380-1455`), the dry run's legacy states (04 lead 2.7).
4. Config and register: the five settings sections (03b leads 2.1-2.5), the dead top keys (03a lead 2.1), the three profit-bars flags (20 lead 2.4), `variant_selection_record` (16 lead 2.4), the register's stale `blocked_on` texts (03b lead 2.6).
5. Files: five skills (1,889 lines), two empty templates, four unreached handoff templates, eight schemas (05a lead 2.6), `handoff.schema.json` (05b lead 2.1), `stages.yaml` archive, `tools/README.md` with two missing files, the `protocols/` pre-generated files no live entry names, `archive/` (six folders), `tools/recorder/`.

### (3) Disagreements between the speech and the element

1. Section 5, "14 code blocks carry the code's marker": grep finds 17 lines with `legacy routing (v26 card G)` (`RP:5676`, `:9890`, `:11739`, `:11764`, `:11783`, `:11842`, `:11904`, `:11991`, `:12018`, `:12027`, `:12975`, `:15818`, `:15866`, `:15886`, `:15997`, `:16115`, `:16290`); 14 are function headers, three are inline comments (`:5676`, `:9890`, `:12018`). The speech counts the headers. Consistent once said.
2. Section 6, "The tools README rates 20 of the 81 tracked entries of `tools/`; two of its 20 files are gone": `ls tools/` gives 82 entries (73 `.py`); the two missing files (`power_check.py`, `prescreen_signal.py`) verified absent; the 20-row count not re-verified (the README's table markup did not match my grep).
3. Section 6, "`quarantine/` (named only, never opened)": the folder is absent in this checkout (`ls`); `archive/` holds `briefs`, `drafts`, `improvements`, `incidents`, `protocols`, `reports`.
4. Step 7, "refuses the fold re-run ... while the variant loop is on": `:5680-5688`; verified, and the consequence (note 3) is not drawn.
5. Section 5 figures: "12 registered steps: 2 never reached, 1 run as code, 2 reached only by a trigger": verified against `:156-256` under the tour's flags. "5 role sheets ... 207, 230, 787, 117 and 548 lines": verified by `wc`. "Validation's two output templates are empty files": 0 bytes; verified. "28 schema files" (stop 05a) and "`protocols/` (15 fixed files)": verified.
6. Reading map verified: `RP:156-256` (entries at `:184-201`, `:216-220`, `:246-250`, `:252-255`), `:1019-1027`, `:20233-20234`, `:20189-20197`, `:3173-3184`, `:1730-1742`, `:9671-9680`, `:20257-20328`, `:20177-20179`, `:19972-19977`, `:20013-20050`, `:20555-20571`, `:16162-16172`, `:16290-16297`, `:20611`, `:7867`, `:19911-19936`, `:7515`, `:19856-19909`, `:20626`, `:1576`, `:9741-9747`, `:16884`, `:18919-18920`, `:11616`, `:11651-11652`; `RC:4546-4554`, `:4294-4303`, `:4319-4334`, `:4683-4769`, `:4869-4871`, `:5633-5650`, `:5680-5688`, `:5767-5774`; `campaign_config.yaml` sections (03b); the five skills; the two templates; the archived yaml `:1-12`; `tools/README.md:6-16`. Not opened: `:9749-9766`, `:19564`, `:9220`, `:9464`, `:11739-12060` bodies, `:12977`, `:15820`, `:15866`, `:15888`, `:15999`, `:16054`, `:13411`, `:16117`; `RC:4555-4591`, `:1037-1166`, `:4400-4404`, `:122`, `:268-292`, `:4625-4631`, `:2931`, `:4337`, `:4488`, `:4646-4647`, `:4463-4466`, `:1380-1455`, `:1458-1487`, `:505`, `:4134`; the two tests named.
