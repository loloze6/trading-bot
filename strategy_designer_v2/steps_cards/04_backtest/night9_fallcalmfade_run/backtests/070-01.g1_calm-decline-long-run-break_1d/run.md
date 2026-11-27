# Backtest of 070-01.g1_calm-decline-long-run-break_1d

- Plan: `../../../../03_test_plan/night9_fallcalmfade_run/plans/070-01.g1_calm-decline-long-run-break_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.059482 | -5.479 |
| w2 | 4 | 0.017951 | 2.873 |
| w3 | 10 | -0.052166 | -6.18 |
| w4 | 1 | 0.006236 | -0.477 |
| w5 | 3 | 0.022913 | 1.452 |
| w6 | 3 | 0.010384 | -2.341 |
| w7 | 7 | 0.045398 | 6.662 |
| w8 | 1 | 0.034372 | 0.721 |
| w9 | 8 | 0.002337 | 1.542 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.016258 | -2.031 |
| w13 | 5 | 0.09305 | 8.325 |
| w14 | 5 | 0.085336 | 19.761 |
| w15 | 0 | None | 0.0 |
| w16 | 1 | 0.059636 | 4.713 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | 0.014226 | 0.764 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.036762 | 3.922 |
| w2 | 0 | None | 0.0 |
| w3 | 5 | -0.016097 | -1.264 |
| w4 | 1 | -0.02418 | -1.049 |
| w5 | 2 | -0.066009 | -3.414 |
| w6 | 6 | 0.00727 | -3.936 |
| w7 | 9 | 0.151429 | 26.346 |
| w8 | 0 | None | 0.0 |
| w9 | 8 | 0.047585 | 7.821 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.020562 | 0.86 |
| w13 | 5 | -0.069141 | -8.899 |
| w14 | 5 | 0.113488 | 19.293 |
| w15 | 5 | 0.029872 | 1.587 |
| w16 | 2 | 0.05245 | 5.334 |
| w17 | 2 | -0.066086 | -5.002 |
| w18 | 1 | -0.011453 | -0.745 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.038845 | -2.262 |
| w23 | 0 | None | 0.0 |
| w24 | 7 | 0.030471 | 4.211 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.089655 | 11.832 |
| w2 | 1 | 0.056333 | 2.763 |
| w3 | 3 | 0.078862 | 5.762 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 7 | 0.049158 | 0.703 |
| w7 | 17 | 0.039536 | 11.182 |
| w8 | 0 | None | 0.0 |
| w9 | 14 | -0.089842 | -13.309 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.02153 | -1.383 |
| w13 | 6 | -0.136302 | -15.488 |
| w14 | 7 | 0.244411 | 44.299 |
| w15 | 5 | -0.005393 | -1.443 |
| w16 | 3 | 0.019494 | 2.909 |
| w17 | 3 | 0.00309 | -2.28 |
| w18 | 2 | -0.001891 | 0.381 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.035255 | -3.701 |
| w21 | 1 | -0.023316 | -2.295 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.010706 | -2.704 |
| w24 | 4 | 0.009079 | 0.612 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.030909 | 2.132 |
| w2 | 2 | 0.080295 | 5.242 |
| w3 | 4 | -0.007207 | -1.911 |
| w4 | 2 | -0.242783 | -13.725 |
| w5 | 2 | -0.079824 | -5.01 |
| w6 | 2 | -0.020543 | -2.542 |
| w7 | 14 | 0.276022 | 48.487 |
| w8 | 1 | 0.039484 | 0.839 |
| w9 | 14 | -0.082414 | -10.582 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.005656 | -1.48 |
| w14 | 4 | 0.017657 | 2.947 |
| w15 | 4 | -0.000464 | -1.266 |
| w16 | 1 | 0.017783 | 0.707 |
| w17 | 0 | None | 0.0 |
| w18 | 1 | -0.007367 | -0.497 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.043719 | 1.155 |
| w21 | 2 | -0.01988 | -2.988 |
| w22 | 0 | None | 0.0 |
| w23 | 1 | -0.000209 | -0.33 |
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
| w1 | 6 | 0.046476 | 6.224 |
| w2 | 1 | -0.139633 | -1.187 |
| w3 | 0 | 0.019225 | 0.0 |
| w4 | 0 | 0.038604 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 5 | -0.039649 | -6.121 |
| w8 | 7 | 0.095837 | 7.019 |
| w9 | 6 | 0.063997 | 7.561 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | -0.043561 | -3.115 |
| w14 | 9 | 0.0216 | -3.016 |
| w15 | 6 | -0.020283 | -3.403 |
| w16 | 1 | 0.052938 | 4.007 |
| w17 | 3 | -0.008684 | -2.664 |
| w18 | 5 | 0.056939 | 5.3 |
| w19 | 5 | 0.103722 | 14.871 |
| w20 | 5 | 0.088116 | 11.099 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 1 | 0.010489 | 0.07 |
| w24 | 11 | -0.07752 | -8.856 |

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
| w1 | 7 | 0.041316 | 5.088 |
| w2 | 3 | -0.024817 | -1.535 |
| w3 | 11 | 0.10146 | 18.678 |
| w4 | 4 | -0.048328 | -4.652 |
| w5 | 4 | 0.08134 | 10.037 |
| w6 | 5 | -0.058053 | -8.58 |
| w7 | 12 | 0.066228 | 11.348 |
| w8 | 8 | -0.066787 | -8.116 |
| w9 | 10 | -0.061841 | -6.249 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | -0.028359 | -1.816 |
| w13 | 6 | -0.022258 | -2.999 |
| w14 | 11 | 0.054311 | 14.507 |
| w15 | 5 | 0.088048 | 7.414 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | -0.02594 | -3.139 |
| w18 | 2 | -0.022808 | -1.731 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | 0.025489 | 0.547 |
| w21 | 2 | -0.191215 | -20.959 |
| w22 | 0 | None | 0.0 |
| w23 | 4 | -0.038762 | -5.359 |
| w24 | 0 | None | 0.0 |

