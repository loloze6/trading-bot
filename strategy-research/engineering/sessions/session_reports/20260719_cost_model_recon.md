# Phase 1.2 Step A — Cost-Model Recon (read-only)

Date: 2026-07-19
Precondition check: PASSED (HEAD=618d548; git status showed exactly the expected untracked venue-survey report).

## Step 1 — Fee/cost sites in trading-bot/'s backtest execution path

### `trading-bot/execution/portfolio_info.py`
- `portfolio_info.py:86-87` — `CommonPortfolioDef.__init__(self, commission_rate=0.001)` → `self.commission_rate = commission_rate`. This is the base class both live and mock portfolios inherit from.
- `portfolio_info.py:105,115,125,133,150,158,172,188` — `update_local_balance()` applies `commission` (= `self.commission_rate`) as a flat multiplicative haircut on quantity/cost for every buy/sell/short/repay branch (e.g. `received_qty = quantity * (1 - commission)`).
- `portfolio_info.py:293,296` — `PortfolioInfo.__init__(self, initial_balance=..., commission_rate=0.001)` (live/Binance-backed class) — same default, passed straight to `super().__init__(commission_rate)`. Note: this class does NOT read the fee from the actual Binance account/API; it's the same hardcoded constructor default as the mock class.
- `portfolio_info.py:324,327` — `MockPortfolioInfo.__init__(self, initial_balance=..., commission_rate=0.001)` — same pattern, used for backtesting.

### `trading-bot/core/backtester.py`
- `backtester.py:43` — `BacktestEngine.__init__(..., commission_rate: float = 0.001, ...)` constructor parameter.
- `backtester.py:73` — `self.commission_rate = commission_rate` (stored but engine itself doesn't apply it directly — see launcher wiring below; it's threaded through to the performance tracker / portfolio classes instead).

### `trading-bot/core/launcher.py` (the actual wiring point)
- `launcher.py:28` — `DEFAULT_COMMISSION_RATE: float = 0.001` — the single global constant.
- `launcher.py:37` — `TradingParams.commission_rate: float = DEFAULT_COMMISSION_RATE` (dataclass default).
- `launcher.py:148-153` — `_build_mock_stack()` passes `params.commission_rate` into both `EnhancedPerformanceTracker(...)` and `MockPortfolioInfo(commission_rate=...)`.
- `launcher.py:199` — a second `EnhancedPerformanceTracker(DEFAULT_COMMISSION_RATE)` construction site (separate from `_build_mock_stack`, does not go through `params.commission_rate`).
- `launcher.py:519` — `TradingParams(..., commission_rate=DEFAULT_COMMISSION_RATE)` in a third builder path — again bypasses whatever `params.commission_rate` the caller might have wanted, always resets to the global default.

### `trading-bot/performance/metrics.py`
- `metrics.py:48` — `CompletedTrade.commission_rate: float = 0.001` (dataclass field default, independent constant, not sourced from launcher's `DEFAULT_COMMISSION_RATE` — a second hardcoded literal).
- `metrics.py:315-316` — `EnhancedPerformanceTracker.__init__(self, commission_rate: float = 0.001, ...)` — third independent hardcoded default `0.001`.
- `metrics.py:175-215` — `entry_commission`/`exit_commission`/`total_commission`/`pnl_with_commission` all apply `commission_rate` as a flat % of trade notional; no spread or slippage term anywhere in this file.

### `trading-bot/execution/execution_handler.py`
- **No fee/commission/spread/slippage logic found at all.** Grepped for fee|commission|slippage|spread|maker|taker — zero matches. The execution handler issues orders (live/mock) but does not itself apply any transaction-cost model; costs are applied entirely downstream in `portfolio_info.py`'s balance simulation and `metrics.py`'s trade accounting.

### `trading-bot/config.json`
- **No fee/commission key exists anywhere in the file.** Full file read; sections are `api`, `trading`, `strategy`, `risk_management`, `logging` — none reference cost/fee/commission. The rate is not configurable via config.json at all; it only lives as Python constructor defaults / a Python constant (`DEFAULT_COMMISSION_RATE` in `launcher.py`).

### Characterization
- **Single flat rate**: yes — 0.001 (10 bps) taker-equivalent, applied identically to every trade regardless of symbol, side, or maker/taker.
- **Spot-only vs. margin-aware**: the commission model itself is fee-only; it has no margin-interest, funding-rate, or borrow-cost term (separate from the margin *balance* mechanics elsewhere in `portfolio_info.py`).
- **Fee-tier-aware**: no — no VIP tier, no BNB discount, no maker/taker split.
- **Spread/slippage modeled**: no — grep for slippage/spread/bid_ask across all of `trading-bot/` found zero cost-relevant hits (the only "spread" hits are `EMASpreadComponent` in `strategy_components.py`, an unrelated EMA-difference indicator, not a trading cost).
- **Swappable per-venue vs. global constant**: currently a **single global Python constant duplicated in three independent places** (`launcher.DEFAULT_COMMISSION_RATE`, `metrics.CompletedTrade.commission_rate` default, `metrics.EnhancedPerformanceTracker.__init__` default), all independently hardcoded to `0.001`, not read from `config.json`, and not keyed by symbol or venue. It is technically a constructor parameter (so callers *can* override it), but nothing in the current call graph varies it per-venue — every builder path in `launcher.py` (`_build_mock_stack`, the two other constructor sites at lines 199 and 519) resolves back to the same single default.

### Important adjacent finding: a parallel, already-parameterized cost model exists — but is not wired to trading-bot at all
`strategy-research/config/cost_model.yaml` (v1.1, updated 2026-07-04) is a **separate, fully venue/symbol-parameterized cost model**: per-symbol `fee_rate_bps` (7.5 bps taker, Binance VIP0 + BNB discount), per-symbol `spread_estimate_bps`, per-symbol `slippage_estimate_bps`, precomputed `round_trip_cost_bps` (17.0–20.5 bps depending on symbol), plus an additive `execution_style.{taker,maker}` block with fill-rate-blended maker costs. Its header states: "RULE: No fee or spread constant may be hardcoded anywhere else after Improvement 09." This model is consumed by `strategy-research/tools/run_protocol.py` (`_cost_paid_bps`), `strategy-research/tools/prescreen_signal.py`, and the verdict-interpreter's `cost_drag` diagnostic — i.e., the **research/validation layer**, not `trading-bot`'s actual `core/backtester.py` / `execution/portfolio_info.py` execution path. Those two cost models currently disagree materially: trading-bot's live/backtest engine assumes flat 10 bps with no spread/slippage; the research layer assumes 17–20.5 bps round-trip (7.5 bps/side fee + spread + slippage) per symbol. They are not the same number and not the same code path.

## Step 2 — Cost-driven near-miss candidates in `campaign_knowledge_base.yaml`

Grepped all `root_cause:` fields (17 findings total) for any literal cost reference. Exactly **one** finding has `root_cause` literally naming cost as the reason:

**Candidate 1 — `rsi_momentum_trending_cost_drag`** (line 153)
- `root_cause: cost_drag` (verbatim, literal cost root cause — the only one in the KB)
- Failing criterion: `cost_drag_pct: 272.865` (signal_property), `forecast_return_corr: 0.018`
- `exhausted_basis` verbatim: "Analytic: cost_drag=273% means gross edge is overwhelmed by transaction costs by 2.7×. corr=0.018 is also near-zero. Structurally cost-unviable at this trade frequency."
- Note: this is not a *narrow* miss (273% vs. an implicit ~100% break-even line is a blowout, not a near-miss), but it is unambiguously the KB's clearest "root_cause = cost" example.

No second finding has `root_cause` literally naming cost. The closest genuine second candidate, reported honestly rather than forcing a match:

**Candidate 2 — `keltner_scoremode_no_edge`** (line 102) — root_cause field is `signal_quality`, **not** cost, but its `exhausted_basis` explicitly cites cost as sufficient on its own to close the family:
- Failing criterion: `cost_drag=84%` on the highest-IC variant (run_028) — closer to the ~100% break-even line than candidate 1's 273%, i.e. the more "near-miss"-shaped of the two by magnitude.
- `exhausted_basis` verbatim (partial): "Analytic (A5.1): cost_drag=84% on the highest-IC variant (run_028) is a 4× structural cost barrier — arithmetic, not parameter-sensitive. No tuning reduces round-trip cost at this signal frequency. ... The analytic cost failure alone suffices to close this family per A5.1 (math doesn't need replication)."

Also considered and rejected as weaker matches (cost_check failed but was not the dominant/named root_cause — root_cause was `already_priced_in`, `lag_mismatch_to_regime_persistence`, or `no_informational_content_this_venue` respectively, with `edge_to_cost_ratio` 0.36/0.24/0.25 vs. the 2.0 `safety_factor` threshold in `cost_model.yaml`, all far below the pass line rather than a narrow miss): `ema_spread_trend_continuation_v1_auto`, `funding_rate_continuous_mean_reversion_expanded_auto`, `volume_impulse_continuation_blocked`. Also considered: `fear_greed_contrarian_v2_validation_rejected` (line 302), whose `exhausted_basis` cites "cost-feasibility infeasibility (6% activation / 270 trades over 13mo against a 34 bps/trade requirement vs. a 5-20 bps historical sentiment edge)" as one of two blocking grounds (the other being an era sign-flip) — cost-relevant but entangled with a second independent blocking ground, so not cleanly attributable to cost alone.

## Step 3 — Swap-in vs. structural rework

Two distinct systems exist: (1) `trading-bot`'s actual backtest/live engine, which uses a single hardcoded global commission constant (0.001, duplicated across `launcher.py` and `metrics.py`) with **no spread, no slippage, no per-symbol/venue table, and no config.json exposure** — this needs structural rework (add spread/slippage terms, a per-symbol/venue rate table, and config.json exposure) before it can be venue-parameterized; and (2) `strategy-research/config/cost_model.yaml`, which is already fully venue/symbol-parameterized (fee/spread/slippage/maker-taker) for Binance but is wired only into the research validation tools, not into `trading-bot`'s execution path at all. Swapping in Kraken's numbers is a trivial edit in system (2) but does nothing for system (1) unless it's also rebuilt to consume the same structure.
