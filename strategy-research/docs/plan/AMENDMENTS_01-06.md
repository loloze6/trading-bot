# Amendments to Improvement Plans 01–06

Targeted edits an implementation agent must apply when implementing the corresponding plan. Each amendment states the defect in the original and the exact change. Amendments marked *(added/extended post-M0)* derive from the Improvement 07 Keltner reconciliation (run_033 "confirmed edge" traced to an IC of 0.2145 with negative per-trade expectancy; median-Sharpe pinning on sparse traders; bit-identical metrics across four runs) — the empirical motivation is stated inline where it matters. This file also amends `08`/`09` despite the filename. Where an amendment conflicts with the original plan text, the amendment wins.

---

## 01 — Edge-Source Taxonomy

### A1.1 — Add a fifth `edge_source.category`: `persistent_behavioral_bias`

**Defect:** The four categories (information_asymmetry, structural_forced_flow, liquidity_provision, cross_venue_dislocation) exclude the mechanism behind most OHLCV-testable strategies — including the campaign's only confirmed edge (Keltner mean-reversion), which is behavioral overreaction, not forced flow or asymmetric information. With no honest category available, the schema will force the LLM to confabulate a structural mechanism, laundering noise as causality — the exact failure mode this plan exists to prevent.

**Change:** add to the enum:
- **persistent_behavioral_bias** — systematic over/under-reaction, herding, anchoring, or disposition effects that recur because they arise from human/algorithmic behavior rather than exploitable-once information. `why_not_arbitraged` bar for this category: must argue why the bias persists at this timeframe/venue despite being publicly known (e.g., capacity limits, risk limits of arbitrageurs, crowding cycles) — skepticism required, but the category must exist so it can be claimed honestly.

### A1.2 — Constrain `evidence_type` to backtestable feeds

**Defect:** 01 deliberately pushes toward `order_book`, `liquidation_data`, `cross_exchange` evidence types. The trading-bot's FEED_REGISTRY currently supports OHLCV, funding rate, and Fear & Greed. Pushing generation toward untestable evidence types converts the generative improvement into a stream of `component_gap` human-pauses.

**Change:** add `config/available_feeds.yaml` (auto-derivable from FEED_REGISTRY). `hypothesis-design` hard rule: `evidence_type` must be in available feeds, OR the hypothesis is explicitly tagged `requires_new_feed: <name>` and routed to a backlog artifact (`feed_wishlist.yaml`) instead of the run queue — the human sees an aggregated, prioritized case for building a feed, rather than the pipeline stalling per-run. The innovation-expansion rule "≥1 non-price_volume_only variant" is satisfiable today via `funding_open_interest` (funding feed exists) — note this explicitly in the skill so the model doesn't reach for order-book data it cannot test.

### A1.3 — Anti-confabulation check on `specific_mechanism`

**Change:** `specific_mechanism` must name at least one **measurable proxy in an available feed** that would look different if the mechanism were real vs. absent (this becomes an input to `validation_protocol.falsifiable_statement`). If no proxy exists, category must fall back to `persistent_behavioral_bias` or the hypothesis is rejected — a mechanism that cannot leave a trace in available data is a story, not a hypothesis.

### A1.4 — Acceptance protocol for prompt-level changes *(added at 01 review; applies equally to 04, 05)*

Skill/prompt rewrites have no behavior until an LLM executes them; they are accepted by **output audit**, never by diff review. For 01: (a) schema negative tests (missing `edge_source`, out-of-enum category, unavailable `evidence_type` without `requires_new_feed` — all must fail validation); (b) a **generation trial** — run hypothesis-design and innovation-expansion on a real research brief and audit every card: category honesty, proxy computability from available feeds, no regime-gated leakage (A2.3), wishlist entries specific enough to justify a feed build; (c) the first audit-passing card proceeds live through the full gate stack as the end-to-end pass-path test (transferred from A8.2). Expect and fix at least one compliant-looking confabulation in the first trial — schema-constrained generation fails by satisfying the letter while violating the spirit; captured examples go back into the skill. Additionally: verdict-interpreter's venue-level escalation actions (different venue, lower-fee instrument) must route to a wishlist-style note, not an executable prescription, until multi-venue options exist. *(Status: 01 accepted via full protocol. 04 accepted at the deterministic layer only — validator tests passed; the generation audit is deferred to the first live hypothesis batch, whose `library_lookup`, affinity-deviation justifications, and `diversity_audit` outputs must be audited against this protocol before 04 is fully accepted.)*

---

## 02 — Regime Attribution

### A2.1 — Detector-confidence deadlock escape

**Defect:** Rule 1 blocks any hypothesis-level kill/pivot while `detector_confidence != high`. If the detector never reaches high confidence for a symbol/timeframe (plausible — crypto 1h regime detection is genuinely hard), every regime-gated hypothesis accumulates as `inconclusive` forever and the campaign stalls.

**Change:** `signal_bad_everywhere` may be concluded regardless of detector confidence when the **ungated** evidence supports it — pooled IC ≈ 0 with tight CI from `prescreen_result.yaml` (Improvement 08) or ungated backtest metrics. Rationale: a signal with no edge over all bars has no edge under any partition of those bars; only regime-*conditional* conclusions require a trusted detector. Additionally: if `regime_audit_decision.status != trustworthy` persists after one retune cycle, the orchestrator switches hypothesis generation for that symbol/timeframe to ungated-only (recorded in campaign_knowledge_base) rather than pausing indefinitely.

### A2.2 — Class-conditional sensitivity, activation-rate band, and the retune firewall *(added after the first detector report)*

**Defect (empirically demonstrated):** the first report showed `parameter_sensitivity = 0.016` (reassuring) alongside a TRENDING activation rate of 1.1–1.6% (alarming). Sensitivity denominated over *all* bars is misleading for rare labels: 1.6% of all bars flipping is consistent with the TRENDING set itself turning over by >100% under ±10% perturbation. A gate labeling ~1% of bars TRENDING also makes any TRENDING-gated strategy dark by construction — the observed ~29% zero-trade months need no market-structure explanation.

**Changes to `tools/validate_regime_detector.py` and the report schema:**
- Add `class_conditional_sensitivity` per regime label: of bars carrying label L at baseline, the fraction that lose L under perturbation, plus the relative change in the label's population size. The `confidence` rule must use the class-conditional figure for any label with activation < 10%; the all-bars figure is retained but may not upgrade confidence.
- Add `activation_rate` per label as a first-class metric with a configurable plausibility band (default for a trend label on 1h crypto: 10–40% of bars). Activation outside the band caps confidence at `medium` and must appear in the regime-auditor's `recommended_action`.

**Retune firewall (hard rule, embed in `regime-auditor` skill and orchestrator):** detector parameters are tuned **only** against detector-intrinsic criteria — persistence, class-conditional stability, activation within band, agreement with reference labels if any. Strategy PnL, Sharpe, IC, or any backtest output may never appear in retune acceptance. A detector tuned against strategy performance becomes a fitted strategy parameter: every regime-gated result thereafter is a hidden trial and the Improvement 06 accounting is unrecoverable. If a retune cycle cannot reach `trustworthy` on intrinsic criteria alone, the correct outcome is A2.1's ungated-only fallback, not a softer criterion.

### A2.3 — Post-`unusable` policy *(added after the retune verdict)*

The one permitted retune cycle (48-cell grid, hysteresis + dwell) established analytically that stateless ER-family detection on BTC/ETH 1h is Pareto-blocked: activation within [10%, 40%] and transitions/window ≤ 4 cannot be satisfied simultaneously (best achievable ~18 transitions/window at dwell=24). Verdict: `unusable_for_this_symbol_timeframe`. Standing policy from this point:

1. **No replacement detector (ADX, HMM, or other) is built until an ungated edge exists** whose Improvement 03 diagnostics show regime-dependent performance. Regime gating is an optimization over a working edge; with zero confirmed edges, a new detector is added trial surface with no payoff. Record candidate detector families in a `detector_wishlist` entry (mirroring A1.2's feed_wishlist), not as work items.
2. When that trigger fires, the **preferred first candidate is a daily-timeframe regime overlay** on 1h strategies — persistence measured in days clears the intrinsic gates by construction, and it is a config change, not an engine extension.
3. Any future detector, whatever the family, must pass the full 02 gate (`validate_regime_detector.py` incl. class-conditional sensitivity, then regime-auditor) before its labels may condition any metric. The 02 machinery is detector-agnostic and permanent.
4. `prescreen_result.ic_by_regime` (Improvement 08) is suspended — ungated IC only — until a `trustworthy` detector exists.
5. The ungated-escape criterion in A2.1 requires IC computed over **all bars**; an IC computed on detector-gated bars (e.g., run_033's `forecast_return_corr` on ~1% TRENDING-labeled bars) is not admissible for or against the escape. Verify measurement scope before applying the rule.

---

## 03 — Trade-Level Diagnostics

### A3.1 — Add post-exit tracking (required by the plan's own decision table)

**Defect:** the `holding_sizing` row triggers on "stop_loss exits on trades that **would have recovered**" — a counterfactual requiring price data after the exit, which the per-trade schema does not capture. As written, the rule can never fire.

**Change:** add per-trade fields `post_exit_return_5bars: float`, `post_exit_return_20bars: float` (signed in the direction of the closed position), and summary field `stop_loss_recovery_rate: float` (fraction of stop_loss exits where post_exit_return_20bars > 0). The `holding_sizing` rule triggers on `stop_loss_recovery_rate` above a threshold.

### A3.2 — Per-trade cost field

**Change:** add `cost_paid: float` (bps) per trade, sourced from `config/cost_model.yaml` (Improvement 09). Enables trade-level decomposition of `cost_drag` (many small costly trades vs few expensive reversals) and closes the loop with 09's estimate-vs-realized recalibration.

### A3.3 — Note on `exit_efficiency`

`exit_efficiency` benchmarks against the best possible exit in the window — an unattainable hindsight optimum. Valid for *relative* comparison across variants and for trend detection within a family; must not be interpreted as achievable headroom. Add one sentence to the verdict-interpreter skill to that effect (cheap guard against the LLM prescribing "capture the remaining X%" refinements).

### A3.4 — Trade-count floor: window-Sharpe is invalid for sparse traders *(added post-M0, from the Keltner reconciliation)*

**Defect (empirically demonstrated):** for regime-gated strategies producing 1–3 trades per window, per-window Sharpe is statistically undefined-in-practice and `median_sharpe` pins to 0.000 regardless of whether the strategy is profitable (observed: Keltner v1 and v2 both median 0.000 while per-trade expectancy was −26 and −58 bps respectively). Any diagnostic rule thresholding on `median_sharpe` returns noise for exactly the selective, regime-gated strategy class the campaign most often generates.

**Change:**
- `protocol_result.yaml`: per-window Sharpe is reported as `null` (not 0.0) when the window's closed-trade count is below a floor (default: 5 trades); add summary fields `per_trade_expectancy_bps: {mean, se, t_stat, n}` computed over all closed trades pooled.
- `verdict-interpreter`: when the fraction of below-floor windows exceeds 50%, `median_sharpe`-based rules are suspended and **per-trade expectancy (mean ± SE)** becomes the primary performance statistic for the verdict; the verdict must state which statistic it was decided on.
- The zero-trade-slot rate itself becomes a first-class reported metric (`zero_trade_slot_pct`) — a strategy dark in ~30% of calendar slots has a deployment problem independent of its expectancy.

### A3.5 — Named regression fixture: `keltner_163` *(added post-M0)*

The 163-trade Keltner ledger from the baseline_v2 re-run (run per Improvement 07 acceptance criterion 4) is preserved as a permanent regression fixture. Improvement 03's diagnostics, run on this ledger, must reproduce its known signature: win rate rising 51%→57% from 2024 to 2025 cohorts while per-trade expectancy worsens −26→−58 bps — i.e., the MAE/MFE decomposition, `exit_reason_breakdown`, and `pnl_concentration` outputs must together attribute the loss asymmetry (larger losers relative to winners in 2025) to a specific channel. ### A3.6 — Winner/loser-conditional metrics are standard summary fields *(added at Step 3 acceptance)*

**Defect (empirically demonstrated by the fixture):** aggregate `exit_efficiency_median` = 0.39 looked healthy while loser-conditional exit efficiency was −0.90/−1.46 per cohort — aggregate medians are dominated by the winning majority and can fully mask the failure channel. **Change:** `trade_diagnostics_summary` reports, as standard required fields, winner-conditional and loser-conditional versions of: avg return, median MAE, median MFE, exit_efficiency_median, and median holding_bars; plus `pct_pnl_from_worst_decile_trades` (loss-side mirror of the existing top-decile concentration). The verdict-interpreter's `none_healthy` conclusion requires the conditional metrics, not aggregates alone.

---

## 05 — Campaign Knowledge Base

### A5.1 — Minimum-evidence thresholds

**Defect:** with ~36 runs, most mechanism × regime × symbol × timeframe cells hold 0–2 observations. Nothing prevents an n=1 cell from hard-constraining generation — the KB becomes an overfitting amplifier that institutionalizes flukes.

**Change:**
- Add `evidence_count: int` (number of *independent* supporting runs — variants within one run count once) to each `findings` entry.
- `exhausted_mechanisms` entry requires `evidence_count >= 3` with consistent outcome, OR `evidence_count >= 1` where the failure is *analytic* rather than empirical (e.g., cost-hurdle arithmetic from Improvement 09 — math doesn't need replication).
- `hypothesis-design` treats findings with `evidence_count < 3` as **priors/hints** (may be contradicted with justification), and only `exhausted_mechanisms` entries as hard constraints.

### A5.2 — Rename outcome `confirmed_no_edge` → `no_edge_observed`, and ban unearned edge claims *(extended post-M0)*

One failed implementation does not confirm the absence of an edge; it observes one. The enum name will be read literally by LLM stages downstream — precision in the label is cheap insurance against overgeneralized carryover.

**Extension — vocabulary hard rule (empirically motivated):** during the campaign, a run_033 `refine` verdict with `forecast_return_corr = 0.2145` and median Sharpe 0.000 was stored and repeated across runs as a "confirmed edge" — a promising correlation was linguistically upgraded to a validated result and propagated for months through carryover memory. No code was wrong; the words were. Therefore:

- All edge claims in `campaign_knowledge_base.yaml`, `findings_carryover.yaml`, and campaign summaries must use **outcome enums only**; free-text fields (`notes`) may describe evidence but may not assert edge status.
- No artifact may record an outcome stronger than `edge_but_*` / `inconclusive` for a hypothesis_id that has no passing `promotion_audit.yaml` (Improvement 06). The word "confirmed" is reserved for post-holdout, post-deflation results and is mechanically unwritable before then (schema-level: `confirmed_edge_found` is only valid alongside a `promotion_audit_ref`).
- A positive `forecast_return_corr` alone must never be recorded as an edge outcome — correlation that does not monetize per trade is a *signal property*, stored as such (see A6.2 extension and Improvement 09: Keltner's IC of 0.21 coexisted with −26 bps/trade expectancy).

### A5.3 — Tag findings with `protocol_version` and `detector_version` *(extended post-A2.2)*

Required by Improvement 07: conclusions drawn on baseline_v1 (2024-only) are not exchangeable with baseline_v2 conclusions, particularly regime-availability findings.

**Extension:** every finding with a regime dimension must also carry `detector_version` (from `regime_detector_report.detector_version`). Motivation: the first A2.2 report showed the historical detector's TRENDING label had ~50–59% class-conditional flip rate — all regime-conditional findings from runs 001–039 are findings about *those* labels, not about market regimes. After any retune, entries from prior detector versions may inform hypothesis generation only as low-confidence priors (per A5.1), never as `exhausted_mechanisms` evidence for regime-conditional claims.

---

## 06 — Promotion Rigor

### A6.1 — Split: data reservation moves to NOW (Improvement 07)

The holdout **range reservation** and the walk-forward/holdout **overlap check** are pulled forward into Improvement 07 and implemented before the next run. Rationale: their cost of delay compounds per run (every run further burns potential holdout data); the rest of 06 (deflated Sharpe, promotion_audit, holdout_evaluation stage) keeps its late slot as planned. "Holdout fixed at campaign start" is replaced by the retrofit rule in 07 (holdout disjoint from the union of all historical protocol windows).

### A6.2 — Deflated Sharpe needs cross-trial variance, not just trial count

**Defect:** `promotion_audit.yaml` stores `total_hypotheses_tested` / `total_variants_tested`, but the standard deflated Sharpe ratio (Bailey & López de Prado) requires the **variance (and ideally skew/kurtosis inputs) of the Sharpe estimates across trials**, not only N. With counts alone the tool cannot compute what the plan specifies.

**Change:** `campaign_state.yaml` gains `trial_sharpes: list[float]` — the walk-forward median (or pooled) Sharpe of every trial, appended by the orchestrator after every `protocol_execution` AND every prescreen kill (recorded as Sharpe 0.0 or excluded-with-count, document the choice). `promotion_audit.yaml` gains `trial_sharpe_variance: float`. Prescreened-and-killed variants (Improvement 08) count as trials.

**Extension (post-M0, from A3.4):** median window-Sharpe from sparse-trading strategies is pinned at 0.000 and must not pollute the deflation variance. `campaign_state` stores per trial a record, not a bare float: `{trial_id, sharpe: float|null, expectancy_bps: float|null, n_trades: int, statistic_valid: enum[sharpe, expectancy, neither]}`. The deflation tool computes over `statistic_valid = sharpe` trials and reports the excluded count; the promotion decision for a sparse-trading candidate must rest on expectancy with a t-stat requirement, documented in `promotion_audit.yaml`, not on a Sharpe deflation computed from other strategies' trials.

### A6.3 — Refinement iterations count as trials

Each parameter-bracket refinement re-tested on the same windows is an additional comparison against the same data. Trial count = runs + expansion variants + refinement iterations, not runs alone. (The plan says "variants, not just runs" — extend the same logic one level down.)

### A6.4 — Deduplicate identical trials and verify metric freshness *(added post-M0)*

**Defect (observed):** `forecast_return_corr = 0.2145` was bit-identical across runs 017/024/027/033. Two possible causes, both requiring action before trial counting starts:
1. **Cached/stale computation** being re-read instead of recomputed — given this campaign's history (dead `config_path` wiring, `default_regime` contamination), this must be ruled out first. One-time audit: recompute the metric from raw v1 data for one of those runs and confirm it matches; add a `computed_at` + input-data-hash field to `protocol_result.yaml` diagnostics so staleness is detectable thereafter.
2. **Genuinely identical config on identical data** run four times — legitimate, but then those four runs constitute **one** trial for multiple-testing purposes, not four. *(Resolved: this was the actual cause — identical Keltner signal params across runs 017/024/027/033.)* **Dedup key correction:** the originally specified `(strategy_config_hash, protocol_hash)` key fails here — the four runs' full config hashes *differ* on secondary parameters while producing identical forecasts. Deduplicate by **forecast-series hash** (hash of the computed forecast values over the protocol range — available for free from Improvement 08's prescreen) or, equivalently, a hash of the signal-defining parameter subset only. Identical forecasts on identical data = one comparison, regardless of what else differs in the config.

---

## 08 / 09 — Signal Prescreen & Cost Hurdle *(added post-M0)*

### A8.1 — 08 and 09 must land together, and IC alone is never a pass

**Defect (empirically demonstrated by the Keltner reconciliation):** a signal with IC = 0.2145 delivered −26 bps/trade net. Prescreen's IC gate alone would have *passed* this strategy with a wide margin — 08 without 09's `cost_check` layer creates a gate that dead-but-correlated signals sail through, and stamps them "prescreened," which is worse than no gate. Change: 08 and 09 ship as one step; `prescreen_result.yaml` has no standalone pass state — the proceed-to-backtest route requires both `ic_significance` **and** `cost_check.pass`. Update the routing table in `08` accordingly.

### A9.1 — Named must-reject fixture: `keltner_163`

Improvement 09 acceptance gains a criterion: Layer 2, given the Keltner strategy config and baseline_v2 data, must route it away from a full backtest (fail `cost_check` or equivalent), despite its passing IC. A gate that cannot reject the campaign's best-documented false positive is not calibrated. (Same fixture as A3.5; one dataset, two consumers.) **Side effect to capture:** this fixture run computes the Keltner config's *all-bars* IC via prescreen — write it back into `run_039/artifacts/regime_audit_decision.yaml` to resolve the `ungated_escape_eligible: indeterminate` flag at zero marginal cost; do not run a dedicated ungated backtest for that purpose.

### A8.2 — End-to-end test case: Keltner risk-cap refine *(added at Step 3 acceptance)*

Step 3's channel attribution on `keltner_163` found `primary_weakness = holding_sizing`: direction-picking intact (57% net win rate, winners stable ≈ +65 bps), failure entirely from uncapped adverse excursion (losers −117→−228 bps; worst decile = 129.6% of total PnL; 95% signal-flip exits, no risk cap). Per 03's routing this licenses an execution-layer refine without discarding the signal — creating a tension with the family's `exhausted` status. Ruling:

1. The refine ("Keltner + risk cap") is a **new hypothesis instance**, permitted once, entering through the full gate stack (prescreen → cost hurdle → baseline_v2 walk-forward), counted as a new trial, judged on per-trade expectancy ± SE per A3.4. It serves double duty as the end-to-end acceptance test of the completed 08+09 pipeline.
2. **A-priori parameterization only:** the risk cap is fixed by convention before any run (e.g., stop = k×ATR with conventional k, or time-stop at a principled percentile of holding period) — never tuned against the `keltner_163` ledger, which is fully burnt for this family. One parameterization, one trial. Any grid over stop levels on 2024–2025 data is forbidden.
3. **Calibrated expectations, recorded a priori:** the optimistic bound (losers capped at −80 bps, zero winners harmed) yields ≈ +5 bps/trade net — marginal before stop-out damage to winners and added exit/re-entry costs. A result consistent with ≈ 0 is the expected outcome; the test's primary value is exercising the pipeline. The 2026 holdout is not spent on this hypothesis unless the walk-forward result is unambiguously strong.

### A8.3 — Sparse-forecast IC methodology and full-range computation *(added at 08+09 review)*

**Defect (empirically demonstrated by the A9.1 fixture run):** the Keltner config's "ungated IC ≈ 0" is a tie artifact — with a non-zero forecast on ~1% of bars, Spearman over all bars is dominated by the tie mass at forecast = 0 and collapses toward zero by construction. Consequences: (a) every selective/gated/event-driven strategy fails the prescreen IC gate artifactually — a systematic false-kill channel for exactly the strategy class 03's routing deems refinable; (b) the A9.1 must-reject was not actually validated, because the cost layer was never exercised against a signal that passed the IC gate.

**Changes:**
1. `prescreen_result.yaml` reports `ic_all_bars`, `ic_active_bars` (conditional on non-zero/changing forecast), and `forecast_sparsity_pct`. The IC gate evaluates **active-bar IC**, with significance computed on the active-bar n (block bootstrap on the active subsequence). Dense signals: the two ICs converge; behavior unchanged.
2. Prescreen computes over the **full walk-forward range** (the signal layer without portfolio simulation is near-free); any subsampling requires a documented runtime justification and must be seeded and year-stratified, with n reflected in the significance test. The shipped 2-windows-per-symbol sampling is replaced.
3. **A9.1 re-run required for acceptance:** active-bar IC for the Keltner fixture should land near the historical ~0.2; `cost_check` must then reject independently on edge-vs-cost arithmetic. Add a synthetic boundary case (known IC, turnover engineered to sit just below ratio 2.0) so the threshold is exercised, not only the extremes.
4. `run_039`'s `ungated_escape_eligible` write-back is deferred until the active-bar figure exists; a tie-artifact zero must not resolve the flag toward `signal_bad_everywhere`. *(Resolved: ic_all_bars = −0.012 [CI −0.064, +0.039] AND ic_active_bars = −0.032 [p = 0.83] — escape valid on the conjunction.)*
5. **Conjunction rule for sparse signals:** when `forecast_sparsity_pct` exceeds ~50%, `signal_bad_everywhere` (and the A2.1 escape) requires **both** `ic_all_bars` and `ic_active_bars` to be statistically indistinguishable from zero. All-bars IC alone is ≈ 0 by tie construction for sparse forecasts and is inadmissible as sole evidence; active-bar IC alone measures only the gated subsample. Update A2.3 rule 5 accordingly.

### A8.2 closure *(recorded at 08+09 acceptance)*

The full-range prescreen established that the Keltner signal's pooled active-bar IC is −0.032 (p = 0.83, n = 1125): the historical 0.2145 was a small-per-window-sample artifact (n_active 5–35 per window, IC SE 0.18–0.58). The risk-cap refine's premise — direction-picking skill worth preserving — is falsified: the 57% win rate is a payoff-shape effect of signal-flip exits (many small wins, rare large losses), producible by a zero-IC signal. Step 3's `keltner_163` channel attribution stands as to *where* PnL asymmetry lived (`holding_sizing`) but its implication of a salvageable signal is retracted. **A8.2 is closed unrun**: the refine would be (and effectively was) killed at prescreen — the pipeline enforcing the conclusion is the test passing. The end-to-end pass-path test (prescreen-pass → backtest → verdict) transfers to the first real ungated hypothesis. The Keltner families remain exhausted with root cause upgraded from `no_edge_observed` to signal-level: no informational content on active bars.

---

### A8.4 — Feed-timing alignment check *(added at 01 acceptance; applies to every non-OHLCV feed hypothesis)*

Before prescreen runs on any hypothesis whose forecast consumes a non-OHLCV feed, a documented alignment check must confirm that each bar's feed value was **publicly known at that bar's open** (e.g., funding: predicted-rate vs settlement-published-rate; F&G: daily publication time vs bar assignment). Lookahead through feed alignment is the classic false-positive generator for exactly this hypothesis class, and it inflates prescreen IC — the gate designed to catch weak signals would instead certify a leak. The check is recorded in the run artifacts (`feed_alignment_check: {feed, publication_lag_assumed, verified_how}`). A strong prescreen IC on a feed-based signal triggers re-verification of alignment before routing to backtest, not celebration.

### A8.5 — Condition-activated mechanisms, in-sample thresholds, recalibration trials *(added at run_041)*

Three rules from the H-041-A prescreen (funding extremes never activated in 2024–2025; recalibrated threshold underpowered at n_eff = 10; verdict `insufficient_sample_inconclusive`):

1. **Dormant-mechanism disposition.** `insufficient_sample_inconclusive` caused by regime non-activation is neither kill nor park-indefinitely. Two resolutions, in preference order: (a) **backward data extension** onto unburnt pre-2024 history when the activating condition demonstrably occurs there — prescreen-only first, significance block-bootstrapped **by episode** (extremes cluster; n_events, not n_bars, is the effective sample), results tagged with their era and transferability caveat; (b) parking with a **condition-based reactivation trigger** stored in the knowledge base (e.g., "trailing 30-day funding percentile > X"), not a time-based revisit. Outcome enum for 05: `inconclusive` + `reactivation_condition`.
2. **Percentile thresholds are rolling/past-only.** A signal parameter defined as a percentile of the full test-period distribution embeds future distribution knowledge in the signal definition. All percentile-style activation thresholds must be computed on an expanding or rolling past-only window.
3. **Recalibration = a new trial.** A config whose signal never activates makes no data comparison and is not a trial; the moment a recalibrated variant computes an IC against the data, it is one, recorded as such. Threshold sweeps at prescreen are trials per point — sweeping is discouraged for the same reason prescreen must not rank variants (see the filter-not-fitness rule in `08`).

### A8.6 — A-priori power check at hypothesis registration *(added at run_042)*

**Defect (empirically demonstrated twice):** run_041 (n_eff = 10) and run_042 (n_eff = 13, needed 35+) were both predictably underpowered before any code was written — expected n_eff follows from feed frequency × activation rate × data span × effective symbols. Components were built for prescreens whose verdicts were determined in advance.

**Change:** hypothesis registration (validation gate) computes, deterministically: `expected_active_n`, `expected_n_eff` (episode-clustered where the condition clusters), and `min_detectable_ic` at the campaign's significance level. If `min_detectable_ic` exceeds the plausible IC range for the signal class, the hypothesis routes to `insufficient_power_a_priori` with its stated data requirement (years/symbols needed) — no component is built, no prescreen runs, no trial is spent. Note for market-wide signals (F&G and similar single-index feeds): additional symbols add sublinear power due to return correlation and a shared signal — the correct adjustment is `n_eff_symbols = n / (1 + (n−1)·ρ̄)` with ρ̄ the measured average pairwise return correlation (at ρ̄ ≈ 0.8, ten symbols ≈ 1.2 effective, two ≈ 1.1). A `sqrt(n)` heuristic materially overstates power and is not acceptable; history is the binding resource. Parked-for-power hypotheses carry a `reactivation_condition` naming the data requirement; a consolidated backward-extension work item (pre-2024 history, one prescreen pass over all parked entries) is scheduled after the plan's build steps complete — not per-hypothesis, not ad hoc.

### A8.5.1a-spec — Episode-blocked significance *(added at P1b, 2026-07-05; implements the "significance block-bootstrapped by episode" clause of A8.5 rule 1)*

**Problem this closes:** A8.5 rule 1 named the requirement ("significance block-bootstrapped by episode... n_events, not n_bars, is the effective sample") but left "episode" undefined and unimplemented. The existing prescreen significance path (`prescreen_signal._block_adjusted_significance`) computes `n_eff = active_bars / 24` and applies a Fisher-z normal approximation — this assumes each 24-bar chunk is an independent draw. For a sparse signal whose active bars cluster into real-world episodes lasting far longer than 24 bars (a funding-extreme event, a multi-day sentiment regime), that assumption fabricates independent evidence that does not exist: all bars within one episode share the same underlying draw (the event), not `episode_length / 24` separate draws.

**Full spec** (pre-registered before implementation; see `strategy-research/tools/episode_significance.py`):

1. **Episode construction.** An episode is a maximal run of active bars where consecutive active bars are separated by ≤ `G` inactive bars (`G` configurable, `campaign_config.yaml: episode_significance.gap_bars`, default 48 bars @ 1h ≈ 2 days; gaps > `G` close the episode). An episode never spans a data gap or feed-availability/era boundary — era boundaries are hard cuts regardless of gap size.
2. **Bootstrap.** Statistic = pooled active-bar IC (Spearman, over the concatenated active bars of the episode set). Resample episodes with replacement (same episode count as observed), keeping each episode's internal bars intact; recompute the pooled IC per resample; p-value and CI are read off that resampled distribution (5th/95th percentile CI; two-tailed p-value via the reflection method against zero).
3. **Headline sample size is `n_episodes`**, reported alongside `active_n_bars`. Minimum for any significance claim: `n_episodes >= 8` (`campaign_config.yaml: episode_significance.min_n_episodes`). Below that floor, only descriptive statistics are reported — disposition stays `insufficient_sample_inconclusive` regardless of the computed p-value ("a bootstrap over 4 episodes is theater").
4. **Density fallback.** If activation ≥ 50% of bars (`episode_significance.density_fallback_pct`), episodes degenerate into the whole series — use the existing 24-bar block method (`_block_adjusted_significance`) unchanged. The method is conditional on sparsity.
5. **Era stratification is reporting, not resampling.** Per-era IC and episode counts are reported for context (a 2019–2021 cluster and a 2025 cluster are different market structures), but the bootstrap itself pools across eras — era boundaries only affect where episodes are allowed to break (rule 1), not how many separate bootstraps are run.

**Fixtures** (`strategy-research/tests/test_a851a_episode_bootstrap.py`): (a) synthetic clustered signal with a known per-episode slope → recovered CI covers the pooled point estimate; (b) the same data scored with the naive 24-bar Fisher-z method produces a narrower (overconfident) CI than the episode-bootstrap method — demonstrated empirically, not asserted by construction, using long (200-bar) episodes with per-episode slope variance so the naive method's implicit "~8 independent blocks per episode" assumption is falsified; (c) `n_episodes < 8` suppresses any significance claim regardless of the (deliberately extreme) underlying signal.

**Scope note:** this method is additive — it does not replace `_block_adjusted_significance` for the existing dense, single-era 2024–2025 baseline_v2 window (density fallback routes those cases to the unchanged existing method). It activates specifically for sparse signals evaluated over the P1b multi-era backward-extension range.

---

## Revised implementation order

1. **07** — data extension + holdout retrofit *(one day of work; before any further run)* — **DONE (M0 achieved)**
2. **02** — regime detector validation *(as planned; with A2.1; seed `known_weak_periods` candidates with the 14 zero-trade window-symbol slots from the Keltner v2 re-run so the detector audit explicitly adjudicates whether "structural regime absence" is real or a threshold-calibration artifact)*
3. **03** — trade diagnostics *(as planned; with A3.1–5, incl. the `keltner_163` signature-reproduction fixture)*
4. **08 + 09** — signal prescreen + cost hurdle *(land together per A8.1; `keltner_163` must-reject per A9.1; unlocks cheap kills + A2.1's escape hatch)*
5. **01** — edge-source taxonomy *(with A1.1–3; after 02/03 per original plan)*
6. **05** — knowledge base *(with A5.1–3, incl. the vocabulary hard rule)*
7. **04** — indicator library *(as written; lowest priority — the "book indicator" convergence is primarily a data-scope symptom, which A1.2's feed_wishlist addresses at the root)*
8. **06** — remaining promotion rigor *(deflated Sharpe with A6.2–4, holdout_evaluation stage; before any live deployment)*

**Standing one-time audit (before step 2 concludes):** the A6.4 metric-freshness check on the identical `0.2145` correlations across runs 017/024/027/033 — if it reveals stale computation, that is a stop-the-line bug to fix before any new trial is recorded.
