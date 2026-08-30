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
`features / logic`). I recommend **not** adding them as columns. Argument:

- **The existing cells are already prose, not cells.** §2.2's stage-3
  Objective is 68 words and contains a quoted string, a parenthetical, a
  measured count and a date. Stage 4's contains a conditional
  (`if min_detectable_ic > plausible_ic_upper`). These are paragraphs living
  in a table because there was nowhere else to put them.
- **Markdown tables cannot hold what the new columns must hold.** A stage
  input is a *list* of files with provenance. Logic is a *numbered sequence*.
  Neither survives a `|`-delimited cell — no line breaks, no nesting, no code
  fences. The only way to fit them is to compress, and compressing is exactly
  how the hard constraint gets violated.
- **7 columns of prose is unreadable at any terminal width.** The current
  4-column table already wraps badly. 7 would be worse, and the widest column
  (logic) is the one the operator most needs to read carefully.
- **The bug-list symptom needs precision, not glanceability.** "Which
  sub-steps does this feature reach?" is answered by an exact I/O contract
  with `file:line` anchors. That is a block, not a cell.

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

**Objective.** One sentence. WHY this stage exists, in plain language, in
terms of what it buys the campaign. Not a call sequence. Not a list of
amendment codes. If you cannot say it without naming a function, it is not
an objective yet.

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

**Features / logic in place**

Numbered, concrete, in execution order. Each step names the amendment code
it implements where one exists, and carries a `file:line` anchor.

1. Step … (A8.3) — `tools/x.py:123`
2. Step … — `tools/x.py:456`

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

**Why the fields are these:**

- **Engine / Runs** — separated because "who executes" and "when" were
  conflated. Stage 9 is auto-triggered; stage 1 is a human. The current table
  buries "auto-triggered before verdict when the report is stale" inside the
  Objective.
- **Required?** on inputs — the difference between "the stage cannot run" and
  "the stage degrades" is the single most useful thing to know before you
  change a producer.
- **Side effects called out in output** — see finding F7 below. Stage 7
  writes into stage 10's artifact and no reader of the guide could know.
- **`file:line` anchors** — the guide's §2 preamble already says "when this
  section and the code disagree, the code wins and this section is a bug."
  Anchors are what make that checkable instead of aspirational.

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
**Schema:** `path/…` — *(declared; not enforced at runtime, see §3 preamble)* | *(none)*

| Field | Definition |
|---|---|

**Notes** *(optional)* — traps, invalidation conditions, fields that mean
something other than they look like.
```

**Rules that make the metadata normalised:**

1. **All five metadata lines are always present.** Absence is written
   explicitly — `*(none — write-once)*`, `*(none)*` — never omitted. Today a
   missing line is ambiguous between "does not apply" and "nobody checked".
   `trade_diagnostics.json` has no `Schema` and no `Updated by`; a reader
   cannot tell which case it is.
2. **`Created by` lists every path.** If two different pieces of code can
   write the file, both are named. See finding F4.
3. **`Schema` states enforcement status inline.** §3's preamble already
   records that no schema is loaded by any code; repeating the status at each
   entry stops the per-entry line from implying validation that does not
   happen.
4. **The rationale headliner is one line and blockquoted**, so it is visually
   distinct from the metadata and cannot be mistaken for another field.
5. **Field tables stay descriptive, not exhaustive** — but if the table is a
   selection from a larger real artifact, that is stated. Otherwise a reader
   concludes a field does not exist. See finding F3.
6. **"Logic" prose does not live here.** Per the EPIC, it relocates to the
   owning stage's block. The artifact entry describes the *file*; the stage
   block describes the *computation*. (Relocation, not deletion — §4.)

---

## 3. Worked sample

Filled in by reading `strategy-research/tools/prescreen_signal.py` and
`strategy-research/workflow/run_phase1_research.py`, not by paraphrasing the
existing text. Disagreements are in §5.

### 3.1 Stage 7

#### Stage 7 — `signal_prescreen`
**Engine:** Python tool (`tools/prescreen_signal.py`), launched as a
subprocess by the orchestrator (`workflow/run_phase1_research.py:1074`
`run_tool_worker`). No LLM call, no token cost.
**Runs:** after `backtest_specification` emits `spec_ready`. The orchestrator
runs an A8.6 power pre-flight *around* the tool first — see logic step 0.

**Objective.** Decide cheaply, on the signal alone, whether this idea
deserves an expensive walk-forward backtest. A full protocol run costs
compute and — because every run counts as a trial — it costs statistical
budget. The prescreen buys that decision for the price of one pass over the
forecast series: does the signal carry directional information at all, and
could it clear its own trading costs if it did?

**Stage input**

| What | Where it comes from | Required? |
|---|---|---|
| `artifacts/candidate_strategy_config.json` | stage 6 `backtest_specification` | yes |
| protocol JSON (`symbols`, `windows`, `timeframe`) | `_resolve_protocol_path()` — `run_phase1_research.py:1086` | yes |
| `config/cost_model.yaml` | repo config — round-trip cost bps per symbol, `safety_factor` (default 2.0) | yes |
| `trading-bot/local_data/{SYMBOL}_{tf}.csv` | data cache; a coarser timeframe is DERIVED from a finer one (`_resolve_ohlcv_source`, `prescreen_signal.py:306`) | yes |
| aux feeds — funding rate, fear & greed | `config` `aux_feeds` list; loaded at `prescreen_signal.py:151`/`:171` | only if config declares them |
| `config/campaign_data_policy.yaml` | eras + `episode_significance` settings | only on the A8.5.1a path |
| `runs/{run_id}/artifacts/regime_audit_decision.yaml` | stage 10 | only if present — read to resolve A9.1, see side effect below |
| `campaign_state.yaml` | campaign root | read by the orchestrator wrapper, not the tool |

**Stage output**

| What | Written where | Read by |
|---|---|---|
| `prescreen_result.yaml` | `runs/{run_id}/prescreen/`, copied to `runs/{run_id}/artifacts/` (`run_phase1_research.py:1113`) | `verdict_interpreter`, orchestrator routing |
| *(side effect)* `regime_audit_decision.yaml` — field `ungated_escape_eligible` resolved in place | `runs/{run_id}/artifacts/` | `verdict_interpreter`, orchestrator — **stage 10's artifact, rewritten by stage 7** (`prescreen_signal.py:1582` → `:1092`) |
| *(side effect, orchestrator not tool)* a row in `campaign_state.trial_sharpes` | campaign root | `deflate_sharpe.py`, campaign accounting |

**Features / logic in place**

0. **A8.6 a-priori power pre-flight — orchestrator, before the tool starts**
   (`run_phase1_research.py:6217`). If `min_detectable_ic > plausible_ic_upper`
   the tool is never launched: the orchestrator writes
   `prescreen_result.yaml` itself with `route: insufficient_power_a_priori`
   and records the trial (`:6232`, `:6235`). The same check also runs earlier,
   at the validation gate (`determine_post_validation_route`, `:2287`), which
   can write the artifact before stage 7 is reached — the orchestrator then
   detects the existing file and skips the tool (`:6207`).
   **This step is not in `prescreen_signal.py` at all.** See finding F1.
1. Load config + protocol; derive `block_size = bars_per_day(timeframe)` from
   `tools/timeframe.py` — the single source shared with the A8.6 gate and
   `power_check.py`. There is no fallback; an unparseable timeframe raises.
   (`prescreen_signal.py:1215`)
2. Per symbol: load OHLCV over the full protocol range (earliest window start
   → latest window end), merge aux feeds, extract the forecast series by
   driving the real strategy through `CandleBuilder` (`_extract_forecasts`,
   `:470`).
3. **Gap suppression (#50 A).** A forecast/return pair whose two bars are not
   one expected step apart spans a data gap and is dropped. Counts are
   surfaced per symbol, because pooled figures can read "no gap effect" while
   one symbol's entire sample was destroyed (red-team D6). (`:1264`, `:1267`)
4. **Degenerate-input guards — fail loud, not flattering.** A symbol whose
   usable record count is zero *because of* gap suppression raises (`:1284`).
   If no symbol loaded any usable data at all, the run raises rather than
   emitting a route from zero bars (`:1320`, added 2026-08-28 after run_060).
5. Pool records across symbols; compute `ic_all_bars` and `ic_active_bars`
   separately (A8.3). Active-bar IC — conditional on a non-zero/changing
   forecast — is the primary gate; all-bars IC is tie-dominated for sparse
   signals and is reserved for A2.1.
6. **Significance on active-bar n.** Default method is **block-deflated
   Fisher z**: `n_eff = active_n / block_size`, `z = IC * sqrt(n_eff - 3)`,
   labelled `block_{block_size}_fisher_z` (`:643`, `:1377`). The label is
   derived from the block size actually used — it read `block_24_fisher_z`
   until 2026-08-28 while `block_size` had already become per-timeframe, so a
   4h run stamped `block_24` while dividing by 6.
   **#50 (B):** a block that cannot be placed without spanning a gap does not
   exist and does not enter `n_eff`; counted per symbol, because pooling
   first would read the seam between two symbols as a contiguous step
   (`:1359`).
   Two alternative methods replace it:
   - **A8.5.1a episode-blocked** (opt-in, config `significance_methodology:
     episode_blocked_a851a`) for multi-era backward-extension data (`:1402`).
     Default behaviour with the flag absent is unchanged, so every archived
     run stays reproducible.
   - **Stationary block bootstrap** (automatic fallback) when the active-bar
     forecast is *structurally* degenerate — one constant magnitude whenever
     active, so `ic_active_bars` is undefined by construction rather than a
     no-edge result (`:730`, branch at `:1429`, detector `:720`; found 2026-07-07 via the P4_ts_trend
     shakedown). A merely-small active sample is a power problem, not a
     structural one, and is left to A8.5.1a's own disposition.
7. **Turnover proxy** — active bars per trade implies a holding period
   (`_compute_turnover_proxy`, `:813`). Redefined 2026-07-07 to count
   activity transitions; the prior sign-flip-only counter silently merged
   long-only episodes across flat gaps into one trade.
8. **Cost check (Layer 2).** Estimated gross edge from `ic_for_cost` ×
   `sigma_bar_bps` × holding period, versus round-trip cost from
   `cost_model.yaml`. Passes when `edge_to_cost_ratio >= safety_factor`
   (default 2.0) (`:897`). `sigma_bar_bps` is measured from the records; if no
   symbol yields an estimate, a placeholder `_DEFAULT_SIGMA_BAR_BPS = 15.0` is
   substituted and `sigma_is_placeholder: true` is carried into the artifact —
   **when that flag is true the cost check and every required-IC figure in the
   artifact are invalid.**
9. **Route decision** (`_determine_route`, `:982`) — see the route table.
   A8.1: both IC significance **and** `cost_check.pass` are required for
   `proceed_to_backtest`.
10. **F5c zero-signal-artifact override** (`:1481`), which takes priority over
    every route above. If `active_n_bars == 0`, or swallowed component
    exceptions exceed 5% of processed bars, the route becomes
    `no_signal_artifact`. This must not be scored as `kill_no_ic`:
    `kill_no_ic` says "tested, found nothing", whereas here the hypothesis was
    never tested. From run_044 (2026-07-04) — a
    `FundingRateMeanReversionComponent` divide-by-zero produced
    `active_n_bars=0`, which read as a real `kill_no_ic` verdict and nearly
    closed an otherwise-untested hypothesis family.
11. **A2.3:** `ic_by_regime` is emitted as `{suspended: true}` — suspended
    until a trustworthy detector exists. Only ungated IC decides the
    prescreen.
12. **A9.1 side effect:** resolve `ungated_escape_eligible` in stage 10's
    `regime_audit_decision.yaml` using `ic_all_bars` — the all-bars IC is the
    only metric A2.1 admits, because an IC computed on detector-gated bars is
    not admissible for or against the escape (A2.3 rule 5) (`:1582`, `:1092`).
13. Write `prescreen_result.yaml` (`:1585`).
14. **A6.2 trial recording — orchestrator, after the tool returns**
    (`_record_prescreen_trial`, `run_phase1_research.py:4039`, called at
    `:1130`). Kills count as trials; `statistic_valid = "neither"` when there
    is no backtest Sharpe. Upsert on `(trial_id, "prescreen")` since 2026-08-16
    (issue #28 / E-025) so a crash-retry replaces the stale row instead of
    being swallowed. **Not in `prescreen_signal.py`.** See finding F6.

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

- Signal layer only — no portfolio simulation, no backtest engine invocation.
- Two significance thresholds operate in one function and only the first is
  documented anywhere: `_SIG_THRESHOLD = 0.10` is the main IC gate
  (`prescreen_signal.py:87`), while `p > 0.05` is a *secondary* test inside
  the cost branch separating `kill_cost_hurdle` from `refine_cost_hurdle`.
- `gap_skipped_pct` is computed over pairs actually **reached** (post-warmup).
  It is **not** the cache's contamination rate — gaps inside the warmup are
  never reached, so it reads lower than `tools/cache_gap_census.py` by a
  config-dependent amount (red-team D4/D5). For the cache rate, run the census.
- The gap fix is partial and knowingly so: (A) fixes the return label and (B)
  the block count. **Neither fixes rolling indicators, which still span the
  holes.** Segment-and-re-warm would fix it and was rejected — it destroys 91%
  of the `kraken_SUIUSD` train sample.
- `n_eff_nominal_blocks` is computed over the *post-*(A) active count, so it
  is a like-for-like comparison against `n_eff_placeable_blocks`, not the
  pre-#50 value.

**Owned by which code**

`tools/prescreen_signal.py:1185` (`run_prescreen`) · `:982` (`_determine_route`)
· `:643` (`_block_adjusted_significance`) · `:730` (stationary block bootstrap)
· `:897` (`_cost_check`) · `:1092` (`_resolve_ungated_escape`) ·
`workflow/run_phase1_research.py:1074` (`run_tool_worker`) · `:6217` and `:2287`
(A8.6) · `:4039` (`_record_prescreen_trial`)

### 3.2 Artifact `prescreen_result.yaml`

### `prescreen_result.yaml`

> **Why this file exists.** It is the record of the cheap go/no-go on a
> signal — the evidence that justified either spending a full walk-forward
> backtest on this hypothesis or killing it without one. It is also the
> trial's receipt: `forecast_hash` from this file is what stops the same
> signal being counted twice in the deflated-Sharpe denominator.

**Created by:**
- `signal_prescreen` tool — `tools/prescreen_signal.py:1585` (normal path)
- orchestrator — `workflow/run_phase1_research.py:6232`, when the A8.6
  pre-flight blocks before stage 7 and the tool never runs
- orchestrator — `workflow/run_phase1_research.py:2297`, when A8.6 blocks
  earlier still, at the validation gate

**Updated by:** *(none — write-once per run; the orchestrator copies it from
`runs/{run_id}/prescreen/` to `runs/{run_id}/artifacts/` unchanged,
`run_phase1_research.py:1113`)*
**Read by:** `verdict_interpreter`, orchestrator routing
(`determine_post_prescreen_route`), `_record_prescreen_trial`,
`_check_prescreen_conformance` (`run_phase1_research.py:3146`)
**Written to:** `runs/{run_id}/prescreen/prescreen_result.yaml`, copied to
`runs/{run_id}/artifacts/prescreen_result.yaml`
**Schema:** `workflow_artifacts/schemas/prescreen_result.schema.json` —
*declared; not loaded by any code, see §3 preamble*

*Selected fields — the artifact carries roughly 30 top-level keys; this table
covers the decision-bearing ones.*

| Field | Definition |
|---|---|
| `route` | Routing decision: `proceed_to_backtest`, `kill_no_ic`, `refine_inverted_ic`, `refine_cost_hurdle`, `kill_cost_hurdle`, `no_signal_artifact`, `insufficient_power_a_priori` |
| `route_rationale` | Human-readable sentence explaining the route, with the numbers that drove it |
| `prescreen_kill_reason` | `no_informational_content_this_venue`, `insufficient_episodes_a851a`, `cost_drag_structural`, `component_error`, `zero_activation`, or null |
| `ic_all_bars` | Spearman IC over all bars (tie-dominated for sparse signals); the only metric A2.1 admits for the ungated escape |
| `ic_active_bars` | Spearman IC conditional on non-zero/changing forecast — the primary IC gate |
| `ic_spearman_pooled` | Legacy alias, equals `ic_active_bars`; kept for backward compatibility |
| `active_n_bars` | Count of active bars; `0` forces `no_signal_artifact` |
| `forecast_sparsity_pct` | Fraction of bars with zero/unchanging forecast |
| `forecast_hash` | Fingerprint of the forecast series — the dedup key for trial counting |
| `ic_significance` | Result of the significance test that **decided the route** |
| `ic_significance_block24` | The original block Fisher-z result, always computed for continuity even when another method decided |
| `significance_methodology_used` | Which of the three methods decided: `block_{n}_fisher_z`, `episode_blocked_a851a`, or the stationary block bootstrap |
| `degenerate_active_forecast` | Structural flag: the component emits one constant magnitude when active, so `ic_active_bars` is undefined rather than zero |
| `active_forecast_distinct_count` | Distinct active-bar forecast values; the input to the flag above |
| `cost_check` | `{pass, edge_to_cost_ratio, required_gross_edge_bps, safety_factor_required, …}` — Layer 2 gate |
| `sigma_bar_bps` | Per-bar volatility in bps used by the cost check |
| `sigma_is_placeholder` | **`true` invalidates `cost_check` and every required-IC figure in this file** — the sigma is a default constant, not a measurement |
| `turnover_proxy` | `{active_bars_total, implied_trades_estimated, avg_holding_bars, forecast_sparsity_pct}` |
| `gap_skipped_pairs` / `gap_skipped_pct` | Pairs suppressed for spanning a data gap; the pct is over pairs **reached**, not over the cache |
| `gap_stats_by_symbol` | Per-symbol gap accounting — a pooled "no gap effect" can hide one symbol's sample being destroyed |
| `n_eff_placeable_blocks` / `n_eff_nominal_blocks` | Gap-aware vs nominal effective sample, for like-for-like comparison |
| `ic_by_era` | Per-era IC report; populated only on the A8.5.1a path, else null |
| `ic_by_regime` | `{suspended: true}` — A2.3, until a trustworthy detector exists |
| `component_error_count` / `component_error_sample` | Swallowed component exceptions during `update()`; > 5% forces `no_signal_artifact` (F5c) |
| `a86_power_check` | Present **only** on the `insufficient_power_a_priori` path; carries `min_detectable_ic`, `plausible_ic_upper`, `expected_n_eff`, `data_requirement` |
| `config_sha8` / `computed_at` / `protocol_version` / `symbols` / `prescreen_windows_used` / `n_bars_total` | Provenance |

**Notes**

- The file has **two shapes**. On the A8.6 path it is a four-key stub
  (`run_id`, `route`, `a86_power_check`, `note`) — none of the IC, cost or
  provenance fields exist. Any consumer must tolerate that.
- `sigma_is_placeholder: true` is the one flag that invalidates other fields
  in the same file. Read it before reading `cost_check`.

---

## 4. Information-loss checklist

The procedure S2 and S4 are held to. It is a **relocation inventory**, not an
eyeball pass. A rewrite that cannot produce this table does not land.

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

The failure mode the EPIC names is "an agent optimising for a tidy document
and quietly dropping the sentence that explains why a guard exists." An agent
reviewing its own rewrite by reading it will not catch that — it already
believes the result is complete. The token diff does not care what the agent
believes.

**Limits, stated honestly:** the check catches dropped *tokens*, not dropped
*reasoning*. A sentence rewritten from "rejected because it destroys 91% of
the sample" to "rejected (91%)" passes the mechanical check and loses the
reason. That is what the relocation inventory's `Verbatim?` column is for,
and it is why prose rationale is required to move **verbatim** by default.
The two controls are complementary; neither alone is sufficient.

### 4.5 Landing criteria

A rewrite lands only when all four hold:

- [ ] relocation inventory committed, every row has a destination
- [ ] mechanical residue check run, output pasted, every decrease explained
- [ ] all `file:line` anchors re-verified at the review SHA
- [ ] a reviewer other than the author has read the inventory (not the doc)

---

## 5. Findings raised while proving the template

Filling in stage 7 forced a read of the code. These are the disagreements it
surfaced. **Recorded, not fixed** — per the EPIC's record-don't-fix rule. They
seed `E-037/FINDINGS.md` in S2. No code and no guide text was changed.

| ID | Severity | Finding |
|---|---|---|
| **F1** | medium | §2.2 stage 7's Objective opens "A8.6 pre-flight first (blocks if power insufficient)", under Engine = *Python tool*. `tools/prescreen_signal.py` contains **no power check at all**. A8.6 runs in the orchestrator, at `run_phase1_research.py:6217` (immediately before the tool subprocess) and again at `:2287` inside `determine_post_validation_route`. The stage row conflates orchestrator wrapper logic with tool logic — exactly the confusion E-037 exists to remove. §2.1's stage map is *not* wrong here: it correctly attaches A8.6 to both validation_gate and signal_prescreen. |
| **F2** | medium | §3's `prescreen_result.yaml` `route` enum lists 6 values and **omits `no_signal_artifact`**, which the code emits at `prescreen_signal.py:1481` and which **overrides every other route**. A reader of §3 cannot know the most consequential route exists. |
| **F3** | low | §3's field table lists 6 fields; the written artifact has roughly 30 top-level keys. Load-bearing omissions: `forecast_hash` (dedup key for trial counting), `sigma_is_placeholder` (invalidates `cost_check` when true), `significance_methodology_used`, `gap_stats_by_symbol`, `a86_power_check`. Not an error — but nothing marks the table as a selection, so absence reads as non-existence. |
| **F4** | medium | §3 says **Created by:** "signal_prescreen tool (`tools/prescreen_signal.py`)". On the insufficient-power path the file is created by the **orchestrator** (`run_phase1_research.py:6232` and `:2297`) and the tool never runs. The `Created by` line is wrong for one of its three creation paths, and the resulting artifact has a completely different shape (4 keys, no IC/cost/provenance fields) that §3 does not mention. |
| **F5** | medium | Both §2.2 stage 7 ("block-bootstrap significance") and §3 (`ic_significance` — "block-bootstrap") name the **fallback** method as if it were the default. The default is block-deflated **Fisher z** (`z = IC * sqrt(n_eff - 3)`, `prescreen_signal.py:643`, labelled `block_{n}_fisher_z` at `:1377`). A stationary block bootstrap runs only on the degenerate-active-forecast path (`:730`), and A8.5.1a episode-blocking is a third method (`:1402`). Three methods, one name in the doc. |
| **F6** | low | §2.2 stage 7 says "Records trial in `campaign_state.trial_sharpes` (A6.2)". Done by the orchestrator (`_record_prescreen_trial`, `run_phase1_research.py:4039`, called at `:1130`, `:6215`, `:6235`), not by the tool. Same class as F1. |
| **F7** | **high** | **Undocumented cross-stage write.** `run_prescreen` writes into **stage 10's** artifact: it opens `runs/{run_id}/artifacts/regime_audit_decision.yaml` and resolves `ungated_escape_eligible` in place (`prescreen_signal.py:1582` → `_resolve_ungated_escape`, `:1092`). §3's `regime_audit_decision.yaml` entry says **Created by:** "regime-auditor skill" and has **no** `Updated by` line, so no reader of the guide could discover that stage 7 rewrites it. This is precisely the input/output-contract blind spot the EPIC blames for the bug list feeling uncontrollable — and it is the strongest evidence that the `Updated by` normalisation in §2 of this document is load-bearing rather than cosmetic. |
| **F8** | low | Two significance thresholds live in `_determine_route` and only the stricter one is documented anywhere: `_SIG_THRESHOLD = 0.10` gates IC significance (`prescreen_signal.py:87`), while a second `p > 0.05` test inside the cost branch decides `kill_cost_hurdle` vs `refine_cost_hurdle` (`:1042`). Neither §2.2 nor §3 mentions either number. |

| **F9** | medium | `strategy-research/CLAUDE.md` — loaded into every session in this directory — contradicts `USER_GUIDE.md` twice. (a) It lists a **10-stage** workflow (`screening_backtest`, `walk_forward_validation`, `final_holdout_test`, `robustness_analysis`, `research_decision`) that does not match the guide's canonical 13 stages; four of those five names exist nowhere in the guide. (b) Its global rule "Validate outputs against schemas before moving to the next stage" asserts exactly the schema enforcement that §3's own 2026-08-27 correction records as **false**. The guide's §2 preamble claims to be "the only place that is maintained as authoritative", but the file an agent reads *first* says something else. Out of scope to fix here; noted because S4's cross-linking work has to decide whether `CLAUDE.md` points at the guide or restates it. |

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
- Did not fix any code, and did not correct the guide text for F1–F8.
- Did not shorten anything.
