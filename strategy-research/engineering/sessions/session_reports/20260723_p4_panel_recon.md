# P4 Panel-Backtester Recon — 2026-07-23

Read-only recon. No backtest run, no strategy code executed, no KB/queue/protocol file
edited, no git commit made. This is the only file written by this dispatch.

---

## 0. Precondition manifest

- `git status --porcelain`: empty output. MATCH.
- `git log --oneline -1`: `19fa1b9 Arc close-out: refresh NEXT_SESSION.md + SESSION_LOG for C7-EXT/XS-park arc`. MATCH.

Preconditions held; proceeded.

## Premises

- P1: `strategy-research/tools/panel_backtester.py` exists. CONFIRMED (read in full, 546 lines).
- P2: `strategy-research/runs/run_054` and `run_057` exist with `artifacts/` dirs. CONFIRMED.
- P3: `campaign_knowledge_base.yaml` contains `id: p4_sma_trend_longonly_daily_auto` at line 882. CONFIRMED.

All premises held.

---

## Step 2 — Queue entry vs KB finding: verbatim fields

**Queue entry** (`strategy-research/config/campaign_queue.yaml`):
- `status` (line 6): `done`

**KB finding** (`strategy-research/campaign_knowledge_base.yaml`, `id: p4_sma_trend_longonly_daily_auto`, starts line 882):
- `outcome` (line 891): `ungated_er_gate_variant_too_sparse_to_evaluate`
- `verdict_status` (line 892): `ungated`
- `exhausted` (line 1036): `true`
- `exhausted_basis` (lines 1037–1043): `'Empirical (run_057, 2026-07-11): the regime-gated refinement direction prescribed by the prior refine_pending_regime_gating outcome was tested via an ER(20)>=0.30 entry-latch gate (GatedSmaTrendLongOnlyComponent) and killed on the pre-registered pass rule plus an independent S2 mechanism falsification. This closes the ER-at-entry-gate refinement specifically -- it does not, on its own, mark the broader persistent_behavioral_bias / SMA-trend-family search space exhausted (one parameterization tested, per the outcome_reason framing above).'`
- `reactivation_condition` (line 1044): `null`
- Consequence-for-queue sentence, in `readjudication_20260722` (lines 929–931): `'CONSEQUENCE FOR THE QUEUE: P4_ts_trend is neither promoted, refined, nor killed by run_057. It is not reopened by this correction either -- reopening is a separate decision requiring a registration that can actually produce trades.'`

**Uncoordinated/incompatible assertions, listed without resolving:**

1. Queue `status: done` (queue.yaml:6) reads as a closed/terminal lineage state. The KB's own `readjudication_20260722` (kb:929) states in the same breath that the lineage is "neither promoted, refined, nor killed" — a description that does not obviously map onto "done" as a terminal disposition, yet nothing in either file updates `status` away from `done` to reflect the relabelling.
2. The queue's long `notes` field (queue.yaml:10-36) still narrates the 2026-07-11 close under the **superseded** outcome name `kill_er_gate_mechanism_falsified` (queue.yaml:11, 30, 33) — the very label the KB's `readjudication_20260722` (kb:893-894) says was corrected away from on 2026-07-22. The queue's prose was not touched by the 2026-07-22 correction; only the KB fields were.
3. `exhausted: true` (kb:1036) plus `exhausted_basis` (kb:1037) still frames the empirical basis as a `kill` (word "killed", kb:1039), while `outcome`/`verdict_status` (kb:891-892) now assert `ungated`/too-sparse-to-evaluate rather than a kill. `exhausted_basis` was not rewritten in the 2026-07-22 pass to match the new `outcome` wording.
4. `verdict_status: ungated` (kb:892) is, per the readjudication text itself (kb:900-907), the corrected position — no mechanical gate ever ran on run_057 — but the queue's `status: done` gives no indication the closure was non-gated; a reader of the queue alone would not learn that.

I did not edit either file.

### Addendum A1 — `engine_provenance_caveat`

`engine_provenance_caveat` (kb:1045-1063), filed 2026-07-19 (before the 2026-07-22 readjudication):

> `'Filed 2026-07-19 (run_059 close-out, tz-bug arc): protocol_version ts_trend_daily_v1 executed on 1d bars BEFORE the 2026-07-18 CandleBuilder._align() fix (commit 2529f5b). ... the run_054/run_057 verdicts above (kill_er_gate_mechanism_falsified) are MAINTAINED, not relitigated; this caveat exists so a future reader auditing window-edge trade counts knows the historical alignment context.'` (kb:1058-1061, name quoted verbatim)

**Inconsistency:** the caveat names the run_054/run_057 verdicts as `kill_er_gate_mechanism_falsified` — precisely the outcome string the 2026-07-22 `readjudication_20260722` field (kb:893-894) states was relabelled away from, to `ungated_er_gate_variant_too_sparse_to_evaluate` (kb:891). The caveat was never updated after the relabel, so it now cites a name that no longer appears as this finding's `outcome`.

**Which a reader meets first:** reading the finding top to bottom, `outcome` (kb:891) and `verdict_status` (kb:892) appear near the top, immediately after `evidence_count` — a reader sees the corrected `ungated_...` label first. `engine_provenance_caveat` is the last field in the finding (kb:1045), so the stale `kill_er_gate_mechanism_falsified` reference is encountered only after the corrected fields, not before them. `engine_provenance_caveat` is prose addressed to a future auditor of window-edge trade counts (its own stated purpose, kb:1060-1061) — it is not a status field and does not appear to be intended as one of the fields the campaign treats as the current disposition (`outcome`/`verdict_status`/`exhausted`); it reads as an archival footnote whose internal citation simply was not swept forward when the outcome string it names was superseded. Not resolved here, only reported.

---

## Step 3 — run_057 sample, from `runs/run_057/artifacts/` only

Source: `runs/run_057/artifacts/protocol_result.yaml` (996 lines).

- **Symbols:** 2 — BTCUSDT, ETHUSDT (`protocol_result.yaml`, `results[].symbol`, e.g. lines 5, 445; confirmed again at `per_symbol_summary` keys, lines 890/895).
- **Windows per symbol:** 15 each (semi-annual windows 2018-04 through 2025-04; `results[]` entries at lines 5-866, 15 BTCUSDT blocks + 15 ETHUSDT blocks = 30 window-symbol slots total).
- **Per-window trade counts** (`results[].core.trade_count`):
  - BTCUSDT (2018-04→2025-04, lines 12,42,72,100,130,160,188,218,246,276,306,336,366,396,424): `[4,1,0,2,2,0,3,0,1,3,2,1,1,0,0]`
  - ETHUSDT (2018-04→2025-04, lines 452,482,512,542,572,602,630,660,690,720,750,780,808,838,866): `[1,1,1,2,2,0,2,2,2,5,1,0,2,0,1]`
- **Evaluable (non-null) per-window Sharpe:** exactly **1 of 30** slots — ETHUSDT 2022-10, `sharpe: -0.686` (`protocol_result.yaml:718`), on `trade_count: 5` (`protocol_result.yaml:720`). All other 29 window-symbol slots carry `sharpe: null` (confirmed via full-field scan of every `- symbol:`/`sharpe:`/`trade_count:` triple in the file). This matches the KB's own recomputation claim at kb:909-914.
- Aggregate confirmation: `per_symbol_summary` (`protocol_result.yaml:889-899`): BTCUSDT `median_sharpe: null`, ETHUSDT `median_sharpe: -0.686`.
- Pooled expectancy sample: `hypothesis_verdict.diagnostics.per_trade_expectancy_bps` (`protocol_result.yaml:958-962`): `mean: 433.7313, se: 441.388, t_stat: 0.9827, n: 42`.

**`pre_registration.yaml` — `pass_rule` location and evaluability:**
`runs/run_057/artifacts/pre_registration.yaml:20-28`. The `pass_rule` sits under `machine_constraints.pass_rule` (`pre_registration.yaml:7,20`), **not** at the top level of the document. It is a single **prose string** (a paragraph beginning `'PASS (-> refine/promote routing per verdict-interpreter) iff: (a) gated bar-level median Sharpe >= 0.5791 ...'`, lines 20-28) — not the structured `{criteria, outcomes}` shape the K2 kernel (`verdict_criteria_evaluator.py`) requires. It is **prose, not machine-evaluable** — confirmed independently by `verdict_criteria_evaluator.py`'s own resolution logic (Step 7 below), which returns `legacy_not_evaluable` for exactly this shape (`_resolve_pass_rule`, `verdict_criteria_evaluator.py:796-801`).

---

## Step 4 — `panel_backtester.py` input contract

File: `strategy-research/tools/panel_backtester.py` (546 lines), read in full.

- **Universe supply:**
  - Gate path (`validate_gate`): hardcoded 2-symbol tuple `("BTCUSDT", "ETHUSDT")` (`panel_backtester.py:267`).
  - XS path (`run_xs`): hardcoded 19-base list `_XS_UNIVERSE` (`panel_backtester.py:323-324`), sourced per its own comment from `research_brief_XS_momentum.md` frontmatter (`panel_backtester.py:322`).
  - Neither path accepts a universe as a CLI/config argument; both are literal in-file constants.
- **Bar interval(s) and where enforced:**
  - Gate path: daily bars, hardcoded filename pattern `f"{sym}_1d.csv"` (`panel_backtester.py:266`).
  - XS path: hourly bars, hardcoded filename pattern `f"kraken_{base}USD_1h.csv"` (`panel_backtester.py:342`).
  - No timeframe parameter exists anywhere in the file; the interval is fixed by which loader function/filename-pattern is called.
- **Signal/strategy rule expression — function, config, or hardcoded:**
  - Gate path: hardcoded Python function `sma_long_only_signal(closes, L=100)` (`panel_backtester.py:152-157`), long-only 0/1 signal from `close > SMA_L`.
  - XS path: rule logic is inlined directly inside `run_xs()` (`panel_backtester.py:409-424`) — momentum computed once (`MOM`, lines 375-377), cross-sectional rank-based long/short partition computed inline (`np.argsort`, lines 416-421). Not a pluggable function; there is no signal-object/strategy-interface parameter — only numeric knobs (`lookback_L`, `rebalance_every`, `min_n`, `long_short_frac`) are parameterized (`panel_backtester.py:350-352`), the ranking mechanic itself is fixed code.
- **Cost model and its source:**
  - Gate path: `DEFAULT_COMMISSION_RATE = 0.001` (10 bps one-way), a hardcoded module constant (`panel_backtester.py:56`), commented as mirroring the production engine's own default — **not** read from `cost_model.yaml`.
  - XS path: `_load_perp_cost_bps()` (`panel_backtester.py:329-334`) reads `strategy-research/config/cost_model.yaml`'s `perp.fee_rate_bps.default` key (`cost_model.yaml:158-160`, value `5.0` bps).
- **Position/netting model:**
  - Gate path: single-symbol sequential long/flat episodes (`simulate_long_flat`, `panel_backtester.py:160-191`) — one position at a time, no netting needed (one symbol per call).
  - XS path: vectorized dollar-neutral panel netting — weight vector `W` over all N assets, long leg weights sum to `+1`, short leg to `-1` (`panel_backtester.py:379, 420-421`).
- **Output emitted:**
  - Gate path: `validate_gate()` returns `{"all_pass": bool, "rows": [...]}`, a per-field pass/fail comparison table against `runs/run_054/protocol_summary.json` (`panel_backtester.py:260-294`); printed to stdout when run as `python panel_backtester.py gate` (`panel_backtester.py:521-545`). Not written to a file by this script.
  - XS path: `run_xs()` returns a `(result_dict, n_elig_hist, daily_df)` tuple (`panel_backtester.py:450-468`); `result_dict` fields are `spec`, `net_sharpe`, `gross_sharpe`, `total_net_return_pct`, `total_gross_return_pct`, `max_drawdown_pct`, `annualized_turnover_x`, `total_cost_drag_pct_of_equity`, `n_eligible_min/max`, `first_rebalance_ts`. Printed as JSON to stdout under `python panel_backtester.py xs` (`panel_backtester.py:492-520`). Not written to a file by this script.

---

## Step 5 — validation gate against an archived production run

Function: `validate_gate()`, `panel_backtester.py:260-294`. It reproduces **run_054** specifically (`recorded_path = .../runs/run_054/protocol_summary.json`, `panel_backtester.py:262`) — not run_057.

- **Granularity of the check:** every recorded window-symbol slot from run_054's `protocol_summary.json["results"]` (`panel_backtester.py:264, 282`), cross-checked field-by-field against 7 fields per slot (`TOL` dict, `panel_backtester.py:270-278`: `trade_count`, `net_return_pct`, `sharpe`, `max_drawdown_pct`, `gross_pnl`, `net_pnl`, `fees_paid`).
- **Tolerances** (`panel_backtester.py:270-278`): `trade_count` exact match; `net_return_pct` within 0.5 pp OR 2% relative; `sharpe` within 0.10 absolute; `max_drawdown_pct` within 0.5 absolute; `gross_pnl`/`net_pnl`/`fees_paid` within 2% relative.
- **What it validated:** BTCUSDT/ETHUSDT (`panel_backtester.py:267`), daily bars (`_1d.csv`, line 266), **long-only, single-symbol** trend rule (`sma_long_only_signal`, line 152 — the SMA(100) long-only rule, per the module docstring lines 11-14 and 24-36 explicitly describing this as reproducing "P4_ts_trend / run_054, SmaTrendLongOnlyComponent L=100, daily, long-only"). It is explicitly **not** a cross-sectional/ranking/short reproduction — the docstring (line 12) names the exact mechanism reproduced.

---

## Step 6 — Capability question (split per addendum A2)

### 6a. Signal generation

Yes, `panel_backtester.py` computes both entries and exits from raw price series itself in both code paths — it does not merely score externally-supplied trades in either path as actually invoked.

- Gate path: `sma_long_only_signal()` computes the boolean position signal directly from `closes` (`panel_backtester.py:152-157`); `simulate_long_flat()` (`panel_backtester.py:160-191`) walks that signal bar-by-bar and decides entry/exit at lines 178-185 (`if sig and not in_pos: ... elif (not sig) and in_pos: ...`).
- XS path: `MOM` is computed directly from panel closes (`panel_backtester.py:375-377`); the position decision (long/short assignment via cross-sectional rank) happens inline at `panel_backtester.py:409-424`.

**Is the generation path general over rule shapes, or structurally specific to cross-sectional ranking?** The two paths are structurally different, and each is specific to its own shape:
- The single-symbol long-only machinery (`sma_long_only_signal` + `simulate_long_flat`, lines 152-191) is **general in form** — it operates on one symbol's OHLCV plus a boolean signal series, with no cross-sectional dependency, and this is in fact already the exact shape a per-symbol threshold rule (no ranking, no shorts) would need. However, as it stands it is wired into exactly one caller, `validate_gate()`, which hardcodes the symbol pair to `("BTCUSDT", "ETHUSDT")` (`panel_backtester.py:267`) and drives its loop from run_054's own recorded window/result list (`panel_backtester.py:264, 282: for rec in recorded`), not from an arbitrary externally-supplied universe or window set. There is no function in the file that takes an arbitrary symbol list and daily bars and runs `sma_long_only_signal`/`simulate_long_flat` independently per symbol without that run_054-comparison harness around it.
- The cross-sectional ranking machinery (`run_xs`, lines 350-465) is **structurally specific to cross-sectional ranking and dollar-neutrality**: it operates on a `(T, N)` matrix across the whole named universe simultaneously (`panel_backtester.py:369-377`), uses `np.argsort` over assets at a given bar to select longs/shorts (`panel_backtester.py:416-419`), and always produces a dollar-neutral weight vector with a short leg (`panel_backtester.py:420-421`). It has no code path that could run one symbol's rule independent of the others' data being present in the same matrix — it is bound to the panel shape by construction.

### 6b. Trade scoring

Separately, `core_metrics_from_trades(trades)` (`panel_backtester.py:114-145`) is a self-contained function that accepts a list of trade dicts and returns core metrics — nothing about it requires the trades to have been internally generated. Its documented input contract (module docstring, `panel_backtester.py:75-78`) is a list of dicts each carrying `exit_time`, `portfolio_impact_pct`, `profitable_net`, `profit_loss_absolute`, `net_profit_loss_absolute`, `total_commission`, `initial_portfolio_value`, `final_portfolio_value`, `entry_time`.

However, **as the file is actually wired, this function is never called with an externally-supplied trade set** — every call site (`validate_gate()` → `_window_gate()` → `simulate_long_flat()` at line 253, feeding `core_metrics_from_trades` at line 254) passes trades that `simulate_long_flat` itself just generated internally in the same call chain. There is no code path in this file that loads an external trades.json (or any other externally-produced trade list) and scores it through `core_metrics_from_trades`.

**6a vs 6b, stated as the finding:** the file generates its own signals/trades in both paths (6a = yes, generation-driven); the trade-scoring function is *capable* of scoring an externally-supplied set by its input contract, but *nothing in the file currently does that* (6b = capability present, unused/unwired). These are different answers, as anticipated.

### Original Step 6 framing — can it express a long-only daily-bar SMA-trend rule run independently across N symbols, unmodified, at HEAD?

**No**, not as a general-purpose facility, even though the core single-symbol computational primitives already exist and are demonstrably correct (they are exactly what `validate_gate` uses to reproduce run_054). What's missing, one item per file:line:

- **Absent** — a driver function that runs `sma_long_only_signal` + `simulate_long_flat` over an arbitrary, externally-supplied list of N symbols without requiring a matching run_054-style `recorded` comparison set to iterate over. `validate_gate()`'s only loop (`panel_backtester.py:282: for rec in recorded`) is driven by `runs/run_054/protocol_summary.json`'s own contents, not a general symbol list.
- **Present but hardcoded to a fixed 2-symbol case, not absent** — the symbol set itself: `("BTCUSDT", "ETHUSDT")` (`panel_backtester.py:267`).
- **Absent** — an output emitter shaped like `protocol_result.yaml` (with `per_symbol_summary`, `trade_diagnostics_summary`, `hypothesis_verdict` keys — see Step 7). `core_metrics_from_trades` (`panel_backtester.py:136-145`) emits a flatter dict (`net_return_pct, sharpe, max_drawdown_pct, trade_count, win_rate, fees_paid, gross_pnl, net_pnl`) missing fields present in the real engine's `protocol_result.yaml` (e.g. `cost_drag_pct`, `forecast_return_corr`, `avg_trade_duration_bars`, `per_regime`, `regime_validity` — see `runs/run_057/artifacts/protocol_result.yaml:8-34` for the shape these are missing against).
- **Present, general in form, not cross-sectional-specific** — the per-symbol signal/simulate primitives themselves (`sma_long_only_signal`, `simulate_long_flat`, lines 152-191): these could run per-symbol independently with no ranking and no shorts if driven by a different, more general caller.

---

## Step 7 — Gateability question

### (a) Can the evaluator consume `panel_backtester.py`'s output as-is?

**No.** `verdict_criteria_evaluator.py`'s criterion lookup (`_lookup_metric_value`, `verdict_criteria_evaluator.py:173-199`) reads `protocol_result.get("per_symbol_summary")` (per-symbol criteria, line 183-184) or `protocol_result.get("trade_diagnostics_summary")` falling back to `protocol_result.get("hypothesis_verdict", {}).get("diagnostics")` (pooled criteria, lines 186-198). Confirmed against the real engine's own output shape: `runs/run_057/artifacts/protocol_result.yaml` carries exactly these three top-level keys — `per_symbol_summary` (line 889), `hypothesis_verdict` (line 903), `trade_diagnostics_summary` (line 964). The G1–G4 verdict preconditions (`evaluate_verdict_preconditions`, `verdict_criteria_evaluator.py:483-494`) additionally require `deployable_today` (`_gate_deployable_today`, lines 425-450) and inspect `robustness_checks` (`_gate_robustness_mechanism`, lines 453-480) directly off `protocol_result`.

`panel_backtester.py`'s two return shapes — `validate_gate()`'s `{"all_pass", "rows"}` (line 294) and `run_xs()`'s `{"spec", "net_sharpe", "gross_sharpe", "total_net_return_pct", ...}` (lines 450-465) — contain **none** of `per_symbol_summary`, `trade_diagnostics_summary`, `hypothesis_verdict`, `deployable_today`, or `robustness_checks`. Neither shape is consumable by the evaluator unmodified.

### (b) What shape adapter would be required (fields and file:line, not code)

To make a `panel_backtester.py` daily-SMA-across-N-symbols run gateable, an adapter would need to map its output onto:
- `per_symbol_summary: {SYMBOL: {median_sharpe, max_abs_drawdown_pct, min_trade_count, zero_trade_slot_pct}}` — modeled on `runs/run_057/artifacts/protocol_result.yaml:889-899`. `panel_backtester.py` currently computes per-window `sharpe`/`trade_count`/`max_drawdown_pct` per slot inside `_window_gate()` (`panel_backtester.py:237-257`) but never aggregates these into a per-symbol median/min across windows the way `per_symbol_summary` requires.
- `trade_diagnostics_summary` / `hypothesis_verdict.diagnostics.per_trade_expectancy_bps: {mean, se, t_stat, n}` — modeled on `runs/run_057/artifacts/protocol_result.yaml:958-962`. `panel_backtester.py` has no expectancy-aggregation step anywhere; `core_metrics_from_trades` (line 114) computes per-slot totals only, not a pooled per-trade expectancy with SE/t-stat across all slots.
- `deployable_today: {year, net_sharpe, net_return_pct, cost_basis}` — required by G3 (`verdict_criteria_evaluator.py:425-450`); `panel_backtester.py` has no most-recent-full-year breakout at all in either path.
- `robustness_checks` — required by G4 (`verdict_criteria_evaluator.py:453-480`) only when a check is flagged `anomalous`; absent from `panel_backtester.py` entirely (no robustness-check emission of any kind).
- A `pre_registration.yaml`-conformant **structured** `pass_rule` (`{criteria, outcomes}` shape, not prose) would also be required for `_resolve_pass_rule` (`verdict_criteria_evaluator.py:786-811`) to do anything other than return `legacy_not_evaluable` — this is a pre-registration artifact, not a `panel_backtester.py` output, but is a precondition for gateability regardless of the adapter above.

### (c) Cost basis — same Kraken basis ratified in Phase 1.3, or different?

**Different bases in the two paths, and neither is uniformly "the Phase 1.3 Kraken basis" for the P4 daily-SMA case specifically:**

- Phase 1.3 ratified the Kraken perp cost basis at **5 bps one-way / 10 bps round-trip** — `strategy-research/config/cost_model.yaml:158-162` (`perp.fee_rate_bps.default: 5.0`, `perp.round_trip_cost_bps.default: 10.0`), sourced per that block's own comment (`cost_model.yaml:135-136`) from "Kraken perpetual-futures taker fee, base tier ... 0.0500% at $0+", and explicitly cross-referenced in `PIPELINE_IMPROVEMENTS_20260712_v4.md:2239-2240`: `"XS_momentum's Kraken venue registration (venue: kraken_perp) and its cost basis (cost_model.yaml perp block, 5 bps one-way)"`.
- `panel_backtester.py`'s **XS-momentum path** (`run_xs`, `_load_perp_cost_bps()`, line 329-334) reads exactly this key — `cm["perp"]["fee_rate_bps"]["default"]` = **5.0 bps**. This path **does** use the Phase-1.3-ratified Kraken basis.
- `panel_backtester.py`'s **gate path** (`validate_gate`, used to reproduce the P4 daily-SMA run_054/run_057 lineage) uses `DEFAULT_COMMISSION_RATE = 0.001` = **10 bps one-way**, a hardcoded module constant (`panel_backtester.py:56`) explicitly commented as mirroring "engine DEFAULT_COMMISSION_RATE" — i.e., the production engine's own default, which per `cost_model.yaml:65-77` (`fee_rate_bps`, "Binance spot, Regular/VIP0 tier, BNB discount applied") is a **Binance spot** figure, not the Kraken perp basis at all, and is double the Phase-1.3 Kraken one-way rate (10 bps vs 5 bps).

**Consequence for gateability specifically on the P4 SMA-trend lineage:** the only part of `panel_backtester.py` that reproduces the P4 daily-SMA mechanism (the gate path) is costed at the Binance-derived 10 bps engine default, not the Phase-1.3 Kraken 5 bps figure — so even setting aside the shape-adapter gap in (b), a P4 re-registration run through this file's gate mechanism would not, unmodified, be costed on the basis the campaign ratified for Kraken instruments in Phase 1.3.

---

## Notes on scope adherence

No code was run to produce any of the above; all figures are read directly from artifacts already on disk (`protocol_result.yaml`, `pre_registration.yaml`, `cost_model.yaml`, `campaign_knowledge_base.yaml`, `campaign_queue.yaml`) and from the source of `panel_backtester.py` / `verdict_criteria_evaluator.py`. No 2026-dated price/performance figures were read or reported (all quoted figures above are either backtest-window results dated 2018–2025, or config/code constants). This file is the only write made during this dispatch.
