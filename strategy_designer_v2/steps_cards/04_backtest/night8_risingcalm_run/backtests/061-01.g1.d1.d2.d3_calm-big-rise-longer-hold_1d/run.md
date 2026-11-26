# Backtest of 061-01.g1.d1.d2.d3_calm-big-rise-longer-hold_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/061-01.g1.d1.d2.d3_calm-big-rise-longer-hold_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.05667 | -18.71 |
| w2 | 6 | -0.128987 | -33.708 |
| w3 | 10 | 0.059064 | -36.18 |
| w4 | 3 | 0.14008 | 51.38 |
| w5 | 15 | 0.031596 | -3.404 |
| w6 | 4 | -0.004158 | 55.857 |
| w7 | 10 | 0.104238 | -13.116 |
| w8 | 9 | -0.04668 | 13.777 |
| w9 | 7 | -0.096434 | -24.657 |
| w10 | 7 | 0.191875 | 36.148 |
| w11 | 1 | -0.108515 | 0.581 |
| w12 | 2 | 0.001908 | -1.881 |
| w13 | 6 | -0.018412 | 8.398 |
| w14 | 12 | 0.045057 | -44.762 |
| w15 | 0 | None | 0.0 |
| w16 | 3 | -0.060625 | 10.895 |
| w17 | 5 | 0.065705 | 40.611 |
| w18 | 2 | 0.162607 | 10.36 |
| w19 | 0 | None | 0.0 |
| w20 | 7 | 0.048605 | 3.355 |
| w21 | 7 | -0.084115 | 6.721 |
| w22 | 9 | 0.000739 | -24.243 |
| w23 | 11 | 0.17748 | 5.928 |
| w24 | 10 | 0.057833 | -17.997 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.010197 | 3.401 |
| w2 | 3 | -0.11016 | -18.988 |
| w3 | 9 | 0.063236 | -21.639 |
| w4 | 6 | 0.052903 | 34.521 |
| w5 | 16 | -0.075887 | -22.868 |
| w6 | 9 | 0.022836 | 12.378 |
| w7 | 7 | -0.009264 | -17.402 |
| w8 | 7 | 0.100674 | -5.546 |
| w9 | 6 | 0.00041 | -18.86 |
| w10 | 6 | -0.033249 | 19.53 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.041525 | -3.17 |
| w13 | 0 | None | 0.0 |
| w14 | 1 | -0.004185 | -15.25 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | -0.015338 | 13.716 |
| w17 | 4 | -0.01492 | 23.993 |
| w18 | 5 | 0.059586 | 33.032 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.000675 | -3.68 |
| w21 | 10 | -0.016417 | 15.5 |
| w22 | 4 | -0.001819 | -2.035 |
| w23 | 1 | 0.127603 | 37.539 |
| w24 | 3 | -0.015971 | 0.37 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.066667 | -20.511 |
| w2 | 10 | -0.040573 | -24.38 |
| w3 | 9 | 0.053217 | 9.54 |
| w4 | 6 | -0.101148 | 0.091 |
| w5 | 12 | -0.005001 | -28.047 |
| w6 | 9 | 0.12609 | 29.784 |
| w7 | 4 | -0.056886 | -22.442 |
| w8 | 3 | 0.04184 | 18.328 |
| w9 | 4 | -0.028849 | -6.469 |
| w10 | 8 | -0.152951 | 41.574 |
| w11 | 0 | None | 0.0 |
| w12 | 8 | 0.071361 | 26.28 |
| w13 | 2 | -0.163175 | -6.94 |
| w14 | 6 | -0.034897 | -34.012 |
| w15 | 0 | -0.214259 | 0.0 |
| w16 | 1 | -0.044289 | -3.554 |
| w17 | 8 | -0.019025 | 0.131 |
| w18 | 4 | -0.013132 | 22.155 |
| w19 | 6 | 0.068573 | 32.159 |
| w20 | 12 | -0.072689 | -19.747 |
| w21 | 15 | -0.024316 | 15.962 |
| w22 | 0 | None | 0.0 |
| w23 | 8 | 0.096467 | 35.682 |
| w24 | 5 | -0.18877 | -25.113 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.090831 | -27.935 |
| w2 | 4 | -0.040896 | -9.701 |
| w3 | 11 | -0.041856 | -16.47 |
| w4 | 13 | -0.185653 | 16.638 |
| w5 | 21 | 0.110178 | -11.188 |
| w6 | 11 | 0.011605 | 17.005 |
| w7 | 9 | -0.060025 | -23.778 |
| w8 | 5 | -0.019097 | 8.237 |
| w9 | 6 | -0.200856 | -36.859 |
| w10 | 10 | -0.115629 | 20.786 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | -0.00552 | -22.19 |
| w14 | 12 | -0.0585 | -42.996 |
| w15 | 0 | None | 0.0 |
| w16 | 4 | -0.093763 | 6.425 |
| w17 | 2 | 0.133098 | 3.54 |
| w18 | 7 | 0.043957 | 20.092 |
| w19 | 2 | -0.017154 | -13.97 |
| w20 | 8 | 0.001604 | 4.639 |
| w21 | 16 | -0.011325 | 10.551 |
| w22 | 5 | 0.065951 | 38.605 |
| w23 | 9 | -0.035714 | -23.129 |
| w24 | 3 | 0.044928 | -0.312 |

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
| w1 | 11 | 0.000797 | -7.185 |
| w2 | 0 | -0.034355 | 0.0 |
| w3 | 0 | 0.018461 | 0.0 |
| w4 | 0 | -0.05177 | 0.0 |
| w5 | 4 | -0.050372 | 21.497 |
| w6 | 6 | 0.089814 | 68.852 |
| w8 | 12 | 0.043201 | 3.058 |
| w9 | 8 | -0.063966 | -31.372 |
| w10 | 10 | -0.065406 | 44.195 |
| w11 | 0 | None | 0.0 |
| w12 | 9 | -0.132847 | -19.764 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.3081 | 25.162 |
| w16 | 1 | -0.018224 | -0.897 |
| w17 | 7 | -0.003061 | 251.162 |
| w18 | 2 | 0.110223 | 34.888 |
| w19 | 7 | 0.020947 | -0.098 |
| w20 | 6 | -0.131008 | -10.562 |
| w21 | 7 | -0.038772 | 148.796 |
| w22 | 1 | -0.006203 | -1.298 |
| w23 | 11 | 0.086346 | 73.016 |
| w24 | 8 | -0.029312 | -22.695 |

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
| w1 | 1 | -0.027057 | -0.834 |
| w2 | 5 | -0.017104 | -11.108 |
| w3 | 8 | -0.065849 | -24.489 |
| w4 | 11 | -0.150841 | -6.318 |
| w5 | 14 | -0.077023 | -30.108 |
| w6 | 13 | 0.005727 | 7.614 |
| w7 | 6 | 0.107046 | -6.101 |
| w8 | 12 | -0.066898 | 34.773 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | 0.109888 | 1.291 |
| w11 | 0 | None | 0.0 |
| w12 | 7 | 0.045687 | 22.641 |
| w13 | 0 | None | 0.0 |
| w14 | 9 | 0.070162 | -24.365 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | 0.052979 | 17.289 |
| w18 | 2 | -0.004474 | 21.057 |
| w19 | 0 | None | 0.0 |
| w20 | 7 | -0.15494 | -29.083 |
| w21 | 6 | -0.030924 | 13.033 |
| w22 | 0 | None | 0.0 |
| w23 | 7 | 0.064451 | 4.179 |
| w24 | 4 | 0.020387 | 5.546 |

