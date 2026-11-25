# Backtest of 059-01.b2_falling-calm-decline-continues_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/059-01.b2_falling-calm-decline-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | -0.080543 | -9.659 |
| w2 | 6 | 0.256222 | 23.114 |
| w3 | 21 | 0.121445 | -11.155 |
| w4 | 4 | -0.013791 | -0.778 |
| w5 | 11 | -0.070657 | -8.966 |
| w6 | 3 | 0.028798 | 0.693 |
| w7 | 23 | -0.000521 | 4.444 |
| w8 | 4 | 0.02714 | 0.335 |
| w9 | 21 | -0.231184 | -45.151 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | 0.034784 | -5.423 |
| w12 | 11 | -0.019254 | -1.929 |
| w13 | 10 | -0.046788 | -1.236 |
| w14 | 9 | 0.163581 | 38.703 |
| w15 | 0 | None | 0.0 |
| w16 | 4 | -0.091558 | -2.887 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | -0.070702 | -4.856 |
| w21 | 0 | None | 0.0 |
| w22 | 3 | -0.022724 | -9.502 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | 0.162928 | 12.838 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | 0.01094 | 8.805 |
| w2 | 2 | -0.088467 | 7.566 |
| w3 | 17 | 0.05454 | -0.642 |
| w4 | 0 | -0.099421 | 0.0 |
| w5 | 7 | -0.029119 | -1.255 |
| w6 | 17 | -0.0495 | -12.03 |
| w7 | 25 | 0.079731 | 33.053 |
| w8 | 0 | None | 0.0 |
| w9 | 35 | -0.122089 | -12.71 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | -0.013967 | -0.432 |
| w13 | 14 | 0.160389 | 27.753 |
| w14 | 11 | 0.140087 | 25.971 |
| w15 | 15 | 0.029569 | 1.716 |
| w16 | 0 | 0.006171 | 0.0 |
| w17 | 0 | 0.003397 | 0.0 |
| w18 | 2 | -0.011453 | -4.466 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 4 | -0.057313 | -9.123 |
| w22 | 7 | -0.04837 | 4.637 |
| w23 | 0 | None | 0.0 |
| w24 | 17 | 0.017147 | 3.194 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 42 | -0.127671 | -7.7 |
| w2 | 1 | 0.324927 | 15.379 |
| w3 | 12 | -0.012998 | -2.112 |
| w4 | 5 | -0.134184 | -11.754 |
| w5 | 4 | -0.08748 | 0.251 |
| w6 | 14 | -0.010736 | -5.139 |
| w7 | 38 | 0.036777 | 31.786 |
| w8 | 0 | None | 0.0 |
| w9 | 44 | -0.101555 | -6.25 |
| w10 | 8 | -0.011842 | -1.555 |
| w11 | 0 | None | 0.0 |
| w12 | 7 | -0.033324 | -2.556 |
| w13 | 16 | 0.02242 | 0.805 |
| w14 | 19 | 0.060994 | 15.664 |
| w15 | 13 | 0.066975 | 2.902 |
| w16 | 2 | -0.069516 | -1.977 |
| w17 | 2 | -0.027614 | -1.49 |
| w18 | 9 | -0.023507 | -3.872 |
| w19 | 2 | -0.110343 | -14.893 |
| w20 | 17 | -0.01984 | 0.736 |
| w21 | 2 | -0.026282 | -3.578 |
| w22 | 4 | 0.098922 | 8.302 |
| w23 | 0 | None | 0.0 |
| w24 | 12 | -0.048748 | -7.064 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.138026 | -14.792 |
| w2 | 0 | None | 0.0 |
| w3 | 14 | -0.096275 | -10.217 |
| w4 | 5 | -0.263971 | -6.651 |
| w5 | 9 | -0.089404 | -6.837 |
| w6 | 8 | -0.020179 | -3.73 |
| w7 | 49 | -0.036909 | 5.461 |
| w8 | 4 | 0.042904 | 0.207 |
| w9 | 38 | -0.079802 | -0.728 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 22 | -0.012538 | 1.542 |
| w14 | 5 | 0.177246 | 41.148 |
| w15 | 8 | 0.070215 | 6.737 |
| w16 | 2 | -0.10895 | -8.336 |
| w17 | 0 | None | 0.0 |
| w18 | 3 | -0.035219 | -4.316 |
| w19 | 0 | None | 0.0 |
| w20 | 7 | -0.119524 | -9.24 |
| w21 | 7 | -0.053886 | -14.95 |
| w22 | 4 | -0.153547 | -13.693 |
| w23 | 10 | 0.076815 | 27.764 |
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
| w1 | 24 | 0.038954 | 15.728 |
| w2 | 7 | -0.034697 | 18.213 |
| w3 | 0 | 0.041056 | 0.0 |
| w4 | 0 | -0.041683 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 11 | -0.049987 | -4.457 |
| w8 | 20 | -0.111587 | -6.36 |
| w9 | 28 | -0.014313 | 1.877 |
| w10 | 9 | -0.063064 | -10.579 |
| w11 | 0 | None | 0.0 |
| w12 | 11 | -0.010325 | -0.861 |
| w14 | 19 | 0.025312 | -28.459 |
| w15 | 18 | 0.021687 | 6.101 |
| w16 | 3 | -0.059946 | -0.95 |
| w17 | 5 | -0.040482 | -4.895 |
| w18 | 8 | -0.017128 | -3.579 |
| w19 | 14 | -0.049943 | -7.845 |
| w20 | 20 | 0.087961 | 16.396 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 34 | -0.152268 | 6.167 |

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
| w1 | 22 | 0.028666 | 4.766 |
| w2 | 6 | -0.068933 | -4.51 |
| w3 | 38 | 0.095076 | 15.385 |
| w4 | 15 | -0.12743 | -18.559 |
| w5 | 21 | 0.007495 | 16.743 |
| w6 | 12 | -0.041305 | -4.885 |
| w7 | 39 | -0.035457 | -4.606 |
| w8 | 18 | -0.040068 | -7.615 |
| w9 | 23 | 0.020304 | 2.526 |
| w10 | 2 | -0.081071 | 0.545 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 19 | 0.064212 | 13.553 |
| w14 | 24 | 0.07912 | 7.746 |
| w15 | 13 | 0.021445 | 4.894 |
| w16 | 0 | None | 0.0 |
| w17 | 12 | 0.065402 | 1.471 |
| w18 | 5 | -0.040576 | -4.018 |
| w19 | 0 | None | 0.0 |
| w20 | 5 | -0.008474 | -4.313 |
| w21 | 9 | -0.050989 | -6.981 |
| w22 | 2 | -0.180561 | -4.594 |
| w23 | 13 | 0.004126 | -4.715 |
| w24 | 0 | None | 0.0 |

