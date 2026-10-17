---
strategy_domain: daily_breadth
market_universe:
- BTCUSDT
timeframe: 1d
venue: kraken
product: perp
research_goal: 'Test a finding the forecast_power reader noticed after run_095 on
  idea OVERNIGHT_GAP_MEAN_REVERSION_1D_BTC__forecast_power-run_094-1: In this strategy,
  which goes short whenever its forecast is negative, short lots earn a lower mean
  net return than the other lots in most windows. Its claim block is pre-filled (candidate.claim).
  Evidence: q11:horizons.trade.effect=-0.011784709; q11:horizons.trade.windows_claimed_sign=5;
  q11:horizons.trade.windows_with_value=6; q9:horizons.1.effect=-0.0017097614 It backtests
  on fold C (2018-01, 2018-09, 2019-05, 2020-01, 2020-09, 2021-05; config/folds.yaml),
  drawn among the folds its source run run_095 is not on (A, B, C). It starts from
  run_095''s base config (candidate.start_config) -- the block the claim is about.'
machine_constraints:
  protocol:
    symbols:
    - BTCUSDT
    timeframe: 1d
    fold: C
    start: '2018-01-01'
    end: '2021-08-31'
    window_months: 4
candidate:
  claim:
    statement: 'In this strategy, which goes short whenever its forecast is negative,
      short lots earn a lower mean net return than the other lots in most windows.

      '
    kind: execution_behaviour
    tests:
    - name: shorts_earn_less_than_other_lots
      selector:
        kind: trade
        where:
        - field: side
          op: ==
          value: short
      outcome:
        kind: trade_net_return
      baseline:
        kind: other_trades
      statistic: mean_diff
      direction: less
      floor:
        min_events: 100
        min_windows: 4
    pass_if: 'On the unseen fold, short lots have a lower mean trade_net_return than
      the other lots, the effect points the same way in most windows, with at least
      100 short lots.

      '
    fail_if: 'Short lots earn the same or a higher mean net return than the other
      lots, or the effect is lower in only a minority of windows.

      '
    rationale: 'Short lots lost in every window measured, so the result is not one
      market regime. Their average loss is far larger than the one-bar forward move
      after a large up day, which leans the short way (lower, though small). So the
      shortfall is not a missed reversal at the forecast''s own horizon; it comes
      from how the short lots are entered and exited.

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
    rationale: The negated one-bar price evolution component with its clip is the
      signal under test; the ungated detector and the null regimes are engine scaffolding.
  criteria_from: hypothesis_generation
  source:
    origin: reader
    proposal_ref: runs/run_095/artifacts/proposals/forecast_power.yaml#forecast_power-run_095-1
    source_run: run_095
    parent_hypothesis_id: OVERNIGHT_GAP_MEAN_REVERSION_1D_BTC__forecast_power-run_094-1
    hypothesis_id: OVERNIGHT_GAP_MEAN_REVERSION_1D_BTC__forecast_power-run_094-1__forecast_power-run_095-1
    decision_ref: runs/run_095/artifacts/decision_record.yaml
    proposal:
      kind: side_finding
      claim:
        statement: 'In this strategy, which goes short whenever its forecast is negative,
          short lots earn a lower mean net return than the other lots in most windows.

          '
        kind: execution_behaviour
        tests:
        - name: shorts_earn_less_than_other_lots
          selector:
            kind: trade
            where:
            - field: side
              op: ==
              value: short
          outcome:
            kind: trade_net_return
          baseline:
            kind: other_trades
          statistic: mean_diff
          direction: less
          floor:
            min_events: 100
            min_windows: 4
        pass_if: 'On the unseen fold, short lots have a lower mean trade_net_return
          than the other lots, the effect points the same way in most windows, with
          at least 100 short lots.

          '
        fail_if: 'Short lots earn the same or a higher mean net return than the other
          lots, or the effect is lower in only a minority of windows.

          '
        rationale: 'Short lots lost in every window measured, so the result is not
          one market regime. Their average loss is far larger than the one-bar forward
          move after a large up day, which leans the short way (lower, though small).
          So the shortfall is not a missed reversal at the forecast''s own horizon;
          it comes from how the short lots are entered and exited.

          '
      evidence:
      - q11:horizons.trade.effect=-0.011784709
      - q11:horizons.trade.windows_claimed_sign=5
      - q11:horizons.trade.windows_with_value=6
      - q9:horizons.1.effect=-0.0017097614
      config_change: []
      vehicle: []
      combines_as: execution_rule
      fold_observed: D
    base_config_ref: runs/run_095/artifacts/variants/base/strategy_config.json
    start_config_sha256: d58e86d72b548c8f75765f4237c10d6d55016f47098ac0b4300117f44d96a2dd
---

# forecast_power-run_095-1

Written by tools/decide_next.py (E-059, slice 6b) from runs/run_095/artifacts/proposals/forecast_power.yaml#forecast_power-run_095-1; decision record: runs/run_095/artifacts/decision_record.yaml.

This brief carries no pass criteria on purpose (operator decision 2, 2026-09-24): step 1a writes a hypothesis card and criteria coherent with the proposed idea, from config/criterion_menu.yaml. A patch's resolved config passes through to 1b (candidate.config), and 5a checks it against candidate.source.expected_config_sha256.
