---
strategy_domain: time_series_trend
market_universe:
- BTCUSDT
- ETHUSDT
- LTCUSDT
timeframe: 1d
venue: kraken
product: perp
research_goal: 'Re-run of run_089''s strategy, unchanged, on fold D (2024-01, 2024-05,
  2024-09, 2025-01, 2025-05, 2025-09; config/folds.yaml), branch 3 only, by the operator''s
  refold command (D-122). The source run''s goal, written for its own fold: Lane 1
  v3, design run, shorter lookback: does the v2 daily trend signal (distance from
  SMA(50), vol-targeted, long or flat) earn more than its costs on unseen data, fold
  B (six 4-month blocks of 2018-2021), on an equal-weight basket of 3 Kraken coins?
  Fold A (2022-2023, runs 081-083) FAILED its pre-registered rule; the failure''s
  label "cost binds" was an artefact of the lot-based ratio, and at position size
  costs were 13-26% of gross (D-107). Who pays: trend in crypto is attributed to slow-moving
  and constrained flows (retail herding, leverage liquidation cascades, scheduled
  rebalancers). Why not arbitraged: trend is a premium for bearing crash and whipsaw
  risk; whether it shows on bars this signal has never been run on is what this run
  measures.'
constraints:
- "Build EXACTLY this strategy config (JSON): run_089's authored base config (runs/run_089/artifacts/backtest_spec.yaml),\
  \ unchanged.\n{\n  \"regime_detector\": {\n    \"mode\": \"threshold_rules\",\n\
  \    \"components\": [],\n    \"rules\": [],\n    \"default_regime\": \"unknown\"\
  \n  },\n  \"strategies\": {\n    \"regimes\": {\n      \"unknown\": {\n        \"\
  components\": [\n          {\n            \"id\": \"trend\",\n            \"class\"\
  : \"strategies.strategy_components.MovingAverageDistanceComponent\",\n         \
  \   \"params\": {\n              \"period\": 50,\n              \"average\": \"\
  sma\"\n            },\n            \"weight\": 1.0,\n            \"transforms\"\
  : [\n              {\n                \"op\": \"scale\",\n                \"params\"\
  : {\n                  \"factor\": 5\n                }\n              },\n    \
  \          {\n                \"op\": \"clip\",\n                \"params\": {\n\
  \                  \"min\": 0,\n                  \"max\": 10\n                }\n\
  \              },\n              {\n                \"op\": \"vol_target\",\n  \
  \              \"params\": {\n                  \"window\": 60,\n              \
  \    \"target_annual_vol\": 0.4,\n                  \"periods_per_year\": 365\n\
  \                }\n              },\n              {\n                \"op\": \"\
  clip\",\n                \"params\": {\n                  \"min\": 0,\n        \
  \          \"max\": 10\n                }\n              }\n            ]\n    \
  \      }\n        ]\n      },\n      \"trending\": null,\n      \"mean_reversion\"\
  : null,\n      \"chop\": null\n    }\n  }\n}"
- "Use EXACTLY this block manifest (JSON): run_089's block manifest (runs/run_089/artifacts/block_manifest.yaml),\
  \ unchanged.\n{\n  \"block\": {\n    \"kind\": \"forecast\",\n    \"config_paths\"\
  : [\n      \"/strategies/regimes/unknown/components/0\"\n    ]\n  },\n  \"scaffolding\"\
  : [\n    \"/regime_detector\"\n  ],\n  \"rationale\": \"The MovingAverageDistanceComponent\
  \ with its transform pipeline (scaling, clipping, vol-targeting) is the core hypothesis\
  \ implementing the SMA(50) distance trend-following signal. The ungated regime detector\
  \ is scaffolding required to execute the signal on every bar unconditionally.\"\n\
  }"
machine_constraints:
  protocol:
    symbols:
    - BTCUSDT
    - ETHUSDT
    - LTCUSDT
    timeframe: 1d
    fold: D
    start: '2024-01-01'
    end: '2025-12-31'
    window_months: 4
refold:
  source_run: run_089
  fold: D
---

# Refold: run_089 on fold D

Written by `run_campaign.py refold` (D-122). Branch 3 only: run_089's card, config, block manifest and pass_rule, unchanged, backtested on fold D; no model call, no readers, no decide-next after it.
