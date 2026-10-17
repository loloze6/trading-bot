---
strategy_domain: daily_breadth
market_universe:
- BTCUSDT
timeframe: 1d
venue: kraken
product: perp
research_goal: 'Test a finding the forecast_power reader noticed after run_094 on
  idea OVERNIGHT_GAP_MEAN_REVERSION_1D_BTC: In this strategy, lots opened at a forecast
  of 10 or more, or of -10 or less (a full-size entry on either side), earn a lower
  mean net return than the other lots, in most windows. Its claim block is pre-filled
  (candidate.claim). Evidence: q9:horizons.trade.effect=-0.0021951265; q10:horizons.trade.effect=-0.0086628842;
  q7:horizons.1.effect=-0.0016518528 It backtests on fold D (2024-01, 2024-05, 2024-09,
  2025-01, 2025-05, 2025-09; config/folds.yaml), drawn among the folds its source
  run run_094 is not on (B, C, D). It starts from run_094''s base config (candidate.start_config)
  -- the block the claim is about.'
machine_constraints:
  protocol:
    symbols:
    - BTCUSDT
    timeframe: 1d
    fold: D
    start: '2024-01-01'
    end: '2025-12-31'
    window_months: 4
candidate:
  claim:
    statement: 'In this strategy, lots opened at a forecast of 10 or more, or of -10
      or less (a full-size entry on either side), earn a lower mean net return than
      the other lots, in most windows.

      '
    kind: execution_behaviour
    tests:
    - name: long_strong_entries_earn_less
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
      direction: less
      floor:
        min_events: 100
        min_windows: 4
    - name: short_strong_entries_earn_less
      selector:
        kind: trade
        where:
        - field: entry_forecast
          op: <=
          value: -10
      outcome:
        kind: trade_net_return
      baseline:
        kind: other_trades
      statistic: mean_diff
      direction: less
      floor:
        min_events: 100
        min_windows: 4
    pass_if: 'On the unseen fold, both tests show a negative effect (the selected
      lots earn less than the other lots), with at least 100 selected lots each and
      the sign in most windows.

      '
    fail_if: 'Either test shows a zero or positive effect (the selected lots earn
      at least as much as the other lots), or the effect points the other way in most
      windows.

      '
    rationale: 'Overnight gaps in this market continue rather than refill: after a
      large gap, the next bar moves further in the gap''s direction, not back. The
      strategy''s negated forecast bets on the refill, so the lots it opens at large
      size are on the wrong side. The loss appears on both legs, so it is not a side
      effect of one direction.

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
          - id: gap_reversion
            class: strategies.strategy_components.PriceEvolutionComponent
            params:
              period: 1
              scaling_factor: 20.0
            weight: 1.0
            transforms:
            - op: negate
            - op: clip
              params:
                min: -20.0
                max: 20.0
        trending: null
        mean_reversion: null
        chop: null
  start_manifest:
    block:
      kind: forecast
      config_paths:
      - /strategies/regimes/unknown/components/0
    scaffolding:
    - /regime_detector
    - /strategies/regimes/trending
    - /strategies/regimes/mean_reversion
    - /strategies/regimes/chop
    rationale: The PriceEvolutionComponent with negate and clip transforms (component/0
      under unknown regime) is the core gap-mean-reversion signal. The ungated detector
      (empty rules, empty components, default to unknown) and the null regimes are
      config structure required by the engine, not part of the hypothesis itself.
  criteria_from: hypothesis_generation
  source:
    origin: reader
    proposal_ref: runs/run_094/artifacts/proposals/forecast_power.yaml#forecast_power-run_094-1
    source_run: run_094
    parent_hypothesis_id: OVERNIGHT_GAP_MEAN_REVERSION_1D_BTC
    hypothesis_id: OVERNIGHT_GAP_MEAN_REVERSION_1D_BTC__forecast_power-run_094-1
    decision_ref: runs/run_094/artifacts/decision_record.yaml
    proposal:
      kind: side_finding
      claim:
        statement: 'In this strategy, lots opened at a forecast of 10 or more, or
          of -10 or less (a full-size entry on either side), earn a lower mean net
          return than the other lots, in most windows.

          '
        kind: execution_behaviour
        tests:
        - name: long_strong_entries_earn_less
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
          direction: less
          floor:
            min_events: 100
            min_windows: 4
        - name: short_strong_entries_earn_less
          selector:
            kind: trade
            where:
            - field: entry_forecast
              op: <=
              value: -10
          outcome:
            kind: trade_net_return
          baseline:
            kind: other_trades
          statistic: mean_diff
          direction: less
          floor:
            min_events: 100
            min_windows: 4
        pass_if: 'On the unseen fold, both tests show a negative effect (the selected
          lots earn less than the other lots), with at least 100 selected lots each
          and the sign in most windows.

          '
        fail_if: 'Either test shows a zero or positive effect (the selected lots earn
          at least as much as the other lots), or the effect points the other way
          in most windows.

          '
        rationale: 'Overnight gaps in this market continue rather than refill: after
          a large gap, the next bar moves further in the gap''s direction, not back.
          The strategy''s negated forecast bets on the refill, so the lots it opens
          at large size are on the wrong side. The loss appears on both legs, so it
          is not a side effect of one direction.

          '
      evidence:
      - q9:horizons.trade.effect=-0.0021951265
      - q10:horizons.trade.effect=-0.0086628842
      - q7:horizons.1.effect=-0.0016518528
      config_change: []
      vehicle: []
      combines_as: execution_rule
      fold_observed: A
    base_config_ref: runs/run_094/artifacts/variants/base/strategy_config.json
    start_config_sha256: d58e86d72b548c8f75765f4237c10d6d55016f47098ac0b4300117f44d96a2dd
---

# forecast_power-run_094-1

Written by tools/decide_next.py (E-059, slice 6b) from runs/run_094/artifacts/proposals/forecast_power.yaml#forecast_power-run_094-1; decision record: runs/run_094/artifacts/decision_record.yaml.

This brief carries no pass criteria on purpose (operator decision 2, 2026-09-24): step 1a writes a hypothesis card and criteria coherent with the proposed idea, from config/criterion_menu.yaml. A patch's resolved config passes through to 1b (candidate.config), and 5a checks it against candidate.source.expected_config_sha256.
