---
strategy_domain: SMA trend
market_universe:
- BTCUSDT
timeframe: 1h
venue: kraken
product: perp
research_goal: 'Test a finding the trade_efficiency reader noticed after run_101 on
  idea SMA_PULLBACK_IN_TREND_24H_1H_BTC_FOLD_A: After bars whose past 168-hour return
  is in the top 20% of its trailing 500 bars, BTC returns over the next 6 and 24 hours
  are higher than on other bars. The slow trend leg therefore carries the persistent
  part of the forecast, and the negated 24-bar stretch leg, which bets on reversal,
  adds sign flips without a matching reversal edge. Its claim block is pre-filled
  (candidate.claim). Evidence: q19:horizons.6.effect=0.00086019856; q19:horizons.24.effect=0.0027784451;
  q19:horizons.6.windows_claimed_sign=5; q19:horizons.24.windows_claimed_sign=4 It
  backtests on fold B (2018-05, 2019-01, 2019-09, 2020-05, 2021-01, 2021-09; config/folds.yaml),
  drawn among the folds its source run run_101 is not on (B, C, D). It starts from
  run_101''s base config (candidate.start_config) with the finding''s config change:
  /strategies/regimes/unknown/components/1/weight -> 0.25; -- the block the claim
  is about.'
machine_constraints:
  protocol:
    symbols:
    - BTCUSDT
    timeframe: 1h
    start: '2018-05-01'
    end: '2021-12-31'
    window_months: 4
    fold: B
evaluation:
  pass_rule:
    criteria:
    - id: forecast_ic_median
      horizon: 24
candidate:
  claim:
    statement: 'After bars whose past 168-hour return is in the top 20% of its trailing
      500 bars, BTC returns over the next 6 and 24 hours are higher than on other
      bars. The slow trend leg therefore carries the persistent part of the forecast,
      and the negated 24-bar stretch leg, which bets on reversal, adds sign flips
      without a matching reversal edge.

      '
    kind: conditional_behaviour
    tests:
    - name: week_uptrend_continues
      selector:
        kind: quantile
        field: past_return
        bars: 168
        side: top
        q: 0.2
        lookback: 500
      outcome:
        kind: fwd_return
        horizons:
        - 6
        - 24
      baseline:
        kind: complement
      statistic: mean_diff
      direction: greater
      floor:
        min_events: 100
        min_windows: 4
    pass_if: 'On the unseen fold, the top 20% of 168-hour past returns have a higher
      mean forward return than other bars at both 6 and 24 hours. The effect has the
      claimed sign in at least 4 of the windows at each horizon, with at least 100
      events.

      '
    fail_if: 'The effect is lower than the baseline at 6 or 24 hours, or has the claimed
      sign in fewer than 4 windows.

      '
    rationale: 'Fees per lot exceed gross per lot in 5 of 6 windows (q2), and gross
      is negative in total. The median lot is held <n> bars, and the forecast changes
      sign often. The forecast ranks forward returns weakly positively (q9: rank IC
      <n> at 1 bar, <n> at 24 bars). The top and bottom forecast deciles show no consistent
      edge (q15, q16). Short lots lose more than long lots (q8). The strategy averages
      a trend leg (24/168 SMA spread) with a negated distance from the 24-bar SMA.
      The negated leg bets on reversal, and the data do not show a reversal. After
      a top-quintile 24-hour rise the mean forward return is higher than on other
      bars, not lower (q13), and after a top-quintile 168-hour rise it is higher at
      6 and 24 hours (q19). The negated stretch leg therefore fights the slower trend
      leg. It shortens the average holding and adds turnover, with no reversal edge
      to pay for it. Down-weighting that leg keeps the graded trend forecast and cuts
      the sign changes. Limits: this is a bar-level test on a proxy for the trend
      leg, and the effect is small. It does not isolate the stretch leg. The child
      run on the unseen fold is the real test.

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
          - id: stretch_from_short_sma
            class: strategies.strategy_components.MovingAverageDistanceComponent
            params:
              period: 24
              average: sma
            weight: 0.25
            transforms:
            - op: standardise
              params:
                window: 500
                min_periods: 120
            - op: negate
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
    proposal_ref: runs/run_101/artifacts/proposals/trade_efficiency.yaml#trade_efficiency-run_101-1
    source_run: run_101
    parent_hypothesis_id: SMA_PULLBACK_IN_TREND_24H_1H_BTC_FOLD_A
    hypothesis_id: SMA_PULLBACK_IN_TREND_24H_1H_BTC_FOLD_A__trade_efficiency-run_101-1
    decision_ref: runs/run_101/artifacts/decision_record.yaml
    proposal:
      kind: side_finding
      claim:
        statement: 'After bars whose past 168-hour return is in the top 20% of its
          trailing 500 bars, BTC returns over the next 6 and 24 hours are higher than
          on other bars. The slow trend leg therefore carries the persistent part
          of the forecast, and the negated 24-bar stretch leg, which bets on reversal,
          adds sign flips without a matching reversal edge.

          '
        kind: conditional_behaviour
        tests:
        - name: week_uptrend_continues
          selector:
            kind: quantile
            field: past_return
            bars: 168
            side: top
            q: 0.2
            lookback: 500
          outcome:
            kind: fwd_return
            horizons:
            - 6
            - 24
          baseline:
            kind: complement
          statistic: mean_diff
          direction: greater
          floor:
            min_events: 100
            min_windows: 4
        pass_if: 'On the unseen fold, the top 20% of 168-hour past returns have a
          higher mean forward return than other bars at both 6 and 24 hours. The effect
          has the claimed sign in at least 4 of the windows at each horizon, with
          at least 100 events.

          '
        fail_if: 'The effect is lower than the baseline at 6 or 24 hours, or has the
          claimed sign in fewer than 4 windows.

          '
        rationale: 'Fees per lot exceed gross per lot in 5 of 6 windows (q2), and
          gross is negative in total. The median lot is held <n> bars, and the forecast
          changes sign often. The forecast ranks forward returns weakly positively
          (q9: rank IC <n> at 1 bar, <n> at 24 bars). The top and bottom forecast
          deciles show no consistent edge (q15, q16). Short lots lose more than long
          lots (q8). The strategy averages a trend leg (24/168 SMA spread) with a
          negated distance from the 24-bar SMA. The negated leg bets on reversal,
          and the data do not show a reversal. After a top-quintile 24-hour rise the
          mean forward return is higher than on other bars, not lower (q13), and after
          a top-quintile 168-hour rise it is higher at 6 and 24 hours (q19). The negated
          stretch leg therefore fights the slower trend leg. It shortens the average
          holding and adds turnover, with no reversal edge to pay for it. Down-weighting
          that leg keeps the graded trend forecast and cuts the sign changes. Limits:
          this is a bar-level test on a proxy for the trend leg, and the effect is
          small. It does not isolate the stretch leg. The child run on the unseen
          fold is the real test.

          '
      evidence:
      - q19:horizons.6.effect=0.00086019856
      - q19:horizons.24.effect=0.0027784451
      - q19:horizons.6.windows_claimed_sign=5
      - q19:horizons.24.windows_claimed_sign=4
      config_change:
      - component_id: stretch_from_short_sma
        field: weight
        before: 1.0
        after: 0.25
      vehicle:
      - component_id: stretch_from_short_sma
        field: weight
        before: 1.0
        after: 0.25
      combines_as: forecast_block
      fold_observed: A
    base_config_ref: runs/run_101/artifacts/variants/base/strategy_config.json
    start_config_sha256: b0adcce3649ed9d17db07da9f572a7bdb298f7baa3bc22fe8b2fde61e3d92ea3
    config_change_ops:
    - path: /strategies/regimes/unknown/components/1/weight
      value: 0.25
---

# trade_efficiency-run_101-1

Written by tools/decide_next.py (E-059, slice 6b) from runs/run_101/artifacts/proposals/trade_efficiency.yaml#trade_efficiency-run_101-1; decision record: runs/run_101/artifacts/decision_record.yaml.

This fold child keeps its source run's criteria (D-121): evaluation.pass_rule, re-resolved against config/criterion_menu.yaml when the run is registered. A patch's resolved config passes through to 1b (candidate.config), and 5a checks it against candidate.source.expected_config_sha256.

PURPOSE
Branch 1 on the run_101 finding: the negated stretch leg adds sign changes without a reversal
edge. The run tests the same trend-minus-stretch forecast with the stretch leg at weight 0.25
on fold B, the fold the decision record drew. Step 2's split rule (D-195) adds the 0.125 variant.
The review reads, before the bars: sign changes per 100 bars, turnover, gross against fees, for
this run's base and its split variant against run_101's base; then each sub-forecast's IC and
pace from the analyst (D-193).

PRE-REGISTERED OUTCOMES
A. Grid passes on fold B and the claim confirms, and the book's fees fall below its gross with
   sign changes cut: the weight cut repairs the book. This config becomes the brief's base; the
   bars are read for branch 3.
B. Grid passes but the book still loses, fees at or above gross: the stretch leg was not the only
   fault. No further patch of this card (D-011); the next step is a new idea, the trend leg alone
   or the operator's daily-pace brief.
C. Grid fails on fold B: the card is refuted on a second fold and closes. Attention moves to the
   operator's daily-pace brief.
D. Claim refuted while the grid passes: the lens's proxy test was wrong; the vehicle is judged by
   the grid and the bars only, and the claim's lineage is not continued.
