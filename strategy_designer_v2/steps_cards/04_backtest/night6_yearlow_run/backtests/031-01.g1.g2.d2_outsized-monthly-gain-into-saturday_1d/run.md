# Backtest of 031-01.g1.g2.d2_outsized-monthly-gain-into-saturday_1d

- Plan: `../../../../03_test_plan/night6_yearlow_run/plans/031-01.g1.g2.d2_outsized-monthly-gain-into-saturday_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.001802 | -1.071 |
| w2 | 5 | -0.008833 | -1.968 |
| w3 | 2 | 0.035237 | 1.157 |
| w4 | 10 | -0.010915 | 6.088 |
| w5 | 3 | -0.003041 | -0.882 |
| w6 | 13 | -0.039602 | 1.104 |
| w7 | 5 | -0.0379 | -0.903 |
| w8 | 9 | 0.04565 | 6.575 |
| w9 | 3 | 0.063521 | -0.05 |
| w10 | 6 | 0.061958 | 10.101 |
| w11 | 9 | 0.015199 | 6.247 |
| w12 | 4 | -0.008714 | -0.565 |
| w13 | 3 | 0.082858 | 1.731 |
| w14 | 1 | -0.091101 | -2.813 |
| w15 | 13 | 0.065082 | 19.999 |
| w16 | 10 | -0.039877 | -6.867 |
| w17 | 11 | 0.052865 | 10.664 |
| w18 | 5 | 0.009472 | -0.042 |
| w19 | 8 | -0.090895 | -8.426 |
| w20 | 6 | 0.014728 | 0.795 |
| w21 | 9 | -0.088131 | -4.541 |
| w22 | 4 | -0.014195 | -0.926 |
| w23 | 8 | 0.002831 | -0.073 |
| w24 | 3 | 0.015007 | -0.142 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.018658 | 0.339 |
| w2 | 5 | -0.00227 | -1.555 |
| w3 | 3 | 0.056688 | 3.151 |
| w4 | 10 | -0.026146 | 0.547 |
| w5 | 3 | -0.02598 | -1.035 |
| w6 | 9 | -0.048367 | -2.772 |
| w7 | 1 | 0.087518 | 2.316 |
| w8 | 7 | 0.065376 | 4.593 |
| w9 | 1 | -0.030211 | -1.899 |
| w10 | 8 | 0.24417 | 34.995 |
| w11 | 13 | -0.051049 | 1.527 |
| w12 | 6 | -0.022644 | -1.069 |
| w13 | 4 | 0.077677 | 4.749 |
| w14 | 2 | -0.006742 | -0.574 |
| w15 | 5 | -0.016596 | -1.319 |
| w16 | 11 | 0.008171 | -1.018 |
| w17 | 7 | 0.096271 | 9.462 |
| w18 | 6 | 0.047963 | 6.391 |
| w19 | 7 | -0.047897 | -6.255 |
| w20 | 4 | 0.035017 | 1.691 |
| w21 | 7 | 0.055839 | 6.518 |
| w22 | 0 | -0.102033 | 0.0 |
| w23 | 11 | 0.004971 | 5.263 |
| w24 | 1 | 0.035389 | 0.294 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.030862 | 0.421 |
| w2 | 5 | 0.020689 | -0.132 |
| w3 | 8 | 0.014214 | 2.363 |
| w4 | 9 | 0.009292 | 0.723 |
| w5 | 4 | -0.008182 | -1.523 |
| w6 | 3 | 0.009333 | 0.667 |
| w7 | 1 | 0.118743 | 0.544 |
| w8 | 12 | 0.111843 | 18.178 |
| w9 | 2 | -0.013414 | -0.718 |
| w10 | 6 | 0.201214 | 14.743 |
| w11 | 9 | 0.082326 | 8.377 |
| w12 | 5 | 0.029685 | 0.999 |
| w13 | 0 | -0.012742 | 0.0 |
| w14 | 2 | -0.081993 | -3.549 |
| w15 | 6 | 0.029898 | 2.496 |
| w16 | 9 | -0.040021 | -5.715 |
| w17 | 9 | 0.126427 | 14.974 |
| w18 | 6 | -0.056176 | -5.233 |
| w19 | 6 | 0.049141 | 9.394 |
| w20 | 4 | 0.004901 | -0.478 |
| w21 | 9 | 0.068451 | 15.216 |
| w22 | 5 | -0.212163 | -13.206 |
| w23 | 10 | 0.103896 | 9.192 |
| w24 | 1 | 0.117595 | 0.71 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.033544 | 1.38 |
| w2 | 7 | -0.040433 | -5.327 |
| w3 | 4 | -0.028947 | -1.601 |
| w4 | 7 | 0.066474 | 5.636 |
| w5 | 4 | 0.041845 | 0.734 |
| w6 | 11 | -0.004627 | -2.775 |
| w7 | 2 | -0.010466 | -0.436 |
| w8 | 7 | -0.004362 | -0.782 |
| w9 | 4 | 0.057346 | 1.022 |
| w10 | 6 | 0.084561 | 8.709 |
| w11 | 10 | 0.166729 | 25.835 |
| w12 | 3 | -0.036216 | -0.666 |
| w14 | 4 | -0.007396 | -1.319 |
| w15 | 7 | -0.014034 | -2.239 |
| w16 | 11 | -0.039109 | -6.917 |
| w17 | 9 | 0.055861 | 6.132 |
| w18 | 8 | 0.0376 | 3.154 |
| w19 | 5 | -0.03209 | -5.245 |
| w20 | 10 | 0.139555 | 12.453 |
| w21 | 5 | -0.059109 | -3.396 |
| w22 | 5 | -0.152241 | -5.277 |
| w23 | 5 | 0.07664 | 5.997 |
| w24 | 11 | 0.14441 | 13.836 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=481. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 21 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.191187 | 5.112 |
| w2 | 0 | 0.054306 | 0.0 |
| w3 | 0 | -0.048839 | 0.0 |
| w4 | 0 | -0.082739 | 0.0 |
| w5 | 0 | -0.078908 | 0.0 |
| w6 | 4 | -0.015854 | -0.313 |
| w8 | 4 | -0.079659 | -5.316 |
| w9 | 4 | -0.037743 | -4.143 |
| w10 | 7 | 0.252871 | 24.889 |
| w11 | 9 | 0.032717 | 8.715 |
| w12 | 0 | 0.004183 | 0.0 |
| w15 | 6 | -0.077225 | -6.702 |
| w16 | 10 | -0.043308 | -7.538 |
| w17 | 6 | 0.338215 | 71.004 |
| w18 | 5 | 0.143353 | 9.448 |
| w19 | 4 | 0.033123 | 3.256 |
| w20 | 5 | 0.028587 | 2.189 |
| w21 | 8 | 0.247287 | 43.743 |
| w22 | 3 | -0.022105 | -1.02 |
| w23 | 3 | 0.006532 | 0.542 |
| w24 | 0 | 0.02096 | 0.0 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=481. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=481. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 470 warm-up bars -- required_bars=481. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.063962 | 3.903 |
| w2 | 3 | -0.018385 | -1.489 |
| w3 | 2 | -0.016665 | -0.877 |
| w4 | 5 | 0.008637 | 0.048 |
| w5 | 4 | -0.030814 | -2.96 |
| w6 | 8 | 0.026644 | 1.87 |
| w7 | 3 | 0.026586 | 0.857 |
| w8 | 7 | -0.082632 | -6.379 |
| w9 | 2 | -0.064978 | -1.225 |
| w10 | 7 | 0.227073 | 24.869 |
| w11 | 10 | 0.04269 | 8.84 |
| w12 | 6 | -0.006079 | -0.589 |
| w14 | 4 | -0.090355 | -1.582 |
| w15 | 8 | -0.020234 | -5.278 |
| w16 | 9 | -0.122534 | -12.843 |
| w17 | 2 | 0.190325 | 2.366 |
| w18 | 6 | -0.027499 | -3.813 |
| w19 | 4 | 0.132928 | 9.005 |
| w20 | 11 | 0.03914 | 5.162 |
| w21 | 9 | 0.001907 | 1.767 |
| w22 | 4 | -0.028195 | -1.205 |
| w23 | 6 | 0.147021 | 8.715 |
| w24 | 13 | 0.15354 | 32.511 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=481. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

