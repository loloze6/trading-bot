# Strategy-Research Workflow — User Guide

---

## Table of Contents

1. [What This System Does](#1-what-this-system-does)
2. [Workflow Overview](#2-workflow-overview)
   - 2.1 [Stage Map](#21-stage-map)
   - 2.2 [Stage Objectives](#22-stage-objectives)
   - 2.3 [Decision Tree & Routing](#23-decision-tree--routing)
3. [Artifacts](#3-artifacts)
4. [Skills](#4-skills)
5. [Tools & Scripts](#5-tools--scripts)
6. [Glossary](#6-glossary)

---

## 1. What This System Does

This is an **automated strategy research factory**. Its goal is to take a high-level research question ("can volume-confirmed momentum work on BTC?") and systematically generate, validate, backtest, interpret, and decide on trading strategy hypotheses — with minimal human intervention.

The system follows a strict **falsification-first** philosophy: a hypothesis must be formally pressure-tested for failure modes *before* any code is run. This prevents wasting compute on structurally broken ideas.

It is built around three principles:

- **Structured artifacts over prose** — every stage communicates via validated YAML files, not free text.
- **Automated routing** — the pipeline decides its own next step based on rules, not human judgment.
- **Campaign memory** — across many runs, the system tracks what has been tried and detects dead ends automatically.

---

## 2. Workflow Overview

### 2.1 Stage Map

```
[Human]  research_brief
            │
            ▼
[Claude] hypothesis_generation
            │
            ▼
[Claude] innovation_expansion
            │
            ▼
[Claude] validation_gate ──────────────────────────────────┐
            │ approve                                        │ refine (≤2x)
            │                         ┌──────────────────────▼──────────┐
            │                         │     refinement_planner           │
            │                         │       ↓                          │
            │                         │   [back to innovation_expansion] │
            │                         └──────────────────────────────────┘
            ▼
[Claude] backtest_specification
            │ spec_ready
            ▼
[Tool]   protocol_execution  (walk-forward backtest)
            │
            ▼
[Claude] verdict_interpreter
            │
     ┌──────┼──────────────────────────────┐
     │      │                              │
   refine  pivot                       escalate
   (alt 1) (alt 2)                     (alt 3)
     │      │                              │
     └──────┴──────────────────────────────┘
            │
     [new run spawned]
            │
     (after 2+ family failures)
            ▼
[Claude] campaign_review
            │
     ┌──────┼──────────────────┐
     │      │                  │
  continue reframe          terminate
     │      │                  │
     │  [new run]          [kill]
     │
     ▼
[terminal] promote  ──►  research_decision (archive)
           kill     ──►  research_decision (archive)
```

---

### 2.2 Stage Objectives

| # | Stage | Engine | Objective |
|---|---|---|---|
| 1 | **research_brief** | Human | Define the research question, target market, constraints, and existing context. Entry point for every run. |
| 2 | **hypothesis_generation** | Claude | Translate the brief into a single, concrete, testable hypothesis with an explicit signal formula and assumptions. |
| 3 | **innovation_expansion** | Claude | Expand the single hypothesis into 3–6 testable variants covering alternative data sources, reversed logic, behavioral angles, and regime-specific versions. |
| 4 | **validation_gate** | Claude | Stress-test the hypothesis: write falsifiable statements, identify failure modes, specify bias risks, define success/failure decision rules. |
| 5 | **refinement_planner** | Claude | If validation returns `refine`, convert each blocking issue into a concrete implementation fix and decide whether the hypothesis is ready for another round or needs human review. |
| 6 | **backtest_specification** | Claude | Translate the validated hypothesis into a `strategy_config` JSON that plugs directly into the trading-bot backtest engine. |
| 7 | **protocol_execution** | Python tool | Run the strategy config across all walk-forward windows (22 combinations: 11 months × 2 symbols) and produce per-window metrics. |
| 8 | **verdict_interpreter** | Claude | Read backtest diagnostics, apply 5 named diagnostic rules, and issue an altitude decision: refine / pivot / escalate / promote / kill. |
| 9 | **campaign_review** | Claude | After 2+ hypothesis families have failed, step back and assess whether to continue the search, reframe the research question, escalate to a new instrument, or terminate the campaign. |
| 10 | **research_decision** | Claude | Archive the final campaign outcome (promoted strategy config or kill rationale) into a permanent decision artifact. |

---

### 2.3 Decision Tree & Routing

#### After validation_gate

| Validation status | Next stage |
|---|---|
| `approve` or `conditional_approve` | → backtest_specification |
| `refine` (refinement counter < max) | → refinement_planner → innovation_expansion |
| `refine` (counter exhausted) | → `completed_rejected` |
| `reject` | → `completed_rejected` |

#### After refinement_planner

| `implementation_allowed` | Next stage |
|---|---|
| `true` | → innovation_expansion (refinement loop) |
| `false` | → human pause (pipeline suspended, awaiting audit) |

#### After backtest_specification

| Config status | Next stage |
|---|---|
| `spec_ready` | → protocol_execution |
| `component_gap` | → human pause (a new bot component must be built) |

#### After verdict_interpreter — the Altitude System

The verdict interpreter assigns an **altitude** to each decision. Altitude measures how far from the original hypothesis the next step will move.

| Verdict | Altitude | Meaning | What changes next run |
|---|---|---|---|
| `refine` | 1 | Minor tweak | Same hypothesis family, same signal, adjust a parameter (threshold, lookback window) |
| `pivot` | 2 | New idea | New hypothesis family, same research question |
| `escalate` | 3 | New environment | Same methodology, different instrument or timeframe |
| `promote` | — | Terminal success | Strategy passes all gates; archived and handed to live deployment pipeline |
| `kill` | — | Terminal failure | Strategy is dead; root cause archived in campaign memory |

#### Circuit Breakers (anti-loop protection)

The orchestrator detects search-space exhaustion and forces an altitude climb automatically:

| Trigger | Action |
|---|---|
| Same hypothesis family pivoted 2× with identical root cause | Force escalate (altitude 3) |
| Same instrument/timeframe escalated 2× with no improvement | Force terminate or campaign_review |
| Refinement budget exhausted (`max_refinements_after_validation`, default 2) | Reject hypothesis |
| Run token budget exceeded (default 300,000 tokens) | Halt run, preserve state |

#### After campaign_review

| Campaign decision | Next action |
|---|---|
| `continue` | Apply the verdict interpreter's original decision |
| `reframe` | Write a new research_brief with a different angle; spawn next run |
| `escalate_instrument` | Target a new symbol/timeframe; spawn next run |
| `escalate_component` | Identify missing bot component; human pause |
| `terminate` | Kill entire campaign; write research_decision |

---

## 3. Artifacts

Artifacts are YAML files produced and consumed by pipeline stages. They are the only communication channel between stages — no stage reads another stage's raw LLM output. All artifacts are validated against JSON schemas before the pipeline advances.

Each run stores its artifacts in `runs/{run_id}/artifacts/`. Campaign-level artifacts live at the root.

---

### `research_brief.yaml`

**Created by:** Human (or proposed_brief from previous run's verdict_interpreter)  
**Read by:** hypothesis_generation  
**Schema:** `schemas/research_brief.schema.json`

| Field | Definition |
|---|---|
| `strategy_domain` | Asset class and market structure (e.g., `crypto_spot`) |
| `market_universe` | List of symbols to focus on (e.g., `[BTCUSDT]`) |
| `timeframe` | Candle resolution (e.g., `1h`) |
| `research_goal` | The central question this run tries to answer |
| `constraints` | Hard limits the hypothesis must respect (e.g., use existing backtest framework) |
| `existing_context` | What is already known or already tried — prevents re-exploring dead ends |

---

### `hypothesis_card.yaml`

**Created by:** hypothesis_generation skill  
**Read by:** innovation_expansion, validation_gate  
**Schema:** `schemas/hypothesis_card.schema.json`

| Field | Definition |
|---|---|
| `hypothesis_id` | Stable identifier (e.g., `H-005`) used to track the idea across runs |
| `thesis` | One-sentence plain-English claim about why this strategy should work |
| `rationale` | Market microstructure or behavioral reason supporting the thesis |
| `signal_concept` | Pseudo-formula or English description of the signal computation |
| `target_market` | Symbol, timeframe, and regime conditions where the signal applies |
| `assumptions` | List of things that must be true for the signal to work (falsifiable) |
| `expected_failure_modes` | Pre-enumerated ways this hypothesis could fail in practice |

---

### `expanded_hypothesis_card.yaml`

**Created by:** innovation_expansion skill  
**Read by:** validation_gate, backtest_specification  
**Schema:** `schemas/expanded_hypothesis_card.schema.json`

| Field | Definition |
|---|---|
| `base_hypothesis_id` | Links back to the parent hypothesis_card |
| `expanded_variants` | List of 3–6 concrete variants (V1–V6), each with its own signal variant and regime gate |
| `alternative_data_candidates` | Signals from different data sources that could replace or augment the core signal |
| `reverse_hypothesis` | The inverted version of the thesis (what if the signal works the opposite way?) |
| `behavioral_features` | Signals derived from trader psychology or crowd behavior rather than price mechanics |
| `regime_specific_variants` | Versions of the signal that only activate under a particular market regime |

---

### `innovation_notes.yaml`

**Created by:** innovation_expansion skill  
**Read by:** verdict_interpreter (for carryover), campaign_review  
**Schema:** `schemas/innovation_notes.schema.json`

| Field | Definition |
|---|---|
| `key_insight` | The most important conceptual discovery made during expansion |
| `recommended_test_order` | Prioritized list of variants to test first (most promising → least) |
| `risks_identified` | Structural risks seen across all variants |
| `variants_not_pursued` | Ideas that were considered but dropped, with brief rationale |
| `integration_notes` | Notes on how variants interact with existing bot components |

---

### `validation_protocol.yaml`

**Created by:** quant-validation skill  
**Read by:** validation_gate (self-produces it), backtest_specification, protocol_execution  
**Schema:** `schemas/validation_protocol.schema.json`

| Field | Definition |
|---|---|
| `falsifiable_statement` | A single, measurable prediction that, if false, kills the hypothesis |
| `null_expectation` | What results would look like if the signal has no edge (the baseline to beat) |
| `required_evidence` | Minimum metrics that must pass for approval (e.g., walk-forward hit rate ≥ 55%) |
| `bias_risks` | Specific biases this hypothesis is vulnerable to (look-ahead, selection, overfitting) |
| `failure_modes` | At least 5 named ways the strategy could fail in live trading |
| `sample_split_design` | How data is partitioned: train / walk-forward windows / holdout cutoff |
| `decision_rules` | Explicit gate conditions: what triggers approve / refine / reject |

---

### `validation_decision.yaml`

**Created by:** quant-validation skill  
**Read by:** orchestrator (for routing), refinement_planner  
**Schema:** `schemas/validation_decision.schema.json`

| Field | Definition |
|---|---|
| `status` | `approve`, `conditional_approve`, `refine`, or `reject` |
| `rationale` | Brief explanation of the decision |
| `blocking_issues` | List of specific problems that must be fixed before backtest (only present when status = refine) |

---

### `refinement_notes.yaml`

**Created by:** refinement-planner skill  
**Read by:** innovation_expansion (next iteration), orchestrator  
**Schema:** `schemas/refinement_notes.schema.json`

| Field | Definition |
|---|---|
| `blocker_responses` | For each blocking_issue from validation_decision, a concrete fix instruction |
| `decision.next_step` | What stage to route to next |
| `decision.implementation_allowed` | `true` if fixes can be made within the existing framework; `false` if a human must intervene |

---

### `backtest_spec.yaml`

**Created by:** backtest-engineering skill  
**Read by:** protocol_execution tool  
**Schema:** `schemas/backtest_spec.schema.json`

| Field | Definition |
|---|---|
| `status` | `spec_ready` (config is complete) or `component_gap` (a missing bot component blocks execution) |
| `config` | Full `strategy_config` JSON that plugs directly into the trading-bot |
| `config_rationale` | For each config parameter, why that value was chosen |
| `component_gap` | Description of the missing component if `status = component_gap` |

---

### `decision.yaml`

**Created by:** backtest-engineering skill (config validation step)  
**Read by:** orchestrator  
**Schema:** `schemas/decision.schema.json`

A simple gate artifact confirming whether the backtest_spec is valid and executable.

| Field | Definition |
|---|---|
| `stage` | Stage that produced this decision |
| `status` | `approved`, `blocked`, etc. |
| `blocking_issues` | Any config problems found during validation |

---

### `protocol_result.yaml` / `protocol_summary.json`

**Created by:** protocol_execution tool (`tools/run_protocol.py`)  
**Read by:** verdict_interpreter  

| Field | Definition |
|---|---|
| `per_window_metrics` | Sharpe ratio, max drawdown, trade count, win rate per backtest window |
| `per_symbol_metrics` | Aggregated results per symbol |
| `per_regime_metrics` | Results split by detected market regime |
| `median_sharpe` | Median Sharpe across all windows — primary promotion gate |
| `verdict` | `promote`, `kill`, or `refine` — preliminary verdict from the tool |
| `promotion_criteria` | Which gates passed / failed (median_sharpe, max_drawdown, min_trades) |
| `diagnostic_metrics` | `forecast_return_corr` (signal quality), `cost_drag_pct` (trading cost burden), `win_rate_vs_sharpe` (consistency check) |

---

### `verdict_interpretation.yaml`

**Created by:** verdict-interpreter skill  
**Read by:** orchestrator (for routing), campaign_review  

| Field | Definition |
|---|---|
| `altitude` | Numeric altitude of the decision (1 = refine, 2 = pivot, 3 = escalate) |
| `verdict` | `refine`, `pivot`, `escalate`, `promote`, or `kill` |
| `diagnostic_rule_applied` | Which named diagnostic rule triggered this verdict (e.g., `cost_drag`, `signal_inversion`) |
| `root_cause` | The underlying problem identified from diagnostics |
| `parameter_bracket` | If refining a parameter, the [min, max, step] range to search next |
| `next_altitude` | Fallback altitude if the current verdict fails again |

---

### `proposed_brief.yaml`

**Created by:** verdict-interpreter skill (when verdict = refine or pivot)  
**Read by:** next run's hypothesis_generation (becomes that run's research_brief)  

The pre-filled research_brief for the next run. Includes the `existing_context` field populated with what was learned from the current run, so the next run doesn't repeat dead ends.

---

### `escalation_request.yaml`

**Created by:** verdict-interpreter skill (when verdict = escalate)  
**Read by:** orchestrator  

| Field | Definition |
|---|---|
| `target_symbol` | New symbol to test (e.g., `SOLUSDT`) |
| `target_timeframe` | New timeframe to test (e.g., `4h`) |
| `rationale` | Why escalation to this target is expected to change the outcome |

---

### `findings_carryover.yaml`

**Created by:** verdict-interpreter skill  
**Read by:** next run's hypothesis_generation and verdict_interpreter  

Cross-run diagnostic memory. Prevents the next run from re-testing parameters or approaches already proven to fail.

| Field | Definition |
|---|---|
| `what_failed` | Specific configs or approaches that failed and should not be retried |
| `diagnostic_snapshot` | Key metric values from this run (sharpe, corr, cost_drag) for comparison |
| `what_not_to_try` | Explicit exclusion list for next run |
| `parameter_bracket` | Narrowed parameter search range based on this run's results |
| `next_altitude` | Recommended altitude escalation if next run also fails |

---

### `pipeline_state.yaml`

**Created by / Updated by:** orchestrator (`workflow/run_phase1_research.py`)  
**Read by:** orchestrator (on resume), any stage needing run context  

Internal run state — not a research artifact but the orchestrator's working memory.

| Field | Definition |
|---|---|
| `status` | `running`, `completed_promoted`, `completed_rejected`, `human_pause`, `error` |
| `current_stage` | The stage currently executing |
| `completed_stages` | Ordered list of stages already finished |
| `governance` | Budget limits: max_refinements, max_tokens, max_variants |
| `counters` | Runtime counters: `refinements_used`, `reruns_used` |
| `flags` | Boolean gates: `validation_approved`, `screening_passed`, `walk_forward_passed`, `holdout_reserved` |
| `audit_log` | Per-stage record of token usage, cost_usd, attempt number, and timestamp |

---

### `campaign_state.yaml`

**Created by / Updated by:** orchestrator  
**Read by:** orchestrator, campaign-review skill  

Root-level file tracking the entire campaign across all runs.

| Field | Definition |
|---|---|
| `campaign_id` | Unique identifier for this research campaign |
| `runs` | List of all run IDs attempted, with their verdict and altitude |
| `altitude_history` | Chronological record of altitude decisions across runs |
| `failed_families` | Hypothesis families that have been exhausted (prevents re-exploration) |
| `instruments_tried` | Symbols and timeframes already tested |
| `diagnostics_log` | Running record of key diagnostic metrics across runs (for trend analysis) |

---

### Handoff files (`handoffs/{from}_to_{to}.yaml`)

**Created by:** orchestrator (from templates)  
**Read by:** the receiving skill at stage start  

Handoffs are the formal interface contract between stages. Each stage reads its handoff file to know exactly what inputs are available and what it must produce.

| Field | Definition |
|---|---|
| `objective` | Plain-English goal for the receiving stage |
| `required_inputs` | Files the stage must read, with a `reason` for each |
| `optional_inputs` | Files that provide additional context if available |
| `constraints` | Hard rules the stage must not violate |
| `deliverables` | Artifacts the stage must produce |
| `assigned_engine` | Which engine runs this stage: `claude`, `gemini`, or `tool` |

---

## 4. Skills

Skills are LLM persona prompts stored in `skills/{name}/SKILL.md`. Each skill defines a role, a checklist, constraints, and forbidden actions for a Claude agent acting as a specialist. The orchestrator loads the relevant skill at each stage and passes it as the system prompt.

---

### `hypothesis-design`

**Goal:** Transform an open research brief into a single, concrete, testable hypothesis.  
**Why it exists:** Research briefs are necessarily vague. This skill bridges the gap between "I think volume matters" and a signal formula with explicit assumptions. Without this step, the downstream validation stage has nothing concrete to falsify.

Key constraints the skill enforces:
- Hypothesis must include a pseudo-formula or computation path for the signal.
- Assumptions must be falsifiable (not "markets are efficient" but "volume is a reliable proxy for institutional flow during trending regimes").
- Must identify at least 3 expected failure modes.

---

### `innovation-expansion`

**Goal:** Multiply a single hypothesis into 3–6 testable variants that explore the design space without losing scientific coherence.  
**Why it exists:** A single hypothesis tested once is a dead end if it fails. By generating a family of variants up-front, the pipeline can test the idea from multiple angles before discarding the entire family. This is where the system earns its search efficiency.

Key outputs:
- At least one **reverse hypothesis** (what if the signal works backwards?).
- At least one **behavioral variant** (derived from crowd psychology, not just price mechanics).
- At least one **regime-specific variant** (signal only activates in trending or ranging market).

---

### `quant-validation`

**Goal:** Pressure-test the hypothesis for structural flaws before any backtest runs.  
**Why it exists:** Backtesting is expensive and noisy. Running a broken hypothesis wastes compute and pollutes campaign history. This skill acts as a pre-flight check: if the idea cannot survive theoretical scrutiny, it should not enter the backtest queue.

Key outputs:
- A **falsifiable statement** (a single prediction that can be proven wrong).
- At least **5 failure modes** (named, specific failure scenarios).
- **Bias risks** (look-ahead contamination, selection bias, regime endogeneity).
- **Decision rules** (the exact conditions that trigger approve / refine / reject).

The skill is explicitly forbidden from approving a hypothesis that has no falsifiable statement or fewer than 5 failure modes.

---

### `refinement-planner`

**Goal:** Convert validation blockers into concrete, implementable fixes.  
**Why it exists:** When validation returns `refine`, the system needs specific instructions — not vague suggestions. This skill reads each blocking issue and produces an actionable response: which parameter to change, which assumption to drop, which variant to prioritize. It also acts as a circuit breaker: if the fixes require capabilities the bot doesn't have, it sets `implementation_allowed = false` and suspends the pipeline for human review.

---

### `backtest-engineering`

**Goal:** Translate an approved, validated hypothesis into a `strategy_config` JSON that the trading-bot can execute verbatim.  
**Why it exists:** The hypothesis exists in conceptual form (thesis, signal formula, regime gate). The backtest engine needs exact parameters: lookback windows, thresholds, component weights, regime definitions. This skill handles that translation, validates the output against `STRATEGY_CONFIG_REFERENCE.md`, and flags any component that doesn't yet exist in the bot.

The skill is forbidden from:
- Bypassing regime gates.
- Inventing parameter values not derived from the hypothesis.
- Producing configs that reference non-existent bot components.

---

### `verdict-interpreter`

**Goal:** Read backtest diagnostics, identify root causes, and issue an altitude decision.  
**Why it exists:** Raw backtest results (Sharpe = 0.2, drawdown = 18%) don't tell you *why* the strategy underperformed. This skill applies 5 named diagnostic rules to map metric patterns to root causes, then prescribes the correct next action. Without this step, the system would either blindly retry failures or discard salvageable ideas.

The 5 diagnostic rules:

| Rule name | Trigger condition | Prescribed action |
|---|---|---|
| `cost_drag` | `cost_drag_pct > 80%` | Raise threshold_filter to reduce trade frequency |
| `weak_signal` | `forecast_return_corr < 0.03` | Pivot — signal has no predictive content |
| `signal_inversion` | `forecast_return_corr < -0.03` | Reverse signal polarity |
| `regime_uninformative` | Regime split shows no performance difference | Re-gate regime detection |
| `parameter_exhausted` | Same parameter adjusted 2× with no improvement | Pivot hypothesis family |

Also produces **parameter brackets**: if refinement is prescribed, the skill narrows the search range [min, max, step] so the next run doesn't blindly retry the same value.

---

### `campaign-review`

**Goal:** After multiple hypothesis families have failed, step back and assess whether the campaign direction is still sound.  
**Why it exists:** The per-run verdict_interpreter only has local context. After 2+ families fail, the system needs a higher-level question: is this research question fundamentally unanswerable with current data/components, or just poorly explored? Campaign review can reframe the question, target a new instrument, or terminate the campaign entirely — decisions no single-run skill can make.

Key outputs:
- A campaign-level `continue / reframe / escalate / terminate` decision.
- If reframe: a new research_brief for the next run.
- If terminate: a final `research_decision.yaml` with lessons learned.

---

## 5. Tools & Scripts

### `workflow/run_phase1_research.py` — Pipeline Orchestrator

The central state machine. Manages the entire lifecycle of a run.

**Responsibilities:**
- Loads/saves `pipeline_state.yaml` and `campaign_state.yaml` at every transition.
- Invokes skills by building prompts from handoff files + skill personas and sending them to the Claude SDK or Gemini API.
- Routes between stages based on artifact contents (e.g., reads `validation_decision.yaml.status` to decide next step).
- Enforces circuit breakers (refinement budget, token budget, altitude escalation logic).
- Tracks token usage and cost per stage in the audit log.
- Includes iterative YAML repair: if a model produces malformed YAML, it attempts up to 3 auto-repairs before halting.
- Supports **resume**: a human-paused run can be restarted mid-pipeline without re-running completed stages.

### `workflow/setup_run.py` — Run Scaffolder

Creates the directory structure for a new run: `runs/{run_id}/artifacts/`, `runs/{run_id}/handoffs/`, and copies handoff templates. Called automatically by the orchestrator when starting a new run.

### `workflow/stages.yaml` — Stage Registry

Declarative configuration mapping each stage name to its skill file path and required inputs/outputs. The orchestrator reads this file — adding a new stage means adding an entry here plus a skill file, with no orchestrator code changes.

### `tools/run_protocol.py` — Walk-Forward Executor

The only fully deterministic tool (no LLM). Given a `backtest_spec.yaml`, it:
1. Loads the protocol definition (`protocols/baseline_v1.json` or an escalation protocol).
2. Runs the trading-bot backtest engine across each walk-forward window.
3. Aggregates per-window metrics (Sharpe, drawdown, trade count, win rate).
4. Evaluates promotion/kill thresholds.
5. Computes diagnostic metrics (`forecast_return_corr`, `cost_drag_pct`).
6. Writes `protocol_result.yaml` and `protocol_summary.json`.

### `tools/check_data.py` — Data Validator

Utility that checks whether historical OHLCV data is available and complete for the symbols and date ranges required by the protocol. Run before `run_protocol.py` to catch data gaps early.

### `protocols/` — Protocol Definitions

JSON files specifying the exact windows, symbols, timeframes, and thresholds for a backtest protocol.

| File | Purpose |
|---|---|
| `baseline_v1.json` | Default: BTCUSDT + ETHUSDT, 1h, 11 monthly windows (2024-01 to 2024-11) |
| `escalation_solusdt_4h.json` | Escalation to SOLUSDT on 4h timeframe |
| `escalation_avaxusdt_4h.json` | Escalation to AVAXUSDT on 4h timeframe |
| `diagnostic_btceth_4h.json` | Diagnostic run on BTC+ETH at 4h to isolate timeframe effects |

---

## 6. Glossary

| Term | Definition |
|---|---|
| **Campaign** | A sustained research effort around a single research question, spanning multiple runs and hypothesis families. A campaign ends when a strategy is promoted or the question is declared unanswerable. Example: "Can volume-based signals generate edge on BTC 1h?" |
| **Run** | One complete execution of the 10-stage pipeline for a specific hypothesis. Each run lives in `runs/{run_id}/` and produces its own set of artifacts. A campaign contains many runs. |
| **Research Brief** | The entry document for a run. Written by a human (or auto-generated from a previous run's proposed_brief), it defines the research question, target market, constraints, and what has already been tried. |
| **Hypothesis** | A single, falsifiable claim about a trading signal: what it is, why it should work, and under what conditions. More specific than a "strategy idea" — it must include a signal formula and explicit assumptions. |
| **Hypothesis Family** | A group of related hypotheses that share a core thesis but differ in implementation (e.g., all volume-momentum variants). If all variants in a family fail, the family is marked exhausted and excluded from future runs. |
| **Innovation Expansion** | The stage that multiplies a single hypothesis into a family of variants. Not random creativity — it follows a structured template: reverse, behavioral, regime-specific, alternative-data. |
| **Falsifiable Statement** | A prediction specific enough to be proven wrong by data. Required before any backtest. Example: "When momentum > 0 AND vol_ratio > 1.5, next-bar close is higher at least 55% of the time." Without this, a hypothesis cannot be rigorously tested. |
| **Validation Gate** | The pre-backtest quality check. An LLM agent acts as a skeptical quant and tries to find reasons to reject the hypothesis before any compute is spent. Passes → backtest. Fails → refine or reject. |
| **Walk-Forward Test** | A backtesting methodology where the model is evaluated on sequential, non-overlapping out-of-sample windows. Prevents overfitting by ensuring no window's results are used to tune the strategy. The baseline protocol uses 11 monthly windows. |
| **Holdout Period** | A final date range deliberately kept separate from all walk-forward windows. The strategy is never tuned on holdout data. It is only tested once, at the very end, to get an unbiased performance estimate. |
| **Protocol** | A JSON specification of the backtest conditions: which symbols, which timeframe, which windows, and what thresholds trigger promote/kill. Separating protocol from strategy config allows the same strategy to be tested under different conditions. |
| **Altitude** | A measure of how far from the original hypothesis the next search step will move. Altitude 1 = parameter tweak (same hypothesis). Altitude 2 = new hypothesis family (same question). Altitude 3 = new instrument or timeframe (same methodology). Higher altitude = larger change. |
| **Verdict** | The final word from the verdict_interpreter after a backtest: `refine`, `pivot`, `escalate`, `promote`, or `kill`. Each verdict maps to an altitude and a next action. |
| **Refine (altitude 1)** | Adjust a specific parameter of the current hypothesis based on diagnostic findings. The hypothesis family stays the same. Example: raise the threshold filter from 0.5 to 1.0. |
| **Pivot (altitude 2)** | Abandon the current hypothesis family and start a new one. The research question stays the same. Triggered when diagnostics show the core signal has no predictive content. |
| **Escalate (altitude 3)** | Keep the methodology but test it on a different symbol or timeframe. Triggered when the signal shows theoretical promise but the current market environment doesn't support it. |
| **Promote** | Terminal positive verdict. The strategy passed all validation gates, walk-forward windows, and (optionally) holdout. It is added to the campaign's approved strategy list and handed off to the deployment pipeline. |
| **Kill** | Terminal negative verdict. The hypothesis (or entire campaign) is declared unworkable. Root cause and lessons are archived in `research_decision.yaml` to inform future campaigns. |
| **Diagnostic Rule** | A named rule in the verdict_interpreter that maps a specific metric pattern to a root cause and a prescribed action. Example: `cost_drag` rule fires when trading costs consume > 80% of gross returns, prescribing a higher trade filter. |
| **Forecast** | A continuous signal in the range [-20, +20] produced by the strategy. Positive = bullish view, negative = bearish. The forecast drives portfolio allocation: it is converted to a target allocation [-1, +1] and triggers a rebalance when the gap between current and target exceeds the rebalance threshold. |
| **Regime** | A classification of current market conditions (e.g., `TRENDING`, `RANGING`, `HIGH_VOL`). Strategies can be gated to only activate in specific regimes. The regime detector runs in parallel with the signal and can suppress or amplify the forecast. |
| **Component** | A self-contained signal unit within the trading-bot strategy framework. Components implement `SubStrategyComponent` and produce a `ComponentOutput` with a forecast and confidence. Multiple components are combined by a `CompositeStrategy` via weighted sum. |
| **Strategy Config** | A JSON structure that fully specifies a strategy: which components to use, their parameters, regime gates, and combination weights. This is the machine-readable form of a hypothesis and the only input the backtest engine accepts. |
| **Handoff** | A YAML file that formally passes context from one stage to the next. It lists required inputs, optional inputs, constraints, and expected deliverables. Stages only read what their handoff specifies — they do not have access to the full conversation history. |
| **Circuit Breaker** | An automatic rule that interrupts a search loop when exhaustion is detected. Prevents infinite refinement of a dead-end hypothesis by forcing an altitude climb after a fixed number of failed attempts. |
| **Findings Carryover** | An artifact that preserves diagnostic memory across run boundaries. It tells the next run what was tried, what failed, and what parameter range to search next — preventing the campaign from cycling through the same dead ends. |
| **Artifact** | Any structured YAML or JSON file produced by a pipeline stage. Artifacts are the only allowed communication between stages. They must conform to their schema before the pipeline advances. |
| **Schema** | A JSON Schema definition (Draft 7) in `schemas/` that specifies the required fields and types for an artifact. Validation against the schema is a hard gate — a stage cannot advance if its output fails schema validation. |
| **Skill** | A Markdown file in `skills/` that defines a specialist LLM persona: its mission, required inputs/outputs, checklists, constraints, and forbidden actions. The orchestrator loads the relevant skill as the system prompt for each stage. |
| **Backtest Window** | A single contiguous date range used for one out-of-sample evaluation. The baseline protocol uses 11 monthly windows (January–November 2024). Results from all windows are aggregated to produce the final verdict. |
| **Forecast-Return Correlation** | A diagnostic metric measuring how well the strategy's forecast predicts next-bar returns. A value near 0 means the signal is noise. A negative value means the signal is inverted. The verdict_interpreter uses this as the primary signal-quality gate. |
| **Cost Drag %** | The fraction of gross returns consumed by trading costs (spreads, fees). A value above 80% means the strategy's edge is real but smaller than transaction costs — the fix is to trade less frequently. |
| **Parameter Bracket** | A [min, max, step] range produced by the verdict_interpreter when prescribing a refine verdict. Narrows the parameter search space based on current run results, enabling convergent search rather than random re-tries. |
| **Human Pause** | A pipeline state where automated execution is suspended pending human review. Triggered by `implementation_allowed = false` (a fix requires a new bot component) or by a `component_gap` in the backtest_spec. The pipeline resumes after the human resolves the blocker and restarts the orchestrator. |
| **Audit Log** | A per-stage record in `pipeline_state.yaml` tracking token usage, cost in USD, attempt number, and timestamp. Used to enforce token budgets and debug expensive runs. |
| **Campaign Review** | A special stage triggered after 2+ hypothesis families fail. Unlike the per-run verdict_interpreter, it has access to the full campaign history and can issue campaign-level decisions (reframe, terminate) that no single-run stage can make. |
| **Research Decision** | The terminal artifact of a campaign, written when a strategy is promoted or the campaign is terminated. Captures the final verdict, the lessons learned, and (if promoted) the approved strategy config. |
