# Backtest of 031-01_up-streak-length-reversal_1d

- Plan: `../../../../03_test_plan/night6_streak_run/plans/031-01_up-streak-length-reversal_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | -0.020658 | 4.645 |
| w2 | 37 | 0.043106 | 34.561 |
| w3 | 30 | -0.0159 | 21.596 |
| w4 | 34 | -0.112413 | -63.175 |
| w5 | 28 | 0.026927 | -3.928 |
| w6 | 31 | 0.011097 | -63.504 |
| w7 | 36 | -0.115326 | 3.024 |
| w8 | 27 | 0.098855 | -49.223 |
| w9 | 34 | 0.035368 | 50.631 |
| w10 | 28 | 0.155998 | -38.209 |
| w11 | 36 | 0.070068 | -49.014 |
| w12 | 31 | 0.025594 | 0.576 |
| w13 | 26 | 0.045061 | -6.058 |
| w14 | 32 | 0.041544 | 101.091 |
| w15 | 45 | -0.144122 | -47.917 |
| w16 | 33 | 0.160866 | -2.668 |
| w17 | 36 | -0.066187 | -73.673 |
| w18 | 27 | 0.107328 | 9.742 |
| w19 | 39 | -0.013962 | -44.687 |
| w20 | 33 | 0.06389 | 3.39 |
| w21 | 35 | 0.025517 | -57.158 |
| w22 | 24 | 0.058481 | 3.801 |
| w23 | 35 | -0.025429 | -22.49 |
| w24 | 39 | -0.02745 | 37.366 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | -0.078905 | 11.735 |
| w2 | 31 | 0.026774 | 24.144 |
| w3 | 21 | 0.03992 | 10.717 |
| w4 | 34 | 0.000337 | -46.49 |
| w5 | 22 | 0.067488 | 11.375 |
| w6 | 24 | 0.003885 | -49.773 |
| w7 | 33 | -0.0366 | 43.891 |
| w8 | 19 | 0.14539 | -23.503 |
| w9 | 29 | 0.022299 | -4.857 |
| w10 | 40 | -0.018738 | -60.707 |
| w11 | 40 | 0.086311 | -61.491 |
| w12 | 27 | 0.05069 | -0.46 |
| w13 | 29 | -0.142664 | -31.107 |
| w14 | 26 | 0.071464 | 42.037 |
| w15 | 30 | -0.05734 | -32.02 |
| w16 | 35 | 0.077708 | -34.932 |
| w17 | 38 | 0.003746 | -47.307 |
| w18 | 39 | 0.086534 | -23.378 |
| w19 | 36 | 0.019861 | -39.753 |
| w20 | 36 | 0.05729 | -2.665 |
| w21 | 37 | 0.032859 | -48.778 |
| w22 | 25 | 0.145292 | 90.732 |
| w23 | 37 | 0.007866 | -68.481 |
| w24 | 26 | -0.098518 | 34.045 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | 0.067891 | 28.248 |
| w2 | 27 | 0.078712 | 43.793 |
| w3 | 27 | -0.022718 | -36.759 |
| w4 | 41 | 0.03842 | -20.397 |
| w5 | 33 | -0.056277 | 6.514 |
| w6 | 40 | -0.002652 | -21.103 |
| w7 | 27 | 0.07454 | 59.219 |
| w8 | 22 | 0.002059 | -54.092 |
| w9 | 33 | 0.046942 | 27.44 |
| w10 | 33 | 0.260216 | -43.004 |
| w11 | 38 | -0.071375 | -51.498 |
| w12 | 36 | -0.058903 | -6.249 |
| w13 | 28 | 0.111532 | 12.29 |
| w14 | 18 | 0.126729 | 91.977 |
| w15 | 33 | -0.03255 | -1.724 |
| w16 | 36 | 0.11497 | -24.207 |
| w17 | 34 | 0.057481 | -59.726 |
| w18 | 26 | 0.124735 | -11.78 |
| w19 | 30 | 0.053283 | -40.412 |
| w20 | 21 | 0.022393 | 18.745 |
| w21 | 38 | 0.136905 | -56.362 |
| w22 | 34 | -0.049271 | 6.706 |
| w23 | 27 | 0.079406 | -25.656 |
| w24 | 33 | 0.074261 | 40.586 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | 0.057201 | -14.989 |
| w2 | 34 | 0.070629 | -10.223 |
| w3 | 24 | 0.163573 | 10.899 |
| w4 | 23 | 0.13421 | -11.501 |
| w5 | 31 | -0.080306 | -3.41 |
| w6 | 30 | 0.098315 | -27.93 |
| w7 | 18 | 0.099939 | 38.013 |
| w8 | 18 | 0.170742 | -32.385 |
| w9 | 28 | 0.018151 | 43.468 |
| w10 | 34 | 0.206589 | -42.424 |
| w11 | 27 | 0.042163 | -56.713 |
| w12 | 28 | 0.042274 | 33.333 |
| w14 | 21 | 0.199679 | 104.996 |
| w15 | 30 | -0.040542 | -40.971 |
| w16 | 27 | 0.099602 | -52.376 |
| w17 | 29 | 0.198023 | -37.214 |
| w18 | 30 | 0.154116 | 2.236 |
| w19 | 33 | 0.026487 | 61.776 |
| w20 | 29 | 0.189678 | -29.255 |
| w21 | 30 | 0.020239 | -46.266 |
| w22 | 36 | 0.016666 | -39.15 |
| w23 | 44 | -0.066771 | -1.714 |
| w24 | 37 | 0.007892 | -34.004 |

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
| w1 | 33 | -0.06423 | -5.889 |
| w2 | 30 | 0.06414 | 23.468 |
| w3 | 0 | 0.079641 | 0.0 |
| w4 | 0 | 0.209643 | 0.0 |
| w5 | 2 | 0.094349 | 7.186 |
| w6 | 42 | 0.043001 | -37.357 |
| w8 | 21 | 0.178712 | 12.24 |
| w9 | 29 | 0.019895 | -1.889 |
| w10 | 26 | 0.124304 | -38.4 |
| w11 | 31 | 0.036467 | -75.783 |
| w12 | 28 | 0.108746 | 14.876 |
| w14 | 24 | -0.12674 | -33.005 |
| w15 | 19 | -0.088885 | -33.996 |
| w16 | 16 | 0.091205 | -12.813 |
| w17 | 25 | -0.043684 | -86.871 |
| w18 | 31 | 0.157035 | -22.09 |
| w19 | 27 | 0.116873 | -5.13 |
| w20 | 32 | -0.014335 | -19.814 |
| w21 | 40 | -0.168845 | -83.292 |
| w22 | 40 | -0.001591 | 0.774 |
| w23 | 40 | -0.071442 | -27.78 |
| w24 | 35 | -0.000886 | 51.007 |

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
| w1 | 26 | -0.02501 | -23.837 |
| w2 | 35 | 0.050581 | 25.412 |
| w3 | 27 | 0.02613 | 41.154 |
| w4 | 29 | 0.040959 | -3.888 |
| w5 | 32 | -0.004755 | 61.969 |
| w6 | 41 | 0.083456 | -19.524 |
| w7 | 25 | -0.000333 | 29.93 |
| w8 | 11 | 0.169647 | -24.807 |
| w9 | 21 | -0.070496 | -7.463 |
| w10 | 28 | 0.096971 | -43.672 |
| w11 | 39 | -0.135801 | -68.533 |
| w12 | 33 | -0.051597 | -35.672 |
| w14 | 28 | 0.055705 | 75.188 |
| w15 | 13 | 0.075783 | -5.031 |
| w16 | 31 | -0.011309 | -40.045 |
| w17 | 30 | 0.048368 | -7.444 |
| w18 | 29 | 0.184851 | 5.126 |
| w19 | 31 | -0.029042 | -3.103 |
| w20 | 35 | -0.028928 | -34.425 |
| w21 | 32 | -0.099242 | -58.954 |
| w22 | 29 | -0.028954 | 23.065 |
| w23 | 32 | -0.072012 | -21.339 |
| w24 | 44 | -0.12812 | -96.12 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=457. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

