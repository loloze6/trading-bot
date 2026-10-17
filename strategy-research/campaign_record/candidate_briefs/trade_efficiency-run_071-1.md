---
strategy_domain: short_horizon_reversal
market_universe:
- BTCUSDT
- ETHUSDT
timeframe: 1h
venue: kraken
product: perp
research_goal: 'Test a finding the trade_efficiency reader noticed after run_071 on
  idea HOURLY_SHOCK_CONTINUATION_MOMENTUM_1H_BTC_ETH: Marginal-conviction bars (forecast
  < 6) show no forward return advantage over baseline, contradicting a robust herding
  hypothesis and suggesting the tiny positive effect on high-conviction bars is concentrated
  in rare, extreme cases rather than a broad behavioral mechanism. Its claim block
  is pre-filled (candidate.claim). Evidence: claim_result_digest.variants.base.tests.continuation_by_conviction.horizons.4.effect
  = 0.000588; claim_result_digest.variants.base.tests.continuation_by_conviction.horizons.4.n_events
  = 1857; variants.base.slices.overall.per_trade_expectancy_bps.mean = -7.2731; variants.base.slices.overall.entry_efficiency_median
  = -0.025; variants.base.slices.overall.mae_mfe_ratio_median = 1.4853 It backtests
  on fold B (2018-01, 2018-09, 2019-05, 2020-01, 2020-09, 2021-05; config/folds.yaml),
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
    statement: Marginal-conviction bars (forecast < 6) show no forward return advantage
      over baseline, contradicting a robust herding hypothesis and suggesting the
      tiny positive effect on high-conviction bars is concentrated in rare, extreme
      cases rather than a broad behavioral mechanism.
    kind: conditional_behaviour
    tests:
    - name: marginal_conviction_continuation
      selector:
        kind: event
        field: forecast
        op: <
        value: 6
      outcome:
        kind: fwd_return
        horizons:
        - 1
        - 2
        - 3
        - 4
      baseline:
        kind: complement
      statistic: mean_diff
      direction: greater
      floor:
        min_events: 100
        min_windows: 3
      consistency:
        unit: window
        min_same_sign: 3
    pass_if: Marginal-conviction bars show mean forward returns not significantly
      different from or worse than complement bars at every horizon, consistent across
      at least 3 of 6 windows. If the effect is zero or negative, the signal selects
      random extreme close positions (intrabar noise) rather than genuine behavioral
      conviction.
    fail_if: Marginal-conviction bars show significantly HIGHER forward returns than
      complement bars at any horizon, indicating conviction level is not the limiting
      factor—execution lag and costs are. The herding hypothesis might yet hold if
      entry timing were improved.
    rationale: 'The claim shows tiny positive effects only on high-conviction bars
      (base H4: +0.588 bps). If marginal bars (one-third signal strength) also show
      positive effects, herding is robust across conviction levels. If marginal bars
      show zero or reversal, it reveals the signal is sampling random extremes (high
      and low close positions that are inherently noisier and mean-revert faster),
      not detecting genuine herding. This test distinguishes between weak-but-real
      continuation and pure noise selection.'
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
    proposal_ref: runs/run_071/artifacts/proposals/trade_efficiency.yaml#trade_efficiency-run_071-1
    source_run: run_071
    parent_hypothesis_id: HOURLY_SHOCK_CONTINUATION_MOMENTUM_1H_BTC_ETH
    hypothesis_id: HOURLY_SHOCK_CONTINUATION_MOMENTUM_1H_BTC_ETH__trade_efficiency-run_071-1
    decision_ref: runs/run_075/artifacts/decision_record.yaml
    proposal:
      kind: side_finding
      claim:
        statement: Marginal-conviction bars (forecast < 6) show no forward return
          advantage over baseline, contradicting a robust herding hypothesis and suggesting
          the tiny positive effect on high-conviction bars is concentrated in rare,
          extreme cases rather than a broad behavioral mechanism.
        kind: conditional_behaviour
        tests:
        - name: marginal_conviction_continuation
          selector:
            kind: event
            field: forecast
            op: <
            value: 6
          outcome:
            kind: fwd_return
            horizons:
            - 1
            - 2
            - 3
            - 4
          baseline:
            kind: complement
          statistic: mean_diff
          direction: greater
          floor:
            min_events: 100
            min_windows: 3
          consistency:
            unit: window
            min_same_sign: 3
        pass_if: Marginal-conviction bars show mean forward returns not significantly
          different from or worse than complement bars at every horizon, consistent
          across at least 3 of 6 windows. If the effect is zero or negative, the signal
          selects random extreme close positions (intrabar noise) rather than genuine
          behavioral conviction.
        fail_if: Marginal-conviction bars show significantly HIGHER forward returns
          than complement bars at any horizon, indicating conviction level is not
          the limiting factor—execution lag and costs are. The herding hypothesis
          might yet hold if entry timing were improved.
        rationale: 'The claim shows tiny positive effects only on high-conviction
          bars (base H4: +0.588 bps). If marginal bars (one-third signal strength)
          also show positive effects, herding is robust across conviction levels.
          If marginal bars show zero or reversal, it reveals the signal is sampling
          random extremes (high and low close positions that are inherently noisier
          and mean-revert faster), not detecting genuine herding. This test distinguishes
          between weak-but-real continuation and pure noise selection.'
      evidence:
      - claim_result_digest.variants.base.tests.continuation_by_conviction.horizons.4.effect
        = 0.000588
      - claim_result_digest.variants.base.tests.continuation_by_conviction.horizons.4.n_events
        = 1857
      - variants.base.slices.overall.per_trade_expectancy_bps.mean = -7.2731
      - variants.base.slices.overall.entry_efficiency_median = -0.025
      - variants.base.slices.overall.mae_mfe_ratio_median = 1.4853
    base_config_ref: runs/run_071/artifacts/variants/base/strategy_config.json
    start_config_sha256: 6cf77f4eef76884229ac1d4f72473a81329c50d0c15cb17df4effadf1cc27e98
---

# trade_efficiency-run_071-1

Written by tools/decide_next.py (E-059, slice 6b) from runs/run_071/artifacts/proposals/trade_efficiency.yaml#trade_efficiency-run_071-1; decision record: runs/run_075/artifacts/decision_record.yaml.

This brief carries no pass criteria on purpose (operator decision 2, 2026-09-24): step 1a writes a hypothesis card and criteria coherent with the proposed idea, from config/criterion_menu.yaml. A patch's resolved config passes through to 1b (candidate.config), and 5a checks it against candidate.source.expected_config_sha256.
