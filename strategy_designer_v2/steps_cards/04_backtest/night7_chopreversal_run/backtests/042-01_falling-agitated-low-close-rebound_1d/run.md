# Backtest of 042-01_falling-agitated-low-close-rebound_1d

- Plan: `../../../../03_test_plan/night7_chopreversal_run/plans/042-01_falling-agitated-low-close-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.039941 | -5.774 |
| w2 | 58 | 0.010572 | -16.478 |
| w3 | 39 | 0.1928 | 21.616 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | 0.083747 | 8.436 |
| w7 | 0 | None | 0.0 |
| w8 | 14 | -0.043513 | -1.411 |
| w9 | 20 | -0.099274 | -12.766 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | 0.074129 | 3.01 |
| w13 | 45 | 0.085213 | 6.417 |
| w14 | 37 | 0.156366 | 6.099 |
| w15 | 5 | -0.066393 | -3.204 |
| w16 | 42 | 0.195317 | 31.35 |
| w17 | 0 | None | 0.0 |
| w18 | 64 | -0.085205 | -19.163 |
| w19 | 0 | None | 0.0 |
| w20 | 19 | 0.160618 | 13.814 |
| w21 | 0 | None | 0.0 |
| w22 | 42 | 0.18998 | 28.06 |
| w23 | 0 | None | 0.0 |
| w24 | 29 | 0.021667 | -5.725 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.130961 | -16.028 |
| w2 | 67 | -0.020789 | -22.138 |
| w3 | 17 | 0.192149 | 17.847 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 20 | -0.026651 | -0.348 |
| w9 | 17 | 0.063084 | 3.369 |
| w10 | 2 | 0.065973 | 1.682 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 64 | 0.209357 | 14.82 |
| w15 | 14 | 0.034444 | 3.693 |
| w16 | 40 | 0.196175 | 33.764 |
| w17 | 3 | 0.020354 | 1.395 |
| w18 | 24 | -0.024864 | -1.472 |
| w19 | 1 | None | -0.047 |
| w20 | 51 | 0.097053 | 2.386 |
| w21 | 20 | 0.022432 | 4.707 |
| w22 | 64 | 0.124335 | -2.921 |
| w23 | 5 | 0.18856 | 13.294 |
| w24 | 22 | 0.137115 | 5.774 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 60 | 0.053667 | -5.311 |
| w3 | 1 | 0.393083 | 14.003 |
| w4 | 2 | 0.064559 | 3.062 |
| w5 | 21 | -0.000701 | -4.793 |
| w6 | 5 | 0.206667 | 9.533 |
| w7 | 0 | None | 0.0 |
| w8 | 16 | -0.039488 | 0.649 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | 0.048203 | 2.656 |
| w13 | 18 | 0.065489 | 4.616 |
| w14 | 43 | 0.101759 | -0.335 |
| w15 | 19 | 0.103434 | 11.352 |
| w16 | 33 | 0.229835 | 34.167 |
| w17 | 9 | 0.002029 | 2.382 |
| w18 | 36 | 0.056174 | 4.434 |
| w19 | 1 | -0.039182 | -1.119 |
| w20 | 52 | 0.134688 | 7.313 |
| w21 | 1 | 0.047127 | 2.285 |
| w22 | 39 | 0.097928 | 10.246 |
| w23 | 4 | 0.050594 | 4.175 |
| w24 | 43 | -0.070077 | -15.748 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | -0.087782 | -15.787 |
| w2 | 47 | 0.023784 | -2.191 |
| w3 | 3 | 0.174259 | 7.357 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 9 | -0.012609 | 0.048 |
| w7 | 0 | None | 0.0 |
| w8 | 17 | 0.011807 | 1.404 |
| w9 | 2 | -0.002993 | -1.047 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 41 | 0.1264 | 1.869 |
| w15 | 8 | 0.066378 | 5.902 |
| w16 | 39 | 0.229186 | 35.209 |
| w17 | 0 | None | 0.0 |
| w18 | 34 | 0.137256 | 19.936 |
| w19 | 42 | 0.215278 | 29.908 |
| w20 | 5 | 0.274117 | 16.235 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 13 | 0.077795 | 6.265 |
| w24 | 10 | 0.097679 | 11.948 |

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
| w1 | 4 | 0.025313 | 0.675 |
| w2 | 26 | -0.076214 | -11.798 |
| w3 | 0 | -0.004696 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | 0.069463 | 3.257 |
| w8 | 7 | 0.051976 | 1.714 |
| w9 | 11 | 0.116842 | 7.38 |
| w10 | 0 | None | 0.0 |
| w11 | 19 | 0.097516 | 20.708 |
| w12 | 0 | None | 0.0 |
| w14 | 11 | -0.079462 | -8.108 |
| w15 | 9 | 0.021208 | 1.677 |
| w16 | 43 | 0.215452 | 41.549 |
| w17 | 4 | 0.004286 | -1.403 |
| w18 | 27 | -0.008107 | -1.364 |
| w19 | 17 | -0.036251 | -10.031 |
| w20 | 12 | 0.04436 | 8.552 |
| w21 | 7 | -0.042487 | 0.349 |
| w22 | 36 | 0.03674 | 4.301 |
| w23 | 0 | None | 0.0 |
| w24 | 23 | 0.056978 | -0.25 |

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
| w1 | 1 | 0.021729 | 0.965 |
| w2 | 51 | -0.044986 | -16.694 |
| w3 | 21 | 0.171216 | 14.19 |
| w4 | 13 | 0.011659 | 0.824 |
| w5 | 22 | 0.135859 | 14.103 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | -0.063448 | -2.369 |
| w8 | 16 | 0.059475 | 2.943 |
| w9 | 42 | 0.010354 | -9.952 |
| w10 | 4 | -0.074685 | -2.147 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 18 | 0.044496 | 1.852 |
| w14 | 36 | 0.123014 | 4.368 |
| w15 | 14 | -0.090595 | -11.58 |
| w16 | 45 | 0.140115 | 38.157 |
| w17 | 16 | 0.218377 | 22.009 |
| w18 | 34 | 0.008023 | -1.635 |
| w19 | 50 | 0.059649 | -0.3 |
| w20 | 18 | -0.004027 | 4.393 |
| w21 | 10 | -0.006504 | 2.119 |
| w22 | 54 | 0.026593 | -3.026 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

