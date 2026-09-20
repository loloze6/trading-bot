# E-037 S1 — Target shape for the USER_GUIDE rewrite

**State:** proposed — awaiting Jérémy's approval
**Owner:** Jérémy
**Updated:** 2026-08-30
**Scope:** design only. ONE stage (7, `signal_prescreen`) and ONE artifact
(`prescreen_result.yaml`) are filled in as proof. The other 12 stages and
~30 artifacts are untouched — that is S2.

Read [`EPIC.md`](EPIC.md) first. This file delivers S1's four items:

1. [Stage-entry template](#1-stage-entry-template) (+ the table-vs-block decision)
2. [Artifact-entry template](#2-artifact-entry-template)
3. [Worked sample](#3-worked-sample) — stage 7 and `prescreen_result.yaml`
4. [Information-loss checklist](#4-information-loss-checklist) — the S2/S4 procedure

Section [5](#5-findings-raised-while-proving-the-template) records the
doc-vs-code disagreements the worked sample surfaced. **Recorded, not fixed.**

---

## 0. The design constraint, restated

The operator must be able to answer, for any stage, **from one place**:

> what goes in · what comes out · what logic runs · why the stage exists

subject to the EPIC's hard constraint: **nothing is deleted, only relocated.**
Fewer lines is not success. If shortening costs a fact, keep the fact.

---

## 1. Stage-entry template

### 1.1 Decision: keep a 4-column index table, add a per-stage block

**Recommendation: two layers, not a 7-column table.**

The EPIC asks for three more columns (`stage input`, `stage output`,
`features / logic`). I recommend **not** adding them as columns:

- **The cells are already prose.** §2.2's stage-3 Objective is 68 words with a
  quoted string, a measured count and a date. Stage 4's holds a conditional.
  These are paragraphs living in a table because there was nowhere else.
- **A cell cannot hold what the new columns need.** Inputs are a *list* of
  files with provenance; logic is a *numbered sequence*. Neither survives a
  `|`-delimited cell. The only way to fit them is to compress — which is how
  the no-information-loss constraint gets broken.
- **The bug-list symptom needs precision, not glanceability.** "Which
  sub-steps does this feature reach?" is answered by an I/O contract with
  `file:line` anchors. That is a block, not a cell.

So:

| Layer | Shape | Answers |
|---|---|---|
| **Index** (§2.2 table) | the existing 4 columns, Objective compressed to **one plain-language line** | "which stage do I want?" |
| **Detail** (§2.2.N block, one per stage) | the template below | "what does it consume, produce, do, and why?" |

The index table's Objective becomes a pointer; every fact currently in it
relocates into that stage's block. **Nothing leaves the document.** The
relocation inventory in §4 is what proves it.

This still satisfies "from one place": the block *is* the one place. The
index is a table of contents for it.

### 1.2 The template

```markdown
#### Stage N — `stage_name`
**Engine:** Human | Claude | Python tool
**Runs:** when / what triggers it

**Objective.** EXACTLY one sentence. What this stage is for, in plain
language. Not a call sequence, not a list of amendment codes. If you cannot
say it without naming a function, it is not an objective yet.

**Design rationale.** 2-4 bullets. WHY the stage exists in this form: what it
buys, what it costs, why the work happens here rather than earlier or later.

> **The split rule.** If your objective sentence needs a "because", the
> "because" is design rationale and belongs in the field below it. Objective
> answers *what is this for*; design rationale answers *why is it built this
> way*. Both are "why" questions, which is why they get merged by accident --
> keeping them apart is what makes the objective scannable in the index table.

**Stage input**

| What | Where it comes from | Required? |
|---|---|---|
| `artifact.yaml` | stage M | yes |
| `config/x.yaml` | repo config | yes |
| `local_data/…` | data cache | yes |

**Stage output**

| What | Written where | Read by |
|---|---|---|
| `artifact.yaml` | `runs/{run_id}/…` | stage P, orchestrator |
| *(side effect)* `other.yaml` | `runs/{run_id}/…` | stage Q |

Side-effect writes to artifacts owned by another stage are listed here
explicitly. They are the ones that surprise people.

**Terms used in this block**

| Term | In plain words |
|---|---|
| **jargon term** | One line, no jargon in the explanation. |
| **A8.3** | The rule, stated as a rule, in one line. |

**Features / logic in place**

In execution order. Each step is a **title plus a one-line summary**, then
details underneath. The titles alone should read as a summary of the stage.

**1. Short title — what this step does, in one line.**
Details: the how, the amendment code, the `file:line`, the trap.

**2. Next title — …**
Details …

**Routes / outcomes** *(stages that decide)*

| Route | Condition | Next |
|---|---|---|

**Notes, history and traps**

Verbatim survivals: measured counts, dates, decisions and their reasons,
amendment rationale, known traps. This is the section that must never be
trimmed for tidiness. Anything relocated from elsewhere in the guide lands
here with its original wording.

**Owned by which code**

`file:line` list — the anchors that make this block re-verifiable.
```

**No jargon and no code without a plain-language line.** A bare `A6.2`, or a
bare `n_eff`, is an unexpandable reference: load-bearing, so it survives
verbatim, but useless to anyone who does not already know it — and anyone who
does know it did not need the document. The **Terms used in this block** table
carries them: one line each, no jargon inside the explanation, plus a single
link to the codes' source text. After that the bare term is fine.

A terms table beats glossing inline: five inline parentheticals bury the steps
they are attached to, and the same code recurs across stages.

This is not pedantry. Incident **C4, "Rule-citation confabulation"** records a
card citing *"A3.6, n_episodes >= 8 per window"* where the label was wrong
(the real rule was A8.5.1a-spec rule 3) and the qualifier invented, concluding:
*"Plausible-looking fake citations survive until someone quotes the source
verbatim"* (`engineering/improvements/done/IMPROVEMENTS_DONE_20260712.md:216`).
Codes nobody can resolve in one hop are codes nobody checks. See
[E037-12](FINDINGS.md#e037-12) and [E037-13](FINDINGS.md#e037-13).

---

## 2. Artifact-entry template

```markdown
### `artifact_name.yaml`

> **Why this file exists.** One line. The reason the file is in the pipeline
> at all — what would break, or what could not be decided, without it.

**Created by:** …  *(list every creation path, not just the usual one)*
**Updated by:** … | *(none — write-once)*
**Read by:** …
**Written to:** `path/…`
**Schema:** `path/…` — **declared, never checked.** Nothing loads this file, so
a value that violates it still flows through the pipeline. Treat it as a
description of what the artifact was *meant* to look like, not a guarantee.
| *(no schema file exists)*

| Field | Definition — what it means | Values / range (meaning of each) | Example (`run_NNN`, YYYY-MM-DD) |
|---|---|---|---|

**Notes** *(optional)* — traps, invalidation conditions, fields that mean
something other than they look like.
```

**Rules**

1. **All five metadata lines always appear.** Absence is stated —
   `*(none — write-once)*` — never omitted. Today a missing line is ambiguous
   between "does not apply" and "nobody checked": `trade_diagnostics.json` has
   no `Schema` and no `Updated by`, and a reader cannot tell which.
2. **`Created by` lists every path.** Two pieces of code can write the same
   file; name both. See [E037-04](FINDINGS.md#e037-04).
3. **`Schema` says plainly that nothing checks it.** The word "schema" makes
   people assume validation. A reader landing on one entry never sees §3's
   preamble, so the line itself must say there is none.
4. **The rationale headliner is one blockquoted line**, so it cannot be
   mistaken for another metadata field.
5. **Field tables may be a selection, but must say so** — otherwise absence
   reads as non-existence. See [E037-03](FINDINGS.md#e037-03).
6. **Definition = what the field is FOR. Values = what it can hold.**
   A list of legal strings is not a definition. `route` is not "one of seven
   strings"; it is *the decision the prescreen reached, and the field the
   orchestrator reads to pick the next stage*. Each value gets a two-word
   gloss — `kill_no_ic` (tested, no directional content). Scalars get type,
   range, and what `null` means. The glosses carry real knowledge: nothing in
   the old table said `no_signal_artifact` means *never tested* rather than
   *tested and failed*.
7. **Examples are real values from a real run, dated in the column header.**
   Never invented, never tidied. The date is load-bearing: artifacts drift, so
   an undated example becomes a false claim. Proof — the newest real
   `prescreen_result.yaml` is run_060 (2026-08-28) and lacks the `#50` gap
   fields, which landed next day in `97d3bd7a` (2026-08-29). Fields the
   example predates are marked `—` with the reason.
8. **No jargon without a plain-language explanation, and no key name without
   one either.** This is the rule the operator asked for directly. A term like
   IC, `n_eff`, episode or bps, and a code like A8.6, is meaningless to anyone
   who does not already know it — and someone who already knows it does not
   need the document. Each block opens with a **Terms used in this block**
   table: one line each, no jargon inside the explanation. Anything not
   explained there gets explained where it is used. Codes additionally link
   once to their source text. See [E037-12](FINDINGS.md#e037-12) for what the guide
   does today: 14 codes, 26 mentions, zero pointers.
9. **"Logic" prose does not live here.** It belongs in the owning stage's
   block. The artifact entry describes the *file*; the stage block describes
   the *computation*. Relocation, not deletion — see §4.

---

## 3. Worked sample

Filled in by reading `strategy-research/tools/prescreen_signal.py` and
`strategy-research/workflow/run_phase1_research.py`, not by paraphrasing the
existing text. Disagreements are in §5.

### 3.1 Stage 7

> **Superseded as a reference — kept as the S1 record.** This worked sample has
> since been folded into `docs/USER_GUIDE.md` §2.2 stage 7, which is now the
> authoritative copy. Read it there. This one is preserved unchanged because it
> is the artifact S1 was approved on; if the two ever differ, the guide is right
> and this is history.


#### Stage 7 — `signal_prescreen`
**Engine:** Python tool (`tools/prescreen_signal.py`), launched as a
subprocess by the orchestrator (run_phase1_research.py line 1074
`run_tool_worker`). No LLM call, no token cost.
**Runs:** after `backtest_specification` emits `spec_ready`. The orchestrator
runs an A8.6 power pre-flight *around* the tool first — see logic step 0.

**Objective.** Decide cheaply, on the signal alone, whether this hypothesis
deserves an expensive walk-forward backtest.

**Design rationale.**
- A full backtest costs compute, and every run is counted as a trial whether
  it passes or dies, so it also costs statistical budget. Trials spent on
  hopeless signals raise the bar for the promising ones.
- The prescreen answers the question for one pass over the forecast series:
  no portfolio simulation, no backtest engine, no LLM call.
- It asks only the two things answerable without simulating a portfolio: does
  the signal predict anything, and could it out-earn its trading costs.
- It runs after specification, not before, so the answer is about the compiled
  config that would actually be backtested — not about the prose hypothesis.

**Terms used in this block**

| Term | In plain words |
|---|---|
| **IC** (information coefficient) | How well the forecast ranked what actually happened next. `+1` perfect, `0` useless, `-1` perfectly backwards. Measured with Spearman rank correlation. |
| **active bar** | A bar where the signal actually said something (forecast non-zero/changing). A selective signal is silent most of the time. |
| **bps** (basis point) | One hundredth of a percent. Costs and edges are quoted in bps per trade. |
| **effective sample** (`n_eff`) | How many genuinely *independent* observations there are. Adjacent hours move together, so 8928 bars are worth far fewer independent facts — dividing by a block size is how that is accounted for. |
| **episode** | A burst of consecutive active bars treated as **one** event rather than many, for signals that fire in clusters. |
| **A8.6** | Rule: check up front that the sample is even big enough to detect the effect. If not, do not spend the trial. |
| **A8.3** | Rule: score a selective signal on the bars where it spoke. An IC over all bars is swamped by the silent ones and collapses toward zero by construction. |
| **A8.1** | Rule: a good IC alone is never a pass — the cost gate must clear too. A signal with IC 0.2145 still lost 26 bps per trade. |
| **A8.5.1a** | Rule: for signals that fire in bursts, count events, not bars. |
| **A2.1** | "Detector-confidence deadlock escape" — the rule letting a hypothesis be judged without a trusted regime detector. Requires all-bars IC. |
| **A2.3** | "Post-`unusable` policy" — with no trustworthy detector, regime-conditioned numbers are not evidence. Rule 5 says the escape test must use all-bars IC. |
| **A6.2** | Rule: deflated Sharpe needs the spread of results across trials, so every evaluation counts as a trial — kills included. |
| **F5c** | Rule: "the code broke" must never be recorded as "the idea failed". |
| **#50** | Issue: a forecast/return pair straddling a hole in the data cache is not a real observation. |

Full text of every amendment code:
[`AMENDMENTS_01-06.md`](../../improvements/done/design_and_docs/AMENDMENTS_01-06.md).

**Stage input**

| What | Where it comes from | Required? |
|---|---|---|
| `artifacts/candidate_strategy_config.json` | stage 6 `backtest_specification` | yes |
| protocol JSON (`symbols`, `windows`, `timeframe`) | `_resolve_protocol_path()` — run_phase1_research.py line 1086 | yes |
| `config/cost_model.yaml` | round-trip cost in bps per symbol, plus `safety_factor` (default 2.0) | yes |
| `trading-bot/local_data/{SYMBOL}_{tf}.csv` | price cache; a coarser timeframe is derived from a finer one (`_resolve_ohlcv_source`, prescreen_signal.py line 306) | yes |
| aux feeds — funding rate, fear & greed | prescreen_signal.py line 151 / `:171` | only if the config declares them |
| `config/campaign_data_policy.yaml` | era boundaries and episode settings | only on the A8.5.1a path |
| `runs/{run_id}/artifacts/regime_audit_decision.yaml` | stage 10 | only if present — see the side effect below |
| `campaign_state.yaml` | read by the orchestrator wrapper, not the tool | yes |

**Stage output**

| What | Written where | Read by |
|---|---|---|
| `prescreen_result.yaml` | `runs/{run_id}/prescreen/`, copied to `artifacts/` (run_phase1_research.py line 1113) | `verdict_interpreter`, orchestrator routing |
| *(side effect)* `regime_audit_decision.yaml` — `ungated_escape_eligible` rewritten in place | `runs/{run_id}/artifacts/` | **stage 10's file, edited by stage 7** (prescreen_signal.py line 1582 → `:1092`) |
| *(side effect, orchestrator not tool)* one row in `campaign_state.trial_sharpes` | campaign root | `deflate_sharpe.py`, campaign accounting |

**Features / logic in place**

Each step: **title — one-line summary.** Details follow.

**0. A8.6 power pre-flight — the orchestrator can kill the run before the tool starts.**
If the sample is too small to detect the effect even if it were real, the tool
is never launched. The orchestrator writes `prescreen_result.yaml` itself with
`route: insufficient_power_a_priori` and records the trial
(run_phase1_research.py line 6217, `:6232`, `:6235`). The same check runs earlier
at the validation gate (`:2287`); if it already wrote the file, the
orchestrator skips the tool (`:6207`). **None of this is in
`prescreen_signal.py`** — see [E037-01](FINDINGS.md#e037-01).

**1. Setup — load the config and protocol, and fix the block size.**
`block_size = bars_per_day(timeframe)` comes from `tools/timeframe.py`, the
same source the A8.6 gate uses. No fallback: an unparseable timeframe raises
(prescreen_signal.py line 1215).

**2. Extract the forecast — replay the real strategy over the full range.**
Per symbol, load prices from the earliest window start to the latest window
end, merge aux feeds, and drive the actual strategy through `CandleBuilder` to
produce a forecast per bar (`_extract_forecasts`, `:470`).

**3. Gap suppression (#50 A) — drop pairs that straddle a hole in the data.**
If two bars are not one expected step apart, the "next-bar return" is not a
next-bar return, so the pair is discarded. Counts are surfaced per symbol,
because a pooled figure can read "no gap effect" while one symbol's whole
sample was destroyed (red-team D6) (`:1264`, `:1267`).

**4. Degenerate-input guards — fail loud rather than flattering.**
A symbol left with zero usable records by step 3 raises (`:1284`). If no symbol
loaded usable data at all, the run raises rather than emitting a route from
zero bars (`:1320`, added 2026-08-28 after run_060).

**5. Compute the IC — two of them, for two different jobs (A8.3).**
`ic_active_bars` (only bars where the signal spoke) is the primary gate.
`ic_all_bars` is tie-dominated for a sparse signal and is reserved for the
A2.1 escape test, which requires it.

**6. Significance — is the IC bigger than luck, given how few independent observations there are?**
Default method is **block-deflated Fisher z**: `n_eff = active_n / block_size`,
then `z = IC * sqrt(n_eff - 3)`, labelled `block_{block_size}_fisher_z`
(`:643`, `:1377`). The label is derived from the block size actually used — it
read `block_24_fisher_z` until 2026-08-28 while `block_size` had already become
per-timeframe, so a 4h run stamped `block_24` while dividing by 6.
- **#50 (B):** a block that cannot be placed without spanning a gap does not
  exist and does not count toward `n_eff`. Counted per symbol, because pooling
  first would read the seam between two symbols as a contiguous step (`:1359`).
- **A8.5.1a episode-blocked** replaces it on request (config
  `significance_methodology: episode_blocked_a851a`) for multi-era data
  (`:1402`). With the flag absent, behaviour is unchanged, so archived runs
  stay reproducible.
- **Stationary block bootstrap** replaces it automatically when the active-bar
  forecast is *structurally* degenerate — one constant magnitude whenever
  active, which makes `ic_active_bars` undefined by construction rather than a
  no-edge result (`:730`, branch `:1429`, detector `:720`; found 2026-07-07 via
  the P4_ts_trend shakedown). A merely small active sample is a power problem,
  not a structural one, and is left to A8.5.1a.

**7. Turnover proxy — infer how often this would trade.**
Active bars per trade implies a holding period (`_compute_turnover_proxy`,
`:813`). Redefined 2026-07-07 to count activity transitions; the previous
sign-flip-only counter silently merged long-only episodes across flat gaps
into a single trade.

**8. Cost check (Layer 2) — could the edge out-earn the fees?**
Estimated gross edge (`ic_for_cost` × `sigma_bar_bps` × holding period) versus
round-trip cost from `cost_model.yaml`. Passes when `edge_to_cost_ratio >=
safety_factor` (default 2.0) (`:897`).
- `sigma_bar_bps` is measured from the records. If no symbol yields an
  estimate, the placeholder `_DEFAULT_SIGMA_BAR_BPS = 15.0` is substituted and
  `sigma_is_placeholder: true` is written into the artifact. **When that flag
  is true, the cost check and every required-IC figure are invalid.**

**9. Route decision — combine the two gates (A8.1).**
`_determine_route` (`:982`); see the route table below. Both IC significance
**and** `cost_check.pass` are required for `proceed_to_backtest`.

**10. F5c override — "the code broke" is not "the idea failed".**
Takes priority over every route above (`:1481`). If `active_n_bars == 0`, or
swallowed component exceptions exceed 5% of processed bars, the route becomes
`no_signal_artifact` rather than `kill_no_ic` — the latter claims the idea was
tested, and here it was not. From run_044 (2026-07-04): a
`FundingRateMeanReversionComponent` divide-by-zero produced `active_n_bars=0`,
which read as a real `kill_no_ic` and nearly closed an untested family.

**11. A2.3 — per-regime IC is deliberately not computed.**
`ic_by_regime` is emitted as `{suspended: true}` with its reason, so the
absence cannot be mistaken for an oversight. Only ungated IC decides.

**12. Side effect — stage 7 rewrites stage 10's file.**
`ungated_escape_eligible` in `regime_audit_decision.yaml` is resolved using
`ic_all_bars`, because an IC measured on detector-gated bars is not admissible
for or against the escape (A2.3 rule 5) (`:1582`, `:1092`). The code labels
this "A9.1", which appears to be the wrong code — see [E037-13](FINDINGS.md#e037-13).

**13. Write the artifact.** `prescreen_result.yaml` (`:1585`).

**14. A6.2 trial recording — the orchestrator logs the trial after the tool returns.**
`_record_prescreen_trial` (run_phase1_research.py line 4039, called at `:1130`).
Kills count as trials; `statistic_valid = "neither"` when there is no backtest
Sharpe. Upsert on `(trial_id, "prescreen")` since 2026-08-16 (issue #28 /
E-025), so a crash-retry replaces the stale row instead of being swallowed.
**Not in `prescreen_signal.py`** — see [E037-06](FINDINGS.md#e037-06).

**Routes / outcomes**

| Route | Condition | Next |
|---|---|---|
| `no_signal_artifact` | `active_n_bars == 0`, or component-error rate > 5% — overrides everything (F5c) | verdict_interpreter; engineering failure, not evidence |
| `insufficient_power_a_priori` | A8.6: `min_detectable_ic > plausible_ic_upper` — tool never runs | `completed_rejected`, no component built |
| `kill_no_ic` | IC not significant at `p < 0.10` | verdict_interpreter |
| `refine_inverted_ic` | IC significant but negative | verdict_interpreter — flip polarity |
| `kill_cost_hurdle` | IC significant positive, cost fails, and `p > 0.05` or `ratio < 0.5` — structural barrier | verdict_interpreter |
| `refine_cost_hurdle` | IC significant positive, cost fails, but marginally — widen threshold or lengthen holding | verdict_interpreter |
| `proceed_to_backtest` | IC significant positive **and** `cost_check.pass` (A8.1) | stage 8 `protocol_execution` |

**Notes, history and traps**

- Signal layer only — no portfolio simulation, no backtest engine.
- **Two thresholds, one documented.** `_SIG_THRESHOLD = 0.10` is the main IC
  gate (prescreen_signal.py line 87); a separate `p > 0.05` inside the cost
  branch decides `kill_cost_hurdle` vs `refine_cost_hurdle`.
- **`gap_skipped_pct` is not the cache's contamination rate.** It counts pairs
  actually reached after warmup; gaps inside the warmup are never reached, so
  it reads lower than `tools/cache_gap_census.py` by a config-dependent amount
  (red-team D4/D5). For the cache rate, run the census.
- **The gap fix is partial, knowingly.** (A) fixes the return label, (B) the
  block count. Neither fixes rolling indicators, which still span the holes.
  Segment-and-re-warm would, and was rejected: it destroys 91% of the
  `kraken_SUIUSD` train sample.
- `n_eff_nominal_blocks` is computed over the post-(A) active count, so it
  compares like-for-like with `n_eff_placeable_blocks`, not the pre-#50 value.

**Owned by which code**

prescreen_signal.py line 1185 (`run_prescreen`) · `:982` (`_determine_route`)
· `:643` (`_block_adjusted_significance`) · `:730` (stationary block bootstrap)
· `:897` (`_cost_check`) · `:1092` (`_resolve_ungated_escape`) ·
run_phase1_research.py line 1074 (`run_tool_worker`) · `:6217` and `:2287`
(A8.6) · `:4039` (`_record_prescreen_trial`)

### 3.2 Artifact `prescreen_result.yaml`

### `prescreen_result.yaml`

> **Why this file exists.** It is the record of the cheap go/no-go on a
> signal — the evidence that justified either spending a full walk-forward
> backtest on this hypothesis or killing it without one. It is also the
> trial's receipt: `forecast_hash` from this file is what stops the same
> signal being counted twice in the deflated-Sharpe denominator.

**Created by:**
- `signal_prescreen` tool — prescreen_signal.py line 1585 (normal path)
- orchestrator — run_phase1_research.py line 6232, when the A8.6
  pre-flight blocks before stage 7 and the tool never runs
- orchestrator — run_phase1_research.py line 2297, when A8.6 blocks
  earlier still, at the validation gate

**Updated by:** *(none — write-once per run; the orchestrator copies it from
`runs/{run_id}/prescreen/` to `runs/{run_id}/artifacts/` unchanged,
run_phase1_research.py line 1113)*
**Read by:** `verdict_interpreter`, orchestrator routing
(`determine_post_prescreen_route`), `_record_prescreen_trial`,
`_check_prescreen_conformance` (run_phase1_research.py line 3146)
**Written to:** `runs/{run_id}/prescreen/prescreen_result.yaml`, copied to
`runs/{run_id}/artifacts/prescreen_result.yaml`
**Schema:** `workflow_artifacts/schemas/prescreen_result.schema.json` —
*declared; not loaded by any code, see §3 preamble*

*Selected fields — the artifact carries roughly 30 top-level keys; this table
covers the decision-bearing ones.*

**Example column provenance.** Values transcribed verbatim from
`runs/run_060/artifacts/prescreen_result.yaml`, written 2026-08-28T19:54Z —
the newest real prescreen artifact on disk. run_060 was a 4h funding
mean-reversion retest on BTCUSDT + ETHUSDT that died at `kill_no_ic`. Fields
marked `—` are absent from that file, with the reason given; that absence is
itself informative and is not padded with an invented value.

| Field | Definition — what it means | Values / range (meaning of each) | Example (`run_060`, 2026-08-28) |
|---|---|---|---|
| `route` | The decision the prescreen reached. The single field the orchestrator reads to choose the next stage. | `proceed_to_backtest` (send to full walk-forward) · `kill_no_ic` (tested, no directional content) · `refine_inverted_ic` (signal works backwards) · `refine_cost_hurdle` (edge real but too small, fixable) · `kill_cost_hurdle` (edge structurally below cost) · `no_signal_artifact` (never actually tested — engineering failure) · `insufficient_power_a_priori` (sample too small to detect the effect even if real) | `kill_no_ic` |
| `route_rationale` | Prose sentence justifying the route, carrying the numbers that drove it, so a human can audit the decision without re-running. | free text | `Active-bar IC=0.0162, p=0.5315 >= 0.1. Signal has no detectable directional content on this venue/timeframe.` |
| `prescreen_kill_reason` | Machine-readable cause of death; distinguishes *scientific* kills from *engineering* ones. | `no_informational_content_this_venue` (signal carries nothing here) · `insufficient_episodes_a851a` (too few episodes to judge) · `cost_drag_structural` (costs exceed any plausible edge) · `component_error` (code threw) · `zero_activation` (signal never fired) · `null` (not a kill) | `no_informational_content_this_venue` |
| `ic_all_bars` | Rank correlation between forecast and next-bar return across **every** bar. Tie-dominated when the signal is sparse, so it understates a selective signal — reserved for the A2.1 ungated-escape test, which requires it. | float in [-1, 1]; `null` if undefined | `-0.006944` |
| `ic_active_bars` | The same correlation but only over bars where the forecast was non-zero/changing — i.e. where the signal actually made a claim. **The primary gate.** | float in [-1, 1]; `null` if undefined | `0.016237` |
| `ic_spearman_pooled` | Legacy alias of `ic_active_bars`, retained so older consumers keep working. | same as `ic_active_bars` | `0.016237` |
| `active_n_bars` | How many bars the signal was actually live on. The real sample size behind the IC. | integer >= 0; `0` forces `no_signal_artifact` | `8928` (of `n_bars_total: 17854`) |
| `forecast_sparsity_pct` | How often the signal said nothing. High sparsity means the headline IC rests on few bars. | float 0-100 | `49.99` |
| `forecast_hash` | Fingerprint of the forecast series. Two configs producing identical forecasts are **one** trial, however much else differs — this is the dedup key that stops N being inflated. | 16-char hex | `5b0dee1781bc716f` |
| `ic_significance` | The significance test that **decided the route**. Which test ran depends on the path taken. | dict: `method`, `pooled_ic`, `p_value`, `significant` (bool), plus method-specific keys | `{method: block_24_dense_fallback, pooled_ic: 0.0162, p_value: 0.5315, density_pct: 50.01, significant: false}` |
| `ic_significance_block24` | The default block Fisher-z result, always computed even when another method decided — so runs stay comparable across methodology changes. | dict: `pooled_ic`, `z_stat`, `p_value`, `n_eff`, `block_size`, `significant` | `{pooled_ic: 0.0162, z_stat: 0.6257, p_value: 0.5315, n_eff: 1488, block_size: 6, significant: false}` |
| `significance_methodology_used` | Which test decided. Needed because three can, and a later reader reconstructs the maths from this name. Note the config flag that *requests* A8.5.1a is `episode_blocked_a851a`, which is **not** itself a value of this field — the field records which of A8.5.1a's three outcomes actually ran. | `block_{n}_fisher_z` (default, n_eff-deflated) · `episode_block_bootstrap` (A8.5.1a, episode resampling) · `episode_bootstrap_insufficient_n` (A8.5.1a, too few episodes — descriptive only) · `block_24_dense_fallback` (A8.5.1a, signal too dense for episodes) · stationary-bootstrap label (degenerate-forecast fallback) | `block_24_dense_fallback` — **the literal `24` while `block_size` is `6`; see [E037-10](FINDINGS.md#e037-10)** |
| `degenerate_active_forecast` | Flags that the component emits one constant magnitude whenever active, which makes `ic_active_bars` mathematically undefined rather than "zero edge". Prevents a code shape being read as a scientific result. | `true` / `false` | `false` |
| `active_forecast_distinct_count` | How many distinct forecast values occurred on active bars. The measurement behind the flag above. | integer >= 0; `1` means constant | `2` |
| `cost_check` | Whether the estimated gross edge could survive round-trip trading costs at the implied turnover. The second of the two gates, known in the amendments as **Layer 2**. | dict; `pass` true only when `edge_to_cost_ratio >= safety_factor_required` | `{symbol: BTCUSDT, estimated_gross_edge_bps_per_trade: 2.6012, cost_bps_per_trade: 17.0, edge_to_cost_ratio: 0.153, safety_factor_required: 2.0, pass: false, ic_used: ic_active_bars}` |
| `sigma_bar_bps` | Per-bar volatility in basis points. Converts a unitless IC into an expected edge in bps, which is what the cost comparison needs. | float > 0 | `160.1854` |
| `sigma_is_placeholder` | Whether `sigma_bar_bps` was measured or defaulted. **`true` invalidates `cost_check` and every required-IC figure in this file** — read it before trusting any of them. | `true` (default constant, not a measurement) / `false` (measured) | `false` |
| `turnover_proxy` | How often the signal would trade, inferred from activity transitions. Drives the per-trade cost estimate. | dict: `active_bars_total`, `implied_trades_estimated`, `avg_holding_bars`, `forecast_sparsity_pct` | `{active_bars_total: 8928, implied_trades_estimated: 8926, avg_holding_bars: 1.0, forecast_sparsity_pct: 49.99}` |
| `gap_skipped_pairs` / `gap_skipped_pct` | How much of the sample was discarded for straddling a hole in the data cache. The pct is over pairs **reached** post-warmup, **not** the cache's contamination rate. | integer >= 0 / float 0-100 | — *absent: added by `97d3bd7a` on 2026-08-29, one day after this run* |
| `gap_stats_by_symbol` | The same accounting per symbol, because a pooled "no gap effect" can conceal one symbol's sample being wiped out. | dict keyed by symbol | — *absent, same reason* |
| `n_eff_placeable_blocks` / `n_eff_nominal_blocks` | Effective sample size with and without gap-awareness. The pair shows how much the gaps cost in statistical power. | integer >= 0 | — *absent, same reason* |
| `ic_by_era` | IC broken out per market era, so a result that only exists in one regime-era is visible rather than averaged away. | dict keyed `SYMBOL::era_id`; `null` off the A8.5.1a path | `{BTCUSDT::era_2019_2023_full_feed: {ic_active_bars: 0.02237, active_n_bars: 4464, n_episodes: 1}, ETHUSDT::…: {ic_active_bars: 0.010224, …}}` |
| `ic_by_regime` | Reserved for per-regime IC. Deliberately not computed — A2.3 suspends it until a trustworthy detector exists, and the field carries that reason so nobody reads the absence as an oversight. | always `{suspended: true, reason: …}` | `{suspended: true, reason: "A2.3: ic_by_regime suspended until a trustworthy detector exists. …"}` |
| `component_error_count` / `component_error_sample` | How many bars threw a swallowed exception inside the strategy's `update()`, plus a capped sample of them. Separates "the signal is bad" from "the code is broken". | integer >= 0 — a rate above **5%** of processed bars forces `route: no_signal_artifact` (F5c) / list, capped at 5 entries | `0` / `[]` |
| `a86_power_check` | The a-priori power verdict, present **only** on the `insufficient_power_a_priori` path, where the run died before any IC was computed. Its presence means this file is one of the two A8.6 stubs, not a result. | dict: `min_detectable_ic`, `plausible_ic_upper`, `expected_n_eff`, `data_requirement`; absent otherwise | — *absent: run_060 took the normal path* |
| `config_sha8` / `computed_at` / `protocol_version` / `symbols` / `prescreen_windows_used` / `n_bars_total` | Provenance — what was run, against what, when. Makes the result reproducible and comparable. | hex8 / ISO-8601 UTC / path string / list / list of month labels / integer | `041ea0ef` / `2026-08-28T19:54:01.052853+00:00` / `protocols\funding_mr_4h_retest_v1.json` (**backslash — see [E037-11](FINDINGS.md#e037-11)**) / `[BTCUSDT, ETHUSDT]` / 49 month labels `2019-12`…`2023-12` / `17854` |

**Notes**

- ⚠️ **Three shapes, not one.** Besides the full result, the A8.6 power gate
  writes a stub — and the *two* gate sites write **different** stubs:
  - **validation-gate path** (run_phase1_research.py line 2297) — 5 keys:
    `run_id`, `route`, `a86_power_check`, **`stage_blocked_at: validation`**,
    `note: "A8.6 power gate: no component built, no trial spent."`
  - **pre-flight path in `run_loop`** (`:6226`) — 4 keys, the same minus
    `stage_blocked_at`, and a different note: *"A8.6 pre-flight: power
    insufficient before any prescreen IC computed."*

  Neither carries any IC, cost or provenance field. A consumer that needs to
  know *where* the run was stopped must key on `stage_blocked_at`, which only
  one of the two writes. Both shapes are real: `runs/run_060/` holds a voided
  5-key stub (`prescreen_result.VOID_block_size_bug.yaml`) from the
  validation-gate path, alongside the full result the re-run produced.
- `sigma_is_placeholder: true` is the one flag that invalidates other fields
  in the same file. Read it before reading `cost_check`.

---

## 4. Information-loss checklist

The procedure S2 and S4 are held to: a **relocation inventory**, not an eyeball
pass. A rewrite that cannot produce it does not land.

### 4.1 Before rewriting a section

1. **Freeze the source.** Record the reviewed commit SHA and the exact line
   range of the section being rewritten.
2. **Extract the fact inventory.** Every one of the following in the source
   range gets a row, with its source line number:
   - amendment codes (`A8.6`, `A2.3`, `A6.2`, `#50`, `F5c`, `D1`–`D6`, …)
   - measured numbers and counts (`21 of 25`, `74 of 138`, `91%`, `5%`, `2.0`)
   - dates (`2026-08-27`, `run_044`, `run_060`)
   - decisions and their stated reason ("rejected because it destroys 91% …")
   - named traps and the failure they prevent
   - cross-references to other files
   The extraction is **mechanical, not judged** — see 4.4.
3. **Assign each row a destination** before writing: `stays` / `moves to §X` /
   `duplicated in §X` (duplication is allowed; deletion is not).

### 4.2 After rewriting

4. **Produce the relocation inventory** as a table committed alongside the
   rewrite:

   | Fact (verbatim fragment) | Source §/line | Destination §/line | Verbatim? |
   |---|---|---|---|
   | `"of 25 unconstrained expansion runs, 21 land in [3,6]"` | §2.2 L134 | §2.2.3 Notes L— | yes |

   `Verbatim? = no` requires a one-line justification in the same row. Any
   row without a destination is a **loss** and blocks the change.

5. **Run the mechanical residue check** (4.3). Zero unexplained residue, or
   each residue item is listed with its destination.

6. **Re-verify anchors.** Every `file:line` the rewrite introduces or carries
   is re-checked against the working tree at the review SHA. A stale anchor is
   a finding, not a typo.

### 4.3 The mechanical check

Token-level, so it cannot be talked past. From the repo root, comparing the
pre-rewrite blob against the working tree:

```bash
# 1. amendment codes / issue refs / run ids that existed before and not after
diff \
  <(git show <BASE>:strategy-research/docs/USER_GUIDE.md \
      | grep -oE '\b(A[0-9]+\.[0-9]+(\.[0-9]+[a-z]?)?|F[0-9]+[a-z]?|D[0-9]+|#[0-9]+|run_[0-9]+|Impr [0-9]+)\b' \
      | sort | uniq -c) \
  <(grep -oE '\b(A[0-9]+\.[0-9]+(\.[0-9]+[a-z]?)?|F[0-9]+[a-z]?|D[0-9]+|#[0-9]+|run_[0-9]+|Impr [0-9]+)\b' \
      strategy-research/docs/USER_GUIDE.md \
      | sort | uniq -c)

# 2. numbers and dates
diff \
  <(git show <BASE>:strategy-research/docs/USER_GUIDE.md \
      | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]+(\.[0-9]+)?%?' | sort | uniq -c) \
  <(grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]+(\.[0-9]+)?%?' \
      strategy-research/docs/USER_GUIDE.md | sort | uniq -c)

# 3. backticked identifiers (file names, fields, functions)
diff \
  <(git show <BASE>:strategy-research/docs/USER_GUIDE.md \
      | grep -oE '`[^`]+`' | sort | uniq -c) \
  <(grep -oE '`[^`]+`' strategy-research/docs/USER_GUIDE.md | sort | uniq -c)
```

A count that goes **down** must appear in the relocation inventory with a
reason. A count that goes **up** is fine (enrichment is the point).

> Shell note: run these under **bash**, not PowerShell — PowerShell's pipeline
> passes objects and the `uniq -c` counts come back wrong. Line-ending noise
> is avoided because both sides come through `git show`/`grep` on the same
> checkout.

### 4.4 Why mechanical, and its limits

The EPIC's named failure mode is "an agent optimising for a tidy document and
quietly dropping the sentence that explains why a guard exists." An agent
re-reading its own rewrite will not catch that — it already believes the
result is complete. The token diff does not care what the agent believes.

**It works, measured on this document.** Rewriting §3.2's field table, the
check flagged five vanished tokens. Four were genuine losses, restored: `F5c`
and its 5% threshold, `update()`, the `insufficient_power_a_priori` route
name, and the term "Layer 2". The fifth, `required_gross_edge_bps`, had never
existed — the guide documents a `cost_check` subkey no code emits, which
became [E037-14](FINDINGS.md#e037-14). **The check finds phantom content as well as
lost content**, and none of the five was visible on a read-through.

**Limits, stated honestly:** it catches dropped *tokens*, not dropped
*reasoning*. "Rejected because it destroys 91% of the sample" → "rejected
(91%)" passes the check and loses the reason. That is what the inventory's
`Verbatim?` column is for, and why prose rationale moves verbatim by default.
Neither control is sufficient alone.

### 4.5 Landing criteria

A rewrite lands only when all four hold:

- [ ] relocation inventory committed, every row has a destination
- [ ] mechanical residue check run, output pasted, every decrease explained
- [ ] all `file:line` anchors re-verified at the review SHA
- [ ] a reviewer other than the author has read the inventory (not the doc)

---

## 5. Findings raised while proving the template

Filling in stage 7 forced a read of the code. These are the disagreements it
surfaced. **Recorded, not fixed** — per the EPIC's record-don't-fix rule. No
code and no guide text was changed.

> **[`FINDINGS.md`](FINDINGS.md) is the canonical record** — full text,
> severity, type, affected `file:line`, and a proposed disposition per
> finding. S2 appends to it. The table below is an index into it, kept here so
> this document stays readable on its own; it is deliberately a pointer rather
> than a second copy, so the two cannot drift apart.

| ID | Severity | One line — full text in [`FINDINGS.md`](FINDINGS.md) |
|---|---|---|
| [E037-01](FINDINGS.md#e037-01) | medium | Stage 7's row credits the Python tool with the A8.6 power check; it is orchestrator logic, not in `prescreen_signal.py` at all. |
| [E037-02](FINDINGS.md#e037-02) | medium | The `route` enum omits `no_signal_artifact`, which overrides every other route. |
| [E037-03](FINDINGS.md#e037-03) | low | The field table shows 6 of ~30 keys and is not marked as a selection; `forecast_hash` and `sigma_is_placeholder` are among the missing. |
| [E037-04](FINDINGS.md#e037-04) | medium | `Created by` is wrong on one of three creation paths, and that path emits a 4-key artifact §3 never mentions. |
| [E037-05](FINDINGS.md#e037-05) | medium | "block-bootstrap" names the fallback as if it were the default; there are three methods and the default is block-deflated Fisher z. |
| [E037-06](FINDINGS.md#e037-06) | low | Trial recording (A6.2) is credited to the tool; it is the orchestrator. |
| [E037-07](FINDINGS.md#e037-07) | **high** | Stage 7 rewrites stage 10's `regime_audit_decision.yaml` in place, and that entry has no `Updated by` line — invisible to any reader. |
| [E037-08](FINDINGS.md#e037-08) | low | Two significance thresholds (`0.10` and `0.05`) decide different things; neither is documented. |
| [E037-09](FINDINGS.md#e037-09) | medium | `strategy-research/CLAUDE.md` lists a different 10-stage workflow and asserts the schema validation §3 records as false. |
| [E037-10](FINDINGS.md#e037-10) | **high** | The 2026-08-28 "label must track the arithmetic" fix missed the A8.5.1a path; run_060 stamps `block_24_dense_fallback` with `block_size: 6`. Code defect. |
| [E037-11](FINDINGS.md#e037-11) | medium | `protocol_version` is stamped as a platform-dependent path; `Path(...).name` mis-parses it on POSIX. |
| [E037-12](FINDINGS.md#e037-12) | medium | The guide cites 14 distinct amendment codes across 26 mentions and never once says where any of them is defined. Unresolvable references are how the documented C4 confabulation incident happened. |
| [E037-13](FINDINGS.md#e037-13) | medium | `prescreen_signal.py` labels the ungated-escape write-back "A9.1", but A9.1 is the `keltner_163` must-reject fixture; the governing rules look like A2.1 / A2.3 rule 5. |
| [E037-14](FINDINGS.md#e037-14) | medium | The guide documents a `cost_check` subkey `required_gross_edge_bps` that no code emits, while omitting six real ones. |

**Verified consistent** (no finding): §2.2's "A8.1: both IC significance AND
`cost_check.pass` required for `proceed_to_backtest`" matches
`_determine_route` exactly. §2.1's placement of A8.6 at both validation_gate
and signal_prescreen matches the two orchestrator call sites.

---

## 6. What S1 did not do

- Did not touch the other 12 stages or the other ~30 artifacts.
- Did not modify `docs/USER_GUIDE.md`. The worked sample lives here so the
  shape can be rejected cheaply.
- Did not restructure the stage map (§2.1) — that is S4.
- Did not fix any code, and did not correct the guide text for E037-01–E037-08.
- Did not shorten anything.
