---
strategy_domain: short_horizon_reversal
market_universe:
- BTCUSDT
- ETHUSDT
timeframe: 1h
venue: kraken
product: perp
research_goal: 'Test a finding the forecast_power reader noticed after run_078 on
  idea HOURLY_SHOCK_CONTINUATION_MOMENTUM_1H_BTC_ETH__trade_efficiency-run_071-4:
  In this strategy, after a bar whose one-bar move is in the top 20% of its trailing
  500 bars, the forecast''s rank correlation with the next 24 bars'' return is below
  zero: a higher forecast goes with a lower return, in most windows. Its claim block
  is pre-filled (candidate.claim). Evidence: q7:horizons.24.effect=-0.080438177; q7:horizons.24.windows_claimed_sign=6;
  q7:horizons.24.n_events=2724; q8:horizons.24.effect=-0.080320161 It backtests on
  fold C (2018-01, 2018-09, 2019-05, 2020-01, 2020-09, 2021-05; config/folds.yaml),
  the next fold its lineage (run_078, run_071) has not used. It starts from run_078''s
  base config (candidate.start_config) -- the block the claim is about.'
machine_constraints:
  protocol:
    symbols:
    - BTCUSDT
    - ETHUSDT
    timeframe: 1h
    start: '2018-01-01'
    end: '2021-08-31'
    window_months: 4
    fold: C
candidate:
  claim:
    statement: 'In this strategy, after a bar whose one-bar move is in the top 20%
      of its trailing 500 bars, the forecast''s rank correlation with the next 24
      bars'' return is below zero: a higher forecast goes with a lower return, in
      most windows.

      '
    kind: execution_behaviour
    tests:
    - name: forecast_reverses_after_large_rise_24
      selector:
        kind: quantile
        field: past_return
        bars: 1
        side: top
        q: 0.2
        lookback: 500
      outcome:
        kind: fwd_return
        horizons:
        - 1
        - 4
        - 24
      baseline: null
      statistic: rank_ic
      direction: less
      floor:
        min_events: 100
        min_windows: 4
    pass_if: 'At 24 bars the rank correlation is below zero (direction less holds)
      in most windows, with at least 100 events, on the unseen fold.

      '
    fail_if: 'At 24 bars the rank correlation is above zero in most windows, or the
      24-bar effect has the opposite sign to the claim.

      '
    rationale: 'The forecast is built from a one-bar move-magnitude component and
      a 20-bar range-extremeness component, so it is large after large moves. After
      a large one-bar move, whichever way it went, the forecast ranks forward returns
      negatively over a day, which is the reversal the strategy''s own lots then give
      back. The same result on the bottom side argues this is about move size, not
      direction. This run''s bars cover BTCUSD only, so a coin effect is not ruled
      out here.

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
          - id: move_magnitude
            class: strategies.strategy_components.PriceEvolutionComponent
            params:
              period: 1
              scaling_factor: 10.0
            weight: 1.0
            lookback: 500
            transforms:
            - op: ratio_to_mean
            - op: scale
              params:
                factor: 10.0
          - id: extremeness_in_range
            class: strategies.strategy_components.DonchianBreakoutComponent
            params:
              period: 20
              scaling_factor: 10.0
            weight: 1.0
            lookback: 500
            transforms:
            - op: ratio_to_mean
            - op: scale
              params:
                factor: 10.0
        trending: null
        mean_reversion: null
        chop: null
  start_manifest:
    block:
      kind: forecast
      config_paths:
      - /strategies/regimes/unknown/components/0
      - /strategies/regimes/unknown/components/1
    scaffolding:
    - /regime_detector
    rationale: 'The PriceEvolutionComponent(period=1) and DonchianBreakoutComponent(period=20),
      normalized via ratio_to_mean and scaled by 10 each, form the hypothesis block—jointly
      measuring continuation strength via 1-bar move magnitude and close position
      in recent range. The ungated regime_detector is scaffolding: it routes every
      bar to the ''unknown'' regime unconditionally, allowing the signal to activate
      on all bars. The claim stratifies these entries post-execution by forecast magnitude
      (>= 10 vs. < 10 as entry_forecast field) to test whether high-magnitude confluence
      points produce superior trade returns.'
  criteria_from: hypothesis_generation
  source:
    origin: reader
    proposal_ref: runs/run_078/artifacts/proposals/forecast_power.yaml#forecast_power-run_078-1
    source_run: run_078
    parent_hypothesis_id: HOURLY_SHOCK_CONTINUATION_MOMENTUM_1H_BTC_ETH__trade_efficiency-run_071-4
    hypothesis_id: HOURLY_SHOCK_CONTINUATION_MOMENTUM_1H_BTC_ETH__trade_efficiency-run_071-4__forecast_power-run_078-1
    decision_ref: runs/run_083/artifacts/decision_record.yaml
    proposal:
      kind: side_finding
      claim:
        statement: 'In this strategy, after a bar whose one-bar move is in the top
          20% of its trailing 500 bars, the forecast''s rank correlation with the
          next 24 bars'' return is below zero: a higher forecast goes with a lower
          return, in most windows.

          '
        kind: execution_behaviour
        tests:
        - name: forecast_reverses_after_large_rise_24
          selector:
            kind: quantile
            field: past_return
            bars: 1
            side: top
            q: 0.2
            lookback: 500
          outcome:
            kind: fwd_return
            horizons:
            - 1
            - 4
            - 24
          baseline: null
          statistic: rank_ic
          direction: less
          floor:
            min_events: 100
            min_windows: 4
        pass_if: 'At 24 bars the rank correlation is below zero (direction less holds)
          in most windows, with at least 100 events, on the unseen fold.

          '
        fail_if: 'At 24 bars the rank correlation is above zero in most windows, or
          the 24-bar effect has the opposite sign to the claim.

          '
        rationale: 'The forecast is built from a one-bar move-magnitude component
          and a 20-bar range-extremeness component, so it is large after large moves.
          After a large one-bar move, whichever way it went, the forecast ranks forward
          returns negatively over a day, which is the reversal the strategy''s own
          lots then give back. The same result on the bottom side argues this is about
          move size, not direction. This run''s bars cover BTCUSD only, so a coin
          effect is not ruled out here.

          '
      evidence:
      - q7:horizons.24.effect=-0.080438177
      - q7:horizons.24.windows_claimed_sign=6
      - q7:horizons.24.n_events=2724
      - q8:horizons.24.effect=-0.080320161
      config_change: []
      vehicle: []
      combines_as: knowledge_only
      fold_observed: B
    base_config_ref: runs/run_078/artifacts/variants/base/strategy_config.json
    start_config_sha256: 6cf77f4eef76884229ac1d4f72473a81329c50d0c15cb17df4effadf1cc27e98
---

# forecast_power-run_078-1

Written by tools/decide_next.py (E-059, slice 6b) from runs/run_078/artifacts/proposals/forecast_power.yaml#forecast_power-run_078-1; decision record: runs/run_083/artifacts/decision_record.yaml.

This brief carries no pass criteria on purpose (operator decision 2, 2026-09-24): step 1a writes a hypothesis card and criteria coherent with the proposed idea, from config/criterion_menu.yaml. A patch's resolved config passes through to 1b (candidate.config), and 5a checks it against candidate.source.expected_config_sha256.
