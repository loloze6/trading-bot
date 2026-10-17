---
strategy_domain: volatility_managed_trend
market_universe:
- BTCUSDT
- ETHUSDT
timeframe: 1h
venue: kraken
product: perp
research_goal: 'Test a finding the trade_efficiency reader noticed after run_079 on
  idea VOL_MANAGED_TIME_SERIES_MOMENTUM__trade_efficiency-run_066-2: In this strategy,
  lots opened at an entry forecast between -5 and 5 (a weak entry, close to zero)
  earn a lower mean net return than the other lots, in most windows. Its claim block
  is pre-filled (candidate.claim). Evidence: q9:horizons.trade.effect=-0.00116; q9:horizons.trade.windows_claimed_sign=5;
  q9:horizons.trade.n_events=2586; q11:groups.all.n_trades=1871; q5:groups.all.n_trades=3480
  It backtests on fold C (2018-01, 2018-09, 2019-05, 2020-01, 2020-09, 2021-05; config/folds.yaml),
  the next fold its lineage (run_079, run_066) has not used. It starts from run_079''s
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
    statement: 'In this strategy, lots opened at an entry forecast between -5 and
      5 (a weak entry, close to zero) earn a lower mean net return than the other
      lots, in most windows.

      '
    kind: execution_behaviour
    tests:
    - name: weak_entries_earn_less
      selector:
        kind: trade
        where:
        - field: entry_forecast
          op: '>='
          value: -5
        - field: entry_forecast
          op: <=
          value: 5
      outcome:
        kind: trade_net_return
      baseline:
        kind: other_trades
      statistic: mean_diff
      direction: less
      floor:
        min_events: 100
        min_windows: 4
    pass_if: 'On the unseen fold, lots opened at an entry forecast between -5 and
      5 have a lower mean net return than the other lots, the effect points that way
      in at least 4 windows, with at least 100 such lots.

      '
    fail_if: 'On the unseen fold, weak-entry lots earn the same or more than the other
      lots, or the lower mean holds in only a few windows.

      '
    rationale: 'The Keltner forecast is a scaled distance of price from its band-relative
      EMA. A forecast near zero means price sits almost on its EMA and the signal
      has only just turned, so a lot opened there has little room before the forecast
      crosses zero again. The second query supports this: lots closed by a sign flip
      are over-represented among weak entries (most flip-closed lots opened at a weak
      forecast, against a quarter of all lots), and flip-closed lots are the ones
      that lose on average. Only the entry-time field is selected; the exit cause
      is used as the explanation, not as the selector.

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
      is the hypothesis''s block: it implements the graded momentum forecast via ATR-normalized
      distance from EMA, with parameters EMA-20, ATR-20, multiplier-2.0 exactly as
      in run_066. The ungated regime_detector (rules=[], components=[], default_regime=''unknown'')
      is scaffolding required to activate the signal on every bar.'
  criteria_from: hypothesis_generation
  source:
    origin: reader
    proposal_ref: runs/run_079/artifacts/proposals/trade_efficiency.yaml#trade_efficiency-run_079-1
    source_run: run_079
    parent_hypothesis_id: VOL_MANAGED_TIME_SERIES_MOMENTUM__trade_efficiency-run_066-2
    hypothesis_id: VOL_MANAGED_TIME_SERIES_MOMENTUM__trade_efficiency-run_066-2__trade_efficiency-run_079-1
    decision_ref: runs/run_079/artifacts/decision_record.yaml
    proposal:
      kind: side_finding
      claim:
        statement: 'In this strategy, lots opened at an entry forecast between -5
          and 5 (a weak entry, close to zero) earn a lower mean net return than the
          other lots, in most windows.

          '
        kind: execution_behaviour
        tests:
        - name: weak_entries_earn_less
          selector:
            kind: trade
            where:
            - field: entry_forecast
              op: '>='
              value: -5
            - field: entry_forecast
              op: <=
              value: 5
          outcome:
            kind: trade_net_return
          baseline:
            kind: other_trades
          statistic: mean_diff
          direction: less
          floor:
            min_events: 100
            min_windows: 4
        pass_if: 'On the unseen fold, lots opened at an entry forecast between -5
          and 5 have a lower mean net return than the other lots, the effect points
          that way in at least 4 windows, with at least 100 such lots.

          '
        fail_if: 'On the unseen fold, weak-entry lots earn the same or more than the
          other lots, or the lower mean holds in only a few windows.

          '
        rationale: 'The Keltner forecast is a scaled distance of price from its band-relative
          EMA. A forecast near zero means price sits almost on its EMA and the signal
          has only just turned, so a lot opened there has little room before the forecast
          crosses zero again. The second query supports this: lots closed by a sign
          flip are over-represented among weak entries (most flip-closed lots opened
          at a weak forecast, against a quarter of all lots), and flip-closed lots
          are the ones that lose on average. Only the entry-time field is selected;
          the exit cause is used as the explanation, not as the selector.

          '
      evidence:
      - q9:horizons.trade.effect=-0.00116
      - q9:horizons.trade.windows_claimed_sign=5
      - q9:horizons.trade.n_events=2586
      - q11:groups.all.n_trades=1871
      - q5:groups.all.n_trades=3480
      config_change: []
      vehicle: []
      combines_as: execution_rule
      fold_observed: B
    base_config_ref: runs/run_079/artifacts/variants/base/strategy_config.json
    start_config_sha256: daead3965e303ab52ce7eb52d86d20938129ab1825102a2db9cb3842d58e894c
---

# trade_efficiency-run_079-1

Written by tools/decide_next.py (E-059, slice 6b) from runs/run_079/artifacts/proposals/trade_efficiency.yaml#trade_efficiency-run_079-1; decision record: runs/run_079/artifacts/decision_record.yaml.

This brief carries no pass criteria on purpose (operator decision 2, 2026-09-24): step 1a writes a hypothesis card and criteria coherent with the proposed idea, from config/criterion_menu.yaml. A patch's resolved config passes through to 1b (candidate.config), and 5a checks it against candidate.source.expected_config_sha256.
