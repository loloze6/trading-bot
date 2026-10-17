---
strategy_domain: short_horizon_reversal
market_universe:
- BTCUSDT
- ETHUSDT
timeframe: 1h
venue: kraken
product: perp
research_goal: 'Test a finding the trade_efficiency reader noticed after run_073 on
  idea HOURLY_SHOCK_REVERSAL_MEAN_REVERSION_1H_BTC_ETH__trade_efficiency-run_070-1:
  The shock reversal signal (period=2 smoothing, zscore-normalized 1-bar price move,
  negated for mean-reversion) has positive predictive power for price direction, as
  confirmed by residual IC of 0.077 (p=0.019). Rank correlation of the forecast with
  forward returns should be positive and consistent across windows. The negative realized
  profitability is driven by cost and execution risk, not directional error in the
  forecast itself. Its claim block is pre-filled (candidate.claim). Evidence: grid_evaluation.residual_ic.base.value:
  0.076977, p_value_one_sided: 0.01937; grid_evaluation.residual_ic.design_period_3.value:
  0.075277, p_value_one_sided: 0.021625; variants.base.slices.overall.per_trade_expectancy_bps.mean:
  -6.1015 (negative despite positive IC, confirming cost is the problem); variants.base.slices.overall.realized_edge_to_cost_ratio:
  -1.2805 (costs exceed edge)'
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
    statement: The shock reversal signal (period=2 smoothing, zscore-normalized 1-bar
      price move, negated for mean-reversion) has positive predictive power for price
      direction, as confirmed by residual IC of 0.077 (p=0.019). Rank correlation
      of the forecast with forward returns should be positive and consistent across
      windows. The negative realized profitability is driven by cost and execution
      risk, not directional error in the forecast itself.
    kind: direction_forecast
    tests:
    - name: rank_ic_shock_reversal_1bar
      selector:
        kind: all
      outcome:
        kind: fwd_return
        horizons:
        - 1
      baseline: null
      statistic: rank_ic
      direction: greater
      floor:
        min_events: 1000
        min_windows: 4
      consistency:
        unit: window
        min_same_sign: 4
    - name: rank_ic_shock_reversal_3bar
      selector:
        kind: all
      outcome:
        kind: fwd_return
        horizons:
        - 3
      baseline: null
      statistic: rank_ic
      direction: greater
      floor:
        min_events: 1000
        min_windows: 4
      consistency:
        unit: window
        min_same_sign: 4
    pass_if: Rank IC is positive and statistically significant at both 1-bar and 3-bar
      horizons, and the effect sign remains positive (same direction) in at least
      4 distinct windows. This confirms the forecast detects price reversals reliably
      and the poor profitability is due to cost structure or entry/exit slippage,
      not forecast direction error.
    fail_if: Rank IC is negative at any horizon, or the sign flips inconsistently
      across windows (e.g., positive in some windows, negative in others). This would
      indicate the forecast direction is unreliable or regime-dependent.
    rationale: The grid's residual_ic=0.077 is a measure of the forecast's information
      content. By testing rank_ic of the forecast directly against forward returns,
      we isolate whether the problem is the signal's direction (which passes this
      test) or the cost/execution structure (which a passed direction test confirms
      is the binding constraint). If rank_ic passes, the strategy's loss is not from
      wrong direction but from fees and slippage on trades held too short; the solution
      would be cost reduction or hold-minimum constraints, not signal redesign.
  criteria_from: hypothesis_generation
  source:
    origin: reader
    proposal_ref: runs/run_073/artifacts/proposals/trade_efficiency.yaml#trade_efficiency-run_073-1
    source_run: run_073
    parent_hypothesis_id: HOURLY_SHOCK_REVERSAL_MEAN_REVERSION_1H_BTC_ETH__trade_efficiency-run_070-1
    hypothesis_id: HOURLY_SHOCK_REVERSAL_MEAN_REVERSION_1H_BTC_ETH__trade_efficiency-run_070-1__trade_efficiency-run_073-1
    decision_ref: runs/run_074/artifacts/decision_record.yaml
    proposal:
      kind: side_finding
      claim:
        statement: The shock reversal signal (period=2 smoothing, zscore-normalized
          1-bar price move, negated for mean-reversion) has positive predictive power
          for price direction, as confirmed by residual IC of 0.077 (p=0.019). Rank
          correlation of the forecast with forward returns should be positive and
          consistent across windows. The negative realized profitability is driven
          by cost and execution risk, not directional error in the forecast itself.
        kind: direction_forecast
        tests:
        - name: rank_ic_shock_reversal_1bar
          selector:
            kind: all
          outcome:
            kind: fwd_return
            horizons:
            - 1
          baseline: null
          statistic: rank_ic
          direction: greater
          floor:
            min_events: 1000
            min_windows: 4
          consistency:
            unit: window
            min_same_sign: 4
        - name: rank_ic_shock_reversal_3bar
          selector:
            kind: all
          outcome:
            kind: fwd_return
            horizons:
            - 3
          baseline: null
          statistic: rank_ic
          direction: greater
          floor:
            min_events: 1000
            min_windows: 4
          consistency:
            unit: window
            min_same_sign: 4
        pass_if: Rank IC is positive and statistically significant at both 1-bar and
          3-bar horizons, and the effect sign remains positive (same direction) in
          at least 4 distinct windows. This confirms the forecast detects price reversals
          reliably and the poor profitability is due to cost structure or entry/exit
          slippage, not forecast direction error.
        fail_if: Rank IC is negative at any horizon, or the sign flips inconsistently
          across windows (e.g., positive in some windows, negative in others). This
          would indicate the forecast direction is unreliable or regime-dependent.
        rationale: The grid's residual_ic=0.077 is a measure of the forecast's information
          content. By testing rank_ic of the forecast directly against forward returns,
          we isolate whether the problem is the signal's direction (which passes this
          test) or the cost/execution structure (which a passed direction test confirms
          is the binding constraint). If rank_ic passes, the strategy's loss is not
          from wrong direction but from fees and slippage on trades held too short;
          the solution would be cost reduction or hold-minimum constraints, not signal
          redesign.
      evidence:
      - 'grid_evaluation.residual_ic.base.value: 0.076977, p_value_one_sided: 0.01937'
      - 'grid_evaluation.residual_ic.design_period_3.value: 0.075277, p_value_one_sided:
        0.021625'
      - 'variants.base.slices.overall.per_trade_expectancy_bps.mean: -6.1015 (negative
        despite positive IC, confirming cost is the problem)'
      - 'variants.base.slices.overall.realized_edge_to_cost_ratio: -1.2805 (costs
        exceed edge)'
---

# trade_efficiency-run_073-1

Written by tools/decide_next.py (E-059, slice 6b) from runs/run_073/artifacts/proposals/trade_efficiency.yaml#trade_efficiency-run_073-1; decision record: runs/run_074/artifacts/decision_record.yaml.

This brief carries no pass criteria on purpose (operator decision 2, 2026-09-24): step 1a writes a hypothesis card and criteria coherent with the proposed idea, from config/criterion_menu.yaml. A patch's resolved config passes through to 1b (candidate.config), and 5a checks it against candidate.source.expected_config_sha256.
