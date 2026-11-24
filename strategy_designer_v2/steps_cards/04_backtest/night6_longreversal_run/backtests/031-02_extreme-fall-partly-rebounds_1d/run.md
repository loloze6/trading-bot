# Backtest of 031-02_extreme-fall-partly-rebounds_1d

- Plan: `../../../../03_test_plan/night6_longreversal_run/plans/031-02_extreme-fall-partly-rebounds_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 3 | 0.186878 | -38.805 |
| w3 | 3 | 0.133787 | -0.421 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 3 | -0.111267 | -3.321 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 1 | 0.124308 | 6.526 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | 0.067001 | 1.914 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 4 | 0.122708 | -22.892 |
| w3 | 2 | 0.002478 | -9.465 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.031021 | 50.286 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.101604 | 17.745 |
| w9 | 4 | 0.176568 | 2.345 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.00949 | -2.237 |
| w21 | 6 | 0.021968 | 21.263 |
| w22 | 8 | 0.056116 | -22.006 |
| w23 | 3 | 0.081779 | 31.16 |
| w24 | 0 | None | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.048162 | -4.732 |
| w2 | 2 | 0.021441 | -36.755 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | 0.007733 | -4.686 |
| w6 | 8 | -0.036619 | 18.347 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 6 | 0.023505 | 7.474 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 9 | 0.038214 | -22.555 |
| w21 | 4 | 0.008701 | 12.717 |
| w22 | 5 | 0.109714 | 8.975 |
| w23 | 4 | 0.054897 | -0.226 |
| w24 | 4 | -0.047173 | -2.61 |

- XMRUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.017094 | -1.322 |
| w2 | 5 | 0.10938 | 4.59 |
| w3 | 1 | 0.168284 | 27.993 |
| w4 | 1 | 0.02453 | 1.477 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.096105 | 30.132 |
| w8 | 1 | -0.01696 | 2.961 |
| w9 | 6 | 0.072854 | 3.371 |
| w10 | 2 | 0.171248 | 9.808 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | 0.216863 | 22.732 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 6 | 0.122665 | 6.589 |
| w20 | 1 | 0.069831 | 25.24 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 3 | 0.144124 | 3.912 |
| w24 | 2 | 0.080115 | 6.536 |

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
| w1 | 0 | None | 0.0 |
| w2 | 7 | 0.133808 | -14.121 |
| w3 | 0 | 0.013389 | 0.0 |
| w4 | 0 | 0.053575 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | 0.123111 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 5 | 0.068558 | -1.687 |
| w10 | 6 | -0.114033 | -1.297 |
| w11 | 2 | 0.042181 | 15.693 |
| w12 | 0 | None | 0.0 |
| w15 | 1 | -0.065424 | -15.033 |
| w16 | 4 | 0.221906 | 80.399 |
| w17 | 2 | 0.010113 | 139.584 |
| w18 | 0 | None | 0.0 |
| w19 | 3 | 0.033015 | 33.728 |
| w20 | 2 | -0.033427 | 16.969 |
| w21 | 3 | -0.000108 | 489.348 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

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
| w1 | 6 | 0.120682 | 52.127 |
| w2 | 7 | 0.039371 | -20.705 |
| w3 | 6 | 0.079216 | -28.933 |
| w4 | 5 | 0.177286 | 40.966 |
| w5 | 11 | 0.229415 | -21.454 |
| w6 | 4 | 0.086931 | 31.704 |
| w8 | 4 | -0.056546 | 8.896 |
| w9 | 17 | 0.063131 | -25.133 |
| w10 | 2 | 0.097466 | 13.844 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 2 | 0.198377 | -13.68 |
| w15 | 2 | -0.092199 | -8.96 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.075816 | 22.264 |
| w18 | 1 | 0.054837 | 5.11 |
| w19 | 2 | 0.099673 | 16.568 |
| w20 | 3 | -0.083723 | 16.856 |
| w21 | 0 | None | 0.0 |
| w22 | 5 | 0.087694 | 2.432 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

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

