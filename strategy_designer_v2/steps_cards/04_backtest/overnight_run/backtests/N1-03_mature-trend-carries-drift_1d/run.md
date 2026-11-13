# Backtest of N1-03_mature-trend-carries-drift_1d

- Plan: `../../../../03_test_plan/overnight_run/plans_newcomp/N1-03_mature-trend-carries-drift_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 5 | -0.092424 | 12.12 |
| w5 | 1 | 0.020705 | -5.782 |
| w6 | 5 | -0.047872 | 10.954 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | -0.026012 | -0.664 |
| w9 | 1 | -0.086115 | -21.525 |
| w10 | 10 | 0.023043 | 48.357 |
| w11 | 1 | 0.093444 | 153.293 |
| w12 | 5 | -0.169526 | -17.806 |
| w13 | 2 | -0.188525 | -50.892 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | -0.161377 | 16.912 |
| w16 | 2 | -0.098177 | -4.067 |
| w17 | 6 | -0.176782 | 333.089 |
| w18 | 1 | -0.2123 | -39.239 |
| w19 | 4 | 0.095055 | 57.034 |
| w20 | 2 | -0.029517 | -6.145 |
| w21 | 5 | -0.082238 | 4.56 |
| w22 | 6 | -0.120356 | -29.744 |
| w23 | 11 | -0.101459 | 0.318 |
| w24 | 2 | 0.056637 | -4.694 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.0958 | -13.282 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 5 | -0.104658 | 11.843 |
| w5 | 1 | 0.010204 | -9.63 |
| w6 | 4 | -0.005448 | 5.201 |
| w7 | 1 | -0.011437 | -12.59 |
| w8 | 1 | -0.040081 | -1.187 |
| w9 | 0 | -0.088795 | 0.0 |
| w10 | 15 | 0.10234 | 243.772 |
| w11 | 2 | 0.116075 | 495.634 |
| w12 | 5 | -0.001939 | -7.184 |
| w13 | 2 | -0.066005 | -30.842 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | -0.111445 | -17.375 |
| w16 | 3 | -0.284929 | -33.965 |
| w17 | 8 | -0.189284 | 53.689 |
| w18 | 2 | -0.123068 | -39.5 |
| w19 | 5 | 0.012604 | 34.445 |
| w20 | 1 | 0.048754 | 4.396 |
| w21 | 3 | -0.091652 | -2.188 |
| w22 | 3 | -0.012846 | -15.068 |
| w23 | 5 | -0.033519 | 16.172 |
| w24 | 7 | -0.053321 | -46.017 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | -0.049304 | -1.684 |
| w4 | 7 | -0.24077 | -19.36 |
| w5 | 5 | -0.165649 | -14.109 |
| w6 | 0 | -0.261858 | 0.0 |
| w7 | 0 | -0.056279 | 0.0 |
| w8 | 3 | -0.053266 | 3.179 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | 0.003594 | 1.91 |
| w11 | 16 | -0.070356 | 165.902 |
| w12 | 3 | -0.151145 | -16.853 |
| w13 | 3 | -0.055455 | -52.428 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | -0.00072 | -22.312 |
| w16 | 2 | -0.135113 | -5.707 |
| w17 | 9 | 0.089081 | 78.736 |
| w18 | 4 | -0.092219 | -70.318 |
| w19 | 7 | -0.065184 | -19.924 |
| w20 | 2 | 0.01443 | -8.169 |
| w21 | 5 | -0.04643 | 5.507 |
| w22 | 10 | -0.04073 | -45.123 |
| w23 | 5 | -0.078609 | -6.937 |
| w24 | 4 | -0.007013 | -22.649 |

- XMRUSD: 21 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.079362 | -9.916 |
| w2 | 1 | -0.131084 | -6.878 |
| w3 | 0 | -0.076934 | 0.0 |
| w4 | 7 | -0.13167 | -13.633 |
| w5 | 6 | -0.062366 | -5.078 |
| w6 | 9 | -0.083448 | -1.708 |
| w8 | 0 | -0.194372 | 0.0 |
| w9 | 0 | -0.123894 | 0.0 |
| w10 | 16 | 0.063489 | 79.886 |
| w11 | 6 | -0.043932 | 281.553 |
| w12 | 1 | -0.162417 | -5.832 |
| w15 | 6 | -0.112881 | -21.27 |
| w16 | 4 | -0.170572 | -22.273 |
| w17 | 8 | 0.005541 | 111.431 |
| w18 | 2 | -0.198222 | -57.316 |
| w19 | 3 | -0.219546 | -32.259 |
| w20 | 9 | -0.074751 | 9.364 |
| w21 | 6 | -0.121257 | -30.767 |
| w22 | 8 | -0.003467 | 70.683 |
| w23 | 4 | 0.031998 | -1.471 |
| w24 | 6 | -0.069989 | 7.728 |

- w7 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 483 prefetch bars (<date> to <date>) -- required_bars=400. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 364 prefetch bars (<date> to <date>) -- required_bars=400. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 606 prefetch bars (<date> to <date>) -- required_bars=400. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 20 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | -0.110556 | -4.678 |
| w4 | 6 | -0.09877 | 0.431 |
| w5 | 13 | 0.015521 | -10.411 |
| w6 | 6 | -0.07223 | -3.178 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | -0.029675 | -0.641 |
| w11 | 6 | 0.04927 | 183.263 |
| w12 | 7 | -0.217979 | -26.038 |
| w15 | 4 | -0.107454 | -17.818 |
| w16 | 1 | -0.091419 | -4.871 |
| w17 | 16 | 0.083795 | -49.997 |
| w18 | 12 | -0.164192 | -87.883 |
| w19 | 4 | -0.120679 | -15.884 |
| w20 | 7 | -0.129789 | -7.802 |
| w21 | 10 | -0.038592 | 66.69 |
| w22 | 16 | -0.079741 | -57.655 |
| w23 | 8 | -0.119541 | -13.063 |
| w24 | 3 | -0.033341 | -25.289 |

- w7 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 347 prefetch bars (<date> to <date>) -- required_bars=400. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w8 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 592 prefetch bars (<date> to <date>) -- required_bars=400. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 228 prefetch bars (<date> to <date>) -- required_bars=400. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 470 prefetch bars (<date> to <date>) -- required_bars=400. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.147144 | -27.629 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.254565 | -2.447 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 12 | -0.001319 | 52.022 |
| w11 | 19 | -0.073719 | 251.454 |
| w12 | 6 | -0.082418 | -21.63 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.108357 | -13.515 |
| w16 | 5 | -0.182683 | -26.672 |
| w17 | 10 | -0.200073 | -72.803 |
| w18 | 9 | -0.14737 | -89.966 |
| w19 | 1 | -0.163389 | -7.667 |
| w20 | 7 | -0.123288 | -22.752 |
| w21 | 26 | -0.038808 | 27.06 |
| w22 | 5 | -0.092179 | -53.443 |
| w23 | 3 | -0.191839 | -5.829 |
| w24 | 28 | -0.101004 | 1064.741 |

- w7 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 548 prefetch bars (<date> to <date>) -- required_bars=400. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 429 prefetch bars (<date> to <date>) -- required_bars=400. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

