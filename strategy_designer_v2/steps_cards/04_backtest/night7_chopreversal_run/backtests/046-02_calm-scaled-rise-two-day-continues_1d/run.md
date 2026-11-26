# Backtest of 046-02_calm-scaled-rise-two-day-continues_1d

- Plan: `../../../../03_test_plan/night7_chopreversal_run/plans/046-02_calm-scaled-rise-two-day-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 37 | 0.001752 | -9.751 |
| w2 | 22 | -0.026346 | -9.965 |
| w3 | 30 | 0.035733 | 6.106 |
| w4 | 41 | 0.065957 | 41.285 |
| w5 | 62 | -0.107187 | -25.921 |
| w6 | 27 | 0.022825 | 17.194 |
| w7 | 58 | 0.068159 | 11.677 |
| w8 | 42 | 0.032891 | 23.075 |
| w9 | 38 | -0.073838 | -15.957 |
| w10 | 41 | -0.038413 | 9.303 |
| w11 | 10 | -0.068918 | -2.539 |
| w12 | 35 | -0.111409 | -27.612 |
| w13 | 23 | -0.056862 | -5.286 |
| w14 | 36 | -0.022853 | -27.949 |
| w15 | 7 | 0.159779 | 31.215 |
| w16 | 32 | -0.049587 | -5.651 |
| w17 | 44 | -0.013277 | 20.577 |
| w18 | 19 | 0.105655 | 14.039 |
| w19 | 8 | 0.192384 | 39.494 |
| w20 | 19 | 0.035796 | 6.229 |
| w21 | 34 | 0.164152 | 53.643 |
| w22 | 31 | -0.026387 | -22.704 |
| w23 | 63 | -0.070794 | -1.82 |
| w24 | 25 | 0.063563 | -8.463 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 45 | 0.033391 | -7.164 |
| w2 | 5 | -0.173653 | -27.439 |
| w3 | 28 | 0.086427 | 7.163 |
| w4 | 69 | 0.063807 | 25.983 |
| w5 | 56 | -0.157073 | -26.431 |
| w6 | 40 | 0.008294 | 12.897 |
| w7 | 51 | -0.037105 | -15.42 |
| w8 | 34 | -0.128116 | -0.402 |
| w9 | 43 | -0.031346 | -5.785 |
| w10 | 43 | 0.059154 | 54.559 |
| w11 | 19 | -0.014491 | 17.134 |
| w12 | 49 | -0.076879 | -12.745 |
| w13 | 27 | -0.026336 | 0.296 |
| w14 | 11 | -0.091963 | -20.077 |
| w15 | 38 | 0.061115 | 12.177 |
| w16 | 28 | -0.000506 | 33.124 |
| w17 | 30 | 0.093736 | 18.779 |
| w18 | 25 | 0.004704 | 13.648 |
| w19 | 20 | 0.089905 | 40.158 |
| w20 | 13 | -0.018279 | 0.374 |
| w21 | 21 | 0.01379 | 11.792 |
| w22 | 10 | -0.084084 | -14.72 |
| w23 | 37 | 0.121627 | 48.725 |
| w24 | 27 | 0.018426 | -9.826 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 63 | -0.072347 | -28.198 |
| w2 | 26 | -0.069719 | -13.322 |
| w3 | 34 | 0.05325 | 18.148 |
| w4 | 49 | -0.042844 | -8.116 |
| w5 | 26 | 0.009321 | -0.847 |
| w6 | 60 | -0.05884 | -27.739 |
| w7 | 44 | -0.056695 | -20.977 |
| w8 | 16 | -0.004356 | 9.697 |
| w9 | 50 | -0.032677 | 1.187 |
| w10 | 57 | -0.19963 | -1.167 |
| w11 | 11 | 0.044803 | 6.043 |
| w12 | 40 | 0.075795 | 0.138 |
| w13 | 32 | -0.086592 | -7.546 |
| w14 | 28 | -0.111872 | -24.201 |
| w15 | 23 | 0.122995 | -3.711 |
| w16 | 38 | -0.055619 | 0.332 |
| w17 | 19 | 0.009791 | 1.678 |
| w18 | 26 | 0.042726 | 14.567 |
| w19 | 20 | 0.108487 | 17.612 |
| w20 | 26 | -0.066509 | -27.899 |
| w21 | 20 | 0.020217 | 7.026 |
| w22 | 2 | 0.003141 | -0.416 |
| w23 | 48 | 0.02302 | 4.985 |
| w24 | 30 | -0.144531 | -28.911 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.014639 | 3.683 |
| w2 | 25 | 0.005025 | -2.92 |
| w3 | 56 | -0.072774 | -5.811 |
| w4 | 61 | -0.005484 | -8.267 |
| w5 | 74 | 0.063933 | -7.585 |
| w6 | 56 | -0.06516 | 4.511 |
| w7 | 49 | -0.069015 | -14.986 |
| w8 | 54 | -0.042789 | 17.838 |
| w9 | 54 | -0.009095 | -21.727 |
| w10 | 62 | -0.133775 | 3.582 |
| w11 | 20 | -0.036124 | 28.294 |
| w12 | 46 | -0.015057 | -28.814 |
| w14 | 27 | -0.070055 | -23.939 |
| w15 | 29 | 0.170549 | 18.915 |
| w16 | 26 | -0.049629 | 20.118 |
| w17 | 43 | -0.093369 | -0.467 |
| w18 | 25 | 0.07574 | 18.869 |
| w19 | 2 | -0.017154 | -18.373 |
| w20 | 19 | -0.069395 | 0.721 |
| w21 | 31 | 0.168389 | 29.872 |
| w22 | 26 | -0.011363 | 9.758 |
| w23 | 28 | 0.107716 | 11.448 |
| w24 | 10 | -0.018903 | -1.85 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 46 | 0.048733 | -5.996 |
| w2 | 5 | -0.048231 | -9.453 |
| w3 | 0 | -0.029942 | 0.0 |
| w4 | 0 | -0.129542 | 0.0 |
| w5 | 13 | -0.038599 | -5.135 |
| w6 | 38 | 0.003138 | 30.157 |
| w8 | 47 | -0.15926 | -12.167 |
| w9 | 37 | -0.054247 | -10.988 |
| w10 | 46 | -0.002995 | 27.691 |
| w11 | 0 | None | 0.0 |
| w12 | 58 | -0.014926 | -16.377 |
| w14 | 30 | -0.003375 | 2.404 |
| w15 | 34 | 0.212601 | 47.011 |
| w16 | 15 | 0.080232 | 16.126 |
| w17 | 26 | 0.139436 | 56.365 |
| w18 | 30 | 0.16166 | 45.25 |
| w19 | 35 | -0.010203 | -5.489 |
| w20 | 32 | -0.18165 | -31.151 |
| w21 | 17 | 0.03642 | 44.333 |
| w22 | 3 | -0.022065 | -5.545 |
| w23 | 51 | 0.1112 | 50.686 |
| w24 | 37 | 0.026285 | -14.807 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 41 | 0.076508 | 10.425 |
| w2 | 26 | 0.098874 | 8.485 |
| w3 | 43 | -0.084101 | -32.568 |
| w4 | 62 | -0.128676 | -12.646 |
| w5 | 42 | -0.041768 | -21.358 |
| w6 | 69 | -0.09065 | -11.551 |
| w7 | 43 | 0.038929 | 0.387 |
| w8 | 47 | -0.020511 | 0.017 |
| w9 | 35 | 0.03437 | 7.537 |
| w10 | 40 | 0.038753 | 42.325 |
| w11 | 20 | 0.095886 | 35.226 |
| w12 | 29 | 0.055677 | 5.844 |
| w13 | 20 | 0.038939 | -1.131 |
| w14 | 36 | 0.034765 | -21.809 |
| w15 | 31 | 0.020445 | -1.46 |
| w16 | 0 | None | 0.0 |
| w17 | 29 | 0.056951 | 13.117 |
| w18 | 28 | -0.012936 | 4.81 |
| w19 | 0 | None | 0.0 |
| w20 | 18 | -0.052321 | -7.357 |
| w21 | 16 | 0.108993 | 16.44 |
| w22 | 3 | -0.076009 | -3.675 |
| w23 | 40 | 0.157343 | 13.026 |
| w24 | 10 | -0.071081 | -1.169 |

