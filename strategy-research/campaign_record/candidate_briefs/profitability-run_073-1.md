---
strategy_domain: short_horizon_reversal
market_universe:
- BTCUSDT
- ETHUSDT
timeframe: 1h
venue: kraken
product: perp
research_goal: 'Test a finding the profitability reader noticed after run_073 on idea
  HOURLY_SHOCK_REVERSAL_MEAN_REVERSION_1H_BTC_ETH__trade_efficiency-run_070-1: The
  shock_reversal forecast at period=2 predicts zero forward returns (median forecast_return_corr=-0.0057,
  not significant), indicating smoothing reduces oscillation but cannot create an
  edge from a noisy signal. Its claim block is pre-filled (candidate.claim). Evidence:
  variants.base.slices.overall.diagnostics.median_forecast_return_corr=-0.0057; variants.base.slices.per_window[1,2,3,4,5,6].core.forecast_return_corr:
  -0.0112, -0.0002, +0.0196, -0.0154, -0.0269, +0.0120; all p_value > 0.143 (block-adjusted
  > 0.768); variants.design_period_3.slices.overall.diagnostics.median_forecast_return_corr=-0.0047
  (same zero signal across variant); variants.base.slices.overall.diagnostics.per_trade_expectancy_bps.mean=-6.1015
  (highly negative t-stat -12.47) despite zero forecast correlation, ruling out cost-only
  hypothesis'
machine_constraints:
  protocol:
    symbols:
    - BTCUSDT
    - ETHUSDT
    timeframe: 1h
    start: '2022-01-01'
    end: '2023-12-31'
    window_months: 4
candidate:
  claim:
    statement: The shock_reversal forecast at period=2 predicts zero forward returns
      (median forecast_return_corr=-0.0057, not significant), indicating smoothing
      reduces oscillation but cannot create an edge from a noisy signal.
    kind: direction_forecast
    tests:
    - name: shock_reversal_rank_ic
      selector:
        kind: all
      outcome:
        kind: fwd_return
        horizons:
        - 1
        - 2
        - 3
        - 4
      baseline: null
      statistic: rank_ic
      direction: greater
      floor:
        min_windows: 4
    pass_if: Rank IC between shock_reversal forecast and forward returns at horizons
      1-4 is significantly positive (z > 1.96 equivalent) in at least 4 windows, with
      min_events 100.
    fail_if: Rank IC is near zero (< 0.03 absolute magnitude) or negative and consistent
      across most windows, confirming no directional predictive power.
    rationale: If the forecast has no directional content (IC ≈ 0), smoothing the
      signal's oscillation cannot create profitability. The measured forecast_return_corr
      of -0.0057 median across all 6 windows suggests the zscore shock reversal mechanism,
      even period-2 averaged, captures noise rather than mean-reversion. This test
      verifies whether the block predicts returns independent of turnover, separating
      forecast quality from cost-adjustment.
  criteria_from: hypothesis_generation
  source:
    origin: reader
    proposal_ref: runs/run_073/artifacts/proposals/profitability.yaml#profitability-run_073-1
    source_run: run_073
    parent_hypothesis_id: HOURLY_SHOCK_REVERSAL_MEAN_REVERSION_1H_BTC_ETH__trade_efficiency-run_070-1
    hypothesis_id: HOURLY_SHOCK_REVERSAL_MEAN_REVERSION_1H_BTC_ETH__trade_efficiency-run_070-1__profitability-run_073-1
    decision_ref: runs/run_073/artifacts/decision_record.yaml
    proposal:
      kind: side_finding
      claim:
        statement: The shock_reversal forecast at period=2 predicts zero forward returns
          (median forecast_return_corr=-0.0057, not significant), indicating smoothing
          reduces oscillation but cannot create an edge from a noisy signal.
        kind: direction_forecast
        tests:
        - name: shock_reversal_rank_ic
          selector:
            kind: all
          outcome:
            kind: fwd_return
            horizons:
            - 1
            - 2
            - 3
            - 4
          baseline: null
          statistic: rank_ic
          direction: greater
          floor:
            min_windows: 4
        pass_if: Rank IC between shock_reversal forecast and forward returns at horizons
          1-4 is significantly positive (z > 1.96 equivalent) in at least 4 windows,
          with min_events 100.
        fail_if: Rank IC is near zero (< 0.03 absolute magnitude) or negative and
          consistent across most windows, confirming no directional predictive power.
        rationale: If the forecast has no directional content (IC ≈ 0), smoothing
          the signal's oscillation cannot create profitability. The measured forecast_return_corr
          of -0.0057 median across all 6 windows suggests the zscore shock reversal
          mechanism, even period-2 averaged, captures noise rather than mean-reversion.
          This test verifies whether the block predicts returns independent of turnover,
          separating forecast quality from cost-adjustment.
      evidence:
      - variants.base.slices.overall.diagnostics.median_forecast_return_corr=-0.0057
      - 'variants.base.slices.per_window[1,2,3,4,5,6].core.forecast_return_corr: -0.0112,
        -0.0002, +0.0196, -0.0154, -0.0269, +0.0120; all p_value > 0.143 (block-adjusted
        > 0.768)'
      - variants.design_period_3.slices.overall.diagnostics.median_forecast_return_corr=-0.0047
        (same zero signal across variant)
      - variants.base.slices.overall.diagnostics.per_trade_expectancy_bps.mean=-6.1015
        (highly negative t-stat -12.47) despite zero forecast correlation, ruling
        out cost-only hypothesis
---

# profitability-run_073-1

Written by tools/decide_next.py (E-059, slice 6b) from runs/run_073/artifacts/proposals/profitability.yaml#profitability-run_073-1; decision record: runs/run_073/artifacts/decision_record.yaml.

This brief carries no pass criteria on purpose (operator decision 2, 2026-09-24): step 1a writes a hypothesis card and criteria coherent with the proposed idea, from config/criterion_menu.yaml. A patch's resolved config passes through to 1b (candidate.config), and 5a checks it against candidate.source.expected_config_sha256.
