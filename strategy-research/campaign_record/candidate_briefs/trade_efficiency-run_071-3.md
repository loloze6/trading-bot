---
strategy_domain: short_horizon_reversal
market_universe:
- BTCUSDT
- ETHUSDT
timeframe: 1h
venue: kraken
product: perp
research_goal: 'Test a finding the trade_efficiency reader noticed after run_071 on
  idea HOURLY_SHOCK_CONTINUATION_MOMENTUM_1H_BTC_ETH: In this strategy, lots opened
  at a forecast of 10 or more (a full-size long entry) earn a higher mean net return
  than the other lots, in every window. Its claim block is pre-filled (candidate.claim).
  Evidence: q11:horizons.trade.effect=0.000988; q11:horizons.trade.windows_claimed_sign=6;
  q13:horizons.trade.effect=0.000361; q13:horizons.trade.windows_claimed_sign=3 It
  backtests on fold B (2018-01, 2018-09, 2019-05, 2020-01, 2020-09, 2021-05; config/folds.yaml),
  the next fold its lineage (run_071) has not used. It starts from run_071''s base
  config (candidate.start_config) -- the block the claim is about.'
machine_constraints:
  protocol:
    symbols:
    - BTCUSDT
    - ETHUSDT
    timeframe: 1h
    start: '2018-01-01'
    end: '2021-08-31'
    window_months: 4
    fold: B
candidate:
  claim:
    statement: 'In this strategy, lots opened at a forecast of 10 or more (a full-size
      long entry) earn a higher mean net return than the other lots, in every window.

      '
    kind: execution_behaviour
    tests:
    - name: strong_long_entries_earn_more
      selector:
        kind: trade
        where:
        - field: entry_forecast
          op: '>='
          value: 10
      outcome:
        kind: trade_net_return
      baseline:
        kind: other_trades
      statistic: mean_diff
      direction: greater
      floor:
        min_events: 100
        min_windows: 4
    pass_if: 'On the unseen fold, lots with an entry forecast of 10 or more have a
      higher mean trade net return than the other lots, with at least 100 such lots,
      and the effect points the same way in most windows.

      '
    fail_if: 'On the unseen fold, these lots have a mean trade net return at or below
      the other lots'' mean, or the effect points the claimed way in only about half
      the windows or fewer.

      '
    rationale: 'The target allocation is the forecast divided by 10, and a rebalance
      happens on each allocation change at or above the band. A forecast of 10 or
      more therefore opens a full-size long, after the strongest combined reading
      of the move and Donchian extremeness. This is a single-side effect of magnitude,
      not of side: all longs together earn less than the strong longs and point the
      claimed way in only about half the windows, so side alone does not explain it.
      The measured windows are BTCUSD windows only, so the claim is confined to this
      strategy and its entry rule, not to the market.

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
      normalized and scaled, form the hypothesis block—jointly measuring continuation
      strength via 1-bar move magnitude and close position in recent range (proxies
      for intrabar body_fraction and extremeness_percentile). The ungated regime_detector
      is scaffolding: it routes every bar to the ''unknown'' regime unconditionally,
      allowing the signal to activate on all bars as the hypothesis requires.'
  criteria_from: hypothesis_generation
  source:
    origin: reader
    proposal_ref: runs/run_071/artifacts/proposals/trade_efficiency.yaml#trade_efficiency-run_071-3
    source_run: run_071
    parent_hypothesis_id: HOURLY_SHOCK_CONTINUATION_MOMENTUM_1H_BTC_ETH
    hypothesis_id: HOURLY_SHOCK_CONTINUATION_MOMENTUM_1H_BTC_ETH__trade_efficiency-run_071-3
    decision_ref: runs/run_075/artifacts/decision_record_2.yaml
    proposal:
      kind: side_finding
      claim:
        statement: 'In this strategy, lots opened at a forecast of 10 or more (a full-size
          long entry) earn a higher mean net return than the other lots, in every
          window.

          '
        kind: execution_behaviour
        tests:
        - name: strong_long_entries_earn_more
          selector:
            kind: trade
            where:
            - field: entry_forecast
              op: '>='
              value: 10
          outcome:
            kind: trade_net_return
          baseline:
            kind: other_trades
          statistic: mean_diff
          direction: greater
          floor:
            min_events: 100
            min_windows: 4
        pass_if: 'On the unseen fold, lots with an entry forecast of 10 or more have
          a higher mean trade net return than the other lots, with at least 100 such
          lots, and the effect points the same way in most windows.

          '
        fail_if: 'On the unseen fold, these lots have a mean trade net return at or
          below the other lots'' mean, or the effect points the claimed way in only
          about half the windows or fewer.

          '
        rationale: 'The target allocation is the forecast divided by 10, and a rebalance
          happens on each allocation change at or above the band. A forecast of 10
          or more therefore opens a full-size long, after the strongest combined reading
          of the move and Donchian extremeness. This is a single-side effect of magnitude,
          not of side: all longs together earn less than the strong longs and point
          the claimed way in only about half the windows, so side alone does not explain
          it. The measured windows are BTCUSD windows only, so the claim is confined
          to this strategy and its entry rule, not to the market.

          '
      evidence:
      - q11:horizons.trade.effect=0.000988
      - q11:horizons.trade.windows_claimed_sign=6
      - q13:horizons.trade.effect=0.000361
      - q13:horizons.trade.windows_claimed_sign=3
      config_change: []
      vehicle: []
      combines_as: execution_rule
    base_config_ref: runs/run_071/artifacts/variants/base/strategy_config.json
    start_config_sha256: 6cf77f4eef76884229ac1d4f72473a81329c50d0c15cb17df4effadf1cc27e98
---

# trade_efficiency-run_071-3

Written by tools/decide_next.py (E-059, slice 6b) from runs/run_071/artifacts/proposals/trade_efficiency.yaml#trade_efficiency-run_071-3; decision record: runs/run_075/artifacts/decision_record_2.yaml.

This brief carries no pass criteria on purpose (operator decision 2, 2026-09-24): step 1a writes a hypothesis card and criteria coherent with the proposed idea, from config/criterion_menu.yaml. A patch's resolved config passes through to 1b (candidate.config), and 5a checks it against candidate.source.expected_config_sha256.
