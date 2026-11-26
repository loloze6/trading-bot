# Backtest of 038-02_calm-scaled-weekly-fall-continues_1d

- Plan: `../../../../03_test_plan/night7_chopreversal_run/plans/038-02_calm-scaled-weekly-fall-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 38 | 0.0098 | 14.295 |
| w2 | 28 | 0.062029 | 42.11 |
| w3 | 26 | 0.0758 | 3.213 |
| w4 | 22 | 0.047317 | -14.367 |
| w5 | 49 | 0.068644 | 16.367 |
| w6 | 15 | -0.064159 | -16.98 |
| w7 | 47 | 0.056488 | 5.48 |
| w8 | 23 | -0.054209 | -11.233 |
| w9 | 34 | -0.181924 | -36.115 |
| w10 | 24 | 0.015657 | -3.543 |
| w11 | 5 | 0.057012 | 0.761 |
| w12 | 37 | -0.036602 | -2.063 |
| w13 | 11 | 0.017182 | -3.463 |
| w14 | 24 | 0.126393 | 60.998 |
| w15 | 2 | -0.081792 | 0.094 |
| w16 | 23 | 0.005139 | -17.385 |
| w17 | 9 | 0.117977 | -3.884 |
| w18 | 6 | -0.06546 | -4.423 |
| w19 | 4 | -0.060063 | -9.786 |
| w20 | 16 | 0.025268 | 5.199 |
| w21 | 23 | -0.124119 | -22.583 |
| w22 | 20 | -0.09827 | -19.275 |
| w23 | 34 | -0.032171 | -3.886 |
| w24 | 13 | -0.06651 | 6.0 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | -0.002563 | 17.348 |
| w2 | 8 | 0.175874 | 35.35 |
| w3 | 18 | 0.133378 | 6.837 |
| w4 | 25 | -0.019921 | -19.56 |
| w5 | 45 | 0.040549 | 15.413 |
| w6 | 24 | 0.022539 | -10.186 |
| w7 | 51 | -0.042264 | 20.951 |
| w8 | 20 | -0.090405 | -17.421 |
| w9 | 29 | -0.050356 | -6.948 |
| w10 | 28 | -0.038266 | -12.421 |
| w11 | 6 | -0.063608 | -10.284 |
| w12 | 28 | -0.068792 | -7.526 |
| w13 | 17 | 0.147624 | 28.117 |
| w14 | 8 | 0.23901 | 50.119 |
| w15 | 22 | 0.046225 | 5.094 |
| w16 | 4 | -0.043354 | -6.526 |
| w17 | 11 | -0.054998 | -15.911 |
| w18 | 8 | -0.104806 | -2.148 |
| w19 | 0 | None | 0.0 |
| w20 | 8 | 0.056071 | 5.529 |
| w21 | 17 | -0.111898 | -36.041 |
| w22 | 12 | -0.042271 | 0.56 |
| w23 | 15 | -0.018622 | -14.079 |
| w24 | 23 | 0.004493 | 7.172 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 40 | -0.019935 | 8.382 |
| w2 | 21 | -0.028488 | 6.699 |
| w3 | 23 | 0.005184 | -6.394 |
| w4 | 21 | 0.008582 | -9.484 |
| w5 | 23 | 0.113366 | 17.274 |
| w6 | 32 | -0.018279 | -4.977 |
| w7 | 51 | 0.012155 | 32.2 |
| w8 | 4 | -0.060662 | -7.964 |
| w9 | 40 | -0.011406 | 7.73 |
| w10 | 44 | -0.03513 | -16.937 |
| w11 | 4 | -0.085872 | -7.79 |
| w12 | 13 | -0.025365 | -6.745 |
| w13 | 31 | -0.059657 | -0.557 |
| w14 | 23 | 0.118588 | 43.965 |
| w15 | 21 | 0.125635 | 26.393 |
| w16 | 11 | -0.06971 | -14.487 |
| w17 | 12 | -0.083585 | -18.952 |
| w18 | 13 | -0.020224 | -3.519 |
| w19 | 12 | -0.10032 | -27.087 |
| w20 | 22 | 0.005284 | 6.379 |
| w21 | 14 | -0.038777 | -17.537 |
| w22 | 2 | 0.016948 | 10.511 |
| w23 | 32 | -0.143817 | -13.375 |
| w24 | 17 | -0.013712 | 4.609 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.015343 | -2.144 |
| w2 | 12 | -0.095835 | -9.605 |
| w3 | 29 | -0.088994 | -8.964 |
| w4 | 37 | -0.044146 | -10.85 |
| w5 | 63 | -0.019087 | 4.532 |
| w6 | 30 | -0.080031 | -24.187 |
| w7 | 52 | 0.000893 | 17.78 |
| w8 | 27 | -0.09819 | -13.693 |
| w9 | 45 | 0.032734 | 8.746 |
| w10 | 31 | -0.192789 | -17.527 |
| w11 | 4 | -0.035499 | -5.398 |
| w12 | 33 | -0.059824 | 4.775 |
| w14 | 21 | 0.133203 | 52.353 |
| w15 | 18 | 0.03854 | 6.59 |
| w16 | 5 | 0.01602 | -4.504 |
| w17 | 10 | -0.110793 | -11.23 |
| w18 | 9 | -0.024997 | -8.808 |
| w19 | 3 | 0.125959 | 17.788 |
| w20 | 7 | -0.031807 | -16.755 |
| w21 | 30 | 0.017006 | -10.044 |
| w22 | 13 | 0.055068 | -4.964 |
| w23 | 15 | 0.106727 | 29.351 |
| w24 | 6 | 0.024294 | -2.485 |

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
| w1 | 33 | 0.084879 | 20.523 |
| w2 | 7 | -0.122921 | 22.391 |
| w3 | 0 | -0.014664 | 0.0 |
| w4 | 0 | -0.014655 | 0.0 |
| w5 | 15 | 0.050828 | -27.312 |
| w6 | 16 | 0.020873 | -5.959 |
| w8 | 47 | -0.18891 | -13.98 |
| w9 | 45 | -0.006618 | 11.281 |
| w10 | 43 | 0.014789 | -0.556 |
| w11 | 0 | None | 0.0 |
| w12 | 49 | -0.078981 | -1.09 |
| w14 | 27 | 0.046223 | 4.145 |
| w15 | 31 | 0.036254 | 3.803 |
| w16 | 0 | -0.194304 | 0.0 |
| w17 | 13 | -0.014188 | -8.653 |
| w18 | 16 | -0.044678 | -10.673 |
| w19 | 18 | -0.097631 | -20.119 |
| w20 | 31 | 0.009665 | -2.906 |
| w21 | 7 | -0.009757 | -10.994 |
| w22 | 4 | 0.073604 | 4.112 |
| w23 | 42 | -0.062126 | -17.222 |
| w24 | 39 | -0.039013 | 31.574 |

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
| w1 | 39 | 0.12177 | 11.852 |
| w2 | 18 | -0.096585 | -12.708 |
| w3 | 44 | 0.028104 | 26.171 |
| w4 | 39 | 0.012798 | -0.789 |
| w5 | 31 | 0.102621 | 35.391 |
| w6 | 23 | -0.018766 | -12.472 |
| w7 | 47 | -0.050913 | -1.079 |
| w8 | 37 | -0.003138 | -1.56 |
| w9 | 23 | 0.047496 | -2.302 |
| w10 | 28 | -0.150817 | -26.169 |
| w11 | 4 | -0.060222 | -10.474 |
| w12 | 14 | -0.028398 | -22.574 |
| w13 | 19 | 0.065764 | -0.743 |
| w14 | 30 | 0.099235 | 18.494 |
| w15 | 22 | -0.031138 | -2.681 |
| w16 | 0 | None | 0.0 |
| w17 | 14 | -0.011482 | -9.293 |
| w18 | 7 | -0.015436 | -1.53 |
| w19 | 0 | None | 0.0 |
| w20 | 11 | -0.022491 | -3.093 |
| w21 | 15 | -0.08139 | -9.101 |
| w22 | 1 | 0.000429 | 4.272 |
| w23 | 36 | -0.085046 | -24.37 |
| w24 | 4 | -0.003577 | -6.873 |

