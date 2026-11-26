# Backtest of 061-01.d1_calm-big-up-day-long-only_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/061-01.d1_calm-big-up-day-long-only_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | 0.001752 | -16.104 |
| w2 | 17 | -0.026346 | -31.412 |
| w3 | 26 | 0.035733 | -26.054 |
| w4 | 31 | 0.065957 | 61.499 |
| w5 | 47 | -0.107187 | -27.978 |
| w6 | 17 | 0.022825 | 37.087 |
| w7 | 38 | 0.068159 | 0.225 |
| w8 | 26 | 0.032891 | 53.088 |
| w9 | 24 | -0.073838 | -10.384 |
| w10 | 27 | -0.038413 | 22.266 |
| w11 | 7 | -0.068918 | -10.677 |
| w12 | 30 | -0.111409 | -27.961 |
| w13 | 7 | -0.056862 | 8.761 |
| w14 | 29 | -0.022853 | -41.847 |
| w15 | 7 | 0.159779 | 49.13 |
| w16 | 20 | -0.049587 | -2.104 |
| w17 | 22 | -0.013277 | 94.096 |
| w18 | 12 | 0.105655 | 20.233 |
| w19 | 7 | 0.192384 | 40.973 |
| w20 | 14 | 0.035796 | -6.057 |
| w21 | 23 | 0.164152 | 50.75 |
| w22 | 23 | -0.026387 | -15.948 |
| w23 | 48 | -0.070794 | 6.72 |
| w24 | 22 | 0.063563 | -7.147 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | 0.033391 | 4.257 |
| w2 | 6 | -0.173653 | -34.183 |
| w3 | 20 | 0.086427 | -28.911 |
| w4 | 42 | 0.063807 | 40.068 |
| w5 | 38 | -0.157073 | -20.135 |
| w6 | 29 | 0.008294 | 29.383 |
| w7 | 35 | -0.037105 | -36.088 |
| w8 | 22 | -0.128116 | 23.498 |
| w9 | 32 | -0.031346 | -21.121 |
| w10 | 28 | 0.059154 | 100.256 |
| w11 | 9 | -0.014491 | 25.795 |
| w12 | 28 | -0.076879 | -8.332 |
| w13 | 15 | -0.026336 | -1.615 |
| w14 | 9 | -0.091963 | -37.233 |
| w15 | 22 | 0.061115 | 41.529 |
| w16 | 14 | -0.000506 | 86.95 |
| w17 | 17 | 0.093736 | 51.558 |
| w18 | 16 | 0.004704 | 32.009 |
| w19 | 12 | 0.089905 | 77.96 |
| w20 | 11 | -0.018279 | -12.657 |
| w21 | 17 | 0.01379 | 6.14 |
| w22 | 7 | -0.084084 | -21.766 |
| w23 | 27 | 0.121627 | 75.435 |
| w24 | 21 | 0.018426 | -14.311 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | -0.072347 | -24.243 |
| w2 | 21 | -0.069719 | -31.834 |
| w3 | 27 | 0.05325 | -2.698 |
| w4 | 32 | -0.042844 | 4.662 |
| w5 | 18 | 0.009321 | -14.896 |
| w6 | 47 | -0.05884 | -5.547 |
| w7 | 33 | -0.056695 | -28.007 |
| w8 | 12 | -0.004356 | 17.563 |
| w9 | 36 | -0.032677 | -14.028 |
| w10 | 31 | -0.19963 | 35.735 |
| w11 | 8 | 0.044803 | 16.766 |
| w12 | 29 | 0.075795 | -9.263 |
| w13 | 16 | -0.086592 | -12.465 |
| w14 | 24 | -0.111872 | -37.197 |
| w15 | 16 | 0.122995 | -5.351 |
| w16 | 26 | -0.055619 | 32.183 |
| w17 | 15 | 0.009791 | 26.028 |
| w18 | 12 | 0.042726 | 26.531 |
| w19 | 14 | 0.108487 | 9.776 |
| w20 | 18 | -0.066509 | -37.293 |
| w21 | 23 | 0.020217 | 17.305 |
| w22 | 2 | 0.003141 | -8.452 |
| w23 | 38 | 0.02302 | 18.134 |
| w24 | 22 | -0.144531 | -25.142 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.014639 | -8.388 |
| w2 | 15 | 0.005025 | -4.58 |
| w3 | 39 | -0.072774 | -17.789 |
| w4 | 30 | -0.005484 | 17.89 |
| w5 | 49 | 0.063933 | -14.506 |
| w6 | 31 | -0.06516 | 9.374 |
| w7 | 41 | -0.069015 | -23.283 |
| w8 | 34 | -0.042789 | 33.602 |
| w9 | 40 | -0.009095 | -21.861 |
| w10 | 36 | -0.133775 | 30.97 |
| w11 | 4 | -0.036124 | 39.392 |
| w12 | 37 | -0.015057 | -30.884 |
| w14 | 24 | -0.070055 | -41.948 |
| w15 | 16 | 0.170549 | 29.995 |
| w16 | 19 | -0.049629 | 53.914 |
| w17 | 23 | -0.093369 | 14.7 |
| w18 | 16 | 0.07574 | 19.706 |
| w19 | 2 | -0.017154 | -19.827 |
| w20 | 15 | -0.069395 | 5.438 |
| w21 | 23 | 0.168389 | 43.124 |
| w22 | 18 | -0.011363 | 20.184 |
| w23 | 20 | 0.107716 | -2.317 |
| w24 | 11 | -0.018903 | -3.206 |

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
| w1 | 31 | 0.048733 | 6.297 |
| w2 | 4 | -0.048231 | -26.507 |
| w3 | 0 | -0.029942 | 0.0 |
| w4 | 0 | -0.129542 | 0.0 |
| w5 | 10 | -0.038599 | 33.994 |
| w6 | 28 | 0.003138 | 38.485 |
| w8 | 34 | -0.15926 | -7.246 |
| w9 | 30 | -0.054247 | -15.634 |
| w10 | 31 | -0.002995 | 56.421 |
| w11 | 0 | None | 0.0 |
| w12 | 39 | -0.014926 | -19.812 |
| w14 | 25 | -0.003375 | 23.433 |
| w15 | 23 | 0.212601 | 6.838 |
| w16 | 12 | 0.080232 | 10.824 |
| w17 | 18 | 0.139436 | 233.737 |
| w18 | 19 | 0.16166 | 52.397 |
| w19 | 18 | -0.010203 | 8.083 |
| w20 | 18 | -0.18165 | -17.718 |
| w21 | 12 | 0.03642 | 82.439 |
| w22 | 3 | -0.022065 | -15.189 |
| w23 | 36 | 0.1112 | 33.78 |
| w24 | 31 | 0.026285 | -13.81 |

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
| w1 | 31 | 0.076508 | 4.642 |
| w2 | 14 | 0.098874 | 7.443 |
| w3 | 36 | -0.084101 | -51.658 |
| w4 | 32 | -0.128676 | -1.766 |
| w5 | 27 | -0.041768 | -45.634 |
| w6 | 41 | -0.09065 | 2.938 |
| w7 | 32 | 0.038929 | -22.839 |
| w8 | 33 | -0.020511 | 33.925 |
| w9 | 25 | 0.03437 | 6.791 |
| w10 | 27 | 0.038753 | 69.176 |
| w11 | 13 | 0.095886 | 34.753 |
| w12 | 17 | 0.055677 | -8.686 |
| w13 | 15 | 0.038939 | 2.859 |
| w14 | 23 | 0.034765 | -34.926 |
| w15 | 25 | 0.020445 | -12.489 |
| w16 | 0 | None | 0.0 |
| w17 | 23 | 0.056951 | 7.46 |
| w18 | 16 | -0.012936 | 19.827 |
| w19 | 0 | None | 0.0 |
| w20 | 14 | -0.052321 | 0.285 |
| w21 | 13 | 0.108993 | 23.531 |
| w22 | 3 | -0.076009 | -12.796 |
| w23 | 29 | 0.157343 | 9.62 |
| w24 | 7 | -0.071081 | 57.354 |

