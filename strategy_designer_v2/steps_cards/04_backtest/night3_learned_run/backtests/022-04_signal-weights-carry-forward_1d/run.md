# Backtest of 022-04_signal-weights-carry-forward_1d

- Plan: `../../../../03_test_plan/night3_learned_run/plans/022-04_signal-weights-carry-forward_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | -0.020844 | -5.865 |
| w2 | 51 | 0.028372 | 2.04 |
| w3 | 58 | 0.062342 | 11.039 |
| w4 | 39 | -0.14801 | -44.27 |
| w5 | 34 | -0.175466 | -9.204 |
| w6 | 48 | -0.147335 | -28.967 |
| w7 | 38 | -0.172266 | -6.175 |
| w8 | 46 | -0.193271 | -39.646 |
| w9 | 43 | 0.005642 | -15.167 |
| w10 | 60 | 0.13345 | -19.608 |
| w11 | 43 | -0.084906 | 10.68 |
| w12 | 55 | -0.039871 | -5.233 |
| w13 | 30 | -0.089629 | -13.065 |
| w14 | 31 | 0.110606 | 24.7 |
| w15 | 46 | 0.006321 | 9.725 |
| w16 | 33 | -0.167193 | -19.409 |
| w17 | 55 | -0.027428 | -41.29 |
| w18 | 59 | -0.107018 | -17.872 |
| w19 | 66 | -0.071143 | -4.38 |
| w20 | 37 | -0.252088 | -25.699 |
| w21 | 35 | -0.082213 | -4.33 |
| w22 | 38 | 0.13172 | 2.063 |
| w23 | 52 | 0.017445 | -0.375 |
| w24 | 54 | -0.067755 | 6.822 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 58 | -0.10898 | -20.703 |
| w2 | 42 | 0.160324 | -2.177 |
| w3 | 26 | 0.081705 | 5.482 |
| w4 | 31 | -0.171884 | -19.62 |
| w5 | 45 | -0.116776 | -17.433 |
| w6 | 57 | 0.02326 | -9.154 |
| w7 | 57 | -0.052521 | 19.591 |
| w8 | 45 | -0.14133 | -16.107 |
| w9 | 37 | -0.074169 | -8.77 |
| w10 | 29 | -0.038028 | -17.634 |
| w11 | 50 | -0.151926 | -27.064 |
| w12 | 63 | -0.04261 | 0.757 |
| w13 | 72 | -0.016287 | -1.637 |
| w14 | 50 | 0.064692 | 43.544 |
| w15 | 40 | -0.156932 | -18.717 |
| w16 | 48 | -0.024678 | 4.706 |
| w17 | 39 | -0.030594 | 1.818 |
| w18 | 43 | 0.128055 | 11.408 |
| w19 | 58 | -0.086577 | -14.611 |
| w20 | 36 | -0.160503 | -13.412 |
| w21 | 36 | -0.110003 | -14.112 |
| w22 | 41 | -0.11471 | -3.736 |
| w23 | 34 | -0.117141 | 16.37 |
| w24 | 49 | -0.085507 | 1.968 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 51 | 0.005102 | -14.808 |
| w2 | 50 | 0.184307 | -8.695 |
| w3 | 57 | -0.023885 | -14.035 |
| w4 | 40 | -0.078411 | -18.778 |
| w5 | 59 | 0.055906 | 33.578 |
| w6 | 58 | 0.102163 | 9.7 |
| w7 | 54 | -0.207258 | 8.32 |
| w8 | 43 | -0.183232 | -29.995 |
| w9 | 25 | -0.19882 | -3.161 |
| w10 | 43 | 0.146628 | -12.799 |
| w11 | 52 | -0.114892 | -5.955 |
| w12 | 50 | 0.066025 | -2.287 |
| w13 | 49 | -0.178266 | -7.584 |
| w14 | 45 | 0.152773 | 35.457 |
| w15 | 39 | 0.080007 | 5.238 |
| w16 | 52 | -0.008613 | -7.413 |
| w17 | 42 | -0.044612 | 18.967 |
| w18 | 38 | -0.071026 | -14.185 |
| w19 | 59 | 0.028277 | -16.87 |
| w20 | 56 | -0.008469 | -11.046 |
| w21 | 53 | -0.119062 | -31.95 |
| w22 | 57 | -0.087307 | -7.412 |
| w23 | 52 | 0.07513 | -2.784 |
| w24 | 69 | 0.058254 | 5.62 |

- XMRUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 56 | 0.055553 | -0.055 |
| w2 | 46 | 0.110846 | -0.502 |
| w3 | 43 | 0.193938 | 15.906 |
| w4 | 53 | 0.033007 | -7.932 |
| w5 | 64 | -0.062196 | -19.874 |
| w6 | 47 | 0.047263 | -17.688 |
| w8 | 31 | -0.058949 | -23.234 |
| w9 | 43 | -0.056647 | -12.528 |
| w10 | 33 | -0.12898 | -23.383 |
| w11 | 61 | -0.049663 | -6.125 |
| w12 | 57 | 0.031765 | -8.122 |
| w14 | 42 | 0.235884 | 57.194 |
| w15 | 30 | -0.05774 | 0.665 |
| w16 | 56 | -0.029223 | 5.739 |
| w17 | 42 | 0.130291 | -12.694 |
| w18 | 41 | 0.105144 | 24.45 |
| w19 | 58 | 0.264771 | 34.982 |
| w20 | 47 | 0.134888 | 2.861 |
| w21 | 58 | 0.118527 | 1.632 |
| w22 | 54 | 0.115207 | -0.511 |
| w23 | 46 | -0.239827 | -33.03 |
| w24 | 38 | -0.112484 | -5.621 |

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
| w1 | 32 | -0.04147 | -3.85 |
| w2 | 34 | 0.111107 | 7.279 |
| w3 | 0 | -0.013793 | 0.0 |
| w4 | 0 | 0.160487 | 0.0 |
| w5 | 0 | 0.085519 | 0.0 |
| w6 | 15 | 0.0454 | 1.224 |
| w8 | 42 | -0.042306 | -4.819 |
| w9 | 48 | 0.045382 | -12.158 |
| w10 | 54 | -0.010087 | -27.361 |
| w11 | 49 | -0.072551 | -36.969 |
| w12 | 20 | 0.015701 | -3.972 |
| w15 | 41 | -0.06296 | -15.11 |
| w16 | 46 | 0.013867 | -15.279 |
| w17 | 42 | 0.059783 | -32.329 |
| w18 | 45 | -0.067641 | 9.532 |
| w19 | 49 | 0.078282 | -4.825 |
| w20 | 54 | -0.062365 | -9.616 |
| w21 | 63 | -0.04142 | -26.433 |
| w22 | 54 | -0.073148 | 0.294 |
| w23 | 53 | -0.028154 | 2.147 |
| w24 | 43 | -0.084797 | -9.715 |

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
| w1 | 44 | -0.101868 | -9.938 |
| w2 | 39 | 0.097471 | -2.174 |
| w3 | 47 | 0.080638 | 4.64 |
| w4 | 43 | 0.103812 | 3.294 |
| w5 | 64 | 0.2026 | 102.866 |
| w6 | 82 | 0.083806 | -7.349 |
| w8 | 54 | -0.047663 | -7.963 |
| w9 | 48 | -0.051425 | -18.126 |
| w10 | 61 | -0.184497 | -7.263 |
| w11 | 48 | -0.05776 | -18.655 |
| w12 | 52 | -0.023705 | 22.094 |
| w14 | 42 | 0.204504 | -24.561 |
| w15 | 42 | -0.071997 | -8.479 |
| w16 | 54 | 0.067196 | 24.85 |
| w17 | 26 | -0.09482 | -8.158 |
| w18 | 50 | 0.175957 | 18.084 |
| w19 | 37 | -0.077506 | -18.57 |
| w20 | 35 | -0.096916 | -4.576 |
| w21 | 40 | -0.024426 | -8.811 |
| w22 | 45 | -0.113409 | -12.569 |
| w23 | 24 | 0.058687 | 7.439 |
| w24 | 65 | -0.019724 | -20.93 |

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

