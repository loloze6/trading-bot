# Backtest of 040-01_agitated-fall-size-next-day-rebound_1d

- Plan: `../../../../03_test_plan/night7_steadydecline_run/plans/040-01_agitated-fall-size-next-day-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.057602 | -6.623 |
| w2 | 26 | 0.098307 | 1.538 |
| w3 | 24 | 0.208064 | 18.06 |
| w4 | 10 | 0.106486 | 7.855 |
| w5 | 0 | None | 0.0 |
| w6 | 23 | 0.264466 | 43.17 |
| w7 | 0 | None | 0.0 |
| w8 | 12 | 0.039585 | 2.927 |
| w9 | 15 | -0.027261 | -5.73 |
| w10 | 15 | 0.046276 | 7.59 |
| w11 | 37 | 0.06541 | 16.618 |
| w12 | 12 | 0.056713 | 4.466 |
| w13 | 40 | 0.005833 | -1.09 |
| w14 | 20 | 0.178107 | 20.34 |
| w15 | 44 | -0.072111 | -2.911 |
| w16 | 21 | 0.259208 | 27.961 |
| w17 | 20 | 0.028039 | 11.489 |
| w18 | 41 | 0.196239 | 28.577 |
| w19 | 39 | 0.11409 | 22.555 |
| w20 | 39 | 0.05075 | 0.241 |
| w21 | 18 | 0.055615 | 9.9 |
| w22 | 25 | 0.192933 | 22.512 |
| w23 | 2 | -0.036521 | -0.404 |
| w24 | 34 | -0.000169 | -10.312 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.146887 | -12.956 |
| w2 | 47 | 0.041611 | -9.093 |
| w3 | 23 | 0.284552 | 28.685 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 20 | 0.171161 | 22.954 |
| w7 | 0 | None | 0.0 |
| w8 | 16 | 0.175541 | 11.606 |
| w9 | 13 | 0.044206 | 1.636 |
| w10 | 16 | 0.040661 | 6.955 |
| w11 | 33 | 0.08398 | 23.645 |
| w12 | 9 | 0.067439 | 5.19 |
| w13 | 24 | -0.087489 | -11.072 |
| w14 | 41 | 0.175631 | 18.8 |
| w15 | 20 | 0.03331 | 3.64 |
| w16 | 32 | 0.01459 | -9.61 |
| w17 | 23 | 0.01191 | 1.324 |
| w18 | 36 | 0.086284 | 16.957 |
| w19 | 34 | -0.082026 | -13.922 |
| w20 | 42 | 0.094915 | 0.042 |
| w21 | 34 | 0.0086 | 5.506 |
| w22 | 47 | 0.080735 | -2.206 |
| w23 | 17 | 0.134424 | 22.138 |
| w24 | 22 | 0.041001 | -2.578 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 32 | 0.089917 | 4.519 |
| w3 | 19 | 0.160189 | 20.066 |
| w4 | 9 | 0.134848 | 8.987 |
| w5 | 22 | 0.02596 | -1.141 |
| w6 | 1 | 0.066606 | 2.17 |
| w7 | 0 | None | 0.0 |
| w8 | 40 | 0.044923 | 13.539 |
| w9 | 0 | None | 0.0 |
| w10 | 10 | 0.030032 | 2.97 |
| w11 | 43 | -0.094683 | -6.253 |
| w12 | 21 | -0.054742 | -10.396 |
| w13 | 25 | -0.017672 | 0.781 |
| w14 | 27 | 0.178808 | 17.087 |
| w15 | 27 | 0.152929 | 16.032 |
| w16 | 22 | 0.060985 | -5.082 |
| w17 | 25 | 0.049753 | 11.685 |
| w18 | 31 | 0.152329 | 17.744 |
| w19 | 31 | 0.139017 | 30.318 |
| w20 | 26 | 0.118882 | 6.934 |
| w21 | 34 | -0.020872 | -0.386 |
| w22 | 46 | -0.082887 | -12.613 |
| w23 | 11 | 0.065986 | 5.644 |
| w24 | 30 | -0.024777 | -7.709 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | -0.061794 | -11.231 |
| w2 | 29 | 0.012362 | -5.585 |
| w3 | 10 | 0.107367 | 5.976 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 10 | 0.0538 | 2.506 |
| w7 | 0 | None | 0.0 |
| w8 | 10 | 0.085102 | 3.852 |
| w9 | 2 | 0.03494 | 0.551 |
| w10 | 5 | 0.089388 | 6.606 |
| w11 | 36 | 0.024787 | 20.768 |
| w12 | 10 | -0.000264 | -3.375 |
| w14 | 29 | 0.132007 | 8.17 |
| w15 | 29 | 0.003776 | -0.719 |
| w16 | 31 | 0.079767 | 0.266 |
| w17 | 22 | -0.032179 | -5.802 |
| w18 | 36 | 0.227858 | 36.529 |
| w19 | 47 | 0.25127 | 44.524 |
| w20 | 26 | 0.140868 | 16.13 |
| w21 | 19 | 0.093073 | 11.334 |
| w22 | 25 | 0.092814 | 11.051 |
| w23 | 27 | -0.187471 | -23.207 |
| w24 | 34 | -0.088538 | -6.986 |

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
| w1 | 6 | 0.104946 | 2.67 |
| w2 | 0 | -0.001701 | 0.0 |
| w3 | 0 | 0.149245 | 0.0 |
| w4 | 0 | 0.104684 | 0.0 |
| w5 | 25 | -0.03563 | 0.026 |
| w6 | 16 | 0.063067 | 7.869 |
| w8 | 4 | 0.086274 | 2.678 |
| w9 | 12 | 0.081682 | 4.606 |
| w10 | 7 | 0.045674 | 4.402 |
| w11 | 42 | 0.007462 | 19.777 |
| w12 | 4 | -0.031062 | -1.371 |
| w14 | 18 | 0.084258 | 6.812 |
| w15 | 20 | 0.050846 | 3.594 |
| w16 | 43 | 0.031877 | -7.083 |
| w17 | 32 | 0.000158 | 5.182 |
| w18 | 27 | 0.155514 | 11.783 |
| w19 | 34 | -0.014101 | -6.705 |
| w20 | 22 | -0.029154 | -2.676 |
| w21 | 33 | -0.037713 | 13.913 |
| w22 | 43 | 0.027829 | 0.465 |
| w23 | 11 | 0.084342 | 7.217 |
| w24 | 11 | 0.032975 | -1.089 |

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
| w1 | 15 | 0.141169 | 10.667 |
| w2 | 36 | 0.130237 | 7.558 |
| w3 | 9 | 0.209174 | 15.479 |
| w4 | 6 | -0.033887 | -1.441 |
| w5 | 17 | 0.107344 | 9.505 |
| w6 | 10 | 0.102736 | 7.663 |
| w7 | 8 | -0.014689 | -2.522 |
| w8 | 8 | 0.160206 | 3.965 |
| w9 | 23 | 0.125429 | 7.101 |
| w10 | 20 | -0.048847 | 2.292 |
| w11 | 37 | 0.016867 | 18.427 |
| w12 | 28 | 0.002941 | -0.132 |
| w13 | 29 | 0.060452 | 4.988 |
| w14 | 22 | 0.166226 | 14.654 |
| w15 | 29 | 0.053706 | 0.459 |
| w16 | 48 | 0.021893 | 11.218 |
| w17 | 27 | 0.014588 | -6.055 |
| w18 | 36 | 0.23555 | 30.917 |
| w19 | 56 | 0.041557 | -6.418 |
| w20 | 38 | -0.068347 | -5.435 |
| w21 | 40 | -0.02664 | 4.46 |
| w22 | 44 | -0.088222 | -17.883 |
| w23 | 13 | -0.060982 | -5.152 |
| w24 | 39 | -0.055312 | 8.077 |

