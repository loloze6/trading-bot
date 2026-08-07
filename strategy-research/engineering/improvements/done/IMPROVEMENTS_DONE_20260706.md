# Strategy-Research Pipeline — Closing State (Plan v2 Complete)

**Status: enhancement plan complete (M0–M3). All acceptance tests pass (23/23). Calibration outputs on record. P1a (mini-batch + wiring shakedown) CLOSED 2026-07-04 — see §7. P1b (backward-extension reactivation) CLOSED 2026-07-06 — see §8.**  
This document supersedes `00_overview_v2.md` as the entry point. Future sessions start here, then `engineering/improvements/done/design_and_docs/AMENDMENTS_01-06.md` (which overrides the original plan docs `01`–`09` wherever they conflict). Do not reconstruct campaign state from run artifacts or memory — this document plus the amendments file plus `campaign_knowledge_base.yaml` are the canonical record.

Plan docs (01–09, amendments, this file) are archived under version control in `docs/plan/`.

---

## 1. What was built (one line per step, implementation order)

| Step | Delivered |
|---|---|
| 07 | baseline_v2 (24 windows, 2024–2025), frozen 2026-H1 holdout with mechanical overlap guard, burned-range accounting, `config/campaign_data_policy.yaml` |
| 02 | Detector validation tool (persistence, class-conditional sensitivity, activation band), regime-auditor skill, retune firewall (hard-fail) — verdict: ER-family detection **unusable** on BTC/ETH 1h (48-cell grid, Pareto-blocked); campaign is **ungated-only** |
| 03 | Trade-level diagnostics (MAE/MFE, entry/exit efficiency, post-exit tracking, per-trade cost, winner/loser-conditional metrics), A3.4 sparse-Sharpe null-floor + expectancy-primary rule, `keltner_163` fixture (exact-match reproduction) |
| 08+09 | Signal prescreen (active-bar IC, sparsity, block-bootstrap significance, full-range) + two-layer cost hurdle, single `config/cost_model.yaml`, trial recording live from the first gate |
| 01 | Five-category edge-source taxonomy (incl. `persistent_behavioral_bias`), anti-confabulation proxy rule, `config/available_feeds.yaml` constraint, `feed_wishlist.yaml`, structured `mechanism_failure` root causes |
| 05 | `campaign_knowledge_base.yaml` with auto-write hook, derived views (coverage matrix, exhausted mechanisms with A5.1 thresholds enforced in view logic), KB-gated campaign-review and hypothesis-design handoffs |
| 04 (slim) | Seeded `config/indicator_library.yaml` (15 entries), lookup protocol in hypothesis-design, real-diversity check in innovation-expansion; **no** empirical write-back (KB owns results) |
| 06 | Deflated Sharpe (B&LdP) over deduplicated structured trial records, expectancy path for sparse traders, `workflow_artifacts/schemas/promotion_audit.schema.json`, single-use `holdout_evaluation` stage with pre-registered expected ranges |
| A8.x | Methodology layer from live runs: sparse-IC conjunction rule, feed-timing alignment check, dormant-mechanism dispositions, rolling-only percentile thresholds, a-priori power check with correlation-adjusted effective symbols (`n/(1+(n−1)·ρ̄)`) |

---

## 2. Improvement 06 calibration outputs (on record)

All 23/23 acceptance tests pass. Calibration numbers follow.

### Keltner must-NOT-pass — Sharpe path (test fixture, exercises formula branch)
- **Trial distribution** (no dedup needed — no shared forecast_hash in this test): 12 trials; 4 Keltner (sharpe 0.0) + 8 other strategies (range −0.15 to +0.20)
- **Statistic path:** Sharpe path (candidate_sr = 0.0). In real campaign Keltner is sparse (A3.4 below_floor_pct > 50%), so actual path is expectancy; this test exercises the Sharpe-formula branch independently.
- **DSR formula outputs:** trial_mean = 0.025, trial_std = 0.102, expected_max_sharpe = 0.194, z = (0.0 − 0.194) / 0.102 = −1.91, **DSR = 0.028** — fails threshold 0.95. ✓

### Keltner must-NOT-pass — Expectancy path (real keltner_163 fixture)
- **Source:** keltner_163 baseline_v2 run (163 trades, 14/48 zero-trade slots, is_sparse=True).
- **Std estimate:** binary win/loss distribution: winners ≈ +65 bps, losers ≈ −117 bps (2024) / −221 bps (2025); std = |win−loss|×√(p×(1−p)).
- **2024 cohort:** n=69, mean=−26.3 bps, std=91 bps, SE=10.96 bps → **t = −2.401** → passes=False (t << 2.0 threshold). ✓
- **2025 cohort:** n=94, mean=−58.0 bps, std=142 bps, SE=14.60 bps → **t = −3.971** → passes=False. ✓
- **Pooled:** n=163, mean=−44.6 bps, std=123 bps, SE=9.61 bps → **t = −4.637** → passes=False. ✓
- **Promotion_audit.yaml (expectancy path, if SE stored):**
  ```yaml
  is_sparse_trading: true
  passes_deflated_threshold: false
  correction_method: expectancy_t_stat_bonferroni
  expectancy_promotion:
    mean_expectancy_bps: -44.6
    expectancy_se_bps: 9.61
    n_trades: 163
    t_stat: -4.637
    threshold_t: 2.0
    passes: false
    cohort_breakdown:
      "2024": {n: 69, mean_bps: -26.3, t_stat: -2.401}
      "2025": {n: 94, mean_bps: -58.0, t_stat: -3.971}
  ```

### Expectancy-path boundary pair (straddle t = 2.0)
- **Parameters:** n=50 trades, std=200 bps, SE=28.28 bps (boundary mean = 56.57 bps).
- **Fail:** mean=54 bps → t=1.909 < 2.0 → passes=False. ✓
- **Pass:** mean=58 bps → t=2.051 > 2.0 → passes=True. ✓

### Sharpe-path boundary pair (straddle DSR = 0.95)
- **Trial set (n=20):** [0.0, 0.0, 0.0, 0.0, 0.15, −0.10, 0.05, 0.20, −0.05, 0.08, 0.12, −0.15, −0.08, 0.18, 0.03, 0.11, −0.12, 0.07, 0.02, −0.06]
- **Parameters:** mu=0.0225, sigma=0.0989, E_max=0.2104.
- **Fail:** candidate_sr=0.353, z=1.442 → **DSR=0.9253** < 0.95 → passes=False. ✓
- **Pass:** candidate_sr=0.393, z=1.846 → **DSR=0.9676** > 0.95 → passes=True. ✓

### Synthetic must-PASS (extreme, formula check only)
- **Parameters:** candidate_sr = 2.5; 10 injected trials with mean = 0.018, std = 0.061
- **DSR outputs:** expected_max_sharpe = 0.115, z = (2.5 − 0.115) / 0.061 = 38.83, **DSR = 1.0000** — passes threshold 0.95. ✓

### Monotonicity (fixed μ = 0.1, σ = 0.2, candidate_sr = 1.0; holds σ constant to isolate N effect)
N=2 → DSR 0.999966 | N=5 → 0.999529 | N=10 → 0.998280 | N=20 → 0.995329 | N=50 → 0.986916 | N=100 → 0.975546 — strictly decreasing. ✓

### Dedup (runs 017/024/027/033 Keltner quartet)
- Input: 5 records (4 sharing `forecast_hash=keltner_v1_forecast_abc123`, 1 distinct)
- After dedup: 2 survivors (run_017 + run_040), 3 removed. ✓

### Single-use holdout refusal
- H-041-A (in `holdout_consumed_by`): refused. H-042-A (not consumed): allowed. ✓

---

## 3. Campaign epistemic state (honest)

- **Confirmed edges: zero.** The historical "confirmed edge" (Keltner, IC 0.2145) was fully dismantled: unstable regime labels → tiny selected sample → small-sample noise (pooled active-bar IC −0.032, p 0.83) → payoff-shape illusion (57% win rate manufactured by signal-flip exits) → linguistic inflation carried by memory. Every layer has a named countermeasure now in place.
- **H-041-A and H-041-C are CLOSED as of P1b (2026-07-06)** — both reactivations ran to completion on the real backward-extension range with adequate power (see §8). Neither is "parked pending data" any longer; H-041-A is a genuine null (kill), H-041-C is a genuine era-unstable signal (refine, not simply parked).
- **Blocked:** H-041-B volume impulse (mechanism-impure proxy; unblocks with `liquidation_data` feed).
- **Structural findings:** ER regime detection unusable on 1h (detector wishlist holds daily-overlay as priority-1, trigger: an ungated edge showing regime-dependent performance). OHLCV-only generated zero honest hypotheses; the viable space is feed-driven, and current feeds (funding 8h, F&G daily) are power-limited on 2 years × 2 correlated symbols.
- **Runs 001–039 are historical only:** baseline_v1 windows are burnt; regime-conditional conclusions from that era are labeled with their detector version and are inadmissible as exhaustion evidence.
- **KB state (post-P1b, 2026-07-06):** 15 findings (6 exhausted by analytic basis, 1 blocked, 2 invalidated_artifact [run_044, run_047], 2 real P1a results, 2 real P1b results below, 1 H-041-A closed-null, 1 H-041-C era-unstable), 3 meta-findings, exhausted_mechanisms view populated (6 entries).
- **P1a real scientific results (2026-07-04, first live hypotheses run through the full pipeline post-F1-F4 wiring fixes):**
  - `EMA_SPREAD_TREND_CONTINUATION_V1` (run_043): dense EMA(9/21) crossover, BTC/ETH 1h ungated. `ic_all_bars=ic_active_bars=-0.021091`, p=0.5876, n_eff=664. Cost fails (ratio 0.36). `no_edge_observed`, root_cause `already_priced_in` — consistent with every other price-only technical indicator tested in this campaign (RSI, Keltner in all variants).
  - `FUNDING_RATE_CONTINUOUS_MEAN_REVERSION_EXPANDED` (run_044): continuous (threshold=0.0, not extreme-only) 8h funding-rate-sign mean-reversion, BTC/ETH 1h ungated — a materially different, better-powered claim than parked H-041-A. `ic_all_bars=-0.008706`, `ic_active_bars=0.016737`, p=0.881, n_eff=83 (power-adequate, unlike H-041-A's n_eff=10). Cost fails (ratio 0.24). `inconclusive`, root_cause `lag_mismatch_to_regime_persistence`, escalated to timeframe (not killed) — mechanism may still work at 4h/daily.
  - Both ran against `protocols/baseline_v1.json`, not the canonical `baseline_v2.json` — a live wiring gap in the orchestrator's default protocol-selection fallback, found during P1a, not fixed (out of scope for F1-F8). **Partially addressed in P1b** (§8): F4d's conformance gate now catches this specific failure mode for any run carrying a `machine_constraints` block, though the underlying default-fallback behavior for unconstrained runs is unchanged.
- **P1b real scientific results (2026-07-06, backward-extension reactivation, full detail in §8):**
  - H-041-A (run_050, corrected — see §8 for run_047's invalidated first attempt): `ic_active_bars=0.017764`, p=0.521, n_episodes=139 (2019-09→2025-12, 7 years). Not significant. `kill_no_ic` — a genuine, well-powered null; family closed, pivoted away.
  - H-041-C (run_048): `ic_active_bars=-0.040257`, p=0.081 (significant, wrong sign), n_episodes=234 (2018-02→2025-12). Per-era breakdown (A8.5.1a) shows the sign ITSELF flips between eras — negative in 2018-2023 (BTC -0.058 to -0.073, ETH -0.071 to -0.135), positive in 2024-2025 (BTC +0.101 to +0.182, ETH +0.094 to +0.163). `refine_inverted_ic` routed a "flip polarity" proposal (`run_052`, scaffolded not launched) — but a naive polarity flip does not address the underlying era-instability; era-transferability here is a user-level call, not an automatic fix.
- **trial_sharpes in campaign_state:** 8 records — run_041 (H-041-A) and run_042 (H-041-C) backfilled manually (pre-A6.2 runs); run_043 (EMA spread, live-recorded, first-ever live fire of `_record_prescreen_trial(source="prescreen")`); run_044 (invalidated_artifact — bug-artifact `kill_no_ic`, F5a); run_044_post_f5 (the real result, recorded under a distinct trial_id since the id-reuse guard correctly-but-inconveniently blocks reusing "run_044"); run_047 (invalidated_artifact — wrong protocol range + dropped significance_methodology, F4d); run_050 (H-041-A corrected result); run_048 (H-041-C result).

---

## 4. Standing rules (survive the plan; violations are stop-the-line)

1. **Holdout (2026-H1) is untouchable** except by `holdout_evaluation`, once per hypothesis, pre-registered expected range, failure terminal.
2. **Everything that touches data is a trial** — prescreen kills, recalibrations, refinements — recorded as structured records (`statistic_valid`), deduplicated by forecast-series hash.
3. **Vocabulary is mechanical:** outcome enums only; "confirmed" is unwritable without a passing `promotion_audit`; positive IC is a signal property, never an edge outcome.
4. **Detector retunes never see PnL** (hard-fail firewall); any new detector passes the full 02 gate before its labels condition anything.
5. **Non-OHLCV feeds require a documented alignment check before prescreen**; a strong feed-signal IC triggers alignment re-verification, not celebration.
6. **Prescreen is a filter, not a fitness function** — no variant ranking by IC; percentile thresholds are rolling/past-only.
7. **Power is checked a priori** (deterministic, pre-component-build); market-wide signals use `n/(1+(n−1)·ρ̄)` effective symbols.
8. **Sparse signals:** window-Sharpe below the trade floor is null, expectancy ± SE is primary; `signal_bad_everywhere` needs the all-bars AND active-bar IC conjunction.
9. **Prompt/skill changes are accepted by output audit** (A1.4), never diff review; new metrics are accepted against known-answer fixtures (`keltner_163` is the standing one).
10. **Fee/spread constants live in `config/cost_model.yaml` only**; `config/campaign_config.yaml` values are drift-guarded by test against code constants.

---

## 5. Open items

| Item | Status / trigger |
|---|---|
| 04 generation audit | **Partially closed (P1a, 2026-07-04).** `library_lookup` fired correctly on all 4 hypothesis-generation attempts (run_043 ×2, run_044 ×2); prior-campaign-failure citations and crowding-deviation justifications were substantive, not boilerplate. **`diversity_audit` still NOT genuinely exercised** — both hypotheses' research briefs constrained to "one variant only" (P1a's own scoping choice, to bound cost), so `innovation_expansion` self-reported diversity as a *hypothetical* pass ("V1+V2+V3 would span 2 categories") every time, never against an actually-executed multi-variant set. Closing 04's audit for real requires a future brief that does NOT constrain to one variant, so the real-diversity-vs-cosmetic check runs against genuine candidates. |
| Backward-extension pass | **Launched as P1b, 2026-07-04** — see §8. |
| Feed wishlist | `liquidation_data` (argued case: unblocks mechanism-pure volume hypotheses) |
| Detector wishlist | Daily-overlay priority 1; trigger: ungated edge with regime-dependent 03 diagnostics |
| Config runtime wiring | Code still reads own constants; drift-guard test in place; "new campaign = config-only" bar NOT met until refactor |
| Trading-bot backlog | Engine-recorded exit reasons in PerformanceTracker (replace post-hoc inference, currently 95% inferred) |
| Trading-bot backlog | Post-only maker execution path + fill-rate calibration — **parked**: no fee benefit at VIP0 (maker=taker fee); revisit only at VIP1+ or with `order_book` feed. See `engineering/improvements/done/design_and_docs/10_maker_execution_assessment.md` |
| Trading-bot backlog (F7, 2026-07-04) | **Engine defect, not fixed this pass — reproduction test already committed.** `main_strategy.is_ready()` gates on `strategy_engine.is_ready(self.regime_engine.current_regime)`, read BEFORE `classify()` has run for the current bar — so on the very first ready-candidate bar, `current_regime` is still the class-init default `MarketRegime.UNKNOWN`. `ConfigDrivenStrategyEngine.is_ready()` returns `True` unconditionally when that stale key isn't registered in its `_components` dict — true whenever the real signal sits under any `strategies.regimes` key other than `"unknown"`. Net effect: the very first forecast is computed one bar early, from as few as ~4 bars of history, silently ignoring the configured `warmup`. Affects EVERY strategy config (gated or ungated) on its first-ever ready bar, not just the F1 ungated pattern — invisible in aggregate metrics because it touches exactly one bar out of thousands, but confirmed present in run_042's own shipped config via direct instrumentation (F1, 2026-07-04). Reproduction: `trading-bot/tests/test_ungated_config_pattern.py::test_pattern_a_unknown_is_the_unique_warmup_safe_choice` and `::test_run_042_precedent_shares_the_stale_regime_readiness_mechanism` (both committed, both passing against current behavior — they document the defect, they do not fix it). Fix requires moving the `current_regime` read to after `classify()` runs, or an explicit "first bar" guard in `is_ready()`; out of scope for a config-pattern/orchestrator fix, needs its own review given it touches core engine readiness semantics used by every live and backtest strategy. |
| Viable-space map | `engineering/improvements/done/design_and_docs/11_viable_space_map.md` (2026-07-04, **rev. 3, frozen — advisory only, never blocks registration/A8.6/prescreen**). Layer-1 cost-hurdle projection over indicator_library × {1h,4h,1d}, taker-only. OHLCV oscillator/volatility/volume-flow/structural-rate cells: implausible or not_meaningful (sub-1-bar hold) at every timeframe. `fear_greed_index_contrarian`: cost-plausible, matching run_042's actual Layer-2 result (ratio 3.75) — still parked on power grounds (H-041-C unchanged). `moving_average_crossover`/`keltner_channel_trend`/`macd`: `model_blind` (linear-IC model can't price convex trend-following payoffs) — not scored either way. De-prioritizes OHLCV retests at coarser timeframes for P4 |

---

## 6. Pending decision — RESOLVED 2026-07-04

**New hypothesis batch first vs backward-extension first.** Resolved: batch first (P1a), extension second (P1b, launched immediately after P1a's closure — see §7). Outcome matches the recorded expectation: the batch returned two real null/inconclusive results (§3) rather than an edge, so the extension is the natural successor.

---

## 7. P1a closure (2026-07-04)

**Status: CLOSED.** Scope: 2-hypothesis mini-batch run through the full live pipeline (not hand-executed), surfacing and fixing 8 distinct wiring defects (F1–F8) plus 2 soft patches, along the way. Both hypotheses reached real, credible verdicts (§3). Full run transcripts, artifacts, and recovery notes live under `runs/run_043/` and `runs/run_044/` (including `attempt_1_blocked/`, `attempt_2_invalidated_by_f5_bug/` subfolders preserving each blocked/invalidated attempt for audit).

### Defect ledger (F1–F8), one line each

| # | Defect | Root cause |
|---|---|---|
| F1 | Ungated config pattern unsafe for 3 of 4 regime names | `main_strategy.is_ready()` reads `regime_engine.current_regime` before `classify()` runs on the first ready bar; only `default_regime="unknown"` avoids computing a forecast from under-warmed history. `validate_config.py` V9 also only ever checked `default_regime=="trending"`, unconditionally — both gaps fixed; engine defect itself filed as F7, not fixed. |
| F2 | `STRATEGY_CONFIG_REFERENCE.md`/`WORKFLOW_CAPABILITIES.md` never updated for two existing components | `FundingRateMeanReversionComponent`/`FearGreedContrarianComponent` (Improvement 01) shipped without doc updates, causing a false `component_gap` verdict (run_044 attempt 1) on an already-working component. |
| F3 | `_should_trigger_campaign_review` crashed | `campaign_state.failed_families` is a mixed list of dicts (post-Improvement-07) and strings (`record_pivot()`); `set(failed)` on dict entries raises `TypeError`. First live run to reach this code path since the Improvement 07 schema migration. |
| F4 | `ensure_files()` had no YAML auto-repair | Unlike `load_yaml()`, which retries via `_repair_yaml()`, `ensure_files()` did a bare `yaml.safe_load()` — the exact unquoted-colon failure every skill file warns about crashed the pipeline when it landed in a stage's own deliverable rather than a handoff/state file. |
| F5a | `FundingRateMeanReversionComponent` divide-by-zero at `threshold=0.0` | Confidence calc `abs(funding_rate) / (self.threshold * 3.0)` divides by zero for the legitimate continuous-mode design (threshold=0 fires at every settlement, not just extremes). |
| F5b | Component exceptions silently swallowed, uncounted | `main_strategy.update()`'s broad `except` logged and continued with no count/classification — the exact mechanism that let F5a masquerade as a real "no signal" result for one full run. |
| F5c | No distinction between "tested, found nothing" and "never actually tested" | New `no_signal_artifact` prescreen route (`active_n_bars==0` or component-error-rate above threshold) intercepted before `verdict_interpreter`, routed straight to an engineering pause — never a `kill_no_ic`. |
| F6 | Circuit-breaker state was global, not per-family | `recent_parameter_dimensions` (flat list) let stale, unrelated-family history force a brand-new family's first-ever refine straight to pivot (run_044, using leftover Keltner/RSI-era dimensions). Scoped per-family; also fixed the same dict/string mismatch as F3 in the escalate-to-pivot counter; added `component_execution_error` as a breaker-immune mechanism_failure value. |
| F7 | `main_strategy.is_ready()` one-bar warmup-bypass defect | Filed, not fixed (see F1). Systemic — affects every strategy config, gated or ungated, on its first-ever ready bar; invisible in aggregate metrics. Reproduction tests committed in `trading-bot/tests/test_ungated_config_pattern.py`. |
| F8 | `_next_run_id()` collided on run allocation | Naive "current + 1" with no uniqueness check, no overwrite guard. Collided TWICE in one session (run_043's reframe → "run_044", already in use by an independent sibling run; the recovery's own reframe → "run_045", by then also in use). Fixed at allocation (scans `runs/` + `campaign_state.runs` for the true max) plus two independent overwrite-refusal backstops (`setup_run.py`, `_safe_write_new_research_brief`). |

Two soft patches (not defects, quality-of-signal improvements): (a) `plausible_ic_upper` anchor table in `hypothesis-design/SKILL.md`, keyed by signal class, closing an observed 3× free-form variance; (b) A8.6 pre-flight logs LLM-vs-machine power-computation discrepancies to `power_check_discrepancy_log.yaml` (fired live during the real P1a run, not just its test fixture).

### What P1a did NOT close
- **04's `diversity_audit`** — see Open Items table above. Needs a future multi-variant brief.
- **`main_strategy.is_ready()`'s one-bar defect (F7)** — filed, not fixed.
- **Orchestrator default protocol-selection fallback** (defaults to `baseline_v1.json`, not the canonical `baseline_v2.json`, when `campaign_state.last_escalation` is unset) — found during P1a, out of scope for F1–F8, not fixed.
- **Two parked, near-duplicate "daily regime overlay" briefs** (`runs/run_045/`, `runs/run_046/`) — both recommended by `campaign_review` without checking `detector_wishlist.yaml`'s own `trigger_condition` (status: `not_triggered` — no confirmed ungated edge exists yet). Annotated `status: parked_pending_a23_trigger`; `campaign-review/SKILL.md` patched with a "Wishlist-gated recommendations" rule to prevent recurrence; KB meta-finding `daily_regime_overlay_recommended_before_a23_trigger` records the pattern.

---

## 8. P1b closure (2026-07-06)

**Status: CLOSED.** Scope: backward-extension data backfill (2018/2019→2025) + episode-blocked significance methodology (A8.5.1a, brand new) + two re-prescreens of the parked H-041-A/H-041-C reactivations, launched through the orchestrator (not hand-executed), per the standing rule established in this campaign's P1a work. Surfaced and fixed 5 more distinct orchestrator defects (F4a–F4e) along the way, one of them (F4d) discovered only after an initial run (run_047) completed end-to-end on the wrong data and had to be invalidated and redone. Full artifacts under `runs/run_047/` (invalidated), `runs/run_050/` (H-041-A corrected), `runs/run_048/` (H-041-C).

### Data backfill

Verified via real fetcher calls (no assumptions): BTCUSDT/ETHUSDT 1h OHLCV back to 2018-01-01 (spot market, 74,457 rows each); funding rate back to each symbol's real Binance perpetual-futures inception (BTC 2019-09-10, ETH 2019-11-27; 7,467/7,234 rows); Fear & Greed back to 2018-02-01 (alternative.me history start; 3,073 rows). Gap report and event cross-checks (COVID-crash funding backwardation, 2018 F&G extreme-fear cluster) in `engineering/improvements/done/design_and_docs/p1b_fetch_manifest.md`. `campaign_data_policy.yaml` extended with a `backward_extension` block (`walk_forward_eligible`, holdout untouched) and a 5-era `eras` list for stratified reporting.

### A8.5.1a — episode-blocked significance (new methodology)

Full spec in `engineering/improvements/done/design_and_docs/AMENDMENTS_01-06.md` ("A8.5.1a-spec"); implementation in `strategy-research/tools/episode_significance.py`. Episodes = runs of active bars separated by ≤48 1h-bars (era boundaries are hard cuts); bootstrap resamples whole episodes, not fixed blocks; `n_episodes≥8` floor for any significance claim; density≥50% falls back to the existing 24-bar method; era stratification is reporting only, not resampling. Three required fixtures (recovered-CI-covers-truth, naive-block-overconfident-vs-episode, below-floor-suppressed) in `tests/test_a851a_episode_bootstrap.py`. Wired into `prescreen_signal.py` as an **opt-in** flag (`significance_methodology: episode_blocked_a851a` in the config) — default behavior for every prior run is unchanged and still reproducible under the old method.

### Defect ledger (F4a–F4e), one line each

| # | Defect | Root cause |
|---|---|---|
| F4a | `_repair_yaml` gave up on a colon in a wrapped multi-line list item | `_quote_yaml_line` only recognized a colon on the SAME physical line as a `- ` marker or `key:` mapping; a continuation line (no marker of its own) couldn't be identified or quoted. Added `_repair_multiline_list_item` (walks back to the marker, folds all continuation lines, quotes the merged value). Fixture: run_047's real hypothesis_card.yaml output. |
| F4b | No recovery path when an LLM stage's output is unrepairable | One bounded retry (`_invoke_agent_with_yaml_retry`): re-invoke the SAME stage once with the parse error + offending lines appended to the prompt; second failure still fails to human, unchanged. Logged to `pipeline_state.yaml`'s new `yaml_retry_count`. |
| F4c | Token circuit breaker summed raw tokens, not cost | `claude_agent_sdk`'s `ResultMessage.usage` is cumulative FOR THE SESSION (across internal turns), not a single-call snapshot — a validation call with 836,461 heavily-discounted `cache_read` tokens tripped the old 300k raw-token budget despite a real dollar cost of $0.35. Switched to cost-weighted units (`_weighted_token_units`: input×1.0, output×5.0, cache_read×0.1, cache_creation×1.25); budget now actually read from `campaign_config.yaml` at runtime (the one constant in this file with real runtime loading, by design — see that file's comment). |
| F4d | Pre-registered constraints (data range, significance methodology) were prose-only, mechanically unenforced | run_047 silently used `baseline_v1.json` (2024-only) instead of the pre-registered backward-extension range, AND silently dropped the MANDATORY `significance_methodology`, yet completed end-to-end and wrote a KB finding. Added `machine_constraints` to `pre_registration.yaml` — the orchestrator now generates the protocol file + `run_context.yaml` override directly from it, force-injects `significance_methodology` into the candidate config regardless of LLM memory, and gates entry to `verdict_interpreter` on a conformance check (mismatch → `paused_for_human`, no KB write, trial marked `invalidated_artifact` — same principle as F5c). Regression fixture: run_047's real, frozen mismatch. A follow-on bug in my OWN first implementation (missing `run_type: forced_diagnostic` in the generated `run_context.yaml`, silently falling back to a STALE campaign-wide `last_escalation.protocol_path` from a prior unrelated run) was caught live on run_050's first conformance-clean attempt and fixed the same session. |
| F4e | `episode_significance.per_era_report()`'s dict keys crashed on YAML read-back | `prescreen_signal.py`'s real wiring uses a `(symbol, era_id)` tuple as `era_of()`'s return value (needed to keep episodes symbol-bounded when pooled) — this round-trips fine through `yaml.safe_dump` but crashes `yaml.safe_load` ("found unhashable key"), because a YAML complex-mapping-key sequence deserializes as a Python list, not a tuple. Caught live on run_050's second attempt (wrote successfully, crashed the very next read). Fixed by stringifying tuple keys (`"SYMBOL::era_id"`) at the output boundary only. |

None of F4a–F4e were caught by my own unit tests before their live occurrence — every one was found by an actual orchestrator run hitting real data/LLM output shapes my fixtures hadn't reproduced. Each has a regression test now, built from the real failure.

### run_047 invalidation record

`run_047` (H-041-A's first reactivation attempt) completed end-to-end — prescreen, verdict, campaign_review — before F4d existed to catch it. Root cause: both defects above (wrong protocol, dropped methodology). Remediation: `campaign_knowledge_base.yaml`'s `funding_rate_mean_reversion_inconclusive` entry reverted to run_041-only evidence (`evidence_count` 2→1); a new sibling finding `funding_rate_mean_reversion_run047_invalidated` (`outcome: invalidated_artifact`) preserves the record; `campaign_state.yaml`'s run_047 trial marked `invalidated_artifact: true`; `run_047/artifacts/campaign_review.yaml` annotated with a postscript (its own "continue" recommendation and suspicion that something was wrong were correct and are unchanged in substance).

### Final results

- **H-041-A** (run_050, corrected): `ic_active_bars=0.017764`, `p=0.521`, `n_episodes=139` over 2019-09→2025-12 (7 years, both symbols pooled). Direction matches run_041's original (+0.014) but still not significant even at ~14× the original episode count. `kill_no_ic` — a real, well-powered null. `verdict_interpreter`'s prose narrative incorrectly states "4h timeframe" (the run was actually 1h) — a hallucinated detail that does not affect the real computed numbers; flagged, not corrected in the artifact.
- **H-041-C** (run_048): `ic_active_bars=-0.040257`, `p=0.081` (significant), `n_episodes=234` over 2018-02→2025-12. **The A8.5.1a per-era breakdown is the actual finding here**: the sign flips cleanly between eras — negative throughout 2018-2023 (BTC -0.058 to -0.073, ETH -0.071 to -0.135) and positive throughout 2024-2025 (BTC +0.101 to +0.182, ETH +0.094 to +0.163), consistently across both symbols and all 8 era-symbol pairs. `refine_inverted_ic` proposed a polarity flip (`run_052`, scaffolded, **not launched**) — but flipping the sign fixes only the pooled result; it does not resolve the underlying era-instability (a flipped signal would now fail 2018-2023 instead of 2024-2025). This is exactly the era-transferability concern flagged in the original P1b prompt ("2018–2021 market structure ≠ 2026... a user-level review, not an automatic route") — surfaced here even though the hypothesis never "passed both gates" in the naive sense.
- **Neither hypothesis passed both gates** (IC-significance AND cost), so no walk-forward was ever triggered — the P1b prompt's "STOP before any walk-forward" condition is satisfied trivially, not because it was invoked.

### What P1b did NOT close
- **`run_052`** (H-041-C flip-polarity proposal) — scaffolded, not launched; the era-instability finding above means launching it as-is would repeat the same naive-fix mistake. Needs a user decision on how (or whether) to pursue era-conditional variants.
- **`run_049`** (H-041-A's original 15m timeframe escalation from run_047, now itself downstream of an invalidated run) — scaffolded, not launched; likely stale given run_047's invalidation, not reviewed.
- **The general orchestrator default-protocol-fallback behavior** for runs WITHOUT a `machine_constraints` block — F4d only closes the gap for constrained runs; an ordinary run with no override still silently falls back to `campaign_state.last_escalation` or `baseline_v1.json`.
- **`verdict_interpreter`'s hallucinated timeframe detail** on run_050 — noted, not corrected in the artifact (the real computed numbers are unaffected).

---

## 9. Orientation for future sessions

Read order: this file → `engineering/improvements/done/design_and_docs/AMENDMENTS_01-06.md` → the specific plan doc for whatever is being touched → `campaign_knowledge_base.yaml` for empirical state. The amendments override the plan docs. The knowledge base, not `findings_carryover.yaml`, is the cross-run memory. Acceptance culture: known-answer fixtures for metrics, output audits for prompts, pre-registered expectations for runs, and outputs (numbers, channels, cards) reported — never bare pass marks.
