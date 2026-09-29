# C4 prep — two real runs on the new pipeline (continuation plan C4.1–C4.4)

**Status:** prepared 2026-09-29, **not started**. Nothing here runs until the operator gives an
explicit go. No real LLM call, backtest or trial row was made to write this file.

## In plain words

1. **Ready to go, except three things only you can do:** pick the idea for the first brief
   (§3), say how the flag switch is recorded (§2.3), and give the go.
2. **The switch is 14 flags, not 12.** The runbook's list predates profit bars v2 and score
   provenance; both are added here (§2.1).
3. **Switching the flags also changes what the tests see.** The register test ties each flag's
   declared state to the real config file, so the switch must flip the register too, and some
   tests read the real config. §2.4 has the (partial) measured effect; one clean suite run is
   still needed before the go.
4. **C4 gives the cost numbers solidly, but only one or zero data points for the patch
   question (C5.4).** Two runs cannot give a rate; §4.3 says what C4 can and cannot tell us.

---

## 1. Pre-conditions (C4.1) — checked 2026-09-29 on master `5816dced`

| Pre-condition | State | Evidence |
|---|---|---|
| C0–C3 merged | yes (E-062 S2b-2c moved after C4 by the operator) | SESSION_LOG 2026-09-29; PRs #254–#267 |
| C1.1 end-to-end test green with the C2/C3 extensions | yes (28/28 incl. slow at S2b-4) | PR #267 |
| Bars file signed | yes, `ratified_by`/`ratified_at` set | `config/profitability_bars.yaml:233-234`, PR #269 |
| Bars file sha on THIS checkout | `a752a2eb…` (CRLF) — matches SIGNING_CHECKLIST §5 | `certutil -hashfile`, measured today |
| `residual_ic` menu entry ratified | yes, `ratified: true` | `config/criterion_menu.yaml:151` |
| No campaign running | yes, no `campaign.pid` | measured today |
| Queue has no ready entry that would run first | yes: P4_ts_trend `blocked_on_daily_bar_ingest`, 4 others `done` | `config/campaign_queue.yaml` |
| No campaign memory / block registry yet | yes — first run creates them | `campaign_record/` listing |
| Venv has the SDKs | yes (claude-agent-sdk 0.2.82, google-genai 2.16.0) | SESSION_LOG 2026-09-29 |

**Grade and spend on this Windows checkout only** until CUL-348 (bars sha depends on line
endings). C4 never spends the holdout; before any spend: CUL-340, CUL-335, CUL-348.

---

## 2. The flag set (C4.2)

### 2.1 Exact edit — `strategy-research/config/campaign_config.yaml`, `orchestrator:` block

14 flags go `false` → `true`; the 5 already on stay on; `halt_policy.quarantine_enabled` stays
`false`. Unquoted booleans only (7 readers are not strict: a quoted `"false"` reads as ON).

| flag | now | C4 | why / dependency |
|---|---|---|---|
| exclusion_digest_input | true | true | unchanged; switches to `tried_ideas.yaml` once memory exists |
| stale_input_path_fix | true | true | unchanged |
| variant_selection_record | true | true | unchanged; inert under config-direct |
| schedulability_block | true | true | unchanged |
| data_availability_gate | true | true | unchanged |
| config_direct_authoring | false | **true** | root |
| variant_loop | false | **true** | needs config_direct_authoring |
| grid_evaluation | false | **true** | root |
| category_reports | false | **true** | root |
| specialist_readers | false | **true** | needs grid_evaluation + category_reports |
| regroup_record | false | **true** | needs specialist_readers |
| profit_bars_file | false | **true** | root; file is signed |
| profit_bars_every_backtest | false | **true** | needs profit_bars_file + regroup_record |
| **profit_bars_v2** | false | **true** | needs profit_bars_every_backtest (C3 / D-034..D-047) — *not in RUNBOOK §1e's list* |
| decide_next | false | **true** | needs regroup_record + config_direct_authoring |
| verdict_routing_retired | false | **true** | needs decide_next + profit_bars_every_backtest — **declared behaviour change** |
| variant_anti_adjacency_gate | false | **true** | needs regroup_record while no memory file exists; its switch-on condition (S2b replay reported: 0 REPEAT) is met (DECISION_LOG row after D-027) |
| composition_runs | false | **true** | needs decide_next + variant_loop + profit_bars_every_backtest + verdict_routing_retired; residual_ic now ratified |
| **score_provenance** | false | **true** | needs specialist_readers (D-049 item 1) — *not in RUNBOOK §1e's list* |
| halt_policy.quarantine_enabled | false | false | leave off (its DONE path also calls decide_next) |

What two of these do on the very first run, so nothing surprises:
- **composition_runs ON** adds the `residual_ic` criterion (> 0.02, one-sided p < 0.05,
  n_eff ≥ 30) to every forecast-block idea. With no block registered yet the composite is
  `none`, so the residual IC is the candidate's own all-bar IC (`tools/residual_ic.py` header).
  It is one more bar to clear, not a deadlock. A composition run itself cannot fire until two
  blocks are validated (E-060 S4 stays deferred).
- **score_provenance ON** adds one stop path: a reader writing a wrong `rubric_version` twice
  fails the run through the reader retry path (accepted in D-049).

### 2.2 Same edit — `strategy-research/config/feature_flag_register.yaml`

`tests/test_feature_flag_register.py:111-115` fails when a register entry's `state` disagrees
with the real `enabled:` value. So the one edit also sets `state: "on"` on the same 14 entries.
Their `criterion` text should gain one line ("switched on for C4, <date>, operator go").

### 2.3 How the switch is recorded — **operator choice**

**Recommended: a dedicated branch `c4/flag-set`, never merged to master.** One commit flips the
14 flags and the 14 register states. The C4 runs are launched from the main checkout on that
branch, so each run artifact's git SHA pins the exact flag set. Master stays flags-off until
C7's declared "new pipeline becomes the default" change. That is where the tests that assume
flags-off get fixed. The C4 switch is not the place to do it (§2.4).

Rejected alternative: an uncommitted edit on master. The run's config hash would capture it,
but the git SHA would not. It would also leave master's working tree dirty and its suite red
for the whole of C4.

### 2.4 Measured (partial): what the flip does to the test suites

Scratch worktree at master `5816dced` with the §2.1 + §2.2 edit applied by script (diff: 14
`enabled` lines and 14 `state` lines, nothing else). Research suite, all markers, in two
sequential halves:

- **Incomplete.** Half 1 was stopped at about 65% by the host when memory ran low. Half 2
  never ran. A first attempt, two full suites in parallel, died at 13–16% with
  `Windows fatal exception 0xc000070a` inside `ast.parse` (`test_cul336_closed_book`) on
  both the flipped and the unflipped tree. That was my error: this machine needs one suite
  process at a time, in halves (plan rule 11).
- **What was measured:** 12 failures in the first ~65% of half 1 (half 1 = 83 of 167 test files).
  - One contiguous block of 6 near 5% matches the known environmental e054/k3 set (a
    worktree has no venv).
  - The other 6 are **not yet identified**: pytest prints names only at the end.
  - The flip is therefore **not test-neutral**, as expected, since tests read the real config.
- **Still needed before the go:** one flipped-tree run, in halves, one process, while the
  machine is otherwise idle. List every failure. Re-run each failing test on unflipped
  master. A test that fails only when flipped is a flags-off assumption (C7 work). A test
  that fails on both is pre-existing. The C4 go does not need these tests green, but it
  needs each one explained.

---

## 3. First brief (C4.2) — from the C1.7 template

Template: `workflow_artifacts/templates/research_brief_new_pipeline.md`. Copy to
`briefs/<name>.md`, fill every `<FILL IN…>` (registration refuses any left), no `promotion`
block, no `pass_rule` (criteria come from step 1a via `criteria_from: hypothesis_generation`).

**Kept from the template (recommended, answers the DECISION_LOG "first real run: which
protocol" pending item):** BTCUSDT + ETHUSDT, 1h, generated protocol 2018-02-01 → 2025-12-31,
95 monthly windows over four eras (20 / 51 / 11 / 13), holdout omitted so it defaults to the
policy's range. Changing it adds a second unknown to a run whose purpose is to prove the
pipeline and measure it.

**Operator choice — the idea.** Already tried on this campaign (exclusion digest):
RSI mean reversion / momentum, Keltner breakout / mean reversion / trend / score mode, SMA trend
(following), funding-rate mean reversion. Funding carry is out: the engine does not model
funding cash flows yet (`model_funding` off, E-014). Two candidates, both price- or feed-only
with full coverage from 2018-02 on both coins:

- **A (recommended): volatility-managed time-series momentum.** Multi-week return sign, position
  scaled down when recent realised volatility is high. It sits in the lane the kill map ranks
  highest ("slow trend with vol targeting") and is not the plain SMA trend already tried. Who
  pays: trend-following flows and slow re-pricing after large moves; vol scaling cuts the
  crash-risk that kills plain trend on crypto.
- **B: sentiment contrarian on the daily Fear & Greed index** (fear_greed_daily covers 2018-02).
  Different information source, but single-indicator and slower to accumulate the 100 trades
  per coin D-035 requires.

Draft for A (the `<FILL IN>` fields only; everything else stays as the template has it):

```yaml
strategy_domain: "volatility_managed_trend"
venue: "kraken"
product: "spot"
research_goal: >
  Test whether multi-week time-series momentum on BTC and ETH, with position size
  scaled inversely to recent realised volatility, earns a return after fees and
  slippage that beats buy-and-hold. The other side: slow-reacting flows that keep
  trending after large re-pricings; vol scaling is there to cut exposure in the
  high-volatility crash regimes where plain trend following loses most. It must
  trade slowly enough that costs stay a small share of the edge, yet reach 100
  trades per coin over the whole test.
```
Title line: `# Volatility-managed trend on BTC/ETH 1h (C4 first brief)`.

Register (only after the go): `PYTHONUTF8=1 ../venv/Scripts/python.exe workflow/run_campaign.py
register --brief briefs/<name>.md --priority 1 --notes "C4 first new-pipeline brief"`, then
RUNBOOK §1a dry run, then single-step launch (§1d).

---

## 4. Measurement plan (C4.3)

All of it is read from files the runs already write; nothing new has to be built to collect it.

### 4.1 Per stage, per run

| Measure | Where it is recorded |
|---|---|
| turns (must be **1**, CUL-336) | `runs/<run>/pipeline_state.yaml` → `audit_log.<stage>_attempt_<n>.num_turns` |
| tokens (input / output / cache read / cache creation / total / weighted) | same entry → `tokens` |
| cost (USD) | same entry → `cost_usd` |
| wall time (s) | same entry → `execution_time_seconds` (LLM stages only). Tool stages (5a, data gate, protocol_execution, regroup, decide) write **no** audit entry (only the three `"engine":` sites at `run_phase1_research.py:1233/1402/4065` do), so: launch single-step with the console output tee'd to `runs/<run>/c4_console.log` and time each tool stage from it |
| retries | extra `_attempt_<n>` / `_retry<k>` keys per stage |
| readers (5) | `audit_log.specialist_readers_<category>_attempt_<n>[_retry<k>]` — same fields plus `provenance` |
| model actually used vs requested | `provenance.{requested, observed, mismatch, self_report_differs}` (D-048) |
| pauses | `status: paused_for_human` + the `flags` that caused it (e.g. `inconclusive_grid`), time to resume, what the operator did |
| budget breaker | weighted units per run vs `token_budget_per_run_weighted_units` (1.5M) |

Prediction to compare against (A3 §3.8): a forecast-block run is ≥ 8 Claude calls (1a, 1b, 2,
five readers), all on `claude-haiku-4-5`; 3 `run_protocol` subprocesses (base, design, asset
variant). A divergence is a finding to explain, not a number to prefer.

### 4.2 Per run (outcome and accounting)

- Trial rows named `<run_id>:<variant_id>` in `campaign_state.trial_sharpes`; N before and after
  (real ledger N = 12 today). A variant that crashed or was refused still lands its row.
- Grid `idea_status` per idea; profit-bar rows per variant (v2, seven rows) with their basis.
- `campaign_record/campaign_memory.yaml`, `block_registry.yaml` and
  `runs/<run>/artifacts/decision_record.yaml` written.
- Real trades per coin over the whole test (feeds the parked D-047 calendar-rate question).
- The holdout store appears in no stage input and no `run_context.yaml`.

### 4.3 D-049 item 2 (C5.4): reader proposals re-graded on the same windows

**Metric:** among runs whose queue entry carries a `proposal_ref` (the next idea came from a
reader proposal), the share where the source variant's grid result was FAIL/refuted and the
child's is PASS/validated **on the same windows** (same protocol windows fingerprint,
`tools/novelty.py`), reported separately for `kind: patch` and `kind: new_block`
(`tools/reader_proposals.py`). Also recorded: FAIL→FAIL, FAIL→INCONCLUSIVE, and which criteria
flipped.

**What C4 can give:** at most one data point. Run 2 comes from a reader proposal only if
decide_next ranks one above step 1a's extra hypothesis cards for the same brief. So C4 checks
that the lineage is recorded well enough to compute the metric; the rate itself needs the
later campaign runs, and the held-aside-windows decision waits for it (D-049).

### 4.4 D-048: citation resolved / unresolved rate

Per reader and in total: resolved and unresolved evidence paths from
`audit_log.specialist_readers_<category>_attempt_<n>.provenance.citations.proposals.<id>`,
plus `files_unavailable` (an absent grid or registry summary is normal on run 1 and must be
counted apart, or it inflates "unresolved"). Two runs × five readers is 10 reader outputs:
enough to see whether unresolved is near 0 % or large, not a precise rate. The A+/B decision
follows.

### 4.5 Report (C4.4)

One page after run 2: what worked, what broke, cost per run and per stage, the four measures
above, the observed model string. Then the operator decides models per stage and whether the
campaign continues.
