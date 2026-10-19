---
strategy_domain: short_horizon_reversal
market_universe:
- BTCUSDT
- ETHUSDT
timeframe: 1h
venue: kraken
product: perp
research_goal: 'Test a finding the trade_efficiency reader noticed after run_075 on
  idea HOURLY_SHOCK_REVERSAL_HORIZON_DECAY_1H_BTC_ETH: In this strategy, lots opened
  at an entry forecast of -5 or below (large short entries, taken after a sharp rise
  in the bar before) earn a lower mean net return per lot than the other lots. Its
  claim block is pre-filled (candidate.claim). Evidence: q14:horizons.trade.effect=-0.00044936663;
  q14:horizons.trade.n_events=6451; q14:horizons.trade.windows_claimed_sign=4; q8:groups.all.trade_net_return_mean=-0.0056648929;
  q15:horizons.trade.effect=0.00017717894 It backtests on fold B (2018-05, 2019-01,
  2019-09, 2020-05, 2021-01, 2021-09; config/folds.yaml), drawn among the folds its
  source run run_075 is not on (B, C, D). It starts from run_075''s base config (candidate.start_config)
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
    statement: 'In this strategy, lots opened at an entry forecast of -5 or below
      (large short entries, taken after a sharp rise in the bar before) earn a lower
      mean net return per lot than the other lots.

      '
    kind: execution_behaviour
    tests:
    - name: short_entries_large_forecast_lose_more
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
    pass_if: 'On the unseen fold, lots opened at an entry forecast of -5 or below
      have a lower mean trade net return than the other lots, the effect points the
      claimed way in most windows, with at least 100 such lots.

      '
    fail_if: 'On the unseen fold the effect is zero or points the other way in most
      windows, or the selected lots earn at least as much as the other lots.

      '
    rationale: 'The forecast is the negated one-bar move scaled by 20, and the target
      allocation is the forecast divided by <n>, so a strongly negative forecast opens
      a large short at the close of a sharp rise. Lots closed by a reduction are the
      lots opened at the largest forecasts, and they earn clearly less than flip-closed
      lots. Their post-exit drift is close to zero, so their loss happens inside the
      hold, which fits a mean-reversion bet failing on the bar after entry. The long
      side does not show the same effect, so the asymmetry belongs to this strategy''s
      short entries rather than to every large forecast.

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
          - id: shock_1h
            class: strategies.strategy_components.PriceEvolutionComponent
            params:
              period: 1
              scaling_factor: 1.0
            weight: 1.0
            lookback: 500
            transforms:
            - op: ratio_to_mean
            - op: negate
            - op: scale
              params:
                factor: 20.0
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
    rationale: 'PriceEvolutionComponent(period=1) with ratio_to_mean normalization,
      sign inversion, and magnitude scaling implements the hypothesis''s core signal:
      mean-reversion forecasts on 1h price shocks. The ungated regime detector (empty
      rules, components=[], default_regime=unknown) runs this signal on every bar,
      per the hypothesis specification of no regime condition.'
  criteria_from: hypothesis_generation
  source:
    origin: reader
    proposal_ref: runs/run_075/artifacts/proposals/trade_efficiency.yaml#trade_efficiency-run_075-1
    source_run: run_075
    parent_hypothesis_id: HOURLY_SHOCK_REVERSAL_HORIZON_DECAY_1H_BTC_ETH
    hypothesis_id: HOURLY_SHOCK_REVERSAL_HORIZON_DECAY_1H_BTC_ETH__trade_efficiency-run_075-1
    decision_ref: runs/run_097/artifacts/decision_record.yaml
    proposal:
      kind: side_finding
      claim:
        statement: 'In this strategy, lots opened at an entry forecast of -5 or below
          (large short entries, taken after a sharp rise in the bar before) earn a
          lower mean net return per lot than the other lots.

          '
        kind: execution_behaviour
        tests:
        - name: short_entries_large_forecast_lose_more
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
        pass_if: 'On the unseen fold, lots opened at an entry forecast of -5 or below
          have a lower mean trade net return than the other lots, the effect points
          the claimed way in most windows, with at least 100 such lots.

          '
        fail_if: 'On the unseen fold the effect is zero or points the other way in
          most windows, or the selected lots earn at least as much as the other lots.

          '
        rationale: 'The forecast is the negated one-bar move scaled by 20, and the
          target allocation is the forecast divided by <n>, so a strongly negative
          forecast opens a large short at the close of a sharp rise. Lots closed by
          a reduction are the lots opened at the largest forecasts, and they earn
          clearly less than flip-closed lots. Their post-exit drift is close to zero,
          so their loss happens inside the hold, which fits a mean-reversion bet failing
          on the bar after entry. The long side does not show the same effect, so
          the asymmetry belongs to this strategy''s short entries rather than to every
          large forecast.

          '
      evidence:
      - q14:horizons.trade.effect=-0.00044936663
      - q14:horizons.trade.n_events=6451
      - q14:horizons.trade.windows_claimed_sign=4
      - q8:groups.all.trade_net_return_mean=-0.0056648929
      - q15:horizons.trade.effect=0.00017717894
      config_change: []
      vehicle: []
      combines_as: execution_rule
    base_config_ref: runs/run_075/artifacts/variants/base/strategy_config.json
    start_config_sha256: 00867317466b1fed16ee9e6f2ba1a686665dfc3f8ad81d5905b98f13ed5e558e
---

# trade_efficiency-run_075-1

Written by tools/decide_next.py (E-059, slice 6b) from runs/run_075/artifacts/proposals/trade_efficiency.yaml#trade_efficiency-run_075-1; decision record: runs/run_097/artifacts/decision_record.yaml.

This brief carries no pass criteria on purpose (operator decision 2, 2026-09-24): step 1a writes a hypothesis card and criteria coherent with the proposed idea, from config/criterion_menu.yaml. A patch's resolved config passes through to 1b (candidate.config), and 5a checks it against candidate.source.expected_config_sha256.
