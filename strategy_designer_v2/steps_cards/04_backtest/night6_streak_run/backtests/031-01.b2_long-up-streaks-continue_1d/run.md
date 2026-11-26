# Backtest of 031-01.b2_long-up-streaks-continue_1d

- Plan: `../../../../03_test_plan/night6_streak_run/plans/031-01.b2_long-up-streaks-continue_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 57 | -0.010893 | -20.015 |
| w2 | 50 | -0.032863 | -14.116 |
| w3 | 59 | 0.004957 | -16.93 |
| w4 | 62 | 0.138624 | 107.899 |
| w5 | 67 | 0.001354 | -5.643 |
| w6 | 64 | 0.009695 | 98.939 |
| w7 | 49 | 0.138605 | 7.081 |
| w8 | 58 | -0.077557 | 35.055 |
| w9 | 54 | -0.019014 | -21.119 |
| w10 | 72 | -0.141345 | 31.984 |
| w11 | 56 | -0.048461 | 37.338 |
| w12 | 68 | -0.041087 | -20.17 |
| w13 | 54 | -0.043085 | -7.096 |
| w14 | 59 | -0.01839 | -47.097 |
| w15 | 42 | 0.163162 | 58.338 |
| w16 | 53 | -0.09279 | -8.443 |
| w17 | 59 | 0.071073 | 114.458 |
| w18 | 55 | -0.075357 | -12.013 |
| w19 | 50 | 0.053227 | 38.785 |
| w20 | 49 | -0.036228 | -0.993 |
| w21 | 53 | 0.005859 | 58.534 |
| w22 | 60 | -0.08592 | -13.87 |
| w23 | 58 | 0.005536 | 4.108 |
| w24 | 59 | 0.024558 | -34.181 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 51 | 0.047752 | -18.77 |
| w2 | 47 | -0.004542 | -16.991 |
| w3 | 47 | -0.044606 | -8.566 |
| w4 | 43 | 0.024421 | 47.09 |
| w5 | 67 | -0.058944 | -20.576 |
| w6 | 52 | 0.007861 | 35.628 |
| w7 | 39 | 0.088053 | -15.193 |
| w8 | 50 | -0.155391 | -10.868 |
| w9 | 49 | 0.009647 | 0.377 |
| w10 | 41 | 0.063844 | 90.974 |
| w11 | 63 | -0.093816 | 58.166 |
| w12 | 60 | -0.055821 | -6.383 |
| w13 | 47 | 0.140983 | 30.36 |
| w14 | 44 | -0.032964 | -24.772 |
| w15 | 48 | 0.06834 | 17.264 |
| w16 | 47 | -0.047419 | 11.382 |
| w17 | 53 | -0.017503 | 33.698 |
| w18 | 48 | -0.047338 | 0.462 |
| w19 | 64 | -0.018501 | 11.544 |
| w20 | 64 | -0.05078 | -5.26 |
| w21 | 52 | -0.01728 | 37.54 |
| w22 | 48 | -0.144241 | -46.161 |
| w23 | 52 | 0.000646 | 93.364 |
| w24 | 48 | 0.092373 | -19.088 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 37 | -0.087086 | -15.361 |
| w2 | 47 | -0.074439 | -19.696 |
| w3 | 48 | 0.018484 | 3.141 |
| w4 | 51 | -0.042903 | -7.437 |
| w5 | 52 | 0.079671 | -7.138 |
| w6 | 46 | 0.023946 | 5.356 |
| w7 | 43 | -0.063161 | -30.285 |
| w8 | 38 | 0.009281 | 39.359 |
| w9 | 53 | -0.054613 | -18.56 |
| w10 | 62 | -0.260625 | 19.109 |
| w11 | 57 | 0.054115 | 48.367 |
| w12 | 62 | 0.045682 | 0.88 |
| w13 | 42 | -0.135491 | -21.933 |
| w14 | 35 | -0.105899 | -53.08 |
| w15 | 51 | 0.012091 | -19.863 |
| w16 | 42 | -0.094691 | -4.28 |
| w17 | 52 | -0.058834 | 30.258 |
| w18 | 40 | -0.099124 | -11.714 |
| w19 | 46 | -0.028521 | 19.334 |
| w20 | 51 | 0.006769 | -22.567 |
| w21 | 72 | -0.144891 | 25.182 |
| w22 | 56 | 0.050092 | -14.103 |
| w23 | 53 | -0.072733 | -6.01 |
| w24 | 58 | -0.113693 | -47.662 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 47 | -0.058926 | 8.402 |
| w2 | 52 | -0.06713 | -21.25 |
| w3 | 62 | -0.165144 | -20.388 |
| w4 | 70 | -0.148917 | -20.129 |
| w5 | 60 | 0.099351 | 4.604 |
| w6 | 66 | -0.096224 | 19.145 |
| w7 | 36 | -0.063884 | -32.237 |
| w8 | 49 | -0.192914 | 7.063 |
| w9 | 52 | -0.016774 | -38.651 |
| w10 | 56 | -0.1733 | 15.779 |
| w11 | 58 | -0.045402 | 55.886 |
| w12 | 68 | -0.090785 | -41.236 |
| w14 | 48 | -0.195528 | -56.895 |
| w15 | 39 | 0.057828 | 10.893 |
| w16 | 46 | -0.062196 | 19.372 |
| w17 | 58 | -0.215617 | 2.166 |
| w18 | 47 | -0.120461 | -16.418 |
| w19 | 64 | -0.036743 | -26.243 |
| w20 | 50 | -0.096484 | 16.022 |
| w21 | 61 | -0.016237 | 15.718 |
| w22 | 61 | 0.00454 | 30.145 |
| w23 | 60 | 0.03492 | -14.751 |
| w24 | 59 | -0.013253 | 27.539 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=457. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 43 | 0.067309 | 0.324 |
| w2 | 12 | -0.075943 | -31.527 |
| w3 | 0 | -0.096276 | 0.0 |
| w4 | 0 | -0.170993 | 0.0 |
| w5 | 5 | -0.076945 | -5.563 |
| w6 | 44 | 0.031074 | 42.946 |
| w8 | 53 | -0.216637 | -30.584 |
| w9 | 41 | -0.001437 | -9.897 |
| w10 | 53 | -0.054933 | 34.012 |
| w11 | 46 | -0.064723 | 95.22 |
| w12 | 42 | -0.113152 | -30.282 |
| w14 | 48 | 0.148901 | 23.249 |
| w15 | 46 | 0.075678 | 11.258 |
| w16 | 40 | -0.058011 | -13.623 |
| w17 | 57 | 0.041597 | 75.77 |
| w18 | 44 | -0.155977 | -13.341 |
| w19 | 55 | -0.127208 | -25.736 |
| w20 | 51 | 0.026926 | 25.025 |
| w21 | 47 | 0.194834 | 166.155 |
| w22 | 42 | -0.026941 | -4.794 |
| w23 | 61 | 0.046548 | 10.584 |
| w24 | 54 | -0.020286 | -32.524 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=457. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=457. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 48 | 0.001599 | 4.556 |
| w2 | 45 | -0.007241 | -19.813 |
| w3 | 53 | -0.028892 | -38.478 |
| w4 | 48 | -0.041907 | -6.501 |
| w5 | 64 | 3.6e-05 | -33.878 |
| w6 | 62 | -0.061193 | 3.758 |
| w7 | 42 | 0.02172 | -23.568 |
| w8 | 36 | -0.162726 | -6.634 |
| w9 | 43 | 0.086527 | 3.211 |
| w10 | 55 | -0.125225 | 3.333 |
| w11 | 41 | 0.149402 | 133.185 |
| w12 | 58 | 0.044789 | 21.862 |
| w14 | 46 | -0.035346 | -57.168 |
| w15 | 47 | -0.058779 | -11.815 |
| w16 | 48 | 0.021691 | 30.155 |
| w17 | 39 | -0.062245 | -17.773 |
| w18 | 53 | -0.134436 | -14.863 |
| w19 | 39 | 0.031222 | -16.632 |
| w20 | 47 | 0.039111 | 15.479 |
| w21 | 50 | 0.08827 | 59.133 |
| w22 | 39 | 0.016805 | -22.523 |
| w23 | 53 | 0.038394 | -3.69 |
| w24 | 53 | 0.125127 | 176.002 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=457. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

