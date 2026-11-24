# Backtest of 031-02.b2_graded-deep-and-recent-fall_1d

- Plan: `../../../../03_test_plan/night6_longreversal_run/plans/031-02.b2_graded-deep-and-recent-fall_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 8 | 0.182346 | -35.658 |
| w3 | 6 | 0.146366 | 5.259 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 8 | -0.085012 | 6.545 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 3 | 0.156805 | 6.2 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | 0.113351 | 1.625 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 6 | 0.0886 | -27.62 |
| w3 | 3 | 0.080833 | -1.439 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | 0.037611 | 31.757 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.101722 | 12.798 |
| w9 | 4 | 0.181736 | 3.762 |
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
| w20 | 3 | 0.00132 | -3.191 |
| w21 | 7 | 0.052051 | 11.218 |
| w22 | 10 | 0.044604 | -19.168 |
| w23 | 2 | 0.100809 | 12.133 |
| w24 | 0 | None | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.03833 | -5.119 |
| w2 | 12 | 0.030689 | -27.71 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 4 | 0.01453 | -2.621 |
| w6 | 9 | -0.029909 | 11.948 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 6 | 0.026315 | 5.663 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 11 | 0.108819 | -10.656 |
| w21 | 4 | 0.013704 | 2.172 |
| w22 | 2 | 0.116811 | 11.261 |
| w23 | 3 | 0.055828 | -0.183 |
| w24 | 2 | -0.035725 | -4.136 |

- XMRUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.013929 | 2.596 |
| w2 | 10 | 0.107518 | 7.28 |
| w3 | 3 | 0.182492 | 25.106 |
| w4 | 2 | 0.025941 | 0.701 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | 0.096675 | 17.54 |
| w8 | 8 | -0.003385 | 6.704 |
| w9 | 6 | 0.08117 | 2.817 |
| w10 | 2 | 0.170129 | 3.842 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | 0.216863 | 27.438 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 14 | 0.18738 | 18.367 |
| w20 | 5 | 0.105863 | 18.496 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 1 | 0.166047 | 3.546 |
| w24 | 2 | 0.080115 | 11.876 |

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
| w2 | 11 | 0.127 | -16.36 |
| w3 | 0 | 0.010432 | 0.0 |
| w4 | 0 | 0.047434 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | 0.12454 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 8 | 0.069555 | -7.334 |
| w10 | 5 | -0.091601 | 1.461 |
| w11 | 2 | 0.042181 | 17.462 |
| w12 | 0 | None | 0.0 |
| w15 | 2 | -0.051483 | -9.825 |
| w16 | 7 | 0.23391 | 80.032 |
| w17 | 4 | 0.014765 | 94.152 |
| w18 | 0 | None | 0.0 |
| w19 | 4 | 0.027422 | 31.438 |
| w20 | 7 | -0.017145 | 22.666 |
| w21 | 4 | -0.013514 | 368.357 |
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
| w1 | 2 | 0.118894 | 16.172 |
| w2 | 12 | 0.062832 | -10.246 |
| w3 | 9 | 0.08407 | -21.605 |
| w4 | 5 | 0.172335 | 33.134 |
| w5 | 11 | 0.211858 | -13.343 |
| w6 | 6 | 0.091992 | 22.912 |
| w8 | 8 | -0.03833 | 1.88 |
| w9 | 13 | 0.085061 | -14.713 |
| w10 | 2 | 0.097466 | 6.574 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 2 | 0.238302 | -13.68 |
| w15 | 2 | -0.091515 | -5.701 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.077736 | 17.808 |
| w18 | 3 | 0.035443 | 6.431 |
| w19 | 4 | 0.094769 | 27.055 |
| w20 | 9 | -0.042389 | 42.653 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | 0.178323 | 7.627 |
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

