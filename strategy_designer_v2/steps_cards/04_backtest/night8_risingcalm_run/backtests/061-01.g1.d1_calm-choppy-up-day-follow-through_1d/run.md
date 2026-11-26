# Backtest of 061-01.g1.d1_calm-choppy-up-day-follow-through_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/061-01.g1.d1_calm-choppy-up-day-follow-through_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.072537 | -29.696 |
| w2 | 8 | -0.144875 | -37.658 |
| w3 | 14 | 0.041444 | -34.155 |
| w4 | 3 | 0.145526 | 41.203 |
| w5 | 25 | -0.040492 | -9.918 |
| w6 | 10 | -0.012914 | 33.408 |
| w7 | 20 | 0.024331 | 2.191 |
| w8 | 17 | -0.081705 | 3.247 |
| w9 | 13 | -0.09065 | -20.326 |
| w10 | 11 | 0.166879 | 29.581 |
| w11 | 1 | -0.108515 | -4.996 |
| w12 | 2 | 0.003458 | -1.238 |
| w13 | 8 | -0.089387 | 2.16 |
| w14 | 15 | 0.044754 | -12.513 |
| w15 | 0 | None | 0.0 |
| w16 | 5 | -0.052116 | 9.46 |
| w17 | 9 | 0.063545 | 33.292 |
| w18 | 3 | 0.162523 | 16.379 |
| w19 | 0 | None | 0.0 |
| w20 | 14 | 0.020353 | -6.032 |
| w21 | 7 | -0.059286 | 16.436 |
| w22 | 21 | 0.024724 | -16.858 |
| w23 | 12 | 0.117032 | 14.51 |
| w24 | 19 | 0.071237 | -6.371 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.011704 | -7.512 |
| w2 | 3 | -0.115809 | -12.642 |
| w3 | 10 | 0.053337 | -32.601 |
| w4 | 5 | 0.026953 | 28.247 |
| w5 | 27 | -0.062125 | -1.984 |
| w6 | 13 | 0.001986 | 3.219 |
| w7 | 5 | -0.056418 | -10.306 |
| w8 | 6 | 0.027683 | -1.524 |
| w9 | 12 | -0.015052 | -6.941 |
| w10 | 5 | -0.036576 | 14.904 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | -0.04506 | -3.292 |
| w13 | 0 | None | 0.0 |
| w14 | 1 | -0.004185 | -0.184 |
| w15 | 0 | None | 0.0 |
| w16 | 3 | -0.00416 | 5.906 |
| w17 | 11 | -0.012748 | 12.577 |
| w18 | 6 | 0.063956 | 21.352 |
| w19 | 0 | None | 0.0 |
| w20 | 9 | -0.021159 | 8.187 |
| w21 | 14 | -0.004632 | 7.919 |
| w22 | 2 | 0.01316 | 2.108 |
| w23 | 1 | 0.127603 | 11.054 |
| w24 | 3 | 0.00387 | 8.988 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.057309 | -19.983 |
| w2 | 14 | -0.05527 | -31.308 |
| w3 | 14 | 0.017376 | 31.787 |
| w4 | 8 | -0.061416 | 2.947 |
| w5 | 14 | 0.030368 | -16.523 |
| w6 | 21 | 0.134997 | 33.56 |
| w7 | 5 | -0.038863 | -10.328 |
| w8 | 3 | 0.041155 | 0.741 |
| w9 | 5 | -0.000114 | -4.655 |
| w10 | 16 | -0.112732 | 8.51 |
| w11 | 0 | None | 0.0 |
| w12 | 10 | 0.064904 | 12.253 |
| w13 | 2 | -0.163354 | -11.415 |
| w14 | 8 | -0.031185 | -10.536 |
| w15 | 0 | -0.214259 | 0.0 |
| w16 | 1 | -0.044289 | -3.664 |
| w17 | 6 | -0.021377 | -7.61 |
| w18 | 3 | -0.012409 | 11.083 |
| w19 | 14 | 0.059902 | 10.805 |
| w20 | 12 | -0.06335 | -33.604 |
| w21 | 15 | -0.002722 | 16.727 |
| w22 | 0 | None | 0.0 |
| w23 | 16 | 0.02827 | 33.934 |
| w24 | 10 | -0.165688 | -20.627 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.092662 | -22.192 |
| w2 | 4 | -0.040896 | -2.789 |
| w3 | 26 | -0.003014 | -11.093 |
| w4 | 29 | -0.149279 | -8.755 |
| w5 | 37 | 0.073412 | -10.086 |
| w6 | 15 | 0.050297 | -7.268 |
| w7 | 12 | -0.073014 | -15.575 |
| w8 | 14 | -0.03999 | 5.069 |
| w9 | 9 | -0.177334 | -23.864 |
| w10 | 10 | -0.110223 | 6.334 |
| w11 | 0 | None | 0.0 |
| w12 | 20 | 0.01713 | -28.327 |
| w14 | 11 | 0.010805 | -33.531 |
| w15 | 0 | None | 0.0 |
| w16 | 6 | -0.087969 | -0.235 |
| w17 | 2 | 0.133098 | 2.166 |
| w18 | 8 | 0.055698 | 13.925 |
| w19 | 2 | -0.017154 | -19.827 |
| w20 | 11 | -0.025665 | -5.648 |
| w21 | 20 | 0.003571 | 23.359 |
| w22 | 16 | 0.0127 | 28.127 |
| w23 | 8 | -0.068622 | -22.469 |
| w24 | 6 | 0.051633 | 2.311 |

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
| w1 | 13 | -0.009802 | -1.649 |
| w2 | 0 | -0.030261 | 0.0 |
| w3 | 0 | 0.027242 | 0.0 |
| w4 | 0 | -0.030226 | 0.0 |
| w5 | 8 | -0.048464 | -6.365 |
| w6 | 6 | 0.033029 | 34.509 |
| w8 | 18 | 0.06377 | 7.372 |
| w9 | 9 | -0.078254 | -20.738 |
| w10 | 19 | -0.061834 | -13.31 |
| w11 | 0 | None | 0.0 |
| w12 | 13 | -0.089477 | -8.413 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.301307 | 23.254 |
| w16 | 1 | -0.018224 | -0.897 |
| w17 | 8 | -0.007429 | 33.431 |
| w18 | 2 | 0.097163 | 38.358 |
| w19 | 11 | 0.039037 | -16.058 |
| w20 | 8 | -0.134979 | -22.441 |
| w21 | 11 | -0.022505 | 77.251 |
| w22 | 2 | -0.000196 | -0.886 |
| w23 | 24 | 0.070712 | 38.183 |
| w24 | 10 | -0.014808 | -8.726 |

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
| w1 | 1 | -0.027057 | -1.338 |
| w2 | 7 | 0.026414 | -4.264 |
| w3 | 11 | -0.076927 | -8.655 |
| w4 | 18 | -0.164472 | -6.89 |
| w5 | 16 | -0.045699 | -13.582 |
| w6 | 15 | -0.004107 | -6.884 |
| w7 | 5 | 0.166455 | 12.028 |
| w8 | 19 | -0.116316 | 8.709 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | 0.109888 | -1.765 |
| w11 | 0 | None | 0.0 |
| w12 | 11 | 0.053449 | 13.826 |
| w13 | 0 | None | 0.0 |
| w14 | 9 | 0.057744 | -6.271 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 8 | 0.062091 | 17.247 |
| w18 | 2 | -0.012506 | 8.813 |
| w19 | 0 | None | 0.0 |
| w20 | 9 | -0.12857 | -19.305 |
| w21 | 7 | -0.019754 | 8.696 |
| w22 | 0 | None | 0.0 |
| w23 | 10 | 0.099821 | 0.784 |
| w24 | 2 | 0.019531 | 4.317 |

