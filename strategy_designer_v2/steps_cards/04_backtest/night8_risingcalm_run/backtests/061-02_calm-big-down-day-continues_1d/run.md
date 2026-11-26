# Backtest of 061-02_calm-big-down-day-continues_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/061-02_calm-big-down-day-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 38 | -0.005799 | -1.114 |
| w2 | 27 | 0.028715 | 42.68 |
| w3 | 30 | 0.207744 | -0.534 |
| w4 | 33 | 0.069022 | -34.617 |
| w5 | 44 | 0.004972 | 5.783 |
| w6 | 23 | 0.108736 | -12.278 |
| w7 | 54 | -0.071535 | -2.35 |
| w8 | 35 | -0.062016 | -24.951 |
| w9 | 37 | -0.050762 | -10.325 |
| w10 | 32 | -0.091987 | -26.244 |
| w11 | 11 | 0.077044 | 7.563 |
| w12 | 30 | 0.116155 | 17.879 |
| w13 | 14 | 0.008972 | -7.528 |
| w14 | 43 | 0.144062 | 62.267 |
| w15 | 6 | -0.187178 | -10.481 |
| w16 | 29 | -0.021533 | -0.852 |
| w17 | 32 | 0.104415 | -41.478 |
| w18 | 13 | -0.097243 | -7.929 |
| w19 | 7 | -0.012159 | -6.465 |
| w20 | 7 | 0.07882 | 16.928 |
| w21 | 27 | 0.130685 | -21.925 |
| w22 | 19 | 0.076866 | 25.255 |
| w23 | 48 | -0.005901 | -8.727 |
| w24 | 22 | 0.08027 | 21.771 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 42 | 0.017597 | 14.265 |
| w2 | 7 | 0.042404 | 31.38 |
| w3 | 31 | 0.138411 | 8.958 |
| w4 | 44 | -0.07819 | -35.088 |
| w5 | 57 | -0.052661 | 9.426 |
| w6 | 32 | -0.027356 | -25.755 |
| w7 | 49 | -0.088644 | 44.473 |
| w8 | 38 | -0.016014 | -18.94 |
| w9 | 38 | 0.064377 | 39.225 |
| w10 | 30 | -0.124691 | -42.214 |
| w11 | 13 | 0.008882 | -14.292 |
| w12 | 37 | -0.095052 | -8.738 |
| w13 | 22 | 0.011706 | 17.722 |
| w14 | 19 | 0.167661 | 77.609 |
| w15 | 36 | 0.016434 | -19.981 |
| w16 | 17 | -0.141003 | -32.606 |
| w17 | 20 | -0.072588 | -33.719 |
| w18 | 9 | -0.125433 | -21.779 |
| w19 | 10 | -0.218599 | -22.112 |
| w20 | 6 | 0.089512 | 16.996 |
| w21 | 21 | 0.107675 | -27.966 |
| w22 | 15 | -0.095816 | 5.361 |
| w23 | 31 | 0.127095 | -28.537 |
| w24 | 28 | 0.101719 | 14.599 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 45 | -0.03081 | 10.164 |
| w2 | 27 | -0.056349 | 19.204 |
| w3 | 34 | 0.108095 | -23.369 |
| w4 | 41 | 0.029387 | -17.996 |
| w5 | 27 | 0.08909 | 38.607 |
| w6 | 49 | -0.043895 | -35.699 |
| w7 | 44 | -0.154345 | 50.933 |
| w8 | 12 | 0.002394 | -24.93 |
| w9 | 44 | 0.029183 | 23.383 |
| w10 | 41 | -0.235751 | -33.943 |
| w11 | 5 | -0.081541 | -16.321 |
| w12 | 30 | 0.058081 | -1.354 |
| w13 | 29 | -0.074968 | 9.293 |
| w14 | 29 | 0.00064 | 43.84 |
| w15 | 22 | 0.153048 | 12.921 |
| w16 | 21 | -0.086885 | -33.606 |
| w17 | 14 | -0.036828 | -24.81 |
| w18 | 19 | -0.132037 | -22.39 |
| w19 | 13 | 0.081885 | -11.067 |
| w20 | 24 | 0.027234 | 23.249 |
| w21 | 20 | 0.055406 | -15.828 |
| w22 | 2 | 0.109656 | 6.875 |
| w23 | 51 | -0.114108 | -29.812 |
| w24 | 24 | -0.032749 | 18.073 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | -0.094525 | 1.056 |
| w2 | 21 | -0.121963 | -12.634 |
| w3 | 36 | -0.083252 | -10.655 |
| w4 | 46 | -0.190809 | -30.661 |
| w5 | 41 | 0.019433 | 12.688 |
| w6 | 40 | -0.163465 | -37.547 |
| w7 | 48 | -0.195277 | 1.532 |
| w8 | 32 | -0.169398 | -37.746 |
| w9 | 50 | -0.041885 | 18.268 |
| w10 | 49 | -0.30628 | -52.333 |
| w11 | 8 | -0.09533 | -26.476 |
| w12 | 32 | -0.017089 | 4.863 |
| w14 | 25 | -0.033211 | 50.81 |
| w15 | 21 | 0.050107 | -10.565 |
| w16 | 17 | -0.088314 | -14.316 |
| w17 | 21 | -0.241928 | -21.222 |
| w18 | 15 | -0.103876 | -15.366 |
| w19 | 1 | 0.144092 | 12.433 |
| w20 | 10 | -0.163332 | -18.482 |
| w21 | 26 | 0.036186 | -6.672 |
| w22 | 20 | -0.045799 | -9.165 |
| w23 | 20 | -0.039912 | 2.244 |
| w24 | 10 | 0.013745 | 5.111 |

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
| w1 | 48 | -0.016299 | -12.641 |
| w2 | 5 | -0.096727 | 37.568 |
| w3 | 0 | -0.103059 | 0.0 |
| w4 | 0 | -0.284615 | 0.0 |
| w5 | 17 | -0.030984 | -25.093 |
| w6 | 32 | -0.124794 | -23.148 |
| w8 | 44 | -0.193909 | -4.809 |
| w9 | 33 | 0.067279 | 60.802 |
| w10 | 37 | -0.177108 | -29.753 |
| w11 | 0 | None | 0.0 |
| w12 | 47 | -0.090854 | 8.308 |
| w14 | 33 | 0.019058 | -18.455 |
| w15 | 38 | -0.001254 | -26.708 |
| w16 | 8 | -0.065191 | -19.973 |
| w17 | 21 | 0.020046 | -74.595 |
| w18 | 23 | -0.140191 | -31.999 |
| w19 | 23 | -0.139718 | -15.416 |
| w20 | 22 | 0.001455 | 21.109 |
| w21 | 18 | 0.090067 | -9.696 |
| w22 | 5 | -0.035007 | 10.237 |
| w23 | 47 | -0.100704 | -18.225 |
| w24 | 34 | 0.082334 | 29.409 |

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
| w1 | 37 | 0.115006 | -3.491 |
| w2 | 15 | -0.008225 | -5.652 |
| w3 | 35 | 0.005838 | 26.968 |
| w4 | 38 | -0.099039 | -13.516 |
| w5 | 38 | 0.093874 | 51.884 |
| w6 | 49 | -0.083764 | -38.444 |
| w7 | 45 | -0.171105 | -26.615 |
| w8 | 45 | -0.120325 | -23.747 |
| w9 | 33 | 0.160929 | 17.988 |
| w10 | 36 | -0.158323 | -43.701 |
| w11 | 8 | 0.094012 | -11.979 |
| w12 | 22 | -0.026027 | -26.268 |
| w13 | 22 | -0.051115 | 3.459 |
| w14 | 34 | 0.055381 | 39.633 |
| w15 | 25 | -0.044198 | -19.136 |
| w16 | 0 | None | 0.0 |
| w17 | 20 | -0.104447 | -26.219 |
| w18 | 13 | -0.103434 | -15.117 |
| w19 | 0 | None | 0.0 |
| w20 | 21 | 0.002708 | -0.32 |
| w21 | 16 | 0.083604 | -8.355 |
| w22 | 4 | -0.037724 | 6.053 |
| w23 | 37 | -0.049934 | -31.407 |
| w24 | 11 | -0.061518 | -43.787 |

