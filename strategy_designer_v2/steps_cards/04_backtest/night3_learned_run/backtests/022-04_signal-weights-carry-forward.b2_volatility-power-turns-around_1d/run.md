# Backtest of 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d

- Plan: `../../../../03_test_plan/night3_learned_run/plans/022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | 0.046527 | 1.068 |
| w2 | 22 | -0.031703 | -23.708 |
| w3 | 22 | 0.019707 | -8.453 |
| w4 | 17 | 0.148765 | 42.07 |
| w5 | 16 | 0.082898 | 4.927 |
| w6 | 24 | 0.061169 | 22.29 |
| w7 | 26 | 0.128436 | 20.678 |
| w8 | 35 | 0.109864 | 55.93 |
| w9 | 24 | -0.085883 | -10.228 |
| w10 | 27 | 0.046672 | 39.456 |
| w11 | 15 | -0.064954 | -22.017 |
| w12 | 36 | 0.062289 | 10.277 |
| w13 | 36 | 0.037821 | 1.114 |
| w14 | 19 | -0.127303 | -6.185 |
| w15 | 37 | -0.057327 | 13.052 |
| w16 | 33 | 0.136406 | 8.699 |
| w17 | 11 | -0.136752 | 13.912 |
| w18 | 25 | 0.050269 | 4.145 |
| w19 | 35 | 0.140022 | 18.773 |
| w20 | 16 | 0.04889 | 12.954 |
| w21 | 35 | -0.013722 | -32.944 |
| w22 | 35 | 0.087066 | 12.657 |
| w23 | 25 | -0.045339 | -9.633 |
| w24 | 27 | 0.04065 | -0.146 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | 0.098394 | 25.773 |
| w2 | 19 | -0.247803 | -27.097 |
| w3 | 31 | 0.006652 | -7.231 |
| w4 | 10 | 0.192561 | 37.549 |
| w5 | 20 | 0.171479 | 28.789 |
| w6 | 22 | 0.038219 | -4.254 |
| w7 | 28 | -0.046216 | -42.301 |
| w8 | 21 | 0.166001 | 56.522 |
| w9 | 20 | 0.140235 | 20.947 |
| w10 | 16 | 0.100287 | 54.247 |
| w11 | 10 | 0.098109 | 10.082 |
| w12 | 31 | 0.145028 | 21.158 |
| w13 | 24 | 0.244367 | 34.412 |
| w14 | 30 | -0.153995 | -55.12 |
| w15 | 7 | 0.209012 | 24.022 |
| w16 | 33 | -0.107429 | -45.325 |
| w17 | 5 | 0.032429 | 4.361 |
| w18 | 19 | -0.110598 | -44.18 |
| w19 | 36 | 0.127317 | 41.458 |
| w20 | 24 | 0.024677 | -0.413 |
| w21 | 37 | 0.007953 | -2.844 |
| w22 | 33 | 0.050225 | -14.323 |
| w23 | 16 | 0.076887 | 12.711 |
| w24 | 11 | 0.030979 | 2.081 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | 0.070603 | 28.842 |
| w2 | 29 | 0.040321 | 15.741 |
| w3 | 19 | 0.075678 | 6.146 |
| w4 | 8 | 0.108468 | 2.553 |
| w5 | 19 | 0.090983 | 14.209 |
| w6 | 18 | 0.024225 | 10.34 |
| w7 | 6 | 0.168541 | 18.44 |
| w8 | 29 | 0.197373 | 22.5 |
| w9 | 25 | 0.197927 | -13.656 |
| w10 | 16 | 0.013996 | 20.477 |
| w11 | 29 | 0.106677 | -4.397 |
| w12 | 32 | -0.133038 | -39.326 |
| w13 | 5 | 0.09305 | 4.127 |
| w14 | 16 | -0.100104 | -24.368 |
| w15 | 43 | -0.086642 | -23.664 |
| w16 | 27 | 0.022201 | 6.605 |
| w17 | 13 | 0.139762 | 16.335 |
| w18 | 35 | -0.023913 | -28.221 |
| w19 | 19 | -0.037918 | 2.158 |
| w20 | 24 | 0.075786 | 28.66 |
| w21 | 29 | 0.14718 | 38.026 |
| w22 | 20 | 0.162232 | 18.178 |
| w23 | 19 | -0.167397 | -37.691 |
| w24 | 32 | 0.056351 | 23.414 |

- XMRUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.019199 | 12.344 |
| w2 | 13 | -0.03298 | -6.096 |
| w3 | 16 | -0.010492 | -3.653 |
| w4 | 17 | 0.108353 | 16.408 |
| w5 | 42 | 0.082005 | 7.029 |
| w6 | 16 | 0.123159 | 38.339 |
| w8 | 33 | 0.119545 | 39.06 |
| w9 | 26 | 0.041093 | 23.813 |
| w10 | 19 | 0.050961 | 67.689 |
| w11 | 21 | 0.224881 | 3.643 |
| w12 | 14 | 0.052838 | 18.593 |
| w14 | 23 | -0.133398 | -41.555 |
| w15 | 27 | 0.001668 | -4.723 |
| w16 | 36 | -0.117705 | -60.489 |
| w17 | 9 | -0.036942 | -0.258 |
| w18 | 25 | -0.024123 | -24.236 |
| w19 | 33 | -0.090879 | -4.958 |
| w20 | 22 | 0.033556 | 2.32 |
| w21 | 24 | 0.005795 | -2.434 |
| w22 | 13 | -0.018505 | -2.046 |
| w23 | 21 | -0.005365 | 6.301 |
| w24 | 38 | 0.113003 | 35.406 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 483 warm-up bars -- required_bars=569. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=569. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 21 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.106168 | 18.277 |
| w2 | 15 | 0.123245 | 19.073 |
| w3 | 0 | 0.073304 | 0.0 |
| w4 | 0 | 0.038414 | 0.0 |
| w5 | 0 | -0.034269 | 0.0 |
| w6 | 6 | -0.048384 | 1.668 |
| w8 | 36 | 0.1027 | 16.284 |
| w9 | 35 | 0.167247 | 42.446 |
| w10 | 20 | -0.018052 | 38.353 |
| w11 | 24 | -0.033773 | 53.673 |
| w12 | 20 | -0.035733 | 13.905 |
| w15 | 32 | 0.042619 | -0.454 |
| w16 | 20 | 0.017486 | -0.713 |
| w17 | 28 | -0.213857 | -6.224 |
| w18 | 16 | -0.155077 | -35.008 |
| w19 | 19 | -0.066032 | -17.054 |
| w20 | 19 | 0.026809 | 3.76 |
| w21 | 33 | 0.158401 | -8.9 |
| w22 | 14 | 0.121298 | 9.955 |
| w23 | 4 | -0.152234 | -13.653 |
| w24 | 19 | 0.077519 | 14.8 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=569. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=569. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 470 warm-up bars -- required_bars=569. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | 0.136986 | 19.503 |
| w2 | 18 | -0.013258 | 2.717 |
| w3 | 16 | -0.014393 | 7.057 |
| w4 | 14 | 0.113248 | 15.095 |
| w5 | 35 | -0.096743 | -41.349 |
| w6 | 14 | 0.085336 | 38.984 |
| w8 | 26 | -0.084262 | -21.569 |
| w9 | 19 | 0.06736 | 15.962 |
| w10 | 29 | 0.18473 | 78.202 |
| w11 | 31 | 0.15267 | 23.483 |
| w12 | 22 | -0.061302 | -32.526 |
| w14 | 24 | -0.027503 | 34.145 |
| w15 | 30 | -0.060345 | -20.809 |
| w16 | 28 | 0.055612 | 9.554 |
| w17 | 11 | 0.045201 | 0.874 |
| w18 | 17 | -0.104571 | -49.95 |
| w19 | 20 | 0.064889 | 11.786 |
| w20 | 14 | 0.21345 | 16.892 |
| w21 | 21 | 0.146703 | 17.231 |
| w22 | 29 | 0.030154 | -2.262 |
| w23 | 31 | -0.03804 | -24.198 |
| w24 | 30 | 0.216079 | -1.227 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 548 warm-up bars -- required_bars=569. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=569. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

