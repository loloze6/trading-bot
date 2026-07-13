# Research Brief — P4-TS-TREND: Time-Series Trend Following (daily)
# Format: adapt field names to the research_brief handoff template in use; content is authoritative.
source: user_delivered   # authoritative version, delivered from the Phase-P advisor set

objective: >
  Test canonical time-series momentum on daily bars per coin: hold long when
  trailing return / MA-cross condition is positive, flat otherwise (spot-only,
  no shorts). Daily timeframe chosen deliberately: the same per-trade edge is
  amortized over multi-week holds, which is what makes ~17 bps round-trip
  survivable (P3 viable-space map should confirm this cell clears Layer 1).

edge_source:
  category: persistent_behavioral_bias
  specific_mechanism: >
    Serial correlation of returns at multi-week horizons from underreaction /
    slow capital flows; the most replicated anomaly in the managed-futures
    literature, documented in crypto majors.
  why_not_arbitraged: >
    Requires tolerating long flat/whipsaw periods and deep relative drawdowns;
    the premium is compensation for that path, not free money. Crowding caps
    size, which is irrelevant at retail scale.
  evidence_type: price_volume_only
  measurable_proxy: sign(trailing L-day return) vs subsequent-period return
    (active-bar IC on entry/exit transitions; A8.3 sparse rules apply — the
    signal changes rarely at daily frequency).

hypothesis_space:
  signal: long iff close > SMA(L) (or trailing L-day return > 0 — pick ONE
    formulation at registration, do not test both silently; the second is a
    separate registered trial).
  parameters_a_priori:
    lookback_L: 100d      # literature-conventional; NOT swept
    execution: next-day open after signal change
    position: full allocation per symbol, universe-parallel (one trial covers
      all universe symbols as breadth, per Improvement 11 Part D)
  variants_allowed: none in first pass.

constraints:
  - protocol: daily bars over the extended range (2019+ where per-symbol history
    exists), baseline windows; per-symbol results aggregated with
    correlation-adjusted breadth.
  - benchmark rule: report excess over buy-and-hold per symbol AND over
    equal-weight universe — TS trend on crypto majors 2019–2025 must beat
    holding, not just zero, to matter. Also report the flat-period fraction and
    max relative drawdown vs buy-and-hold (the realistic adoption killers).
  - cost: daily-bar trades are infrequent; Layer 2 should pass easily — if it
    does not, the cost model is misconfigured, investigate before proceeding.

power_preregistration:
  expected_active_n: signal transitions ≈ 10–25 per symbol over 6y; episodes
    cluster — n_events accounting per A8.5. Breadth across ~15 symbols with
    correlation adjustment is what makes this powered at all; single-symbol
    verdicts are explicitly out of scope.
  min_detectable_effect: <compute at registration>
  plausible_outcome_range: net excess-over-hold Sharpe 0.0–0.5; long flat
    periods expected. Materially higher → audit first.

kill_criteria_preregistered:
  - pooled per-trade expectancy (net, across universe) CI includes 0 →
    insufficient/no edge per A3.4 statistic rules
  - beats zero but not buy-and-hold on excess → recorded as
    edge_but_wrong_benchmark (KB note: trend as drawdown-reduction overlay is a
    different, later hypothesis — do not silently morph this one into it)

# ---------------------------------------------------------------------------
# ADDENDUM (2026-07-07, added by the research pipeline). The original
# user-delivered brief text above is UNCHANGED and remains byte-identical to
# the installed original per the custody rule — this section registers an
# operational significance-methodology decision required before this brief's
# SMA(100)-daily hypothesis could be run through prescreen_signal.py.
# ---------------------------------------------------------------------------

pre_registration_addendum:
  finding: >
    The brief's own signal formulation (long iff close > SMA(L), flat
    otherwise, spot-only/no shorts) is long-only with a single constant
    magnitude when active. prescreen_signal.py's default active-bar Spearman
    IC (ic_active_bars) is mathematically undefined for this shape (zero
    variance among active-bar forecasts) — discovered via a pre-launch
    shakedown run on 2026-07-07, BEFORE the real registration.
  significance_methodology_for_single_magnitude_signals: block_bootstrap_all_bars_v1
  methodology_description: >
    Circular stationary block bootstrap on the pooled ALL-BARS rank IC
    (prescreen_signal._stationary_block_bootstrap_ic_significance), used only
    when the active-bar forecast is structurally degenerate (fewer than 2
    distinct values among active bars —
    prescreen_signal._is_degenerate_active_forecast). Triggers automatically;
    no per-hypothesis config flag needed.
  block_size_bars: 20   # ~1 trading month — matches this brief's own
    # edge_source.specific_mechanism "multi-week horizons" serial-correlation
    # claim. Fixed BEFORE observing this run's IC value — see
    # prescreen_signal._BOOTSTRAP_BLOCK_SIZE_1D for the full justification.
  n_resamples: 1000
  seed: 20260707   # fixed for reproducibility, not re-randomized per call
  significance_threshold: 0.10   # matches the campaign-wide p<0.10 gate (unchanged)
  in_sample_value_seen_pre_registration: >
    A shakedown run (2026-07-07, prior to this addendum and prior to the real
    registration) observed ic_all_bars=0.0359 on this exact SMA(100)-daily
    config over the full 2018-2025 range. This value was OBSERVED, not used to
    tune block_size, n_resamples, or the threshold above — those were fixed
    from the campaign-wide defaults (0.10 significance) and an a-priori
    justification (block_size from the brief's own stated mechanism horizon)
    before this value was seen. Recorded here for audit transparency per this
    campaign's pre-registration hygiene standard.
  related_finding: >
    The same shakedown also surfaced a second, independent bug in
    prescreen_signal.py's turnover proxy (trade-count estimator used for the
    Layer-2 cost gate): it counted sign FLIPS only, so any long-only (or
    short-only) signal with flat gaps between episodes was undercounted as a
    single trade. Fixed the same day (prescreen_signal._compute_turnover_proxy,
    activity-transition definition) — this brief's SMA(100)-daily registration
    is the first hypothesis to depend on a correct turnover estimate for a
    long-only signal.
  reference: strategy-research/tools/prescreen_signal.py (functions
    _is_degenerate_active_forecast, _stationary_block_bootstrap_ic_significance,
    _compute_turnover_proxy)
  regression_tests:
    - strategy-research/tests/test_prescreen_degenerate_signal_gate.py
    - strategy-research/tests/test_turnover_proxy.py

  second_addendum_2026_07_08:
    warmup_insufficiency_finding: >
      A real protocol_execution run (2026-07-07/08, before this addendum) showed
      ZERO trades in every monthly window of the original protocol, regardless of
      symbol. Root cause: SmaTrendLongOnlyComponent needs 101 days of warmup, but
      the engine's actual readiness requirement is closer to 2x that (~200 bars)
      -- strategy_engine.is_ready() requires each component's history deque to
      reach length strategy_engine._warmup, and that deque only starts filling
      once the component itself becomes ready at required_bars bars, so total
      bars needed before first readiness is required_bars + _warmup - 2 (verified
      empirically: 101+101-2=200, matching an observed first-ready bar of 200).
      A single ~30-day monthly window can never supply that much daily-bar
      history on its own -- every window showed trades=0 by construction, not
      because the signal lacks edge. This run leaked NO information about the
      signal itself (a structurally-zero-trade result carries no evidence either
      way) and is not cited as a finding about the mechanism.
    engine_fix: >
      trading-bot/core/launcher.py's run_backtest() gained an opt-in
      warmup_prefetch flag (default False, bit-identical when omitted -- see
      trading-bot/tests/test_warmup_prefetch_bit_identical.py): when True, fetches
      2x strategy.required_bars of EXTRA history before the window's start date
      and feeds it through the strategy silently (BacktestEngine/TradingBot's new
      warmup_cutoff_timestamp -- bars before it update the strategy but never
      trade), asserting is_ready() actually holds by window_start. 2x is a
      proven-sufficient upper bound (strategy_engine._warmup <= required_bars
      always), not the fragile exact formula. This applies to every strategy
      config, including 1h production ones -- documented so the 2x prefetch is
      not later "optimized" back to 1x. strategy-research/tools/run_protocol.py
      now passes warmup_prefetch=True unconditionally, with an assertion that the
      backward-extended buffer never reaches into the holdout range.
    left_edge_data_resolution: >
      The 2x-required_bars (202-day) prefetch for the first window would reach
      before Binance's earliest BTCUSDT/ETHUSDT data. Confirmed via live fetch:
      both symbols' true exchange history starts 2017-08-17 (not 2018-01-01, the
      prior local_data/*_1d.csv cache start). Resolved by BOTH: (1) extending the
      backfill to 2017-08-17 (verified continuous, no gaps, via check_data.py),
      and (2) moving the protocol's first scored window to 2018-04-01 (Q2) rather
      than 2018-01-01, giving a 25-day safety margin (2018-04-01 minus 202 days =
      2017-09-11, after the 2017-08-17 floor).
    window_redesign: >
      Monthly (~30-day) windows, copied from the 1h baseline_v2.json convention,
      are also statistically meaningless for this signal independent of the
      warmup fix: the shakedown showed ~6.4 opens/symbol/year (51 opens/symbol
      over the full 2018-2025 range) -- far below what any 1h-calibrated
      per-window density assumption expects. Redesigned to semi-annual (182-day)
      non-overlapping windows (~3.2 expected trades/window): comfortably clears a
      quarterly (91-day, ~1.6 expected) floor with real margin, while giving 2x
      the walk-forward sample count of annual windows. 15 windows total,
      2018-04-01 through 2025-10-01, all ending before the 2026-01-01 holdout
      boundary (asserted in run_protocol.py).
    min_trade_count_gate_finding: >
      protocols/ts_trend_daily_v1.json's promotion.min_trade_count_gte was 20,
      also copied from the 1h baseline_v2.json convention (a per-WINDOW minimum
      across all windows, per run_protocol.py's _promote()/min() logic) -- this
      brief's own power_preregistration expects only 10-25 TOTAL transitions per
      symbol over 6 years; no window length, however long, would plausibly reach
      20 trades per window for this signal class without collapsing the
      walk-forward to 1-2 windows total. Revised to 1 (at least one completed
      round-trip required for a window to count as evaluable), matching the lower
      end of the brief's own a-priori expectation (10-25 transitions / 15 windows
      ~= 0.7-1.7/window). Pre-registered floor, not tuned to observed values.
    bar_count_sweep_not_actionable: >
      Swept everything downstream of protocol_execution for other bar-count
      assumptions: performance/metrics.py's core calculate_sharpe_ratio already
      groups to calendar days before applying sqrt(365) annualization (confirmed
      timeframe-agnostic by direct inspection and by the bit-identical test's own
      captured sharpe_annualization field). A separate function,
      classify_full_history, hardcodes sqrt(8760) (hourly) annualization for its
      own rolling-volatility regime heuristic, but is confirmed reachable only
      via launcher.py's interactive CLI path, never via run_backtest()/
      run_protocol.py -- not on this hypothesis's critical path, documented only.
      run_054's validation_protocol.yaml (LLM-authored) narrates "12 overlapping
      30-day windows," mismatched with the actual 15 semi-annual windows above --
      informational only (run_protocol.py's criterion evaluator extracts
      metric/operator/threshold from decision_rules/required_evidence text, not
      window count), not regenerated (would require re-running the
      backtest_specification LLM stage, out of scope for a manual protocol fix).
    reference:
      - trading-bot/core/launcher.py (run_backtest's warmup_prefetch)
      - trading-bot/core/backtester.py (BacktestEngine.warmup_cutoff_timestamp)
      - trading-bot/core/trading_bot.py (TradingBot._process_symbol_candle_completion)
      - trading-bot/tests/test_warmup_prefetch_bit_identical.py
      - strategy-research/tools/run_protocol.py (warmup_prefetch wiring, holdout guard)
      - strategy-research/protocols/ts_trend_daily_v1.json (windows, min_trade_count_gte)
