---
strategy_domain: short_horizon_reversal
market_universe:
- BTCUSDT
- ETHUSDT
timeframe: 1h
venue: kraken
product: perp
research_goal: 'Test a finding the component_attribution reader noticed after run_071
  on idea HOURLY_SHOCK_CONTINUATION_MOMENTUM_1H_BTC_ETH: Forecast quantile selection—the
  top 10% of rolling forecast strength—shows stronger and more consistent continuation
  than a fixed forecast threshold (>= 12), because quantile-based selection adapts
  to market volatility and component oscillation across eras. Its claim block is pre-filled
  (candidate.claim). Evidence: Component contributions by era show extreme oscillation:
  extremeness_in_range mean 2022-01 to 2023-09 ranges -0.247 to +0.544; Base claim
  effect sizes are marginal (h1 effect = 0.00020949); quantile filtering may isolate
  stronger signal in high-conviction subset; Asset variant (SOL) shows weakened signal;
  quantile selection removes lowest-conviction bars where cross-asset noise dominates;
  Window consistency is weak (4 of 6 windows claimed positive at h1); top decile may
  improve to 5 or 6 windows'
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
    statement: 'Forecast quantile selection—the top 10% of rolling forecast strength—shows
      stronger and more consistent continuation than a fixed forecast threshold (>=
      12), because quantile-based selection adapts to market volatility and component
      oscillation across eras.

      '
    kind: conditional_behaviour
    tests:
    - name: top_decile_forecast_continuation
      selector:
        kind: quantile
        field: forecast
        side: top
        q: 0.1
        lookback: 100
      outcome:
        kind: fwd_return
        horizons:
        - 1
        - 2
        - 3
        - 4
      baseline:
        kind: complement
      statistic: mean_diff
      direction: greater
      floor:
        min_events: 40
        min_windows: 3
      consistency:
        unit: window
        min_same_sign: 3
    pass_if: 'At every horizon, the top 10% of rolling forecast strength shows significantly
      higher mean returns than the complement 90%, with effect magnitude consistent
      in at least 3 of 6 windows.

      '
    fail_if: 'At any horizon, top-decile forecasts show significantly lower returns
      (reversed), contradicting the signal''s intended direction.

      '
    rationale: 'The base claim''s fixed threshold (forecast >= 12) selects ~22% of
      bars per window. Component attribution shows extremeness_in_range and move_magnitude
      both oscillate in magnitude and sign by era and asset, indicating that component
      strength varies regime-dependently. A quantile-based selector adapts to this
      variation: the top 10% automatically concentrates on the strongest-conviction
      bars in each window, filtering out marginal entries when components are weak.
      If continuation is real but masked by weak-conviction bars, isolating the top
      decile should reveal a stronger effect than the original threshold. If the signal
      is actually reversed in weak bars (mean-reversion), the top decile may show
      different behavior.

      '
  criteria_from: hypothesis_generation
  source:
    origin: reader
    proposal_ref: runs/run_071/artifacts/proposals/component_attribution.yaml#component_attribution-run_071-1
    source_run: run_071
    parent_hypothesis_id: HOURLY_SHOCK_CONTINUATION_MOMENTUM_1H_BTC_ETH
    hypothesis_id: HOURLY_SHOCK_CONTINUATION_MOMENTUM_1H_BTC_ETH__component_attribution-run_071-1
    decision_ref: runs/run_071/artifacts/decision_record.yaml
    proposal:
      kind: side_finding
      claim:
        statement: 'Forecast quantile selection—the top 10% of rolling forecast strength—shows
          stronger and more consistent continuation than a fixed forecast threshold
          (>= 12), because quantile-based selection adapts to market volatility and
          component oscillation across eras.

          '
        kind: conditional_behaviour
        tests:
        - name: top_decile_forecast_continuation
          selector:
            kind: quantile
            field: forecast
            side: top
            q: 0.1
            lookback: 100
          outcome:
            kind: fwd_return
            horizons:
            - 1
            - 2
            - 3
            - 4
          baseline:
            kind: complement
          statistic: mean_diff
          direction: greater
          floor:
            min_events: 40
            min_windows: 3
          consistency:
            unit: window
            min_same_sign: 3
        pass_if: 'At every horizon, the top 10% of rolling forecast strength shows
          significantly higher mean returns than the complement 90%, with effect magnitude
          consistent in at least 3 of 6 windows.

          '
        fail_if: 'At any horizon, top-decile forecasts show significantly lower returns
          (reversed), contradicting the signal''s intended direction.

          '
        rationale: 'The base claim''s fixed threshold (forecast >= 12) selects ~22%
          of bars per window. Component attribution shows extremeness_in_range and
          move_magnitude both oscillate in magnitude and sign by era and asset, indicating
          that component strength varies regime-dependently. A quantile-based selector
          adapts to this variation: the top 10% automatically concentrates on the
          strongest-conviction bars in each window, filtering out marginal entries
          when components are weak. If continuation is real but masked by weak-conviction
          bars, isolating the top decile should reveal a stronger effect than the
          original threshold. If the signal is actually reversed in weak bars (mean-reversion),
          the top decile may show different behavior.

          '
      evidence:
      - 'Component contributions by era show extreme oscillation: extremeness_in_range
        mean 2022-01 to 2023-09 ranges -0.247 to +0.544'
      - Base claim effect sizes are marginal (h1 effect = 0.00020949); quantile filtering
        may isolate stronger signal in high-conviction subset
      - Asset variant (SOL) shows weakened signal; quantile selection removes lowest-conviction
        bars where cross-asset noise dominates
      - Window consistency is weak (4 of 6 windows claimed positive at h1); top decile
        may improve to 5 or 6 windows
---

# component_attribution-run_071-1

Written by tools/decide_next.py (E-059, slice 6b) from runs/run_071/artifacts/proposals/component_attribution.yaml#component_attribution-run_071-1; decision record: runs/run_071/artifacts/decision_record.yaml.

This brief carries no pass criteria on purpose (operator decision 2, 2026-09-24): step 1a writes a hypothesis card and criteria coherent with the proposed idea, from config/criterion_menu.yaml. A patch's resolved config passes through to 1b (candidate.config), and 5a checks it against candidate.source.expected_config_sha256.
