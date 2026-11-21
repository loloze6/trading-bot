# Backtest of 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d

- Plan: `../../../../03_test_plan/night3_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | -0.07946 | -8.846 |
| w2 | 14 | -0.033566 | 3.955 |
| w3 | 23 | -0.167499 | -22.273 |
| w4 | 38 | 0.218096 | 42.095 |
| w5 | 30 | 0.115358 | 16.833 |
| w6 | 32 | 0.006143 | 15.353 |
| w7 | 22 | 0.134848 | 9.681 |
| w8 | 23 | 0.114892 | 72.011 |
| w9 | 29 | 0.219266 | 15.307 |
| w10 | 23 | -0.182535 | 39.224 |
| w11 | 34 | 0.162627 | 24.322 |
| w12 | 8 | 0.024147 | 0.403 |
| w13 | 31 | 0.047061 | -0.718 |
| w14 | 21 | -0.096731 | -1.482 |
| w15 | 39 | 0.106632 | -9.896 |
| w16 | 26 | -0.056692 | -8.308 |
| w17 | 35 | -0.066103 | 43.667 |
| w18 | 21 | -0.01158 | -16.43 |
| w19 | 57 | 0.109388 | 23.807 |
| w20 | 44 | 0.213037 | 40.924 |
| w21 | 49 | 0.16849 | 58.746 |
| w22 | 40 | -0.057867 | -21.767 |
| w23 | 28 | 0.17666 | 24.318 |
| w24 | 39 | 0.306882 | 65.402 |

- ETHUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 44 | -0.04419 | -11.943 |
| w2 | 37 | 0.058607 | 18.228 |
| w3 | 43 | -0.220625 | -41.062 |
| w4 | 23 | 0.123049 | 48.761 |
| w5 | 36 | 0.06301 | 7.217 |
| w6 | 39 | -0.005231 | -20.436 |
| w7 | 40 | -0.126419 | 19.086 |
| w8 | 22 | -0.057518 | 3.543 |
| w9 | 9 | 0.150294 | 6.038 |
| w10 | 37 | -0.000453 | 53.184 |
| w11 | 33 | 0.270242 | 19.365 |
| w12 | 10 | 0.132771 | 9.446 |
| w14 | 28 | -0.127555 | -4.237 |
| w15 | 29 | 0.038899 | -1.123 |
| w16 | 30 | 0.046897 | -0.665 |
| w17 | 24 | 0.045588 | 10.505 |
| w18 | 30 | 0.022365 | 32.364 |
| w19 | 43 | -0.099902 | -44.305 |
| w20 | 30 | 0.175283 | 34.93 |
| w21 | 19 | 0.029863 | 9.459 |
| w22 | 31 | 0.133469 | 39.608 |
| w23 | 26 | 0.040059 | -12.205 |
| w24 | 27 | 0.098311 | 12.302 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 873 warm-up bars -- required_bars=940. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 42 | 0.003972 | -5.034 |
| w2 | 49 | -0.143245 | -28.106 |
| w3 | 30 | 0.036656 | 10.861 |
| w4 | 36 | 0.114302 | -6.465 |
| w5 | 35 | -0.005622 | -7.04 |
| w6 | 20 | 0.14677 | 13.863 |
| w7 | 31 | 0.178025 | -14.815 |
| w8 | 24 | 0.038432 | 51.419 |
| w9 | 12 | 0.202635 | 4.175 |
| w10 | 21 | 0.048267 | 43.086 |
| w11 | 23 | 0.21824 | 2.309 |
| w12 | 14 | 0.002605 | 3.851 |
| w13 | 9 | 0.042842 | 14.631 |
| w14 | 33 | -0.137033 | -7.759 |
| w15 | 15 | -0.028557 | -0.109 |
| w16 | 23 | 0.01135 | 3.17 |
| w17 | 36 | 0.083561 | 22.052 |
| w18 | 27 | 0.066954 | 20.235 |
| w19 | 30 | 0.190726 | 23.562 |
| w20 | 29 | 0.082058 | -1.11 |
| w21 | 38 | 0.03098 | 3.221 |
| w22 | 47 | 0.210307 | 70.495 |
| w23 | 24 | 0.229865 | 24.836 |
| w24 | 22 | -0.040889 | 2.232 |

- XMRUSD: 19 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | -0.028333 | -3.485 |
| w2 | 39 | -0.147623 | -44.772 |
| w3 | 27 | -0.222734 | -18.191 |
| w4 | 22 | 0.25408 | 13.2 |
| w5 | 36 | 0.129482 | 32.831 |
| w6 | 35 | 0.157709 | 9.147 |
| w9 | 38 | 0.193706 | 9.007 |
| w10 | 24 | -0.015819 | 48.934 |
| w11 | 41 | 0.065344 | -4.993 |
| w12 | 7 | 0.229042 | 10.073 |
| w16 | 49 | -0.05977 | -39.623 |
| w17 | 26 | 0.019955 | 14.484 |
| w18 | 37 | 0.133984 | 67.276 |
| w19 | 41 | -0.083098 | -8.986 |
| w20 | 27 | 0.183696 | 7.91 |
| w21 | 40 | 0.069096 | 10.835 |
| w22 | 39 | 0.244999 | 33.892 |
| w23 | 24 | -0.03127 | -26.049 |
| w24 | 59 | 0.159245 | 23.629 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 483 warm-up bars -- required_bars=940. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w8 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 728 warm-up bars -- required_bars=940. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=940. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 606 warm-up bars -- required_bars=940. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w15 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 848 warm-up bars -- required_bars=940. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 18 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.060475 | -16.173 |
| w2 | 24 | -0.095625 | -9.327 |
| w3 | 0 | 0.15921 | 0.0 |
| w4 | 0 | 0.123496 | 0.0 |
| w5 | 0 | 0.040831 | 0.0 |
| w6 | 0 | 0.120565 | 0.0 |
| w10 | 40 | -0.01629 | 1.698 |
| w11 | 27 | 0.036349 | 17.708 |
| w12 | 20 | -0.082961 | -7.418 |
| w16 | 26 | 0.110437 | 26.332 |
| w17 | 30 | -0.178598 | -70.331 |
| w18 | 27 | 0.064909 | 23.27 |
| w19 | 0 | 0.030541 | 0.0 |
| w20 | 0 | 0.067408 | 0.0 |
| w21 | 8 | -0.025336 | 3.888 |
| w22 | 30 | 0.064469 | 14.634 |
| w23 | 41 | 0.061916 | -6.501 |
| w24 | 41 | 0.076795 | 26.973 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=940. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w8 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 592 warm-up bars -- required_bars=940. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w9 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 835 warm-up bars -- required_bars=940. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=940. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 470 warm-up bars -- required_bars=940. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w15 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 712 warm-up bars -- required_bars=940. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 19 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 33 | 0.006329 | 9.24 |
| w2 | 30 | 0.054676 | 12.007 |
| w3 | 33 | -0.035352 | -8.82 |
| w4 | 33 | 0.097912 | 26.04 |
| w5 | 34 | -0.280907 | -60.853 |
| w6 | 39 | 0.037389 | 23.506 |
| w9 | 16 | 0.108649 | -0.49 |
| w10 | 12 | 0.002222 | 9.836 |
| w11 | 63 | 0.036238 | 33.241 |
| w12 | 11 | 0.143577 | 8.373 |
| w16 | 30 | -0.076778 | -36.68 |
| w17 | 35 | -0.189942 | -23.148 |
| w18 | 37 | 0.017536 | 4.797 |
| w19 | 26 | 0.106731 | 13.531 |
| w20 | 34 | 0.00511 | -13.302 |
| w21 | 49 | 0.045491 | 20.621 |
| w22 | 31 | 0.075293 | -3.013 |
| w23 | 32 | -0.014722 | -11.828 |
| w24 | 43 | -0.049895 | -42.577 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 548 warm-up bars -- required_bars=940. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w8 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 793 warm-up bars -- required_bars=940. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=940. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 671 warm-up bars -- required_bars=940. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w15 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 913 warm-up bars -- required_bars=940. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

