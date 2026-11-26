# Backtest of 059-01_choppy-calm-weekly-rise-continues_1d

- Plan: `../../../../03_test_plan/night8_choppyagitated_run/plans/059-01_choppy-calm-weekly-rise-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.029839 | -4.865 |
| w2 | 4 | 0.007285 | -9.638 |
| w3 | 16 | -0.004651 | -24.363 |
| w4 | 7 | 0.137305 | 43.098 |
| w5 | 16 | 0.076696 | -3.18 |
| w6 | 11 | -0.035587 | 23.664 |
| w7 | 10 | 0.168975 | -0.51 |
| w8 | 14 | -0.09266 | 0.548 |
| w9 | 8 | -0.107116 | -8.869 |
| w10 | 9 | 0.217305 | 33.267 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 7 | -0.009064 | 9.114 |
| w14 | 13 | 0.01279 | -8.434 |
| w15 | 0 | None | 0.0 |
| w16 | 5 | -0.055411 | -17.223 |
| w17 | 11 | 0.031947 | 28.713 |
| w18 | 4 | 0.098487 | 22.085 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | 0.150816 | 7.222 |
| w21 | 8 | -0.081752 | 7.113 |
| w22 | 7 | 0.020927 | -9.585 |
| w23 | 9 | 0.141286 | 12.9 |
| w24 | 13 | 0.095788 | 8.827 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.020315 | 3.134 |
| w2 | 0 | None | 0.0 |
| w3 | 12 | 0.042296 | -9.459 |
| w4 | 7 | 0.195786 | 49.161 |
| w5 | 15 | -0.060123 | -11.536 |
| w6 | 10 | 0.036669 | 10.786 |
| w7 | 3 | 0.006905 | -9.314 |
| w8 | 4 | 0.144221 | -5.395 |
| w9 | 9 | -0.032334 | -17.704 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.048728 | -1.786 |
| w13 | 0 | None | 0.0 |
| w14 | 5 | 0.038224 | -9.873 |
| w15 | 1 | -0.040628 | -2.946 |
| w16 | 3 | -0.01801 | -3.884 |
| w17 | 9 | -0.061386 | -3.593 |
| w18 | 6 | 0.085229 | 24.411 |
| w19 | 0 | None | 0.0 |
| w20 | 5 | 0.186009 | 12.128 |
| w21 | 8 | -0.046366 | 9.155 |
| w22 | 0 | -0.044821 | 0.0 |
| w23 | 3 | 0.074824 | 35.061 |
| w24 | 1 | -0.08815 | -3.828 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.029513 | -8.966 |
| w2 | 5 | -0.092255 | -18.789 |
| w3 | 14 | 0.029472 | -9.942 |
| w4 | 11 | -0.079514 | -3.502 |
| w5 | 8 | 0.054309 | -5.118 |
| w6 | 14 | 0.11497 | 27.612 |
| w7 | 6 | -0.082819 | -16.736 |
| w8 | 0 | None | 0.0 |
| w9 | 6 | -0.031797 | 2.401 |
| w10 | 17 | 0.006048 | 30.195 |
| w11 | 0 | None | 0.0 |
| w12 | 8 | 0.027218 | 24.849 |
| w13 | 1 | -0.07597 | -2.381 |
| w14 | 7 | -0.019309 | -11.091 |
| w15 | 0 | None | 0.0 |
| w16 | 1 | -0.016629 | -0.07 |
| w17 | 3 | -0.052251 | -8.949 |
| w18 | 5 | 0.0358 | 12.526 |
| w19 | 12 | 0.097007 | 10.466 |
| w20 | 10 | -0.081857 | -27.089 |
| w21 | 18 | -0.03961 | 1.527 |
| w22 | 0 | None | 0.0 |
| w23 | 17 | 0.135234 | 38.835 |
| w24 | 6 | -0.042256 | -12.671 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.106656 | -41.597 |
| w2 | 4 | -0.022387 | -1.041 |
| w3 | 26 | -0.1 | -17.964 |
| w4 | 22 | -0.073871 | 9.91 |
| w5 | 20 | 0.210285 | 20.343 |
| w6 | 19 | 0.051789 | 6.924 |
| w7 | 9 | 0.01531 | -6.567 |
| w8 | 10 | -0.092071 | -3.184 |
| w9 | 7 | -0.064063 | -23.529 |
| w10 | 9 | -0.085066 | 3.06 |
| w11 | 0 | None | 0.0 |
| w12 | 10 | -0.096335 | -15.967 |
| w14 | 7 | -0.090518 | -20.927 |
| w15 | 0 | None | 0.0 |
| w16 | 7 | -0.014453 | -5.264 |
| w17 | 0 | 0.133098 | 0.0 |
| w18 | 7 | 0.0284 | 15.617 |
| w19 | 0 | None | 0.0 |
| w20 | 5 | -0.024971 | -1.009 |
| w21 | 15 | -0.05624 | -20.937 |
| w22 | 14 | 0.082749 | 30.31 |
| w23 | 7 | -0.025175 | -3.445 |
| w24 | 8 | 0.002878 | 1.654 |

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
| w1 | 6 | -0.057626 | -12.265 |
| w2 | 0 | -0.075323 | 0.0 |
| w3 | 0 | -0.01682 | 0.0 |
| w4 | 0 | -0.028684 | 0.0 |
| w5 | 3 | -0.019648 | -6.697 |
| w6 | 8 | 0.094635 | 26.359 |
| w8 | 16 | 0.127601 | 16.994 |
| w9 | 2 | -0.156394 | -27.377 |
| w10 | 12 | -0.021715 | 34.759 |
| w11 | 0 | None | 0.0 |
| w12 | 10 | -0.101803 | -21.045 |
| w14 | 0 | None | 0.0 |
| w15 | 5 | 0.260709 | 23.434 |
| w16 | 1 | -0.018224 | -0.897 |
| w17 | 11 | 0.006206 | 87.023 |
| w18 | 3 | 0.217427 | 32.562 |
| w19 | 9 | 0.060572 | -1.957 |
| w20 | 6 | -0.069947 | -11.793 |
| w21 | 19 | -0.04084 | 37.01 |
| w22 | 2 | -0.017434 | -1.584 |
| w23 | 17 | 0.099882 | 39.984 |
| w24 | 12 | -0.030246 | -9.968 |

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
| w1 | 0 | None | 0.0 |
| w2 | 2 | -0.017552 | -6.549 |
| w3 | 9 | 0.003044 | -11.788 |
| w4 | 12 | -0.100413 | -3.801 |
| w5 | 9 | -0.086675 | -15.036 |
| w6 | 14 | 0.059599 | 2.654 |
| w7 | 3 | 0.004525 | -11.731 |
| w8 | 17 | -0.042972 | 5.084 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 14 | 0.014606 | 19.675 |
| w13 | 0 | None | 0.0 |
| w14 | 9 | 0.069628 | -0.739 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | -0.014292 | 21.316 |
| w18 | 5 | 0.026145 | 18.777 |
| w19 | 0 | None | 0.0 |
| w20 | 7 | -0.116465 | -5.075 |
| w21 | 3 | -0.052601 | 1.324 |
| w22 | 2 | -0.042239 | 1.925 |
| w23 | 6 | -0.05229 | -9.888 |
| w24 | 4 | 0.077981 | 2.591 |

