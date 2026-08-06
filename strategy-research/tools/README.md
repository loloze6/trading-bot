# tools/ — what each tool is for

Lookup table for an operator who has forgotten what a file does. One entry per
tracked file in `strategy-research/tools/` (20 files).

**Reading the STATUS field**

| Status | Meaning |
|---|---|
| `live` | Some production file imports it or shells out to it. Breaking it breaks a pipeline stage. |
| `CLI-only` | Nothing imports it. That is its **normal, healthy state** — it is a command you run by hand or from a runbook/dispatch. A CLI entry point is never imported, so "no referrer" is not evidence of death. |
| `orphaned` | Genuinely unreferenced *and* superseded. Only one file here. |

"PROD referrer" below means a non-test `.py`/`.sh`, a `config/*.yaml`, a
`workflow/*.yaml`, or the git hook. Tests, docs, briefs, `runs/` and `results/`
are excluded — a tool referenced only from those is still CLI-only, not dead.

---

## build_inventory.sh

**PURPOSE** — Regenerates `engineering/improvements/ongoing-improvement-design/INVENTORY.tsv`: every tracked file under
`strategy-research/` with its byte count and git-history aggregates.
*In plain terms: takes stock of the repo so you can decide what to archive.*

**WHO READS IT** — No PROD referrer. CLI entry point, run by hand during cleanup work.

**HOW IT IS INVOKED** — `sh strategy-research/tools/build_inventory.sh` (no
arguments). `cd`s to the repo root itself (`:12`), so it can be run from anywhere.

**KEY PARAMETERS** — None. Three paths are excluded by design (`:5-10`, `:36`,
`:193`): its own output TSVs and the script itself — self-description would make
the generator non-idempotent.

**STATUS** — CLI-only.

---

## check_data.py

**PURPOSE** — Confirms the OHLCV bars a protocol needs are actually on disk, and
refuses if the protocol's date range overlaps the sealed holdout window.
*In plain terms: "do we have the data, and are we about to cheat?"*

**WHO READS IT** — No PROD referrer. CLI entry point; run before launching a
protocol. Reads `config/campaign_data_policy.yaml` (`:36`).

**HOW IT IS INVOKED** (docstring `:4-12`, argparse `:195-212`):
```
python strategy-research/tools/check_data.py
python strategy-research/tools/check_data.py --protocol strategy-research/protocols/baseline_v2.json
        [--policy PATH] [--skip-data-check] [--timeframe 1h|1d|...]
```

**KEY PARAMETERS**
- `--protocol` — the protocol to check; also where symbols and dates are read from.
- `--policy` — override which data-policy file defines the sealed window.
- `--skip-data-check` — only test for holdout overlap; don't download anything.
- Exit codes (`:14-17`): `0` clean, `1` **holdout overlap — hard rejection**, `2` data gap > 1 day.

**STATUS** — CLI-only.

---

## deflate_sharpe.py

**PURPOSE** — Applies the Bailey & López de Prado (2014) Deflated Sharpe Ratio,
discounting a run's Sharpe for how many hypotheses the campaign has already tried.
*In plain terms: if you test enough ideas, one will look good by luck. This says
how good it would have to look to not be luck.*

**WHO READS IT (PROD, measured)**
- `workflow/stages.yaml:153` — `tool: tools/deflate_sharpe.py` for the robustness stage
- `workflow/run_phase1_research.py:3940` — mirrors its `exclude_invalidated_trials` logic in a separate copy

**HOW IT IS INVOKED** (docstring `:11-13`, argparse `:351-363`):
```
python strategy-research/tools/deflate_sharpe.py <run_id> [--campaign-state PATH]
```

**KEY PARAMETERS**
- `run_id` — which run to deflate; artifacts read from `runs/<run_id>/artifacts/`.
- `--campaign-state` — where the trial history comes from (defaults to `strategy-research/campaign_record/campaign_state.yaml`). This file supplies the trial count that drives the whole correction.

**STATUS** — live.

---

## episode_significance.py

**PURPOSE** — Computes IC significance by bootstrapping over **episodes** (runs of
consecutive active bars) rather than fixed 24-bar blocks.
*In plain terms: if a signal only fires during a handful of multi-day events, you
have a handful of independent observations — not thousands. This counts them honestly.*

**WHO READS IT (PROD, measured)**
- `workflow/run_phase1_research.py:2141` — `import episode_significance as _es`; `:2132` cites its `VALID_METHODS`
- `config/campaign_config.yaml:46,51` — the `episode_significance:` block holds its thresholds
- Imports `prescreen_signal` at `:48` to reuse `_spearman` / `_block_adjusted_significance` rather than reimplement them

**HOW IT IS INVOKED** — As a library, imported by the orchestrator. No `main()`.

**KEY PARAMETERS** (all live in `campaign_config.yaml`, not here)
- `gap_bars: 48` — how long a quiet stretch has to be before it ends one episode and starts another.
- `min_n_episodes: 8` — below this, no significance claim is made at all ("a bootstrap over 4 episodes is theater", `:27-29`).
- `density_fallback_pct: 50` — if the signal is on more than half the time, episodes are meaningless; fall back to the old 24-bar method.

**STATUS** — live.

---

## fragment_patterns.py

**PURPOSE** — Diagnostic tables over LIFO trade fragments in `trades.json`.
*In plain terms: descriptive "what did the trades look like" statistics, for
coming up with new ideas — never for judging an existing one.*

**WHO READS IT** — **No PROD referrer, by design.** A firewall (`:5-16`) forbids
any decision-path code from importing it; `tests/test_fragment_patterns_firewall.py`
enforces this mechanically, and `tests/…` asserts `run_protocol.py` does not import it.

**HOW IT IS INVOKED** — As a library: `compute_fragment_patterns_for_run(run_dir,
protocol_result)` (`:314`) → `write_fragment_patterns_yaml(path, data)` (`:360`).

**KEY PARAMETERS** — None to tune. Every table it emits is stamped
`basis: lifo_fragment, ideation_only` (`:11-12`). If you find yourself citing this
output in a verdict, the firewall has been breached.

**STATUS** — CLI-only (library; deliberately unreferenced).

---

## holdout_date_gate.sh

**PURPOSE** — Scans the git index for any date inside the sealed holdout window
(defined by `campaign_data_policy.yaml:holdout_range`) and blocks the commit if it
finds an unregistered one.
*In plain terms: the mechanical lock on the data we promised not to look at.*

**WHO READS IT (PROD, measured)**
- `tools/hooks/pre-commit:23` — resolves it as `$GATE`; `:33` runs it, `:26-31` blocks the commit if the file is missing
- `config/holdout_gate_exemptions.txt:1,23,32` — the registry it consumes, which documents this tool as its consumer
- Reads the registry at `:57`

**HOW IT IS INVOKED** (`:42-45`)
```
sh strategy-research/tools/holdout_date_gate.sh              # scan the index (hook mode)
sh strategy-research/tools/holdout_date_gate.sh --self-test-only
sh strategy-research/tools/holdout_date_gate.sh --report-residual   # path<TAB>count, registry format
```

**KEY PARAMETERS**
- `--report-residual` — lists what would block, in the exact format the exemption registry uses. This is how you generate candidate entries.
- **Deny by default** (`:17-21`): missing git, failed self-test, unreadable registry, or *zero files scanned* all FAIL the commit. Silence is never success. Exit `0` clean, `1` blocked.

**STATUS** — live.

---

## hooks/pre-commit

**PURPOSE** — The versioned source of truth for the git pre-commit hook: runs the
holdout gate, then the test suite.
*In plain terms: `.git/hooks/` isn't tracked, so a fresh clone would silently have
no checks at all. This is the copy that survives cloning.*

**WHO READS IT** — Nothing imports it; git runs the **installed copy**, not this one.

**HOW IT IS INVOKED** — Install once per clone (`:7-8`):
```
cp strategy-research/tools/hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```
Thereafter git runs it on every `git commit`.

**KEY PARAMETERS**
- Gate 1, holdout date gate (`:22-33`) — fast, unconditional, runs first.
- Gate 2, `pytest tests/ -q` in `trading-bot/` (`:38-40`) — blocks on exit 1/2/3; exit 5 (no tests collected) is tolerated.
- Bypass is `git commit --no-verify` (`:18`) — and if you use it, say why in the commit message.

**STATUS** — live.

---

## lint_verdict_provenance.py

**PURPOSE** — Standalone checker that every verdict-bearing record in the knowledge
base and the queue either cites a resolvable `pass_rule_evaluation.yaml` or honestly
declares itself `ungated`.
*In plain terms: audits whether the campaign's memory is making claims it can't back up.*

**WHO READS IT** — No PROD referrer. CLI entry point — deliberately so: it exists
precisely because the same check previously ran *only* as a side effect of the
orchestrator writing a file, so hand edits went unexamined between runs (`:4-21`).
It imports `record_schema` (`:43`) and `verdict_criteria_evaluator` (`:44`).

**HOW IT IS INVOKED** (`:23-24`, argparse `:87`)
```
python strategy-research/tools/lint_verdict_provenance.py [--root <dir>]
```

**KEY PARAMETERS**
- `--root` — audit a different tree (used by tests).
- Exit `0` = every claim is backed; exit `1` = at least one record asserts something nothing in the repo supports (`:26-29`).

**STATUS** — CLI-only. Run it after any hand edit to the KB or the queue.

---

## measure_bar_sigma.py

**PURPOSE** — Measures `sigma_bar_bps` — the standard deviation of one-bar returns,
in bps — for the 19 recorded Kraken pairs.
*In plain terms: how much a typical bar moves. It sets the bar for how big an edge
has to be to beat costs.*

**WHO READS IT (PROD, measured)**
- `config/holdout_gate_exemptions.txt:192,198` — registered (1 line) with a note explaining it measures the walk-forward window only
- Mirrors `prescreen_signal._sigma_from_records` (`:172`, `:224`) and calls out `_DEFAULT_SIGMA_BAR_BPS` as a fallback that was wrongly used as a measurement (`:18`)

**HOW IT IS INVOKED** (`:5`, argparse `:261-267`)
```
python -m tools.measure_bar_sigma [--pairs ...] [--start ...] [--end ...]
                                  [--local-data PATH] [--full-history]
```

**KEY PARAMETERS**
- `--pairs` / `--start` / `--end` — which instruments and window. Defaults are the walk-forward extension window; it **refuses** to read sealed candles (`:125`).
- `--full-history` — widen beyond the default window.
- Why it exists: this figure was wrong twice, in opposite directions, and one wrong scalar produced a terminal "the family is untradeable" verdict (`:11-25`). Do not substitute a remembered number.

**STATUS** — CLI-only.

---

## measure_funding_carry.py

**PURPOSE** — Measures realized perpetual-funding carry on the in-sample window only.
*In plain terms: how much you'd actually have earned or paid just for holding a
perp position, historically.*

**WHO READS IT** — No PROD referrer under the `config/*.yaml` definition.
`config/holdout_gate_exemptions.txt:181` registers it (1 line) — that file is `.txt`,
so it falls outside the measured PROD set but is a real reference.

**HOW IT IS INVOKED** — `python strategy-research/tools/measure_funding_carry.py`
(no arguments; `main()` at `:73`). Reads exactly two CSVs (`:4-5`).

**KEY PARAMETERS**
- `WINDOW_START` / `WINDOW_END` (`:25-26`) — hardcoded `2019-12-01 .. 2023-12-31`, **on purpose**: the CSVs on disk physically contain the frozen holdout and a sealed Kraken tranche, and the shared loader applies no bound of its own (`:7-12`). The bound lives here so it cannot be forgotten.
- `SYMBOLS` (`:28`) — BTCUSDT, ETHUSDT.
- No repair, no imputation: malformed input raises (`:17`).

**STATUS** — CLI-only.

---

## panel_backtester.py

**PURPOSE** — Research-only vectorized backtester for cross-sectional (multi-symbol)
strategies that the production engine structurally cannot express.
*In plain terms: the real engine trades one symbol at a time. This one ranks a
basket against itself — long the strong, short the weak.*

**WHO READS IT (PROD, measured)**
- `config/campaign_queue.yaml:237` — named as the tool for that entry; `:256` records `research_path_panel_backtester_20260722`
- `config/campaign_data_policy.yaml:170` — its flat + `kraken_1h` cache-path patterns
- `config/holdout_gate_exemptions.txt:182` — registered, 1 line

**HOW IT IS INVOKED** (`:483-491`)
```
python strategy-research/tools/panel_backtester.py gate
python strategy-research/tools/panel_backtester.py xs [--lookback 168] [--rebalance 24] [--min-n 6]
```

**KEY PARAMETERS**
- `gate` — **run this first.** Reproduces an archived production run (run_054) to prove this file's accounting matches the trusted engine (`:11-14`). A cross-sectional result from an ungated build is not evidence.
- `xs --lookback` — how many hours of past return the ranking uses (default 168 = 1 week).
- `--rebalance` — how often to re-rank, in bars (default 24 = daily).
- `--min-n` — minimum eligible symbols before it will trade at all.
- Its Sharpe/drawdown formulas are deliberate copies of the engine's (`:18-22`) so the gate catches drift.

**STATUS** — live (research path; explicitly NOT production, `:4-8`).

---

## power_check.py

**PURPOSE** — A-priori statistical power check at hypothesis registration: can this
test detect the effect it's looking for, given how rarely the signal fires?
*In plain terms: asks "even if we're right, do we have enough data to prove it?"
before spending a backtest finding out.*

**WHO READS IT (PROD, measured)**
- `workflow/run_phase1_research.py:3284` — `"A8.6: A-priori power pre-flight (inline of power_check.py logic)"`; `:3436` — `"Mirrors power_check.py logic identically — both must be updated together."`

⚠️ Note: that is a **duplicate, not an import**. `_run_a86_power_check` (`:3432`)
reimplements this file. Change one and you must change the other.

**HOW IT IS INVOKED** (`:22`, argparse `:123-127`)
```
python power_check.py --hypothesis-card path/to/hypothesis_card.yaml
                      [--config path/to/campaign_config.yaml] [--out path/to/out.yaml]
```

**KEY PARAMETERS**
- `--hypothesis-card` — supplies activation rate, symbol count, plausible IC ceiling.
- `--config` — where `rho_bar` (how correlated the symbols are) is read from; defaults to `../config/campaign_config.yaml`.
- Exit `0` power adequate, `1` insufficient power a priori, `2` missing params (`:24`).
- For market-wide signals the `sqrt(n)` shortcut is **not** used — it materially overstates power (`:10-12`).

**STATUS** — CLI-only (but its logic is live via the orchestrator's copy).

---

## prescreen_signal.py

**PURPOSE** — The cheap gate before a full walk-forward backtest: feeds bars into
the signal layer only (no portfolio simulation), computes information coefficient,
significance, and the Layer-2 cost hurdle.
*In plain terms: does this signal predict anything at all, and is the prediction
big enough to pay for the trading? Kills bad ideas for pennies.*

**WHO READS IT (PROD, measured)**
- `workflow/run_phase1_research.py:1002` — the real invocation, `subprocess.run`; `:1011` raises on failure
- `workflow/stages.yaml:70` — `tool: tools/prescreen_signal.py` for the `signal_prescreen` stage
- `config/campaign_config.yaml:15,24` — the `prescreen:` block; `config/cost_model.yaml:258` — its Layer 2 formula
- `tools/episode_significance.py:48`, `tools/measure_bar_sigma.py:18`, `tools/fragment_patterns.py:68` — reuse its statistics
- `config/campaign_queue.yaml:115,176,179` — notes on what it does and does not read

**HOW IT IS INVOKED** (`:32-34`, argparse `:1360-1363`)
```
python strategy-research/tools/prescreen_signal.py <config_path> <protocol_path>
       [--run-id run_041] [--out-dir DIR]
```

**KEY PARAMETERS**
- `config_path` / `protocol_path` — the candidate strategy and the windows to screen it on.
- `--run-id`, `--out-dir` — artifact labelling and destination; the orchestrator sets both.
- Route out (`:13-14`): `proceed_to_backtest` requires **both** a significant IC and a passing cost check. Otherwise `kill_no_ic` / `refine_inverted_ic` / `kill_cost_hurdle`.
- It evaluates IC on **active bars**, not all bars (`:16-18`) — a sparse signal's all-bar IC collapses toward zero from tie mass at forecast=0.

**STATUS** — live.

---

## record_schema.py

**PURPOSE** — Closed (allow-list) schema for knowledge-base findings and queue
entries: a record may contain **only** the enumerated fields, and a verdict may
live in exactly one designated field.
*In plain terms: stops anyone — human or model — from smuggling a conclusion into
the campaign's memory under a field name nobody thought to forbid.*

**WHO READS IT (PROD, measured)**
- `workflow/run_campaign.py:69` — `import record_schema`; `:124` validates each queue entry against `QUEUE_ENTRY_SCHEMA` on save
- `tools/lint_verdict_provenance.py:43,64,66` — uses both `KB_FINDING_SCHEMA` and `QUEUE_ENTRY_SCHEMA`

**HOW IT IS INVOKED** — Library only. `validate_kb_finding(entry)` / the queue
equivalent (`:366`, `:370`), both wrapping `validate_record_schema` (`:336`).

**KEY PARAMETERS**
- `KB_FINDING_SCHEMA`, `QUEUE_ENTRY_SCHEMA` — the two allow-lists. Adding a field means editing these.
- Design rationale (`:5-36`) is worth reading before you widen anything: three previous rounds used *denylists* of forbidden field names and each was defeated within minutes by a synonym. Enumerating good names is the fix; enumerating bad ones is not.

**STATUS** — live.

---

## retune_regime_detector.py

**PURPOSE** — One-shot grid search over regime-detector parameters
(`ER_enter`, `ER_exit`, `min_dwell`), scored only on intrinsic criteria.
*In plain terms: hunts for detector settings that produce stable, sensibly-sized
regimes — deliberately without looking at whether they make money.*

**WHO READS IT** — No PROD referrer. It writes `config/regime_retune_winner.json`
(`:72`).

⚠️ **This file is already slated for deletion elsewhere.** Documented here for
completeness; no action taken in this pass.

**HOW IT IS INVOKED** (`:22-24`, argparse `:363-366`)
```
python strategy-research/tools/retune_regime_detector.py [--symbols ...]
       [--start 2024-01-01] [--end 2025-12-31] [--skip-validate]
```

**KEY PARAMETERS**
- Grid (`:12-16`): `ER_enter` 0.20–0.45, `ER_exit_ratio` {1.00, 0.80}, `min_dwell` {1, 6, 12, 24} bars.
- Scoring is the four intrinsic criteria only (`:4-10`), max 8 points — persistence, activation band, class-conditional sensitivity, transition frequency. **No PnL, Sharpe or IC**, by firewall.

**STATUS** — orphaned, pending deletion.

---

## run_protocol.py

**PURPOSE** — Walk-forward protocol runner: executes each protocol window as an
independent backtest via `core.launcher.run_backtest`, then emits
`protocol_result.yaml` / `protocol_summary.json`.
*In plain terms: this is the thing that actually runs the backtest. It takes a
strategy and a list of date ranges, trades each range separately so results can't
leak between periods, and writes down what happened.*

**WHO READS IT (PROD, measured)**
- `workflow/run_phase1_research.py:1048` — the real invocation, `subprocess.run` on the `protocol_execution` stage
- `workflow/stages.yaml:89` — `tool: tools/run_protocol.py` for that stage
- `config/cost_model.yaml:4,66,115` — names it as the consumer of the fee blocks
- `config/campaign_queue.yaml:174` — notes it never reads `timeframe` from the protocol
- `config/campaign_data_policy.yaml:333` — `run_protocol.py:1173` used as a reproduction fixture
- `tools/verdict_criteria_evaluator.py:5,9` — replaces this file's `evaluate_against_decision_rules`
- `tools/fragment_patterns.py:7`, `tools/panel_backtester.py:234` — reference its decision-rule and `_SPARSE_TRADE_FLOOR` semantics

**HOW IT IS INVOKED** (argparse `:980-1008`)
```
python strategy-research/tools/run_protocol.py <config_path> <protocol_path>
       [--validation-protocol PATH] [--out-dir DIR]
       [--cost-product {spot,perp}] [--commission-bps FLOAT]
       [--holdout --i-understand]      # both or neither, enforced at :1011
```

**KEY PARAMETERS**
- `config_path` — the strategy being tested (its parameters).
- `protocol_path` — which date windows to test it over.
- `--validation-protocol` — the pass/fail rules for this specific hypothesis.
- `--out-dir` — where results land; the orchestrator points this at the run folder.
- `--cost-product` — which fee table to charge the run at: `spot` (default) or `perp`. Don't use `perp` for funding-carry ideas.
- `--commission-bps` — manual fee override, to ask "does the edge still hold at X bps?". Beats `--cost-product` when both are given.
- `--holdout` + `--i-understand` — unlocks the sealed final test data. Two flags on purpose, so it can't happen by accident.
- `_SPARSE_TRADE_FLOOR = 5` (`:33`) — windows with fewer closed trades get a **null** Sharpe rather than a noisy one.

**STATUS** — live.

---

## stamp_protocol.py

**PURPOSE** — Version-stamps a protocol JSON file and prints its content hash for
pasting into a pre-registration's `protocol_ref_content_hash`.
*In plain terms: fingerprints the test plan, so you can prove afterwards that the
plan wasn't edited once the results came in.*

**WHO READS IT (PROD, measured)**
- `workflow/run_phase1_research.py:2198` — cited over the field-name collision with K3's own §5 stamp

**HOW IT IS INVOKED** (`:18-20`, argparse `:60-61`)
```
python strategy-research/tools/stamp_protocol.py protocols/ts_trend_daily_v2.json
python strategy-research/tools/stamp_protocol.py protocols/<file>.json --version 2026-07-15
```

**KEY PARAMETERS**
- `protocol_path` — the file to stamp.
- `--version` — the version label to write (defaults to today).
- The hash is **structural**, not byte-verbatim (`:6-11`): keys are sorted before hashing, so hand-editing whitespace or reordering keys does not change it. It also excludes the protocol's own version/hash fields, avoiding a hash-of-a-hash loop.
- The formula is deliberately duplicated from `run_phase1_research.py`'s `_compute_protocol_content_hash` (`:11-16`) because importing that module drags in the agent SDK. A round-trip test pins the two together.

**STATUS** — live.

---

## validate_regime_detector.py

**PURPOSE** — Deterministic validation of the regime detector: persistence,
transition frequency, parameter sensitivity, activation rate — and a confidence
grade derived from them.
*In plain terms: before trusting "the market is trending", checks that the label is
stable, not hair-trigger, and doesn't fire absurdly often or almost never.*

**WHO READS IT (PROD, measured)**
- `workflow/run_phase1_research.py:1465` — invokes it via subprocess; `:1439` re-runs it when the report is stale or absent; `:1472` warns on failure
- `workflow/stages.yaml:122` — `tool: tools/validate_regime_detector.py`
- `config/campaign_config.yaml:64` — the `regime_detector:` thresholds block
- Reads `config/campaign_data_policy.yaml` at `:426`

**HOW IT IS INVOKED** (`:31-34`, argparse `:419-423`)
```
python strategy-research/tools/validate_regime_detector.py
       [--config PATH] [--symbols ...] [--start 2024-01-01] [--end 2025-12-31] [--out PATH]
```

**KEY PARAMETERS**
- `--config` — the strategy config whose detector is being graded.
- `--start` / `--end` — the window to grade over.
- `--out` — defaults to campaign-level `regime_detector_report.yaml` at the root of `strategy-research/`.
- Confidence rules (`:15-23`): `high` needs persistence ≥ 24 bars, ≤ 4 transitions/window, sensitivity ≤ 0.15 **and** activation inside the band. Rare labels (activation < 10%) are graded on class-conditional sensitivity instead.
- **Retune firewall** (`:25-27`): detector parameters may only be tuned on intrinsic criteria. PnL, Sharpe or IC must never appear in retune acceptance.

**STATUS** — live.

---

## verdict_criteria_evaluator.py

**PURPOSE** — The machine-checkable pass-rule evaluator (K2 kernel): reads a run's
computed results plus its pre-registered criteria and resolves the verdict
deterministically — no keyword matching, no prose parsing, no LLM.
*In plain terms: the pre-registration said what "success" means; this decides
whether it happened, with no room for interpretation.*

**WHO READS IT (PROD, measured)**
- `workflow/run_campaign.py:70` — `import verdict_criteria_evaluator as vce`
- `workflow/run_phase1_research.py:1082`, `:3066`, `:3271` — `import verdict_criteria_evaluator as _vce`; `:2272` cites its `legacy_not_evaluable` path
- `tools/lint_verdict_provenance.py:44`, `tools/record_schema.py:40` — provenance validation

**HOW IT IS INVOKED** — Library only, imported by the orchestrator. Gates are
composed in the evaluator list at `:490`.

**KEY PARAMETERS**
- Gate ids at `:55` onward, e.g. `cost_model_completeness` (G1, implemented `:329`).
- Read `:26-35` before trusting a pass: **G1–G4 are presence checks, not content checks.** They establish that a figure was *reported*, not that it was reported carefully — `skew: 0`, `cost_basis: ""` and `mechanism_explanation: "."` all clear their gates. A MET precondition is not a quality warrant.
- It supersedes `run_protocol.py`'s `evaluate_against_decision_rules` as the decision authority (`:9-12`); that function's output is informational from here on.

**STATUS** — live.

---

## whale_footprint_evaluation.py

**PURPOSE** — Evaluation harness for `prereg_whale_footprint_v2.yaml`: applies the
pre-registration's own thresholds and verdict mapping mechanically.
*In plain terms: the Phase 2.3 scorer. Every number it checks against comes out of
the pre-registration file, so it cannot be talked into a different answer.*

**WHO READS IT** — No PROD referrer. CLI entry point — this is the Phase 2.3
evaluation path, invoked from its dispatch.

**HOW IT IS INVOKED** (argparse `:296-300`)
```
python strategy-research/tools/whale_footprint_evaluation.py --prereg <path> [--run-id manual_run]
```

**KEY PARAMETERS**
- `--prereg` — required; **every** threshold is read from it, none are hardcoded here (`:5-6`).
- `--run-id` — labels the run for the single-use mark.
- Gate order is fixed (`:13-18`): single-use → economic feasibility → coverage floor → minimum-N. The first blocking gate stops evaluation, and a blocked run does **not** consume the single-use mark.
- Economic feasibility (`:20-30`) is data-independent: if the required IC exceeds what a correlation can even express, the idea is untradeable before any data is collected.
- ⚠️ `:8-11`: this module is **unrun against the real capture**. Every existing test uses synthetic planted-answer fixtures.

**STATUS** — CLI-only.
