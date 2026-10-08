# Strategy-Research Workflow — User Guide

Not sure this is the doc you need? See [`DOC_INDEX.md`](DOC_INDEX.md) first.

---

## Table of Contents

<!-- TOC:START -->
- [1. What This System Does](#1-what-this-system-does)
- [2. Workflow Overview](#2-workflow-overview)
  - [2.1 Stage Map](#21-stage-map)
  - [2.2 Stage Objectives](#22-stage-objectives)
  - [2.2.x Stage detail blocks](#22x-stage-detail-blocks)
    - [The input — `research_brief`](#the-input--research_brief)
    - [Stage 2 — `hypothesis_generation`](#stage-2--hypothesis_generation)
    - [Stage 15 — `strategy_config_authoring`](#stage-15--strategy_config_authoring)
    - [Stage 3 — `innovation_expansion`](#stage-3--innovation_expansion)
    - [Stage 4 — `validation_gate`](#stage-4--validation_gate)
    - [Stage 6 — `backtest_specification`](#stage-6--backtest_specification)
    - [Stage 14 — `data_availability_gate`](#stage-14--data_availability_gate)
    - [Stage 8 — `protocol_execution`](#stage-8--protocol_execution)
    - [Stage 9 — `regime_detector_validation`](#stage-9--regime_detector_validation)
    - [Not a stage — `regime_auditor` (a human procedure)](#not-a-stage--regime_auditor-a-human-procedure)
    - [Stage 11 — `verdict_interpreter`](#stage-11--verdict_interpreter)
    - [Stage 16 — `specialist_readers`](#stage-16--specialist_readers)
    - [Stage 17 — `regroup_record`](#stage-17--regroup_record)
    - [Stage 12 — `campaign_review`](#stage-12--campaign_review)
    - [Stage 13 — `holdout_evaluation`](#stage-13--holdout_evaluation)
  - [2.3 Decision Tree & Routing](#23-decision-tree--routing)
    - [After validation_gate](#after-validation_gate)
    - [After backtest_specification](#after-backtest_specification)
    - [After verdict_interpreter — the Altitude System](#after-verdict_interpreter--the-altitude-system)
    - [Circuit Breakers (anti-loop protection)](#circuit-breakers-anti-loop-protection)
    - [After campaign_review](#after-campaign_review)
    - [After holdout_evaluation](#after-holdout_evaluation)
    - [Composition mode (E-060 S3b, `orchestrator.composition_runs.enabled`, off by default)](#composition-mode-e-060-s3b-orchestratorcomposition_runsenabled-off-by-default)
- [3. Artifacts](#3-artifacts)
  - [`research_brief.yaml`](#research_briefyaml)
  - [`hypothesis_card.yaml`](#hypothesis_cardyaml)
  - [`expanded_hypothesis_card.yaml`](#expanded_hypothesis_cardyaml)
  - [`innovation_notes.yaml`](#innovation_notesyaml)
  - [`validation_protocol.yaml`](#validation_protocolyaml)
  - [`validation_decision.yaml`](#validation_decisionyaml)
  - [`refinement_notes.yaml`](#refinement_notesyaml)
  - [`backtest_spec.yaml`](#backtest_specyaml)
  - [`decision.yaml`](#decisionyaml)
  - [`protocol_result.yaml` / `protocol_summary.json`](#protocol_resultyaml--protocol_summaryjson)
  - [`verdict_interpretation.yaml`](#verdict_interpretationyaml)
  - [`proposed_brief.yaml`](#proposed_briefyaml)
  - [`escalation_request.yaml`](#escalation_requestyaml)
  - [`findings_carryover.yaml`](#findings_carryoveryaml)
  - [`pipeline_state.yaml`](#pipeline_stateyaml)
  - [`variant_selection.yaml` (per run)](#variant_selectionyaml-per-run)
  - [`variants_not_pursued.yaml` (per run)](#variants_not_pursuedyaml-per-run)
  - [`tried_ideas.yaml` (per run)](#tried_ideasyaml-per-run)
  - [`variant_anti_adjacency_result.yaml` (per run)](#variant_anti_adjacency_resultyaml-per-run)
  - [`schedulability.yaml` (campaign level)](#schedulabilityyaml-campaign-level)
  - [`campaign_state.yaml`](#campaign_stateyaml)
  - [Handoff files (`handoffs/{from}_to_{to}.yaml`)](#handoff-files-handoffsfrom_to_toyaml)
  - [`trade_diagnostics.json`](#trade_diagnosticsjson)
  - [`regime_detector_report.yaml`](#regime_detector_reportyaml)
  - [`regime_audit_decision.yaml`](#regime_audit_decisionyaml)
  - [`promotion_audit.yaml`](#promotion_audityaml)
  - [`holdout_result.yaml`](#holdout_resultyaml)
  - [`pre_registration.yaml`](#pre_registrationyaml)
  - [`pass_rule_evaluation.yaml`](#pass_rule_evaluationyaml)
  - [`run_context.yaml`](#run_contextyaml)
  - [`human_resolution.yaml`](#human_resolutionyaml)
  - [`config/venue_tradability.yaml` *(config)*](#configvenue_tradabilityyaml-config)
  - [`research_decision.yaml`](#research_decisionyaml)
  - [Config files (section 3 addendum)](#config-files-section-3-addendum)
- [4. Skills](#4-skills)
  - [`hypothesis-design`](#hypothesis-design)
  - [`innovation-expansion`](#innovation-expansion)
  - [`quant-validation`](#quant-validation)
  - [`backtest-engineering`](#backtest-engineering)
  - [`verdict-interpreter`](#verdict-interpreter)
  - [`campaign-review`](#campaign-review)
- [5. Tools & Scripts](#5-tools--scripts)
  - [`workflow/run_campaign.py` — Multi-Run Campaign Wrapper](#workflowrun_campaignpy--multi-run-campaign-wrapper)
  - [`tools/fragment_patterns.py` — Ideation-Only Fragment Diagnostics](#toolsfragment_patternspy--ideation-only-fragment-diagnostics)
  - [`workflow/run_phase1_research.py` — Pipeline Orchestrator](#workflowrun_phase1_researchpy--pipeline-orchestrator)
  - [`workflow/setup_run.py` — Run Scaffolder](#workflowsetup_runpy--run-scaffolder)
  - [`workflow/stages.yaml` — ARCHIVED 2026-08-24 (never read by the orchestrator)](#workflowstagesyaml--archived-2026-08-24-never-read-by-the-orchestrator)
  - [`tools/run_protocol.py` — Walk-Forward Executor](#toolsrun_protocolpy--walk-forward-executor)
  - [`tools/check_data.py` — Data Validator](#toolscheck_datapy--data-validator)
  - [`protocols/` — Protocol Definitions](#protocols--protocol-definitions)
  - [Tool inventory — everything in `tools/`](#tool-inventory--everything-in-tools)
- [6. Glossary](#6-glossary)
- [7. Acceptance Culture](#7-acceptance-culture)
  - [Known-answer fixtures (for metrics)](#known-answer-fixtures-for-metrics)
  - [Output audits (for prompts and skills)](#output-audits-for-prompts-and-skills)
  - [Pre-registration (for runs)](#pre-registration-for-runs)
  - [Calibration reporting](#calibration-reporting)
  - [Conflicting agent state (2026-07-10)](#conflicting-agent-state-2026-07-10)
- [8. The Machinery Around the Pipeline](#8-the-machinery-around-the-pipeline)
  - [8.1 What guards this repository](#81-what-guards-this-repository)
  - [8.2 Enforcement ledger — who actually enforces each rule](#82-enforcement-ledger--who-actually-enforces-each-rule)
  - [8.3 Documentation guards](#83-documentation-guards)
<!-- TOC:END -->

---

## 1. What This System Does

This is an **automated strategy research factory**. Its goal is to take a high-level research question ("can volume-confirmed momentum work on BTC?") and systematically generate, validate, backtest, interpret, and decide on trading strategy hypotheses — with minimal human intervention.

It is built around five principles.

- **Learn from the failure, don't just discard it.** A strategy that loses money
  is not a wasted run — it is the only evidence you have about *why* the idea
  does not work, and the input to the next one. The unit that fails is never
  "an indicator": it is a whole composition — a regime rule, a set of weighted
  sub-strategies, and the allocation between them. Discarding a run because it
  was unprofitable throws away the attribution that would tell you which part
  was wrong.
- **Understand the observation.** Do not run the next attempt without knowing
  what the last one did and why. Its absence is the costliest failure this
  campaign has had: **35 runs before anyone asked why the kills kept
  recurring.** A loop that produces results faster than they are understood is
  not research.
- **Structured artifacts over prose.** Every stage communicates through YAML
  files rather than free text, so a decision can be re-read later.
- **Automated routing.** The pipeline decides its own next step from rules
  rather than human judgment.
- **[Campaign](#g-campaign) memory.** Across many runs the system tracks what
  has been tried and detects dead ends.

**Falsification-first** — pressure-testing a [hypothesis](#g-hypothesis) for
failure modes before any code is [run](#g-run) — is a **feature of the
validation gate, not the governing philosophy**. It earns its place, but it is
one gate among several.

<details>
<summary>Corrections to this section (2026-08-31)</summary>

- "Structured artifacts" previously read *"validated* YAML files". **Nothing
  validates them** — no schema under `workflow_artifacts/schemas/` is loaded by
  any code. This was the third place that same false claim lived; see §3's
  preamble and [E037-34](../engineering/roadmap/E-037/FINDINGS.md#e037-34).
- Falsification-first was stated as *the* philosophy until 2026-08-31, which
  crowded out the two principles now above it.

</details>

---

## 2. Workflow Overview

> **THIS SECTION IS THE CANONICAL DESCRIPTION OF THE PIPELINE STAGES.**
> If you are looking for what the process steps are, what each stage is for,
> what it receives, or what it decides — it is here, and this is the only
> place that is maintained as authoritative.
>
> Anything else that describes stages is either operational (`RUNBOOK.md` —
> how to resume/halt), per-persona (`workflow_artifacts/skills/*/SKILL.md` —
> how one stage reasons), or historical (`engineering/improvements/done/` —
> design notes frozen at their date). **`workflow/stages.yaml` is NOT
> authoritative and is not read by any code** — see §"Stage Registry" below.
>
> Ground truth for the code is `STAGE_CONFIGS` + the handoff templates + the
> `determine_post_*` routing functions. When this section and the code
> disagree, the code wins and this section is a bug — fix it here rather than
> documenting the pipeline somewhere new. Reviewed/corrected 2026-08-24
> (E-033); the full stage review is E-033 S1.

**The three branches after a backtest** (terms used throughout this guide;
defined in `engineering/roadmap_review_2026-09-16.md` and roadmap card H).
On the new pipeline, every backtest's results feed three branches:

- **Branch 1, pass/fail:** the grid (`grid_evaluation.yaml` → `idea_status.yaml`)
  judges the idea on its pre-registered criteria. It is the only branch that
  decides the idea's status.
- **Branch 2, specialist patterns:** five category reports and their readers
  (stage 16). They propose next ideas and decide nothing. Since D-061 a
  malformed proposal is dropped and recorded, never a stop.
- **Branch 3, campaign-wide bar:** the profit bars, checked on every backtest.
  Passing them is the only way to the holdout (D-021).

`regroup_record` (stage 17) then writes all three into campaign memory before
anything decides what comes next.

### 2.1 Stage Map

Steps and links only. **Every gate, threshold, amendment code and caveat that
used to be drawn on this diagram now lives in that stage's block in
[§2.2](#22-stage-objectives)** — the map answers *"what follows what"*, the
block answers *"what does it do and why"*.

```
   [input]     research_brief          written by a human or the campaign runner
               │
   [Claude]  2  hypothesis_generation
               │
   [Claude]  3  innovation_expansion  ◄──────────┐
               │                                 │ refine (bounded — same call also
   [Claude]  4  validation_gate                  │ produces its own refinement plan,
               ├── approve ──┐                   │ no separate stage for it any more)
               ├── refine ───┼─────────────────► ┘
               └── reject ───┼─► completed_rejected
                             │
   [Claude]  6  backtest_specification
               │ spec_ready
   [Tool]   14  data_availability_gate         (E-054 Layer 2, ON BY DEFAULT since
               ├── validate ──────────────────► 8            2026-09-20 — config
               ├── refine ──► human_pause                    orchestrator.data_
               └── decline ─► completed_rejected              availability_gate.enabled)
               │
   [Tool]    8  protocol_execution             (always runs a full backtest —
               │                                there is no pre-backtest signal gate)
               │
   [Tool]    9  regime_detector_validation      (before the verdict, if stale)
               │
   [Claude] 11  verdict_interpreter
               ├── refine / pivot / escalate ──► new run
               ├── promote (provisional) ──────► 13
               └── kill                          ─ terminal
               │
   [Claude] 12  campaign_review                 (after 2+ family failures)
               ├── continue / reframe ─────────► new run
               └── terminate                     ─ terminal
               │
   [Tool]   13  holdout_evaluation
               ├── pass ─► promote               ─ terminal
               └── fail ─► kill                  ─ terminal
```

**Engine tags:** `[input]` not a step — an artifact the flow starts from ·
`[Claude]` an LLM stage the orchestrator dispatches · `[Tool]` a deterministic
Python stage, no LLM call.

**Numbering.** Stages keep the numbers this guide has always used, so 1, 7
and 10 are missing from the diagram on purpose: `research_brief` is an input
rather than a step, `regime_auditor` is a human procedure the orchestrator
never dispatches, and stage 7 (a pre-backtest signal gate) no longer exists —
the pipeline always runs a full backtest instead. `research_brief` and
`regime_auditor` are still documented below. `data_availability_gate` is
numbered **14**, out of position in the diagram above — it was added later
(E-054) and slotted into its real execution position (between 6 and 8)
without renumbering every stage after it; the number says nothing about
execution order, the diagram position does.

> **Every strategy currently trades all the time.** None of them switches
> itself on and off by market condition. Why, and what would change it, is in
> [stage 9](#stage-9--regime_detector_validation) — it is a fact about the
> campaign's present state, not a step in the flow.

**Config-direct-authoring variant (E-056 Slice 3b, off by default —
`orchestrator.config_direct_authoring.enabled`).** The diagram above is the
default-flag-off shape. When the flag is on, the graph is reshaped, not just
extended: a new `[Claude]` stage, `strategy_config_authoring`, is inserted
between `hypothesis_generation` (2) and `innovation_expansion` (3) — it
authors the single BASE strategy config directly from the hypothesis, before
any variants exist (adapted from `backtest_specification`'s own old job,
relocated earlier). `innovation_expansion` then produces
`variant_patches.yaml` (patches against that base config) instead of a prose
variant menu. `validation_gate` (4) becomes unreached — not deleted, its
stage-registry entry and routing code stay intact for flag-off runs, they are
simply never routed to. `backtest_specification` (6) becomes a `[Tool]`
stage: it applies each patch, validates the result
(`trading-bot/tools/validate_config.py`, including VIOLATION V12), and writes
one `strategy_config.json` per variant — the flow then rejoins the diagram
above at `data_availability_gate`/`protocol_execution`, run against the
`base` variant. See `strategy-config-authoring`/`innovation-expansion`
SKILL.md for the full mechanics.

**Verdict-routing-retired variant (E-059 S3, slice 6c S2a, off by default —
`orchestrator.verdict_routing_retired.enabled`; requires `decide_next` and
`profit_bars_every_backtest`).** Under the readers/regroup flags the graph
already reads `protocol_execution` → `specialist_readers` (16) →
`regroup_record` (17) → the grid's route. With this flag on, that route no
longer branches into promote / kill / refine / pivot / escalate: after the
`component_execution_error` pause and the `profit_bars_reached` stop
(both unchanged), the run ends at `completed_validated`, `completed_refuted`
or `completed_inconclusive` — the grid's `idea_status`, nothing else — and
`run_campaign.py`'s DONE branch runs decide-next, the only thing that picks
the next run. `verdict_interpreter` (11), the circuit breakers, the
escalation/timeframe protocols, continuation children and the route to
`holdout_evaluation` (13) are unreachable (their code stays for flag-off
runs, marked `# legacy routing (v26 card G)`; `_dispatch_verdict_route`
raises if entered, on the flag value run_loop read once in its pre-flight). The holdout is reached only from the `profit_bars_reached` stop
plus an operator unlock (slice 6c S2d): the resume reads
`artifacts/holdout_decision.yaml` — `spend` → the existing
`holdout_evaluation` gate for the named passing variant, `continue` →
`completed_<idea_status>` and decide-next. See stage 17, items 12 and 14.
Slice 6c S2c: under the same flag a run waiting on a missing component (step
1b's `component_gap`, or 5a failing only on a genuinely missing class) or on
fetchable missing data (a data-gate `decline` outside the sealed range, with no
fetch error, reserved or unknown feed) is **parked**, not paused: its
queue entry becomes `paused:waiting_for_component|data`, decide-next picks the
next run, and `run_campaign.py --unpark <entry_id>` restores it once the piece
exists (`docs/RUNBOOK.md` §3/§4).

---

### 2.2 Stage Objectives

**This table is the index.** One line per stage, answering *"which stage do I
want?"*. Everything else — what it consumes, what it produces, what logic runs,
the amendment codes, the traps — is in that stage's block below, which is the
one place to read when the answer matters.

| # | Stage | Engine | Objective — why the stage exists |
|---|---|---|---|
| — | [**research_brief**](#the-input--research_brief) | *input, not a step* | State the question this run exists to answer, and the limits it must respect. |
| 2 | [**hypothesis_generation**](#stage-2--hypothesis_generation) | Claude | Turn the research question into one concrete, testable claim. |
| 15 | [**strategy_config_authoring**](#stage-15--strategy_config_authoring) | Claude | Off by default (E-056 Slice 3b, `orchestrator.config_direct_authoring.enabled`). Config-direct-authoring flow only — sits between 2 and 3. Authors the single BASE strategy config directly from the hypothesis, before any variants exist (`strategy-config-authoring/SKILL.md`, adapted from stage 6's old job). |
| 3 | [**innovation_expansion**](#stage-3--innovation_expansion) | Claude | Produce variants that differ in kind, so a [kill](#g-kill) blames the idea rather than one setting. Config-direct-authoring flow: produces `variant_patches.yaml` (patches against stage 15's base config) instead of a prose variant menu. |
| 4 | [**validation_gate**](#stage-4--validation_gate) | Claude | Try to kill the hypothesis on paper, before any code is written for it. If it decides `refine`, the same call also decides whether the blockers can be fixed inside the current engine, and how. |
| 6 | [**backtest_specification**](#stage-6--backtest_specification) | Claude | Compile the validated idea into a config the engine can actually execute. Config-direct-authoring flow: becomes a Python tool stage instead — applies stage 3's `variant_patches.yaml` to stage 15's base config, validates each variant, writes one config per variant. |
| 14 | [**data_availability_gate**](#stage-14--data_availability_gate) | Python tool | Off by default (E-054). Check, per window and per declared aux feed, whether the data this variant needs can actually be assembled — before spending an expensive backtest on it. |
| 8 | [**protocol_execution**](#stage-8--protocol_execution) | Python tool | Trade the strategy across every walk-forward window and record what happened. |
| 9 | [**regime_detector_validation**](#stage-9--regime_detector_validation) | Python tool | Establish whether the regime detector is trustworthy enough to condition any metric. |
| — | [**regime_auditor**](#not-a-stage--regime_auditor-a-human-procedure) | ⚠️ Human, not dispatched | Judge the detector without letting profitability leak into the decision. **Not dispatched by the orchestrator** — see the block. |
| 11 | [**verdict_interpreter**](#stage-11--verdict_interpreter) | Claude | Decide what the result means, what to do next, and at what size of change. |
| 16 | [**specialist_readers**](#stage-16--specialist_readers) | Claude (×5 reader skills) | Off by default (E-046a Slice 5b-ii-B, `orchestrator.specialist_readers.enabled`). Replaces stage 11 when on: five readers each propose evidence-grounded changes from one category report; the route comes from the grid (`idea_status.yaml`), never from the readers. |
| 17 | [**regroup_record**](#stage-17--regroup_record) | Python tool | Off by default (E-058 S2a, `orchestrator.regroup_record.enabled`; requires stage 16's flag). Sits between 16 and its route: records the run in `campaign_record/campaign_memory.yaml` before the grid's route is taken. Decides nothing, writes no trial rows. |
| 12 | [**campaign_review**](#stage-12--campaign_review) | Claude | Ask whether the campaign's whole line of attack is still worth pursuing. |
| 13 | [**holdout_evaluation**](#stage-13--holdout_evaluation) | Python tool + human | Spend the one-shot holdout, and only after everything cheaper has passed. |

---

### 2.2.x Stage detail blocks

The table above is the index. Each block below answers, for one stage: what it
consumes, what it produces, what logic runs, and why it exists.

> **How rules are worded here, and why it matters.** A rule enforced by code
> is written as a fact — *"the run pauses"*, *"it raises"*, *"a second attempt
> is refused"*. A rule that only instructs the model is written as **"the skill
> is instructed to…"**. The difference is deliberate: several rules in earlier
> versions of this guide were phrased as gates — *"Must…"*, *"…= rejected"* —
> when nothing in the code could produce that outcome, so readers reasonably
> assumed a check existed. §8.2's ledger lists which is which.

**Terms used throughout this section**

*Stage-reading vocabulary. Campaign-level terms — campaign, run, hypothesis
family, [altitude](#g-altitude), exhausted — are in the [Glossary](#6-glossary).*

| Term | In plain words |
|---|---|
| **IC** (information coefficient) | How well a [forecast](#g-forecast) ranked what actually happened next. `+1` perfect, `0` useless, `-1` perfectly backwards. Spearman rank correlation. |
| **active bar** | A bar where the signal actually said something. A selective signal is silent most of the time. |
| **bps** (basis point) | One hundredth of a percent. Costs and edges are quoted in bps per trade. |
| **effective sample** (`n_eff`) | How many genuinely *independent* observations there are. Adjacent hours move together, so bar count overstates it. |
| **episode** | A burst of consecutive active bars treated as one event rather than many. |
| **[trial](#g-trial)** | One evaluation counted against the multiple-testing budget. Kills count. |
| **altitude** | How big a change the [verdict](#g-verdict) proposes: parameter → [component](#g-component) → family → instrument. |
| **[handoff](#g-handoff)** | The YAML file one stage writes to tell the next what to do and what inputs exist. |
| **DSR** (deflated Sharpe) | A Sharpe corrected for how many things you tried. More trials, higher bar. |
| **warmup** | The first stretch of bars an indicator needs before its output means anything. Decisions are not taken during it. |
| **turnover** | How often a strategy trades. High turnover pays the cost more often, so it needs a bigger edge to survive. |
| **Fisher z** | A transform that turns a correlation into something you can do normal statistics on, to ask "is this bigger than luck?". |
| **block** / **block bootstrap** | Nearby bars are not independent, so statistics are computed over *blocks* of bars rather than single ones. A **bootstrap** re-shuffles those blocks many times to see how often chance alone would produce the result. **Stationary block bootstrap** is one variant of that shuffle. |
| **firewall** (retune firewall) | A rule that keeps profitability out of a decision that is supposed to be about instrument quality. You may not retune a regime detector because it made more money. |
| **conformance gate** | A check that a run actually obeyed what it registered in advance — the [protocol](#g-protocol) it pinned, the method it declared. |
| **upsert** | Write-or-replace. Used for trial rows so a re-run replaces its earlier row instead of adding a second one and inflating the count. |
| **orchestrator** | The Python program that actually runs the pipeline: `workflow/run_phase1_research.py`. It decides which stage runs next and calls it. When this guide says "the orchestrator does X", it means that file. |
| **`STAGE_CONFIGS`** | The orchestrator's **list of stages it knows how to run**. If a stage name is not a key in it, the orchestrator has no way to reach that stage. It holds 11 entries. |
| **`_SKILL_MAP`** | The orchestrator's **list of which stages are run by an LLM, and which instruction file each uses**. 7 entries. A stage missing from it cannot be given to Claude — `_build_stage_prompt` refuses and raises an error rather than guessing. |
| **skill** | The instruction file an LLM stage is given, e.g. `workflow_artifacts/skills/quant-validation/SKILL.md`. It tells the model what to produce. A skill file can exist on disk without anything ever calling it. |
| **`library_category`** | A field in `config/indicator_library.yaml` saying what **kind** of indicator something is — trend, volatility, funding, and so on. Two variants built from different categories are genuinely different ideas; two that differ only in a threshold are the same idea twice. |
| **`data_requirements`** | Which data feeds a variant needs. The other way a variant can be genuinely different: same category, but it reads a feed the sibling does not. |
| **`CandleBuilder`** | The engine component that aggregates whatever rows it is fed into finished bars of `interval_seconds`. `CcxtFetcher` fetches and cache-keys at the exact requested timeframe, so by default `CandleBuilder` is only ever fed rows already at that timeframe — there is no automatic finer-cache derivation. `trading-bot`'s `DataManager` accepts an independent, opt-in `fetch_interval_seconds` (off by default) that fetches/caches at a finer resolution and lets `CandleBuilder` aggregate up during replay; a caller must opt in, it is never automatic. |
| **`KNOWN_STATUSES`** | A stage's list of result values it recognises. A value outside the list is not guessed at — the run pauses for a human. Being strict here is deliberate; see stage 6. |
| **`REPLICATION_DIAGNOSTIC`** | A constraint a brief can carry meaning "re-run this exactly, do not explore". It is why an expansion stage can legitimately return one variant instead of 3–6. |
| **raises** | Stops the run with an error instead of carrying on. Used deliberately where continuing would produce a decision from bad data — the project's rule is that anything feeding a decision fails loudly rather than quietly. |

> **Two kinds of name appear in these blocks, and only one is a term you need
> to learn.** A name followed by a file and a location — e.g.
> `run_protocol.py::_a851a_episode_significance` — is the **address of the
> code that does it**, not vocabulary: the sentence around it already says
> what happens, and the name is there so you can go and read it. A name in
> the table below **is** vocabulary, and you will not follow the block
> without it. When a block says a step **raises**, that means the run stops
> with an error rather than continuing on a bad value.

Amendment codes (`A2.1`, …) are defined in
[`AMENDMENTS_01-06.md`](../engineering/improvements/done/design_and_docs/AMENDMENTS_01-06.md);
each block glosses the ones it uses.

---

#### The input — `research_brief`

> **Not a step.** It has no entry in the orchestrator's stage registry, no
> engine and no logic of its own. It is the artifact the pipeline starts from,
> numbered as stage 1 in earlier versions of this guide because §2.2 is a
> reading order rather than a dispatch table.

**Written by:** a human, the campaign runner, or the previous run's verdict.
**Exists before:** anything else in the run.

**Objective.** State the question this run exists to answer, and the limits it
must respect.

**Design rationale.**
- Everything downstream is derived from the brief, so an unstated constraint
  here becomes an unstated constraint everywhere.
- `existing_context` is what stops the campaign re-exploring a dead end; it is
  the cheapest form of campaign memory.

**Stage input** — human intent, or `proposed_brief.yaml` from a previous run's
verdict_interpreter.

**Stage output**

| What | Written where | Read by |
|---|---|---|
| `research_brief.yaml` | `runs/{run_id}/artifacts/` | hypothesis_generation; also the holdout tradability gate and the pass-rule evaluator |

**Features / logic in place**

**1. Three different things write this file.**
The campaign runner (`run_campaign.py::_materialize_run`, `_materialize_run`), the next-run
spawner when a verdict proposes a new brief
(`run_phase1_research.py::_safe_write_new_research_brief`, `::setup_next_run`), or a human by hand. **Only the
campaign runner writes `research_only`**, which matters because the holdout
gate requires it — see stage 13.

**2. It is read late as well as early.**
Not only by stage 2. The pass-rule evaluator reads it (`::run_tool_worker`) because
deciding whether funding must be modelled needs the market_type, timeframe and
rebalance frequency; the holdout gate reads it to check tradability.

<details>
<summary><strong>Notes, history and traps</strong> — measured counts, past incidents, and the reasons behind each guard. Open when you need the evidence; skip when you need the flow.</summary>

- **F8 (2026-07-04):** only ever write `research_brief.yaml` for a run that
  does not already have one (`::_safe_write_new_research_brief`) — overwriting one mid-campaign silently
  rewrites the question a run was answering.
- A brief that does not declare `research_only: false` will be **refused** at
  the holdout gate. Silence is not a green light there.

</details>

---

#### Stage 2 — `hypothesis_generation`
**Engine:** Claude (skill `hypothesis-design`)
**Runs:** immediately after the brief. `default_next: innovation_expansion`.

**Objective.** Turn the research question into one concrete, testable claim.

**Design rationale.**
- **A hypothesis has to say who is losing the money you expect to make.** A
  forced seller, a flow that ignores fees, someone constrained by a mandate.
  "RSI crosses 30" names an indicator but no counterparty, so there is nothing
  to disprove — it either worked or it didn't, and you learn nothing either
  way. **The skill is instructed to** write `edge_source` before
  `signal_concept`, so the counterparty is named before the formula. Nothing in
  the code checks the ordering.
- **Check the library before inventing.** `indicator_library.yaml` records
  which indicator classes have already been tried and what killed them, so the
  campaign does not rediscover a dead end. **The skill is instructed to** do
  this lookup (A1.4 / Improvement 04); no code verifies that it did.

**Stage input**

| What | Where it comes from | Required? |
|---|---|---|
| `research_brief.yaml` | stage 1 | yes |
| handoff `research_brief_to_hypothesis.yaml` | orchestrator | yes |
| `config/indicator_library.yaml` | 15 seeded entries | consulted by the skill |
| `config/available_feeds.yaml` | which feeds are testable today | consulted by the skill |

**Stage output**

| What | Written where | Read by |
|---|---|---|
| `hypothesis_card.yaml` | `runs/{run_id}/artifacts/` | innovation_expansion, validation |

**Features / logic in place**

**1. Ordering and library lookup are skill instructions, not code gates.**
A1.1–A1.3 (populate `edge_source` before `signal_concept`) and A1.4 (look the
indicator up in `indicator_library.yaml`) live in the skill prompt. As with
stage 3, no Python enforces them — see [E037-18](../engineering/roadmap/E-037/FINDINGS.md#e037-18).

**2. Say which data the signal is built on.**
The card names its `evidence_type`, chosen from `config/available_feeds.yaml` —
the list of feeds that exist and are testable today.

**3. If the data does not exist, ask for it instead of assuming it.**
A signal needing a feed nobody has routes to `feed_wishlist.yaml` rather than
being written against imaginary data.

**4. If the model returns several hypotheses instead of one, they are split
rather than rejected.**
(`run_phase1_research.py::_handle_hypothesis_generation_multi_card_split`)

**5. What was already tried is an optional input.**
Under `orchestrator.exclusion_digest_input.enabled` (on), the stage receives
[`tried_ideas.yaml`](#tried_ideasyaml-per-run) — one row per recorded run
(idea, coins, timeframe, grid status), no family grouping — when
`campaign_record/campaign_memory.yaml` exists; otherwise (today's default)
the legacy family-grain `campaign_record/exclusion_digest.yaml`, exactly as
before E-036 S2a (`run_phase1_research.py::_apply_exclusion_digest_input`).
The skill is told to redirect rather than repeat; the binding check is the
exact-match check at stage 6.

---

#### Stage 15 — `strategy_config_authoring`
**Engine:** Claude (skill `strategy-config-authoring`)
**Runs:** off by default (`orchestrator.config_direct_authoring.enabled`,
`config/campaign_config.yaml`). When on, immediately after stage 2, before
stage 3. `default_next: innovation_expansion`.

**Objective.** Author the single BASE `strategy_config` directly from the
hypothesis — no variant menu exists yet at this point in this flow. Adapted
from `backtest-engineering`'s old job (stage 6), relocated from
post-validation/post-expansion to pre-expansion.

**Design rationale.**
- **Config-direct authoring reverses the old order.** Instead of expanding
  variants first and compiling one of them into a config last (stage 6's old
  position), this flow compiles the base config FIRST, so stage 3
  (`innovation_expansion`) can express every variant as a patch against a
  real, already-valid config rather than free-text.
- **No `selected_variant_id`.** Stage 6's old `IMPROVEMENT 01` (pick one menu
  entry, name it) does not apply here — there is nothing to pick from yet.
  **The skill is instructed** to omit that field entirely in this flow.
- **`validation_gate` (stage 4) becomes unreached, not deleted**, when this
  flag is on — its registry entry and routing code stay intact for flag-off
  runs; nothing routes to it under config-direct authoring (see stage 3's
  own block and stage 6's routing note below).

**Stage input**

| What | Where it comes from | Required? |
|---|---|---|
| `hypothesis_card.yaml` | stage 2 | yes |
| `STRATEGY_DESIGN_GUIDE.md` | `strategy-research/docs/` | yes |
| `COMPONENT_CATALOG.md` | `strategy-research/docs/` | yes |
| `DATA_AVAILABILITY.md` | `strategy-research/docs/` | optional, forced-read on a new timeframe/symbol/venue |
| `quant-fundamentals/SKILL.md` | `workflow_artifacts/skills/`, added by code (CUL-336) | yes |

**Stage output**

| What | Written where | Read by |
|---|---|---|
| `backtest_spec.yaml` | `runs/{run_id}/artifacts/` | innovation_expansion (as the base config to patch), the tool-only stage 6, verdict_interpreter |
| `decision.yaml` | `runs/{run_id}/artifacts/` | `determine_post_strategy_config_authoring_route` |
| `block_manifest.yaml` (spec_ready only) | `runs/{run_id}/artifacts/` | `determine_post_strategy_config_authoring_route` (checked, one retry), the tool-only stage 6 (re-checked, fails loud), `tools/block_registry.py` (stage 17) |

**Features / logic in place**

**1. Same `decision.yaml` contract as stage 6's old LLM path.**
`status: spec_ready` routes to `innovation_expansion`; `status: component_gap`
pauses for a human (`determine_post_strategy_config_authoring_route`,
`run_phase1_research.py`) — the same shape `determine_post_spec_route` uses
for stage 6, just a different success target.
Under `orchestrator.nearest_build.enabled` (off by default; requires
`config_direct_authoring` and `claim_tests`; D-075), 1b builds
the nearest version of an idea instead of parking it: it answers `spec_ready`
with the closest config the catalogue allows and lists each difference in
`decision.yaml` `deviations` (clause, built_instead, missing, effect). Code
writes `artifacts/deviations.yaml`, adds each missing piece to
`campaign_record/component_requests.yaml` as a `kind: deviation` row (never
an `--unpark`, cap or request-count input), and shows the deviations first in
the finding ("this run tested an approximation of the idea: ..."), the
findings-summary row and the readers' digest. A `component_gap` must then
name `core_lost: {clause, why}`, or it gets O-21's one retry.
**2. Same "Ungated hypotheses" and "Forbidden" rules as `backtest-engineering`.**
Carried over intact from that skill (E-056 Slice 3b's own pre-registered
success signal for this rewrite was a byte-diff against the retired content
confirming no rule was silently dropped).
**3. Writes `block_manifest.yaml` (E-056 1b block manifest, 2026-09-24).**
Which part of the base config IS the hypothesis's block, as opposed to
scaffolding: `{block: {kind: forecast|regime, config_paths: [JSON pointers]},
scaffolding: [JSON pointers], rationale}` — contract in
`STRATEGY_DESIGN_GUIDE.md` ("Manifest contract"), schema
`workflow_artifacts/schemas/block_manifest.schema.json`, one implementation in
`tools/block_manifest.py`. A stale manifest is deleted when this stage
starts. Right after it, `determine_post_strategy_config_authoring_route`
checks the manifest against `backtest_spec.yaml`'s config: missing or
invalid sends this stage back once with the error in its handoff
(`injected_context.block_manifest_error`), a second failure stops the run.
The tool-only stage 6 re-checks it as a backstop; per variant only block
paths must resolve (scaffolding may change). No coin field (a block is
usable on any coin).

---

#### Stage 3 — `innovation_expansion`
**Engine:** Claude (skill `innovation-expansion`)
**Runs:** after stage 2, and again on every refinement loop.
`default_next: validation`.

**Objective.** Turn one hypothesis into a small set of genuinely different
variants, so the test is of a mechanism rather than of one arbitrary
parameterisation.

**Design rationale.**
- Testing one parameterisation confounds "the idea is wrong" with "this
  setting is wrong".
- **The skill is instructed to** make variants differ in *kind* rather than in
  threshold value — otherwise the set is one trial wearing several hats, and it
  inflates the count without adding information. This is guidance to the model,
  not a check; see logic step 2.

> ⚠️ **This stage generates 3–8 variants and the pipeline tests one.** Measured
> across every run: **139 generated, 36 tested, 103 discarded untested (74%)**,
> and no run has ever built more than one config. So the objective above is not
> currently achieved — a kill still cannot separate "the mechanism is wrong"
> from "this setting was wrong". Owned by
> [E-033](../engineering/roadmap/E-033/EPIC.md) S3; recorded as
> [E037-36](../engineering/roadmap/E-037/FINDINGS.md#e037-36).

**Stage input:** `hypothesis_card.yaml`, handoff
`hypothesis_to_innovation_expansion.yaml`, `config/indicator_library.yaml`,
`config/coin_universe.yaml` (added by code, CUL-336);
optionally [`tried_ideas.yaml`](#tried_ideasyaml-per-run) (same rule as
stage 2's item 5).

**Stage output:** `expanded_hypothesis_card.yaml`, `innovation_notes.yaml`
(including a self-reported `diversity_audit` block). Config-direct flow
(`orchestrator.config_direct_authoring.enabled`): also `variant_patches.yaml`,
a checked deliverable since E-061 C1.2 (`::_config_direct_step2_deliverables`,
added in memory only — to the prompt's handoff and to run_loop's check, never to
the run's handoff file, so a flag-off resume does not require it). It must be
written by this attempt: a previous attempt's file is moved to
`runs/<run_id>/.previous_attempts/innovation_expansion_attempt_<n>/` when the attempt
starts (`::_clear_config_direct_attempt_outputs`) and the file must exist after it
(`::_check_config_direct_attempt_outputs`), so a step 2 that omits it, or leaves a
previous attempt's file, fails here, not at 5a. The stage input then also carries
`backtest_spec.yaml` (stage 15's base config).

**Features / logic in place**

**1. 3–6 variants, when the brief leaves it free.**
A brief carrying `"Single registered hypothesis, no parameter sweep"` or a
`REPLICATION_DIAGNOSTIC` constraint correctly yields one variant, and that is
obedience, not stage failure. Measured 2026-08-26: of 25 *unconstrained*
expansion runs, 21 land in [3,6].

**2. ⚠️ The diversity check is not enforced by any code.**
The rule is meant to stop the stage producing variants that only *look*
different — five versions of one idea with different threshold numbers, which
would spend five trials to learn one thing. Real difference means either a
different **`library_category`** (a different kind of indicator: trend vs
volatility vs funding) or different **`data_requirements`** (it reads a feed the
others do not).

**Nothing checks it.** `library_category` appears **once** in all of
`workflow/` and `tools/` — and not even in a prompt: it is inside a *docstring*
recounting a YAML-repair incident
(`run_phase1_research.py::ensure_files`). The rule lives in
`workflow_artifacts/skills/innovation-expansion/SKILL.md:74-105`, and the model
self-reports the verdict. **No code can produce the "rejected" outcome.**
See [E037-18](../engineering/roadmap/E-037/FINDINGS.md#e037-18).

---

#### Stage 4 — `validation_gate`
**Engine:** Claude (skill `quant-validation`)
**Code name:** `validation` — that is the `STAGE_CONFIGS` key, the
`_SKILL_MAP` key, and the name in `determine_post_validation_route`.
**Runs:** after expansion. `default_next: dynamic_routing`.

**Objective.** Try to kill the hypothesis on paper, before any code is written
for it. If its own verdict is `refine`, the same call also decides whether
the blockers it found can actually be fixed inside the current engine, and
how (E-039 S4, 2026-09-12 — see item 4 below).

**Design rationale.**
- Falsification is cheapest before implementation. A failure mode found here
  costs a paragraph; found after a backtest it costs a trial.
- There is no pre-flight kill on an *estimated* activation rate here — the
  pipeline's premise is "always backtest": E-054's data-availability gate
  handles the real structural/data question (can this even be assembled),
  and the go/no-go on the signal itself is decided from real, measured
  numbers once a backtest has actually run (`determine_route`/`cost_check`,
  `trading-bot/performance/signal_statistics.py`), not from an early
  statistical guess.
- The refine loop back to expansion is bounded (2 by default,
  `max_refinements_after_validation`) so a hypothesis cannot be refined
  indefinitely into a fit.

**Stage input:** `expanded_hypothesis_card.yaml`, `hypothesis_card.yaml`,
`innovation_notes.yaml` (only needed on the refine path), handoff
`innovation_expansion_to_validation.yaml`, `pipeline_state.yaml`
(for the refinement counter), `pre_registration.yaml` if present (the
pre-registered `sample_split_design.holdout_range`, A6.1 — see below),
`config/cost_model.yaml` (required, for the information-only `cost_feasibility`
estimate, added by code — CUL-336; since O-3 it never blocks approval). `innovation_notes.yaml` and `docs/DATA_AVAILABILITY.md` are added
only when the run is already in a refine loop (`artifacts/refinement_notes.yaml`
exists), keeping a first pass at minimal context. `config/campaign_data_policy.yaml` is deliberately
not an input: the skill says not to read it directly, and the one field it
fed (`sample_split_design.walk_forward_range`) has no code reader.

**Stage output:** `validation_protocol.yaml`, `validation_decision.yaml`,
and — only when its own `status` is `refine` — `refinement_notes.yaml`
(carrying `decision.implementation_allowed`) in the same response.

**Features / logic in place**

**1. The router reads this stage's own verdict to pick the next stage.**
The stage writes `validation_decision.yaml`; the orchestrator's router then
reads it. Two different actors, not a loop.
It looks for `status`, falling back to `family_status` — the skill once emitted
the latter for a multi-variant family validation (run_053, 2026-07-06, F4f). If
neither key is present it raises rather than guessing
(`::determine_post_validation_route`).

**2. No power gate here.** An `approve`/`conditional_approve` routes to
`backtest_specification` unconditionally — there is no a-priori power check
that can block a run at this stage.

**3. `conditional_approve` aggregates per-variant conditions.**
The family-schema output has no top-level `conditions`, so they are collected
from `variant_decisions` (`::determine_post_validation_route`).

**4. A `refine` verdict resolves its own next step in the same call — no
separate stage.** E-039 S4 (2026-09-12) retired `refinement_planner` as its
own pipeline stage: it used to be a second LLM call, receiving this stage's
`refine` decision as a handoff and doing nothing but turn it into a plan.
Now this same call reads its own `blocking_issues` and produces
`refinement_notes.yaml` directly (`decision.implementation_allowed`, default
`True` if absent). `determine_post_validation_route` then reads that file
immediately: `implementation_allowed: false` pauses the pipeline for a human
(write `human_resolution.yaml`, then `--resume`); otherwise it loops back to
`innovation_expansion` (`::determine_post_refinement_route`, still a
separate function, just no longer a separate stage).

**Routes / outcomes**

| Decision status | Next |
|---|---|
| `approve` / `conditional_approve` | `backtest_specification` unconditionally |
| `refine`, `implementation_allowed: false` in the same response's `refinement_notes.yaml` | `human_pause` — write `human_resolution.yaml`, then `--resume` |
| `refine`, otherwise, up to `max_refinements_after_validation` (default 2) | `innovation_expansion` |
| `refine`, refinement limit already reached | `completed_rejected` |
| `reject` | `completed_rejected` |

<details>
<summary><strong>Notes, history and traps</strong> — measured counts, past incidents, and the reasons behind each guard. Open when you need the evidence; skip when you need the flow.</summary>

- The guide's §2.3 lists approve / refine / reject. **`conditional_approve` is
  a fourth accepted status** and behaves as approve with printed conditions.
- A6.1's holdout-range declaration (`sample_split_design.holdout_range`) is
  pre-registered once, at brief materialization
  (`run_campaign.py::_materialize_run`/`_materialize_refinement_run`,
  alongside `pass_rule`) — **not** produced by this stage. Moved here
  2026-09-12 (E-039 S4) from this stage's own skill, which used to re-read
  `campaign_data_policy.yaml` and restate the same, never-changing value on
  every run; confirmed unread anywhere as a `validation_protocol.yaml` field,
  so the move cost nothing. This stage's own job is only the walk-forward
  window *design* around that frozen boundary (`sample_split_design.windows`/
  `window_size_bars`/`step_size_bars`).

</details>

---

#### Stage 6 — `backtest_specification`
**Engine:** Claude (skill `backtest-engineering`)
**Runs:** after an approved validation. `default_next: dynamic_routing`.

**Objective.** Compile the validated idea into a config the backtest engine can
actually execute.

**Design rationale.**
- This is where an idea stops being prose. Everything after it is measured
  against the compiled config, not the description.
- Declaring a *component gap* rather than improvising one is what keeps the
  engine's component set honest.

**Stage input:** `expanded_hypothesis_card.yaml`,
`validation_decision.yaml`, handoff
`validation_to_backtest_specification.yaml`; added by code (CUL-336):
`quant-fundamentals/SKILL.md` (required) and, when present,
`innovation_notes.yaml`, `docs/DATA_AVAILABILITY.md`,
`findings_carryover.yaml`, `run_context.yaml`.

**Stage output:** `candidate_strategy_config.json`, `decision.yaml`,
`variant_selection.yaml`.

**Config-direct flow (tool stage, E-061 C1.2).** The stage loads
`handoffs/config_direct_backtest_specification.yaml` instead, rewritten by code
from the current flags at every stage entry (`::_config_direct_handoff_path`):
**input** `backtest_spec.yaml` (stage 15's base config) and `variant_patches.yaml`
(stage 3), no `validation_protocol.yaml` (stage 4 is never reached);
**output** `variants/index.yaml` (checked: the previous one is moved to
`.previous_attempts/` when the attempt starts, so it must be this attempt's), one
`variants/<variant_id>/strategy_config.json` per variant, and
`candidate_strategy_config.json` when the `base` variant validates.

**Features / logic in place**

**1. Exactly two known statuses; anything else pauses.**
`spec_ready` → `protocol_execution` (optionally via `data_availability_gate`
first — see below). `component_gap` → `human_pause` with a pointer to
`STRATEGY_EXTENDING.md`. **Any unrecognised status also pauses**, printing
that the SKILL may need a new status case rather than guessing
(`::determine_post_spec_route`). Failing closed on an unknown status is deliberate.

**2. Exact-match repeat check (off by default).**
Under `orchestrator.variant_anti_adjacency_gate.enabled` (E-034 S3, redesigned
by E-036 S2a; `false`), the config about to be backtested is checked against
`campaign_record/campaign_memory.yaml` on the same key decide-next binds on
(`tools/novelty.py`: config hash, sorted symbols, the protocol file's timeframe
and a hash of its windows). Binary: REPEAT or NOVEL — no family, no
neighbour; the knowledge-base check is recorded as an advisory only. It runs
for every queue origin (operator, external, queued card, reader, brief).
- LLM flow: right after `candidate_strategy_config.json` is written
  (`::_route_post_variant_selection`); REPEAT → `human_pause`, reason
  `variant_anti_adjacency_gate_refused`.
- Config-direct flow (tool stage): per variant, before routing
  (`::_gate_config_direct_variants`); a REPEAT variant is marked `not_tested`
  (`reason: "repeat: ..."`) and is never backtested (no trial row); if every
  variant is a repeat the run ends `completed_no_new_hypothesis`. A repeat
  skip is never read as a data shortfall: the variant loop's "at least 3
  validated" check counts only non-repeat variants (repeats alone never
  pause the run; data declines among the rest still pause or park as
  before), and parking ignores repeat skips. Composition runs are not gated.
Result: [`variant_anti_adjacency_result.yaml`](#variant_anti_adjacency_resultyaml-per-run).
With no memory file and `regroup_record` off, the gate raises rather than
admit everything.

**Routes / outcomes**

| `decision.status` | Next |
|---|---|
| `spec_ready` | stage 14 `data_availability_gate` by default (`orchestrator.data_availability_gate.enabled`, default true — see stage 14's own block), else stage 8 `protocol_execution` directly if explicitly disabled in config |
| `component_gap` | `human_pause` — extend the engine, then resume |
| anything else | `human_pause` |
| exact repeat (gate on, item 2) | LLM flow: `human_pause`; config-direct: repeat variants skipped, all repeats → `completed_no_new_hypothesis` |

---

#### Stage 14 — `data_availability_gate`
**Engine:** Python tool (`tools/data_availability_gate.py`), launched as a
subprocess by the orchestrator (`workflow/run_phase1_research.py::run_tool_worker`).
No LLM call, no token cost.
**Runs:** after `backtest_specification` emits `spec_ready` and the config
passes schema validation — **by default** (delivery_plan_v26.md s:0.4 item
14, 2026-09-20: the one flag in this codebase that ships on). Gated by
`orchestrator.data_availability_gate.enabled` in `config/campaign_config.yaml`,
default `true` on a missing key/section/file
(`run_phase1_research.py::_data_availability_gate_enabled`). Only when
explicitly set to `false` is this stage skipped, with `spec_ready` routing
straight to stage 8 `protocol_execution` instead — byte-identical to the
gate's original 2026-09-11 off-by-default (env-var) behavior.

**Objective.** A hard, mechanical, data-only check: for the symbols,
timeframe, windows, and declared aux feeds this variant needs, can the data
actually be assembled — *before* an expensive backtest is ever invoked on it.
Real precedent this stage exists to catch: `run_050`/`run_060` both crashed
mid-`protocol_execution` on exactly this failure mode (CUL-230).

**Design rationale.**
- Two layers, because they answer genuinely different questions. **Layer 1**
  (`strategy-research/config/venue_data_capability.yaml`, a committed,
  human-audited reference — E-054's own prerequisite work) is a cheap,
  zero-network capability audit: could this (venue, symbol, timeframe,
  aux-feed) combination possibly exist at all. **Layer 2** (this stage's own
  code, `tools/data_availability_gate.py`) is the real, per-window data
  touch for whatever survives Layer 1: is the actual cached/fetchable data
  clean enough within each specific window. No audit can answer Layer 2's
  question in advance — internal gaps are a property of what actually
  happened to the data over time.
- **Every window is checked individually**, not the full protocol span in
  one call — the only way a `refine` outcome (narrow around the bad window,
  keep the rest) is possible instead of an all-or-nothing verdict.
- Resolves the protocol via the SAME shared resolver
  (`tools/protocol_resolution.py::resolve_protocol_path`, extracted from this
  orchestrator's own `_resolve_protocol_path`) that `protocol_execution`
  uses — so it checks the literal protocol that will
  execute, never a hypothesis-level declared timeframe (those can silently
  diverge from what actually runs — confirmed during E-054's own
  characterization).
- Exchange resolution mirrors `tools/run_protocol.py`'s locked "Option Y"
  order exactly: explicit override → `protocol.get("exchange")` →
  `"binance"`.
- Gap tolerance: **5%** of a window's (or an aux feed's own native-cadence
  window's) expected observations missing → `refine`; above that →
  `decline`; 0% → `validate`. An aux feed coarser than the strategy's candle
  interval (e.g. daily `fear_greed` under an hourly strategy) is measured in
  its OWN native cadence, never candle units — measuring in candle units
  would make every normal daily feed look ~95%+ "missing" by construction.
- Off by default, unlike every other stage in this table: a brand-new,
  unproven pre-flight check gates every future campaign run the moment it is
  turned on, so it ships opt-in first (bit-identity discipline).

**Stage input:** `candidate_strategy_config.json` (declared `aux_feeds`), the
resolved protocol JSON (symbols/timeframe/windows).

**Stage output:** `data_availability_gate.yaml` — `outcome`
(`validate`/`refine`/`decline`), `reasons`, and full per-window/per-feed
detail.

**Config-direct flow (E-061 C1.2).** Handoff
`handoffs/config_direct_data_availability_gate.yaml`, rewritten by code from the
current flags at every stage entry (the legacy
`backtest_spec_to_data_availability_gate.yaml` is written only on the legacy 5a
branch). With `orchestrator.variant_loop.enabled`: **input** `variants/index.yaml`;
the gate runs once per validated variant and writes
`variants/<variant_id>/data_availability_gate.yaml`, marking a
refine/decline/crashed variant `not_tested`. **Checked outputs**: every
variant's previous gate file is moved to `.previous_attempts/` when the attempt
starts (`::_clear_config_direct_attempt_outputs`); after it, the gate file of every
variant still `validated` must exist (`::_check_config_direct_attempt_outputs`; a
variant whose gate crashed is `not_tested`, so not required; a gate that writes
nothing fails the stage). The index is the stage's input, rewritten in place, so it
is not cleared. Never `artifacts/data_availability_gate.yaml`.
Without the variant loop: the input/output above.

**Routes / outcomes**

| `data_availability_gate.yaml`'s `outcome` | Next |
|---|---|
| `validate` | stage 8 `protocol_execution` |
| `refine` | `human_pause` — a human narrows the variant (drop the listed window(s)/feed), writes `human_resolution.yaml`, then `--resume` |
| `decline` | `completed_rejected` — a required series does not exist at all, no workaround |

---

#### Stage 8 — `protocol_execution`
**Engine:** Python tool (`tools/run_protocol.py`), launched as a subprocess.
**Runs:** unconditionally, after `backtest_specification` (optionally via
`data_availability_gate` first). There is no pre-backtest signal gate that
can skip it. `default_next: verdict_interpreter`.

**Objective.** Actually trade the strategy across every walk-forward window and
record what happened.

**Design rationale.**
- Walk-forward rather than one fit: a strategy that only works on the window it
  was designed against is a curve fit, and this is what exposes that.
- It emits per-trade records, not just aggregates, because aggregate medians
  hide the failure channel — the finding behind A3.6.

**Stage input**

| What | Where it comes from | Required? |
|---|---|---|
| `candidate_strategy_config.json` | stage 6 | yes (variant loop: `variants/index.yaml` and each validated variant's config instead) |
| protocol JSON | `_resolve_protocol_path()` | yes |
| `validation_protocol.yaml` | stage 4 | legacy flow: yes. Config-direct flow: no — stage 4 never runs, so it is passed to `run_protocol.py` only when it exists, else `--diagnostics-only` (E-061 C1.3, `::_validation_protocol_args`); handoff `handoffs/config_direct_protocol_execution.yaml`, rewritten from the current flags at every stage entry (E-061 C1.2) |
| `pre_registration.yaml` | the registered `pass_rule` | yes for the C7 evaluation |
| `research_brief.yaml` | stage 1 | yes since C7-EXT (funding-modelling precondition) |

**`signal_real_but_subscale_vs_costs`** (a `root_cause.mechanism_failure` value): written by the `verdict_interpreter` LLM stage — a soft judgment call, not a threshold. Do not confuse it with `kill_cost_hurdle`/`refine_cost_hurdle` (`determine_route`, `trading-bot/performance/signal_statistics.py`), a real mechanical threshold (`edge ÷ cost` vs. 2.0/0.5) computed from real, measured backtest data — see `protocol_result.yaml`'s post-backtest fields below.

**E-016 (fee-reduction autopsy field), not yet merged to master (branch `feat/e016-fee-reduction-autopsy`):** once landed, a cost-dominated kill (`kill_cost_hurdle`/`refine_cost_hurdle`) is meant to feed `root_cause.fee_reduction_assessment.candidate_system` — narrowed from an earlier 5-option infra-level enum to 4 timing-only options: `trade_less_often`, `combine_nearby_trades`, `exit_later`, `enter_earlier`. See `workflow_artifacts/skills/verdict-interpreter/SKILL.md`'s "IMPROVEMENT 10" for the selection rule, and `trade_diagnostics.json`'s `summary.fee_reduction_metrics` for the 8 supporting diagnostic metrics (2 per lever) it reads to pick between them.

**Stage output**

| What | Written where | Read by |
|---|---|---|
| `protocol_summary.json` → `protocol_result.yaml` | run dir → `artifacts/` | verdict_interpreter |
| `pass_rule_evaluation.yaml` | `artifacts/` | **verdict_interpreter — REQUIRED input, and the decision authority** — not written by the variant loop under `config_direct_authoring` AND `verdict_routing_retired` (C5.8), where nothing binding reads it |
| `grid_evaluation.yaml`, `idea_status.yaml` | `artifacts/` | **optional, E-046b S2 (2026-09-20) — only written when `orchestrator.grid_evaluation.enabled` is true (off by default) AND `pre_registration.yaml`'s pass_rule is menu-shaped (criteria carry `source`/`reducer` fields, `config/criterion_menu.yaml`). Additive: `evaluate_pass_rule_criteria`'s own call and `pass_rule_evaluation.yaml`'s write are unaffected either way. `idea_status.yaml` carries `validated`/`refuted`/`inconclusive` plus a `pass_rule_evaluation.yaml`-shaped `result`/`hypothesis_verdict`/`lineage_routing` triple. **CORRECTED 2026-09-28** (re-verified directly against `run_phase1_research.py`): the claim that it is "NOT yet read by any routing call site" is stale — `determine_post_specialist_readers_route` (under `orchestrator.specialist_readers.enabled`) reads it via `_load_idea_status` and drives the whole post-backtest route from it (promote / kill / human-pause), and the DONE branch's decide-next step re-reads it the same way. It still does not override `verdict_interpreter`'s own (stage 11) narrative verdict when that stage runs — the two are separate routing paths, never merged.** |
| `trade_diagnostics.json` | run dir (or `variants/<id>/` under `orchestrator.variant_loop.enabled`), not `artifacts/` — **CORRECTED 2026-09-28**, `run_protocol.py`'s `--out-dir` argument | verdict_interpreter |
| a row in `campaign_state.trial_sharpes` | campaign root | DSR accounting |

**Features / logic in place**

**1. Run the walk-forward backtest.**
`run_protocol.py` with config, protocol and validation protocol
(`run_phase1_research.py::run_tool_worker`). Produces per-window metrics including
per-trade expectancy (A3.4). E-061 C1.3:
- A `--validation-protocol` that is passed is read, and the rule evaluator is
  dry-run on it with a small synthetic summary, before any window runs
  (`run_protocol.py::_load_validation_protocol`; it used to be opened only after
  every window had run). It is refused exactly when that would fail: a missing,
  unreadable (incl. not UTF-8), unparseable file, or one the evaluator raises on
  (e.g. run_003's `decision_rules: {approve: [...]}`, `approve_if_all_met: null`, an
  empty or non-mapping document) → exit **3** with `[run_protocol] NO DATA TOUCHED`
  opening the first line of stderr. A document the evaluator accepts — even with
  zero rules, like run_018's rules nested under `variants` — runs exactly as before.
  Measured on the 49 `runs/*/artifacts/validation_protocol.yaml` in this checkout: 45
  proceed, 4 are refused (run_003's shape; run_004–006 do not parse).
- The orchestrator records a refusal with **no trial row** only when all three hold:
  exit 3, the token opening stderr's first line (`tools/protocol_refusal.py`), and
  no window result written under the call's `--out-dir` by that call
  (`::_refused_before_any_backtest`). In the variant loop the refused variant is
  marked `not_tested` (reason: refused before any backtest) and the loop continues
  with the others; in the single-config branch the stage fails. Anything else is a
  real backtest failure and still records its `backtest_failed` row.
- `--diagnostics-only` (passed by the orchestrator only under config-direct, when
  there is no validation protocol): `hypothesis_verdict` is the diagnostics block —
  cost drag, gross PnL, forecast/return correlation, `below_floor_pct`, per-trade
  expectancy, … — with `verdict: null`, `criteria_results: []`, and
  `win_rate_vs_sharpe: "N/A (no rule set)"`
  (`run_protocol.py::diagnostics_only_hypothesis_verdict`, G14), so the category
  reports and the trial row keep their inputs. For the trial row this is a change:
  on master a config-direct run's variants recorded only a `backtest_failed` row
  (the missing `validation_protocol.yaml` made `run_protocol.py` exit 1 after every
  window ran); now each records a full `backtest` row. Compared with a row built
  from `hypothesis_verdict: null` (`below_floor_pct` 0, `expectancy_bps` None), a
  sparse strategy (more than 50% of windows under 5 trades) moves from
  `statistic_valid: sharpe` — or `neither` when `median_sharpe` is None — to
  `expectancy`, with the per-trade mean as `expectancy_bps`.
- With neither flag (a manual call, `composite_cache`), `hypothesis_verdict` stays
  `null`, byte-identical to before.

**2. C7 pass-rule evaluation — the machine verdict, and the decision authority.**
`verdict_criteria_evaluator.evaluate_pass_rule_criteria()` scores the summary
against the *pre-registered* `pass_rule` and writes
`pass_rule_evaluation.yaml` (`::run_tool_worker`). Since the K2 kernel (2026-07-13)
this **replaced** `evaluate_against_decision_rules` as the authority; that
function's output is informational only. `evaluator_version: 2` since C7-EXT
(2026-07-22) added the G1–G5 preconditions.
**R3 ruling:** a legacy (string-shaped or absent) `pass_rule` never raises — it
returns `legacy_not_evaluable` and the LLM's own judgment applies exactly as
before K2. Every pre-K2 run, including run_057's, is that legacy shape.
**C5.8 (C13, D-050):** under `config_direct_authoring` AND `verdict_routing_retired`
(`_promotion_retired_enabled`, the C5.6 condition) the variant loop does not write
this file at all (every binding reader of it is retired there; a stale one from an
earlier attempt is deleted), and `reports/profitability.yaml` drops
`verdict`/`verdict_reason` and the `post_backtest_route*` / `cost_dominated_real`
labels (`build_reports(legacy_verdict_retired=True)`), keeping every number. Trial
rows are unchanged; the single-run branch still writes the file.

**3. Every failure path still records the trial (H4-core, issue #28 / E-025).**
A backtest that touched market data has spent a look, whether or not it
finished. Three branches each call `_record_failed_backtest_trial` before
re-raising: non-zero exit (`::run_tool_worker`), missing `protocol_summary.json`
(`::run_tool_worker`), and — added later — the **post-success window** where the
subprocess exited 0 and wrote its summary but `json.load` or the pass-rule
evaluation then raised (`::run_tool_worker`). That third window previously left no
trial row while the data had already been spent, so N was under-counted.
Recording is wrapped so its own failure only logs; the original error is
re-raised unchanged.

**4. `metrics.json` → `protocol_summary.json`: one dict per window, hand-assembled, not generic.**
Trading-bot writes one `metrics.json` per individual backtest window (a
hypothesis is normally walk-forward tested across many windows). `run_protocol.py`
reads every window's `metrics.json` and copies specific keys into a per-window
`result_entry` dict, which becomes one row of `protocol_summary.json`'s
`"results"` list:

```python
result_entry = {
    "core":            core,                     # metrics.json's own "core" block, copied wholesale
    "per_regime":      m.get("per_regime", {}),
    "regime_validity": m.get("regime_validity", {}),
    "data_quality":    m.get("data_quality"),     # CUL-263 — see below
}
```

**This copy list is NOT generic** — a field that exists in `metrics.json` but
isn't named here is silently absent from `protocol_summary.json`, and therefore
never reaches `verdict_interpreter`, even though it was computed correctly.
This bit twice in one night (2026-09-04):

- Fields nested *inside* `metrics.json`'s `"core"` block (e.g. CUL-262's
  `forecast_return_corr_pvalue_block_adjusted`/`forecast_return_corr_n_eff`,
  CUL-264's `sigma_bar_bps`/`post_backtest_route`) ride along automatically,
  since `"core"` is copied whole.
- `"data_quality"` (CUL-261's gap-detection block) is a **top-level sibling**
  of `"core"` in `metrics.json`, not nested inside it — it was being computed,
  written, and then silently dropped here, never reaching `verdict_interpreter`.
  Fixed by CUL-263 (`fix/cul-263-trade-diagnostics-flow`), adding the one line
  above. `None` when a window ran with `gap_detection=False` (the gap rule is on
  by default for backtests since 2026-10-01), present as a key either way.

**Separately, at the cross-window pooling step** (`_build_extended_summary`,
same file), one further statistic is computed that cannot live in a single
window's `metrics.json` at all: A8.5.1a episode-blocked significance (CUL-265)
needs bars from *every* window for a symbol at once, so it is computed here —
imported directly from `episode_significance.py` (both files live in
`strategy-research`, so no port was needed, unlike CUL-262's Fisher-z) — and
written as `episode_blocked_significance_a851a`, alongside (never replacing)
`median_forecast_return_corr`.

**Anyone adding a new `metrics.json` field that needs to reach
`verdict_interpreter` must add it to `result_entry` explicitly, in this same
step.** `sigma_bar_bps`/`n_eff`/cost hurdle/route are defined in
`trading-bot/performance/signal_statistics.py`'s own docstrings (the
`signal_prescreen` stage that used to hold this glossary was removed, E-039
step 5) — see `determine_route`, `block_adjusted_pvalue`, and `cost_check`
there for what these fields mean.

**5. Pre-registration conformance gate — checked right after this stage.**
Once `protocol_result.yaml` is written, the orchestrator's routing dispatch
(`run_phase1_research.py::run_loop`, `protocol_execution` branch) runs
`_check_protocol_execution_conformance` against `pre_registration.yaml`'s
`machine_constraints`: it compares `protocol_result.yaml`'s `protocol_file`
against the pinned `protocol_ref` (bare-filename match), and — when
`significance_methodology: episode_blocked_a851a` is pre-registered — checks
every symbol in `episode_blocked_significance_by_symbol` against
`is_a851a_method()`. Any violation calls `_mark_trial_invalidated`
(`run_phase1_research.py::_mark_trial_invalidated`) and pauses the run
(`status="paused_for_human"`, `flags.conformance_violation: true`) rather
than letting an un-registered test reach a verdict.

<details>
<summary><strong>Notes, history and traps</strong> — measured counts, past incidents, and the reasons behind each guard. Open when you need the evidence; skip when you need the flow.</summary>

- The `pass_rule_evaluation.yaml` step is invisible in §3 — it has no artifact
  entry. See [E037-19](../engineering/roadmap/E-037/FINDINGS.md#e037-19).
- **E-018 (2026-09-13):** a verdict that contradicts `pass_rule_evaluation.yaml`
  no longer halts the pipeline. Before this date, any disagreement between
  verdict_interpreter's own restated verdict and this file's binding one was a
  blocking conformance violation (`human_pause`). It is now recorded as an
  informational flag only (`pipeline_state.yaml`'s
  `pass_rule_evaluation_disagreement`) — because routing itself no longer
  depends on the stage's restated copy being correct (see stage 11 below and
  [`verdict_interpretation.yaml`](#verdict_interpretationyaml)'s note).

</details>

---

#### Stage 9 — `regime_detector_validation`
**Engine:** Python tool (`tools/validate_regime_detector.py`)
**Not a registry stage.** It is a helper, `_ensure_regime_detector_report`
(`run_phase1_research.py::_ensure_regime_detector_report`), called from inside verdict_interpreter
handling (`::run_loop`, `::run_loop`).

**Objective.** Establish whether the regime detector is trustworthy enough for
its labels to be allowed to condition any metric.

> **What a regime gate is, and how a regime idea is judged.**
> A *regime gate* means a strategy only trades when the market is in a state it
> likes — trending, say — and sits out otherwise. To do that you need a
> **detector**: a rule that labels each bar with the current state.
>
> The detector built for this campaign (ER-based) was measured and **failed its
> own quality gate**: its labels change under a small parameter nudge, and it
> cannot hit the required activation band and stay stable at the same time. Its
> labels are therefore noise wearing a label, and gating on them would add
> noise rather than selectivity. That verdict came from one run and says nothing
> about whether gating improves a strategy, so it is no longer a veto, and the
> old rule that banned regime-gated hypotheses (A2.3) is deleted (D-052).
>
> **A regime-gated idea is allowed.** It carries its ungated version as its
> design variant: the same config with the regime detector's `rules` emptied
> (`"rules": []`) and `default_regime` set to the regime that holds the strategy,
> so every bar is in that regime. The value of the regime is judged by gated
> versus ungated, plus the roadmap's regime health checks.

**Design rationale.**
- A detector that flips label under a small parameter nudge produces
  regime-conditioned numbers that are noise wearing a label.
- It runs before the verdict, not after, so the verdict knows how much to trust
  any regime-split evidence.

**Stage input:** `candidate_strategy_config.json`; the existing
`regime_detector_report.yaml` if any.

**Stage output:** `regime_detector_report.yaml` — **at the campaign root, not
per run.** One file shared by every run.

**Features / logic in place**

**1. Freshness check — "stale" means older than 30 days.**
If the report exists and `evaluated_at` is under 30 days old, nothing runs
(`::_ensure_regime_detector_report`).

**2. ⚠️ It can silently do nothing.**
If `candidate_strategy_config.json` is missing, it prints a warning and
returns `None` (`::_ensure_regime_detector_report`). If the subprocess exits non-zero, it prints and
returns `None` (`::_ensure_regime_detector_report`). **Neither raises.** The verdict then proceeds
with no detector report and the only trace is stdout. This sits badly beside
the project's standing rule that anything feeding decisions raises on
degenerate inputs. See [E037-17](../engineering/roadmap/E-037/FINDINGS.md#e037-17).

**3. Computes the A2.2 gate metrics.**
Persistence, class-conditional sensitivity under ±10% perturbation, and
activation band.

---

#### Not a stage — `regime_auditor` (a human procedure)

> **This is not part of the pipeline.** It is kept here because the guide
> referred to it as stage 10 until 2026-08-31 and because the skill and its
> artifact are real. Nothing dispatches it: it is absent from `STAGE_CONFIGS`
> and `_SKILL_MAP`, and no code writes `regime_audit_decision.yaml`. What
> happens in practice is that the pipeline pauses and a person runs the skill
> by hand. Merging its judgment into
> [stage 9](#stage-9--regime_detector_validation) — which already computes the
> metrics it judges — is proposed as its own epic. See
> [E037-16](../engineering/roadmap/E-037/FINDINGS.md#e037-16).

**Engine:** Human, invoking a skill.
**Runs:** only when the pipeline pauses on
`root_cause.mechanism_failure == regime_misattribution`.

**Objective.** Decide whether the detector is trustworthy, needs a retune, or
is unusable — and do so without letting profitability leak into the judgment.

**Design rationale.**
- If a detector could be retuned until the PnL looked good, it would stop being
  an instrument and become a fitted parameter. The firewall is what keeps
  detector quality and strategy quality separate questions.

**⚠️ Status — read this before relying on the stage.**
**In plain terms: the program that runs the pipeline has no way to reach this
stage.** Two lists control that, and it is in neither —
`STAGE_CONFIGS`, the stages the orchestrator knows how to run, and `_SKILL_MAP`,
the stages it can hand to an LLM. A stage missing from the second cannot be
dispatched even if something tried: `_build_stage_prompt` raises `ValueError`
rather than guessing which instructions to use (`::_build_stage_prompt`). **No code writes
`regime_audit_decision.yaml`** — the orchestrator only reads it if it already
exists (`::run_loop`, `::run_loop`); it is written only by a human running the
regime-auditor skill by hand, including its `ungated_escape_eligible` field.
What happens in practice is a pause (`status="paused_for_human"`)
printing *"consult regime-auditor skill and regime_detector_report.yaml"*
(`::determine_post_verdict_route`). See [E037-16](../engineering/roadmap/E-037/FINDINGS.md#e037-16).

**Stage input:** `regime_detector_report.yaml` (campaign root).

**Stage output:** `regime_audit_decision.yaml`, written by a human running the
skill.

**Features / logic in place**

**1. A2.2 retune firewall — enforced in code, and it raises.**
`_validate_retune_firewall` (`::_validate_retune_firewall`) scans `recommended_action` for
`pnl`, `sharpe`, `ic`, `backtest`, `cost_drag`, `forecast_return_corr`,
`per_trade`, `expectancy`. Any hit raises `RuntimeError` and halts the run
(`::run_loop`). Unlike the diversity check, **this one is real.**

**2. The decision is injected into the verdict handoff.**
`_inject_regime_context_into_handoff` passes the report and the audit decision
into `protocol_to_verdict_interpreter.yaml` (`::run_loop`).

---

#### Stage 11 — `verdict_interpreter`
**Engine:** Claude (skill `verdict-interpreter`)
**Runs:** after the backtest. `default_next: dynamic_routing`.

**Objective.** Decide what the result means and what to do next — and at what
size of change.

**Design rationale.**
- Separating *what happened* (stage 8) from *what it means* keeps the
  measurement honest and the interpretation auditable.
- The altitude system exists so a failure produces a proportionate response:
  a bad parameter should not kill a family, and a dead family should not be
  refined forever.

**Stage input:** `protocol_result.yaml`, `pass_rule_evaluation.yaml`
(**required**), `trade_diagnostics.json`, `regime_detector_report.yaml` and
`regime_audit_decision.yaml` if present. (CUL-336: these reach the prompt
through `_apply_closed_book_inputs` — before it no handoff listed them at a path
that resolves, and the agent could only have opened them itself:
`pass_rule_evaluation.yaml`, required once `protocol_result.yaml` records a
completed backtest, optional otherwise; `config/coin_universe.yaml` and
`quant-fundamentals/SKILL.md`, required; `campaign_record/campaign_state.yaml`,
optional; and `artifacts/trade_diagnostics_summary.yaml`, the `summary` block
of this run's `trade_diagnostics.json`, written by code — the per-trade list
(up to ~480 KB) is not given. `innovation_notes.yaml` is still not an input of
this stage.) `post_backtest_routes` (CUL-264) is
injected directly into this stage's own handoff — not a separate file — when a real
backtest produced measured trade/window data; see item 7 below.
`config/coin_universe.yaml` and `innovation_notes.yaml`, if available, feed
the asset-stability gate (E-026, 2026-09-12 — see item 8). `near_miss_scoreboard.yaml`
(E-018, 2026-09-13 — see item 9) is given as an optional input, whether or not
this run has a registered `pass_rule`. `grid_evaluation.yaml`/`idea_status.yaml`
(E-046b S2, 2026-09-20 — see stage 8's own output table) are optional inputs,
present only when `orchestrator.grid_evaluation.enabled` is on and this run's
pass_rule is menu-shaped; not yet wired to override this stage's own
verdict — see `verdict_criteria_evaluator.py::evaluate_grid`'s docstring for
why `idea_status.yaml`'s routing isn't binding yet.

**Stage output:** `verdict_interpretation.yaml`; possibly `proposed_brief.yaml`,
`escalation_request.yaml`, `findings_carryover.yaml`, `promotion_audit.yaml`.

**Features / logic in place**

**1. Engineering failure is immune to everything downstream.**
Checked **before** any circuit-breaker logic: if
`root_cause.mechanism_failure == component_execution_error`, the run pauses for
a human (`::determine_post_verdict_route`). No trial slot, no parameter-dimension slot, no family
marked failed. F6 (2026-07-04) — a component bug is not a research finding.

**2. Regime misattribution pauses rather than routes.**
`mechanism_failure == regime_misattribution` pauses for the regime-auditor
(`::determine_post_verdict_route`) — see stage 10 for what that actually means.

**3. [Circuit breaker](#g-circuit-breaker) — anti-loop protection, scoped per family.**
`_apply_circuit_breaker` (`::_apply_circuit_breaker`) can force `refine` up to `pivot` when the
same parameter dimension keeps recurring. **Scoped per [hypothesis family](#g-hypothesis-family) since
F6 (2026-07-04)**: a global list let stale dimensions from the long-closed
Keltner/RSI families force run_044's first-ever refine straight to pivot.

**4. Five named diagnostic rules.**
The verdict is reached by applying five *named* rules rather than free
judgment, so two runs with the same evidence reach the same altitude. The names
appear in `altitude_justification` (run_060's reads *"Rule 2 (weak signal)"*),
which is what makes a verdict auditable after the fact.

**5. The altitude ladder is numbered — but only in prose.**
§2.1's map labelled the three non-terminal outcomes `alt 1` (refine), `alt 2`
(pivot) and `alt 3` (escalate), matching the numbering §3 once ascribed to an
`altitude` field. **No real artifact carries that field** — measured 0 of 39,
see [E037-22](../engineering/roadmap/E-037/FINDINGS.md#e037-22). The ladder is real and
the ordering is meaningful; the numeric field was intended and never built.
What the artifact carries is `status`.

**6. [Promote](#g-promote) is provisional.**
A pass writes `promotion_audit.yaml` and routes to `holdout_evaluation`
(`::_dispatch_verdict_route`); it is not a promotion.

**7. Post-backtest route is injected as context, never a gate (CUL-264).**
`_inject_post_backtest_route_into_handoff` (`::run_loop`) surfaces each
window's real, measured `post_backtest_route`/`post_backtest_route_real`
(computed by `signal_statistics.py::determine_route`/`cost_check` from
actual trade/correlation data, not an estimate) into
`post_backtest_routes` on this stage's own handoff, alongside a constraint
telling the model to treat it as supporting evidence — same as
`forecast_return_corr` — never as a binding verdict the way
`pass_rule_evaluation.yaml` is. No-ops cleanly when `protocol_result.yaml`
is absent or no window carries a route (a pre-CUL-264 run). This is the
signal-quality go/no-go for the pipeline: a real, measured check on the
actual backtest data rather than an early statistical guess.

**8. Asset stability gate — mandatory before `promote` (E-026, 2026-09-12).**
A strategy tested on only one symbol, or on symbols from only one
`config/coin_universe.yaml` category, has not shown a real edge — it has
fit one series of numbers. Before recommending `promote`, the skill checks
how many distinct symbols/categories the protocol actually covered; fewer
than 2 categories routes to `refine` instead, citing the gap explicitly.
This does not add a second decision authority — it plugs into the same K2
disagreement/`human_pause` mechanism already described above. Motivated by
Dorian's H003: a strategy's edge *collapsed*, rather than improved, as the
tested coin universe grew, consistent with correlated alts trading as
leveraged BTC beta rather than independent bets.

**9. Near-miss scoreboard — informs the write-up, never the verdict (E-018,
2026-09-13).** `near_miss_scoreboard.yaml` (`tools/near_miss_scoreboard.py`,
a ranked table of past runs' near-miss root causes) is given to this stage
unconditionally — deliberately with no guard tied to whether *this* run has
a registered `pass_rule`. It may inform `root_cause`/`proposed_brief`/
`findings_carryover` (e.g. citing a repeated near-miss pattern), but must
never touch `hypothesis_verdict`/`lineage_routing` — those come from
`pass_rule_evaluation.yaml` directly when binding (item above), or from the
five diagnostic rules when not. This is what makes giving the scoreboard to
this stage safe at all: on a run with a binding pass rule, the stage is no
longer the actual promote/kill decision-maker, so seeing "how close other
runs got" cannot soften that decision. The static test that previously
enforced zero promotion-code access to the scoreboard
(`tests/test_near_miss_scoreboard_firewall.py`) was removed the same day,
by operator decision, once this stage became a reviewed, named exception to
it — the firewall is now verified by inspection of the routing functions,
not by a standing test.

---

#### Stage 16 — `specialist_readers`
**Engine:** Claude — five skills, one call each, in order
(`workflow_artifacts/skills/readers/<category>-reader/`, categories from
`tools/build_reports.py::REPORT_CATEGORIES`).
**Runs:** after `protocol_execution`, only when
`orchestrator.specialist_readers.enabled` is on (off by default; requires
`grid_evaluation` and `category_reports` on too, or the run fails at start).
`default_next: dynamic_routing`.

**Objective.** Turn each category report into concrete, evidence-cited
proposals for what to try next — without deciding anything about this idea.

**Design rationale.** An idea's status is the grid's job (`idea_status.yaml`,
mechanical). Readers only propose; their scores rank the next candidate in the
later decide-next step (delivery_plan_v26.md slice 6b). Keeping them out of the
route means an LLM can never soften or harden a verdict.

**Stage input (per reader):** `artifacts/reports/<category>.yaml`,
`artifacts/grid_evaluation.yaml`, and (D-063) what was claimed and what really
exists: `artifacts/hypothesis_card.yaml`, this run's base config (the base
variant's `strategy_config.json`, else `candidate_strategy_config.json`),
`docs/COMPONENT_CATALOG.md` and `docs/STRATEGY_DESIGN_GUIDE.md` (the two docs
step 2 gets), `artifacts/block_manifest.yaml` when present, then
`artifacts/registry_summary.yaml`. Nothing else (no pre-registration, no other
category's report, no regime-audit decision).

**Stage output:** `artifacts/proposals/<category>.yaml` × 5 (a YAML list, `[]`
for none), each validated by `tools/reader_proposals.py::load_proposals`; a
malformed file stops the run. A proposal's fields
(`workflow_artifacts/schemas/proposal.schema.json`): `proposal_id`
(`<category>-<run_id>-<n>`), `kind` (`patch` | `new_block`), `patch` or
`block`, `evidence`, `scores` (three 0-3 anchors), `model_id`,
`rubric_version`, and the optional `requires_feed: {feed, reason}` (E-035
S2c, item 7). Plus, only when some proposal carries `requires_feed` for a
feed that is not wired, one row per such feed in
`campaign_record/data_requests.yaml`.

**Features / logic in place**

1. **Explicit output path, validated before it lands.** `run_reader_worker`
   validates each reader's single fenced YAML block for its category, then
   moves it into `proposals/<category>.yaml` (temp file + `os.replace`);
   `run_claude_worker`'s shared filename regex is not used or changed. An
   invalid output gets one retry with the error in the prompt. After a second
   failure the raw answer is saved as
   `debug_specialist_readers_<category>_raw_output.txt`, and the run does
   **not** stop (D-061, CUL-380). Each proposal is re-validated on its own;
   the valid ones go to the final path, and the invalid ones are dropped and
   listed with their error in the audit log (`dropped_proposals`). An invalid
   proposal never reaches the final path. A `new_block`'s `block` is exactly
   `{kind: forecast|regime, config_paths, scaffolding (optional), rationale}`.
   `rationale` is required: it becomes the next idea's research goal if
   decide-next picks the proposal.
2. **Retune firewall** (`_validate_retune_firewall`) runs at stage entry,
   before any reader call (and on every resume).
3. **Everything comes from this attempt.** Under the flag `protocol_execution`
   deletes `idea_status.yaml`, `grid_evaluation.yaml`, `reports/` and
   `proposals/` on entry, builds the reports from this run's own output only
   (CUL-381: never the campaign-level `regime_detector_report.yaml`), and
   fails (after its trial rows are recorded) if the grid or the reports
   cannot be produced. `run_loop` also refuses to start
   a flag-on run whose `pre_registration.yaml` pass_rule is not menu-shaped.
   A token budget exceeded between readers ends the run as
   `rejected_budget_exceeded`, like the loop-top check.
4. **Route from the grid only** (`::determine_post_specialist_readers_route`):
   any `results[*].component_errors.count > 0` in `protocol_result.yaml` →
   human pause `component_execution_error` (readers are not run); then
   `idea_status.yaml`: `validated` → promote (holdout path, unchanged),
   `refuted` → kill/terminate, `inconclusive` → human pause
   `inconclusive_grid`. Missing or malformed `idea_status.yaml` fails the run.
   No refine/pivot/escalate and no circuit breaker under this flag; a kill
   records the run and its diagnostics only (no `altitude_history`, family
   or `continuation_*` bookkeeping).
5. **Stage 11 is unreached, not deleted.** Its registry entry and code stay
   for flag-off runs; `verdict_interpretation.yaml` is never written under the
   flag. Its readers are listed in
   `engineering/roadmap/E-046a/S2_5B_II_B_CALLERS.md`.
6. **With stage 17 on**, the route in item 4 runs after `regroup_record`
   instead of here (same function, same result).
7. **Feed requests** (E-035 S2c, delivery_plan_v26.md slice 8.2; no flag of
   its own). A proposal of either `kind` may carry `requires_feed: {feed,
   reason}` when its report shows the missing data would plausibly change the
   result: `feed` is a lowercase snake_case name as a strategy config's
   `aux_feeds` would name it, `reason` a non-empty string; any other shape
   stops the run. One vocabulary: each reader's handoff carries
   `injected_context.feed_names` (`run_phase1_research._reader_feed_vocabulary`)
   -- `wired` (`FEED_REGISTRY` keys), `reserved` (`RESERVED_FEED_REGISTRY`
   keys) and `wishlist_only` (`campaign_record/feed_wishlist.yaml` names in
   neither) -- and its SKILL.md tells it to use a listed name, never a
   synonym. An unreadable registry or wishlist is reported in that block,
   never raised. After the proposals validate, `_route_reader_feed_requests`
   reads the feed registry (only if some proposal carries the field; then an
   unreadable registry stops the run) and appends ONE row per feed asked for
   that is not wired to `campaign_record/data_requests.yaml`:
   `{run_id, stage: specialist_reader, feed, request, proposals: [{category,
   proposal_id, reason}], reason}`, where `request` is `acquisition` (never
   built; reason `requires_feed:<feed> -- ...`) or `designation` (a reserved
   feed, which needs a `campaign_data_policy.yaml` designation; reason
   `requires_feed_reserved:<feed> -- ...`). A wired feed gets no row. Rows are
   keyed on (run, stage, feed) (`campaign_review_retired.feed_request_key`),
   so a resume, or a re-attempt that asks for the same feed in other words or
   under another proposal id, adds nothing. It changes no status, route or
   queue entry: decide-next gates the candidate (§5 `run_campaign.py`).
8. **Readers v3** (E-068 slice 5, D-073, `orchestrator.reader_findings.enabled`,
   off by default; requires `claim_tests` and `specialist_readers`). Off, items
   1-7 are exactly as above. On:
   - **SKILLs:** `workflow_artifacts/skills/readers_v3/<category>-reader/SKILL.md`
     (one focus each, under 3 KB) plus the shared
     `readers_v3/READING_CONTRACT.md`. The v2 SKILLs are untouched.
   - **Inputs:** the same report, grid, card, base config, catalogue and registry
     summary; `hypothesis-design/CLAIM_TESTS.md` instead of the design guide; and,
     written by code before the first reader, `artifacts/claim_result_digest.yaml`
     (the claim's tests and each variant's effect sizes from its
     `claim_test.yaml`, numbers only when measured on this attempt's bars, else
     `stale`; and, CUL-410, `variant_patches`: each variant's id, kind, symbol
     and exact patch from `variant_patches.yaml`, so a reader never infers a
     variant's settings from its name) and `artifacts/findings_summary_for_readers.yaml` (earlier runs'
     findings from the campaign memory, this run left out, newest 10, compact);
     `claim_measurement.yaml` when it exists (an older run's `claim_status.yaml`,
     its name before D-077). The digest labels every number with its statistic
     (`statistic_label`, e.g. rank IC (Spearman) vs a difference of means;
     CUL-413), and with this flag on the forecast_power report carries
     `statistic_labels` (its `forecast_return_corr` is a Pearson correlation of
     the forecast with the next bar's return on active bars). If either
     code-written file cannot be
     written (e.g. an OSError), the stage does not stop: the error is printed and
     listed in `artifacts/reader_input_gaps.yaml`, an older copy is removed when
     possible (a file named there counts as missing even if it is still on disk),
     and the readers run without that file: their handoff names it as missing and
     each reading's audit entry keeps it as `missing_inputs`.
   - **Skip rules (no model call):** `regime_power` when `block_manifest.yaml`
     lists `/regime_detector` as scaffolding or the base config's detector has no
     components and no rules; `component_attribution` when every graded variant
     has at most one component. The proposals file is then a `skipped` reading
     with the rule (never `[]`); the memory entry's proposals block carries
     `skipped`; `campaign_record/reader_skips.yaml` counts it and the campaign
     summary shows "Readers skipped by a code rule". An answer refused after its
     retry is recorded the same way (rule `output_refused_after_retry`), as is a
     reader whose E-072 exploration copies are missing (rule
     `exploration_inputs_unavailable`, item 9).
   - **Output:** `proposals/<category>.yaml` is ONE mapping: `schema_version: 3`,
     `reading_id`, `model_id`, `rubric_version: <category>-reading-v1`,
     `explanation`, `evidence`, `side_findings` (0-2, each a full claim block plus
     evidence and scores, optionally with `config_change`: the
     `[{component_id, field, before, after}]` change to test the claim with).
     No verdict field. **One proposal kind (D-078):** the stand-alone `patch` is
     removed from what a reader writes; a reading carrying one is refused with a
     message naming `config_change` (salvage drops it). A LEGACY reading with a
     `patch` still loads and flattens as before. Where it is
     written, code checks each side finding with `claim_card.check_claim`,
     resolves its `config_change` against the base config
     (`decide_next.resolve_patch`) and refuses a change under a scaffolding path;
     a refusal gets the one retry, then each item is kept or dropped on its own. Warnings only, in the audit
     log (`reading_review`): a test whose `spec_hash` is already in the findings
     or is this run's own claim test; a block-kind claim whose tests cannot see
     the block. `tests: none` adds a `test_requests.yaml` row. v2 list files and
     v3 readings load side by side (`load_proposals` flattens a reading into
     items). The v3 shape is enforced in code (`reader_proposals.check_reading`);
     `proposal.schema.json` describes v2 only.
   - **Decide-next:** two side findings with the same tests collapse inside ONE
     decision only. The twin left in `collapsed_sources` is not in the queue, so
     a later decision can offer it again; once the first one's finding is
     recorded it carries a `repeats_measured_spec` warning (repeats warn, never
     refuse, by decision; with approval mode on, the operator sees it).
   - **The start config (CUL-412, D-078):** a side finding starts from the
     source run's base config and block manifest (its `config_change` applied,
     when it has one). Decide-next marks it INFEASIBLE when they are not on disk
     or the change does not resolve; a change gets a novelty key like a patch
     (NOVEL / REPEAT), an unchanged start is `NOT_APPLICABLE` ("a new claim on
     it"); same tests collapse only on the same config. The brief carries
     `candidate.start_config` / `start_manifest` (never `config` / `manifest`,
     which mark a pass-through) and `source.start_config_sha256`. Step 1b gets
     them as `artifacts/start_config.json` / `start_block_manifest.yaml` plus
     `START_FROM_CONFIG.md`; after 1b's manifest is accepted, every difference
     between what 1b built and the start (config leaves, the manifest's block or
     scaffolding) is a structured deviation in `artifacts/deviations.yaml`
     (`source: code_diff_from_start_config`), listed by 1b or not. A composite
     source carries no start config.
9. **Exploration and confirmation windows** (E-072, D-080,
   `orchestrator.explore_confirm.enabled`, off by default; requires
   `reader_findings` and `variant_loop`). Off, items 1-8 are exactly as above.
   On (`tools/explore_confirm.py`; design and defaults in
   `engineering/roadmap/E-072/PHASE_A.md`):
   - **The split:** at protocol_execution entry, before any backtest,
     `artifacts/explore_confirm.yaml` records the run's protocol windows in
     time order, first half exploration, the rest confirmation (an odd count
     gives the extra window to confirmation). A re-run keeps the file. Nothing
     here stops a run: fewer than 2 windows records `status: not_applicable`
     and that run proceeds exactly as with the flag off; any other split
     failure is logged and the readers are skipped (next bullet).
   - **What the readers see:** only `artifacts/exploration/` copies of every
     input that carries a result -- the five reports (cut to the exploration
     windows; the pooled `overall` slices `withheld`), the grid (window criteria
     re-evaluated on those windows; pooled criteria and the idea status
     `withheld`), the claim digest (measured again on those windows), the
     earlier findings (numbers, `statement` and `reason` withheld) and the
     registry summary (numbers `withheld`), and a whitelisted card copy (the
     claim's statement/kind/tests and the signal spec; free text and numeric
     evidence left out) -- plus `readers_v3/EXPLORATION.md`;
     `claim_measurement.yaml` is not given. A split that cannot be read, or a
     missing report, grid, registry or card copy, skips that reader with the
     code rule `exploration_inputs_unavailable` (recorded in
     `reader_skips.yaml`; the run continues); a digest or findings copy that
     cannot be written is a recorded gap (item 8's rule). Never the all-window
     file instead. The run's own grid, idea status and routing are unchanged.
   - **Confirmation, after every reader:** each side finding's tests on the
     confirmation windows. A pure (price-only) finding is measured in this run
     on the base variant's bars; a forecast/regime block claim (or a finding
     whose `config_change` alters what its tests read) is `pending` until the
     run built from it (its brief's `candidate.source.proposal_ref`) measures
     its own claim on its own confirmation windows -- not when those overlap
     the windows the proposer saw. Result: `confirmation_sign_retained: true /
     false / pending` (true only when every test keeps the claimed sign at every
     horizon with a value; no events is false; `null` only when nothing could
     be measured), in `artifacts/confirmation.yaml` and
     `campaign_record/confirmations.yaml`. A resolution by the follow-up run is
     WEAK and marked so (`confirmation_basis: follow_up_run`,
     `proposer_exposure: step_1a_saw_all_window_knowledge_base`, `weak: true`):
     step 1a wrote that run's card after reading the all-window knowledge base.
     When its tests differ from the finding's, the result is `not_comparable`.
   - **Looks:** the ledger counts every look per confirmation set (tests and
     test x horizon comparisons; a resume never counts twice; a re-run replaces
     the run's own findings but its earlier looks stay counted) and the
     campaign summary shows "Side findings on unseen windows", with follow-up
     resolutions on their own line, never in the clean held / not-held counts.
     The bar is "the sign held on unseen windows, counted against the looks",
     never "proven"; the confirmation windows are within the reader model's
     training period, so "unseen" means unseen in this pipeline.
     Information only: nothing routes, stops, parks or ranks on it.

---

#### Stage 17 — `regroup_record`
**Engine:** Python tool (`workflow/run_phase1_research.py::_run_regroup_record_stage`,
writer `tools/campaign_memory.py`). No LLM call.
**Runs:** after `specialist_readers`, only when `orchestrator.regroup_record.enabled`
is on (off by default; requires `orchestrator.specialist_readers.enabled`, or the
run fails at start). `default_next: dynamic_routing`.

**Objective.** Write down what this run found, in one place that later steps
can read, before the grid's route is taken ("memory before decision", roadmap
card H; delivery_plan_v26.md slice 6a).

**Design rationale.** Under stage 16's flag, `campaign_state.runs` misses
promoted and paused runs, and the legacy KB writer is never reached. The
memory is the complete per-run list. It only records: the idea's status is
copied from the grid, and reader proposals are referenced, never scored.

**Stage input:** `artifacts/idea_status.yaml`, `artifacts/grid_evaluation.yaml`,
`artifacts/hypothesis_card.yaml`, `artifacts/protocol_result.yaml` (plus
`artifacts/variants/index.yaml` and each variant's `protocol_result.yaml`
under the variant loop, `artifacts/proposals/*.yaml`, and
`campaign_state.trial_sharpes`, read only).

**Stage output:** one entry in `campaign_record/campaign_memory.yaml`, keyed
by `run_id`. File shape: `schema_version: 1`, `legacy_note`, `runs: {<run_id>:
<entry>}` (`workflow_artifacts/schemas/campaign_memory.schema.json`, applied at
write time by `validate_workflow_artifact`: warn by default, blocking under
`WORKFLOW_ARTIFACT_VALIDATION=raise`). Full entry fields:

```yaml
run_id, hypothesis_id, legacy: false, recorded_at
idea_status            # validated|refuted|inconclusive, from idea_status.yaml
idea_status_reason, idea_status_ref
engineering_fault: null, engineering_fault_detail: []
grid: {ref, criteria, variants, cells: {<criterion>: {<variant>: {result, value, threshold, n_windows, n_trades}}},
       counts: {PASS, FAIL, INCONCLUSIVE}}
variants: {<id>: {status: tested|failed|not_tested, reason, config_ref,
                  forecast_hash,   # copied from the variant's trial_sharpes row; null when not_tested
                  symbols, n_windows,   # n_windows = distinct windows, not symbol x window rows
                  trial_id}}
trial_ids              # this run's backtest / backtest_failed rows in trial_sharpes (read only)
protocol_ref           # protocol_result.yaml's protocol_file
timeframe              # hypothesis_card.yaml (string or null; anything else raises)
proposals: [{category, ref, proposal_ids, count}]   # never scores
registry: {block_ids: [...]} | {skipped: no_manifest|not_validated}   # E-058 S2b, see item 8
profit_bars: null, profit_bars_reason: "not evaluated before regroup"
kb_entry_id: grid_<run_id> | null   # E-058 S2b, see item 9; null only when the KB file is absent
finding: {...}         # E-068 slice 4, only with orchestrator.claim_tests.enabled (D-072)
```

With `orchestrator.claim_tests.enabled` on, a full entry also carries
`finding` (`tools/claim_findings.py`), added after the registry and KB entry:
the claim's statement, kind and tests (with `spec_hash`), whether the tests
can see the block, the scope, the effect sizes per variant with their sign
counts, the trial ids and the source run (detail by reference to each
`claim_test.yaml`). Numbers are attached only when the measurement belongs to
the attempt the entry describes, otherwise `not_measured` / `stale`. The
stage then writes `artifacts/findings_summary.yaml` (every finding so far,
deterministic). Information only: an error is recorded (`status: error`) and
the stage continues; no prompt reads either yet.

**Claim tests show the number only (D-077).** With `orchestrator.claim_tests`
on, a claim's tests are checked (`tools/claim_card.py`), measured after the
backtests (`tools/claim_measure.py` -> `artifacts/claim_measurement.yaml`;
`claim_status.yaml` before D-077, still read for older runs) and recorded as
findings; nothing grades the claim. The grading path of `tools/claim_tests.py`
(its significance methods, its grading rule, the calibration gate with
`tools/claim_tests_calibration.py`, and its grading CLI) is **PARKED
(CUL-394)**: kept as code and tested, called by no run, reader or prompt. A few
internal field names keep the older word (`verdict_possible` in
`claim_check.yaml` / `claim_test_status.yaml`, the `claim_status` key inside
the measurement file); they are names only. The real pass/fail is unchanged:
the profit bars, the count of all attempts, and the holdout.

A run with component errors gets the fault-only form instead:
`{run_id, hypothesis_id (null if hypothesis_card.yaml is unreadable), legacy:
false, recorded_at, engineering_fault: component_execution_error,
engineering_fault_detail}`.

**Features / logic in place**

1. **Replaced on re-run.** A second pass for the same `run_id` replaces its
   entry; other entries are kept. The read-modify-write runs under an
   exclusive lock file (`campaign_record/.campaign_memory.lock`, the E-011
   `tools/campaign_lock.py` primitive) with a bounded 30 s wait, and is written
   atomically (temp file + `os.replace`). A malformed existing file, or a lock
   still held after the wait, stops the run; the file is not overwritten.
2. **Engineering faults are recorded, not judged.** If `protocol_result.yaml`
   (or a variant's copy) has component errors, only the fault-only entry is
   written; the run's grid, variants and proposals are not parsed. If even
   that write fails, the failure is logged loudly and the route still pauses
   as `component_execution_error` (stage 16).
3. **No trial rows, and the ledger must be complete.** `protocol_execution`
   already wrote them; this stage only reads them. A tested variant without its
   `backtest` row (or with no `forecast_hash` on it) stops the run. Any
   `index.yaml` status or entry key outside the known set also stops the run.
   Tested: the trial ledger is byte-identical before and after.
4. **No backfill.** Runs before this stage are not listed; the file's
   `legacy_note` points to `campaign_knowledge_base.yaml` for them.
5. **No retired fields.** No `hypothesis_family`, altitude, lineage routing or
   continuation field; the writer refuses an entry that carries one.
6. **Pause leaves `pending_stage: regroup_record`.** An inconclusive grid or a
   component error pauses from this stage's route; resuming re-runs the record
   (replacing the entry) and the route. A run left at `regroup_record` while the
   flag is off fails loudly.
7. **Not stopped by the loop-top token budget check.** It is a zero-cost tool
   stage that carries the route flag-off runs take in the readers' own
   iteration; the next stage is budget-checked as usual.
8. **Block registry (E-058 S2b, `tools/block_registry.py`).** A run whose
   grid is `validated`, with no engineering fault, AND with
   `artifacts/block_manifest.yaml` (`{block: {kind: forecast|regime,
   config_paths: [JSON pointers]}, scaffolding, rationale}`, checked by
   `tools/block_manifest.py` exactly as stage 6 checks it) appends one block to
   `campaign_record/block_registry.yaml` (`schema_version`, `revision`,
   `updated_at`, `blocks: [...]`; schema
   `workflow_artifacts/schemas/block_registry.schema.json`). A block holds
   `block_id` (`<hypothesis_id>:<run_id>`), `kind`, `config_fragment` (the
   pointers' values in the tested base config, whose sha256 must equal the
   base variant's trial `forecast_hash`), `regime_assignment`,
   `criteria_passed`, `variants_passed`, `numbers` (grid cells),
   `symbols_tested` (informational: a block is usable on any coin),
   `correlation_to_composite: null` and `residual_ic: null` (slice 7),
   `source_config_ref`, `source_config_sha256`, `validated_by_run`,
   `registered_at`. No manifest: nothing is registered, the memory says
   `registry: {skipped: no_manifest}` and a WARNING line is printed (only
   stage 15, under `orchestrator.config_direct_authoring`, writes the
   manifest).
   The file is append-only: a re-run that would register a different block,
   or no block, for a run that already registered one stops before the memory
   entry is replaced; a person decides. A component-error re-run writes its
   fault-only memory entry FIRST, then, if an earlier validated pass left a
   block or a grid KB entry, prints an error naming `block_registry.yaml` / the
   KB (never edited by code); the `component_execution_error` pause still
   fires. The base config is chosen exactly as `protocol_execution` chooses its
   base variant (`base`, else the first validated id in sorted order;
   `tools/json_pointer.py`, which also holds the JSON-pointer helpers both
   share). Same lock and atomic write as the memory.
9. **Grid KB entry (E-058 S2b, `tools/grid_kb_writer.py`).** Every non-fault
   run adds one entry `grid_<run_id>` to `campaign_knowledge_base.yaml`:
   `outcome: <idea_status>`, `legacy_schema: false`, and for validated/refuted
   `verdict_status: gated` + `pass_rule_evaluation_ref:
   runs/<id>/artifacts/idea_status.yaml` (which carries `result: PASS|FAIL`).
   It never merges into or closes another entry (a legacy entry with the same
   `hypothesis_id` is untouched, so the F09 reactivation closure is never
   reached); a re-run replaces only its own entry. Every finding is
   re-validated before the write (closed schema + provenance); a malformed KB
   stops the run. An absent KB file is skipped with a WARNING line, as the
   legacy writer does. Entries without `legacy_schema: false` are legacy. The
   legacy writer (`_write_kb_findings_entry`) skips grid entries when it looks
   up a `hypothesis_id`, and takes the same `.campaign_knowledge_base.lock`.
10. **Near-miss scoreboard (E-058 S2b).** After the memory is written the stage
   rebuilds `engineering/roadmap/E-018/artifacts/near_miss_scoreboard.{yaml,md}`
   (`tools/near_miss_scoreboard.py::build_scoreboard` + `write_scoreboard`;
   a run with `grid_evaluation.yaml` and no verdict file is tier `grid`,
   `legacy: false`, ranked by `idea_status`, near miss = each criterion's worst
   failing cell with the comparator frozen with the run; other rows are
   `legacy: true`; an unreadable run dir gets a `malformed` row). Nothing on the
   route reads it, and a scoreboard error is logged and never fails the stage.
   Each run therefore changes that tracked file.
11. **Campaign-review input (E-058 S2b).** Only with this flag on,
   `campaign_review`'s handoff gains `../../campaign_record/campaign_memory.yaml`
   as a required input (`_apply_regroup_record_context`) whose reason tells the
   model which fields to cite -- only when that file exists. The template and `SKILL.md` are unchanged, so
   the flag-off prompt is byte-identical.
12. **Route with verdict routing retired (E-059 S3, slice 6c S2a,
   `orchestrator.verdict_routing_retired.enabled`, off by default; requires
   `decide_next` and `profit_bars_every_backtest`, else every run fails at
   start).** The route after this stage becomes: component errors → pause
   (unchanged); the `profit_bars_reached` stop (unchanged); else
   `completed_<idea_status>` (`completed_validated` / `completed_refuted` /
   `completed_inconclusive`, `status: completed`). Inconclusive no longer
   pauses. `_dispatch_verdict_route` and every function it fed are never
   called; no child run is scaffolded and no `continuation_child` written;
   `promotion_audit.yaml` is not written and nothing routes to
   `holdout_evaluation` except the operator's `spend` (item 14). Any other run found there pauses as
   `holdout_refused_under_retired_routing`, unless its holdout was already
   spent by hand (`holdout_result.yaml` present): then only the
   `holdout_consumed_by` record runs and the run ends. Campaign review runs
   only through the memory-count trigger of item 13 (slice 6c S2b); any other
   run found at `campaign_review` (a legacy review) pauses as
   `campaign_review_refused_under_retired_routing` before its LLM call. The run is still appended to
   `campaign_state.runs`, with one `diagnostics_log` row per run. A resume
   after the `profit_bars_reached` stop is decided by the operator's
   `holdout_decision.yaml` (item 14): `continue` ends the run the same way. The queue
   runner halts on a legacy continuation
   (`legacy_continuation_under_retired_routing`, also before `run_loop` when
   the current run was minted by legacy routing), on an unconsumed
   `refinement_brief_path` (`refinement_brief_under_retired_routing`), and at
   DONE on a missing, unreadable or mismatched `idea_status.yaml`
   (`idea_status_missing_at_done`); RUNBOOK §3.
13. **Campaign review with verdict routing retired (E-059 S3, slice 6c S2b,
   same flag).** After item 12's route has produced `completed_<idea_status>`,
   `_retired_review_trigger` counts the entries of
   `campaign_record/campaign_memory.yaml` without an `engineering_fault` that no
   COMPLETED review has covered yet (`campaign_record/campaign_review_log.yaml`,
   append-only); when that count reaches `campaign_state.yaml`'s
   `review_every_n_runs` (6), the run goes to stage 12 instead
   (`pipeline_state.yaml` records the trigger, with the counted runs, under
   `campaign_review_trigger`). Only a completed review resets the count, so a
   review lost to a budget stop, a pause, a crash or a late flag switch is due
   again on the next run, and no run is ever counted twice. The legacy trigger
   (`failed_families`, which never changes again and already holds 9 distinct
   families, so it would fire after every run) is never evaluated. The review
   gets its own handoff: a code-written digest of the memory
   (`artifacts/campaign_review_digest.yaml`: the runs since the last completed
   review in full, counts for the earlier ones), the run's
   `research_brief.yaml`, and the KB as an OPTIONAL input (absent: its reason
   says so); never the whole memory, `campaign_state.yaml` or
   `verdict_interpretation.yaml`. With the flag still on, the note
   `workflow_artifacts/skills/campaign-review/RETIRED_ROUTING.md` is added as
   a required input (`_apply_retired_routing_review_context`; `SKILL.md` and
   the legacy template are unchanged, so the flag-off prompt is
   byte-identical). A triggered review resumed with the flag off fails loud.
   Its route (`_route_retired_campaign_review`, the first line of
   `determine_post_campaign_review_route` under the flag):
   `continue` / `escalate_instrument` / `escalate_component` are recorded,
   not routed (`escalate_component` appends its rationale to
   `campaign_record/component_requests.yaml`, through the locked writer shared
   with `backtest_specification`); `reframe` writes
   `campaign_record/candidate_briefs/<run_id>__reframe.md` with
   `criteria_from: hypothesis_generation` (criteria fitted at step 1a from the
   menu, as for a decide-next candidate) and the source run's protocol pin,
   which the queue runner registers as a `ready` entry (`origin:
   campaign_review`, `priority: 999`) before decide-next runs (the A5.4
   KB-reactivation check still comes first; a registration that cannot happen
   halts as `campaign_review_reframe_unregistered`); `terminate` appends to the
   `campaign_decision.yaml` history and stops the campaign as the
   `campaign_review_terminate` pause (an operator's continue-anyway resume
   appends an `override_continue` event). Every ending is
   `completed_<idea_status>`, re-read from `idea_status.yaml`: the review
   never changes an idea's status and never picks the next run. RUNBOOK §3.
14. **The holdout unlock with verdict routing retired (E-059 S3, slice 6c S2d,
   same flag).** Operator decision of 2026-09-25: the holdout is reached ONLY
   through branch 3. A backtest passes every profit bar, the
   `profit_bars_reached` stop fires, and the operator resumes with
   `runs/<run_id>/artifacts/holdout_decision.yaml`. The grid's `idea_status`
   is neither a precondition nor a route. A `validated` idea never reaches the
   holdout by itself, and a refuted or inconclusive idea whose variant passed
   may be spent on. The file has a closed schema: `decision` (`spend` or
   `continue`), `run_id`, `profit_bars_stop_evaluation` (the stop it answers,
   from `pipeline_state.yaml`), `variant_id` (a passing backtest; required for
   `spend`), `trial_ledgers_merged` (`true`, required for `spend`),
   `ratified_by`, `ratified_at`, and an optional `note`. After
   `regroup_record` and the stop route, `_holdout_unlock_route` reads it:
   - `continue` records the choice (`pipeline_state.yaml` →
     `holdout_decision_record`), leaves the holdout untouched, and ends the run
     `completed_<idea_status>`, so decide-next runs;
   - `spend` goes to `holdout_evaluation` for the named variant, with the
     single-use check and the research_only hold. It is refused unless
     `trial_ledgers_merged: true` is attested, this run's evaluation records
     PASS for that variant under the bars file in place now (whole-file
     sha256), the variant's deflated Sharpe still clears the bar on the
     current trial ledger, the hypothesis (from `hypothesis_card.yaml` only) is
     not in `holdout_consumed_by`, and no other run or writer holds an
     unfinished spend of the one physical seal. Bars ratification is the
     operator's manual check, not enforced in code. The run pauses for the
     manual backtest (`holdout_unlocked_awaiting_result`). Once
     `holdout_result.yaml` exists, the spend is recorded first (a per-run
     intent, `holdout_consume_record`, then the marker if absent), so a crash
     never writes it twice or skips it. Only then is the ending decided: a
     result not bound to the unlock (`variant_id`, `trial_id`,
     `decision_sha256`) or rewritten after the record pauses; otherwise the run
     ends `completed_promoted` or `completed_rejected`, and decide-next runs.
     A result with no valid unlock is recorded and pauses as
     `holdout_spent_without_unlock`, never promoted.
   A missing, malformed, wrong-run, stale or otherwise refused file pauses as
   `holdout_unlock_refused` (the code is in `holdout_unlock_refusal`), and
   `--resume` refuses it first. Every other path to the holdout is refused as
   `holdout_refused_under_retired_routing`. RUNBOOK §3 has the procedure and
   one row per refusal code.
15. **Profit bars v2: whole-test bars (E-062, D-034..D-047,
   `orchestrator.profit_bars_v2.enabled`, off by default; requires
   `profit_bars_every_backtest`).** Same bars file, same seven bar names, but a
   variant is judged on its whole test at once rather than window by window.
   Flag off, nothing below applies and the earlier definitions run
   byte-identically. Each evaluation records `bars_definitions: v2`, and every
   row records its `basis` and `comparator`. Operator decisions behind it:
   - **One curve for the whole test (D-034, D-035, D-036).** Each window's
     equal-weight curve is chained, in window order, into one. Sharpe, average
     daily return and maximum drawdown are read off that one curve (drawdown on
     bars, the worst fall over the whole test, not the worst window). Trade
     count is per coin over the whole test, not counting the forced close at
     each window's end. Two bars are new: beat equal-weight buy-and-hold after
     costs (D-037) and realised gross edge over cost above 2.2, i.e. it
     survives doubled costs (D-038). These numbers are unsigned until the
     operator signs the bars file (`engineering/roadmap/E-062/SIGNING_CHECKLIST.md`).
   - **The deflated-Sharpe bar (D-041, D-046).** One scoring mechanism for
     every strategy, fast or slow: the whole-test daily Sharpe is deflated by
     N, every counted trial in the campaign ledger (N never shrinks). K is how
     many of those trials carry a Sharpe on this same whole-test basis (a
     `whole_test` block on the ledger row, or an entry in the recompute overlay
     file). With fewer than `dsr_min_same_basis_trials` (10) such trials the
     luck benchmark is the pure-luck spread, `1/sqrt(T-1)` for T daily returns;
     from 10 on it is the spread of the K Sharpes themselves. A small K is
     never "not evaluable", so a variant never has to be run twice just to be
     graded. The threshold stays 0.95 but means something different under this
     formula, which is why the operator re-signs it. The evaluation's
     `dsr_basis` records `sharpe_basis`, `n_same_basis`, `min_same_basis` and
     `basis_overlay` (`present: false` when no recompute overlay exists).
   - **A coin with partial coverage (D-042, D-047).** An asset variant whose
     coin covers fewer than all the run protocol's windows (at least 60% of
     them, else it is not tested) is graded on its share `f` of the run's
     calendar days: trade minimum and the cost-ratio bar's trade floor become
     `max(ceil(100 * f), 60)`, and the drawdown limit becomes `20 * sqrt(f)`, so
     a shorter period can never pass more easily. The ratio 2.2, Sharpe, DSR,
     average return and buy-and-hold are unchanged. Such a variant's rows carry
     the threshold actually used and `detail.normalisation` (covered and full
     days, `f`, the base and floor, the formula); a full-coverage variant is
     graded exactly as before. Step 5a freezes the run protocol as
     `artifacts/variants/run_protocol.json` (its sha256 on every per-coin entry
     of `variants/index.yaml`); grading and the holdout `spend` read only that
     copy, and `spend` re-derives the thresholds and refuses if they differ
     (`bars_changed`) or cannot be re-derived (`normalisation_unverifiable`).
   - **The era rule (D-047, as amended in the S2b-3b review).** `sign_consistent_by_era`
     with fewer than two eras represented cannot fail, so it reads
     INCONCLUSIVE, on every variant including the base (most committed
     protocols are single-era). A single era whose median is exactly zero stays
     FAIL.
   - **A retest on wider coverage is a new trial (D-047).** A partial variant's
     repeat key and the DSR dedupe key both carry its own window fingerprint
     (`windows_sha256`). The same coin retested on the same coverage is a
     repeat (skipped, no trial); on wider coverage it is a new trial and N goes
     up by one. Full-coverage variants' keys are unchanged.
   Old trial rows have no `whole_test` block. D-046 (4) plans a recompute tool
   (S2b-2c: append-only overlay `campaign_record/trial_sharpe_basis_recompute.yaml`,
   dry run by default, writing it an operator step); **that tool is not in the
   repository yet**, so no overlay exists and those rows count in N but not in
   K.
16. **Score provenance (C5.7b, D-048, `orchestrator.score_provenance.enabled`,
   off by default; requires `specialist_readers`).** Flag off, nothing changes.
   On: (a) the `model_id` on reader proposals and brief-card scores is stamped
   by code from the model that actually answered, and the model's own claim is
   kept in the audit log's `provenance` block; a `mismatch` means the observed
   model differs from the one requested, is recorded and never stops the run;
   (b) a proposal's `rubric_version` must be exactly its category's
   `<category>-reader-v2` (pinned to the five SKILL files), and an unknown value
   is rejected through the reader's existing one-retry path; (c) each proposal's
   cited evidence paths are resolved against the files the reader was given and
   the resolved and unresolved counts are recorded (record only, nothing is
   rejected; enforcing it is decided after the first real reader output).
   **Turning it on adds a stop path:** a reader that writes a wrong
   `rubric_version` twice in a row fails the run, and a `proposals/` file left
   by an attempt made before the flag (a `-v1` rubric) fails a flag-on resume.

---

#### Stage 12 — `campaign_review`
**Engine:** Claude (skill `campaign-review`)
**Runs:** after 2+ hypothesis families have failed, or every 6 runs.
`default_next: dynamic_routing`.

**Objective.** Step back from the individual run and ask whether the campaign's
whole line of attack is still worth pursuing.

**Design rationale.**
- Per-run verdicts cannot see a pattern across runs. Without a periodic step
  back, a campaign can refine its way through a dozen runs of the same dead
  idea — which is the failure the epic's own log describes as "35 runs before
  anyone asked why the kills kept recurring."

**Stage input:** `campaign_state.yaml`, prior verdicts,
`campaign_knowledge_base.yaml`, and `quant-fundamentals/SKILL.md` (added by
code, CUL-336).

**Stage output:** `campaign_review.yaml`.

**Features / logic in place**

**1. Output YAML is validated before use, and re-run if malformed.**
The orchestrator parses it and re-invokes the agent if parsing fails — the LLM
often emits colons inside list items (`::run_loop`).

**2. Shares the circuit breaker with stage 11.**
`determine_post_campaign_review_route` (`::determine_post_campaign_review_route`) applies the identical
per-family breaker, deliberately, so both paths behave the same.

**Routes / outcomes:** continue · reframe (new brief) · escalate (new
instrument/timeframe) · terminate.

**Under `orchestrator.verdict_routing_retired.enabled`** (slice 6c S2b, off by
default) the trigger, the inputs and the routes above are replaced: see stage
17, item 13.

---

#### Stage 13 — `holdout_evaluation`
**Engine:** Python tool + human
**Runs:** only on a provisional promote. Failure is terminal.

**Objective.** Spend the one-shot holdout, and only when everything cheaper has
already been passed.

**Design rationale.**
- The holdout is single-use and terminal. Every gate before it exists to avoid
  spending it, so **the order of the gates is load-bearing** and the code says
  so explicitly.

**Stage input:** `promotion_audit.yaml`, `config/campaign_data_policy.yaml`,
`research_brief.yaml`, `holdout_result.yaml` (human-produced).

**Stage output:** updated `campaign_data_policy.yaml`
(`holdout_consumed_by`, `consumed_at`); terminal promote or kill.

**Features / logic in place** — *in execution order; the order is the design*
(`_route_holdout_evaluation`, `::_route_holdout_evaluation`).

**1. DSR gate — reject before the seal is touched.**
`passes_deflated_threshold is False` → `completed_rejected` (`::_route_holdout_evaluation`). The
deflated Sharpe ratio is **Bailey & López de Prado**'s correction: it lowers a
Sharpe according to how many things were tried, so the trial count and the
spread of trial Sharpes decide whether this result is distinguishable from the
best of many guesses.

**2. Single-use enforcement — a second attempt is mechanically refused.**
If `hypothesis_id` is already in `holdout_consumed_by`, refuse (`::_route_holdout_evaluation`). A6.1.

**2b. Tradability gate — silence is not a green light (E-015 S3).**
`brief.research_only is not False` → hold. **Affirmative check, not a negative
one:** measured 2026-08-18, **0 of 57 briefs** in the tree carry the key at
all, and only one of the three `research_brief.yaml` writers writes it, so a
negative check would protect nothing. Position is deliberate — below 1 and 2
because those are terminal rejects that never touch the seal, above 3 and 4
because those are the acts it exists to prevent. Safe to fail closed:
`holdout_consumed_by` is empty and no run has ever reached this gate.

**3. Pause for a human — the holdout backtest is run externally.**
If `holdout_result.yaml` is absent, pause.

**4. Mark consumed, then evaluate against a range fixed in advance.**
`consumed_at` is stamped, then `status` is read. The comparison is against
`holdout_result.yaml`'s **pre-registered `expected_range`**
(`{min_sharpe, max_sharpe, rationale}`), which must be written **before** the
holdout is run — otherwise "within expectations" is decided after seeing the
number. Failure is terminal.

<details>
<summary><strong>Notes, history and traps</strong> — measured counts, past incidents, and the reasons behind each guard. Open when you need the evidence; skip when you need the flow.</summary>

- The guide's §2.2 row names gates 1 and 2 only. Gates **2b** and **3** are
  not mentioned there, and 2b will refuse every brief that does not explicitly
  declare `research_only: false`.
- "Looking is spending": gate 2b sits *above* the step that tells a human to go
  run the holdout, not merely above the step that marks it consumed.

</details>

---

---

### 2.3 Decision Tree & Routing

#### After validation_gate

No separate `refinement_planner` stage any more (E-039 S4, 2026-09-12) — a
`refine` verdict's own response already carries `refinement_notes.yaml`, so
its `implementation_allowed` flag is checked immediately, in the same step:

| Validation status | Next stage |
|---|---|
| `approve` or `conditional_approve` | → backtest_specification |
| `refine`, `implementation_allowed: false`, refinement counter < max | → [human pause](#g-human-pause) (pipeline suspended, awaiting audit) |
| `refine`, `implementation_allowed` true (or absent), refinement counter < max | → innovation_expansion (refinement loop) |
| `refine` (counter exhausted) | → `completed_rejected` |
| `reject` | → `completed_rejected` |

#### After backtest_specification

| Config status | Next stage |
|---|---|
| `spec_ready` | → `data_availability_gate` by default (`orchestrator.data_availability_gate.enabled`, default true), else → protocol_execution directly if explicitly disabled |
| `component_gap` | → human pause (a new bot component must be built) |
| **anything else** | → human pause, **deliberately fail-closed**. `KNOWN_STATUSES` holds only the two above; an unrecognised value is not guessed at. A real run produced `validation_incomplete` and took this branch — see [E037-23](../engineering/roadmap/E-037/FINDINGS.md#e037-23). |

#### After verdict_interpreter — the Altitude System

> Under `orchestrator.verdict_routing_retired.enabled` (slice 6c S2a, off by
> default) nothing in this subsection, the circuit breakers below or "After
> campaign_review" is reached: the run ends `completed_<idea_status>` after
> stage 17 and decide-next picks the next run (§2.1's verdict-routing-retired
> variant). Campaign review's own flag route (slice 6c S2b) is stage 17, item 13.

The verdict interpreter assigns an **altitude** to each decision. Altitude measures how far from the original hypothesis the next step will move.

| Verdict | Altitude | Meaning | What changes next run |
|---|---|---|---|
| `refine` | 1 | Minor tweak | Same hypothesis family, same signal, adjust a parameter (threshold, lookback window) |
| `pivot` | 2 | New idea | New hypothesis family, same research question |
| `escalate` | 3 | New environment | Same methodology, different instrument or timeframe |
| `promote` | — | Provisional success | Strategy passes all backtest gates; routes to holdout_evaluation before terminal promotion |
| `kill` | — | Terminal failure | Strategy is dead; root cause archived in campaign memory |

#### Circuit Breakers (anti-loop protection)

> ⚠️ **This whole subsection was corrected on 2026-08-31** after being checked
> against the routing functions for the first time. It was missing the most
> frequently triggered breaker, misstated a second one's condition, and quoted a
> superseded budget constant at one fifth of the live value. See
> [E037-32](../engineering/roadmap/E-037/FINDINGS.md#e037-32).

The orchestrator detects search-space exhaustion and forces an altitude climb automatically:

| Trigger | Action |
|---|---|
| **`refine` when the parameter dimension repeats, or 2 dimensions are already tried for that family** | **Force pivot (altitude 2).** This is the first and most-triggered breaker and was missing from this table. Scoped **per hypothesis family** since F6 (2026-07-04) — a global scope once forced run_044's first-ever refine straight to pivot using dimensions left over from the long-closed Keltner/RSI families. |
| Same hypothesis family appears 2× in `failed_families` | Force [escalate (altitude 3)](#g-escalate). ⚠️ This row previously read "pivoted 2× with identical root cause"; the code counts family occurrences in `failed_families` and does **not** compare root causes. |
| Same instrument/timeframe escalated 2× with no improvement | Force terminate or campaign_review |
| Refinement budget exhausted (`max_refinements_after_validation`, default 2) | Reject hypothesis |
| Run token budget exceeded — **1,800,000 weighted units** by default (raised from 1,500,000 by D-071, 2026-10-04: run_070 used 1,212,255 weighted units = 80.8% of the old budget; 1.8M leaves about 30% headroom) | Halt run, preserve state. ⚠️ This row previously said "300,000 tokens". That is the **superseded** `token_budget_per_run`, which `campaign_config.yaml` marks *"no longer read by the loop"* (F4c, 2026-07-05). The live key is `token_budget_per_run_weighted_units`, read at runtime by `run_phase1_research.py::_load_token_budget` — **5× larger, and in weighted units rather than raw tokens**. |

#### After campaign_review

| Campaign decision | Next action |
|---|---|
| `continue` | Apply the verdict interpreter's original decision |
| `reframe` | Write a new research_brief with a different angle; spawn next run |
| `escalate_instrument` | Target a new symbol/timeframe; spawn next run |
| `escalate_component` | Identify missing bot component; human pause |
| `terminate` | Kill entire campaign; write research_decision |

#### After holdout_evaluation

| Holdout result | Next stage |
|---|---|
| DSR < 0.95 | → completed_rejected (terminal, before holdout runs) |
| Second attempt (already in holdout_consumed_by) | → completed_rejected (mechanically refused) |
| `holdout_result.yaml` absent | → human_pause (run holdout backtest first) |
| `status: pass` | → completed_promoted (terminal success) |
| `status: fail` | → completed_rejected (terminal — no further path) |
| `status: inconclusive` | → human_pause |

#### Composition mode (E-060 S3b, `orchestrator.composition_runs.enabled`, off by default)

Requires `decide_next`, `variant_loop`, `profit_bars_every_backtest` and
`verdict_routing_retired`. Nothing below runs with the flag off.

1. **R1 (decide-next).** When an exact bar size holds >= 2 registered forecast
   blocks whose set has not been composed, R1 picks `composition-<tf>-<hash>`:
   behind a run in progress and ready operator entries, ahead of every agent
   entry, candidate and R2. Once per registry state per timeframe; an
   inconclusive composite re-fires (`<id>-a<n>`) only when its deflated-Sharpe
   bar was missing for want of trials and the ledger now has them.
2. **Code-written variants** (`tools/composition.py`). `base` = equal weights;
   `vol_scaled` (1/σ of each block's stand-alone daily returns, from
   `tools/portfolio_daily.py`) and `ic_weighted` (residual IC) carry a per-window
   `weight_schedule` whose entry for a window is estimated only from data dated
   before that window starts (equal weights, recorded as `estimated: false`, when
   there is too little); the engine applies an entry from its date on. The
   manifest and `campaign_record/compositions.yaml` are written with them.
3. **The run.** Steps 1a (card, pass_rule = `profit_bars`), 1b (config and
   `artifacts/composition_manifest.yaml`, no `block_manifest.yaml`) and 2
   (`variant_patches.yaml`) are code, never an LLM call. 5a checks every variant
   against the manifest (`check_composition_config`: blocks present, gated and
   pinned as their source, scaffolding, weights and schedule). The grid grades
   `profit_bars` with branch 3's own grading (FAIL on a failed bar,
   INCONCLUSIVE on a NOT_EVALUABLE bar or an invalidated trial); branch 3
   labels the variants `composite`. A composite never registers as a block.
4. **7.5.** A reader patch on a composite is admitted only if it still passes
   the same manifest check, and runs as a composition too.
5. **Failures.** `docs/RUNBOOK.md` §3 `composition_failed`.

---

## 3. Artifacts

Artifacts are YAML files produced and consumed by pipeline stages. They are the only communication channel between stages — no stage reads another stage's raw LLM output.

> **Corrected 2026-08-27.** This paragraph previously ended *"All artifacts are
> validated against JSON schemas before the pipeline advances."* **That is
> false.** No schema under `workflow_artifacts/schemas/` is loaded by any code
> — verified by grep across `workflow/` and `tools/`, where the only hits are
> source comments. Measured consequence: `expanded_hypothesis_card.schema.json`
> declares `expanded_variants` as an array of *strings*, and 74 of the 138
> variants in the real corpus (53%) are dicts. A field a schema calls
> `required` is not actually required. Tracked as
> [CUL-11](https://linear.app/culito/issue/CUL-11) (Notion's bug board was
> retired in favor of Linear, 2026-09-02). Where enforcement genuinely exists it is written in
> CODE at the seam that reads the value (see `variant_selection.yaml` below).

Each [run](#g-run) stores its artifacts in `runs/{run_id}/artifacts/`. Campaign-level artifacts live at the root.

---

### `research_brief.yaml`


> **Why this file exists.** The question this run exists to answer, and the limits it must respect. Everything downstream is derived from it, so an unstated constraint here is unstated everywhere.

**Created by:** Human (or proposed_brief from previous run's verdict_interpreter)  
**Read by:** hypothesis_generation  
**[Schema](#g-schema):** `schemas/research_brief.schema.json`

| Field | Definition |
|---|---|
| `strategy_domain` | Asset class and market structure (e.g., `crypto_spot`) |
| `market_universe` | List of symbols to focus on (e.g., `[BTCUSDT]`) |
| `timeframe` | Candle resolution (e.g., `1h`) |
| `research_goal` | The central question this run tries to answer |
| `constraints` | Hard limits the [hypothesis](#g-hypothesis) must respect (e.g., use existing backtest framework) |
| `existing_context` | What is already known or already tried — prevents re-exploring dead ends |

---

### `hypothesis_card.yaml`


> **Why this file exists.** The one concrete claim being tested. It is what makes the run falsifiable rather than exploratory.

**Created by:** hypothesis_generation [skill](#g-skill)  
**Read by:** innovation_expansion, validation_gate  
**Schema:** `workflow_artifacts/schemas/hypothesis_card.schema.json`

| Field | Definition |
|---|---|
| `hypothesis_id` | Stable identifier (e.g., `H-005`) used to track the idea across runs |
| `thesis` | One-sentence plain-English claim about why this strategy should work |
| `rationale` | Market microstructure or behavioral reason supporting the thesis |
| `signal_concept` | Pseudo-formula or English description of the signal computation |
| `target_market` | Symbol, timeframe, and [regime](#g-regime) conditions where the signal applies |
| `assumptions` | List of things that must be true for the signal to work (falsifiable) |
| `expected_failure_modes` | Pre-enumerated ways this hypothesis could fail in practice |

---

### `expanded_hypothesis_card.yaml`


> **Why this file exists.** The variants that separate "the idea is wrong" from "this one setting is wrong". Without them a kill cannot tell you which it was.

**Created by:** innovation_expansion skill  
**Read by:** validation_gate, backtest_specification  
**Schema:** `workflow_artifacts/schemas/expanded_hypothesis_card.schema.json`

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


> **Why this file exists.** The reasoning behind the variant set, including the self-reported diversity audit — the record of *why* these variants and not others.

**Created by:** innovation_expansion skill  
**Read by:** verdict_interpreter (for carryover), campaign_review  
**Schema:** `workflow_artifacts/schemas/innovation_notes.schema.json`

| Field | Definition |
|---|---|
| `key_insight` | The most important conceptual discovery made during expansion |
| `recommended_test_order` | Prioritized list of variants to test first (most promising → least) |
| `risks_identified` | Structural risks seen across all variants |
| `variants_not_pursued` | Ideas that were considered but dropped, with brief rationale |
| `integration_notes` | Notes on how variants interact with existing bot components |

---

### `validation_protocol.yaml`


> **Why this file exists.** The plan for how this hypothesis will be tested, fixed before any result exists.

**Created by:** quant-validation skill  
**Read by:** validation_gate (self-produces it), backtest_specification, protocol_execution  
**Schema:** `workflow_artifacts/schemas/validation_protocol.schema.json`

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


> **Why this file exists.** The gate's verdict on whether the idea survives paper falsification — the field the router reads to decide what happens next.

**Created by:** quant-validation skill  
**Read by:** orchestrator (for routing)  
**Schema:** `workflow_artifacts/schemas/validation_decision.schema.json`

| Field | Definition — what it means | Values / range (meaning of each) | Example (`run_060`, 2026-08-27) |
|---|---|---|---|
| `status` | The gate's [verdict](#g-verdict) — the field the router reads to decide the whole run's next step. | `approve` (proceed to spec) · `conditional_approve` (proceed, conditions printed) · `refine` (this same call also produces `refinement_notes.yaml`, bounded) · `reject` (terminal) | `conditional_approve` |
| `rationale` | Why that verdict, in prose, so the decision can be audited later. | prose | *"Funding-rate mean-reversion mechanism is established (run_059 daily baseline: Sharpe > 0.8 …)"* |
| `conditions` | Conditions the backtest config must respect. Only meaningful on `conditional_approve`. | list of strings | *"Backtest both BTCUSDT and ETHUSDT on the registered windows"* (a cost or edge-to-cost condition is no longer allowed here: costs are judged only by the backtest, O-3) |
| `blocking_issues` | What must be fixed before this can proceed. Non-empty normally implies `refine` or `reject`. | list | `[]` |
| `promotion_path_if_approved` / `..._if_rejected` | Written in advance: what happens on each outcome, so the route is not invented after the result. | prose | *"If walk-forward Sharpe > 0.8 AND max_drawdown < 30% AND the post-backtest cost bar passes, [promote](#g-promote) to holdout_evaluation"* |
| `hypothesis_id` / `approval_issued_by` / `approval_timestamp` | Provenance. | string / string / date | `FUNDING_MR_4H_RETEST` / `validation_gate / run_060` / `2026-08-27` |

⚠️ **`family_status` is an accepted alternative to `status`.** The
quant-validation skill's real output for a multi-variant family validation used
it instead (run_053, 2026-07-06, F4f), and the router falls back to it. If
neither key is present the router raises rather than guessing
(`run_phase1_research.py::determine_post_validation_route`). Note also that §2.3 lists three statuses;
`conditional_approve` is a fourth, and is what run_060 actually returned.

---

### `refinement_notes.yaml`


> **Why this file exists.** What would have to change for a blocked hypothesis to become testable, and whether the engine can even do it.

**Created by:** quant-validation skill — in the same response as `validation_decision.yaml`, only when its own `status` is `refine` (E-039 S4, 2026-09-12; there is no separate `refinement_planner` stage/skill any more)  
**Read by:** innovation_expansion (next iteration), orchestrator  
**Schema:** `workflow_artifacts/schemas/refinement_notes.schema.json`

| Field | Definition |
|---|---|
| `blocker_responses` | For each blocking_issue from validation_decision, a concrete fix instruction |
| `decision.next_step` | What stage to route to next |
| `decision.implementation_allowed` | `true` if fixes can be made within the existing framework; `false` if a human must intervene |

---

### `backtest_spec.yaml`


> **Why this file exists.** The bridge from prose to executable config — the point where the idea stops being a description.

**Created by:** backtest-engineering skill  
**Read by:** protocol_execution tool  
**Schema:** `workflow_artifacts/schemas/backtest_spec.schema.json`

| Field | Definition |
|---|---|
| `status` | `spec_ready` (config is complete) or `component_gap` (a missing bot [component](#g-component) blocks execution) |
| `config` | Full `strategy_config` JSON that plugs directly into the trading-bot |
| `config_rationale` | For each config parameter, why that value was chosen |
| `component_gap` | Description of the missing component if `status = component_gap` |

---

### `decision.yaml`


> **Why this file exists.** Whether a runnable spec was actually produced, or the engine is missing a piece. Two words that route the whole run.

**Created by:** backtest-engineering skill (config validation step)  
**Read by:** orchestrator  
**Schema:** `workflow_artifacts/schemas/decision.schema.json`

A simple gate [artifact](#g-artifact) confirming whether the backtest_spec is valid and executable.

| Field | Definition — what it means | Values / range (meaning of each) | Example (`run_060`, 2026-08-27) |
|---|---|---|---|
| `status` | Whether a runnable spec was produced. Two words that route the run — and anything unrecognised pauses it. | `spec_ready` (→ stage 8 protocol_execution) · `component_gap` (→ [human pause](#g-human-pause); the engine lacks a piece) · **any other value** (→ human pause, deliberately fail-closed) | `spec_ready` |
| `rationale` | Why, naming the component or the gap. | prose | *"FundingRateMeanReversionComponent exists in COMPONENT_CATALOG.md with full threshold=0.0 continuous-forecast support"* |
| `blocking_issues` | What is missing, when there is a gap. | list | `[]` |
| `stage` | Which stage wrote it. | string | `backtest_specification` |

⚠️ **The values this entry used to list — `approved`, `blocked` — have never
occurred.** Measured across the **39** real `decision.yaml` files: `spec_ready`
**38**, `validation_incomplete` **1**. Neither `approved` nor `blocked` appears
once, and neither is in the router's `KNOWN_STATUSES`. Note also that
`validation_incomplete` is **not** a known status either, so that run took the
fail-closed human-pause branch. See
[E037-23](../engineering/roadmap/E-037/FINDINGS.md#e037-23).

An unknown status is **not** treated as a soft failure: `determine_post_spec_route`
prints that the SKILL may need a new status case and pauses
(`run_phase1_research.py::determine_post_spec_route`).

---

### `protocol_result.yaml` / `protocol_summary.json`


> **Why this file exists.** What actually happened when the strategy was traded across every window. The raw evidence every later judgment rests on.

**Created by:** protocol_execution tool (`tools/run_protocol.py`) — every run always executes a full walk-forward backtest.
**Read by:** verdict_interpreter  

| Field | Definition — what it means | Values / range (meaning of each) | Example |
|---|---|---|---|
| `results` | Per-window, per-symbol raw metrics (`net_return_pct`, `sharpe`, `max_drawdown_pct`, `trade_count`, `win_rate`, `fees_paid`, …) — one entry per `{symbol, window}` pair actually run. Each entry also carries `core` (that window's real `metrics.json` core block verbatim, including `forecast_return_corr_pvalue_block_adjusted`/`forecast_return_corr_n_eff`/`forecast_return_corr_all_bars`), `per_regime`, `regime_validity`, `data_quality` — that window's gap-detection block (`null` only if a run switched the gap rule off with `gap_detection=False`; it is on by default for backtests since 2026-10-01) — and `component_errors` — `{count, samples}`, F5b's own exception counters off the strategy object for that window, always present (a healthy run reports an explicit `count: 0`, never a fabricated absence). | list | `run_011`: 24 entries (2 symbols × 12 windows) |
| `per_symbol_summary` | Per-symbol aggregation across windows: `median_sharpe` (the primary promotion gate — see basis note below), `max_abs_drawdown_pct`, `min_trade_count`. | dict keyed by symbol | `run_011`: `{BTCUSDT: {median_sharpe: -5.019, …}, ETHUSDT: {median_sharpe: -2.604, …}}` |
| `verdict` | Preliminary verdict from the tool itself, ahead of the LLM verdict-interpreter's own read. | `promote` · `kill` · `refine` | `kill` |
| `hypothesis_verdict` | The evaluated pre-registered criteria: each one's requirement, actual value, PASS/FAIL/UNTESTED, and a rolled-up `verdict_reason`. This is what `verdict_interpreter` actually reads. | dict: `{verdict, criteria_results: [...], verdict_reason, diagnostics}`; under `--diagnostics-only` (config-direct, E-061 C1.3): `verdict: null`, `criteria_results: []`, `diagnostics` still computed; `null` with neither flag | `run_011`: 4 of 6 evaluable criteria FAIL, 3 UNTESTED |
| `protocol_file` | Bare filename of the protocol this run executed — the pre-registration conformance check compares this against `pre_registration.yaml`'s pinned `machine_constraints.protocol_ref`. | filename | `funding_mr_4h_retest_v1.json` |
| `episode_blocked_significance_by_symbol` | Per-symbol A8.5.1a significance method label — the conformance check (`_check_protocol_execution_conformance`) compares each symbol's label against `is_a851a_method()` (`episode_significance.py::is_a851a_method`) when `machine_constraints.significance_methodology: episode_blocked_a851a` is pre-registered; any symbol failing that check is a conformance violation. | dict keyed by symbol | `{BTCUSDT: episode_blocked_a851a, ETHUSDT: block_6_dense_fallback}` |

**Basis matters for `median_sharpe` (2026-07-10):** the decision-consumed value must be computed on a bar-level equity curve (`bars.csv` `total_portfolio_value`, full-window daily returns) — a LIFO-fragment/trade-exit-day version of the same statistic can disagree sharply under sparse trading and must never feed a verdict; it may exist elsewhere labeled `basis: lifo_fragment, descriptive_only`. See `docs/VERIFICATION_DOCTRINE.md` section 1 for the mechanism and a worked example.

> **Post-backtest go/no-go fields (CUL-261/262/264/266/272).** These
> live in `trading-bot/reporting/run_artifact.py::build_core`, which produces
> `metrics.json`, not this file directly — but `metrics.json`'s hand-picked
> fields are what stage 8 forwards into `protocol_summary.json` (see that
> stage's forwarding block), so they end up here.
>
> **Why these exist.** The signal-quality go/no-go runs *after* the backtest,
> on real measured numbers, rather than as a pre-flight estimate — computed
> by `performance/signal_statistics.py` (trading-bot never imports from
> strategy-research) on the actual bars/trades a real backtest produced.
>
> | Field | Definition — what it means | Worked example |
> |---|---|---|
> | `forecast_return_corr_n_eff` | Effective sample size behind the correlation: active bars placeable into blocks without spanning a real data gap, `÷ block_size` — the "adjacent hours aren't independent" correction. | a run with 8928 active bars, `block_size=24` (1h bars, 24/day) → `n_eff` well under 8928 once gap-spanning blocks are excluded |
> | `forecast_return_corr_pvalue_block_adjusted` | Two-tailed significance of `forecast_return_corr`, computed from `n_eff` above rather than the raw bar count. Always `≥` the naive `forecast_return_corr_pvalue`. | — |
> | `sigma_bar_bps` | Per-bar return volatility in bps, measured directly from the backtest's own bars. | — |
> | `sigma_bar_bps_is_placeholder` | `true` when fewer than 5 bars were available and the placeholder `15.0` was substituted. **When true, `post_backtest_cost_check`/`post_backtest_route` below are not load-bearing.** | — |
> | `post_backtest_cost_check` | Dict: `{estimated_gross_edge_bps_per_trade, cost_bps_per_trade, edge_to_cost_ratio, safety_factor_required, pass}`. **Estimated**, not measured — `IC × sigma_bar_bps × √(avg_holding_bars)` vs. `cost_model.yaml`'s theoretical round-trip cost, run on real post-backtest inputs (A8.1: both IC significance and this cost check are required). | — |
> | `post_backtest_route` | The combined IC-significance + cost-hurdle verdict on the *estimated* cost check above. | `inconclusive_insufficient_data` · `kill_no_ic` · `refine_inverted_ic` · `kill_cost_hurdle` · `refine_cost_hurdle` · `proceed_to_interpretation` |
> | `post_backtest_route_rationale` | One-sentence prose explaining `post_backtest_route`, with the actual numbers substituted in. | *"Active-bar IC=0.0412 (p=0.0231, significant). Edge-to-cost ratio=1.8342 < required 2.0."* |
> | `real_round_trip_cost_bps` | **Measured**: mean `CompletedTrade.total_commission_percent` across every completed trade, in bps. | a real run: `20.0` bps |
> | `real_gross_edge_bps_per_trade` | **Measured**: mean `CompletedTrade.profit_loss_percent` — gross, pre-commission, deliberately not net (net is already cost-adjusted, would double-count fees against `real_round_trip_cost_bps`). | same run: `-2.569` bps/trade |
> | `post_backtest_cost_check_real` | Same shape as `post_backtest_cost_check`, built from the two measured fields above. Carries `"basis": "real"`. Field is still named `estimated_gross_edge_bps_per_trade` (inherited key shape `determine_route()` reads) even though the value is real — check `basis`, not the key name. | that run: `edge_to_cost_ratio ≈ 0.128`, `pass: false` |
> | `post_backtest_route_real` / `post_backtest_route_real_rationale` | The route/rationale pair computed from the *real* cost check instead of the estimated one — the actual go/no-go this run's real economics support. | — |
> | `forecast_return_corr_all_bars` | The **ungated** counterpart to `forecast_return_corr`: same correlation, measured over ALL bars (no `forecast != 0` filter) rather than active bars only. The only figure admissible for the A2.1 ungated-escape criterion — `forecast_return_corr` cannot be, since a signal gated to a rare regime necessarily looks stronger on its own active bars than over the whole series. Equal to `forecast_return_corr` for an always-active (ungated) strategy; diverges for a regime-gated one. | a regime-gated run: `forecast_return_corr=0.21`, `forecast_return_corr_all_bars=0.02` |
> | `forecast_return_corr_all_bars_pvalue_block_adjusted` / `forecast_return_corr_all_bars_n_eff` | Same block-adjusted significance/effective-sample-size machinery as `forecast_return_corr_pvalue_block_adjusted`/`n_eff` above, applied to the all-bars population instead of the active-bar one. | — |
>
> **Priority order inside `determine_route()`, exact, same for both the
> estimated and real routes:**
> 0. Sample too small to trust (`n_eff` below its floor, `n_trades` below its
>    floor, or the cost check rests on a placeholder `sigma_bar_bps`) →
>    `inconclusive_insufficient_data` — not a verdict, "not enough
>    information to judge this," never to be confused with a `kill_*` route.
> 1. IC not significant (`p ≥ 0.10`) → `kill_no_ic`.
> 2. IC significant but negative → `refine_inverted_ic`.
> 3. IC significant and positive — cost hurdle: edge÷cost must be `≥ 2.0`.
>    Fails badly (`p > 0.05` or `ratio < 0.5`) → `kill_cost_hurdle` (structural).
>    Fails narrowly → `refine_cost_hurdle` (try a wider threshold/longer hold).
> 4. Passes both → `proceed_to_interpretation`.
>
> **Worked example, a real run:** `trade_count=110`,
> `real_round_trip_cost_bps=20.0`, `real_gross_edge_bps_per_trade=-2.569`. The
> real edge is *negative* — losing 2.569 bps/trade gross before even reaching
> the 20 bps it costs to trade — so `post_backtest_route_real` reads a kill,
> regardless of what the *estimated* `post_backtest_route` above it says. A
> signal can look viable on `cost_model.yaml`'s theoretical cost and still be
> a real loser once actual fees and outcomes are measured.
>
> **INFORMATIONAL ONLY, both routes.** Nothing in this repository reads
> `post_backtest_route`/`post_backtest_route_real` to skip, gate, or
> short-circuit `verdict_interpreter` or any other stage. Whether a
> mechanical kill here should short-circuit the LLM call is a separate,
> deliberately not-yet-made decision. Until that decision is made, treat
> these fields as evidence for the verdict-interpreter to read and cite, not
> as gates it must obey.

⚠️ **This entry previously documented five fields that no artifact has ever
contained:** `per_window_metrics`, `per_symbol_metrics`, `per_regime_metrics`,
`promotion_criteria`, `diagnostic_metrics` (measured 2026-08-30 across 38
real files; re-measured 2026-08-31, still 0 occurrences of any of the five —
the one correction from the first pass was `median_sharpe`, wrongly listed
as absent because that audit inspected only top-level keys; it is real,
nested inside `per_symbol_summary`, in 31 of the 38). The table above
replaces them with the artifact's real shape. The former names are preserved
here as a historical note rather than silently dropped, because they record
an intended, more granular design (per-window/per-regime breakdowns, an
explicit promotion-criteria block) that the artifact never grew into — the
closest real equivalents are `results` (per-window, at least) and
`hypothesis_verdict.criteria_results` (the pass/fail gates, though not
labeled `promotion_criteria`). See
[E037-24](../engineering/roadmap/E-037/FINDINGS.md#e037-24).

---

### `verdict_interpretation.yaml`


> **Why this file exists.** What the result means and what to do next — kept separate from the measurement so the interpretation stays auditable.

**Created by:** verdict-interpreter skill  
**Read by:** orchestrator, campaign_review. **E-018 (2026-09-13):** the
orchestrator no longer routes off THIS file's `hypothesis_verdict`/
`lineage_routing` when `pass_rule_evaluation.yaml` is binding — it reads that
file directly instead (see stage 11 item 9). It still reads this file for
every other field (`root_cause`, `hypothesis_family`,
`proposed_change_dimension`, etc.) on every run.  

| Field | Definition — what it means | Values / range (meaning of each) | Example |
|---|---|---|---|
| `status` | The [altitude](#g-altitude) decision — what happens next, and at what size of change. Falls back to `protocol_verdict` on older runs. | `refine` (same family, new parameter) · `pivot` (new family) · `escalate` (new instrument/timeframe) · `promote` (provisional → holdout) · `kill` (terminal) | `kill` |
| `hypothesis_verdict` / `lineage_routing` | The verdict on the hypothesis, and what it means for its lineage. | string / `terminate`, `continue`, … | `kill` / `terminate` |
| `criteria_summary` | Each pre-registered criterion with its measured value and result — the audit trail from evidence to verdict. | list of `{criterion, result, value}` | criterion `median_sharpe >= 0.8` → `FAIL` |
| `untested_criteria` | Criteria that were never reached, kept explicit so a partial test is not read as a complete one. | list | `["max_drawdown (not evaluated)"]` |
| `root_cause` | The diagnosis. **`mechanism_failure` is load-bearing:** two of its values divert the run away from any scientific verdict. | dict; `mechanism_failure` ∈ `already_priced_in`, `component_execution_error` (→ human pause, immune to the [circuit breaker](#g-circuit-breaker)), `regime_misattribution` (→ human pause for the regime auditor), … | `{mechanism_failure: already_priced_in, supporting_evidence: "post_backtest_route_real=kill_no_ic (p=…)"}` |
| `primary_failure_mode` | Short label for how it failed. | string | `no_informational_content` |
| `hypothesis_family` | Scopes the circuit breaker. Per-family since F6 (2026-07-04) — a global scope let a dead family's history force an unrelated family straight to pivot. | string | `funding_rate_mean_reversion` |
| `proposed_change_dimension` | Which parameter a `refine` would move. The breaker counts repeats of this within a family. | string or `null` | `null` |
| `altitude_justification` | Why this altitude and not a larger or smaller one. | prose | *"Rule 2 (weak signal): forecast_return_corr=0.0162, p=0.5315 > 0.10 — no statistically significant directional …"* |
| `config_to_failure_map` | Ties the failure back to the exact config that produced it. | prose | *"FundingRateMeanReversionComponent (threshold=0.0, ungated) on 4h timeframe produces forecast_return_corr=0.0162"* |

⚠️ **This entry previously documented five fields that no artifact has ever
contained.** Measured 2026-08-30 across the **39** real
`verdict_interpretation.yaml` files on disk, each of the following appears
**0 times in this artifact**: `altitude` (described as "numeric altitude, 1 =
refine, 2 = pivot, 3 = escalate"), `verdict`, `diagnostic_rule_applied` (e.g.
`cost_drag`, `signal_inversion`), `parameter_bracket` ("[min, max, step] range
to search next"), and `next_altitude` ("fallback altitude if the current verdict
fails again"). The real fields here are `status` (34 of 39) and `root_cause`
(11 of 39).

**But four of those five exist elsewhere, and are populated** — re-measured
2026-08-31. They were documented on the wrong artifact rather than invented:
`verdict` in `protocol_result.yaml` (31), and `diagnostic_rule_applied` (31),
`next_altitude` (30) and `parameter_bracket` (14, of which 2 non-null) in
`findings_carryover.yaml`. Only **`altitude`** appears in no artifact at all.
The former descriptions are preserved here rather than deleted, because they
record an intended design; they do not describe the artifact. See
[E037-22](../engineering/roadmap/E-037/FINDINGS.md#e037-22).

⚠️ **`pass_rule_evaluation.yaml`, not this file, is the decision authority
where a structured `pass_rule` exists — and since E-018 (2026-09-13), routing
reads that file directly rather than trusting this one's copy.** A
disagreement between the two is recorded as an informational flag
(`pass_rule_evaluation_disagreement`) but no longer halts the pipeline;
before 2026-09-13 it was a blocking conformance violation.

---

### `proposed_brief.yaml`


> **Why this file exists.** The next question, written by the run that just finished. This is how a campaign continues rather than restarts.

**Created by:** verdict-interpreter skill (when verdict = refine or pivot)  
**Read by:** next run's hypothesis_generation (becomes that run's research_brief)  

The pre-filled research_brief for the next run. Includes the `existing_context` field populated with what was learned from the current run, so the next run doesn't repeat dead ends.

---

### `escalation_request.yaml`


> **Why this file exists.** The record that a search space was widened, and why — so widening cannot happen silently.

**Created by:** verdict-interpreter skill (when verdict = escalate)  
**Read by:** orchestrator  

| Field | Definition — what it means | Values / range (meaning of each) | Example (`run_020`) |
|---|---|---|---|
| `target` | What dimension is being widened. | `timeframe` · `instrument` | `timeframe` |
| `reason` | Why the current target is exhausted — the evidence that justifies widening rather than refining. | prose | *"TRENDING regime filter (ER≥0.50, VR≥1.20) on 1h bars gates signal generation to <1% of deployment window; zero trades across 22 windows prevent edge evaluation…"* |
| `proposed_capability` | The concrete next test on the new target, plus the expected outcome that would confirm the escalation was warranted. | prose | *"Backtest RSI momentum, Keltner bands, and other signal components on 4h timeframe for BTCUSDT, ETHUSDT. Expected outcome: regime windows expand 4-5x in bar count per fold…"* |

⚠️ **This entry previously documented three fields that no artifact has ever
contained:** `target_symbol`, `target_timeframe` (described as new symbol/
timeframe to test), and `rationale`. Measured 2026-08-30 across the **7**
real `escalation_request.yaml` files on disk: all three appear **0 times**.
The real fields — `target`, `reason`, `proposed_capability` above — describe
the same three concepts under different names (a single `target` field
naming the dimension rather than separate symbol/timeframe fields, since an
escalation widens exactly one dimension at a time). The former field names
are preserved here as a historical note rather than silently dropped,
because they record an intended design that predates the artifact's actual
shape. See [E037-24](../engineering/roadmap/E-037/FINDINGS.md#e037-24).

---

### `findings_carryover.yaml`


> **Why this file exists.** What the next run must not re-learn. Campaign memory in its most direct form.

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


> **Why this file exists.** Where this run is, what it has spent, and whether it is paused. The file that makes a run resumable.

**Created by / Updated by:** orchestrator (`workflow/run_phase1_research.py`)  
**Read by:** orchestrator (on resume), any stage needing run context  

Internal run state — not a research artifact but the orchestrator's working memory.

> ⚠️ **Three terminal states were undocumented until 2026-08-31**, and they are
> the three that actually happen. `completed_refined`, `completed_reframed` and
> `completed_escalated` account for **34 runs on disk** between them and were
> named nowhere in this guide, while `completed_promoted` — documented since the
> beginning — has occurred **zero** times. The guide described the ending nobody
> has reached and omitted the ones everybody reaches. See
> [E037-31](../engineering/roadmap/E-037/FINDINGS.md#e037-31).

| Field | Definition |
|---|---|
| `status` | Where the run ended up. Terminal values, with counts measured over the runs on disk 2026-08-31: `completed_refined` (**20**) · `completed_reframed` (**11**) · `completed_rejected` (4) · `completed_escalated` (3) · `completed_promoted` (**0 — has never happened**). Non-terminal: `running`, `paused_for_human` / `human_pause`, `error`. |
| `current_stage` | The stage currently executing |
| `completed_stages` | Ordered list of stages already finished |
| `governance` | Budget limits: max_refinements, max_tokens, max_variants |
| `counters` | Runtime counters: `refinements_used`, `reruns_used` |
| `flags` | Boolean gates: `validation_approved`, `screening_passed`, `walk_forward_passed`, `holdout_reserved` |
| `audit_log` | Per-stage record of token usage, cost_usd, attempt number, and timestamp |

---

> ### ⚠️ One of these five artifacts is still flag-gated off
>
> `variant_selection.yaml`, `variants_not_pursued.yaml`, the "already tried"
> prompt input (`exclusion_digest.yaml`, or `tried_ideas.yaml` once a campaign
> memory exists) and `schedulability.yaml` are produced or used by default — their gating flags were
> switched on (E-041, 2026-09-02). `variant_anti_adjacency_result.yaml` is the
> exception: `orchestrator.variant_anti_adjacency_gate.enabled` stays `false`.
> Its first design (a family / composition-fingerprint key) was rejected on
> review (E-036, 2026-09-02); E-036 S2a (2026-09-27) rebuilt it as the
> exact-match check, and it is switched on only after the S2b corpus replay
> has published refuse/admit counts and the operator has reviewed them.
>
> | Flag in `config/campaign_config.yaml` | Gates | Default |
> |---|---|---|
> | `orchestrator.variant_selection_record.enabled` | `variant_selection.yaml`, `variants_not_pursued.yaml` | `true` |
> | `orchestrator.variant_anti_adjacency_gate.enabled` | `variant_anti_adjacency_result.yaml` | `false` — blocked on E-036 S2b |
> | `orchestrator.exclusion_digest_input.enabled` | `tried_ideas.yaml` when `campaign_memory.yaml` exists, else `exclusion_digest.yaml` | `true` |
> | `orchestrator.schedulability_block.enabled` | `schedulability.yaml` | `true` |
>
> Flags are read **at runtime**, so this table states the committed default,
> not a permanent fact. A missing key, section or file resolves to `false` —
> silence is never a green light. `variant_anti_adjacency_gate` additionally
> requires `variant_selection_record` in the LLM flow, and `regroup_record`
> when no `campaign_memory.yaml` exists yet; it raises loudly if either is
> missing. `orchestrator.anti_adjacency_retry` was removed by E-036 S2a (it
> fired before any config existed, so it could never catch a repeat).
>
> See [E037-21](../engineering/roadmap/E-037/FINDINGS.md#e037-21) for how this
> was found, and E-041 for the switch-on decisions.

### `variant_selection.yaml` (per run)

**Objective:** record *which* of `innovation_expansion`'s variants was actually
chosen for the backtest, and *why*.

**Why it exists:** `backtest_specification` receives the whole menu of variants
and emits one config. The narrowing happens inside its own reasoning, with no
routing decision in code, so historically nothing recorded the choice — a run
with three distinct threshold variants left no trace of which one was tested.

**Logic:** the stage names its pick in `backtest_spec.yaml`'s
`selected_variant_id`; deterministic code then joins that ID against the menu
and writes the record. **Enforcement is in code, not the schema** — a missing
ID raises, and an ID matching nothing in the menu raises, rather than writing a
silently-broken record. Variant IDs are derived by one shared rule (a dict's
`variant_id`, else `id`/`name`/`variant_name`/`label`, else a positional hash
for bare strings) so the same variant resolves identically everywhere.

Carries: `selected_variant_id`, the matched variant verbatim, resolved
`instrument` and `timeframe`, and the LLM's own rationale relocated where code
can read it. `instrument` may be a **list** for genuinely multi-symbol
hypotheses; consumers must check every entry, not just the first.

### `variants_not_pursued.yaml` (per run)

**Objective:** keep the ideas that were generated and discarded.

**Why it exists:** across 43 runs the loop generated 138 variants and tested one
per run, recording the discards in 1 run out of 59. It then reported *"queue
exhausted"* and stopped — having thrown away roughly a hundred ideas it had
already reasoned about. This is the supply side of that problem.

**Logic:** every menu entry except the chosen one, copied verbatim by code with
its derived ID, plus an optional "why it lost" only when the stage actually
said so — never fabricated.

### `tried_ideas.yaml` (per run)

**Objective:** tell the idea-writing stages (2 and 3) what has already been
tried.

**Why it exists:** without it the generator cannot see campaign history and
re-proposes old ideas. Its predecessor, `campaign_record/exclusion_digest.yaml`
(`tools/build_exclusion_digest.py`), grouped runs into families, a grain the
operator rejected (E-036, 2026-09-02; family machinery retired, card G).

**Logic:** written into `runs/<run_id>/artifacts/` at prompt time, only under
`orchestrator.exclusion_digest_input.enabled` and only when
`campaign_record/campaign_memory.yaml` exists, by
`tools/campaign_memory.tried_ideas`: one row per memory entry — `run_id`,
`hypothesis_id` (an idea's identity), `symbols` its tested variants ran on,
`timeframe` (the protocol file's), the grid's `idea_status` — oldest first, at
most `TRIED_IDEAS_MAX_ROWS` (200) most recent rows, the rest counted in
`omitted_older_runs`; an unreadable old protocol file is listed under
`warnings` and never crashes the prompt. Derived, never edited; the run keeps
exactly what the model was shown. It REPLACES the legacy digest as the input
when the memory exists (never both). With no memory file (today's default)
the stages get `campaign_record/exclusion_digest.yaml` exactly as before
E-036 S2a — family-scoped `(family, instrument, timeframe)` triples,
regenerated on demand by `tools/build_exclusion_digest.py` — so the default
prompt input is unchanged; decide-next also records a lookup from it
(`digest_advisory`, information only).

### `variant_anti_adjacency_result.yaml` (per run)

**Objective:** record whether the config about to be backtested is an exact
repeat of one already tested, and of which.

**Logic:** written by the exact-match check at stage 6 (item 2) under
`orchestrator.variant_anti_adjacency_gate.enabled`. **Layer 2 (binding):** the
candidate's key — `forecast_hash` (`_compute_forecast_hash` of the file the
backtest runs, the trial row's own hash), sorted symbols of the protocol it
runs, that protocol's timeframe and a hash of its windows — looked up in
`campaign_memory.yaml` through `tools/novelty.py`, the same functions
decide-next uses. `route: refuse`, `outcome: repeat` and `matched: [{run_id,
variant_id}]` on a hit; else `admit` / `novel`. A run with no memory entry, an
entry marked `legacy: true`, and the run itself never match. **Layer 1
(advisory):** the knowledge base at mechanism grain, recorded as
`layer1_advisory` (`warn` / `admit` / `no_opinion` / `not_evaluated`); it
never refuses. Also carries `key`, `config_ref`, `protocol_ref`,
`memory_present`; the LLM flow adds `selected_variant_id`; the config-direct
flow writes one result per checked variant plus `repeats` and `run_end`.

### `schedulability.yaml` (campaign level)

**Objective:** make "the loop is idle" visible to the loop itself.

**Why it exists:** `process_once()` returns on `"Queue exhausted"` *before* any
loop-health write, so the one condition that actually stopped this [campaign](#g-campaign) was
the one condition nothing recorded.

**Logic:** re-derived from primary records (`campaign_queue.yaml` +
`campaign_log.md`) on every step, written **before** the exhaustion return.
Carries ready / in_progress / blocked / done counts, days since last completion
(counting quarantine as a completion, since it also retires an entry), and per
blocked entry its dwell time and the blocker itself with its prefix stripped.
A pure projection — safe to delete, the next step rewrites it. Entry IDs are
matched as whole tokens, so activity on a split child (`{parent}__split_{x}`)
cannot reset the blocked parent's dwell to zero.

### `campaign_state.yaml`


> **Why this file exists.** The campaign memory across every run: what was tried, what failed, and -- via trial_sharpes -- how much statistical budget has been spent.

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

Handoffs are the formal interface contract between stages. Each stage reads its [handoff](#g-handoff) file to know exactly what inputs are available and what it must produce.

| Field | Definition |
|---|---|
| `objective` | Plain-English goal for the receiving stage |
| `required_inputs` | Files the stage must read, with a `reason` for each |
| `optional_inputs` | Files that provide additional context if available |
| `constraints` | Hard rules the stage must not violate |
| `deliverables` | Artifacts the stage must produce |
| `assigned_engine` | Which engine runs this stage: `claude`, `gemini`, or `tool` |

**Config-direct authoring (E-061 C1.2).** Under
`orchestrator.config_direct_authoring.enabled`, `backtest_specification`,
`data_availability_gate`, `protocol_execution` and `verdict_interpreter` load
`handoffs/config_direct_<stage>.yaml` instead of their legacy handoffs (which
require `validation_protocol.yaml`, never written in that flow). These are
rewritten by code from the current flags at every stage entry
(`run_phase1_research.py::_config_direct_handoff_path`, the one place that decides
it, used by `run_loop` and `async_invoke_agent`), never by `setup_run`;
flag-off runs never get them. `verdict_interpreter`'s is the legacy template minus
`validation_protocol.yaml`; it is reached under config-direct only with
`specialist_readers` off, which is outside the target flag set.

---

### `trade_diagnostics.json`

> **Why this file exists.** Per-trade records, because aggregate medians hide the failure channel — the finding A3.6 was written for.

**Created by:** protocol_execution tool
**Read by:** verdict_interpreter

Per-trade records (one row per closed trade) with fields: `entry_bar`, `exit_bar`, `pnl_bps`, `cost_paid_bps`, `exit_reason`, `mae_bps`, `mfe_bps`, `post_exit_return_5bars`, `post_exit_return_20bars`. Summary: `trade_diagnostics_summary` with winner/loser-conditional metrics (A3.6), `stop_loss_recovery_rate`, `pnl_concentration`.

---

### `regime_detector_report.yaml`

> **Why this file exists.** Whether the regime detector is trustworthy enough for its labels to be allowed to condition any metric.

**Created by:** `tools/validate_regime_detector.py`
**Read by:** regime_auditor skill

| Field | Definition — what it means | Values / range (meaning of each) | Example (campaign root, 2026-08-28) |
|---|---|---|---|
| `detector_version` | Hash of the detector config, so a finding can be tied to the exact detector that produced it (A5.3). | hex8 | `04cd1e16` |
| `per_symbol_per_timeframe` | The A2.2 gate metrics, per symbol and timeframe. Its nested `metrics` dict carries `regime_persistence_median_bars` (dwell time — the real name for what was once documented as `persistence_score`), `transition_frequency_per_window`, `trending_activation_rate` (the real name for `activation_rate`), `parameter_sensitivity`, `zero_trade_slot_pct`, `agreement_with_reference_labels`, plus two nested sub-blocks: `class_conditional_sensitivity_per_label` (per-label flip rate under perturbation — real name and location for what was documented as a top-level `class_conditional_sensitivity`) and `activation_band_check` (`within_band`, `band_min`/`band_max`, `rare_label_threshold`, `gate_metric_used`). Each entry also carries a sibling `confidence` (`high`/`medium`/`low`), `confidence_rationale` (prose), and `known_weak_periods` (list of window labels) alongside `metrics`. | list of `{symbol, timeframe, metrics{…}, confidence, confidence_rationale, known_weak_periods}` | `{regime_persistence_median_bars: 17544, trending_activation_rate: 0.0, class_conditional_sensitivity_per_label: {unknown: {class_conditional_sensitivity: 0.0, …}}, activation_band_check: {within_band: false, …}}`; `confidence_rationale`: *"persistence=17544.0>=12, all_bars_sensitivity=0.000<=0.25 but fails high gate: activation=0.00% outside [10%,40%] (cap: medium)"* |
| `data_range` / `config_source` / `evaluated_at` | Provenance. `evaluated_at` drives the 30-day staleness check. | dict / path / ISO-8601 | `{start: 2024-01-01, end: 2025-12-31}` / `runs\run_060\artifacts\candidate_strategy_config.json` / `2026-08-28T19:54:21Z` |

⚠️ **This file lives at the campaign root, not under a run** — one file shared
by every run, regenerated when older than 30 days
(`run_phase1_research.py::_ensure_regime_detector_report`). `config_source` records which run's config
last produced it. Note the example's `config_source` is a **Windows path**, the
same portability issue as [E037-11](../engineering/roadmap/E-037/FINDINGS.md#e037-11)
(fixed for the `protocol_version` conformance check, CUL-186, 2026-09-03; this
specific `config_source` display field is unaffected — it is provenance
text, not compared programmatically).

⚠️ **This entry previously documented two fields, `persistence_score` and
`activation_rate`, that appear at no depth in any real artifact** (measured
2026-08-30, one file at the campaign root — `class_conditional_sensitivity`,
also previously listed here, was re-measured 2026-08-31 and found present,
nested, correcting an earlier top-level-only check). The table above
replaces both with their real names and nesting depth. See
[E037-24](../engineering/roadmap/E-037/FINDINGS.md#e037-24).

---

### `regime_audit_decision.yaml`


> **Why this file exists.** The human judgment on the detector, made under a firewall that keeps profitability out of the decision.

**Created by:** regime-auditor skill (a human running it by hand), including `ungated_escape_eligible` — there is no automated second write to this file.
**Read by:** verdict_interpreter, orchestrator

| Field | Definition — what it means | Values / range (meaning of each) | Example (`run_039`, the only real instance on disk) |
|---|---|---|---|
| `status` | The A2.2 classification this audit resolves to. | `trustworthy` · `needs_retune` · `unusable_for_this_symbol_timeframe` | `unusable_for_this_symbol_timeframe` |
| `affected_symbols_timeframes` | Which symbol/timeframe pairs the status applies to. | list of `SYMBOL_timeframe` | `[BTCUSDT_1h, ETHUSDT_1h]` |
| `recommended_action` | The auditor's prose reasoning and next step — under the retune firewall (A2.2: must cite detector-intrinsic criteria only, never PnL/Sharpe; enforced in code by `_validate_retune_firewall`, `run_phase1_research.py::_validate_retune_firewall`, which raises on a violation — the file itself carries no field recording that the check passed). | prose | *"The structural blocker is transition_frequency (~40 transitions/window observed…). Per A2.3 post-unusable policy: record candidate detector families in config/detector_wishlist.yaml…"* |
| `retune_attempted` / `retune_summary` | Whether a retune grid search ran, and if so its full result: `grid_cells_evaluated`, `grid_dimensions`, the `vr_component` drop decision, `best_directly_implementable` vs. `overall_winner_requires_extension` cells, `max_score_achieved` vs. `max_possible_score`, and a `structural_ceiling` prose explanation when no cell passes. | bool / dict (only present when `retune_attempted` is true) | `true` / 48 cells evaluated, best score 5 of 8 possible |
| `official_report_after_retune` | The regime detector's own per-symbol metrics (`confidence`, `persistence`, `transitions_pw`, `cc_sens_trending`, `activation`, `in_band`) after the retuned config, kept alongside the pre-retune `regime_detector_report.yaml` for comparison. | dict keyed by `detector_version`/`evaluated_at`/`config` plus one entry per symbol_timeframe | `btcusdt_1h: {confidence: medium, persistence: 12.0, …}` |
| `a23_policy_applied` / `a23_detector_wishlist` | Legacy fields, present only in `runs/run_039`'s file: whether the former A2.3 post-unusable policy fired, and where candidate detectors were recorded. The policy is deleted (D-052); nothing writes or reads these fields. | bool / path | `true` / `config/detector_wishlist.yaml` |
| `ungated_escape_eligible` | A2.1 escape assessment — whether an all-bars (ungated) IC check can substitute for a trustworthy detector. Set directly by the regime-auditor skill, per its own SKILL.md rules. | `true` · `false` · `indeterminate` | `true` |
| `ungated_escape_rationale` | The prose justification for the `ungated_escape_eligible` value, citing the A2.1 rule it satisfies. | prose | *"IC is within 2 SE of zero — consistent with no edge over all bars. Per A2.1: signal_bad_everywhere may be concluded."* |

⚠️ **This entry previously documented `retune_firewall_check` as a field —
it is absent from the real artifact** (1 real instance on disk, measured
2026-08-30; `class_conditional_sensitivity`, also previously listed here as
absent, was re-measured 2026-08-31 and found present, nested inside
`regime_detector_report.yaml` rather than this file — corrected there, not
here). The firewall itself is real and enforced in code, as the
`recommended_action` row above explains; the decision file simply never grew
a field recording that the check passed. The table above replaces the old
3-row sketch with this file's actual (much larger) shape. See
[E037-07](../engineering/roadmap/E-037/FINDINGS.md#e037-07) and
[E037-24](../engineering/roadmap/E-037/FINDINGS.md#e037-24). This file has
been produced by exactly 1 of 61 runs to date — see
[E-040](../engineering/roadmap/E-040/EPIC.md) for whether that low incidence
reflects the audit rarely triggering or the mechanism being under-used.

---

### `promotion_audit.yaml`

> **Why this file exists.** Whether a promising result survives being corrected for how many things were tried. The gate that stands between a good backtest and the holdout.

**Created by:** orchestrator / `tools/deflate_sharpe.py`
**Read by:** holdout_evaluation tool
**Schema:** `workflow_artifacts/schemas/promotion_audit.schema.json`

| Field | Definition |
|---|---|
| `deflated_sharpe_ratio` | Bailey & López de Prado DSR; `null` for sparse-trading candidates |
| `trial_sharpe_variance` | Variance of the [trial](#g-trial) Sharpe distribution used for DSR |
| `n_trials_used` | Trial count after dedup by `forecast_hash` |
| `passes_deflated_threshold` | `true` if DSR > 0.95 (Sharpe path) or t_stat > 2.0 ([expectancy path](#g-expectancy-path)) |
| `excluded_trial_counts` | Breakdown of excluded trials by reason (statistic_expectancy, statistic_neither, no_sharpe_value, dedup_removed) |
| `expectancy_promotion` | Present on sparse-trading path: `{t_stat, passes, bonferroni_note}` |
| `is_sparse_trading` | `true` when below_floor_pct > 50% (A3.4) |

---

### `holdout_result.yaml`

> **Why this file exists.** The one-shot final exam. Single-use, terminal, and pre-registered — reading it is spending it.

**Created by:** Human (after running holdout backtest) + orchestrator (marks consumed_at)
**Read by:** holdout_evaluation tool
**Schema:** `workflow_artifacts/schemas/holdout_result.schema.json`

| Field | Definition |
|---|---|
| `expected_range` | Pre-registered `{min_sharpe, max_sharpe, rationale}` written BEFORE running holdout |
| `holdout_sharpe` | Window-Sharpe on holdout data; `null` when trade count < 5 (A3.4 null-floor) |
| `per_trade_expectancy` | `{mean_bps, se_bps, t_stat, n_trades}` — primary statistic for sparse strategies |
| `within_expected_range` | Whether holdout_sharpe fell within the pre-registered range |
| `status` | `pass`, `fail`, or `inconclusive` |
| `consumed_at` | ISO timestamp when holdout was spent (single-use enforcement) |

---

### `pre_registration.yaml`

> **Why this file exists.** It is the promise made *before* the data was
> looked at: what result would count as success, and what would count as
> failure. Without it, a verdict is written after seeing the numbers, which is
> how a kill quietly becomes a "learning".

**Created by:** `workflow/run_campaign.py` `_materialize_run()` (alongside `research_brief.yaml`)
**Updated by:** *(none — write-once; rewriting it after a run is the failure it exists to prevent)*
**Read by:** `tools/verdict_criteria_evaluator.py` via stage 8; `_load_machine_constraints()` (`run_phase1_research.py::_load_machine_constraints`) for the `protocol_execution` conformance gate, `run_phase1_research.py::_check_protocol_execution_conformance`
**Written to:** `runs/{run_id}/artifacts/pre_registration.yaml`
**Schema:** *(none)*

| Field | Definition — what it means | Values / range | Example (`run_060`, 2026-08-28) |
|---|---|---|---|
| `pass_rule` | The pre-registered success condition, structured so a machine can evaluate it rather than a human reading prose. | dict with `statement`, `window_set_ref`, `criteria[]`; **or absent** = legacy | `{statement: "PASS iff … BOTH BTCUSDT AND ETHUSDT satisfy: (a) median Sharpe > 0.8; (b) max abs drawdown < 30% …", criteria: [{id: a, metric: median_sharpe, metric_basis: bar_level, comparator: ">"}, …]}` |
| `machine_constraints` | Things pinned before the run that later stages must obey — not advice, but a contract the conformance gate checks. | dict: `protocol_ref`, `protocol_ref_content_hash`, `significance_methodology` | `{protocol_ref: protocols/funding_mr_4h_retest_v1.json, protocol_ref_content_hash: sha256:4fda1f39…, significance_methodology: episode_blocked_a851a}` |
| `expected_*` / `min_detectable_ic` / `plausible_ic_upper` / `power_verdict` | A-priori power figures recorded at registration on the legacy shape. No new run writes these fields. | floats / verdict string | present on the legacy shape (e.g. run_043) |
| `disconfirming_outcome` | Written in advance: what result would falsify the hypothesis. | prose | — |
| `run_id` / `hypothesis_id` / `registered_at` | Provenance. | string / string / ISO-8601 | `run_060` / … / … |
| `sample_split_design` | A6.1's holdout-range declaration, alongside `pass_rule` — written by `_materialize_run`/`_materialize_refinement_run` (2026-09-13; see the enforcement ledger, §8.2). | dict: `holdout_range` (the frozen `[start, end]` pair from `campaign_data_policy.yaml`), `holdout_note` | `{holdout_range: ["2026-01-01", "2026-06-30"], holdout_note: "Single-use per A6.1. Evaluated only at holdout_evaluation stage after the deflated Sharpe gate passes."}` |

**Notes**

- ⚠️ **Two shapes, and most of the corpus is the older one.** Measured
  2026-08-30 over the 10 files on disk: **7 have no `pass_rule` at all**
  (run_043–run_057) and only run_058/059/060 carry the structured dict.
  `machine_constraints` first appears at run_048. `sample_split_design` is
  newer still — written from 2026-09-13 forward, so it appears in 0 of these
  same 10 legacy files.
- The consequence is in [`pass_rule_evaluation.yaml`](#pass_rule_evaluationyaml)
  below: where `pass_rule` is absent the machine verdict returns
  `legacy_not_evaluable` and the LLM's judgment decides, exactly as before the
  K2 kernel. "The machine decides" is true for 3 of 10 runs.

---

### `pass_rule_evaluation.yaml`

> **Why this file exists.** It is the verdict a machine reached by checking the
> pre-registered rule against the result — computed before any LLM reads the
> backtest, so the interpretation cannot drift toward the answer someone
> wanted.

**Created by:** stage 8 `protocol_execution`, via
`tools/verdict_criteria_evaluator.py::evaluate_pass_rule_criteria()`
(`run_phase1_research.py::run_tool_worker`)
**Updated by:** *(none — write-once per run)*
**Read by:** `verdict_interpreter` — **a REQUIRED input**
(`workflow_artifacts/skills/verdict-interpreter/SKILL.md:16`). **E-018
(2026-09-13):** also read DIRECTLY by the orchestrator's own
`determine_post_verdict_route`/`determine_post_campaign_review_route` — when
`result` is binding (`PASS`/`FAIL`, not `discretion: stage`), its own
`hypothesis_verdict`/`lineage_routing` drive routing, not
`verdict_interpretation.yaml`'s restated copy.
**Written to:** `runs/{run_id}/artifacts/pass_rule_evaluation.yaml`
**Schema:** *(none)*

| Field | Definition — what it means | Values / range | Example (`run_060`, 2026-08-28) |
|---|---|---|---|
| `result` | The machine's overall verdict on the pre-registered rule. | `PASS` · `FAIL` · `legacy_not_evaluable` (no structured `pass_rule` to check) | `FAIL` |
| `criteria_results` | Per-criterion, per-symbol breakdown — so a failure names *which* clause failed on *which* symbol, not just that something did. | list of `{id, result, per_symbol: {SYM: {value, threshold, result}}}` | criterion `a`: BTCUSDT `value: -0.296` vs `threshold: 0.8` → FAIL; criterion `c`: PASS |
| `hypothesis_verdict` / `lineage_routing` | The routing the machine's verdict implies, when it is binding. | string | present when `result` is PASS or FAIL |
| `evaluated_at` / `evaluator_version` | Provenance. `2` since C7-EXT added the G1–G5 preconditions (2026-07-22). | ISO-8601 / integer | `2` |

**Notes**

- ⚠️ **This is the decision authority, not a second opinion.** Since the K2
  kernel (2026-07-13) it *replaced* `evaluate_against_decision_rules` in
  `tools/run_protocol.py`, whose prose-criteria output is informational only
  from that date. **Since E-018 (2026-09-13), routing is authoritative on
  this file directly** — a verdict_interpreter restatement that contradicts
  it is recorded as an informational flag, not a blocking conformance
  failure (see `verdict_interpretation.yaml` above).
- **It is only binding where a structured `pass_rule` exists.** On the legacy
  shape it returns `legacy_not_evaluable` and the LLM decides (R3 ruling) — see
  `pre_registration.yaml` above for how much of the corpus that is.

---

### `run_context.yaml`

> **Why this file exists.** It records what makes *this* run different from the
> brief it inherited — the escalation target, or the forced protocol — so a
> child run does not silently re-test its parent's asset.

**Created by:** `run_phase1_research.py::_ensure_protocol_from_constraints` (escalation spawn) and `::_ensure_protocol_from_constraints`
(forced-diagnostic override)
**Updated by:** *(none — write-once per run)*
**Read by:** the stage prompts; `_check_protocol_execution_conformance` compares its
bare-filename `protocol` key (`::_ensure_protocol_ref_pinned`)
**Written to:** `runs/{run_id}/artifacts/run_context.yaml`
**Schema:** *(none)*

| Field | Definition — what it means | Values / range | Example (real run) |
|---|---|---|---|
| `escalation_type` | Which axis was escalated when this run was spawned. | `instrument` · `timeframe` · `new_component` | `instrument` |
| `target_symbol` / `target_timeframe` | The override the child run must apply instead of inheriting the parent's. | symbol / timeframe | `SOLUSDT` / `4h` |
| `escalation_reason` | Why the escalation happened. | string | `hypothesis_family_exhausted` |
| `source_run` | The parent run. | run id | `run_027` |
| `protocol` | Bare filename of the [protocol](#g-protocol) this run is pinned to. Compared by basename, never by path. | filename | — |
| `note` | Instruction to the stages, in prose. | prose | *"Override the asset target to SOLUSDT — do NOT carry forward BTCUSDT or ETHUSDT…"* |

---

### `human_resolution.yaml`

> **Why this file exists.** It is the only way to restart a pipeline that
> paused for a human. Without it the run stays paused forever, and nothing else
> in the guide names it.

**Created by:** Human, by hand
**Updated by:** *(none — write-once)*
**Read by:** `resume_pipeline()` (`run_phase1_research.py::resume_pipeline`)
**Written to:** `runs/{run_id}/artifacts/human_resolution.yaml`
**Schema:** *(none)*

| Field | Definition — what it means | Values / range | Example (real run) |
|---|---|---|---|
| `status` | Whether the human considers the blocker cleared. Only one value resumes the run. | `resolved_proceed` resumes; anything else does not | `resolved_proceed` |
| `resolution_notes` | What was actually done, for the record. | prose | *"Data audit complete. Downloaded 1h Binance liquidation tick data… Verified >150 qualifying events for both BTC and ETH."* |
| `injected_context` | Facts the resolution supplies to the resumed stages. | dict | `{liquidation_data_path: data/historical/binance_liquidations_1h.parquet, verified_event_count_btc: "185", verified_event_count_eth: "162"}` |
| `run_id` / `hypothesis_id` | Provenance. | string | `run_0001` / `H-0001` |

**Which pauses need this file:** refinement with
`implementation_allowed: false` (stage 5), `component_gap` or an unknown status
from stage 6, `component_execution_error` or `regime_misattribution` at stage
11, and the holdout's missing-result pause (stage 13).

---

### `config/venue_tradability.yaml` *(config)*

> **Why this file exists.** It records which venue/market_type combinations this
> operator can legally trade *now*, so research on something untradable cannot
> reach a live-money decision by accident.

**Created by:** Human, from the venue survey
**Updated by:** Human, when the legal or venue position changes
**Read by:** `run_campaign.py::_load_venue_tradability()` (`::_load_venue_tradability`), used by
`_materialize_run()` to auto-flag `research_only` on any brief whose venue and
market_type are not `tradable: true` — **or are undeclared**
**Written to:** `config/venue_tradability.yaml`
**Schema:** *(none)*

| Field | Definition — what it means | Values / range | Example |
|---|---|---|---|
| `venues.<venue>.<market_type>.tradable` | Whether this operator may trade this market_type on this venue today. | `true` / `false` | `venues.kraken.spot.tradable: true` |
| `version` / `created_at` | Provenance of the table itself. | string / date | `"1.0"` / `"2026-07-21"` |

**Notes**

- Scope is **French non-professional retail**; it is not a general statement
  about the venue.
- Sources are named in the file header: `docs/analysis-reports/venue_survey_20260719.md`
  (+ 2026-07-20 supplement), the EEA perp fee verification session report, and
  the KB's `venue_live_tradability` field.
- **Undeclared resolves to not-tradable.** Silence is never a green light —
  the same rule the holdout's gate 2b applies.

---

### `research_decision.yaml`

> **Why this file exists.** The campaign's closing statement for a hypothesis:
> what was decided, why, and what the next person must not have to rediscover.
> It is the last thing written before a mechanism is closed, and the only place
> the whole trajectory across runs is recorded in one paragraph.

**Created by:** `campaign_review` / `verdict_interpreter` on a terminal outcome — the skill is instructed to emit it on `promote` or `kill` (`run_phase1_research.py::_create_remaining_handoffs`)
**Updated by:** *(none — write-once; it closes the entry)*
**Read by:** humans, and the next campaign's `existing_context`
**Written to:** `runs/{run_id}/artifacts/research_decision.yaml`
**Schema:** *(none)*

| Field | Definition — what it means | Values / range | Example (`run_060`, 2026-08-28) |
|---|---|---|---|
| `decision` | The terminal call on this hypothesis. | `kill` · `promote` | `kill` |
| `rationale` | Why, against the pre-registered criteria. A list when several criteria decided it. | prose or list | *"Prescreen IC gate failed (ic_active_bars=0.0162, p=0.5315 >> 0.10, not significant)."* |
| `findings_archive` | The numbers worth keeping, so a later run does not have to re-run to learn them. | dict keyed by run/window | `{run_060_4h: {ic_active_bars: 0.016237, ic_p_value: 0.5315, significant: false, …}}` |
| `mechanism_trajectory` | The whole arc across runs in one line — what was tried, in what order, and what each attempt showed. This is the field that stops a dead mechanism being re-proposed. | prose | *"1h (zero IC, lag confirmed) → 4h (zero IC, Nyquist-correct, no benefit) → daily (IC present but ret…)"* |
| `kb_entry_closure` | Which knowledge-base entry this closes, and which reactivation branches are now spent. | prose | *"parent_entry: funding_rate_continuous_mean_reversion_expanded_auto; reactivation_condition branches: …"* |
| `hypothesis_id` | Provenance. | string | `FUNDING_MR_4H_RETEST` |

**Notes**

- Only `hypothesis_id`, `decision`, `rationale` and `findings_archive` appear in
  both real files; `mechanism_trajectory` and `kb_entry_closure` are in run_060
  only. The shape is **skill-authored prose, not a fixed schema** — treat the
  field list as observed rather than guaranteed.
- Measured 2026-08-31: **2 on disk**, run_059 and run_060, the two most recent
  runs. It is a recent addition, which is why it had no entry until now — the
  same pattern as [E037-19](../engineering/roadmap/E-037/FINDINGS.md#e037-19).

---

### Config files (section 3 addendum)

| File | Purpose |
|---|---|
| `config/campaign_data_policy.yaml` | Frozen holdout range (2026-H1), burned ranges, `holdout_consumed_by` list |
| `config/cost_model.yaml` | Single source of truth for round-trip cost per symbol (bps); read by the post-backtest cost check and validation |
| `config/available_feeds.yaml` | Which data feeds are testable today; constrains `evidence_type` in hypothesis_card |
| `config/campaign_config.yaml` | Named constants for the orchestrator; drift-guarded by test |
| `config/indicator_library.yaml` | 15 seeded entries: regime_affinity, crowding_risk, data_requirements per indicator class |
| `feed_wishlist.yaml` | Feeds needed but not yet available (liquidation_data); argument for each. `trigger_condition.predicate` is a structured, machine-checkable expression evaluated by `workflow/run_campaign.py::evaluate_wishlist_predicate()` — no longer human-reviewed prose. `status`/`last_evaluated_at`/`last_evaluated_against`/`kb_state_hash`/`evaluation_note` are written ONLY by `evaluate_and_persist_wishlist_predicate()` (single authority — never hand-edit); a persisted `status` is only trustworthy if its `kb_state_hash` matches a fresh `sha256` of `campaign_knowledge_base.yaml`'s current bytes. See `RUNBOOK.md` section 3 and `docs/CONCEALMENT_INSTRUCTION_DOCTRINE.md`. |
| `campaign_record/detector_wishlist.yaml` | (In `config/` before D-077; an older checkout's copy there is still read.) Parked detector ideas (daily-timeframe overlay, ADX threshold, hidden Markov model). A list only: it gates and pauses nothing (D-052). A regime idea goes through the normal path with its ungated design variant. |
| `campaign_knowledge_base.yaml` | Durable findings store — see the file itself for the current count; this table doesn't track a point-in-time number. |
| `campaign_record/campaign_memory.yaml` | Per-run memory (E-058 S2a), written only by stage 17 `regroup_record` when `orchestrator.regroup_record.enabled` is on (off by default). One entry per `run_id`; fields in the stage 17 block. No old runs; those live in `campaign_knowledge_base.yaml`. |
| `campaign_record/data_requests.yaml` | Append-only `{requests: [...]}` intake of the feed-acquisition lane. Two writers, both through `run_phase1_research._append_data_requests`: the data-availability gate's per-variant declines (`stage: data_availability_gate`, `{run_id, stage, variant_id, outcome, reason, reasons}`; idempotent only under `verdict_routing_retired`), and (E-035 S2c) stage 16's `requires_feed` proposals (`stage: specialist_reader`, one row per feed that is not wired: `{run_id, stage, feed, request: acquisition|designation, proposals: [{category, proposal_id, reason}], reason}`, always idempotent on `campaign_review_retired.feed_request_key` = run, stage, feed; the gate's rows keep `request_key` = run, stage, variant, reason). Existing rows are never rewritten. Decide-next records its row count as information; the binding check is its own `requires_feed` feasibility gate. |
| `runs/<run_id>/artifacts/decision_record.yaml` | One decide-next decision (E-059 S2a), written by `run_campaign.py`'s DONE branch only when `orchestrator.decide_next.enabled` is on (off by default), from `tools/decide_next.py`. Inputs' hashes, R1/R2 (no-ops), candidates with gates/cost/rank, `picked` or `stop`. Schema `workflow_artifacts/schemas/decision_record.schema.json`. See §5 `run_campaign.py`. |
| `campaign_record/candidate_briefs/<id>.md` | The brief decide-next writes for the candidate it picked (E-059 S2a, same flag). No criteria on purpose: step 1a writes them. |
| `campaign_record/queued_cards/<run_id>/hypothesis_card_<n>.yaml` | A brief's extra hypothesis card, saved by the multi-card split under `orchestrator.decide_next.enabled` (E-059 S2b) and named by its queue entry's `card_ref`. Listed with its 1a scores in `runs/<run_id>/artifacts/queued_hypotheses.yaml`. |
| `runs/<run_id>/artifacts/brief_status.yaml` | Step 1a's "brief exhausted" signal (E-059 S2b, same flag): `{brief_status: exhausted, reason}` and no card -> terminal `completed_brief_exhausted`. |

---

## 4. Skills

> **Scope of this section.** The seven skills below are exactly the seven the
> orchestrator can dispatch — `_SKILL_MAP` in `workflow/run_phase1_research.py::_SKILL_MAP`,
> verified 2026-08-30. Three more exist under `workflow_artifacts/skills/` and
> are **not** dispatchable: `regime-auditor` (invoked by a human on a paused
> pipeline — see stage 10 and [E037-16](../engineering/roadmap/E-037/FINDINGS.md#e037-16)),
> `quant-fundamentals` and `research-system-evolution` (reference/strategic, not
> pipeline stages). `_build_stage_prompt` raises for any stage not in the map,
> so the seven below are an exhaustive list of automated stages, not a
> selection.


Skills are LLM persona prompts stored in `skills/{name}/SKILL.md`. Each [skill](#g-skill) defines a role, a checklist, constraints, and forbidden actions for a Claude agent acting as a specialist. The orchestrator loads the relevant skill at each stage and passes it as the system prompt. The agent has no tools (CUL-336, see §5 `run_phase1_research.py`): a skill line such as "read X" works only if X is in the stage's handoff inputs.

---

### `hypothesis-design`

**Goal:** Transform an open [research brief](#g-research-brief) into a single, concrete, testable [hypothesis](#g-hypothesis).  
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
**Why it exists:** Backtesting is expensive and noisy. Running a broken hypothesis wastes compute and pollutes [campaign](#g-campaign) history. This skill acts as a pre-flight check: if the idea cannot survive theoretical scrutiny, it should not enter the backtest queue.

Key outputs:
- A **[falsifiable statement](#g-falsifiable-statement)** (a single prediction that can be proven wrong).
- At least **5 failure modes** (named, specific failure scenarios).
- **Bias risks** (look-ahead contamination, selection bias, [regime](#g-regime) endogeneity).
- **Decision rules** (the exact conditions that trigger approve / refine / reject).
- **When its own verdict is `refine`:** a refinement plan, in the same response (`refinement_notes.yaml`) — E-039 S4 (2026-09-12) folded this in from a formerly separate `refinement-planner` skill/stage. Specific instructions, not vague suggestions: which parameter to change, which assumption to drop, which variant to prioritize. Also acts as a [circuit breaker](#g-circuit-breaker) — if the fix needs capabilities the bot doesn't have, it sets `implementation_allowed = false` and suspends the pipeline for human review.

The skill is explicitly forbidden from approving a hypothesis that has no falsifiable statement or fewer than 5 failure modes.

---

### `backtest-engineering`

**Goal:** Translate an approved, validated hypothesis into a `strategy_config` JSON that the trading-bot can execute verbatim.  
**Why it exists:** The hypothesis exists in conceptual form (thesis, signal formula, regime gate). The backtest engine needs exact parameters: lookback windows, thresholds, [component](#g-component) weights, regime definitions. This skill handles that translation, validates the output against `COMPONENT_CATALOG.md`, and flags any component that doesn't yet exist in the bot.

The skill is forbidden from:
- Bypassing regime gates.
- Inventing parameter values not derived from the hypothesis.
- Producing configs that reference non-existent bot components.

---

### `verdict-interpreter`

**Goal:** Read backtest diagnostics, identify root causes, and issue an [altitude](#g-altitude) decision.  
**Why it exists:** Raw backtest results (Sharpe = 0.2, drawdown = 18%) don't tell you *why* the strategy underperformed. This skill applies named diagnostic rules to map metric patterns to root causes, then prescribes the correct next action. Without this step, the system would either blindly retry failures or discard salvageable ideas.

The 6 diagnostic rules (applied in order, first match wins — see the skill file
for exact thresholds and the fuller set of amendments/improvements layered on
top, e.g. sparse-trader gates, prescreen-kill routing, regime attribution):

| Rule # | Condition | Prescribed action |
|---|---|---|
| 1 | Cost drag dominates (`cost_drag_pct > 80%`, `gross_pnl > 0`) | Slow the signal (longer component period) to reduce trade frequency; a `threshold_filter` dead zone is not allowed in `strategies` |
| 2 | Signal has no directional edge (`\|median_forecast_return_corr\| < 0.03`) | Pivot to a structurally different signal |
| 3 | Signal is inverted (`median_forecast_return_corr < -0.03`, significant) | Pivot to the reverse signal (cheap — same component, reversed logic) |
| 4 | Regime is uninformative | Pivot to a different regime definition (after ruling out a sample-size issue) |
| 5 | Signal works but regime fires too rarely | Relax regime thresholds, or switch to a more-frequent regime |
| 6 | No diagnostic signal (all metrics null) | Distinguish instrumentation failure vs. genuine regime starvation before deciding |

Also produces **parameter brackets**: if refinement is prescribed, the skill narrows the search range [min, max, step] so the next [run](#g-run) doesn't blindly retry the same value. See `workflow_artifacts/skills/verdict-interpreter/SKILL.md` directly for the current full rule set — this table is a map, not the authority.

---

### `campaign-review`

**Goal:** After multiple hypothesis families have failed, step back and assess whether the campaign direction is still sound.  
**Why it exists:** The per-run verdict_interpreter only has local context. After 2+ families fail, the system needs a higher-level question: is this research question fundamentally unanswerable with current data/components, or just poorly explored? [Campaign review](#g-campaign-review) can reframe the question, target a new instrument, or terminate the campaign entirely — decisions no single-run skill can make.

Key outputs:
- A campaign-level `continue / reframe / escalate / terminate` decision.
- If reframe: a new research_brief for the next run.
- If terminate: a final `research_decision.yaml` with lessons learned.

---

## 5. Tools & Scripts

### `workflow/run_campaign.py` — Multi-Run Campaign Wrapper

Thin wrapper around `run_phase1_research.py` (below): pulls the next `ready`
brief from `config/campaign_queue.yaml`, launches it, follows its lineage
through reframe/escalation, and either advances to the next brief or halts on
a hard-pause condition — without a human re-invoking the orchestrator between
runs. Also owns `evaluate_wishlist_predicate()`/`evaluate_and_persist_wishlist_predicate()`
(mechanical wishlist-trigger evaluation, single-authority persistence — see
the config-files table above). Full operating detail: `RUNBOOK.md`.

**Decide-next (E-059 S2a, off by default: `orchestrator.decide_next.enabled`,
requires `regroup_record` and `config_direct_authoring`).** When a lineage
finishes -- the DONE branch, or the E-030 quarantine path that marks it done --
the finished entry's `outcome` becomes the grid's `idea_status`, citing
`runs/<run_id>/artifacts/idea_status.yaml` (the queue's provenance gate refuses
the flag-off `completed_rejected` with no reference; a run that ended before
the grid keeps its stage outcome, declared `verdict_status: ungated`). Then
`tools/decide_next.py` decides, and only AFTER the decision record (and any
new queue entry) is on disk is the finished entry saved as `done` -- a failure
leaves it `in_progress`, so the next step retries. The record
(`runs/<run_id>/artifacts/decision_record.yaml`) says:
- whatever `_select_entry` will run next if it still has an `in_progress` or
  `ready` entry (operator entries therefore go first; nothing is minted);
- else the best eligible reader proposal (from the runs in
  `campaign_record/campaign_memory.yaml`) becomes ONE `ready` agent entry
  (`source: agent`, `origin: reader`, `priority: 999`, `proposal_ref`,
  `decision_ref`, no `relation`), with a brief in
  `campaign_record/candidate_briefs/<proposal_id>.md` (its id must be a safe
  `<category>-<source run>-<n>` name that collides with no queue id or brief);
- else the loop stops (`DECIDE stop`, RUNBOOK §3 last row).

Under `orchestrator.verdict_routing_retired.enabled` (slice 6c S2a) every run
ends `completed_<idea_status>`, so this DONE branch runs after every
validated, refuted and inconclusive idea, and a legacy continuation
(`completed_refined|reframed|escalated` with a `continuation_child`) halts
the step instead of being followed
(`legacy_continuation_under_retired_routing`). When the run's campaign review
said `reframe` (slice 6c S2b), its brief is registered first, as a `ready`
entry with `origin: campaign_review` (`_register_campaign_review_reframe`,
idempotent on a retried step); decide-next then records the pick, and an
operator `ready` entry still goes first.

Novelty is the exact match against the memory, binding: config hash, measured
symbols, the protocol file's timeframe (normalised) and a content hash of its
windows -- never the per-run protocol path (`tools/novelty.py`, shared with
the stage-6 exact-match check); the legacy exclusion digest is recorded, never
refuses. Feasibility makes a candidate `INFEASIBLE` (ineligible, still listed
in the record with its `reasons`) when: its id is unsafe or collides with a
queue id or brief (`unsafe_proposal_id`, `queue_id_collision`,
`brief_collision`); the source run has no protocol pin or brief
(`source_has_no_protocol_pin`, `source_brief_missing`); a patch's source is
untested, missing or does not resolve (`source_base_variant_not_tested`,
`source_config_missing`, `source_manifest_missing`, `patch_unresolvable`,
`stale_before`, `manifest_unresolved`, `composition_check_failed`,
`unknown_component_class`); a sketch is a regime block
(`regime_block_needs_composition`); or (E-035 S2c) its proposal carries
`requires_feed`, the feed is not wired, and the candidate would read it --
reason `requires_feed_reserved:<feed> -- ...` for a reserved feed (needs a
data-policy designation) or `requires_feed:<feed> -- ...` otherwise (needs
an acquisition, or no feed set was supplied). Reasons name only the missing
feed, so an unrelated registry change never rewrites them. "Would read it":
the patch's resolved config lists the feed in `aux_feeds` or uses a component
class whose `consumes_feeds` names it (`decide_next.config_feeds`); a patch
whose resolved config reads neither is not blocked (its request row is still
filed at stage 16), and a new_block -- no config before 1b -- always counts
as reading it. The layering is deliberate: decide-next checks only that the
feed is WIRED (a `FEED_REGISTRY` key of `trading-bot/data/feed_registry.py`,
classified as the data-availability gate does -- reserved first); whether a
wired feed covers the run's venue, symbols and windows stays that gate's
check at stage 14, which parks the run `waiting_for_data` under slice 6c S2c.
The registries and the components' `consumes_feeds` are read with ast
(`decide_next.load_feed_set`) only when some proposal carries `requires_feed`,
and then an unreadable file stops the decision (retried like any decide
failure); the record's `inputs.feed_set_sha256` is written only then. Such a
candidate stays in the pool and is re-checked at every decision; its
`gates.feasibility.requires_feed` records `{feed, status, consumed,
available, reason}`, and when picked its brief's goal says which feed it
needs. Candidates without `requires_feed` are unchanged.
Ranking (after collapsing eligible duplicates on that
key): `confidence_real` desc, `distance_to_profitable` desc, cost (backtests)
asc, id asc; no lineage demotion. Scores only rank and appear only in the
decision record. A picked candidate is a new idea (`<parent>__<proposal_id>`)
that enters step 1a: its brief carries **no criteria**; `_materialize_run`
writes `pre_registration.yaml` with `pass_rule: null` + `pass_rule_pending:
hypothesis_generation`; run_loop defers the readers pre-flight; 1a gets the
addendum `workflow_artifacts/skills/hypothesis-design/DECIDE_NEXT_CANDIDATES.md`
(flag on only); and after EVERY completion of 1a `_write_pass_rule_from_card`
rebuilds the pass_rule from the current card's menu criteria (only `id` plus a
menu entry's `card_overridable` fields; K3 lint; pre-flight). The marker is
dropped once the run moves past 1a. A patch's resolved config passes through
to 1b; 5a stops if its hash differs from `candidate.source.expected_config_sha256`.
The patch's block manifest is written by code from the brief's `candidate.manifest`
when 1b answers `spec_ready` (CUL-405, D-074); 1b's own manifest, if any, is
replaced, so a 1b edit of its free-text `rationale` cannot refuse the run. The
patch card's claim is checked and measured like any card's (CUL-406). New
queue fields (closed schema, `tools/record_schema.py`): `origin`,
`proposal_ref`, `decision_ref`, `card_ref`, `brief_status`, `parked_reason`,
and status `queued` (never auto-picked).

**Briefs, brief status and R2 (E-059 S2b, same flag).**
- `python workflow/run_campaign.py register ...` while the flag is on writes
  `brief_status: open` on the new entry: it owns that brief. An entry with no
  `brief_status` is a **legacy brief** (operator decision 7): it never
  triggers R2, and at the first decision after the flag is on its queue entry
  gets a one-time `title: "[obsolete] <brief's first '# ' heading, else the
  id>"` (shown next to the id in `campaign_summary.md`). Only the queue entry
  is written; the brief file is never edited. Tagging changes no status and
  nothing the scheduler picks.
- A brief run (anything launched fresh that is not a reader candidate) gets
  `runs/<run_id>/artifacts/brief_hypotheses_context.yaml` (the hypothesis ids
  this brief already produced). Its presence gives step 1a the addendum
  `workflow_artifacts/skills/hypothesis-design/BRIEF_HYPOTHESES.md` (flag on
  only; `SKILL.md` is unchanged, so the flag-off prompt is byte-identical).
- **Several cards** from 1a: card 1 runs now; cards 2..k are copied to
  `campaign_record/queued_cards/<run_id>/`, listed with the three anchored
  scores 1a wrote for each (`artifacts/extra_card_scores.yaml`, rubric
  `brief-card-v1`) in `artifacts/queued_hypotheses.yaml`, and registered as
  `queued` entries `<entry>__h<n>` (`origin: brief`, `card_ref`, `source:
  agent`, priority 999). No sibling run and no `hypothesis_splits` row. A
  missing/malformed score, or several cards from a reader candidate, fails
  the run. When decide-next picks one (it ranks on the same key as a
  proposal), it is flipped `queued` -> `ready`; its launch copies the card and
  starts after 1a (`strategy_config_authoring`), so it is never re-authored.
- **Exhausted**: 1a writes no card and `artifacts/brief_status.yaml`
  `{brief_status: exhausted, reason}` -> the run ends
  `completed_brief_exhausted` (a non-verdict outcome, no provenance needed) and
  the brief's owner entry is flipped to `brief_status: exhausted`.
- **R2**: when nothing is scheduled and no candidate is eligible, decide-next
  asks 1a for more hypotheses on every eligible `open` brief: it reuses that
  brief's waiting request or mints `<owner>__more_<n>` (`origin: brief`, no
  `card_ref`), and EVERY such request is `ready` (no brief waits behind
  another; the scheduler's priority order applies). An owner that is
  superseded, `paused:*` or `blocked_*` gets no request. The loop stops only
  when no eligible brief is open.
- **R2 terminates** (code-review fix 1): a card whose `hypothesis_id` the
  brief already produced is rejected. In the multi-card path it is dropped
  (listed under `rejected` in `queued_hypotheses.yaml`); when no new card is
  left, or a single card repeats, the run ends `completed_no_new_hypothesis`
  before 1b (`artifacts/brief_repeat.yaml`). An open brief whose last
  `decide_next.BRIEF_MAX_CONSECUTIVE_EMPTY_R2` (= 2, operator-adjustable)
  finished R2 requests all ended without a new, eligible card -- no new
  hypothesis, quarantined, failed/paused, or superseded -- is flipped to
  `brief_status: exhausted` with `brief_status_reason: no_new_hypothesis`
  (`step_1a_reported` when 1a said so itself).
- **Ambiguous 1a output fails the run**: `hypothesis_card.yaml` together with
  `hypothesis_card_<n>.yaml` or `extra_card_scores.yaml`; a score item naming
  no card file; a rubric other than `brief-card-v1`; an exhausted signal next
  to cards (checked before anything is copied). Extra cards are enqueued only
  from a run whose 1a completed and that did not fail. Legacy briefs get no
  brief context, hence no addendum; one that writes several cards fails.
- **A picked card whose file is missing** pauses its entry
  (`paused:queued_card_missing`) before any run dir is created.

**Launch pre-flight and the stage-exception pause (E-061 C1.4 / C1.5).** Every
refusal below is a classified pause -- `paused:<reason>` on the entry, a `HALT`
line naming the culprit, a `halt_history` record when a run exists, and
`process_once` returning False -- never a crashed campaign process that a
restart re-crashes, and never after an LLM call. `docs/RUNBOOK.md` §3 has one
row per reason with its resolution.

1. **Flags, on every step, before anything launches** (`_flag_preflight`):
   `config/campaign_config.yaml` is parsed once and handed to every real flag
   reader (`_flag_readers`; each reader takes an optional parsed `cfg`, so the
   readers are the single source of the rules and `process_once` takes its own
   schedulability / decide_next / verdict-routing values from that one
   reading). Every `orchestrator.<name>.enabled` and
   `halt_policy.quarantine_enabled` must be a real YAML boolean (a quoted
   `"false"` or a null is refused, every offending key named), and every flag
   dependency must hold -- each reader's own chain, plus the edges once
   enforced only after spend (A3 §1): `variant_loop` → `config_direct_authoring`,
   `composition_runs` → `decide_next` + `variant_loop` +
   `profit_bars_every_backtest` + `verdict_routing_retired`, and
   `variant_anti_adjacency_gate` → `regroup_record` while
   `campaign_memory.yaml` does not exist (→ `variant_selection_record` on the
   legacy path). Refused: `paused:flag_misconfiguration`, before `setup_run`
   for a fresh entry. `--resume` re-runs the check. The seven readers that used
   plain `bool()` (`grid_evaluation`, `category_reports`, `profit_bars_file`,
   `exclusion_digest_input`, `stale_input_path_fix`, `variant_selection_record`,
   `variant_anti_adjacency_gate`) and `schedulability_block` now use the one
   strict check (`_strict_orchestrator_flag`); an unquoted boolean or a missing
   key reads exactly as before. `register` reads `decide_next`'s own value
   only, so a misconfigured prerequisite is refused here, not by a crash at
   registration.
2. **The protocol the run will execute, before `run_loop`**
   (`_protocol_preflight`): a `machine_constraints.protocol_ref` pin, or --
   with neither pin nor generated protocol -- the protocol
   `tools/protocol_resolution.resolve_protocol_path` selects from
   `run_context.yaml` or a claimed `campaign_state.last_escalation` (no state
   write), must pass the D-3 guard (`assert_promotion_ratified`) -- previously
   first checked at 5a, after 1a/1b/2. For a generated protocol
   (`machine_constraints.protocol`, `_generated_protocol_plan`) spend is
   checked FIRST: once data may have been spent on the run (a trial row, any
   `protocol_result*`, or `protocol_execution` ever entered) the expected
   protocol is never rebuilt and nothing is regenerated -- only the existing
   generated file gets the D-3 check (a missing one is refused; after
   `protocol_execution` completed nothing is checked). Before any spend it
   must be generatable from `pre_registration.yaml`
   (`_expected_generated_protocol` raises exactly where generation raises;
   refused otherwise, before anything is touched), and only a
   `promotion`-only difference from the file is regenerated
   (`_regenerate_protocol`: temp file + `os.replace`, the fields logged) -- a
   `windows` / `symbols` / `timeframe` / `holdout` difference is refused.
   Refused: `paused:protocol_promotion_unratified`, the run `paused_for_human`
   with the reason in `last_error`.
3. **An exception escaping `run_loop`** (or the step in 2): the split /
   queued-card bookkeeping runs (if it fails too, the queue is re-read from
   disk, missing split siblings are re-added, and a paused entry no longer in
   the file is never saved back), then the run is `paused_for_human` with
   `last_error: "<Type>: <message>"` and `flags.stage_exception: true`, the
   entry `paused:stage_exception`. **An exception while launching** (the
   brief, `setup_run`, the materialization and its lints, the brief context,
   the queued card): `paused:launch_exception`; the entry is restored to its
   pre-launch state and records `launch_failed_run_id` (or null),
   `launch_exception_detail` and `launch_prior_status`; a run dir already
   created is marked `status: abandoned_launch` (known to `reconcile_orphans`,
   skipped by every `runs/run_*` knowledge scanner -- the exclusion digest, the
   near-miss scoreboard, the replay repeat gate -- never added to `run_ids`);
   `--resume` relaunches the entry with its pre-launch status.
   `KeyboardInterrupt` / `SystemExit` pass through. Exceptions after
   `run_loop` returned (the DONE branch's decide-next) still propagate: that
   path is retryable by design.
4. **Classification and un-pausing**: the three run flags (`stage_exception`,
   `protocol_promotion_unratified`, `launch_exception`) rank above the
   artifact-based reasons in `_classify_human_pause` (a fresh halt wins over an
   old artifact), and every un-pause path (`--resume`, `--unpark`,
   `resume_pipeline`) clears them (a stale one never masks a later holdout
   step). The `data_block_hitl` resume reads `human_resolution.yaml` first,
   inside the classified handling (a malformed file keeps the entry
   `paused:data_block_hitl`): anything but `resolved_proceed` only closes the
   run (no pre-flight). `resolved_proceed` runs 1 and 2 (and a pre-spend
   regeneration) before `resume_pipeline`; a refusal -- or an exception in
   them -- keeps the entry `paused:data_block_hitl` (the error in
   `last_error`, a HALT line), and an exception from `resume_pipeline` itself
   is a `stage_exception` pause (schedulability.yaml still written when its
   block is on).

With a valid flag set and a ratified (or no pre-registered) protocol, 1 and 2
are read only and the step is unchanged (the one write is regenerating, before
any spend, a generated protocol whose promotion block alone was changed in its
pre-registration).

### `tools/fragment_patterns.py` — Ideation-Only Fragment Diagnostics

Computes `fragment_patterns.yaml` from a completed [run](#g-run)'s `trades.json`/`bars.csv`:
forecast-bin outcome tables, entry/exit [component](#g-component) attribution, initial-entry-
vs-scale-up cost comparison, duration/[regime](#g-regime) cross-tabs. Strictly ideation-only
— never a decision-path input (mechanically enforced, see
`tests/test_fragment_patterns_firewall.py`). This is the "diagnosis" role in
the three-role model for fragment data: `docs/VERIFICATION_DOCTRINE.md`
section 2.

### `workflow/run_phase1_research.py` — Pipeline Orchestrator

The central state machine. Manages the entire lifecycle of a run.

**Responsibilities:**
- Loads/saves `pipeline_state.yaml` and `campaign_state.yaml` at every transition.
- Invokes skills by building prompts from [handoff](#g-handoff) files + [skill](#g-skill) personas and sending them to the Claude SDK or Gemini API.
- **Stage agents run closed-book (CUL-336, 2026-09-27).** Every Claude stage call (`run_claude_worker` and the five specialist readers) uses the options from `_stage_agent_options()`, the only place they are built: `tools=[]` (no built-in tool: no Read, Grep, Bash, Web…), `setting_sources=[]` (no user/project/local settings file, so no machine's permission allow rules and no CLAUDE.md), `strict_mcp_config=True` (no MCP server), `env={"CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1"}` (the bundled CLI loads the auto-memory `MEMORY.md` — keyed on the cwd's git root, i.e. the operator's own session memory for this repository — behind this env var and settings/feature flags, not behind `--setting-sources`), and `cwd` = one fixed empty directory in the system temp dir (`strategy_research_stage_agent_cwd`), outside any repository; the prompt itself is still assembled in-process, so nothing depends on the agent's cwd, and stage transcripts now sit under `~/.claude/projects/<that dir's key>/`. The agent sees its prompt and nothing else, so every file a stage needs must be in its handoff's `required_inputs`/`optional_inputs`. Before CUL-336 the calls passed only `allowed_tools=[]`, which in claude_agent_sdk 0.2.82 sends no flag at all, so stages had the CLI's default tools and a run_060 validation agent read two config files on its own (E-035 S1_FINDINGS §1.2). The files stage skills tell the agent to read and no handoff delivered are now added by `_apply_closed_book_inputs` (`_CLOSED_BOOK_STAGE_INPUTS`): `config/cost_model.yaml` for validation, `config/coin_universe.yaml` for innovation_expansion and verdict_interpreter, `quant-fundamentals/SKILL.md` for backtest_specification, strategy_config_authoring, verdict_interpreter and campaign_review, `campaign_record/campaign_state.yaml` and a trade-diagnostics summary for verdict_interpreter, plus conditional run artifacts (see each stage's "Stage input"). A test (`test_every_skill_reference_is_delivered_or_waived`) fails when a stage skill names a repo path, or lists a "Required inputs" item, that no handoff delivers and no waiver explains. `max_turns` is not set: with no tools a stage is one turn by construction, and `num_turns` in the audit log shows it.
- Routes between stages based on [artifact](#g-artifact) contents (e.g., reads `validation_decision.yaml.status` to decide next step).
- Enforces circuit breakers (refinement budget, token budget, [altitude](#g-altitude) escalation logic).
- Tracks token usage and cost per stage in the [audit log](#g-audit-log).
- Includes iterative YAML repair: if a model produces malformed YAML, it attempts up to 3 auto-repairs before halting.
- Supports **resume**: a human-paused run can be restarted mid-pipeline without re-running completed stages.

### `workflow/setup_run.py` — Run Scaffolder

Creates the directory structure for a new run: `runs/{run_id}/artifacts/`, `runs/{run_id}/handoffs/`, and copies handoff templates. Called automatically by the orchestrator when starting a new run.

### `workflow/stages.yaml` — ARCHIVED 2026-08-24 (never read by the orchestrator)

**Corrected 2026-08-24. The previous text here said "the orchestrator reads
this file — adding a new stage means adding an entry here plus a skill file,
with no orchestrator code changes." That is false and had been false for some
time.** Verified by grep across `workflow/` and `tools/`: `stages.yaml` is
never loaded by any code. Every reference to it is a source comment mentioning
it. There is no `yaml.safe_load` of this file anywhere in the workflow.

What actually drives the pipeline:

| Concern | Real source |
|---|---|
| Which stages exist, and their default next | `STAGE_CONFIGS` (`workflow/run_phase1_research.py`) — **10 stages**, vs 14 declared in `stages.yaml` |
| What a stage receives | the handoff templates in `workflow_artifacts/templates/handoffs/` |
| Conditional routing | the `determine_post_*` functions in `run_phase1_research.py` |
| A stage's behaviour | its skill file under `workflow_artifacts/skills/` |

Consequences of the drift, both found on 2026-08-24: `stages.yaml` declares a
`research_brief` stage whose `next` is `hypothesis` — no such stage exists (the
real one is `hypothesis_generation`). It is harmless *because* nothing reads
`next`, but it is the kind of error a file nobody validates accumulates. It
also declares `anti_adjacency_gate`, which is real but is dispatched by inline
routing rather than from this registry.

**The file was MOVED OUT of `workflow/` on 2026-08-24** to
`engineering/roadmap/E-033/artifacts/stages_yaml_ARCHIVED_not_authoritative.yaml`,
because a wrong, unread file sitting in `workflow/` reads as operational
regardless of any banner. E-033 S2 decides whether it is revived as the real
registry or deleted. **Treat it as a historical design sketch** (make it genuinely authoritative — see also E-009's `STAGE_CONFIGS`/
`skill_map` merge — or remove it). Do not add a stage here and expect it to
run.

### `tools/run_protocol.py` — Walk-Forward Executor

A fully deterministic tool — no LLM call, no token cost. Not the only one:
`validate_regime_detector.py`, `deflate_sharpe.py` and `episode_significance.py`
all run without an LLM too (measured: zero LLM imports in each).

Given a `backtest_spec.yaml`, it:
1. Loads the [protocol](#g-protocol) definition (`protocols/baseline_v1.json` or an escalation protocol).
2. Runs the trading-bot backtest engine across each walk-forward window.
3. Aggregates per-window metrics (Sharpe, drawdown, trade count, win rate).
4. Evaluates promotion/[kill](#g-kill) thresholds.
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

**The four above are 4 of the 13 protocols on disk.** The rest, added since this
table was written:

| File | Purpose |
|---|---|
| `baseline_v2.json` | The protocol behind the **`keltner_163`** fixture that §7 names as the standing known-answer fixture — referenced in this guide's prose but, until now, absent from this table |
| `funding_mr_4h_retest_v1.json` | The 4h funding mean-reversion retest; the protocol run_060 actually executed |
| `funding_mr_daily_retest_v1.json` | The daily arm of the same mechanism |
| `ts_trend_daily_v1.json` | Daily trend-following |
| `h041c_v2_backext.json` | Backward-extended window set |
| `escalation_tf_15m.json` | Timeframe escalation to 15m |
| `run_048_generated.json`, `run_050_generated.json`, `run_053_generated.json` | Per-run protocols generated by `_ensure_protocol_from_constraints` when a brief pins its own window set |

⚠️ **`baseline_v1.json`'s description was verified and is exactly correct** —
BTCUSDT + ETHUSDT, 1h, 11 monthly windows 2024-01 to 2024-11. Checked against
the file, not assumed.

---

### Tool inventory — everything in `tools/`

The entries above cover 3 of the **21** Python files in `tools/`. The rest are
listed here so the section is a complete index rather than a selection. Ordered
by how load-bearing they are, not alphabetically.

**Run the pipeline**

| Tool | What it does |
|---|---|
| `tools/run_protocol.py` | Walk-forward executor for stage 8 *(documented above)*. |
| `tools/verdict_criteria_evaluator.py` | **The K2/C7 machine [verdict](#g-verdict)** — scores a run against its pre-registered `pass_rule` and writes `pass_rule_evaluation.yaml`. Since 2026-07-13 this is the decision authority, not an advisory. |
| `tools/episode_significance.py` | The A8.5.1a episode-blocked significance path. Used by `run_protocol.py` (stage 8, CUL-265), where it is computed unconditionally as an **additive** second opinion pooled across a symbol's windows — it never replaces `median_forecast_return_corr`. |
| `tools/timeframe.py` | Timeframe arithmetic, **derived rather than enumerated** — the single source of `bars_per_day`. A lookup table here was the 4h `n_eff` bug. |
| `tools/validate_regime_detector.py` | Stage 9's detector validation; computes the A2.2 metrics. |
| `tools/retune_regime_detector.py` | One-shot grid search over `(ER_enter, ER_exit, min_dwell)`. Scoring is detector-intrinsic only — the A2.2 retune firewall in tool form. |

**Gate promotion**

| Tool | What it does |
|---|---|
| `tools/deflate_sharpe.py` | Bailey & López de Prado deflated Sharpe — the gate between a good backtest and the holdout. Also where duplicate [trial](#g-trial) IDs are mechanically refused. |
| `tools/lint_verdict_provenance.py` | Standalone G6 provenance checker (C7-EXT-R / D-4), deliberately separate from the evaluator. |
| `tools/stamp_protocol.py` | Version-stamps a protocol JSON and prints its content hash, for the `protocol_ref_content_hash` pin in `pre_registration.yaml`. |
| `tools/record_schema.py` | Closed [schema](#g-schema) for `campaign_knowledge_base.yaml` findings and `config/campaign_queue.yaml`. |

**Flag-gated stages** *(see the flag table in §3 — all currently off)*

| Tool | What it does |
|---|---|
| `tools/anti_adjacency_gate.py` | The exact-match repeat check at stage 6 (E-036 S2a): REPEAT/NOVEL against `campaign_memory.yaml`; KB check advisory only. |
| `tools/novelty.py` | The one exact-match key and lookup (config hash, symbols, protocol timeframe + windows hash), shared by `decide_next.py` and the stage-6 check. |
| `tools/build_exclusion_digest.py` | LEGACY family-grain digest of what has been tried: the stages' prompt input while no `campaign_memory.yaml` exists, and decide-next's informational `digest_advisory` (`legacy_family_lookup`). Never a refusal signal. |

**Data and measurement**

| Tool | What it does |
|---|---|
| `tools/check_data.py` | Data validator *(documented above)*. |
| `tools/cache_gap_census.py` | Timestamp-continuity census over the local OHLCV caches. Written for the issue #50 policy decision — **this, not `gap_skipped_pct`, is the cache's contamination rate**. |
| `tools/measure_bar_sigma.py` | Per-bar return volatility in bps for a recorded pair set. |
| `tools/measure_funding_carry.py` | Realized funding-carry magnitude, in-sample window only, read-only. |

**Analysis and reporting**

| Tool | What it does |
|---|---|
| `tools/fragment_patterns.py` | Ideation-only fragment diagnostics *(documented above)*. |
| `tools/near_miss_scoreboard.py` | Ranked table over every tested idea (E-018 S1) — the campaign's "what came closest" view. Re-run manually (`python tools/near_miss_scoreboard.py`, idempotent); not auto-triggered per run. Since E-018 S2 (2026-09-13), `verdict_interpreter` reads its output unconditionally (see stage 11 item 9) — the only reviewed exception to the "promotion has no read access" doctrine. |
| `tools/panel_backtester.py` | **RESEARCH-ONLY** vectorized panel backtester. Explicitly *not* part of the production engine; results from it are not comparable with `run_protocol.py` output. |
| `tools/whale_footprint_evaluation.py` | Evaluation harness for `prereg_whale_footprint_v2.yaml`. |

> **Why this list matters.** Before it, §5 documented three tools. The tool
> that produces the decision authority (`verdict_criteria_evaluator.py`) was
> absent, while `workflow/stages.yaml` — archived and read by nothing — had a
> full entry.

---
## 6. Glossary

Campaign-level vocabulary. For the terms used when reading a **stage** — IC,
active bar, effective sample, episode, bps, Fisher z, block bootstrap, warmup,
turnover, firewall, upsert — see
[**Terms used throughout this section**](#22x-stage-detail-blocks) in §2.2,
which explains each in one line without jargon.

> ⚠️ **Two entries are marked ⚠️ because they describe fields that are not on
> the artifact their definition names.** `Parameter Bracket` and
> `Diagnostic Rule` are both defined as products of `verdict_interpreter`; they
> appear **0 times** in `verdict_interpretation.yaml` and live instead in
> `findings_carryover.yaml` (14 and 31 files). The concepts are real, the
> attribution is not. See
> [E037-22](../engineering/roadmap/E-037/FINDINGS.md#e037-22) and
> [E037-30](../engineering/roadmap/E-037/FINDINGS.md#e037-30).

> **On stage counts.** This guide documents **13** stages (§2.2); ten of
> those are the engine's `STAGE_CONFIGS` registry, which excludes the human
> brief and the two regime stages (`regime_detector_validation`,
> `regime_auditor`).

| Term | Definition |
|---|---|
| <a id="g-campaign"></a>**Campaign** | A sustained research effort around a single research question, spanning multiple runs and hypothesis families. A campaign ends when a strategy is promoted or the question is declared unanswerable. Example: "Can volume-based signals generate edge on BTC 1h?" |
| <a id="g-run"></a>**Run** | One complete execution of the pipeline for a specific hypothesis — 13 documented stages ([E037-15](../engineering/roadmap/E-037/FINDINGS.md#e037-15)), of which 10 are dispatched by the orchestrator's `STAGE_CONFIGS` (the other three: `research_brief` is a human input, `regime_detector_validation` is a helper function, `regime_auditor` is a human-invoked skill on a paused pipeline). Each run lives in `runs/{run_id}/` and produces its own set of artifacts. A campaign contains many runs. |
| <a id="g-research-brief"></a>**Research Brief** | The entry document for a run. Written by a human (or auto-generated from a previous run's proposed_brief), it defines the research question, target market, constraints, and what has already been tried. |
| <a id="g-hypothesis"></a>**Hypothesis** | A single, falsifiable claim about a trading signal: what it is, why it should work, and under what conditions. More specific than a "strategy idea" — it must include a signal formula and explicit assumptions. |
| <a id="g-hypothesis-family"></a>**Hypothesis Family** | A group of related hypotheses that share a core thesis but differ in implementation (e.g., all volume-momentum variants). If all variants in a family fail, the family is marked exhausted and excluded from future runs. |
| <a id="g-innovation-expansion"></a>**Innovation Expansion** | The stage that multiplies a single hypothesis into a family of variants. Not random creativity — it follows a structured template: reverse, behavioral, regime-specific, alternative-data. |
| <a id="g-falsifiable-statement"></a>**Falsifiable Statement** | A prediction specific enough to be proven wrong by data. Required before any backtest. Example: "When momentum > 0 AND vol_ratio > 1.5, next-bar close is higher at least 55% of the time." Without this, a hypothesis cannot be rigorously tested. |
| <a id="g-validation-gate"></a>**Validation Gate** | The pre-backtest quality check. An LLM agent acts as a skeptical quant and tries to find reasons to reject the hypothesis before any compute is spent. Passes → backtest. Fails → refine or reject. |
| <a id="g-walk-forward-test"></a>**Walk-Forward Test** | A backtesting methodology where the model is evaluated on sequential, non-overlapping out-of-sample windows. Prevents overfitting by ensuring no window's results are used to tune the strategy. The baseline protocol uses 11 monthly windows. |
| <a id="g-holdout-period"></a>**Holdout Period** | A final date range deliberately kept separate from all walk-forward windows. The strategy is never tuned on holdout data. It is only tested once, at the very end, to get an unbiased performance estimate. |
| <a id="g-protocol"></a>**Protocol** | A JSON specification of the backtest conditions: which symbols, which timeframe, which windows, and what thresholds trigger promote/kill. Separating protocol from strategy config allows the same strategy to be tested under different conditions. |
| <a id="g-altitude"></a>**Altitude** | A measure of how far from the original hypothesis the next search step will move. Altitude 1 = parameter tweak (same hypothesis). Altitude 2 = new hypothesis family (same question). Altitude 3 = new instrument or timeframe (same methodology). Higher altitude = larger change. |
| <a id="g-verdict"></a>**Verdict** | The final word from the verdict_interpreter after a backtest: `refine`, `pivot`, `escalate`, `promote`, or `kill`. Each verdict maps to an altitude and a next action. |
| <a id="g-refine"></a>**Refine (altitude 1)** | Adjust a specific parameter of the current hypothesis based on diagnostic findings. The hypothesis family stays the same. Example: raise the threshold filter from 0.5 to 1.0. |
| <a id="g-pivot"></a>**Pivot (altitude 2)** | Abandon the current hypothesis family and start a new one. The research question stays the same. Triggered when diagnostics show the core signal has no predictive content. |
| <a id="g-escalate"></a>**Escalate (altitude 3)** | Keep the methodology but test it on a different symbol or timeframe. Triggered when the signal shows theoretical promise but the current market environment doesn't support it. |
| <a id="g-promote"></a>**Promote** | Terminal positive verdict. The strategy passed all validation gates, walk-forward windows, and (optionally) holdout. It is added to the campaign's approved strategy list and handed off to the deployment pipeline. |
| <a id="g-kill"></a>**Kill** | Terminal negative verdict. The hypothesis (or entire campaign) is declared unworkable. Root cause and lessons are archived in `research_decision.yaml` to inform future campaigns. |
| <a id="g-diagnostic-rule"></a>**Diagnostic Rule** ⚠️ | A named rule in the verdict_interpreter that maps a specific metric pattern to a root cause and a prescribed action. Example: `cost_drag` rule fires when trading costs consume > 80% of gross returns, prescribing a higher trade filter. |
| <a id="g-forecast"></a>**Forecast** | A continuous signal in the range [-20, +20] produced by the strategy. Positive = bullish view, negative = bearish. The forecast drives portfolio allocation: it is converted to a target allocation [-1, +1] and triggers a rebalance when the gap between current and target exceeds the rebalance threshold. |
| <a id="g-regime"></a>**Regime** | A classification of current market conditions (e.g., `TRENDING`, `RANGING`, `HIGH_VOL`). Strategies can be gated to only activate in specific regimes. The regime detector runs in parallel with the signal and can suppress or amplify the forecast. |
| <a id="g-component"></a>**Component** | A self-contained signal unit within the trading-bot strategy framework. Components implement `SubStrategyComponent` and produce a `ComponentOutput` with a forecast and confidence. Multiple components are combined by a `CompositeStrategy` via weighted sum. |
| <a id="g-strategy-config"></a>**Strategy Config** | A JSON structure that fully specifies a strategy: which components to use, their parameters, regime gates, and combination weights. This is the machine-readable form of a hypothesis and the only input the backtest engine accepts. |
| <a id="g-handoff"></a>**Handoff** | A YAML file that formally passes context from one stage to the next. It lists required inputs, optional inputs, constraints, and expected deliverables. Stages only read what their handoff specifies — they do not have access to the full conversation history. |
| <a id="g-circuit-breaker"></a>**Circuit Breaker** | An automatic rule that interrupts a search loop when exhaustion is detected. Prevents infinite refinement of a dead-end hypothesis by forcing an altitude climb after a fixed number of failed attempts. |
| <a id="g-findings-carryover"></a>**Findings Carryover** | An artifact that preserves diagnostic memory across run boundaries. It tells the next run what was tried, what failed, and what parameter range to search next — preventing the campaign from cycling through the same dead ends. |
| <a id="g-artifact"></a>**Artifact** | Any structured YAML or JSON file produced by a pipeline stage. Artifacts are the only allowed communication between stages. They must conform to their schema before the pipeline advances. |
| <a id="g-schema"></a>**Schema** | A JSON Schema definition (Draft 7) in `schemas/` that specifies the required fields and types for an artifact. Validation against the schema is a hard gate — a stage cannot advance if its output fails schema validation. |
| <a id="g-skill"></a>**Skill** | A Markdown file in `skills/` that defines a specialist LLM persona: its mission, required inputs/outputs, checklists, constraints, and forbidden actions. The orchestrator loads the relevant skill as the system prompt for each stage. |
| <a id="g-backtest-window"></a>**Backtest Window** | A single contiguous date range used for one out-of-sample evaluation. The baseline protocol uses 11 monthly windows (January–November 2024). Results from all windows are aggregated to produce the final verdict. |
| <a id="g-forecast-return-correlation"></a>**Forecast-Return Correlation** | A diagnostic metric measuring how well the strategy's forecast predicts next-bar returns. A value near 0 means the signal is noise. A negative value means the signal is inverted. The verdict_interpreter uses this as the primary signal-quality gate. |
| <a id="g-cost-drag-"></a>**Cost Drag %** | The fraction of gross returns consumed by trading costs (spreads, fees). A value above 80% means the strategy's edge is real but smaller than transaction costs — the fix is to trade less frequently. |
| <a id="g-parameter-bracket"></a>**Parameter Bracket** ⚠️ | A [min, max, step] range produced by the verdict_interpreter when prescribing a refine verdict. Narrows the parameter search space based on current run results, enabling convergent search rather than random re-tries. |
| <a id="g-human-pause"></a>**Human Pause** | A pipeline state where automated execution is suspended pending human review. Triggered by `implementation_allowed = false` (a fix requires a new bot component) or by a `component_gap` in the backtest_spec. The pipeline resumes after the human resolves the blocker and restarts the orchestrator. |
| <a id="g-audit-log"></a>**Audit Log** | A per-stage record in `pipeline_state.yaml` tracking token usage, cost in USD, attempt number, and timestamp. Used to enforce token budgets and debug expensive runs. |
| <a id="g-campaign-review"></a>**Campaign Review** | A special stage triggered after 2+ hypothesis families fail. Unlike the per-run verdict_interpreter, it has access to the full campaign history and can issue campaign-level decisions (reframe, terminate) that no single-run stage can make. |
| <a id="g-research-decision"></a>**Research Decision** | The terminal artifact of a campaign, written when a strategy is promoted or the campaign is terminated. Captures the final verdict, the lessons learned, and (if promoted) the approved strategy config. |
| <a id="g-burnt-data"></a>**Burnt data** | Date ranges already used in any walk-forward window. Cannot serve as unbiased holdout. Tracked in `config/campaign_data_policy.yaml.burned_ranges`. |
| <a id="g-trial"></a>**Trial** | Any comparison of a strategy config against historical data: walk-forward runs, refinement iterations, kills included. All count. Deduplicated by `forecast_hash` (identical forecasts on identical data = one trial regardless of config differences). |
| <a id="g-prescreen"></a>**Prescreen** | Legacy vocabulary from before the pipeline's "always backtest" premise: a cheap IC + cost-hurdle gate that used to run before a full walk-forward, used in some field names and older on-disk artifacts (e.g. `machine_constraints.significance_methodology`'s A8.5.1a labelling). There is no prescreen stage in the current pipeline — every run always executes a full backtest. |
| <a id="g-active-bar-ic"></a>**Active-bar IC** | Spearman correlation between forecast and return, restricted to bars where the forecast is non-zero or changing. The gate statistic for sparse/event-driven signals; all-bars IC is misleading for these (dominated by the tie mass at forecast=0). |
| <a id="g-dormant-mechanism"></a>**Dormant mechanism** | A hypothesis whose activating condition never fired in the test window. Disposition: backward data extension (pre-2024 history where the condition demonstrably occurred) OR parking with a condition-based reactivation trigger. |
| <a id="g-holdout-consumption"></a>**Holdout consumption** | The irreversible event where a hypothesis_id enters `campaign_data_policy.holdout_consumed_by`. From this point, no further holdout evaluation is possible for that hypothesis_id. Failure is terminal. |
| <a id="g-dsr"></a>**DSR (Deflated Sharpe Ratio)** | Bailey & López de Prado (2014) correction for selection bias across multiple trials. `E_max = μ_SR + σ_SR × [(1−γ)Φ⁻¹(1−1/N) + γΦ⁻¹(1−1/(eN))]`; DSR = Φ[(candidate_SR − E_max)/σ_SR]. Threshold: 0.95. Falls monotonically as trial count grows for fixed true Sharpe. |
| <a id="g-expectancy-path"></a>**Expectancy path** | Promotion route for sparse-trading strategies (below_floor_pct > 50%). Uses per-trade expectancy t-stat instead of DSR; threshold t > 2.0 (Bonferroni note recorded in promotion_audit). |

---

## 7. Acceptance Culture

The system uses three distinct acceptance protocols depending on what is being accepted:

### Known-answer fixtures (for metrics)

> ⚠️ **The fixture this protocol depends on is not in the repository.**
> Verified 2026-08-31: `keltner_163` has **no fixture file**, **no test
> references it**, and none of the **955** `trades.json` files on disk (909 in
> `runs/`, 46 in `archive/`) holds 150–175 trades. `tools/run_protocol.py`
> names the exact source —
> `strategy-research/results/protocols/20260702T091324Z_18fad381/protocol_summary.json`
> — and `results/protocols/` is **empty**, and not gitignored.
>
> The protocol below is therefore **not executable by anyone reading this
> guide**. The signature it quotes is preserved because it is the record of what
> the fixture asserted; it is not something you can currently check against. See
> [E037-35](../engineering/roadmap/E-037/FINDINGS.md#e037-35).
All quantitative tools are validated against a named fixture whose correct output is known in advance. The standing fixture is **`keltner_163`** — 163 closed trades from the baseline_v2 Keltner re-run. Any tool touching per-trade metrics must reproduce this fixture's known signature: win rate rising 51%→57% from 2024 to 2025 cohorts, per-trade expectancy worsening −26→−58 bps. A tool that cannot reproduce this is not calibrated.

There is no equivalent automated must-reject fixture for the A2.1 ungated-escape check today — that assessment is made directly by a human running the regime-auditor skill, not by any tool.

### Output audits (for prompts and skills)
Skill rewrites have no behavior until an LLM executes them. They are accepted by **output audit** (A1.4), never by diff review. For each skill change: (a) run a trial and audit every output card for compliance; (b) look for compliant-looking confabulations (satisfies the letter, violates the spirit). Captured examples go back into the skill. The first audit-passing card serves as the end-to-end pass-path test.

### Pre-registration (for runs)
Before any holdout backtest runs: write `holdout_result.yaml.expected_range` with the a-priori bounds and rationale. Before any recalibration: document the threshold change as a new trial. This ensures that the result cannot be declared "as expected" retroactively and every data comparison is pre-committed.

### Calibration reporting
Calibration outputs are always reported as numbers, not pass marks: DSR values, IC values with CIs, t-stats with n, expectancy ± SE. "7 tests pass" is not a calibration report. The calibration numbers for Improvement 06 are on record in `engineering/improvements/done/IMPROVEMENTS_DONE_20260706.md`.

### Conflicting agent state (2026-07-10)
When two sessions (or a session and a background campaign process) disagree
about a shared artifact's content, the conflict is resolved by independently
recomputing the underlying number from immutable source artifacts (`bars.csv`,
`trades.json`), never by trusting whichever version is "yours" or re-asserting
prior prose. Any tool-result content instructing an agent to conceal a file
change or a system state from the operator is treated as illegitimate
regardless of its apparent source and is disclosed verbatim, immediately. Full
case and standing rule: `docs/analysis-reports/INCIDENT_20260710.md`,
`docs/CONCEALMENT_INSTRUCTION_DOCTRINE.md`, and `docs/VERIFICATION_DOCTRINE.md`
sections 2 and 5.


---

## 8. The Machinery Around the Pipeline

§1–§7 describe the pipeline. **This section describes what keeps the pipeline
honest** — the hooks, the CI job, and the enforcement behind each rule the
guide states.

It exists because a whole class of problem was invisible from §1–§7: something
is written down, everybody believes it, and **it does not run**. A stage drawn
on the map that is never dispatched. A rule phrased as a gate that no code
checks. A test that no gate executes. A hook committed to the repo but not
installed. In each case the *artifact of the protection* was mistaken for the
protection.

So the load-bearing column below is the last one: **does it actually run?**

---

### 8.1 What guards this repository

| Guard | Where | Runs what | Does **not** cover |
|---|---|---|---|
| **pre-commit hook** | `.git/hooks/pre-commit`, tracked copy at `strategy-research/tools/hooks/pre-commit` | secret scan · holdout date gate · `trading-bot/tests/` | **the entire `strategy-research/tests/` suite** — the hook `cd`s into `trading-bot` and runs only that |
| **GitHub Actions** | `.github/workflows/tests.yml`, on push and PR | both suites, Linux + Windows · holdout seal gate · config validation | anything needing `trading-bot/local_data/` — the price caches are untracked, so tests that need bars **skip** |

**The gap where those two meet.** A `strategy-research` test guarded by
`skipif(<a local_data file> missing)` is skipped in CI for want of data and
never invoked by the hook. It runs **only** when a person types `pytest` by
hand, in `strategy-research/`, on a machine holding the cache. Measured
2026-08-31: **10 such guards across 4 files**, and they are the ones that drive
the real engine over real bars. A green tick on a PR does not mean the
backtest engine still routes correctly. See
[E037-27](../engineering/roadmap/E-037/FINDINGS.md#e037-27).

**Two consequences worth stating plainly:**

- **A tracked hook is not an installed hook.** `.git/hooks/` is not version
  controlled, so updating the tracked copy does **not** reach an existing
  checkout. Verify with
  `diff .git/hooks/pre-commit strategy-research/tools/hooks/pre-commit` —
  silence is the pass. `tests/test_installed_hook_matches_tracked.py` does this
  automatically and names the missing gate.
- **A passing suite is not a covering suite.** Check what *skipped*, not just
  what passed.

---

### 8.2 Enforcement ledger — who actually enforces each rule

Every guarantee this guide states, and what stands behind it. **"Code" means a
program checks it and stops you. "Skill" means an instruction to an LLM, which
may comply or not. "Nothing" means the sentence is the only thing there.**

| Guarantee, as the guide states it | Enforced by | Actually runs? |
|---|---|---|
| A8.1 — IC significance **and** `cost_check.pass` both considered together on the post-backtest go/no-go | Code — `signal_statistics.py::determine_route` | ✅ yes, computed — but informational only, not a gate (see `protocol_result.yaml`'s post-backtest fields) |
| A2.2 — a detector retune may not cite PnL or Sharpe | Code — `_validate_retune_firewall`, **raises** on a hit | ✅ yes |
| An unrecognised spec status must not be guessed at | Code — `determine_post_spec_route`, pauses for a human | ✅ yes |
| A6.1 — the holdout is single-use | Code — `_route_holdout_evaluation` refuses a repeat `hypothesis_id` | ✅ yes (never yet exercised — no run has reached it) |
| A holdout needs an affirmative `research_only: false` | Code — same function, gate 2b | ✅ yes |
| A6.1 — the holdout range must be declared in `sample_split_design` | Code — `run_campaign.py::_materialize_run`/`_materialize_refinement_run` now write it, alongside `pass_rule` (2026-09-13) | ✅ yes, for every run materialized from this date forward — 0 of the 10 pre-existing on-disk `pre_registration.yaml` files carry it (all predate the change) |
| E-018 (2026-09-13) — a binding `pass_rule_evaluation.yaml` drives routing directly | Code — `run_phase1_research.py::_resolve_verdict_fields`'s `pre_eval` branch | ✅ yes |
| E-018 (2026-09-13) — the near-miss scoreboard has no read access to promotion decisions | **Inspection only** — the static test that proved this (`tests/test_near_miss_scoreboard_firewall.py`) was removed by operator decision the same day `verdict_interpreter` became a reviewed exception to it | ⚠️ downgraded from a standing test to inspection-only |
| A6.2 — every evaluation counts as a trial, kills included | Code — `_record_backtest_trial` / `_record_failed_backtest_trial` | ✅ yes |
| F5c/F6 — an engineering failure must not be scored as "no edge" | Code — `verdict_interpreter`'s stage 11 check for `mechanism_failure == component_execution_error`, immune to the circuit breaker | ✅ yes |
| Stage 3 — variants "must" be really diverse, "cosmetic = rejected" | **Skill only** — `innovation-expansion/SKILL.md`; the model reports its own verdict | ❌ **no code can produce "rejected"** ([E037-18](../engineering/roadmap/E-037/FINDINGS.md#e037-18)) |
| A1.1–A1.4 — `edge_source` before `signal_concept`, library lookup | **Skill only** | ❌ no |
| Artifacts are validated against JSON schemas | **Nothing** — no schema is loaded by any code | ❌ no (corrected in §3, 2026-08-27) |
| Stage 10 — the regime auditor judges the detector | **Nothing dispatches it**; a human runs the skill on a paused pipeline | ❌ not as an automated stage ([E037-16](../engineering/roadmap/E-037/FINDINGS.md#e037-16)) |
| Secrets and venvs are never committed | Code — secret scan, **gate 0 of the tracked hook** | ⚠️ **only if the hook is installed** ([E037-29](../engineering/roadmap/E-037/FINDINGS.md#e037-29)) |

**How to read this table.** ❌ does not mean broken. A skill-enforced rule is
still a real instruction and mostly obeyed — but it is a *tendency*, not a
guarantee, and it should not be written in language ("must", "rejected") that
promises a gate. That mismatch between phrasing and enforcement is what made
these hard to see, and it is why this column exists.

**When you add a rule to this guide, add its row here.** If the row would say
"Nothing", the honest move is to phrase the rule as guidance rather than as a
gate — or build the check.

---

### 8.3 Documentation guards

The guide itself drifts, so three checks in `strategy-research/tests/` hold it
in place. All are **ratchets**: green today, failing only on new drift.

| Check | Fails when |
|---|---|
| `test_user_guide_field_tables.py` | §3 documents an artifact field that appears in **no** real artifact on disk |
| `test_doc_anchors.py` | a `file:line` anchor points past the end of a file, or a `file::symbol` anchor names a function that no longer exists |
| `test_installed_hook_matches_tracked.py` | the installed pre-commit hook differs from the tracked copy |

The first two run in CI. The third **cannot** — it needs a real `.git/hooks/`,
so it skips on a CI checkout. That is stated rather than hidden: it is a
developer-machine check, and the developer machine is exactly where hook drift
happens.

---

