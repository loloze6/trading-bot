# Backtest of 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e3_monthly-continuation-in-up-years_1h

- Plan: `../../../../03_test_plan/night3_1h_run/plans/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends.e2_monthly-rise-multiweek-continuation.e3_monthly-continuation-in-up-years_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.011835 | -2.385 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 31 | 0.018164 | 9.68 |
| w6 | 54 | 0.000359 | 75.792 |
| w7 | 27 | 0.006543 | 2.302 |
| w8 | 0 | None | 0.0 |
| w9 | 16 | -0.024351 | -22.205 |
| w10 | 35 | -0.000831 | 26.893 |
| w11 | 53 | -0.018327 | 33.183 |
| w12 | 37 | 0.016006 | 2.947 |
| w13 | 20 | -0.020839 | -11.692 |
| w14 | 17 | -0.00997 | -24.882 |
| w15 | 39 | -0.036922 | -5.078 |
| w16 | 45 | 0.00793 | 31.599 |
| w17 | 61 | 0.031337 | 148.563 |
| w18 | 28 | 0.021269 | 14.073 |
| w19 | 44 | 0.020985 | 42.575 |
| w20 | 25 | -0.035872 | -19.694 |
| w21 | 48 | 0.002148 | 76.38 |
| w22 | 23 | -0.014217 | -4.084 |
| w23 | 53 | 0.008442 | 28.465 |
| w24 | 29 | 0.014276 | -8.355 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 32 | -0.009076 | -3.244 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 25 | -0.004141 | -5.879 |
| w6 | 50 | 0.014462 | 36.513 |
| w7 | 0 | 0.023405 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 18 | -0.009468 | -33.821 |
| w10 | 28 | 0.023349 | 81.93 |
| w11 | 59 | -0.004281 | 105.65 |
| w12 | 37 | 0.007733 | -0.329 |
| w13 | 21 | 0.007827 | -4.069 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 55 | 0.007985 | 47.379 |
| w17 | 48 | 0.013178 | 63.155 |
| w18 | 36 | 0.011077 | 46.637 |
| w19 | 36 | 0.028428 | 51.205 |
| w20 | 24 | 0.004441 | -0.85 |
| w21 | 52 | 0.014337 | 52.422 |
| w22 | 2 | -0.017315 | -4.279 |
| w23 | 21 | -0.006776 | 16.73 |
| w24 | 25 | -0.012179 | -23.084 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.029985 | -4.468 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 1 | -0.012558 | -1.429 |
| w5 | 40 | -0.023653 | -26.618 |
| w6 | 40 | -0.04106 | -9.534 |
| w7 | 0 | 0.003213 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 12 | -0.027291 | -28.051 |
| w10 | 0 | None | 0.0 |
| w11 | 43 | -0.026134 | 34.978 |
| w12 | 31 | -0.006003 | -14.215 |
| w13 | 23 | -0.021046 | -10.951 |
| w14 | 0 | -0.017506 | 0.0 |
| w15 | 15 | -0.013506 | -14.008 |
| w16 | 35 | 0.011 | 26.273 |
| w17 | 24 | 0.002812 | 47.636 |
| w18 | 30 | 0.013377 | 3.971 |
| w19 | 16 | -0.013929 | -10.513 |
| w20 | 5 | 0.004758 | -5.581 |
| w21 | 51 | -0.001144 | 88.93 |
| w22 | 18 | -0.025865 | -25.679 |
| w23 | 53 | 0.01369 | 37.407 |
| w24 | 23 | -0.035178 | -38.822 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.01418 | -27.137 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 9 | -0.00632 | -0.587 |
| w5 | 25 | -0.003342 | -1.052 |
| w6 | 36 | -0.029552 | 21.216 |
| w7 | 0 | -0.00672 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 17 | -0.006536 | 25.404 |
| w11 | 43 | -0.012699 | 55.75 |
| w12 | 18 | -0.004337 | -7.46 |
| w14 | 0 | -0.00397 | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 34 | -0.001708 | 6.475 |
| w17 | 52 | 0.00024 | 38.439 |
| w18 | 31 | 0.003881 | 0.203 |
| w19 | 4 | -0.006609 | -2.725 |
| w20 | 29 | -0.018447 | 1.28 |
| w21 | 31 | -0.013382 | -7.659 |
| w22 | 27 | -0.014653 | 31.0 |
| w23 | 24 | 0.009496 | 2.729 |
| w24 | 23 | -0.042087 | 44.492 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 7757 warm-up bars -- required_bars=8761. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.025259 | -17.17 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 29 | 0.00321 | 5.722 |
| w6 | 24 | -0.003215 | 27.95 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | -0.013311 | -10.991 |
| w10 | 8 | -0.064635 | -10.012 |
| w11 | 44 | 0.0133 | 111.983 |
| w12 | 14 | -0.011939 | -7.623 |
| w14 | 0 | 0.005806 | 0.0 |
| w15 | 3 | -0.030786 | -10.298 |
| w16 | 4 | -0.008155 | -8.924 |
| w17 | 16 | 0.042252 | 130.733 |
| w18 | 18 | 0.024068 | 31.826 |
| w19 | 28 | 0.004725 | 0.761 |
| w20 | 14 | -0.030431 | -9.639 |
| w21 | 47 | 0.040694 | 166.775 |
| w22 | 35 | -0.013562 | -6.463 |
| w23 | 45 | 0.026962 | 36.311 |
| w24 | 17 | -0.005336 | -24.457 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 8280 warm-up bars -- required_bars=8761. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 5455 warm-up bars -- required_bars=8761. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.007799 | 22.036 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | -0.017997 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | -0.001895 | 0.11 |
| w11 | 55 | -0.018613 | 62.592 |
| w12 | 47 | -0.007306 | -12.954 |
| w13 | 19 | -0.00754 | -13.828 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 10 | -0.005949 | 12.21 |
| w17 | 37 | -0.019075 | -12.277 |
| w18 | 28 | 0.005371 | -3.433 |
| w19 | 0 | None | 0.0 |
| w20 | 16 | -0.036095 | 33.407 |
| w21 | 36 | -0.009815 | 39.804 |
| w22 | 29 | -0.028477 | -15.353 |
| w23 | 35 | -0.003675 | 3.195 |
| w24 | 66 | 0.023813 | 316.46 |

