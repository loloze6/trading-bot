---
strategy_domain: SMA trend
market_universe:
- BTCUSDT
timeframe: 1h
venue: kraken
product: perp
research_goal: 'Test a finding the forecast_power reader noticed after run_102 on
  idea SMA_PULLBACK_IN_TREND_24H_1H_BTC_FOLD_A__trade_efficiency-run_101-1: Unlike
  the earlier claim trade_efficiency-run_101-1 (the slow trend leg carries the forecast;
  not confirmed on fold B), the negated 24-bar stretch leg, not the slow trend leg,
  carries the rank information: where its standardised value is at least 5 in size,
  it ranks BTC''s next 6 and 24 hour returns positively (a higher value is followed
  by a higher return), because 24-hour returns on fold B revert after a move away
  from the 24-bar average. The base forecast gives the trend leg weight 1.0 against
  0.25, which swamps this leg. Its claim block is pre-filled (candidate.claim). Evidence:
  q9:horizons.6.effect=0.0308; q9:horizons.24.effect=0.0851; q9:horizons.6.n_events=10166;
  q9:horizons.24.n_events=10108 It backtests on fold C (2018-01, 2018-09, 2019-05,
  2020-01, 2020-09, 2021-05; config/folds.yaml), drawn among the folds its source
  run run_102 is not on (A, C, D). It starts from run_102''s base config (candidate.start_config)
  with the finding''s config change: /strategies/regimes/unknown/components/0/weight
  -> 0.25; /strategies/regimes/unknown/components/1/weight -> 1.0; -- the block the
  claim is about.'
machine_constraints:
  protocol:
    symbols:
    - BTCUSDT
    timeframe: 1h
    start: '2018-01-01'
    end: '2021-08-31'
    window_months: 4
    fold: C
evaluation:
  pass_rule:
    criteria:
    - id: forecast_ic_median
      horizon: 24
candidate:
  claim:
    statement: 'Unlike the earlier claim trade_efficiency-run_101-1 (the slow trend
      leg carries the forecast; not confirmed on fold B), the negated 24-bar stretch
      leg, not the slow trend leg, carries the rank information: where its standardised
      value is at least 5 in size, it ranks BTC''s next 6 and 24 hour returns positively
      (a higher value is followed by a higher return), because 24-hour returns on
      fold B revert after a move away from the 24-bar average. The base forecast gives
      the trend leg weight 1.0 against 0.25, which swamps this leg.

      '
    kind: conditional_behaviour
    tests:
    - name: stretch_leg_ranks_forward_returns
      selector:
        kind: event
        field: abs_forecast
        op: '>='
        value: 5
      outcome:
        kind: fwd_return
        horizons:
        - 6
        - 24
      baseline: null
      statistic: rank_ic
      direction: greater
      signal: debug_info.components.stretch_from_short_sma.post_pipeline_value
      floor:
        min_events: 100
        min_windows: 4
    pass_if: 'On the unseen fold the rank IC of the stretch leg''s post-pipeline value
      with the forward return is positive at horizons 6 and 24 on bars where its size
      is at least 5, in at least 4 windows at each horizon, with at least 100 events.

      '
    fail_if: 'The rank IC is zero or negative at either horizon, or points the claimed
      way in fewer than 4 windows. That would show the reversal edge of this fold
      B run is specific to it.

      '
    rationale: 'On this run''s bars the stretch leg has a positive rank IC at 6 and
      24 hours in all 6 windows (q5), and the trend leg has a negative one at 6 hours
      in 5 of 6 windows (q4). The 24-hour SMA24/SMA168 spread is high after a rally,
      and a rally is followed by lower 24-hour returns, so the trend leg shares the
      stretch leg''s reversal reading with the opposite sign. The base mix puts weight
      1.0 on the trend leg and 0.25 on the stretch leg, so the forecast is dominated
      by the leg that ranks the wrong way (grid IC -0.008353). Swapping the weights
      makes the reversal leg dominate. The mechanism predicts a second query on another
      selector: the bottom quintile of the stretch leg should be followed by lower
      24-hour returns than other bars (q10). It is lower in 5 of 6 windows. The test
      reads the stretch leg''s own output, which the weight change leaves unchanged,
      so a confirmation says the leg ranks returns, and the child run''s grid IC says
      whether the swapped mix uses it.

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
            weight: 0.25
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
    proposal_ref: runs/run_102/artifacts/proposals/forecast_power.yaml#forecast_power-run_102-2
    source_run: run_102
    parent_hypothesis_id: SMA_PULLBACK_IN_TREND_24H_1H_BTC_FOLD_A__trade_efficiency-run_101-1
    hypothesis_id: SMA_PULLBACK_IN_TREND_24H_1H_BTC_FOLD_A__trade_efficiency-run_101-1__forecast_power-run_102-2
    decision_ref: runs/run_102/artifacts/decision_record.yaml
    proposal:
      kind: side_finding
      claim:
        statement: 'Unlike the earlier claim trade_efficiency-run_101-1 (the slow
          trend leg carries the forecast; not confirmed on fold B), the negated 24-bar
          stretch leg, not the slow trend leg, carries the rank information: where
          its standardised value is at least 5 in size, it ranks BTC''s next 6 and
          24 hour returns positively (a higher value is followed by a higher return),
          because 24-hour returns on fold B revert after a move away from the 24-bar
          average. The base forecast gives the trend leg weight 1.0 against 0.25,
          which swamps this leg.

          '
        kind: conditional_behaviour
        tests:
        - name: stretch_leg_ranks_forward_returns
          selector:
            kind: event
            field: abs_forecast
            op: '>='
            value: 5
          outcome:
            kind: fwd_return
            horizons:
            - 6
            - 24
          baseline: null
          statistic: rank_ic
          direction: greater
          signal: debug_info.components.stretch_from_short_sma.post_pipeline_value
          floor:
            min_events: 100
            min_windows: 4
        pass_if: 'On the unseen fold the rank IC of the stretch leg''s post-pipeline
          value with the forward return is positive at horizons 6 and 24 on bars where
          its size is at least 5, in at least 4 windows at each horizon, with at least
          100 events.

          '
        fail_if: 'The rank IC is zero or negative at either horizon, or points the
          claimed way in fewer than 4 windows. That would show the reversal edge of
          this fold B run is specific to it.

          '
        rationale: 'On this run''s bars the stretch leg has a positive rank IC at
          6 and 24 hours in all 6 windows (q5), and the trend leg has a negative one
          at 6 hours in 5 of 6 windows (q4). The 24-hour SMA24/SMA168 spread is high
          after a rally, and a rally is followed by lower 24-hour returns, so the
          trend leg shares the stretch leg''s reversal reading with the opposite sign.
          The base mix puts weight 1.0 on the trend leg and 0.25 on the stretch leg,
          so the forecast is dominated by the leg that ranks the wrong way (grid IC
          -0.008353). Swapping the weights makes the reversal leg dominate. The mechanism
          predicts a second query on another selector: the bottom quintile of the
          stretch leg should be followed by lower 24-hour returns than other bars
          (q10). It is lower in 5 of 6 windows. The test reads the stretch leg''s
          own output, which the weight change leaves unchanged, so a confirmation
          says the leg ranks returns, and the child run''s grid IC says whether the
          swapped mix uses it.

          '
      evidence:
      - q9:horizons.6.effect=0.0308
      - q9:horizons.24.effect=0.0851
      - q9:horizons.6.n_events=10166
      - q9:horizons.24.n_events=10108
      config_change:
      - component_id: trend_spread
        field: weight
        before: 1.0
        after: 0.25
      - component_id: stretch_from_short_sma
        field: weight
        before: 0.25
        after: 1.0
      vehicle:
      - component_id: trend_spread
        field: weight
        before: 1.0
        after: 0.25
      - component_id: stretch_from_short_sma
        field: weight
        before: 0.25
        after: 1.0
      combines_as: forecast_block
      fold_observed: B
    base_config_ref: runs/run_102/artifacts/variants/base/strategy_config.json
    start_config_sha256: 494ccb51e195eb2c008fa9c87597ed06d724c38f2dd52a9dce85f25ed441552f
    config_change_ops:
    - path: /strategies/regimes/unknown/components/0/weight
      value: 0.25
    - path: /strategies/regimes/unknown/components/1/weight
      value: 1.0
  source_observations:
  - statement: 'The trend leg''s rank IC with forward returns is negative at 6 and
      24 hours over all bars, with the claimed positive sign in only 1 of 6 windows
      at each horizon.

      '
    variant: base
    measured:
      function: conditional_effect
      params:
        baseline: null
        by: window
        condition:
          kind: all
        direction: greater
        horizons:
        - 6
        - 24
        outcome: fwd_return
        signal: debug_info.components.trend_spread.post_pipeline_value
        statistic: rank_ic
        variant: base
      statistic: rank_ic
      spec_hash: 9294f3a8751fd5666dc563994a555abf1b4c2ffc836a47fdf2c42d8bad2d4325
      selector:
        kind: all
      outcome:
        kind: fwd_return
        horizons:
        - 6
        - 24
      baseline: null
      direction: greater
      floor:
        min_events: 1
      signal: debug_info.components.trend_spread.post_pipeline_value
    floors_met: true
  - statement: 'The stretch leg''s rank IC over all bars is positive at 6 and 24 hours
      in 6 of 6 windows at each horizon. This is a component-level test on all bars,
      so it is not itself a claim test.

      '
    variant: base
    measured:
      function: conditional_effect
      params:
        baseline: null
        by: window
        condition:
          kind: all
        direction: greater
        horizons:
        - 6
        - 24
        outcome: fwd_return
        signal: debug_info.components.stretch_from_short_sma.post_pipeline_value
        statistic: rank_ic
        variant: base
      statistic: rank_ic
      spec_hash: 52dc10dbb0dfad1eb5207462d2fc58eea9cc51f2fb0c3e925284fd71b4254b34
      selector:
        kind: all
      outcome:
        kind: fwd_return
        horizons:
        - 6
        - 24
      baseline: null
      direction: greater
      floor:
        min_events: 1
      signal: debug_info.components.stretch_from_short_sma.post_pipeline_value
    floors_met: true
  - statement: 'The top quintile of the stretch leg shows higher 24-hour returns than
      the other bars in 4 of 6 windows and lower 6-hour returns in all 6 windows.
      This is weaker than its rank IC and does not clear a 4-window agreement at 6
      hours.

      '
    variant: base
    measured:
      function: conditional_effect
      params:
        baseline:
          kind: complement
        by: null
        condition:
          field: forecast
          kind: quantile
          lookback: 500
          q: 0.2
          side: top
        direction: greater
        floor:
          min_events: 100
          min_windows: 4
        horizons:
        - 6
        - 24
        outcome: fwd_return
        signal: debug_info.components.stretch_from_short_sma.post_pipeline_value
        statistic: mean_diff
        variant: base
      statistic: mean_diff
      spec_hash: 0e2e3d1bc127817598ca9b883102070a28e84b98b42d06f4fb6ea297da003c03
      selector:
        kind: quantile
        field: forecast
        side: top
        q: 0.2
        lookback: 500
      outcome:
        kind: fwd_return
        horizons:
        - 6
        - 24
      baseline:
        kind: complement
      direction: greater
      floor:
        min_events: 100
        min_windows: 4
      signal: debug_info.components.stretch_from_short_sma.post_pipeline_value
    floors_met: true
  - statement: 'The bottom quintile of the stretch leg shows lower 24-hour returns
      than the other bars in 5 of 6 windows, and only 3 of 6 at 6 hours.

      '
    variant: base
    measured:
      function: conditional_effect
      params:
        baseline:
          kind: complement
        by: null
        condition:
          field: forecast
          kind: quantile
          lookback: 500
          q: 0.2
          side: bottom
        direction: less
        floor:
          min_events: 100
          min_windows: 4
        horizons:
        - 6
        - 24
        outcome: fwd_return
        signal: debug_info.components.stretch_from_short_sma.post_pipeline_value
        statistic: mean_diff
        variant: base
      statistic: mean_diff
      spec_hash: 0436f56df80dae581771cab285a2204fe961e486ab7e0965893db90826e79f21
      selector:
        kind: quantile
        field: forecast
        side: bottom
        q: 0.2
        lookback: 500
      outcome:
        kind: fwd_return
        horizons:
        - 6
        - 24
      baseline:
        kind: complement
      direction: less
      floor:
        min_events: 100
        min_windows: 4
      signal: debug_info.components.stretch_from_short_sma.post_pipeline_value
    floors_met: true
  - statement: 'Bars in the bottom quintile of the 24-hour past return show higher
      24-hour forward returns in 4 of 6 windows, with an opposite sign at 6 hours.

      '
    variant: base
    measured:
      function: conditional_effect
      params:
        baseline:
          kind: complement
        by: null
        condition:
          bars: 24
          field: past_return
          kind: quantile
          lookback: 500
          q: 0.2
          side: bottom
        direction: greater
        floor:
          min_events: 100
          min_windows: 4
        horizons:
        - 6
        - 24
        outcome: fwd_return
        statistic: mean_diff
        variant: base
      statistic: mean_diff
      spec_hash: 7a9da714c9432c88e1c5eefca97522a1f0bc1aebaa0ea165d7186ae720510fd5
      selector:
        kind: quantile
        field: past_return
        bars: 24
        side: bottom
        q: 0.2
        lookback: 500
      outcome:
        kind: fwd_return
        horizons:
        - 6
        - 24
      baseline:
        kind: complement
      direction: greater
      floor:
        min_events: 100
        min_windows: 4
    floors_met: true
  - statement: 'The top quintile of the trend leg shows lower forward returns than
      the other bars in only 3 of 6 windows at both horizons, so the trend leg''s
      negative edge is not robust.

      '
    variant: base
    measured:
      function: conditional_effect
      params:
        baseline:
          kind: complement
        by: null
        condition:
          field: forecast
          kind: quantile
          lookback: 500
          q: 0.2
          side: top
        direction: less
        floor:
          min_events: 100
          min_windows: 4
        horizons:
        - 6
        - 24
        outcome: fwd_return
        signal: debug_info.components.trend_spread.post_pipeline_value
        statistic: mean_diff
        variant: base
      statistic: mean_diff
      spec_hash: 011c0dfc983a7a0d31592743c2de8ae8854bf4e94eb608c5b2b2b27e1cab3d17
      selector:
        kind: quantile
        field: forecast
        side: top
        q: 0.2
        lookback: 500
      outcome:
        kind: fwd_return
        horizons:
        - 6
        - 24
      baseline:
        kind: complement
      direction: less
      floor:
        min_events: 100
        min_windows: 4
      signal: debug_info.components.trend_spread.post_pipeline_value
    floors_met: true
  - statement: 'Not reported by the model: query q11 (conditional_effect) cleared
      its own floor; what it measured is in `measured`.'
    variant: base
    measured:
      function: conditional_effect
      params:
        baseline: null
        by: null
        condition:
          field: abs_forecast
          kind: event
          op: '>='
          value: 5
        direction: less
        floor:
          min_events: 100
          min_windows: 4
        horizons:
        - 6
        - 24
        outcome: fwd_return
        signal: debug_info.components.trend_spread.post_pipeline_value
        statistic: rank_ic
        variant: base
      statistic: rank_ic
      spec_hash: 645c8c1e75cadf178a666fd2793191cf5dc2571a4dc6d13bcbbd6511a58c29df
      selector:
        kind: event
        field: abs_forecast
        op: '>='
        value: 5
      outcome:
        kind: fwd_return
        horizons:
        - 6
        - 24
      baseline: null
      direction: less
      floor:
        min_events: 100
        min_windows: 4
      signal: debug_info.components.trend_spread.post_pipeline_value
    floors_met: true
  - statement: 'The slow trend leg (SMA24/SMA168 spread) has a negative rank IC with
      forward returns at 6 and 24 bars, in 5 of 6 windows. This is the opposite of
      the card''s premise.

      '
    variant: base
    measured:
      function: conditional_effect
      params:
        baseline: null
        by: null
        condition:
          kind: all
        direction: less
        floor:
          min_events: 100
          min_windows: 4
        horizons:
        - 6
        - 24
        outcome: fwd_return
        signal: debug_info.components.trend_spread.post_pipeline_value
        statistic: rank_ic
        variant: base
      statistic: rank_ic
      spec_hash: 02da5ff62c8ae659f88a5179d63db8caa55f6ad97dc5fa125a2276256e5a2dd1
      selector:
        kind: all
      outcome:
        kind: fwd_return
        horizons:
        - 6
        - 24
      baseline: null
      direction: less
      floor:
        min_events: 100
        min_windows: 4
      signal: debug_info.components.trend_spread.post_pipeline_value
    floors_met: true
  - statement: 'Bars whose past 24-hour return is in the bottom 20% of the trailing
      500 bars show a higher 24-bar forward return than other bars, but the effect
      points the claimed way in only 4 of 6 windows. At 6 bars it points the other
      way (3 of 6 windows).

      '
    variant: base
    measured:
      function: conditional_effect
      params:
        baseline:
          kind: complement
        by: null
        condition:
          bars: 24
          field: past_return
          kind: quantile
          lookback: 500
          q: 0.2
          side: bottom
        direction: greater
        floor:
          min_events: 100
          min_windows: 4
        horizons:
        - 6
        - 24
        outcome: fwd_return
        statistic: mean_diff
        variant: base
      statistic: mean_diff
      spec_hash: 7a9da714c9432c88e1c5eefca97522a1f0bc1aebaa0ea165d7186ae720510fd5
      selector:
        kind: quantile
        field: past_return
        bars: 24
        side: bottom
        q: 0.2
        lookback: 500
      outcome:
        kind: fwd_return
        horizons:
        - 6
        - 24
      baseline:
        kind: complement
      direction: greater
      floor:
        min_events: 100
        min_windows: 4
    floors_met: true
  - statement: 'Not reported by the model: query q5 (conditional_effect) cleared its
      own floor; what it measured is in `measured`.'
    variant: base
    measured:
      function: conditional_effect
      params:
        baseline: null
        by: null
        condition:
          kind: all
        direction: greater
        floor:
          min_events: 100
          min_windows: 4
        horizons:
        - 6
        - 24
        outcome: fwd_return
        signal: debug_info.components.trend_spread.post_pipeline_value
        statistic: rank_ic
        variant: base
      statistic: rank_ic
      spec_hash: d12fdd53b8201bb80f63f341485d02be0a01a77f3a15f688e805df2c85d02a8c
      selector:
        kind: all
      outcome:
        kind: fwd_return
        horizons:
        - 6
        - 24
      baseline: null
      direction: greater
      floor:
        min_events: 100
        min_windows: 4
      signal: debug_info.components.trend_spread.post_pipeline_value
    floors_met: true
---

# forecast_power-run_102-2

Written by tools/decide_next.py (E-059, slice 6b) from runs/run_102/artifacts/proposals/forecast_power.yaml#forecast_power-run_102-2; decision record: runs/run_102/artifacts/decision_record.yaml.

This fold child keeps its source run's criteria (D-121): evaluation.pass_rule, re-resolved against config/criterion_menu.yaml when the run is registered. A patch's resolved config passes through to 1b (candidate.config), and 5a checks it against candidate.source.expected_config_sha256.
