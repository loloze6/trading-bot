# Backtest of 022-03_combined-extremes-larger-moves_1d

- Plan: `../../../../03_test_plan/night3_learned_run/plans/022-03_combined-extremes-larger-moves_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.046374 | 4.692 |
| w2 | 30 | 0.033128 | -0.377 |
| w3 | 25 | 0.051024 | 11.572 |
| w4 | 40 | -0.131156 | -54.995 |
| w5 | 37 | -0.132021 | -18.108 |
| w6 | 16 | -0.355847 | -17.409 |
| w7 | 8 | -0.227062 | -4.197 |
| w8 | 34 | -0.14317 | -50.403 |
| w9 | 17 | -0.088161 | -21.462 |
| w10 | 38 | 0.019625 | -23.637 |
| w11 | 29 | -0.009292 | 22.553 |
| w12 | 20 | -0.027416 | -4.09 |
| w13 | 36 | -0.034443 | -7.991 |
| w14 | 16 | 0.110162 | 26.267 |
| w15 | 39 | -0.031953 | 25.451 |
| w16 | 18 | -0.120982 | -27.586 |
| w17 | 33 | -0.042934 | -29.621 |
| w18 | 27 | -0.075338 | -16.381 |
| w19 | 50 | -0.10691 | -10.632 |
| w20 | 26 | -0.158778 | -33.654 |
| w21 | 22 | 0.052788 | 0.001 |
| w22 | 25 | 0.096758 | 16.522 |
| w23 | 41 | -0.088975 | -6.049 |
| w24 | 33 | -0.089158 | -27.355 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 41 | -0.171449 | -22.274 |
| w2 | 30 | 0.221009 | 1.146 |
| w3 | 22 | -0.02398 | -5.02 |
| w4 | 23 | -0.055274 | -37.881 |
| w5 | 14 | 0.044925 | 0.132 |
| w6 | 31 | 0.019325 | -21.921 |
| w7 | 36 | -0.083943 | 11.168 |
| w8 | 29 | -0.130538 | -27.954 |
| w9 | 20 | -0.081765 | -10.383 |
| w10 | 47 | -0.066378 | -27.886 |
| w11 | 40 | -0.122819 | -29.675 |
| w12 | 32 | 0.010646 | 4.075 |
| w13 | 42 | 0.04121 | 6.893 |
| w14 | 29 | -0.002938 | 17.514 |
| w15 | 27 | -0.193551 | -14.239 |
| w16 | 31 | 0.021946 | 8.553 |
| w17 | 21 | -0.12161 | -2.651 |
| w18 | 54 | 0.105871 | 10.558 |
| w19 | 48 | -0.047097 | -20.52 |
| w20 | 22 | -0.120574 | -20.006 |
| w21 | 23 | 0.020679 | 2.271 |
| w22 | 26 | -0.161343 | -11.364 |
| w23 | 36 | -0.125523 | -2.067 |
| w24 | 15 | -0.094864 | -2.389 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 33 | -0.104962 | -23.877 |
| w2 | 21 | 0.141998 | -3.873 |
| w3 | 46 | -0.014703 | 21.356 |
| w4 | 52 | -0.113998 | -38.68 |
| w5 | 37 | 0.004618 | 11.379 |
| w6 | 25 | 0.093057 | 18.632 |
| w7 | 17 | -0.182426 | 4.605 |
| w8 | 32 | -0.080847 | -27.055 |
| w9 | 38 | -0.108378 | -0.289 |
| w10 | 33 | 0.053876 | -19.303 |
| w11 | 22 | -0.027552 | 12.295 |
| w12 | 23 | 0.116617 | 8.533 |
| w13 | 40 | -0.153134 | -10.744 |
| w14 | 24 | 0.062413 | 18.16 |
| w15 | 33 | 0.097657 | 28.932 |
| w16 | 36 | -0.025127 | -2.668 |
| w17 | 32 | -0.159653 | -28.859 |
| w18 | 39 | -0.038245 | -18.685 |
| w19 | 35 | 0.002179 | -31.951 |
| w20 | 29 | 0.030563 | 3.579 |
| w21 | 35 | -0.117016 | -66.428 |
| w22 | 52 | -0.049306 | -3.544 |
| w23 | 24 | 0.03467 | -2.382 |
| w24 | 46 | -0.006584 | 8.959 |

- XMRUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 45 | 0.053987 | -6.743 |
| w2 | 33 | 0.057381 | 12.325 |
| w3 | 43 | 0.208238 | 38.551 |
| w4 | 23 | -0.005691 | -10.857 |
| w5 | 29 | 0.06029 | 0.603 |
| w6 | 45 | 0.044809 | -4.33 |
| w8 | 23 | -0.059732 | -34.901 |
| w9 | 38 | -0.063685 | -15.395 |
| w10 | 29 | -0.050306 | -39.376 |
| w11 | 37 | 0.086727 | -0.962 |
| w12 | 41 | 0.036584 | -10.749 |
| w14 | 35 | 0.178367 | 43.2 |
| w15 | 16 | -0.074022 | -1.858 |
| w16 | 41 | 0.031721 | 20.752 |
| w17 | 13 | 0.069164 | -4.992 |
| w18 | 28 | 0.080913 | -22.231 |
| w19 | 45 | 0.256458 | 95.393 |
| w20 | 37 | 0.10899 | 2.056 |
| w21 | 28 | 0.136142 | -12.262 |
| w22 | 39 | 0.057323 | -3.532 |
| w23 | 54 | -0.205032 | -69.143 |
| w24 | 39 | -0.005751 | 27.424 |

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
| w1 | 8 | 0.112481 | 3.753 |
| w2 | 37 | 0.117637 | -4.86 |
| w3 | 0 | -0.036331 | 0.0 |
| w4 | 0 | 0.065611 | 0.0 |
| w5 | 0 | 0.048024 | 0.0 |
| w6 | 3 | 0.117436 | 0.006 |
| w8 | 29 | -0.018339 | -6.356 |
| w9 | 39 | 0.176077 | 3.013 |
| w10 | 29 | -0.115937 | -31.373 |
| w11 | 37 | 0.068753 | -33.87 |
| w12 | 20 | 0.003541 | -9.382 |
| w15 | 30 | -0.02216 | -8.385 |
| w16 | 36 | -0.042971 | -32.626 |
| w17 | 27 | 0.128922 | -38.372 |
| w18 | 10 | -0.115208 | 5.319 |
| w19 | 31 | 0.132958 | 19.06 |
| w20 | 36 | -0.01047 | -18.3 |
| w21 | 31 | -0.017529 | -19.332 |
| w22 | 47 | -0.198967 | -10.507 |
| w23 | 16 | -0.000342 | 11.199 |
| w24 | 39 | -0.093826 | -8.523 |

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
| w1 | 34 | -0.141737 | -26.114 |
| w2 | 24 | 0.092055 | -1.52 |
| w3 | 59 | 0.124505 | 11.276 |
| w4 | 49 | 0.058503 | -5.463 |
| w5 | 29 | 0.159904 | 40.278 |
| w6 | 55 | 0.073683 | -8.326 |
| w8 | 33 | -0.135243 | -31.391 |
| w9 | 14 | -0.158902 | -7.23 |
| w10 | 25 | -0.146437 | -13.249 |
| w11 | 52 | 0.015581 | -38.349 |
| w12 | 37 | 0.052876 | 13.55 |
| w14 | 31 | 0.08385 | -14.291 |
| w15 | 8 | -0.166041 | 3.457 |
| w16 | 34 | 0.027221 | 50.437 |
| w17 | 35 | -0.150361 | -16.716 |
| w18 | 40 | 0.139766 | 23.864 |
| w19 | 52 | 0.055162 | -7.254 |
| w20 | 43 | -0.061789 | -9.014 |
| w21 | 39 | -0.072844 | -7.626 |
| w22 | 27 | -0.173637 | -29.864 |
| w23 | 39 | 0.054588 | 10.686 |
| w24 | 22 | -0.023511 | -35.07 |

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

