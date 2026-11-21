# Backtest of 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e2_monthly-rise-carries-for-weeks_1h

- Plan: `../../../../03_test_plan/night3_1h_run/plans/018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e2_monthly-rise-carries-for-weeks_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | -0.011459 | -6.682 |
| w2 | 15 | 0.00843 | -20.063 |
| w3 | 13 | -0.02046 | -30.451 |
| w4 | 28 | 0.024241 | 110.061 |
| w5 | 24 | 0.013988 | 0.431 |
| w6 | 29 | 0.001168 | 82.048 |
| w7 | 18 | 0.0067 | -12.569 |
| w8 | 32 | -0.002475 | 37.4 |
| w9 | 10 | -0.024523 | -23.692 |
| w10 | 30 | 0.001876 | 40.817 |
| w11 | 25 | -0.018661 | 46.626 |
| w12 | 26 | 0.015915 | 9.101 |
| w13 | 18 | -0.020855 | -13.17 |
| w14 | 22 | -0.010463 | -58.765 |
| w15 | 38 | -0.01931 | 42.553 |
| w16 | 27 | 0.008244 | 30.808 |
| w17 | 36 | 0.031344 | 178.425 |
| w18 | 18 | 0.021225 | 4.296 |
| w19 | 32 | 0.020562 | 52.202 |
| w20 | 22 | -0.035837 | -13.52 |
| w21 | 24 | 0.002492 | 116.382 |
| w22 | 21 | -0.014191 | -12.257 |
| w23 | 27 | 0.008778 | 28.531 |
| w24 | 30 | 0.012254 | -17.167 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | -0.009515 | -3.622 |
| w2 | 11 | 0.025046 | 11.999 |
| w3 | 20 | -0.011475 | -24.392 |
| w4 | 24 | -0.004359 | 52.827 |
| w5 | 16 | -0.009803 | -7.212 |
| w6 | 18 | 0.01495 | 47.99 |
| w7 | 0 | 0.023394 | 0.0 |
| w8 | 19 | -0.027098 | 10.994 |
| w9 | 12 | -0.034097 | -29.834 |
| w10 | 27 | 0.001167 | 98.874 |
| w11 | 19 | -0.004537 | 134.629 |
| w12 | 21 | 0.007788 | 2.466 |
| w13 | 31 | 0.007725 | -5.016 |
| w14 | 0 | -0.028339 | 0.0 |
| w15 | 24 | 0.006821 | 15.689 |
| w16 | 21 | 0.013212 | 55.435 |
| w17 | 15 | 0.01326 | 84.577 |
| w18 | 21 | 0.011644 | 23.793 |
| w19 | 24 | 0.028732 | 68.585 |
| w20 | 15 | 0.004845 | -8.978 |
| w21 | 16 | 0.014517 | 64.183 |
| w22 | 1 | -0.017379 | -2.558 |
| w23 | 41 | 0.028451 | 113.821 |
| w24 | 18 | -0.01258 | -17.997 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.019627 | -20.629 |
| w2 | 7 | 0.010235 | 3.908 |
| w3 | 13 | -0.014133 | 9.397 |
| w4 | 27 | -0.009252 | -1.739 |
| w5 | 24 | -0.023715 | -26.491 |
| w6 | 14 | -0.047216 | 13.395 |
| w7 | 0 | 0.003939 | 0.0 |
| w8 | 25 | -0.016612 | 35.822 |
| w9 | 12 | -0.027202 | -28.799 |
| w10 | 26 | -0.002513 | 34.53 |
| w11 | 20 | -0.025781 | 35.966 |
| w12 | 25 | -0.005937 | -23.377 |
| w13 | 0 | -0.020967 | 0.0 |
| w14 | 0 | -0.027557 | 0.0 |
| w15 | 15 | 0.009887 | 17.279 |
| w16 | 20 | 0.01037 | 25.976 |
| w17 | 15 | 0.012257 | 99.987 |
| w18 | 24 | 0.01361 | -11.173 |
| w19 | 20 | 0.022624 | 22.729 |
| w20 | 19 | -0.026674 | -10.711 |
| w21 | 16 | 0.001416 | 130.864 |
| w22 | 8 | -0.025997 | -20.408 |
| w23 | 30 | 0.014538 | 25.121 |
| w24 | 17 | -0.035361 | -33.356 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | -0.009127 | -15.17 |
| w2 | 23 | -0.012806 | -14.605 |
| w3 | 17 | -0.015501 | -16.067 |
| w4 | 24 | -0.006817 | -1.843 |
| w5 | 23 | -0.003432 | -9.062 |
| w6 | 12 | -0.028813 | 25.694 |
| w7 | 0 | -0.006562 | 0.0 |
| w8 | 13 | -0.016924 | 23.489 |
| w9 | 12 | -0.008109 | -15.554 |
| w10 | 24 | -0.016207 | 46.96 |
| w11 | 14 | -0.011863 | 81.686 |
| w12 | 14 | -0.004344 | -13.058 |
| w14 | 0 | 0.002245 | 0.0 |
| w15 | 26 | -0.013056 | -5.223 |
| w16 | 29 | 0.000785 | 19.6 |
| w17 | 23 | 0.000398 | 47.793 |
| w18 | 19 | 0.004298 | -10.57 |
| w19 | 16 | -0.025407 | -29.509 |
| w20 | 17 | -0.013995 | 26.713 |
| w21 | 15 | -0.007183 | 11.896 |
| w22 | 19 | -0.014904 | 35.328 |
| w23 | 23 | 0.009482 | -12.093 |
| w24 | 7 | -0.041933 | 53.581 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 7757 warm-up bars -- required_bars=9600. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | -0.027623 | -21.072 |
| w2 | 0 | -0.001376 | 0.0 |
| w3 | 0 | 0.012511 | 0.0 |
| w4 | 0 | -0.010271 | 0.0 |
| w5 | 13 | 0.004068 | 14.581 |
| w6 | 22 | -0.004016 | 31.003 |
| w8 | 9 | -0.030596 | -8.84 |
| w9 | 10 | 0.008353 | -17.386 |
| w10 | 28 | 0.025272 | 45.397 |
| w11 | 31 | 0.014415 | 121.562 |
| w12 | 13 | -0.011873 | -10.147 |
| w14 | 0 | 0.003423 | 0.0 |
| w15 | 12 | 0.007006 | 1.293 |
| w16 | 15 | -0.001916 | 4.143 |
| w17 | 18 | 0.040014 | 149.269 |
| w18 | 20 | 0.02463 | 31.71 |
| w19 | 22 | 0.004687 | -10.759 |
| w20 | 20 | -0.017505 | 8.451 |
| w21 | 32 | 0.052237 | 269.156 |
| w22 | 27 | -0.013494 | -6.394 |
| w23 | 35 | 0.027277 | 33.691 |
| w24 | 13 | -0.005607 | -27.304 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 8280 warm-up bars -- required_bars=9600. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 5455 warm-up bars -- required_bars=9600. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.00254 | 38.087 |
| w2 | 11 | -0.001906 | -8.968 |
| w3 | 12 | -0.020107 | -20.803 |
| w4 | 17 | -0.020848 | -33.803 |
| w5 | 12 | 0.007178 | -15.802 |
| w6 | 10 | -0.033964 | -0.877 |
| w7 | 0 | -0.015954 | 0.0 |
| w8 | 10 | -0.000798 | 26.58 |
| w9 | 9 | -0.031735 | -12.228 |
| w10 | 21 | -0.023165 | 53.272 |
| w11 | 22 | -0.018314 | 99.527 |
| w12 | 17 | -0.007127 | -2.543 |
| w14 | 0 | -0.032262 | 0.0 |
| w15 | 17 | 0.000564 | -2.824 |
| w16 | 25 | 0.030018 | 90.344 |
| w17 | 14 | -0.018914 | -7.632 |
| w18 | 29 | 0.00545 | -6.187 |
| w19 | 14 | 0.007535 | 7.133 |
| w20 | 26 | -0.015823 | 8.827 |
| w21 | 18 | -0.00937 | 68.917 |
| w22 | 10 | -0.030438 | -11.351 |
| w23 | 20 | -0.004312 | -7.224 |
| w24 | 28 | 0.023714 | 550.186 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 9318 warm-up bars -- required_bars=9600. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

