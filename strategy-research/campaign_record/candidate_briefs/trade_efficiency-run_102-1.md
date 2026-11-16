---
strategy_domain: SMA trend
market_universe:
- BTCUSDT
timeframe: 1h
venue: kraken
product: perp
research_goal: 'Test a finding the trade_efficiency reader noticed after run_102 on
  idea SMA_PULLBACK_IN_TREND_24H_1H_BTC_FOLD_A__trade_efficiency-run_101-1: On this
  strategy, when the negated standardised distance of the close from its 24-bar SMA
  (the stretch_from_short_sma sub-forecast) is at or below -8, which means the price
  sits far above its 24-bar mean, BTC''s 24-bar forward return is lower than on the
  other bars. Its claim block is pre-filled (candidate.claim). Evidence: q15:horizons.24.effect=-0.00154630790;
  q15:horizons.24.windows_claimed_sign=6; q15:horizons.24.n_events=3741; q14:horizons.24.windows_claimed_sign=6;
  q11:horizons.24.windows_claimed_sign=1 It backtests on fold D (2024-01, 2024-05,
  2024-09, 2025-01, 2025-05, 2025-09; config/folds.yaml), drawn among the folds its
  source run run_102 is not on (A, C, D). It starts from run_102''s base config (candidate.start_config)
  with the finding''s config change: /strategies/regimes/unknown/components/1/weight
  -> 1.0; -- the block the claim is about.'
machine_constraints:
  protocol:
    symbols:
    - BTCUSDT
    timeframe: 1h
    start: '2024-01-01'
    end: '2025-12-31'
    window_months: 4
    fold: D
evaluation:
  pass_rule:
    criteria:
    - id: forecast_ic_median
      horizon: 24
candidate:
  claim:
    statement: 'On this strategy, when the negated standardised distance of the close
      from its 24-bar SMA (the stretch_from_short_sma sub-forecast) is at or below
      -8, which means the price sits far above its 24-bar mean, BTC''s 24-bar forward
      return is lower than on the other bars.

      '
    kind: conditional_behaviour
    tests:
    - name: stretched_up_bars_fall_over_a_day
      selector:
        kind: event
        field: forecast
        op: <=
        value: -8
      outcome:
        kind: fwd_return
        horizons:
        - 24
      baseline:
        kind: complement
      statistic: mean_diff
      direction: less
      floor:
        min_events: 100
        min_windows: 4
      signal: debug_info.components.stretch_from_short_sma.post_pipeline_value
    pass_if: 'On the unseen fold, bars where the stretch sub-forecast is at or below
      -8 have a lower mean 24-bar forward return than the other bars, in at least
      <n> windows, with at least 100 such bars.

      '
    fail_if: 'The mean 24-bar forward return of those bars is higher than or equal
      to the other bars'', or the claimed sign appears in fewer than 4 windows.

      '
    rationale: 'This is a tail-conditional test on part of the bars, not a rank IC
      over all bars. The stretch leg is positive in the window count at the 24-bar
      horizon (q14), and the extreme-negative tail carries the same sign in 6 of 6
      windows (q15). The mirror tail, at or above <n>, is weaker: 4 of 6 windows at
      24 bars (q13). At 6 bars the tail effect is not with the claim (q12), so the
      horizon is restricted to 24, about a day. Mechanism: a close far above its 24-bar
      mean has over-extended in the short term and gives part of the move back over
      about a day. The trend_spread leg shows no such ranking (q11) and still drives
      most of the forecast under the base weights. Raising the stretch weight lets
      this reversal information move the forecast more. The earlier claim trade_efficiency-run_101-1
      said the slow trend leg carries the persistent part. It was not confirmed on
      this fold, and this claim differs from it: the persistence sits in the reversal
      leg''s upward-stretch tail. The market''s drift sits in both groups because
      the baseline is the complement.

      '
  start_config:
    regime_detector:
      mode: threshold_rules
      components: []
      rules: []
      default_regime: unknown
    strategies:
      regimes:
        unknown:
          components:
          - id: trend_spread
            class: strategies.strategy_components.EMASpreadComponent
            params:
              fast_period: 24
              slow_period: 168
              average: sma
            weight: 1.0
            transforms:
            - op: standardise
              params:
                window: 500
                min_periods: 120
          - id: stretch_from_short_sma
            class: strategies.strategy_components.MovingAverageDistanceComponent
            params:
              period: 24
              average: sma
            weight: 1.0
            transforms:
            - op: standardise
              params:
                window: 500
                min_periods: 120
            - op: negate
        trending: null
        mean_reversion: null
        chop: null
      sizing:
        kind: vol_target
        window: 60
        target_annual_vol: 0.2
        periods_per_year: 8760
        max_allocation: 2
  start_manifest:
    block:
      kind: forecast
      config_paths:
      - /strategies/regimes/unknown/components/0
      - /strategies/regimes/unknown/components/1
    scaffolding:
    - /regime_detector
    - /strategies/sizing
    rationale: Component 0 is the SMA24/SMA168 trend leg and component 1 is the negated
      SMA24-distance stretch leg at weight 0.25, which together are the block the
      claim is about. The ungated detector and the vol-target sizing block only run
      and size it.
  source:
    origin: reader
    proposal_ref: runs/run_102/artifacts/proposals/trade_efficiency.yaml#trade_efficiency-run_102-1
    source_run: run_102
    parent_hypothesis_id: SMA_PULLBACK_IN_TREND_24H_1H_BTC_FOLD_A__trade_efficiency-run_101-1
    hypothesis_id: SMA_PULLBACK_IN_TREND_24H_1H_BTC_FOLD_A__trade_efficiency-run_101-1__trade_efficiency-run_102-1
    decision_ref: runs/run_102/artifacts/decision_record.yaml
    proposal:
      kind: side_finding
      claim:
        statement: 'On this strategy, when the negated standardised distance of the
          close from its 24-bar SMA (the stretch_from_short_sma sub-forecast) is at
          or below -8, which means the price sits far above its 24-bar mean, BTC''s
          24-bar forward return is lower than on the other bars.

          '
        kind: conditional_behaviour
        tests:
        - name: stretched_up_bars_fall_over_a_day
          selector:
            kind: event
            field: forecast
            op: <=
            value: -8
          outcome:
            kind: fwd_return
            horizons:
            - 24
          baseline:
            kind: complement
          statistic: mean_diff
          direction: less
          floor:
            min_events: 100
            min_windows: 4
          signal: debug_info.components.stretch_from_short_sma.post_pipeline_value
        pass_if: 'On the unseen fold, bars where the stretch sub-forecast is at or
          below -8 have a lower mean 24-bar forward return than the other bars, in
          at least <n> windows, with at least 100 such bars.

          '
        fail_if: 'The mean 24-bar forward return of those bars is higher than or equal
          to the other bars'', or the claimed sign appears in fewer than 4 windows.

          '
        rationale: 'This is a tail-conditional test on part of the bars, not a rank
          IC over all bars. The stretch leg is positive in the window count at the
          24-bar horizon (q14), and the extreme-negative tail carries the same sign
          in 6 of 6 windows (q15). The mirror tail, at or above <n>, is weaker: 4
          of 6 windows at 24 bars (q13). At 6 bars the tail effect is not with the
          claim (q12), so the horizon is restricted to 24, about a day. Mechanism:
          a close far above its 24-bar mean has over-extended in the short term and
          gives part of the move back over about a day. The trend_spread leg shows
          no such ranking (q11) and still drives most of the forecast under the base
          weights. Raising the stretch weight lets this reversal information move
          the forecast more. The earlier claim trade_efficiency-run_101-1 said the
          slow trend leg carries the persistent part. It was not confirmed on this
          fold, and this claim differs from it: the persistence sits in the reversal
          leg''s upward-stretch tail. The market''s drift sits in both groups because
          the baseline is the complement.

          '
      evidence:
      - q15:horizons.24.effect=-0.00154630790
      - q15:horizons.24.windows_claimed_sign=6
      - q15:horizons.24.n_events=3741
      - q14:horizons.24.windows_claimed_sign=6
      - q11:horizons.24.windows_claimed_sign=1
      config_change:
      - component_id: stretch_from_short_sma
        field: weight
        before: 0.25
        after: 1.0
      vehicle:
      - component_id: stretch_from_short_sma
        field: weight
        before: 0.25
        after: 1.0
      combines_as: forecast_block
      fold_observed: B
    base_config_ref: runs/run_102/artifacts/variants/base/strategy_config.json
    start_config_sha256: b45d1013d9eabd228bdf3e1eb80917ef5c8651bdb64f72dcdd645f1fc1702b18
    config_change_ops:
    - path: /strategies/regimes/unknown/components/1/weight
      value: 1.0
---

# trade_efficiency-run_102-1

Written by tools/decide_next.py (E-059, slice 6b) from runs/run_102/artifacts/proposals/trade_efficiency.yaml#trade_efficiency-run_102-1; decision record: runs/run_102/artifacts/decision_record.yaml.

This fold child keeps its source run's criteria (D-121): evaluation.pass_rule, re-resolved against config/criterion_menu.yaml when the run is registered. A patch's resolved config passes through to 1b (candidate.config), and 5a checks it against candidate.source.expected_config_sha256.
