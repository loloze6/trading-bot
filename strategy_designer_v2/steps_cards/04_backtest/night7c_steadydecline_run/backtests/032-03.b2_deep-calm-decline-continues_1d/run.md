# Backtest of 032-03.b2_deep-calm-decline-continues_1d

- Plan: `../../../../03_test_plan/night7c_steadydecline_run/plans/032-03.b2_deep-calm-decline-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | -0.021226 | 4.007 |
| w2 | 14 | 0.156435 | 52.027 |
| w3 | 9 | -0.106616 | -5.914 |
| w4 | 6 | 0.099276 | -12.618 |
| w5 | 31 | -0.082465 | -20.487 |
| w6 | 11 | 0.014134 | -11.494 |
| w7 | 29 | -0.150913 | -13.861 |
| w8 | 9 | 0.022539 | -11.194 |
| w9 | 32 | -0.061482 | 0.802 |
| w10 | 11 | -0.042285 | -14.486 |
| w11 | 4 | -0.103458 | -4.895 |
| w12 | 13 | -0.013491 | 0.152 |
| w13 | 7 | 0.125977 | 4.431 |
| w14 | 25 | 0.156679 | 81.448 |
| w15 | 4 | 0.000811 | 0.285 |
| w16 | 12 | 0.129247 | 12.207 |
| w17 | 12 | 0.083722 | -4.367 |
| w18 | 11 | 0.243534 | 28.732 |
| w19 | 7 | -0.030387 | -16.598 |
| w20 | 33 | -0.077881 | -12.286 |
| w21 | 9 | -0.004854 | -7.481 |
| w22 | 22 | -0.017507 | 2.863 |
| w23 | 11 | -0.035461 | 1.491 |
| w24 | 24 | -0.121385 | -22.114 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | 0.032035 | 18.004 |
| w2 | 20 | 0.144884 | 72.914 |
| w3 | 8 | -0.031825 | -3.659 |
| w4 | 8 | -0.013785 | -12.16 |
| w5 | 31 | -0.057759 | 3.894 |
| w6 | 16 | 0.026326 | -12.829 |
| w7 | 27 | -0.042063 | 18.588 |
| w8 | 0 | -0.041791 | 0.0 |
| w9 | 29 | -0.009168 | 7.22 |
| w10 | 4 | -0.071246 | -9.033 |
| w11 | 0 | 0.015633 | 0.0 |
| w12 | 17 | -0.087004 | -4.311 |
| w13 | 15 | 0.114341 | 12.561 |
| w14 | 6 | 0.047402 | 47.343 |
| w15 | 18 | 0.015011 | -11.993 |
| w16 | 6 | -0.055067 | -16.921 |
| w17 | 2 | -0.048256 | -5.735 |
| w18 | 7 | 0.033726 | -4.53 |
| w19 | 8 | 0.008967 | -11.187 |
| w20 | 34 | -0.072003 | -6.833 |
| w21 | 18 | -0.081048 | -7.814 |
| w22 | 13 | -0.08524 | 10.89 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | 0.05184 | 0.009 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 32 | -0.068571 | 13.67 |
| w2 | 26 | -0.063762 | 40.316 |
| w3 | 22 | -0.066777 | -10.312 |
| w4 | 15 | -0.057721 | -14.71 |
| w5 | 20 | -0.018094 | 0.167 |
| w6 | 14 | -0.030795 | -12.247 |
| w7 | 36 | -0.145753 | 7.321 |
| w8 | 3 | 0.001693 | -14.791 |
| w9 | 38 | -0.107552 | 0.439 |
| w10 | 18 | -0.094718 | -32.661 |
| w11 | 0 | None | 0.0 |
| w12 | 18 | -0.004686 | -0.977 |
| w13 | 17 | 0.01226 | -1.466 |
| w14 | 27 | 0.04122 | 41.939 |
| w15 | 0 | None | 0.0 |
| w16 | 5 | -0.067603 | -11.715 |
| w17 | 5 | -0.014597 | -11.502 |
| w18 | 9 | -0.014988 | -2.198 |
| w19 | 5 | -0.041189 | -2.658 |
| w20 | 34 | -0.162474 | -5.931 |
| w21 | 7 | -0.042399 | -2.528 |
| w22 | 11 | -0.16541 | -7.951 |
| w23 | 13 | 0.006226 | -3.197 |
| w24 | 15 | -0.069594 | 0.865 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | -0.063596 | -10.644 |
| w2 | 17 | 0.038325 | 0.604 |
| w3 | 30 | -0.164792 | -17.499 |
| w4 | 22 | -0.080484 | -9.181 |
| w5 | 36 | -0.049667 | 2.273 |
| w6 | 15 | -0.047778 | -6.931 |
| w7 | 30 | -0.130048 | -2.468 |
| w8 | 8 | 0.019287 | -9.463 |
| w9 | 39 | -0.097579 | 11.003 |
| w10 | 6 | -0.042334 | -4.442 |
| w11 | 0 | None | 0.0 |
| w12 | 18 | -0.136679 | -6.846 |
| w14 | 13 | 0.103181 | 28.689 |
| w15 | 12 | -0.048022 | -2.575 |
| w16 | 5 | -0.141231 | -13.583 |
| w17 | 9 | -0.156705 | -11.72 |
| w18 | 2 | 0.01451 | -5.424 |
| w19 | 1 | 0.143777 | 4.761 |
| w20 | 3 | 0.054053 | 1.546 |
| w21 | 26 | -0.044738 | -24.611 |
| w22 | 22 | -0.144518 | -20.196 |
| w23 | 13 | 0.124549 | 30.323 |
| w24 | 0 | None | 0.0 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=393. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | 0.057641 | 22.766 |
| w2 | 26 | 0.030774 | 44.183 |
| w3 | 0 | -0.04249 | 0.0 |
| w4 | 0 | -0.159672 | 0.0 |
| w5 | 5 | -0.046634 | -60.19 |
| w6 | 9 | -0.158433 | -7.412 |
| w8 | 11 | -0.046708 | -6.033 |
| w9 | 17 | 0.044184 | 13.306 |
| w10 | 12 | -0.090452 | -15.176 |
| w11 | 4 | 0.011932 | -10.645 |
| w12 | 22 | -0.022149 | 7.895 |
| w14 | 23 | -0.091895 | -36.806 |
| w15 | 8 | -0.039093 | -48.164 |
| w16 | 5 | -0.116811 | -15.472 |
| w17 | 14 | -0.01163 | -7.551 |
| w18 | 11 | 0.023552 | -1.956 |
| w19 | 3 | -0.067511 | -5.63 |
| w20 | 23 | 0.026843 | -21.863 |
| w21 | 20 | 0.134046 | -13.118 |
| w22 | 9 | -0.081843 | -5.094 |
| w23 | 15 | -0.029426 | -20.459 |
| w24 | 47 | -0.069014 | 13.054 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=393. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=393. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.18033 | -26.019 |
| w2 | 18 | -0.055245 | -2.792 |
| w3 | 43 | -0.179828 | 7.003 |
| w4 | 20 | 0.052369 | -4.827 |
| w5 | 35 | 0.049673 | 19.581 |
| w6 | 13 | -0.074306 | -12.278 |
| w7 | 24 | -0.119834 | -5.974 |
| w8 | 10 | -0.058419 | -3.778 |
| w9 | 27 | -0.205435 | -15.652 |
| w10 | 2 | -0.020332 | -8.342 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | -0.072112 | -6.495 |
| w13 | 15 | 0.041195 | 4.367 |
| w14 | 28 | 0.108064 | 20.875 |
| w15 | 7 | 0.064256 | 3.121 |
| w16 | 0 | None | 0.0 |
| w17 | 6 | 0.036657 | -2.979 |
| w18 | 13 | -0.022824 | -7.349 |
| w19 | 2 | -0.061547 | -7.107 |
| w20 | 16 | -0.001205 | -27.057 |
| w21 | 7 | 0.038817 | -7.94 |
| w22 | 18 | -0.058584 | -4.992 |
| w23 | 28 | -0.123918 | -31.347 |
| w24 | 0 | None | 0.0 |

