---
strategy_domain: volatility_managed_trend
market_universe:
- BTCUSDT
- ETHUSDT
timeframe: 1h
venue: kraken
product: perp
research_goal: 'Test a finding the trade_efficiency reader noticed after run_066 on
  idea VOL_MANAGED_TIME_SERIES_MOMENTUM: In this strategy, a lot closed by a forecast
  sign flip is followed by a move in its own direction more often over the next 6
  bars than the other lots are. Its claim block is pre-filled (candidate.claim). Evidence:
  q14:horizons.6.effect=0.0574; q14:horizons.6.n_events=2221; q14:horizons.6.windows_claimed_sign=6;
  q12:groups.all.post_exit_return_h6_share_positive=0.494 It backtests on fold B (2018-05,
  2019-01, 2019-09, 2020-05, 2021-01, 2021-09; config/folds.yaml), the next fold its
  lineage (run_066) has not used. It starts from run_066''s base config (candidate.start_config)
  -- the block the claim is about.'
machine_constraints:
  protocol:
    symbols:
    - BTCUSDT
    - ETHUSDT
    timeframe: 1h
    start: '2018-05-01'
    end: '2021-12-31'
    window_months: 4
    fold: B
candidate:
  claim:
    statement: 'In this strategy, a lot closed by a forecast sign flip is followed
      by a move in its own direction more often over the next 6 bars than the other
      lots are.

      '
    kind: execution_behaviour
    tests:
    - name: flip_closed_lots_continue
      selector:
        kind: trade
        where:
        - field: exit_cause
          op: ==
          value: flip
      outcome:
        kind: post_exit_return
        horizons:
        - 1
        - 6
        - 24
      baseline:
        kind: other_trades
      statistic: hit_rate
      direction: greater
      floor:
        min_events: 100
        min_windows: 4
    pass_if: 'At the 6-bar horizon, flip-closed lots have a higher share of post-exit
      moves in their own direction than the other lots, with at least 100 flip-closed
      lots, in most windows. The same sign holds at 1 and 24 bars.

      '
    fail_if: 'At the 6-bar horizon, the flip-closed lots'' share of post-exit moves
      in their own direction is at or below the other lots'' share in most windows.

      '
    rationale: 'The forecast is a Keltner breakout whose sign turns on a pullback
      toward the EMA, so the strategy closes a lot on a forecast sign change rather
      than on a confirmed market turn. If the sign can change during a pause in the
      move, the price resumes the closed lot''s direction after the exit, and this
      test measures that. Reduction-closed lots show close to even odds of continuing
      over 6 bars, so the effect is specific to flips and is not a general drift.

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
          - id: keltner_momentum
            class: strategies.strategy_components.KeltnerBreakoutComponent
            params:
              ema_period: 20
              atr_period: 20
              atr_multiplier: 2.0
              scaling_factor: 20.0
            weight: 1.0
            transforms:
            - op: identity
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
    rationale: 'The KeltnerBreakoutComponent at /strategies/regimes/unknown/components/0
      is the hypothesis''s block: it implements the momentum-via-ATR-normalized-distance
      measure described in signal_concept (the core graded forecast). The ungated
      regime_detector (rules=[], components=[], default_regime=''unknown'') is scaffolding—required
      to activate the signal on every bar per hypothesis design, but not the signal
      itself. Volatility-scaling division (idealized as forecast / vol_multiplier)
      is not expressible in config and is documented deviation per hypothesis_card.'
  criteria_from: hypothesis_generation
  source:
    origin: reader
    proposal_ref: runs/run_066/artifacts/proposals/trade_efficiency.yaml#trade_efficiency-run_066-2
    source_run: run_066
    parent_hypothesis_id: VOL_MANAGED_TIME_SERIES_MOMENTUM
    hypothesis_id: VOL_MANAGED_TIME_SERIES_MOMENTUM__trade_efficiency-run_066-2
    decision_ref: runs/run_078/artifacts/decision_record_2.yaml
    proposal:
      kind: side_finding
      claim:
        statement: 'In this strategy, a lot closed by a forecast sign flip is followed
          by a move in its own direction more often over the next 6 bars than the
          other lots are.

          '
        kind: execution_behaviour
        tests:
        - name: flip_closed_lots_continue
          selector:
            kind: trade
            where:
            - field: exit_cause
              op: ==
              value: flip
          outcome:
            kind: post_exit_return
            horizons:
            - 1
            - 6
            - 24
          baseline:
            kind: other_trades
          statistic: hit_rate
          direction: greater
          floor:
            min_events: 100
            min_windows: 4
        pass_if: 'At the 6-bar horizon, flip-closed lots have a higher share of post-exit
          moves in their own direction than the other lots, with at least 100 flip-closed
          lots, in most windows. The same sign holds at 1 and 24 bars.

          '
        fail_if: 'At the 6-bar horizon, the flip-closed lots'' share of post-exit
          moves in their own direction is at or below the other lots'' share in most
          windows.

          '
        rationale: 'The forecast is a Keltner breakout whose sign turns on a pullback
          toward the EMA, so the strategy closes a lot on a forecast sign change rather
          than on a confirmed market turn. If the sign can change during a pause in
          the move, the price resumes the closed lot''s direction after the exit,
          and this test measures that. Reduction-closed lots show close to even odds
          of continuing over 6 bars, so the effect is specific to flips and is not
          a general drift.

          '
      evidence:
      - q14:horizons.6.effect=0.0574
      - q14:horizons.6.n_events=2221
      - q14:horizons.6.windows_claimed_sign=6
      - q12:groups.all.post_exit_return_h6_share_positive=0.494
      config_change: []
      vehicle: []
      combines_as: execution_rule
    base_config_ref: runs/run_066/artifacts/variants/base/strategy_config.json
    start_config_sha256: daead3965e303ab52ce7eb52d86d20938129ab1825102a2db9cb3842d58e894c
---

# trade_efficiency-run_066-2

Written by tools/decide_next.py (E-059, slice 6b) from runs/run_066/artifacts/proposals/trade_efficiency.yaml#trade_efficiency-run_066-2; decision record: runs/run_078/artifacts/decision_record_2.yaml.

This brief carries no pass criteria on purpose (operator decision 2, 2026-09-24): step 1a writes a hypothesis card and criteria coherent with the proposed idea, from config/criterion_menu.yaml. A patch's resolved config passes through to 1b (candidate.config), and 5a checks it against candidate.source.expected_config_sha256.
