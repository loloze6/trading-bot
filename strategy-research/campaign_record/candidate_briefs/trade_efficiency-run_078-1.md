---
strategy_domain: short_horizon_reversal
market_universe:
- BTCUSDT
- ETHUSDT
timeframe: 1h
venue: kraken
product: perp
research_goal: 'Test a finding the trade_efficiency reader noticed after run_078 on
  idea HOURLY_SHOCK_CONTINUATION_MOMENTUM_1H_BTC_ETH__trade_efficiency-run_071-4:
  In this strategy, after a lot is closed by a signal flip (its forecast crosses to
  the other side of zero), the market keeps moving in the direction the flip signals
  over the next 1 and 6 bars, more than after the other lots'' exits. Its claim block
  is pre-filled (candidate.claim). Evidence: q11:horizons.1.effect=-0.00019271003;
  q11:horizons.6.effect=-0.0006254103; q10:horizons.1.effect=0.00019271003 It backtests
  on fold C (2018-01, 2018-09, 2019-05, 2020-01, 2020-09, 2021-05; config/folds.yaml),
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
    statement: 'In this strategy, after a lot is closed by a signal flip (its forecast
      crosses to the other side of zero), the market keeps moving in the direction
      the flip signals over the next 1 and 6 bars, more than after the other lots''
      exits.

      '
    kind: execution_behaviour
    tests:
    - name: flip_exits_followed_by_continuation
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
      baseline:
        kind: other_trades
      statistic: mean_diff
      direction: less
      floor:
        min_events: 100
        min_windows: 4
    pass_if: 'On the unseen fold, the effect is negative at both 1 and 6 bars, and
      it points the claimed way in most windows, with at least 100 flip-closed lots.

      '
    fail_if: 'At 1 or 6 bars the effect is zero or positive, or it points the claimed
      way in fewer than half the windows.

      '
    rationale: 'The forecast is a short-memory blend of one-bar move magnitude and
      20-bar range position. A flip closes a lot at the bar where the blend changes
      sign, which is typically just after a short-run move has already turned. Because
      the forecast carries little persistence beyond a few bars, the price tends to
      keep moving in the new direction for a short while after the flip, so the closed
      lot''s side sees the move go against it. The same pattern shows at the opposite
      selector: lots closed by a same-sign reduction show the mirror-image effect
      at the same horizons.

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
    proposal_ref: runs/run_078/artifacts/proposals/trade_efficiency.yaml#trade_efficiency-run_078-1
    source_run: run_078
    parent_hypothesis_id: HOURLY_SHOCK_CONTINUATION_MOMENTUM_1H_BTC_ETH__trade_efficiency-run_071-4
    hypothesis_id: HOURLY_SHOCK_CONTINUATION_MOMENTUM_1H_BTC_ETH__trade_efficiency-run_071-4__trade_efficiency-run_078-1
    decision_ref: runs/run_078/artifacts/decision_record.yaml
    proposal:
      kind: side_finding
      claim:
        statement: 'In this strategy, after a lot is closed by a signal flip (its
          forecast crosses to the other side of zero), the market keeps moving in
          the direction the flip signals over the next 1 and 6 bars, more than after
          the other lots'' exits.

          '
        kind: execution_behaviour
        tests:
        - name: flip_exits_followed_by_continuation
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
          baseline:
            kind: other_trades
          statistic: mean_diff
          direction: less
          floor:
            min_events: 100
            min_windows: 4
        pass_if: 'On the unseen fold, the effect is negative at both 1 and 6 bars,
          and it points the claimed way in most windows, with at least 100 flip-closed
          lots.

          '
        fail_if: 'At 1 or 6 bars the effect is zero or positive, or it points the
          claimed way in fewer than half the windows.

          '
        rationale: 'The forecast is a short-memory blend of one-bar move magnitude
          and 20-bar range position. A flip closes a lot at the bar where the blend
          changes sign, which is typically just after a short-run move has already
          turned. Because the forecast carries little persistence beyond a few bars,
          the price tends to keep moving in the new direction for a short while after
          the flip, so the closed lot''s side sees the move go against it. The same
          pattern shows at the opposite selector: lots closed by a same-sign reduction
          show the mirror-image effect at the same horizons.

          '
      evidence:
      - q11:horizons.1.effect=-0.00019271003
      - q11:horizons.6.effect=-0.0006254103
      - q10:horizons.1.effect=0.00019271003
      config_change: []
      vehicle: []
      combines_as: execution_rule
      fold_observed: B
    base_config_ref: runs/run_078/artifacts/variants/base/strategy_config.json
    start_config_sha256: 6cf77f4eef76884229ac1d4f72473a81329c50d0c15cb17df4effadf1cc27e98
---

# trade_efficiency-run_078-1

Written by tools/decide_next.py (E-059, slice 6b) from runs/run_078/artifacts/proposals/trade_efficiency.yaml#trade_efficiency-run_078-1; decision record: runs/run_078/artifacts/decision_record.yaml.

This brief carries no pass criteria on purpose (operator decision 2, 2026-09-24): step 1a writes a hypothesis card and criteria coherent with the proposed idea, from config/criterion_menu.yaml. A patch's resolved config passes through to 1b (candidate.config), and 5a checks it against candidate.source.expected_config_sha256.
