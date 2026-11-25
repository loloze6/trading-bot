# Backtest of 039-01_agitated-swing-fall-low-close-rebound_1d

- Plan: `../../../../03_test_plan/night7_steadydecline_run/plans/039-01_agitated-swing-fall-low-close-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.054616 | -7.406 |
| w2 | 25 | 0.098022 | 3.194 |
| w3 | 22 | 0.210014 | 21.573 |
| w4 | 11 | 0.113552 | 12.786 |
| w5 | 0 | None | 0.0 |
| w6 | 24 | 0.223462 | 53.349 |
| w7 | 0 | None | 0.0 |
| w8 | 15 | 0.005674 | 0.945 |
| w9 | 16 | -0.0227 | -5.454 |
| w10 | 13 | 0.003116 | 9.338 |
| w11 | 33 | 0.093031 | 34.252 |
| w12 | 13 | 0.054103 | 5.702 |
| w13 | 36 | 0.036715 | 2.643 |
| w14 | 20 | 0.190098 | 21.096 |
| w15 | 39 | -0.082747 | -2.622 |
| w16 | 20 | 0.250015 | 28.243 |
| w17 | 19 | -0.008703 | 8.981 |
| w18 | 42 | 0.164759 | 28.411 |
| w19 | 41 | 0.027682 | 11.592 |
| w20 | 38 | 0.089825 | 8.525 |
| w21 | 17 | 0.06962 | 17.15 |
| w22 | 24 | 0.209396 | 29.661 |
| w23 | 2 | -0.04473 | -1.335 |
| w24 | 35 | 0.008116 | -11.428 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.145291 | -15.471 |
| w2 | 46 | 0.053958 | -9.085 |
| w3 | 23 | 0.276306 | 32.526 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 19 | 0.132946 | 25.605 |
| w7 | 0 | None | 0.0 |
| w8 | 20 | 0.188071 | 16.749 |
| w9 | 13 | 0.032505 | 0.663 |
| w10 | 15 | 0.061851 | 10.742 |
| w11 | 32 | 0.103021 | 47.642 |
| w12 | 9 | 0.052783 | 4.708 |
| w13 | 20 | -0.084554 | -16.549 |
| w14 | 36 | 0.180483 | 20.503 |
| w15 | 19 | 0.044911 | 6.482 |
| w16 | 29 | -0.01127 | -13.346 |
| w17 | 23 | -0.015287 | -1.909 |
| w18 | 36 | 0.062438 | 17.232 |
| w19 | 36 | -0.101621 | -12.915 |
| w20 | 41 | 0.157787 | 12.143 |
| w21 | 32 | 0.021279 | 8.96 |
| w22 | 45 | 0.122964 | 5.699 |
| w23 | 18 | 0.115068 | 29.534 |
| w24 | 23 | 0.028545 | -4.952 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 28 | 0.062358 | 1.596 |
| w3 | 19 | 0.129877 | 18.443 |
| w4 | 10 | 0.118865 | 9.68 |
| w5 | 23 | 0.028045 | -1.667 |
| w6 | 1 | 0.066606 | 2.334 |
| w7 | 0 | None | 0.0 |
| w8 | 42 | 0.069337 | 28.282 |
| w9 | 0 | None | 0.0 |
| w10 | 9 | 0.044429 | 4.646 |
| w11 | 42 | -0.086427 | -4.605 |
| w12 | 21 | -0.051843 | -12.415 |
| w13 | 24 | -0.093822 | -7.07 |
| w14 | 27 | 0.183957 | 18.155 |
| w15 | 30 | 0.150324 | 21.566 |
| w16 | 24 | 0.039133 | -9.322 |
| w17 | 26 | 0.074678 | 21.25 |
| w18 | 34 | 0.125073 | 18.405 |
| w19 | 33 | 0.140868 | 34.563 |
| w20 | 23 | 0.07889 | 0.947 |
| w21 | 34 | -0.015779 | -0.333 |
| w22 | 45 | 0.006033 | -4.346 |
| w23 | 13 | 0.067685 | 7.197 |
| w24 | 27 | -0.026162 | -9.582 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | -0.026312 | -11.046 |
| w2 | 28 | 0.008073 | -7.071 |
| w3 | 9 | 0.110186 | 7.704 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 9 | 0.021405 | 0.458 |
| w7 | 0 | None | 0.0 |
| w8 | 10 | 0.098984 | 5.55 |
| w9 | 2 | 0.034824 | 0.55 |
| w10 | 5 | 0.112101 | 9.995 |
| w11 | 38 | 0.021639 | 25.596 |
| w12 | 9 | -0.009508 | -5.673 |
| w14 | 28 | 0.127336 | 7.508 |
| w15 | 30 | 0.018034 | 1.125 |
| w16 | 32 | 0.066562 | 0.044 |
| w17 | 21 | 0.010765 | 0.802 |
| w18 | 35 | 0.206132 | 39.111 |
| w19 | 48 | 0.208079 | 38.459 |
| w20 | 26 | 0.142428 | 23.198 |
| w21 | 22 | 0.105273 | 16.834 |
| w22 | 23 | 0.032127 | 7.891 |
| w23 | 25 | -0.175811 | -28.831 |
| w24 | 35 | -0.08267 | -7.84 |

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
| w1 | 6 | 0.098475 | 3.783 |
| w2 | 0 | -0.025955 | 0.0 |
| w3 | 0 | 0.123569 | 0.0 |
| w4 | 0 | 0.07944 | 0.0 |
| w5 | 24 | -0.037821 | -0.45 |
| w6 | 16 | -0.027682 | 2.316 |
| w8 | 4 | 0.106242 | 4.22 |
| w9 | 12 | 0.084108 | 6.252 |
| w10 | 7 | 0.047617 | 5.359 |
| w11 | 47 | 0.003469 | 34.725 |
| w12 | 3 | -0.011968 | -0.893 |
| w14 | 20 | 0.075986 | 7.099 |
| w15 | 17 | 0.059458 | 5.513 |
| w16 | 39 | 0.011267 | -12.174 |
| w17 | 32 | -0.004414 | 4.479 |
| w18 | 28 | 0.124787 | 13.058 |
| w19 | 34 | -0.009917 | -7.343 |
| w20 | 28 | -0.029509 | -3.045 |
| w21 | 33 | -0.047383 | 19.809 |
| w22 | 44 | 0.026905 | -1.079 |
| w23 | 11 | 0.079085 | 8.416 |
| w24 | 12 | -0.001935 | -5.674 |

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
| w1 | 15 | 0.138642 | 13.241 |
| w2 | 33 | 0.084988 | 2.541 |
| w3 | 9 | 0.192543 | 15.23 |
| w4 | 6 | -0.029172 | -1.816 |
| w5 | 16 | 0.085812 | 7.295 |
| w6 | 10 | 0.110726 | 9.215 |
| w7 | 7 | -0.060863 | -7.152 |
| w8 | 9 | 0.17813 | 5.583 |
| w9 | 22 | 0.089372 | 2.719 |
| w10 | 18 | -0.086101 | -8.654 |
| w11 | 35 | -0.006922 | 22.537 |
| w12 | 27 | -0.002639 | -2.471 |
| w13 | 27 | 0.063504 | 4.816 |
| w14 | 22 | 0.156908 | 13.016 |
| w15 | 30 | 0.01442 | -5.255 |
| w16 | 45 | -0.03088 | 4.798 |
| w17 | 27 | 0.023435 | -5.188 |
| w18 | 37 | 0.195756 | 37.687 |
| w19 | 57 | 0.026844 | -10.065 |
| w20 | 39 | -0.099384 | -11.999 |
| w21 | 38 | -0.047247 | 3.047 |
| w22 | 42 | -0.094037 | -23.182 |
| w23 | 11 | -0.074466 | -7.882 |
| w24 | 38 | -0.117994 | 3.115 |

