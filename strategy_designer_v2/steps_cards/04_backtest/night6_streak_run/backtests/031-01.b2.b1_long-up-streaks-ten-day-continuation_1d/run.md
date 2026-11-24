# Backtest of 031-01.b2.b1_long-up-streaks-ten-day-continuation_1d

- Plan: `../../../../03_test_plan/night6_streak_run/plans/031-01.b2.b1_long-up-streaks-ten-day-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.014507 | -8.037 |
| w2 | 19 | -0.065428 | -30.904 |
| w3 | 15 | -0.074669 | -23.287 |
| w4 | 21 | 0.166549 | 98.315 |
| w5 | 17 | 0.018055 | -13.247 |
| w6 | 17 | 0.10687 | 99.82 |
| w7 | 17 | 0.100524 | -9.075 |
| w8 | 8 | 0.026482 | 51.737 |
| w9 | 11 | -0.013295 | -12.766 |
| w10 | 11 | -0.177327 | 23.217 |
| w11 | 28 | -0.008928 | 32.924 |
| w12 | 11 | -0.060851 | -3.452 |
| w13 | 17 | -0.056613 | -10.24 |
| w14 | 14 | 0.017166 | -43.315 |
| w15 | 31 | 0.108883 | 73.212 |
| w16 | 14 | -0.056855 | -12.399 |
| w17 | 24 | 0.057883 | 188.87 |
| w18 | 18 | 0.00537 | 5.054 |
| w19 | 21 | 0.092674 | 49.267 |
| w20 | 16 | -0.034176 | -8.054 |
| w21 | 25 | 0.072092 | 61.471 |
| w22 | 19 | -0.039632 | -2.392 |
| w23 | 14 | 0.023318 | 9.062 |
| w24 | 22 | -0.003151 | -31.666 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | 0.03278 | -5.632 |
| w2 | 13 | -0.008015 | -24.963 |
| w3 | 9 | -0.042015 | -15.675 |
| w4 | 26 | 0.061596 | 42.035 |
| w5 | 12 | -0.04196 | -8.647 |
| w6 | 31 | 0.00526 | 60.391 |
| w7 | 25 | 0.053758 | -26.851 |
| w8 | 11 | -0.127692 | 6.824 |
| w9 | 18 | 0.091871 | -19.818 |
| w10 | 13 | 0.074784 | 75.842 |
| w11 | 28 | -0.133433 | 49.748 |
| w12 | 10 | -0.051435 | -1.971 |
| w13 | 23 | 0.163864 | 22.545 |
| w14 | 10 | -0.022012 | -15.966 |
| w15 | 14 | 0.037411 | 16.798 |
| w16 | 18 | -0.043183 | 37.206 |
| w17 | 21 | -0.059406 | 25.445 |
| w18 | 20 | -0.008058 | 30.573 |
| w19 | 14 | -0.025382 | 19.61 |
| w20 | 12 | -0.061124 | -17.097 |
| w21 | 25 | -0.018524 | 33.39 |
| w22 | 4 | -0.141054 | -31.256 |
| w23 | 22 | 0.014826 | 69.672 |
| w24 | 22 | 0.10011 | -20.848 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.057389 | -14.533 |
| w2 | 17 | -0.038956 | -25.635 |
| w3 | 13 | 0.008944 | 4.016 |
| w4 | 11 | -0.037809 | 8.609 |
| w5 | 19 | 0.118966 | -4.892 |
| w6 | 24 | -0.002945 | 7.844 |
| w7 | 14 | -0.07738 | -35.26 |
| w8 | 11 | -0.017848 | 64.187 |
| w9 | 15 | -0.056373 | -23.513 |
| w10 | 8 | -0.292221 | 27.835 |
| w11 | 24 | 0.016505 | 15.525 |
| w12 | 12 | 0.017786 | -7.705 |
| w13 | 11 | -0.142041 | -10.393 |
| w14 | 11 | 0.030362 | -30.198 |
| w15 | 8 | 0.003417 | -12.907 |
| w16 | 28 | -0.067445 | 14.761 |
| w17 | 30 | -0.090258 | 63.636 |
| w18 | 18 | -0.017985 | -1.035 |
| w19 | 23 | -0.015742 | 17.645 |
| w20 | 32 | 0.050463 | -12.894 |
| w21 | 29 | -0.142346 | 50.752 |
| w22 | 12 | 0.064064 | -8.061 |
| w23 | 15 | 0.040314 | 19.781 |
| w24 | 17 | -0.111833 | -25.48 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.068966 | -14.303 |
| w2 | 10 | -0.067395 | -0.897 |
| w3 | 5 | -0.158301 | -0.881 |
| w4 | 7 | -0.18681 | -2.359 |
| w5 | 22 | 0.220552 | -5.522 |
| w6 | 21 | -0.142549 | 20.429 |
| w7 | 14 | -0.023064 | -26.105 |
| w8 | 9 | -0.193943 | 28.437 |
| w9 | 14 | -0.03007 | -27.803 |
| w10 | 13 | -0.138656 | 59.088 |
| w11 | 17 | -0.005429 | 65.862 |
| w12 | 13 | -0.13408 | -14.823 |
| w14 | 8 | -0.181457 | -33.731 |
| w15 | 15 | 0.053192 | 14.471 |
| w16 | 23 | -0.019055 | 18.482 |
| w17 | 17 | -0.212206 | 39.552 |
| w18 | 24 | -0.05307 | -16.097 |
| w19 | 24 | -0.056639 | -37.104 |
| w20 | 31 | -0.077224 | 28.267 |
| w21 | 30 | 0.007355 | 2.873 |
| w22 | 22 | -0.021375 | 10.323 |
| w23 | 21 | 0.03282 | -8.52 |
| w24 | 20 | -0.007904 | 24.281 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=457. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.161808 | -10.679 |
| w2 | 9 | -0.093945 | -25.85 |
| w3 | 0 | -0.079372 | 0.0 |
| w4 | 0 | -0.054756 | 0.0 |
| w5 | 2 | -0.027791 | -1.717 |
| w6 | 18 | 0.003803 | 31.813 |
| w8 | 7 | -0.229701 | -7.762 |
| w9 | 19 | -0.018147 | -28.075 |
| w10 | 14 | 0.139648 | 46.514 |
| w11 | 16 | -0.106929 | 60.317 |
| w12 | 19 | -0.090044 | -26.962 |
| w14 | 10 | 0.143803 | 5.587 |
| w15 | 9 | 0.048809 | -11.464 |
| w16 | 20 | -0.007801 | -2.812 |
| w17 | 25 | 0.01809 | 98.766 |
| w18 | 14 | -0.134229 | 26.989 |
| w19 | 9 | -0.137702 | -3.684 |
| w20 | 19 | 0.063655 | 28.611 |
| w21 | 17 | 0.159979 | 262.444 |
| w22 | 12 | -0.051876 | -5.516 |
| w23 | 23 | 0.047723 | 27.378 |
| w24 | 15 | -0.049526 | -25.838 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=457. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=457. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.033463 | 1.112 |
| w2 | 17 | -0.051403 | -17.912 |
| w3 | 11 | -0.06694 | -29.718 |
| w4 | 22 | -0.024089 | -8.42 |
| w5 | 23 | 0.004153 | -16.36 |
| w6 | 26 | -0.052845 | 12.276 |
| w7 | 15 | -0.008734 | -22.717 |
| w8 | 15 | -0.086536 | 11.805 |
| w9 | 30 | 0.082484 | -34.408 |
| w10 | 10 | -0.128366 | 24.666 |
| w11 | 31 | 0.123506 | 65.312 |
| w12 | 13 | 0.101533 | 13.034 |
| w14 | 15 | -0.025901 | -37.007 |
| w15 | 11 | -0.001352 | -1.761 |
| w16 | 21 | 0.057751 | 57.241 |
| w17 | 13 | -0.065479 | -6.301 |
| w18 | 19 | -0.044161 | -2.873 |
| w19 | 19 | 0.005911 | -2.335 |
| w20 | 18 | 0.067101 | 32.617 |
| w21 | 18 | 0.009449 | 42.501 |
| w22 | 18 | -0.018883 | -15.614 |
| w23 | 20 | -0.014518 | -6.987 |
| w24 | 30 | 0.093379 | 250.363 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=457. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

