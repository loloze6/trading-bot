# Strategy-Research Pipeline — Enhancement Plan v2 (Overview)

> **SUPERSEDED** — This document has been replaced by `00_closing_state.md` as the canonical entry point. All improvements (01–09) are complete. Read `00_closing_state.md` first; treat this file as historical reference only. Where this document conflicts with `AMENDMENTS_01-06.md`, the amendments win.

## Purpose of this plan

This supersedes the original `00_overview.md`. It integrates the six original improvements (`01`–`06`), three new improvements (`07`–`09`), and the targeted corrections in `AMENDMENTS_01-06.md`. Read this file first; then read each numbered file **together with its amendments section** — an implementation agent working on `01` must apply A1.1–A1.3, on `02` apply A2.1, and so on. Plans `07`–`09` are self-contained.

## Diagnosis (revised)

The original diagnosis stands: the pipeline is an effective **rejection engine** and a weak **discovery engine** — search loops instead of converging, verdicts lack causal explanations, knowledge does not accumulate. Two additional problems, invisible from inside the pipeline, change the priority order:

1. **Measurement integrity is compromised before generation is improved.** 36+ runs have adapted to the same 11 monthly windows of 2024 BTC/ETH data. Those windows are burnt at the campaign level: nothing evaluated on them — including the one "confirmed" edge — carries an unbiased performance estimate. Improving generative power while measuring against burnt data converges *faster on false positives*. Therefore the cheapest slice of defensive rigor (data reservation) moves from last to **first**.
2. **The dominant kill causes are discoverable pre-backtest.** `weak_signal` and `cost_drag` — the two most frequent verdicts — are detectable from a vectorized signal computation and cost arithmetic at ~1% of a full walk-forward's compute. Generative power is not only "generate better hypotheses"; it is equally "spend the backtest budget only on hypotheses that could possibly survive it."

## Implementation order

Each step lists its file(s), its dependency rationale, and rough effort. Steps 1–2 are a milestone gate: **no new research run is launched until step 1 is done.**

| # | Improvement | Files | Depends on | Why this position | Effort |
|---|---|---|---|---|---|
| 1 | **Data extension & holdout retrofit** | `07` | — | Cost of delay compounds per run: every run burns more potential holdout data. Freezes 2026-H1, extends walk-forward to 24 windows (baseline_v2), adds the overlap guard pulled forward from `06`. Includes the Keltner re-run on unseen windows — the single most informative experiment currently available. | ~1 day |
| 2 | **Regime detector validation** | `02` + A2.1 | — | Everything downstream that reads `per_regime_metrics` (01, 03, 05) inherits detector trust. A2.1 adds the ungated-evaluation escape so low detector confidence can never deadlock the campaign. | small–medium |
| 3 | **Trade-level diagnostics** | `03` + A3.1–3 | — | Deterministic metrics-engineering on `run_protocol.py`; feeds 01's causal taxonomy and 05's knowledge base. A3.1 (post-exit tracking) and A3.2 (per-trade cost) are required for the plan's own decision rules to be computable. | medium |
| 4 | **Signal prescreen** | `08` | 2 (for regime-conditional IC), engine's signal/reconciliation separation (exists) | Cheap kill path for `weak_signal`-class hypotheses before backtest; provides the detector-independent evidence A2.1 relies on; produces the turnover proxy step 5 consumes. From this point on, backtest volume drops and per-backtest information rises. | medium |
| 5 | **Cost hurdle gate** | `09` | 4 (Layer 2 uses prescreen turnover/IC) | Converts the campaign's #1 empirical killer from a post-backtest surprise into an upstream design constraint; unifies fee assumptions in one `cost_model.yaml`. Layer 1 (validation-gate arithmetic) can land with step 2 if convenient; Layer 2 needs step 4. | small |
| 6 | **Edge-source taxonomy & causal root-cause** | `01` + A1.1–3 | 2, 3 (verdict side reads their evidence) | Generation must declare a mechanism; verdicts must check against it. A1.1 adds `persistent_behavioral_bias` so honest categorization is possible; A1.2 constrains evidence types to backtestable feeds (funding, F&G) and routes the rest to `feed_wishlist.yaml`; A1.3 requires every mechanism to name a measurable proxy. | medium |
| 7 | **Campaign knowledge base** | `05` + A5.1–3 | 1 (protocol_version tag), 2, 3, 6 (structured facts to store) | Aggregation layer over 01–03's structured outputs. A5.1's evidence thresholds are non-optional: without them, at current sample sizes the KB amplifies flukes instead of accumulating knowledge. | medium |
| 8 | **Indicator library** | `04` | 6 (edge_source_compatibility), 7 (empirical write-back) | Lowest priority as originally suspected: the "book indicator" convergence is primarily a data-scope symptom, addressed at the root by A1.2's feed constraint and wishlist. Still worthwhile as a cheap prior for generation once 6–7 exist. | small |
| 9 | **Promotion rigor (remainder)** | `06` + A6.1–3 | 1 (holdout range exists), trial-count plumbing from 4 (prescreen kills are trials) | Deflated Sharpe (with A6.2's cross-trial variance storage and A6.3's refinement-as-trial counting), `promotion_audit.yaml`, and the single-use `holdout_evaluation` stage. Must be complete **before any strategy is sent toward live deployment** — it is the last gate, implemented last, but it is not optional. | medium |

### Milestones

- **M0 (step 1):** measurement integrity restored. Gate: `check_data.py` rejects holdout overlap; baseline_v2 runs end-to-end; Keltner unseen-window result recorded.
- **M1 (steps 2–5):** diagnostic trust + cheap filtering. Gate: regression tests in `02`/`08`/`09` pass against historical runs (false-kill retrocase for 02; ≥3 historical `weak_signal` runs caught by prescreen; ≥2 historical `cost_drag` runs blocked upstream).
- **M2 (steps 6–8):** causal generation + accumulating memory. Gate: `01`/`05` acceptance criteria, including the retrospective check that the KB surfaces an exhausted mechanism the linear carryover chain missed.
- **M3 (step 9):** promotion gate hardened. Gate: `06` acceptance criteria incl. synthetic deflation test and single-use holdout enforcement. Only after M3 may a promoted strategy proceed toward deployment.

## Shared vocabulary (additions to the original)

- **Burnt data**: date ranges that any historical run's verdict has been computed on and fed back into search. Burnt data remains usable for walk-forward *search* but can never yield an unbiased performance estimate. Tracked in `config/campaign_data_policy.yaml`.
- **Prescreen**: deterministic, vectorized evaluation of a strategy config's raw forecast (IC, significance via block bootstrap, turnover proxy) with no portfolio layer. A filter with route-only output — never a fitness function for ranking variants. Prescreen kills count as trials.
- **Trial**: any comparison made against the walk-forward data — full runs, expansion variants, refinement iterations, and prescreen kills all count. The denominator of the deflated Sharpe correction.
- **Cost hurdle**: the requirement that estimated gross edge per trade ≥ 2× round-trip cost (from `config/cost_model.yaml`), enforced coarsely at validation and precisely at prescreen.
- **Evidence count**: number of independent runs supporting a knowledge-base finding. Findings below threshold are priors/hints; only threshold-passing `exhausted_mechanisms` entries hard-constrain generation.
- (Original definitions of mechanism/edge-source, regime attribution, trade-level diagnostics, and KB-vs-carryover are unchanged.)

## Artifacts touched (consolidated)

| Artifact | Existing? | Touched by |
|---|---|---|
| `hypothesis_card.yaml` | yes | 01 (A1.1–3) |
| `validation_protocol.yaml` | yes | 01, 09 (cost_feasibility block) |
| `protocol_result.yaml` / `protocol_summary.json` | yes | 02, 03 |
| `verdict_interpretation.yaml` | yes | 01, 02, 03 |
| `findings_carryover.yaml` | yes | 05, 07 (evidence_window tagging) |
| `campaign_state.yaml` | yes | 05, 06 (A6.2: `trial_sharpes`), 07 |
| `config/campaign_data_policy.yaml` | **new** | 07 |
| `config/cost_model.yaml` | **new** | 09 (consumed by 03, validation gate, backtest engine, cost_drag rule) |
| `config/available_feeds.yaml` | **new** | 01 (A1.2) |
| `feed_wishlist.yaml` | **new** | 01 (A1.2) |
| `regime_detector_report.yaml` / `regime_audit_decision.yaml` | **new** | 02 |
| `trade_diagnostics.json` | **new** | 03 (A3.1–2 fields included) |
| `prescreen_result.yaml` | **new** | 08, 09 (cost_check block) |
| `indicator_library.yaml` | **new** | 04 |
| `campaign_knowledge_base.yaml` | **new** | 05 (A5.1–3), 02, 07 |
| `promotion_audit.yaml` / `holdout_result.yaml` | **new** | 06 (A6.2) |

## Skills touched (consolidated)

| Skill | Touched by |
|---|---|
| `hypothesis-design` | 01 (A1.1–3), 04, 05 (A5.1 prior-vs-constraint rule) |
| `innovation-expansion` | 01 (A1.2 note on funding feed), 04 |
| `quant-validation` | 06, 09 (Layer 1 hard rule) |
| `verdict-interpreter` | 01, 02 (A2.1), 03 (A3.3 note), 08 (prescreen-evidence verdicts), 09 (estimate-vs-realized gap) |
| `campaign-review` | 05, 07 (Part C re-open rule) |
| **new: `regime-auditor`** | 02 |

## Tools/orchestrator touched (consolidated)

| Component | Touched by |
|---|---|
| `tools/run_protocol.py` | 02, 03 |
| `tools/check_data.py` | 07 (holdout overlap guard) |
| **new: `tools/validate_regime_detector.py`** | 02 |
| **new: `tools/prescreen_signal.py`** | 08, 09 |
| **new: `tools/deflate_sharpe.py`** (or in run_protocol) | 06 |
| `workflow/run_phase1_research.py` | 01 (mechanism routing), 02, 05, 06, 07, 08 (prescreen routing + trial counting), 09 |
| `workflow/stages.yaml` | 02, 06, 08 (new stages registered) |
| `protocols/baseline_v2.json` | **new** — 07 |

## Cross-cutting rules (apply to every step)

1. **Trial accounting is universal.** Any code path that evaluates anything against walk-forward data (backtest, prescreen, refinement iteration) must increment the campaign trial record (`campaign_state.trial_sharpes` per A6.2) at the moment it runs — not retrofitted at step 9. Steps 4 and onward must include this hook even though the deflation consumer lands last.
2. **Holdout is untouchable.** From M0 onward, no stage, tool, prescreen, or diagnostic may read candles inside `holdout_range` except the (future) `holdout_evaluation` stage. Enforced in the data loader, not by convention.
3. **One cost model.** No fee/spread constant may be hardcoded anywhere after step 5; `config/cost_model.yaml` is the single source (grep audit in 09's acceptance criteria).
4. **Findings carry their protocol version.** Every knowledge-base or carryover entry written from M0 onward records `protocol_version` (baseline_v1 vs v2); 2024-only conclusions are not exchangeable with v2 conclusions.
5. **Regression tests against campaign history are the acceptance style.** Where a plan claims it would have prevented a past mistake (02's false kill, 08's weak_signal spend, 09's cost_drag kills), the acceptance criterion is a retro-run against the actual historical artifacts, not a synthetic-only test.

## Non-goals (unchanged from v1, plus one)

- Live/paper-trading incubation between promote and deployment.
- Cross-strategy portfolio correlation checks.
- Execution realism (slippage calibration against real fills).
- **New feed integrations** (order book, liquidation, cross-exchange): out of scope here; `feed_wishlist.yaml` (A1.2) accumulates the prioritized case for a future feed-integration plan on the trading-bot side. Building the single highest-demand feed is likely the next plan after M2.

## How to use the per-improvement files

Implementation order: `07 → 02 → 03 → 08 → 09 → 01 → 05 → 04 → 06`. Each file is self-contained (gap, schema changes, skill changes, orchestrator changes, acceptance criteria); files `01`–`06` must be read with their `AMENDMENTS_01-06.md` section applied — amendments override the original text where they conflict. `02`+`03` must land before `01` is finalized (unchanged from v1); `08` must land before `09`'s Layer 2; nothing may skip ahead of `07`.
