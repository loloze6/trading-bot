# Backtest of 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d

- Plan: `../../../../03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.077199 | -6.918 |
| w2 | 16 | -0.066715 | 12.262 |
| w3 | 34 | -0.182861 | -30.175 |
| w4 | 36 | 0.220493 | 40.744 |
| w5 | 33 | 0.120523 | 18.067 |
| w6 | 33 | 0.00453 | 11.867 |
| w7 | 21 | 0.131878 | 9.305 |
| w8 | 20 | 0.113391 | 73.616 |
| w9 | 22 | 0.220257 | 12.085 |
| w10 | 18 | -0.083698 | 43.535 |
| w11 | 31 | 0.162458 | 17.482 |
| w12 | 8 | 0.023108 | 0.211 |
| w13 | 29 | 0.045457 | -2.052 |
| w14 | 21 | -0.103852 | -3.575 |
| w15 | 46 | 0.091711 | -12.965 |
| w16 | 20 | -0.04531 | -13.011 |
| w17 | 29 | -0.075382 | 37.765 |
| w18 | 21 | -0.01086 | -16.065 |
| w19 | 50 | 0.095295 | 24.459 |
| w20 | 50 | 0.171698 | 32.331 |
| w21 | 46 | 0.162304 | 47.576 |
| w22 | 39 | -0.05461 | -19.967 |
| w23 | 29 | 0.180559 | 22.831 |
| w24 | 40 | 0.313259 | 61.833 |

- ETHUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 32 | -0.043933 | -9.503 |
| w2 | 51 | 0.013989 | 7.815 |
| w3 | 54 | -0.228501 | -43.695 |
| w4 | 21 | 0.123835 | 39.027 |
| w5 | 41 | 0.072003 | 11.128 |
| w6 | 36 | -0.004651 | -22.084 |
| w7 | 40 | -0.126419 | 19.086 |
| w8 | 24 | -0.05055 | 5.568 |
| w9 | 6 | 0.150691 | 3.425 |
| w10 | 23 | 0.031061 | 76.634 |
| w11 | 29 | 0.250525 | 14.394 |
| w12 | 10 | 0.140652 | 9.602 |
| w14 | 28 | -0.122716 | -3.02 |
| w15 | 20 | 0.04024 | 0.736 |
| w16 | 36 | 0.028029 | -1.182 |
| w17 | 22 | 0.020723 | 4.994 |
| w18 | 28 | 0.024884 | 31.798 |
| w19 | 43 | -0.101049 | -45.313 |
| w20 | 29 | 0.185785 | 36.412 |
| w21 | 17 | 0.031397 | 8.58 |
| w22 | 29 | 0.139697 | 34.622 |
| w23 | 32 | 0.026072 | -19.253 |
| w24 | 36 | 0.093647 | 15.732 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 873 warm-up bars -- required_bars=911. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | 0.007733 | -3.976 |
| w2 | 53 | -0.137617 | -33.742 |
| w3 | 28 | 0.021363 | 12.225 |
| w4 | 39 | 0.130446 | -0.044 |
| w5 | 34 | -0.004387 | -3.075 |
| w6 | 20 | 0.146277 | 13.797 |
| w7 | 28 | 0.174685 | -11.356 |
| w8 | 23 | 0.045651 | 54.12 |
| w9 | 8 | 0.202241 | 1.533 |
| w10 | 31 | 0.047281 | 41.85 |
| w11 | 22 | 0.212728 | 0.744 |
| w12 | 14 | 0.003053 | 3.055 |
| w13 | 14 | 0.029362 | -6.345 |
| w14 | 32 | -0.159295 | -11.4 |
| w15 | 11 | -0.035644 | -0.13 |
| w16 | 42 | 0.008739 | -6.026 |
| w17 | 31 | 0.078047 | 14.51 |
| w18 | 25 | 0.072441 | 27.318 |
| w19 | 28 | 0.193074 | 23.53 |
| w20 | 30 | 0.104902 | 0.145 |
| w21 | 52 | -0.007696 | -0.005 |
| w22 | 50 | 0.213449 | 71.542 |
| w23 | 21 | 0.230675 | 26.133 |
| w24 | 22 | -0.039608 | 1.329 |

- XMRUSD: 19 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | -0.0211 | -2.946 |
| w2 | 44 | -0.145349 | -44.121 |
| w3 | 30 | -0.1902 | -21.244 |
| w4 | 16 | 0.256113 | 7.516 |
| w5 | 40 | 0.136195 | 36.335 |
| w6 | 37 | 0.160879 | 6.11 |
| w9 | 38 | 0.193706 | 9.007 |
| w10 | 25 | -0.020167 | 46.778 |
| w11 | 39 | 0.06858 | -0.559 |
| w12 | 11 | 0.225229 | 16.314 |
| w16 | 50 | -0.059861 | -39.719 |
| w17 | 19 | 0.022152 | 14.196 |
| w18 | 42 | 0.132969 | 70.178 |
| w19 | 42 | -0.082473 | -10.519 |
| w20 | 28 | 0.191261 | 8.902 |
| w21 | 40 | 0.069855 | 11.551 |
| w22 | 47 | 0.223936 | 36.806 |
| w23 | 22 | -0.063304 | -35.808 |
| w24 | 61 | 0.157168 | 20.027 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 483 warm-up bars -- required_bars=911. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w8 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 728 warm-up bars -- required_bars=911. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=911. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 606 warm-up bars -- required_bars=911. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w15 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 848 warm-up bars -- required_bars=911. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 18 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | -0.041859 | -14.338 |
| w2 | 24 | -0.093859 | -18.676 |
| w3 | 0 | 0.153992 | 0.0 |
| w4 | 0 | 0.133744 | 0.0 |
| w5 | 0 | 0.03793 | 0.0 |
| w6 | 0 | 0.109732 | 0.0 |
| w10 | 40 | -0.015735 | 1.717 |
| w11 | 25 | 0.036615 | 25.031 |
| w12 | 20 | -0.083469 | -6.576 |
| w16 | 26 | 0.110437 | 26.332 |
| w17 | 29 | -0.178791 | -76.437 |
| w18 | 24 | 0.070137 | 10.785 |
| w19 | 0 | 0.022022 | 0.0 |
| w20 | 0 | 0.068706 | 0.0 |
| w21 | 24 | -0.026936 | 22.044 |
| w22 | 28 | 0.068302 | 16.0 |
| w23 | 39 | 0.067174 | -2.058 |
| w24 | 39 | 0.072371 | 27.459 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=911. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w8 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 592 warm-up bars -- required_bars=911. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w9 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 835 warm-up bars -- required_bars=911. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=911. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 470 warm-up bars -- required_bars=911. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w15 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 712 warm-up bars -- required_bars=911. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 20 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 36 | 0.003725 | 9.369 |
| w2 | 45 | 0.078531 | 15.769 |
| w3 | 44 | -0.030157 | -7.321 |
| w4 | 34 | 0.092885 | 26.276 |
| w5 | 36 | -0.279725 | -60.389 |
| w6 | 42 | 0.023116 | 17.303 |
| w9 | 16 | 0.108649 | -0.49 |
| w10 | 20 | 0.000937 | 16.576 |
| w11 | 67 | 0.019554 | 32.0 |
| w12 | 11 | 0.143002 | 6.738 |
| w15 | 19 | -0.071118 | -8.092 |
| w16 | 29 | -0.071332 | -37.177 |
| w17 | 41 | -0.185311 | -29.745 |
| w18 | 39 | 0.018036 | 0.324 |
| w19 | 23 | 0.107482 | 13.309 |
| w20 | 26 | 0.001507 | -14.7 |
| w21 | 52 | 0.038127 | 12.546 |
| w22 | 22 | 0.070709 | -1.392 |
| w23 | 28 | -0.016143 | -7.412 |
| w24 | 43 | -0.049558 | -41.879 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 548 warm-up bars -- required_bars=911. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w8 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 793 warm-up bars -- required_bars=911. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=911. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 671 warm-up bars -- required_bars=911. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

