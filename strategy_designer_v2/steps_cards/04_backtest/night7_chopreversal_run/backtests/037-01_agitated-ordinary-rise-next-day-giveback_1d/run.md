# Backtest of 037-01_agitated-ordinary-rise-next-day-giveback_1d

- Plan: `../../../../03_test_plan/night7_chopreversal_run/plans/037-01_agitated-ordinary-rise-next-day-giveback_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.095327 | -4.423 |
| w2 | 13 | 0.037904 | 3.548 |
| w3 | 14 | 0.04668 | 2.466 |
| w4 | 8 | -0.115243 | -5.692 |
| w5 | 0 | None | 0.0 |
| w6 | 24 | 0.117438 | -1.052 |
| w7 | 0 | None | 0.0 |
| w8 | 17 | 0.116853 | 2.416 |
| w9 | 9 | 0.070965 | 2.988 |
| w10 | 13 | -0.060906 | -4.086 |
| w11 | 26 | 0.034897 | -4.142 |
| w12 | 13 | -0.051797 | -2.967 |
| w13 | 22 | 0.074461 | 5.822 |
| w14 | 12 | 0.160101 | 10.773 |
| w15 | 38 | -0.028349 | -10.258 |
| w16 | 16 | 0.112179 | 7.677 |
| w17 | 18 | -0.105895 | -13.819 |
| w18 | 22 | 0.117565 | 7.727 |
| w19 | 34 | 0.035203 | -4.585 |
| w20 | 24 | 0.030655 | 1.594 |
| w21 | 18 | 0.054384 | -1.443 |
| w22 | 17 | -0.075622 | -4.373 |
| w23 | 3 | -0.029119 | -0.673 |
| w24 | 18 | 0.105016 | 6.62 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.02246 | 0.821 |
| w2 | 26 | 0.076351 | 8.978 |
| w3 | 17 | 0.159361 | 9.497 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 13 | 0.00406 | -3.248 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | -0.015972 | -0.864 |
| w9 | 5 | 0.115934 | 4.405 |
| w10 | 11 | 0.085462 | 1.441 |
| w11 | 23 | 0.048566 | -4.962 |
| w12 | 12 | -0.044551 | -2.772 |
| w13 | 17 | -0.029398 | -2.266 |
| w14 | 17 | 0.063125 | 3.937 |
| w15 | 18 | 0.093489 | 3.95 |
| w16 | 16 | -0.038634 | -5.406 |
| w17 | 20 | 0.005261 | -4.562 |
| w18 | 25 | 0.14528 | 8.414 |
| w19 | 26 | 0.035762 | -0.937 |
| w20 | 29 | 0.101875 | 8.28 |
| w21 | 26 | 0.019542 | -4.51 |
| w22 | 28 | -0.06491 | -2.136 |
| w23 | 10 | 0.095636 | -0.369 |
| w24 | 14 | 0.005578 | 2.535 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 21 | 0.025582 | 2.313 |
| w3 | 10 | 0.185053 | 7.286 |
| w4 | 8 | 0.076175 | 2.172 |
| w5 | 21 | -0.060759 | -8.93 |
| w6 | 2 | -0.223404 | -4.932 |
| w7 | 0 | None | 0.0 |
| w8 | 27 | 0.148829 | 2.008 |
| w9 | 0 | None | 0.0 |
| w10 | 6 | 0.125504 | 2.309 |
| w11 | 26 | 0.05553 | -1.175 |
| w12 | 16 | 0.032945 | 2.547 |
| w13 | 15 | -0.031453 | 0.004 |
| w14 | 9 | 0.085338 | 4.456 |
| w15 | 19 | 0.021417 | 0.296 |
| w16 | 13 | 0.062476 | 1.077 |
| w17 | 24 | -0.002371 | -5.78 |
| w18 | 20 | 0.179703 | 12.986 |
| w19 | 29 | 0.125811 | 6.603 |
| w20 | 23 | -0.065197 | -4.174 |
| w21 | 21 | 0.026882 | -4.55 |
| w22 | 41 | 0.02009 | 0.534 |
| w23 | 6 | 0.056416 | 1.161 |
| w24 | 18 | 0.061145 | 3.354 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | 0.011999 | -0.532 |
| w2 | 20 | -0.039411 | -4.134 |
| w3 | 11 | 0.003279 | -0.891 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 9 | -0.037155 | -5.448 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.026901 | -0.149 |
| w9 | 1 | 0.08913 | 0.491 |
| w10 | 4 | 0.178008 | 4.427 |
| w11 | 23 | -0.156317 | -21.447 |
| w12 | 9 | -0.035141 | -1.624 |
| w14 | 13 | 0.128769 | 8.264 |
| w15 | 17 | 0.036869 | 0.802 |
| w16 | 21 | 0.028094 | 2.369 |
| w17 | 17 | 0.069766 | -0.355 |
| w18 | 29 | 0.169255 | 10.44 |
| w19 | 35 | 0.017508 | -1.63 |
| w20 | 34 | 0.064527 | -4.163 |
| w21 | 21 | 0.004059 | -4.786 |
| w22 | 27 | 0.122798 | 1.389 |
| w23 | 13 | -0.012302 | -1.932 |
| w24 | 26 | -0.132158 | -16.055 |

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
| w1 | 2 | 0.130921 | 3.796 |
| w2 | 1 | 0.202498 | 10.927 |
| w3 | 0 | 0.028499 | 0.0 |
| w4 | 0 | 0.196896 | 0.0 |
| w5 | 9 | -0.013986 | -1.888 |
| w6 | 16 | 0.12113 | 5.394 |
| w8 | 2 | 0.011817 | 0.233 |
| w9 | 6 | -0.081821 | -1.706 |
| w10 | 6 | 0.066755 | 1.286 |
| w11 | 40 | -0.10626 | -25.563 |
| w12 | 1 | -0.083744 | -0.44 |
| w14 | 17 | -0.015701 | -1.478 |
| w15 | 13 | 0.021651 | 1.24 |
| w16 | 26 | 0.089569 | 4.101 |
| w17 | 17 | 0.026925 | 1.444 |
| w18 | 20 | 0.269203 | 13.652 |
| w19 | 18 | 0.089596 | 5.746 |
| w20 | 23 | -0.174225 | -16.581 |
| w21 | 25 | 0.041007 | -4.216 |
| w22 | 36 | -0.142417 | -12.725 |
| w23 | 4 | 0.029385 | 0.772 |
| w24 | 9 | -0.007304 | 0.12 |

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
| w1 | 10 | 0.024059 | 0.387 |
| w2 | 17 | 0.121064 | 6.492 |
| w3 | 9 | -0.140929 | -5.212 |
| w4 | 5 | -0.010316 | -0.675 |
| w5 | 13 | -0.136402 | -6.432 |
| w6 | 2 | 0.091042 | 0.717 |
| w7 | 4 | 0.047542 | 1.722 |
| w8 | 6 | 0.119237 | 1.349 |
| w9 | 12 | 0.169198 | 9.836 |
| w10 | 15 | 0.037401 | -0.999 |
| w11 | 30 | -0.00619 | -10.752 |
| w12 | 19 | -0.033329 | -3.119 |
| w13 | 19 | 0.169092 | 8.649 |
| w14 | 8 | 0.202404 | 8.654 |
| w15 | 10 | 0.166117 | 6.881 |
| w16 | 37 | 0.030823 | -7.049 |
| w17 | 22 | 0.054116 | 2.525 |
| w18 | 26 | 0.134614 | 10.165 |
| w19 | 32 | 0.032274 | 0.384 |
| w20 | 18 | 0.061123 | 1.081 |
| w21 | 20 | 0.059298 | -5.751 |
| w22 | 35 | -0.034649 | -2.902 |
| w23 | 7 | -0.032347 | -2.076 |
| w24 | 33 | -0.007958 | -16.07 |

