# Backtest of 021-04_thin-cloud-downward-breakdown.d1_cloud-breakdown-after-deep-fall_1d

- Plan: `../../../../03_test_plan/night3_ichimoku_run/plans/021-04_thin-cloud-downward-breakdown.d1_cloud-breakdown-after-deep-fall_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.015684 | -2.938 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | 0.451455 | 4.954 |
| w4 | 2 | -0.047564 | -11.782 |
| w5 | 5 | 0.121433 | -7.524 |
| w6 | 0 | None | 0.0 |
| w7 | 2 | -0.064355 | 1.593 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | 0.001097 | -6.76 |
| w11 | 2 | -0.18797 | -11.202 |
| w12 | 2 | -0.009543 | 3.581 |
| w13 | 2 | 0.045615 | 2.551 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.000221 | 0.615 |
| w16 | 1 | 0.027913 | 14.397 |
| w17 | 2 | -0.05905 | -4.848 |
| w18 | 2 | -0.008307 | 33.074 |
| w19 | 4 | -0.015833 | -19.775 |
| w20 | 3 | 0.014811 | 0.359 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.076183 | 2.228 |
| w24 | 2 | -0.187021 | 8.171 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.071562 | 1.585 |
| w2 | 0 | None | 0.0 |
| w3 | 3 | -0.379949 | -6.494 |
| w4 | 2 | 0.031666 | -8.793 |
| w5 | 3 | 0.269075 | 11.727 |
| w6 | 0 | None | 0.0 |
| w7 | 2 | -0.225953 | 0.196 |
| w8 | 2 | 0.030693 | -2.512 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | -0.118175 | -16.86 |
| w13 | 2 | -0.202918 | -4.171 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.121535 | -3.315 |
| w16 | 1 | 0.582778 | 4.387 |
| w17 | 2 | -0.182743 | -4.227 |
| w18 | 3 | -0.246398 | 0.763 |
| w19 | 2 | -0.12293 | -0.081 |
| w20 | 2 | 0.194388 | -0.596 |
| w21 | 4 | -0.03898 | -21.469 |
| w22 | 2 | -0.041127 | 6.722 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | 0.056024 | 5.886 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.058597 | 1.94 |
| w2 | 0 | None | 0.0 |
| w3 | 4 | -0.182507 | -2.179 |
| w4 | 2 | 0.19322 | -5.323 |
| w5 | 10 | -0.039005 | -12.871 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.157443 | -2.717 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | -0.043394 | -0.427 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | 0.085458 | -8.165 |
| w13 | 2 | 0.018771 | 1.136 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.036699 | 2.979 |
| w16 | 1 | 0.017547 | 7.464 |
| w17 | 2 | -0.088047 | 1.288 |
| w18 | 2 | -0.169854 | 0.192 |
| w19 | 5 | -0.052789 | -8.109 |
| w20 | 0 | None | 0.0 |
| w21 | 4 | 0.03997 | -3.4 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.111471 | -0.02 |
| w24 | 4 | 0.089522 | 9.725 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | -0.14367 | 0.0 |
| w2 | 2 | 0.094895 | -5.081 |
| w3 | 4 | 0.309046 | -1.573 |
| w4 | 4 | -0.111796 | -0.571 |
| w5 | 3 | -0.070375 | -1.729 |
| w6 | 0 | None | 0.0 |
| w7 | 2 | 0.061724 | 7.45 |
| w8 | 2 | -0.020149 | -1.349 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 4 | -0.047113 | -33.547 |
| w12 | 5 | 0.108553 | 0.499 |
| w13 | 4 | -0.029956 | 4.449 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.049498 | -13.191 |
| w16 | 1 | 0.215416 | 7.994 |
| w17 | 2 | -0.114735 | -13.618 |
| w18 | 2 | -0.499806 | -12.424 |
| w19 | 10 | -0.389933 | -32.194 |
| w20 | 6 | -0.158319 | -10.707 |
| w21 | 5 | -0.03218 | -21.543 |
| w22 | 4 | 0.110813 | -11.509 |
| w23 | 2 | -0.028898 | -0.511 |
| w24 | 0 | -0.066053 | 0.0 |

- XRPUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.032328 | 1.125 |
| w2 | 0 | -0.024542 | 0.0 |
| w3 | 0 | 0.343154 | 0.0 |
| w4 | 2 | -0.038848 | -0.927 |
| w5 | 5 | -0.019117 | -63.269 |
| w6 | 0 | None | 0.0 |
| w7 | 2 | -0.055058 | 9.534 |
| w8 | 2 | 0.128418 | -0.294 |
| w9 | 2 | -0.018084 | 10.105 |
| w10 | 2 | -0.059944 | 0.566 |
| w11 | 2 | 0.037313 | -10.436 |
| w12 | 6 | -0.029191 | 2.031 |
| w14 | 2 | 0.006227 | 2.914 |
| w15 | 0 | -0.05014 | 0.0 |
| w16 | 2 | -0.042137 | 7.386 |
| w17 | 3 | 0.136335 | 3.246 |
| w18 | 0 | -0.130976 | 0.0 |
| w19 | 4 | -0.062857 | 10.026 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.108373 | 2.995 |
| w23 | 5 | 0.071688 | -27.11 |
| w24 | 4 | -0.093193 | 7.083 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=327. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.036379 | -23.371 |
| w2 | 1 | -0.002254 | 0.035 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | -0.060756 | 5.206 |
| w5 | 1 | 0.214337 | 5.575 |
| w6 | 5 | -0.128093 | -8.363 |
| w7 | 2 | -0.116354 | 6.317 |
| w8 | 2 | 0.084137 | -1.31 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | 0.03219 | -2.092 |
| w13 | 2 | -0.105052 | 2.283 |
| w14 | 2 | -0.039193 | 23.738 |
| w15 | 1 | 0.075719 | 10.48 |
| w16 | 1 | 0.036297 | 5.097 |
| w17 | 3 | 0.253345 | 9.3 |
| w18 | 2 | -0.274456 | -0.958 |
| w19 | 2 | -0.035869 | 7.139 |
| w20 | 2 | 0.028215 | -6.884 |
| w21 | 2 | 0.114244 | 2.497 |
| w22 | 4 | 0.058632 | 0.605 |
| w23 | 2 | 0.045481 | -4.914 |
| w24 | 2 | -0.04775 | -2.038 |

