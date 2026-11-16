---
strategy_domain: SMA trend
market_universe:
- BTCUSDT
timeframe: 1h
venue: kraken
product: perp
research_goal: 'Test a finding the forecast_power reader noticed after run_101 on
  idea SMA_PULLBACK_IN_TREND_24H_1H_BTC_FOLD_A: In this strategy, the forecast ranks
  forward returns positively over 1, 6 and 24 bars on bars where its size is 6 or
  more. The rank IC grows with forecast size and is about zero on bars below 6. Shrinking
  small component readings with a graded dead zone, so the forecast is carried by
  its large readings, should therefore keep the edge and drop the low-information
  trades. Its claim block is pre-filled (candidate.claim). Evidence: q12:horizons.1.effect=0.0721;
  q12:horizons.1.windows_claimed_sign=6; q12:horizons.6.effect=0.0513; q12:horizons.24.effect=0.0711;
  q12:horizons.24.n_events=6636; q9:horizons.24.effect=0.112; q8:horizons.24.effect=-0.0117
  It backtests on fold C (2018-01, 2018-09, 2019-05, 2020-01, 2020-09, 2021-05; config/folds.yaml),
  drawn among the folds its source run run_101 is not on (B, C, D). It runs the finding''s
  config vehicle, a complete strategy config (candidate.start_config), built by code
  at step 1b exactly as given (D-110), with run_101''s block manifest.'
machine_constraints:
  protocol:
    symbols:
    - BTCUSDT
    timeframe: 1h
    start: '2018-01-01'
    end: '2021-08-31'
    window_months: 4
    fold: C
constraints:
- "Build EXACTLY this strategy config (JSON): the config vehicle of forecast_power-run_101-1\
  \ (a side finding of run_101), unchanged (D-162).\n{\n  \"regime_detector\": {\n\
  \    \"mode\": \"threshold_rules\",\n    \"components\": [],\n    \"rules\": [],\n\
  \    \"default_regime\": \"unknown\"\n  },\n  \"strategies\": {\n    \"regimes\"\
  : {\n      \"unknown\": {\n        \"components\": [\n          {\n            \"\
  id\": \"trend_spread\",\n            \"class\": \"strategies.strategy_components.EMASpreadComponent\"\
  ,\n            \"params\": {\n              \"fast_period\": 24,\n             \
  \ \"slow_period\": 168,\n              \"average\": \"sma\"\n            },\n  \
  \          \"weight\": 1.0,\n            \"transforms\": [\n              {\n  \
  \              \"op\": \"standardise\",\n                \"params\": {\n       \
  \           \"window\": 500,\n                  \"min_periods\": 120\n         \
  \       }\n              },\n              {\n                \"op\": \"signed_power\"\
  ,\n                \"params\": {\n                  \"exponent\": 2,\n         \
  \         \"pivot\": 10\n                }\n              }\n            ]\n   \
  \       },\n          {\n            \"id\": \"stretch_from_short_sma\",\n     \
  \       \"class\": \"strategies.strategy_components.MovingAverageDistanceComponent\"\
  ,\n            \"params\": {\n              \"period\": 24,\n              \"average\"\
  : \"sma\"\n            },\n            \"weight\": 1.0,\n            \"transforms\"\
  : [\n              {\n                \"op\": \"standardise\",\n               \
  \ \"params\": {\n                  \"window\": 500,\n                  \"min_periods\"\
  : 120\n                }\n              },\n              {\n                \"\
  op\": \"negate\"\n              },\n              {\n                \"op\": \"\
  signed_power\",\n                \"params\": {\n                  \"exponent\":\
  \ 2,\n                  \"pivot\": 10\n                }\n              }\n    \
  \        ]\n          }\n        ]\n      },\n      \"trending\": null,\n      \"\
  mean_reversion\": null,\n      \"chop\": null\n    },\n    \"sizing\": {\n     \
  \ \"kind\": \"vol_target\",\n      \"window\": 60,\n      \"target_annual_vol\"\
  : 0.2,\n      \"periods_per_year\": 8760,\n      \"max_allocation\": 2\n    }\n\
  \  }\n}"
- "Use EXACTLY this block manifest (JSON): run_101's block manifest, as config_vehicle.derived_manifest\
  \ gives it for this config (D-161).\n{\n  \"block\": {\n    \"kind\": \"forecast\"\
  ,\n    \"config_paths\": [\n      \"/strategies/regimes/unknown/components/0\",\n\
  \      \"/strategies/regimes/unknown/components/1\"\n    ]\n  },\n  \"scaffolding\"\
  : [\n    \"/regime_detector\",\n    \"/strategies/sizing\"\n  ],\n  \"rationale\"\
  : \"Component 0 is the SMA24/SMA168 trend spread and component 1 is the negated\
  \ distance of price from SMA24, which together are the trend-minus-stretch forecast.\
  \ The ungated detector and the vol-target sizing block only run and size it.\"\n\
  }"
evaluation:
  pass_rule:
    criteria:
    - id: forecast_ic_median
      horizon: 24
candidate:
  claim:
    statement: 'In this strategy, the forecast ranks forward returns positively over
      1, 6 and 24 bars on bars where its size is 6 or more. The rank IC grows with
      forecast size and is about zero on bars below 6. Shrinking small component readings
      with a graded dead zone, so the forecast is carried by its large readings, should
      therefore keep the edge and drop the low-information trades.

      '
    kind: conditional_behaviour
    tests:
    - name: large_forecast_ranks_returns
      selector:
        kind: event
        field: abs_forecast
        op: '>='
        value: 6
      outcome:
        kind: fwd_return
        horizons:
        - 1
        - 6
        - 24
      baseline: null
      statistic: rank_ic
      direction: greater
      floor:
        min_events: 100
        min_windows: 4
    pass_if: 'On the unseen fold, the rank IC of the forecast against forward returns
      on bars with |forecast| of 6 or more is positive at 1, 6 and 24 bars. It has
      the claimed sign in at least 4 windows at each horizon and at least 100 events.

      '
    fail_if: 'The rank IC on bars with |forecast| of 6 or more is zero or negative
      at any of 1, 6 or 24 bars, or has the claimed sign in fewer than 4 windows.

      '
    rationale: 'The forecast is the average of two standardised legs: a trend spread
      and a negated stretch from the short SMA. Where the legs agree the average is
      large, and there it predicts the next 1 to 24 bars (q12; the IC is higher still
      at |forecast| of <n> or more, q9). Where they cancel it is small, and the rank
      IC is about zero or negative (q8). The allocation follows the forecast, so the
      strategy trades heavily in that noisy zone and pays fees on it: window_economics
      (q4) shows gross per lot below zero in <n> of 6 windows and fees per lot above
      gross in all 6. A graded dead zone (signed_power, exponent 2) on each leg cuts
      the small readings and keeps the large ones. The edge does not last to <n> bars
      (q7), so the test stops at 24.

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
            weight: 1.0
            transforms:
            - op: standardise
              params:
                window: 500
                min_periods: 120
            - op: signed_power
              params:
                exponent: 2
                pivot: 10
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
            - op: signed_power
              params:
                exponent: 2
                pivot: 10
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
    rationale: Component 0 is the SMA24/SMA168 trend spread and component 1 is the
      negated distance of price from SMA24, which together are the trend-minus-stretch
      forecast. The ungated detector and the vol-target sizing block only run and
      size it.
  source:
    origin: reader
    proposal_ref: runs/run_101/artifacts/proposals/forecast_power.yaml#forecast_power-run_101-1
    source_run: run_101
    parent_hypothesis_id: SMA_PULLBACK_IN_TREND_24H_1H_BTC_FOLD_A
    hypothesis_id: SMA_PULLBACK_IN_TREND_24H_1H_BTC_FOLD_A__forecast_power-run_101-1
    decision_ref: runs/run_101/artifacts/decision_record.yaml
    proposal:
      kind: side_finding
      claim:
        statement: 'In this strategy, the forecast ranks forward returns positively
          over 1, 6 and 24 bars on bars where its size is 6 or more. The rank IC grows
          with forecast size and is about zero on bars below 6. Shrinking small component
          readings with a graded dead zone, so the forecast is carried by its large
          readings, should therefore keep the edge and drop the low-information trades.

          '
        kind: conditional_behaviour
        tests:
        - name: large_forecast_ranks_returns
          selector:
            kind: event
            field: abs_forecast
            op: '>='
            value: 6
          outcome:
            kind: fwd_return
            horizons:
            - 1
            - 6
            - 24
          baseline: null
          statistic: rank_ic
          direction: greater
          floor:
            min_events: 100
            min_windows: 4
        pass_if: 'On the unseen fold, the rank IC of the forecast against forward
          returns on bars with |forecast| of 6 or more is positive at 1, 6 and 24
          bars. It has the claimed sign in at least 4 windows at each horizon and
          at least 100 events.

          '
        fail_if: 'The rank IC on bars with |forecast| of 6 or more is zero or negative
          at any of 1, 6 or 24 bars, or has the claimed sign in fewer than 4 windows.

          '
        rationale: 'The forecast is the average of two standardised legs: a trend
          spread and a negated stretch from the short SMA. Where the legs agree the
          average is large, and there it predicts the next 1 to 24 bars (q12; the
          IC is higher still at |forecast| of <n> or more, q9). Where they cancel
          it is small, and the rank IC is about zero or negative (q8). The allocation
          follows the forecast, so the strategy trades heavily in that noisy zone
          and pays fees on it: window_economics (q4) shows gross per lot below zero
          in <n> of 6 windows and fees per lot above gross in all 6. A graded dead
          zone (signed_power, exponent 2) on each leg cuts the small readings and
          keeps the large ones. The edge does not last to <n> bars (q7), so the test
          stops at 24.

          '
      evidence:
      - q12:horizons.1.effect=0.0721
      - q12:horizons.1.windows_claimed_sign=6
      - q12:horizons.6.effect=0.0513
      - q12:horizons.24.effect=0.0711
      - q12:horizons.24.n_events=6636
      - q9:horizons.24.effect=0.112
      - q8:horizons.24.effect=-0.0117
      vehicle:
        kind: config
        config_sha256: 78dc78cfb970772689cf71015c8dbb40e4e0d39316b44d886fffab72552523ac
        config_ref: candidate.start_config
      combines_as: forecast_block
      fold_observed: A
    base_config_ref: runs/run_101/artifacts/variants/base/strategy_config.json
    start_config_sha256: 78dc78cfb970772689cf71015c8dbb40e4e0d39316b44d886fffab72552523ac
---

# forecast_power-run_101-1

Written by tools/decide_next.py (E-059, slice 6b) from runs/run_101/artifacts/proposals/forecast_power.yaml#forecast_power-run_101-1; decision record: runs/run_101/artifacts/decision_record.yaml.

This fold child keeps its source run's criteria (D-121): evaluation.pass_rule, re-resolved against config/criterion_menu.yaml when the run is registered. A patch's resolved config passes through to 1b (candidate.config), and 5a checks it against candidate.source.expected_config_sha256.
