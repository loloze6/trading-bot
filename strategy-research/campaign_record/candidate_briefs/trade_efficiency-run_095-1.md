---
strategy_domain: daily_breadth
market_universe:
- BTCUSDT
timeframe: 1d
venue: kraken
product: perp
research_goal: 'Test a finding the trade_efficiency reader noticed after run_095 on
  idea OVERNIGHT_GAP_MEAN_REVERSION_1D_BTC__forecast_power-run_094-1: In this strategy,
  lots opened at a forecast of -5 or below (a deep short entry) earn a lower mean
  net return than the other lots, in most windows. Its claim block is pre-filled (candidate.claim).
  Evidence: q11:horizons.trade.effect=-0.0121; q11:horizons.trade.n_events=285 It
  backtests on fold B (2018-05, 2019-01, 2019-09, 2020-05, 2021-01, 2021-09; config/folds.yaml),
  drawn among the folds its source run run_095 is not on (A, B, C). It starts from
  run_095''s base config (candidate.start_config) -- the block the claim is about.'
machine_constraints:
  protocol:
    symbols:
    - BTCUSDT
    timeframe: 1d
    fold: B
    start: '2018-05-01'
    end: '2021-12-31'
    window_months: 4
candidate:
  claim:
    statement: 'In this strategy, lots opened at a forecast of -5 or below (a deep
      short entry) earn a lower mean net return than the other lots, in most windows.

      '
    kind: execution_behaviour
    tests:
    - name: deep_negative_entries_earn_less
      selector:
        kind: trade
        where:
        - field: entry_forecast
          op: <=
          value: -5
      outcome:
        kind: trade_net_return
      baseline:
        kind: other_trades
      statistic: mean_diff
      direction: less
      floor:
        min_events: 100
        min_windows: 4
    pass_if: 'On the unseen fold, lots opened at a forecast of -5 or below have a
      lower mean net return than the other lots, the effect points the same way in
      most windows, with at least 100 such lots.

      '
    fail_if: 'On the unseen fold, the effect is zero or positive, or it points the
      claimed way in only a minority of windows.

      '
    rationale: 'The forecast is the negated one-day price move, clipped, and allocation
      is the forecast divided by <n>, so a forecast of -5 or below opens a large short
      right after a big up-day. Over a daily horizon the market in this sample tends
      to continue the move that opened the lot, so the deepest short entries lose.
      The mechanism predicts the weaker negative-forecast entries lose less; the trade_slice
      on that band (q12) has a median near zero, though on only a few lots.

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
    proposal_ref: runs/run_095/artifacts/proposals/trade_efficiency.yaml#trade_efficiency-run_095-1
    source_run: run_095
    parent_hypothesis_id: OVERNIGHT_GAP_MEAN_REVERSION_1D_BTC__forecast_power-run_094-1
    hypothesis_id: OVERNIGHT_GAP_MEAN_REVERSION_1D_BTC__forecast_power-run_094-1__trade_efficiency-run_095-1
    decision_ref: runs/run_096/artifacts/decision_record.yaml
    proposal:
      kind: side_finding
      claim:
        statement: 'In this strategy, lots opened at a forecast of -5 or below (a
          deep short entry) earn a lower mean net return than the other lots, in most
          windows.

          '
        kind: execution_behaviour
        tests:
        - name: deep_negative_entries_earn_less
          selector:
            kind: trade
            where:
            - field: entry_forecast
              op: <=
              value: -5
          outcome:
            kind: trade_net_return
          baseline:
            kind: other_trades
          statistic: mean_diff
          direction: less
          floor:
            min_events: 100
            min_windows: 4
        pass_if: 'On the unseen fold, lots opened at a forecast of -5 or below have
          a lower mean net return than the other lots, the effect points the same
          way in most windows, with at least 100 such lots.

          '
        fail_if: 'On the unseen fold, the effect is zero or positive, or it points
          the claimed way in only a minority of windows.

          '
        rationale: 'The forecast is the negated one-day price move, clipped, and allocation
          is the forecast divided by <n>, so a forecast of -5 or below opens a large
          short right after a big up-day. Over a daily horizon the market in this
          sample tends to continue the move that opened the lot, so the deepest short
          entries lose. The mechanism predicts the weaker negative-forecast entries
          lose less; the trade_slice on that band (q12) has a median near zero, though
          on only a few lots.

          '
      evidence:
      - q11:horizons.trade.effect=-0.0121
      - q11:horizons.trade.n_events=285
      config_change: []
      vehicle: []
      combines_as: execution_rule
      fold_observed: D
    base_config_ref: runs/run_095/artifacts/variants/base/strategy_config.json
    start_config_sha256: d58e86d72b548c8f75765f4237c10d6d55016f47098ac0b4300117f44d96a2dd
---

# trade_efficiency-run_095-1

Written by tools/decide_next.py (E-059, slice 6b) from runs/run_095/artifacts/proposals/trade_efficiency.yaml#trade_efficiency-run_095-1; decision record: runs/run_096/artifacts/decision_record.yaml.

This brief carries no pass criteria on purpose (operator decision 2, 2026-09-24): step 1a writes a hypothesis card and criteria coherent with the proposed idea, from config/criterion_menu.yaml. A patch's resolved config passes through to 1b (candidate.config), and 5a checks it against candidate.source.expected_config_sha256.
