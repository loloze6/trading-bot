# Backtest of 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d3_combined-score-in-uptrends_1d

- Plan: `../../../../03_test_plan/night3_learned_run/plans/022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d3_combined-score-in-uptrends_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.061541 | -4.329 |
| w2 | 18 | 0.071136 | 16.709 |
| w3 | 15 | 0.038969 | 9.337 |
| w4 | 46 | -0.10974 | -47.589 |
| w5 | 23 | -0.07172 | -9.455 |
| w6 | 43 | -0.240905 | -37.02 |
| w7 | 16 | -0.056527 | -7.122 |
| w8 | 25 | -0.109746 | -51.498 |
| w9 | 16 | 0.110215 | 1.969 |
| w10 | 49 | 0.056307 | -24.062 |
| w11 | 50 | -0.041177 | 18.228 |
| w12 | 23 | -0.012828 | -5.266 |
| w13 | 14 | 0.072054 | 17.092 |
| w14 | 13 | -0.028314 | -9.579 |
| w15 | 48 | -0.023056 | 40.554 |
| w16 | 23 | -0.060773 | -4.282 |
| w17 | 46 | -0.109145 | -50.435 |
| w18 | 27 | 0.003627 | -1.101 |
| w19 | 39 | -0.162513 | -25.048 |
| w20 | 20 | 0.001407 | -0.349 |
| w21 | 35 | -0.052834 | -1.418 |
| w22 | 18 | -0.098452 | 15.125 |
| w23 | 54 | -0.086171 | -20.325 |
| w24 | 20 | -0.000922 | -1.301 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 33 | 0.018301 | -4.186 |
| w2 | 7 | 0.216762 | 42.999 |
| w3 | 13 | -0.002561 | -6.104 |
| w4 | 21 | -0.006199 | -37.106 |
| w5 | 18 | 0.048977 | 7.283 |
| w6 | 46 | 0.026278 | -32.181 |
| w7 | 13 | 0.021758 | 5.588 |
| w8 | 25 | -0.007644 | -21.194 |
| w9 | 18 | -0.098119 | -9.194 |
| w10 | 43 | -0.041638 | -33.931 |
| w11 | 51 | -0.169567 | -41.717 |
| w12 | 40 | -0.075455 | -13.739 |
| w13 | 29 | 0.121246 | 12.169 |
| w14 | 11 | 0.01636 | 4.612 |
| w15 | 38 | -0.1995 | -28.158 |
| w16 | 42 | -0.03842 | 15.175 |
| w17 | 37 | -0.097176 | -16.164 |
| w18 | 37 | 0.23224 | 25.994 |
| w19 | 41 | -0.183183 | -43.657 |
| w20 | 11 | 0.027243 | -9.565 |
| w21 | 48 | -0.105067 | -17.25 |
| w22 | 1 | 0.071765 | -0.026 |
| w23 | 31 | -0.117473 | 37.1 |
| w24 | 10 | -0.037595 | -0.28 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.031932 | -21.299 |
| w2 | 17 | 0.09014 | 10.256 |
| w3 | 29 | 0.020486 | 23.14 |
| w4 | 47 | -0.012154 | -30.679 |
| w5 | 25 | 0.209354 | 34.219 |
| w6 | 37 | 0.08545 | 8.369 |
| w7 | 9 | -0.079295 | 0.9 |
| w8 | 33 | -0.075842 | -31.344 |
| w9 | 8 | 0.040938 | 20.919 |
| w10 | 37 | 0.035788 | -17.763 |
| w11 | 49 | -0.0724 | -4.529 |
| w12 | 27 | 0.148249 | 18.918 |
| w13 | 18 | -0.0703 | 0.384 |
| w14 | 6 | -0.02956 | -9.237 |
| w15 | 25 | 0.121028 | 17.278 |
| w16 | 34 | -0.029491 | -2.382 |
| w17 | 37 | -0.126463 | -38.274 |
| w18 | 20 | 0.022295 | -18.162 |
| w19 | 43 | -0.024269 | -34.112 |
| w20 | 14 | -0.135051 | -7.266 |
| w21 | 51 | -0.134473 | -65.136 |
| w22 | 28 | -0.003726 | 8.13 |
| w23 | 34 | 0.040222 | -11.205 |
| w24 | 12 | -0.052169 | 4.563 |

- XMRUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 45 | 0.021077 | 13.376 |
| w2 | 29 | 0.133074 | 58.239 |
| w3 | 20 | 0.131342 | 31.982 |
| w4 | 33 | 8.8e-05 | -14.878 |
| w5 | 19 | -0.021142 | -5.223 |
| w6 | 48 | 0.103592 | -13.122 |
| w8 | 31 | -0.065086 | -35.464 |
| w9 | 14 | -0.183636 | -17.402 |
| w10 | 28 | -0.002407 | -38.856 |
| w11 | 53 | -0.036398 | -14.89 |
| w12 | 27 | -0.059212 | -12.147 |
| w14 | 16 | -0.039902 | -14.915 |
| w15 | 30 | 0.012991 | 0.484 |
| w16 | 37 | -0.074756 | -18.385 |
| w17 | 38 | 0.07921 | -14.444 |
| w18 | 26 | 0.0458 | 6.482 |
| w19 | 13 | 0.190012 | 17.6 |
| w20 | 35 | 0.050208 | -7.371 |
| w21 | 40 | 0.087247 | -23.471 |
| w22 | 44 | 0.056859 | -18.223 |
| w23 | 35 | -0.225572 | -59.477 |
| w24 | 60 | -0.112761 | 18.044 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 483 warm-up bars -- required_bars=546. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=546. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 21 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | 0.02048 | -1.121 |
| w2 | 0 | 0.117321 | 0.0 |
| w3 | 0 | -0.133645 | 0.0 |
| w4 | 0 | 0.073112 | 0.0 |
| w5 | 0 | 0.113928 | 0.0 |
| w6 | 15 | 0.028567 | 4.472 |
| w8 | 24 | 0.077678 | 3.787 |
| w9 | 21 | 0.043812 | -4.296 |
| w10 | 39 | -0.143439 | -39.175 |
| w11 | 33 | -0.043946 | -45.608 |
| w12 | 11 | -0.001509 | -11.879 |
| w15 | 14 | -0.098257 | -25.08 |
| w16 | 28 | -0.062668 | -28.694 |
| w17 | 26 | -0.022246 | -58.784 |
| w18 | 21 | 0.085207 | 19.616 |
| w19 | 18 | 0.158997 | 11.155 |
| w20 | 21 | -0.069698 | -28.417 |
| w21 | 30 | -0.019294 | -23.404 |
| w22 | 23 | -0.067785 | -6.13 |
| w23 | 39 | 0.043082 | 17.595 |
| w24 | 4 | -0.015205 | -5.552 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=546. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=546. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 470 warm-up bars -- required_bars=546. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | -0.043302 | -3.86 |
| w2 | 21 | -0.079033 | -7.333 |
| w3 | 11 | 0.090579 | 16.65 |
| w4 | 31 | 0.122935 | 1.644 |
| w5 | 15 | -0.00618 | 7.41 |
| w6 | 41 | 0.096877 | -12.9 |
| w7 | 19 | -0.107718 | -23.188 |
| w8 | 24 | -0.046278 | -32.637 |
| w9 | 11 | -0.147661 | -22.625 |
| w10 | 63 | -0.200707 | -14.862 |
| w11 | 55 | 0.060568 | -53.433 |
| w12 | 27 | 0.085749 | 31.227 |
| w14 | 6 | -0.087855 | -22.87 |
| w15 | 22 | -0.144472 | -12.935 |
| w16 | 37 | 0.021812 | 32.459 |
| w17 | 28 | -0.035374 | -10.734 |
| w18 | 26 | 0.105103 | 21.969 |
| w19 | 19 | -0.029467 | -8.621 |
| w20 | 40 | -0.068316 | -18.342 |
| w21 | 34 | -0.057198 | -5.493 |
| w22 | 18 | -0.096513 | -30.344 |
| w23 | 30 | 0.017372 | 5.231 |
| w24 | 37 | -0.040696 | -28.008 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=546. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

