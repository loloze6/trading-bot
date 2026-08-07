# Strategy-Research Pipeline — Closing State (Plan v2 Complete)

**ARCHIVED SNAPSHOT — superseded by `strategy-research/00_closing_state.md` (the
top-level file of the same title is the current, canonical version; this copy
under `docs/plan/` is preserved for historical record only, per that file's
own "archived under version control in `docs/plan/`" note. Read this only for
what the plan looked like at this point in time, not as current status.**

**Status: enhancement plan complete (M0–M3), pending final verification of two Improvement 06 acceptance outputs.** This document supersedes `00_overview_v2.md` as the entry point. Future sessions (human or agent) start here, then `AMENDMENTS_01-06.md` (which overrides the original plan docs `01`–`09` wherever they conflict). Do not reconstruct campaign state from run artifacts or memory — this document plus the amendments file plus `campaign_knowledge_base.yaml` are the canonical record.

## 1. What was built (one line per step, implementation order)

| Step | Delivered |
|---|---|
| 07 | baseline_v2 (24 windows, 2024–2025), frozen 2026-H1 holdout with mechanical overlap guard, burned-range accounting, `campaign_data_policy.yaml` |
| 02 | Detector validation tool (persistence, class-conditional sensitivity, activation band), regime-auditor skill, retune firewall (hard-fail) — verdict: ER-family detection **unusable** on BTC/ETH 1h (48-cell grid, Pareto-blocked); campaign is **ungated-only** |
| 03 | Trade-level diagnostics (MAE/MFE, entry/exit efficiency, post-exit tracking, per-trade cost, winner/loser-conditional metrics), A3.4 sparse-Sharpe null-floor + expectancy-primary rule, `keltner_163` fixture (exact-match reproduction) |
| 08+09 | Signal prescreen (active-bar IC, sparsity, block-bootstrap significance, full-range) + two-layer cost hurdle, single `cost_model.yaml`, trial recording live from the first gate |
| 01 | Five-category edge-source taxonomy (incl. `persistent_behavioral_bias`), anti-confabulation proxy rule, `available_feeds.yaml` constraint, `feed_wishlist.yaml`, structured `mechanism_failure` root causes |
| 05 | `campaign_knowledge_base.yaml` with auto-write hook, derived views (coverage matrix, exhausted mechanisms with A5.1 thresholds enforced in view logic), KB-gated campaign-review and hypothesis-design handoffs |
| 04 (slim) | Seeded `indicator_library.yaml` (12 entries), lookup protocol in hypothesis-design, real-diversity check in innovation-expansion; **no** empirical write-back (KB owns results) |
| 06 | Deflated Sharpe (B&LdP) over deduplicated structured trial records, expectancy path for sparse traders, `promotion_audit.yaml`, single-use `holdout_evaluation` stage with pre-registered expected ranges |
| A8.x | Methodology layer accreted from live runs: sparse-IC conjunction rule, feed-timing alignment check, dormant-mechanism dispositions, rolling-only percentile thresholds, a-priori power check with correlation-adjusted effective symbols |

## 2. Campaign epistemic state (honest)

- **Confirmed edges: zero.** The historical "confirmed edge" (Keltner, IC 0.2145) was fully dismantled: unstable regime labels → tiny selected sample → small-sample noise (pooled active-bar IC −0.032, p 0.83) → payoff-shape illusion (57% win rate manufactured by signal-flip exits) → linguistic inflation carried by memory. Every layer has a named countermeasure now in place.
- **Parked (inconclusive, powered-out, with computed reactivation conditions):** H-041-A funding-extreme mean-reversion (regime dormant 2024–25; trigger: trailing funding percentile OR 2018+ data); H-041-C F&G contrarian (IC +0.19, cost ratio 3.75, n_eff 13 vs 35 needed; fix: 2018+ data → n_eff ≈ 46; more symbols explicitly ruled out — market-wide signal, ρ̄ ≈ 0.82).
- **Blocked:** H-041-B volume impulse (mechanism-impure proxy; unblocks with `liquidation_data` feed).
- **Structural findings:** ER regime detection unusable on 1h (detector wishlist holds daily-overlay as priority-1, trigger: an ungated edge showing regime-dependent performance). OHLCV-only generated zero honest hypotheses; the viable space is feed-driven, and current feeds (funding 8h, F&G daily) are power-limited on 2 years × 2 correlated symbols.
- **Runs 001–039 are historical only:** baseline_v1 windows are burnt; regime-conditional conclusions from that era are labeled with their detector version and are inadmissible as exhaustion evidence.

## 3. Standing rules (survive the plan; violations are stop-the-line)

1. **Holdout (2026-H1) is untouchable** except by `holdout_evaluation`, once per hypothesis, pre-registered expected range, failure terminal.
2. **Everything that touches data is a trial** — prescreen kills, recalibrations, refinements — recorded as structured records (`statistic_valid`), deduplicated by forecast-series hash.
3. **Vocabulary is mechanical:** outcome enums only; "confirmed" is unwritable without a passing `promotion_audit`; positive IC is a signal property, never an edge outcome.
4. **Detector retunes never see PnL** (hard-fail firewall); any new detector passes the full 02 gate before its labels condition anything.
5. **Non-OHLCV feeds require a documented alignment check before prescreen**; a strong feed-signal IC triggers alignment re-verification, not celebration.
6. **Prescreen is a filter, not a fitness function** — no variant ranking by IC; percentile thresholds are rolling/past-only.
7. **Power is checked a priori** (deterministic, pre-component-build); market-wide signals use `n/(1+(n−1)·ρ̄)` effective symbols.
8. **Sparse signals:** window-Sharpe below the trade floor is null, expectancy ± SE is primary; `signal_bad_everywhere` needs the all-bars AND active-bar IC conjunction.
9. **Prompt/skill changes are accepted by output audit** (A1.4), never diff review; new metrics are accepted against known-answer fixtures (`keltner_163` is the standing one).
10. **Fee/spread constants live in `cost_model.yaml` only**; `campaign_config.yaml` values are drift-guarded by test against code constants.

## 4. Open items

| Item | Status / trigger |
|---|---|
| 06 acceptance outputs | Pending: Keltner must-NOT-pass numbers + synthetic must-PASS parameters on record |
| 04 generation audit | Rides on the first live hypothesis batch (audit `library_lookup`, deviation justifications, `diversity_audit`) |
| Backward-extension pass | Scheduled, not started: fetch/validate 2018+ (funding exists ~Sep 2019; F&G from Feb 2018), one prescreen re-run over parked hypotheses |
| Feed wishlist | `liquidation_data` (argued case: unblocks mechanism-pure volume hypotheses) |
| Detector wishlist | Daily-overlay priority 1; trigger: ungated edge with regime-dependent 03 diagnostics |
| Config runtime wiring | Code still reads own constants; drift-guard test in place; "new campaign = config-only" bar NOT met until refactor |
| Trading-bot backlog | Engine-recorded exit reasons in PerformanceTracker (replace post-hoc inference, currently 95% inferred) |

## 5. Pending decision (user's, not an implementation detail)

**New hypothesis batch first vs backward-extension first.** Recommendation on record: batch first (completes 04's audit, exercises the full stack including the never-yet-traversed pass path, near-zero marginal cost under prescreen); extension second (holds the campaign's only live lead, H-041-C, and its data engineering is better done once, deliberately). If the batch returns empty — likely, given the demonstrated narrowness of the honest space — the extension is the obvious successor, so this ordering is nearly free even in hindsight.

## 6. Orientation for future sessions

Read order: this file → `AMENDMENTS_01-06.md` → the specific plan doc for whatever is being touched → `campaign_knowledge_base.yaml` for empirical state. The amendments override the plan docs. The knowledge base, not `findings_carryover.yaml`, is the cross-run memory. Acceptance culture: known-answer fixtures for metrics, output audits for prompts, pre-registered expectations for runs, and outputs (numbers, channels, cards) reported — never bare pass marks.
