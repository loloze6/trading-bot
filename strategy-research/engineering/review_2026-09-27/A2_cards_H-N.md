# A2 vision check, part 2 of 2: roadmap v27 cards H–N (plus post-card sections)

Scope: master `e623531d`, read-only. The question is whether the code behaves as each card decided when the full flag set is ON: `config_direct_authoring`, `variant_loop`, `grid_evaluation`, `category_reports`, `specialist_readers`, `regroup_record`, `profit_bars_file`, `profit_bars_every_backtest`, `decide_next`, `verdict_routing_retired`, `composition_runs`, `variant_anti_adjacency_gate`. `data_availability_gate` is on by default. Flag readers were traced from `strategy-research/config/feature_flag_register.yaml`.

Paths are relative to `strategy-research/` unless stated. `rpr` = `workflow/run_phase1_research.py`, `rc` = `workflow/run_campaign.py`, `dn` = `tools/decide_next.py`.

Execution evidence: `python -m pytest tests/test_e059_6c_s2a_route_retirement.py` gave **69 passed** (retired routing is unreachable under the flag). No other test was run.

Binding later decisions used (these override a card where they differ):
- REALIGNMENT, `engineering/roadmap/E-046a/S1_FINDINGS_5B_II.md:682-714`
- 6b decisions 1–9, `engineering/roadmap/E-059/S1_FINDINGS_6B.md:576-604`
- 6c decision plus guesses 2–13, `engineering/roadmap/E-059/S1_FINDINGS_6C.md:494-508`
- `engineering/roadmap/E-059/S2A_QUESTIONS.md:50-56`
- E-058 decision, `engineering/roadmap/E-058/S1_FINDINGS.md:364-374`
- slice 8 decision, `engineering/roadmap/E-036/S1_FINDINGS_SLICE8.md:399-424`
- E-060 decision, `engineering/roadmap/E-060/S1_FINDINGS.md:405-431`

---

## 1. Per-card verdicts

### Card H: judge → learn → record → decide → park

| card.decision | quote | verdict | evidence | note | severity |
|---|---|---|---|---|---|
| H.1 | "Branches 1, 2 and 3 run in parallel on the same results." | **drift** (partial) | Grid (branch 1) uses every variant: `rpr:1665-1690`. Branch 3 uses every variant: `rpr:10457-10524`, called at `rpr:12592-12594`. Branch 2 (reports, then readers) uses the **base variant only**: `rpr:1602-1608` ("computed ONCE, from the base variant's summary only"); `build_reports.build_reports(RUN_DIR)` at `rpr:1711`; `tools/build_reports.py` contains the token "variant" 0 times. | The branches run in sequence (grid → reports → branch 3 → readers), which is fine. Readers never see the design or asset variants' results. The plan (`delivery_plan_v26.md:299-301`) specified the singular `protocol_result.yaml`. No operator decision narrows the card. | gap |
| H.2 | "Memory is written *before* the decision so the decision is reproducible from what is on disk." | faithful | `specialist_readers → regroup_record` at `rpr:12519-12523`. The route runs after the memory write at `rpr:12533-12563`. decide_next runs later, in `process_once`'s DONE branch (register entry `decide_next`). `decision_record.inputs` records memory/queue/known-classes sha256 and the registry revision (`dn:1715-1729`). | Proposal files and source configs are read but not hashed into the record. They are immutable run artifacts, so the effect is minor. | tidy (hash gap) |
| H.3 | Regroup writes "idea status and grid … block registry … trial rows … readers' proposals … near-miss scoreboard — then stop. It decides nothing." | faithful / faithful_by_later_decision | `_run_regroup_record_stage` at `rpr:6075-6156`: memory entry, `block_registry.record_run`, grid KB entry, scoreboard (`rpr:6171-6184`, never fails the stage). Trial rows are written in `protocol_execution`, per variant (`rpr:1485-1589`); regroup writes none, per E-058 §5 and decision 2026-09-23. Registration happens only with `block_manifest.yaml` (E-058 guess 1). A composition run never registers (`rpr:6145-6149`). | — | — |
| H.4 | "Branch 3 (profit bars) is a check that runs on every backtest, variant or composite alike" | faithful_by_later_decision | `_evaluate_profit_bars_every_backtest` at `rpr:10457-10524` grades every candidate from `_profit_bars_backtest_candidates`. Return and drawdown use the equal-weight portfolio (`config/profitability_bars.yaml:34-96`, operator decision 2026-09-24). Sharpe (median of coin medians) and trade count (worst coin) stay per coin (`profitability_bars.yaml:68-71, 97-101`). Composite variants are labelled composite (register `composition_runs`, S3b). | The "equal-weight portfolio" decision covers return and drawdown only; the file documents this. | — |
| H.5 | "when it passes, the loop **stops** and the operator regroups (card L)" | faithful | `_profit_bars_stop_route` at `rpr:10540-10576` runs after regroup_record (`rpr:12541-12542`). It pauses with `profit_bars_reached` and never touches idea_status. It does not re-pause on the same evaluation (`rpr:10565`). | The bars file is an unratified DRAFT (`profitability_bars.yaml:1-11, 128-129`). Ratification is manual by decision (6c S2d, register lines 457-459), so a stop can fire on placeholder numbers. That is by design and the operator must check. | — |
| H.6 | "The holdout unlock stays a manual act after that stop." | faithful_by_later_decision (6c decision) | The only paths are: (a) `_holdout_unlock_route` at `rpr:4949-4991`, which requires `_profit_stop_raised` and else ignores any `holdout_decision.yaml` (`rpr:4962-4967`); (b) the `holdout_evaluation` entry guard at `rpr:11880-11934`, which refuses without a spend unlock bound to this run's stop. Spend refusals: `ledgers_not_merged`, `holdout_already_consumed`, `seal_spend_pending`, DSR on the current ledger with the bars-file threshold (`rpr:4902-4921`, `rpr:4803`). The backtest itself is by hand: `_unlocked_holdout_evaluation` pauses with "Run the holdout backtest by hand" (`rpr:5092-5098`). The legacy promote → holdout route is guarded (`rpr:10986`). The retired-route test file passed 69/69. | Other code near the seal: `tools/composite_cache.py:199-240` refuses sealed paths and windows that overlap the holdout range, failing closed. | — |

### Card I: how the next idea is picked

| card.decision | quote | verdict | evidence | note | severity |
|---|---|---|---|---|---|
| I.1 | "Gates are yes/no and in code: novelty (repeat checker, card K)" | faithful_by_later_decision | Patch: exact-match key, REPEAT → ineligible (`dn:1387-1392, 1412`). new_block and card candidates: `NOT_APPLICABLE` until 1b (`dn:1404-1405, 1473-1476`). The 5a backstop is `_gate_config_direct_variants` (`rpr:11628-11630`). The legacy digest is advisory (`dn:1409-1410`; 6b decision 3; slice-8 decisions 1, 2, 4). | — | — |
| I.2 | "feasibility (data gate, component exists)" | faithful_by_later_decision | New component classes are checked against the known set (`dn:1374-1381`). Data uses a proxy, the source base variant `status: tested` (`dn:1346-1347`). new_block and cards return `UNKNOWN` and stay eligible, because "step 3's data gate stays binding" (`dn:1406-1408, 1477-1478`; 6b §4.2). Regime sketches are INFEASIBLE (`dn:1396-1398`). The `requires_feed` gate is at `dn:1384-1386`. | — | — |
| I.3 | "the mandatory 'registry changed → composition next' rule" | faithful_by_later_decision | `_r1` at `dn:1148-1190`, applied in `decide()` at `dn:1652-1665`. It waits behind in-progress and operator entries, runs ahead of every agent candidate, and fires only when an exact timeframe holds 2 or more uncomposed forecast blocks (E-060 guess 10 + decisions 3 and 6). | "Mandatory" is softened by operator priority, per the recorded decision. | — |
| I.4 | "LLM scores each candidate on anchored 0–3 rubrics defined in a skill file — … distance to a profitable strategy (3 = fills a missing block type with low correlation to the registry; 0 = neighbour of something already validated), and mechanism plausibility (who is on the other side of the trade, why it is not arbitraged away)" | **drift** | The reader rubrics define `distance_to_profitable` as "how close is the metric to a passing state" (`workflow_artifacts/skills/readers/profitability-reader/SKILL.md:172-177`; the same pattern holds in the four other reader SKILLs, e.g. `forecast_power-reader/SKILL.md:148`). They define `mechanism_plausibility` as cross-cell recurrence ("lone spike … curve fit"), not "who is on the other side". Readers may read only their own report plus `grid_evaluation.yaml` (`profitability-reader/SKILL.md:205-208`), so they **cannot see the registry**. `distance_to_profitable` is rank key #2 (`dn:1574-1580`). The brief-card rubric does match the card (`hypothesis-design/BRIEF_HYPOTHESES.md:60`; 6b note 2026-09-25). | No recorded decision changes the reader anchors. E-046a S1 listed the anchor text as "not defined anywhere" (`E-046a/S1_FINDINGS.md:500-501`), and the slice author wrote it. As built, the ranking favours near-miss tuning of one idea over blocks that fill registry gaps. | breaks_vision |
| I.5 | "Each score must cite its numbers; model id and rubric version are recorded." | drift (weakly enforced) | `reader_proposals._check_proposal` requires only a non-empty `evidence` list and non-empty `model_id`/`rubric_version` strings (`tools/reader_proposals.py:63-65, 93-96, 113-122`). Nothing ties a citation to each score. The reader `rubric_version` is not pinned to a constant, whereas the brief-card version is (`dn:687-689`). `model_id` is self-reported by the LLM; no orchestrator code stamps the model (`rpr` has no writer of `model_id` other than `rpr:5967-5970`, which copies it). | Provenance of scores is by trust. | tidy |
| I.6 | "Ranking is then code: confidence, then distance, ties to the cheapest." | faithful | `rank_key` at `dn:1574-1580`; cost = windows × 3 × symbols × 10.2 s (`dn:1411-1446`). Lineage demotion was dropped (6b decision 6). | — | — |
| I.7 | "Two readers proposing the same block collapse into one proposal with two sources." | faithful_by_later_decision (6b §3.6) | `_collapse` at `dn:1553-1571`: patches collapse on the full novelty key. Sketches collapse only on identical kind + config_paths **from the same source run** (`dn:1419-1421`). | The same sketch proposed after two different runs does not collapse. | tidy |
| I.8 | "These scores pick what to test next; they never touch promotion." | faithful | Scores exist only in `decision_record` (`dn:1433-1434`). Readers are refused routing fields (`reader_proposals.py:60-62`). The route comes from the grid (`rpr:12551-12554`). The retired-field check is at `dn:1739-1741`. | — | — |
| I.9 | "The operator can add a brief by hand at any time" | faithful_by_later_decision (6b decision 4) | Operator `ready` entries go first, unscored (`dn:1583-1586, 1666-1672`). | — | — |

### Card J: component gap, park don't stop

| card.decision | quote | verdict | evidence | note | severity |
|---|---|---|---|---|---|
| J.1 | "caught when the config is checked (Step 5a)" | faithful_by_later_decision | At 5a, a missing class surfaces as a V12 failure from `validate_config.py` (`rpr:2111-2127`). 1b can also declare `component_gap`, which parks (`rpr:11516-11530`; 6c guess 7 accepted). | That means an LLM self-report at 1b can park an idea with no class name attached, and `--unpark` then has no class to check. | tidy |
| J.2 | "The gapped variant is 'not tested' (not an attempt)" | faithful | Such a variant is marked `not_tested` in `index.yaml` (`rpr:2080-2127`) and has no trial row; only validated variants reach the loop (`rpr:1463, 1485`). | — | — |
| J.3 | "a component request is appended to one file the operator reads (surfaced in the campaign summary)" | faithful | `campaign_record/component_requests.yaml` via `_crr.append_component_requests` (`rpr:11519-11525`). Summary "Parked" table: `rc:2003-2016`. | — | — |
| J.4 | "the other variants still run; if fewer than three remain the idea is parked as 'waiting for component'" | faithful | `rpr:12309-12341`: fewer than `_min_needed` (3) validated → `_variant_park_kind` → `_park_run`. When nothing is validated, 5a itself parks (`rpr:11633-11647`). | Under the default of 3 variants, one gap parks the whole idea before any variant runs. That matches the literal "fewer than three". | — |
| J.5 | "becomes runnable again once the component exists. The loop stops only if nothing else is runnable." | faithful_by_later_decision (6c guess 8) | `--unpark` runs under the campaign lock (`rc:1778-1814`) and the same run resumes at its parking stage. Parked entries are never selected (`rc:1683-1687`). decide_next stops only with no ready/in-progress entry, no eligible candidate and no R2 (`dn:1706-1711`). | Unparking is manual, not automatic. | — |

### Card K: the config is the vocabulary

| card.decision | quote | verdict | evidence | note | severity |
|---|---|---|---|---|---|
| K.1 | "Step 1b writes the real bot config directly, under a design guide, plus a manifest … plus a prose rationale" | faithful | Stage `strategy_config_authoring`; `block_manifest.yaml` is required and checked (`rpr:2023-2033`); `config_rationale` is in the SKILL (`strategy-config-authoring/SKILL.md:53, 78`). | — | — |
| K.2 | "A variant (E-057) is a named patch on that config — one field changed." (with card D: "one asset variation on a coin from a different category") | **drift / not_built** | Patches are a list of `{path, value}` with no one-field check and no cap-4 check (`rpr:2043-2139`). **The config has no symbol field**: "§7a … PROPOSED, NOT BUILT … no symbol, timeframe, or instrument-set key anywhere" (`docs/STRATEGY_DESIGN_GUIDE.md:396-417`). Every variant runs on the same run-level protocol (`rpr:1478, 1515-1518`), whose `symbols` are the coins run (`tools/run_protocol.py:1968`). The Step 2 skill tells the LLM to write the asset variant as "a patch changing whatever config path encodes the traded symbol" (`innovation-expansion/SKILL.md:268-271`), yet its own example "asset" patch edits `/regime_detector/components/0/params/period` (`SKILL.md:251-256`). | **As built, the asset variant cannot change the coin.** All three variants trade the same symbols, and grid unanimity then claims setup-independence across coins that was never tested. No decision records this gap for the variant set. The ledger records only the absent field (`research/ledger/win.md:841`). | **breaks_vision** |
| K.3 | "Step 5a needs no LLM: validator, component-class check, manifest check, three patched configs assembled" | faithful | Tool stage under config_direct: `rpr:1965-2139`; routing: `rpr:12205-12215`. | — | — |
| K.4 | "A repeat (Step 4) is an exact match on the config hash plus instrument, timeframe and window set" | faithful_by_later_decision (slice-8 decision 2 + correction) | `tools/novelty.py` key = (forecast_hash, sorted symbols, protocol timeframe, windows sha), looked up in `campaign_memory.yaml` (`rpr:6575-6634`). Legacy runs are absent from memory and never match. | Variants dropped as repeats shrink the grid's column set (`rpr:12318-12319`). Whether their earlier results are attached to the grid was not verified. | gap (inference) |
| K.5 | "anything else is a neighbour, attached as information, never refused" | faithful_by_later_decision (slice-8 decision 1: NEIGHBOUR dropped) | `layer2_digest_check` returns only REPEAT/NOVEL (`tools/anti_adjacency_gate.py:386-396`). Layer 1 only warns (`anti_adjacency_gate.py:425`). | — | — |

### Card L: operator cases and the runbook

| card.decision | quote | verdict | evidence | note | severity |
|---|---|---|---|---|---|
| L.1 | "Every case where a human must act gets a runbook row: what to read, what to decide, which artifact to update, which command resumes" | faithful | `docs/RUNBOOK.md` §3 rows: `profit_bars_reached` (L410), `holdout_unlock_refused` ×11 codes (L437-447), `holdout_refused_under_retired_routing` (L431), `campaign_review_terminate` (L449), `paused:waiting_for_component/data` (L453), `queue_exhausted_with_open_briefs` (L454), `decide_next stop: no_eligible_candidate` (L425), `composition_failed` (L455), `legacy_continuation_under_retired_routing` (L430); `--unpark` (L600). | Completeness of each row's four elements was spot-checked only. | — |
| L.2 | "profit bars reached (review the composite; decide whether to spend …; run it by hand; record the outcome in the holdout result and the data-policy file; resume into Step 10 or promote)" | faithful_by_later_decision (6c S2d; CUL-331) | spend/continue: `rpr:4949-4991`. The by-hand pause is at `rpr:5092-5098`. The consume marker is written by code once `holdout_result.yaml` exists (`rpr:5103-5110`). continue → `completed_<idea_status>` → decide-next (`rpr:4981-4985`). | — | — |
| L.3 | "Idea parked, loop continues: component missing; data missing …; an idea inconclusive twice for data reasons" | faithful_by_later_decision (6c guess 2) | Parking: `rpr:12320-12341, 11516-11530, 11633-11647`. "Inconclusive twice" is deferred, because nothing re-runs an idea automatically. | — | — |
| L.4 | "campaign review says stop" is a loop stop | faithful_by_later_decision (6c guess 5) | terminate → `campaign_review_terminate` pause (`rpr:5149-5152`, `rpr:12565-12573`). | — | — |
| L.5 | "Restart after any stop is the existing resume command: it clears the stop flag and re-enters Step 10." | faithful | After the stop, `holdout_decision.yaml: continue` → run ends `completed_<idea_status>` → decide-next. `--resume` refuses first on an invalid decision (`rpr:5113-5126`). | — | — |
| L.6 | "the two new 'parked' queue states" | faithful | `rc:124-125` (`paused:waiting_for_{component,data}`). | — | — |

### Card M: briefs with several hypotheses

| card.decision | quote | verdict | evidence | note | severity |
|---|---|---|---|---|---|
| M.1 | "one runs now, the others go to the queue with the brief as their source" | faithful (minor drift) | Cards 2..k are copied to `campaign_record/queued_cards/<run>/` and recorded in `queued_hypotheses.yaml` with scores (`rpr:5936-5962`). They are enqueued `queued` with `card_ref` and `origin: brief` (register `decide_next` S2b). | The card that runs now is simply `new_cards[0]` (`rpr:5936`), not ranked against its siblings' scores. | tidy |
| M.2 | "the brief stays open until 1a says it is exhausted" | faithful + code guard | `brief_status.yaml` exhausted → `completed_brief_exhausted` (register S2b). There is also a code cap, `BRIEF_MAX_CONSECUTIVE_EMPTY_R2 = 2` (`dn:163, 1499-1503`). | The cap came from a code-review fix; no operator decision for it was found. It is reasonable as a spend guard. | tidy |
| M.3 | "Before declaring the queue empty, Step 10 re-reads open briefs and asks 1a for more." | faithful | `_r2` at `dn:1491-1545`, fired at `dn:1690-1705`. Legacy briefs never trigger it (6b decision 7). | — | — |
| M.4 | extra cards "scored like everything else" | faithful_by_later_decision (6b decision 4) | 1a scores each extra card under `brief-card-v1` (`dn:674-691`). Ranked with the proposals at `dn:1631-1641`. | — | — |

### Card N: one entry point

| card.decision | quote | verdict | evidence | note | severity |
|---|---|---|---|---|---|
| N.1 | "Every candidate enters at Step 1a, whatever its source." | faithful_by_later_decision | Reader candidates enter at 1a (6b decision 2; `dn:1756-1845`). Brief extra cards skip 1a (6b decision 9). An unparked run resumes at its parking stage (6c guess 8). A composition run's 1a/1b/2 are code (`rpr:3809-3857`, E-060 S3b). | — | — |
| N.2 | "A candidate that already carries a config and criteria passes through with a completeness check only." | faithful_by_later_decision | Criteria are **not** carried: 1a writes them from the menu (6b decision 2; `rpr:5700-5717`; S2A_QUESTIONS option (c)). The config passes through 1b by prompt and is hash-checked at 5a (`rpr:5744-5784`, called at `rpr:2036, 2138`). | 1b is still an LLM call that re-emits the config; only the hash guarantees it is unchanged. That costs spend but causes no drift. | tidy |
| N.3 | "The former validation stage between Step 2 and Step 5 is deleted" | faithful_by_later_decision (6c guess 10: unreached, code kept) | `rpr:12205-12206`: `validation` → `backtest_specification` under config_direct. | — | — |

### Post-card sections (walkthrough and notes)

| section | quote | verdict | evidence | note | severity |
|---|---|---|---|---|---|
| Step 0 / 10 | "No source creates a run directly any more … every one of them goes through the same queue and the same decide-next step" | faithful_by_later_decision (6c guess 6) | A campaign-review reframe is registered `ready` (priority 999, origin `campaign_review`) **before** decide-next (`rpr:5144-5148`; `rc:3489-3523`). `decide()` then picks it as `scheduled`, unscored and ungated (`dn:1666-1672`). | An LLM-originated brief skips card I's scores and the novelty gate and goes ahead of every reader candidate. That is accepted, but it is the one place an LLM chooses the next run. | gap (note) |
| Step 10 | "Three different things decide … refine/pivot/escalate … campaign review … queue" → "Verdict routing is retired." | faithful | `_dispatch_verdict_route` raises under the flag. Continuation children halt (register `verdict_routing_retired`; `rpr:10986`). The test passed 69/69. Campaign-review `continue`/`escalate_*` is recorded only (`rpr:5142-5143`). | Residual text: the campaign summary still prints "Distinct failed hypothesis families" (`rc:1975-1976, 2026`) and a run total from `campaign_state.runs`, which is incomplete under the flags. | tidy |
| Step 11 | "a candidate is re-scored when memory changes" | faithful_by_later_decision (6b guess 4: "left for later") | Scores are read as written; there is no re-score. | — | — |
| Step 12 | "It reads the profit-bars file instead of per-protocol thresholds" | faithful (unlock) / tidy (stale comment) | The unlock DSR check uses `bars["deflated_sharpe_threshold"]` (`rpr:4803`). `config/profitability_bars.yaml:22-28` still says the holdout gate reads the hardcoded 0.95. The per-protocol `promotion` blocks still exist (6c guess 11, separate ticket). | — | tidy |
| Note "Regime ideas" | "a regime idea is a composition run with two versions: ungated / gated" | not_built; superseded in part by E-060 decision 4 | `dn:1396-1398` (`regime_block_needs_composition`). E-060 decision 4: regime blocks are validated on identification quality, and gated-vs-ungated is only a composition question, a "later sub-step behind its own flag". | The A2.3 "no regime-gated hypotheses" rule therefore still stands in practice. | — |
| Note "Composition runs" | "counts its own attempts" | faithful (variants), with a caveat | Composition variants run through the same per-variant trial loop (`rpr:1485-1589`). The residual-IC composite **re-runs the composite config as a full `run_protocol` backtest on the candidate's coins and windows** and records no trial row (`tools/composite_cache.py:35-58, 333-365`, "not a trial, not graded"). This is E-060 guess 5, a safe-to-build default not objected to in the 2026-09-26 decision. | Any reader of `campaign_record/composite/*/protocol_summary.json` (PnL included) is looking at an uncounted result. Nothing in the loop reads it for decisions; checked by grep of the cache path's consumers in `tools/composite_cache.py` only (inference). | gap |

---

## 2. Top findings (most severe first)

1. **The asset variant cannot change the coin, so card D's "asset variation on a coin from a different category" is never tested.**
   - Evidence: `docs/STRATEGY_DESIGN_GUIDE.md:396-417` (§7a "PROPOSED, NOT BUILT", no symbol field in the config). Every variant uses one `protocol_path` (`rpr:1478, 1515-1518`), whose symbols come from `tools/run_protocol.py:1968`. The skill's own "asset" example patches a detector period (`workflow_artifacts/skills/innovation-expansion/SKILL.md:251-256`).
   - Consequence: "validated on every variant" can mean three near-identical setups on the same coins. Grid unanimity overstates robustness, and ideas may enter the block registry as coin-general without ever running on another coin.

2. **The reader score rubrics do not implement card I's "distance to a profitable strategy" or "mechanism plausibility" anchors, and readers cannot see the registry.**
   - Evidence: `readers/profitability-reader/SKILL.md:172-177, 205-208` (same pattern in the other four readers); rank key at `dn:1574-1580`. The card's text is in the roadmap's card I.
   - Consequence: decide-next ranks "close to passing" refinements of the last idea above blocks that fill registry gaps. That tilts the loop toward tuning one lineage instead of accumulating diverse blocks.

3. **Reader patches are re-tested on the same walk-forward windows that motivated them, and 1a picks their criteria after seeing that evidence** (inference: a same-sample refinement risk, not strict lookahead).
   - Evidence: `dn:1775-1794` (the source `machine_constraints` window pin is copied, and the evidence text goes into the 1a goal).
   - Consequence: a patched idea is graded in-sample. Only trial counting (DSR) and the single-use holdout guard against a curve-fit reaching the profit-bars stop.

4. **Branch 2 reads only the base variant.**
   - Evidence: `rpr:1602-1608, 1703-1711`; `tools/build_reports.py` has no variant handling.
   - Consequence: the readers never see that an idea failed on its design variant, so proposals ignore the evidence the grid used to refute it.

5. **Card D/K variant shape is unenforced: no cap of four, no "one field changed".**
   - Evidence: `rpr:2043-2139`; `innovation-expansion/SKILL.md:267-274` ("more are permitted").
   - Consequence: the Step 2 LLM can emit many multi-field variants. Each is honestly counted as a trial, which inflates N, and "variant" no longer isolates one change.

6. **The residual-IC composite is a real backtest with no trial row** (decided default E-060 guess 5).
   - Evidence: `tools/composite_cache.py:35-58, 333-365`.
   - Consequence: PnL-bearing summaries for new (config, coin, window) combinations accumulate under `campaign_record/composite/` outside the trial ledger. That is harmless while nobody reads them for decisions.

7. **A campaign-review reframe (LLM output) jumps the queue, unscored and ungated** (decided, 6c guess 6).
   - Evidence: `rpr:5144-5148`; `rc:3489-3523`; `dn:1666-1672`.
   - Consequence: this is the one remaining path where an LLM, not decide_next's gates and scores, chooses the next run. The 5a exact-match gate is the only repeat backstop.

8. **Score provenance is trust-based.**
   - Evidence: `tools/reader_proposals.py:63-65, 93-96`.
   - Consequence: `model_id` is self-reported, the reader `rubric_version` is any string, and there is no per-score citation. An audit cannot prove which model or rubric produced a ranking.

9. **Branch 3 can stop the loop on unratified placeholder bars** (by decision: ratification is manual).
   - Evidence: `config/profitability_bars.yaml:1-11, 128-129`.
   - Consequence: the first `profit_bars_reached` stop after switch-on may reflect invented thresholds. The operator must ratify before trusting any stop.

10. **Stale text.**
    - Evidence: the campaign summary still reports the retired "failed hypothesis families" (`rc:1975-1976, 2026`); the bars-file comment says the holdout gate uses the hardcoded DSR 0.95 while the unlock reads the file (`profitability_bars.yaml:22-28` vs `rpr:4803`).
    - Consequence: operators reading the summary or the bars file get a wrong picture of what gates what.

Verified clean (no finding):
- The holdout is reachable only through the branch-3 stop plus the operator's `holdout_decision.yaml` (`rpr:4949-4991, 11880-11934`).
- Status comes only from the grid.
- Refine/pivot/escalate/kill, the circuit breaker, `hypothesis_family` and continuation children are unreachable under `verdict_routing_retired` (69/69 tests).
- Every tested variant writes a trial row, including failures (`rpr:1485-1589`).
- Composition weights and residual IC are past-only (`tools/composition.py:442-476`; `tools/composite_cache.py:60-63`).

---

## 3. Could not verify

- Every loop behaviour under the full flag set with a real LLM and real data. No run on disk has passed through `regroup_record`/`decide_next` (register `blocked_on` entries), so all verdicts rest on code reading plus one targeted unit-test file. That makes them `untestable_without_run` in the strict sense.
- Whether a variant skipped as an exact REPEAT has its earlier result attached to the grid, or the grid simply runs with fewer columns (`rpr:12318-12319`). This matters for unanimity (card C, part 1's scope).
- Whether any consumer outside `tools/composite_cache.py` reads `campaign_record/composite/**/protocol_summary.json` (only spot-grepped).
- Whether the `model_id` a reader writes matches the model the worker actually invoked.
- The completeness of every RUNBOOK row's four required elements (what to read, what to decide, artifact to update, resume command). Row existence was checked; content was spot-checked only.
- Whether `_select_entry`'s priority order can let an operator entry registered with a priority number above 999 run after a campaign-review reframe (priority 999). Not traced.
- E-035 automated external dispatch: confirmed parked by decision (slice-8 decision 5). Only the `requires_feed` lane exists (`dn:1384-1386, 1786-1790`). No dispatch code was searched beyond that.
