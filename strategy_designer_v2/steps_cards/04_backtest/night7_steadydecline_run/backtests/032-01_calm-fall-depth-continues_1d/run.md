# Backtest of 032-01_calm-fall-depth-continues_1d

- Plan: `../../../../03_test_plan/night7_steadydecline_run/plans/032-01_calm-fall-depth-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.000116 | 2.296 |
| w2 | 2 | 0.19165 | 14.994 |
| w3 | 9 | 0.044141 | 4.786 |
| w4 | 2 | -0.001441 | -3.679 |
| w5 | 11 | -0.086531 | -10.034 |
| w6 | 1 | 0.100244 | 3.579 |
| w7 | 16 | -0.015662 | 3.49 |
| w8 | 2 | 0.045313 | 0.6 |
| w9 | 21 | -0.118423 | -15.076 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | 0.034784 | 0.122 |
| w12 | 8 | -0.011603 | -0.982 |
| w13 | 10 | -0.020705 | -1.836 |
| w14 | 10 | 0.138701 | 40.658 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | -0.097335 | -2.79 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | -0.083692 | -7.744 |
| w21 | 0 | None | 0.0 |
| w22 | 1 | -0.022724 | -1.4 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | 0.204714 | 15.517 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.004064 | 1.021 |
| w2 | 1 | -0.088467 | -5.957 |
| w3 | 14 | -0.006966 | 1.061 |
| w4 | 4 | -0.078451 | -1.622 |
| w5 | 10 | -0.070815 | -8.188 |
| w6 | 14 | 0.030366 | -7.641 |
| w7 | 21 | 0.008602 | 19.526 |
| w8 | 0 | None | 0.0 |
| w9 | 17 | -0.035333 | 3.769 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.020557 | 0.843 |
| w13 | 15 | 0.053473 | 3.567 |
| w14 | 12 | 0.212499 | 37.381 |
| w15 | 10 | 0.06458 | 3.276 |
| w16 | 4 | -0.041405 | -4.471 |
| w17 | 1 | -0.057376 | -0.421 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | -0.003574 | -0.194 |
| w22 | 6 | -0.005523 | 3.566 |
| w23 | 0 | None | 0.0 |
| w24 | 11 | 0.06828 | 16.628 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 36 | -0.092346 | -2.226 |
| w2 | 2 | 0.265198 | 9.95 |
| w3 | 10 | 0.022162 | -0.542 |
| w4 | 2 | -0.110715 | -5.39 |
| w5 | 2 | -0.077242 | -3.614 |
| w6 | 5 | 0.080197 | 3.4 |
| w7 | 32 | -0.088738 | 9.841 |
| w8 | 0 | None | 0.0 |
| w9 | 33 | -0.079744 | 7.37 |
| w10 | 2 | -0.022693 | -4.575 |
| w11 | 0 | None | 0.0 |
| w12 | 6 | -0.007516 | -0.297 |
| w13 | 17 | -0.048933 | -7.001 |
| w14 | 16 | 0.095455 | 36.178 |
| w15 | 7 | 0.068638 | 5.948 |
| w16 | 2 | -0.055117 | -2.099 |
| w17 | 4 | -0.003831 | -2.117 |
| w18 | 3 | 0.026216 | -2.208 |
| w19 | 1 | -0.110343 | -8.0 |
| w20 | 14 | 0.024316 | 5.15 |
| w21 | 4 | -0.021205 | -1.841 |
| w22 | 2 | 0.107994 | 7.002 |
| w23 | 0 | -0.116672 | 0.0 |
| w24 | 13 | -0.038777 | -2.429 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.15163 | -3.383 |
| w2 | 0 | None | 0.0 |
| w3 | 14 | -0.085177 | -9.157 |
| w4 | 8 | -0.270639 | -9.423 |
| w5 | 8 | -0.105396 | -15.02 |
| w6 | 2 | -0.01857 | -2.248 |
| w7 | 36 | -0.167343 | -13.053 |
| w8 | 3 | 0.057822 | 0.991 |
| w9 | 37 | -0.07809 | -0.914 |
| w10 | 0 | -0.308113 | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 17 | -0.011598 | 0.883 |
| w14 | 6 | 0.137374 | 34.119 |
| w15 | 6 | 0.035732 | 1.313 |
| w16 | 2 | -0.127735 | -10.357 |
| w17 | 0 | None | 0.0 |
| w18 | 1 | -0.045516 | -0.445 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | -0.070971 | -5.341 |
| w21 | 4 | -0.128104 | -6.864 |
| w22 | 2 | -0.123728 | -5.111 |
| w23 | 5 | 0.07215 | 11.523 |
| w24 | 0 | None | 0.0 |

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
| w1 | 24 | 0.028452 | 10.711 |
| w2 | 4 | 0.02156 | 16.422 |
| w3 | 0 | 0.013938 | 0.0 |
| w4 | 0 | -0.008989 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.090336 | -0.207 |
| w8 | 12 | -0.077946 | -3.19 |
| w9 | 23 | 0.041943 | 16.147 |
| w10 | 5 | -0.120335 | -20.439 |
| w11 | 0 | None | 0.0 |
| w12 | 7 | -0.031096 | -2.556 |
| w14 | 19 | -0.057242 | -17.937 |
| w15 | 18 | 0.032056 | 4.174 |
| w16 | 1 | -0.122307 | -7.578 |
| w17 | 2 | -0.04049 | 0.308 |
| w18 | 4 | 0.033923 | -3.769 |
| w19 | 13 | -0.07876 | -14.041 |
| w20 | 12 | 0.130213 | 17.992 |
| w21 | 0 | None | 0.0 |
| w22 | 1 | -0.069772 | -2.076 |
| w23 | 0 | -0.020124 | 0.0 |
| w24 | 30 | -0.069239 | 2.261 |

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
| w1 | 19 | -0.025007 | -7.204 |
| w2 | 6 | -0.136242 | -3.514 |
| w3 | 31 | 0.108485 | 18.642 |
| w4 | 9 | -0.107338 | -15.91 |
| w5 | 19 | 0.02437 | 6.992 |
| w6 | 5 | -0.063198 | -7.28 |
| w7 | 21 | -0.112479 | -9.635 |
| w8 | 9 | 0.001457 | -0.068 |
| w9 | 21 | -0.092148 | -10.918 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.076316 | -1.261 |
| w13 | 13 | 0.027283 | 7.218 |
| w14 | 29 | 0.118151 | 31.138 |
| w15 | 4 | 0.06548 | 8.059 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | -0.076122 | -4.097 |
| w18 | 5 | -0.068695 | -1.612 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | 0.030208 | 0.606 |
| w21 | 2 | -0.024258 | -2.258 |
| w22 | 1 | -0.180561 | -5.38 |
| w23 | 16 | -0.103077 | -12.08 |
| w24 | 0 | None | 0.0 |

