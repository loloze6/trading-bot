# Backtest of 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high_1d

- Plan: `../../../../03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.159331 | -3.706 |
| w2 | 2 | -0.189616 | 8.701 |
| w3 | 2 | -0.054383 | 4.323 |
| w4 | 1 | -0.15291 | 0.49 |
| w5 | 2 | -0.105476 | -2.183 |
| w6 | 3 | -0.035596 | 22.365 |
| w7 | 2 | -0.00083 | 4.76 |
| w8 | 0 | 0.045134 | 0.0 |
| w9 | 2 | -0.092249 | -2.993 |
| w10 | 2 | -0.070993 | 4.088 |
| w11 | 14 | -0.051933 | 5.777 |
| w12 | 10 | -0.094193 | -6.744 |
| w13 | 3 | -0.071683 | 1.542 |
| w14 | 1 | -0.07411 | 8.867 |
| w15 | 3 | -0.111061 | 10.412 |
| w16 | 2 | -0.144587 | -9.908 |
| w17 | 5 | 0.06589 | 35.171 |
| w18 | 4 | -0.122969 | -0.545 |
| w19 | 24 | 0.004686 | 8.14 |
| w20 | 16 | -0.144914 | -8.0 |
| w21 | 12 | -0.002767 | 3.44 |
| w22 | 13 | -0.134297 | -10.901 |
| w23 | 11 | -0.070432 | -1.421 |
| w24 | 10 | -0.007999 | 2.574 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.152379 | -1.679 |
| w2 | 2 | -0.164144 | 9.889 |
| w3 | 2 | -0.05906 | 2.951 |
| w4 | 1 | -0.178352 | -1.097 |
| w5 | 2 | -0.152904 | -3.789 |
| w6 | 2 | -0.078165 | 11.555 |
| w7 | 3 | -0.157946 | 7.802 |
| w8 | 0 | 0.035878 | 0.0 |
| w9 | 2 | -0.029781 | -4.391 |
| w10 | 2 | 0.077583 | 17.585 |
| w11 | 14 | -0.082233 | 17.333 |
| w12 | 12 | -0.162395 | -5.123 |
| w13 | 5 | 0.060451 | 7.652 |
| w14 | 2 | 0.046099 | 10.571 |
| w15 | 1 | -0.264971 | -3.416 |
| w16 | 3 | -0.165137 | -7.966 |
| w17 | 3 | -0.072089 | 12.428 |
| w18 | 10 | 0.018935 | 2.895 |
| w19 | 12 | 0.05529 | 7.835 |
| w20 | 9 | -0.07149 | -3.973 |
| w21 | 9 | -0.081599 | -10.66 |
| w22 | 4 | -0.075481 | 6.405 |
| w23 | 9 | -0.097749 | -4.389 |
| w24 | 3 | -0.082432 | -2.39 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.093401 | 3.526 |
| w2 | 0 | -0.187155 | 0.0 |
| w3 | 0 | -0.052328 | 0.0 |
| w4 | 2 | -0.249853 | -1.178 |
| w5 | 2 | -0.003353 | -2.731 |
| w6 | 0 | -0.310994 | 0.0 |
| w7 | 1 | -0.056688 | 10.145 |
| w8 | 0 | -0.061593 | 0.0 |
| w9 | 0 | -0.05156 | 0.0 |
| w10 | 1 | 0.03593 | -0.201 |
| w11 | 8 | -0.044706 | 5.559 |
| w12 | 5 | -0.174401 | -5.168 |
| w13 | 6 | -0.154919 | 0.668 |
| w14 | 1 | -0.002957 | 8.382 |
| w15 | 3 | -0.014015 | -3.106 |
| w16 | 1 | -0.112627 | -4.568 |
| w17 | 3 | 0.00987 | 12.476 |
| w18 | 3 | -0.064073 | 0.386 |
| w19 | 6 | -0.142772 | -7.68 |
| w20 | 1 | -0.18222 | -2.094 |
| w21 | 2 | -0.037064 | 0.777 |
| w22 | 8 | -0.103683 | -5.841 |
| w23 | 3 | -0.132729 | -1.855 |
| w24 | 5 | -0.121875 | -2.943 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.048157 | -4.774 |
| w2 | 0 | -0.136014 | 0.0 |
| w3 | 0 | -0.347887 | 0.0 |
| w4 | 0 | -0.162104 | 0.0 |
| w5 | 2 | -0.085262 | -3.522 |
| w6 | 2 | -0.191912 | 3.869 |
| w7 | 1 | -0.161543 | 2.341 |
| w8 | 0 | -0.003979 | 0.0 |
| w9 | 2 | -0.084129 | -3.374 |
| w10 | 2 | -0.008157 | 5.766 |
| w11 | 11 | 0.005078 | 10.485 |
| w12 | 1 | -0.160244 | 4.685 |
| w14 | 1 | -0.100494 | 2.977 |
| w15 | 1 | -0.197311 | -2.191 |
| w16 | 4 | -0.143075 | -8.035 |
| w17 | 3 | -0.187177 | 9.626 |
| w18 | 6 | -0.061805 | 1.243 |
| w19 | 10 | -0.244679 | -17.72 |
| w20 | 10 | -0.217622 | -6.323 |
| w21 | 11 | -0.198676 | -7.272 |
| w22 | 15 | -0.135008 | -1.165 |
| w23 | 4 | 0.175619 | 19.97 |
| w24 | 17 | -0.130123 | -14.954 |

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 364 prefetch bars (<date> to <date>) -- required_bars=455. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.179418 | 2.282 |
| w2 | 1 | -0.257157 | 2.212 |
| w3 | 0 | -0.206517 | 0.0 |
| w4 | 1 | -0.133776 | -1.26 |
| w5 | 5 | 0.014492 | 19.499 |
| w6 | 1 | -0.160141 | -1.601 |
| w8 | 0 | -0.024499 | 0.0 |
| w9 | 0 | -0.103141 | 0.0 |
| w10 | 2 | 0.064611 | 2.592 |
| w11 | 8 | -0.02628 | 6.962 |
| w12 | 3 | -0.212499 | -2.833 |
| w14 | 0 | -0.135258 | 0.0 |
| w15 | 1 | -0.106669 | -3.629 |
| w16 | 3 | -0.135277 | -6.456 |
| w17 | 8 | 0.133966 | 13.912 |
| w18 | 8 | -0.147587 | -5.784 |
| w19 | 3 | -0.193864 | -1.973 |
| w20 | 4 | -0.093468 | -7.062 |
| w21 | 7 | 0.290579 | 35.399 |
| w22 | 10 | -0.103414 | -5.254 |
| w23 | 10 | -0.106704 | -7.706 |
| w24 | 4 | -0.077851 | 3.293 |

- w7 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 347 prefetch bars (<date> to <date>) -- required_bars=455. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 228 prefetch bars (<date> to <date>) -- required_bars=455. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.085861 | -1.507 |
| w2 | 1 | -0.207308 | -0.101 |
| w3 | 0 | -0.090328 | 0.0 |
| w4 | 0 | -0.119334 | 0.0 |
| w5 | 0 | -0.163905 | 0.0 |
| w6 | 1 | -0.151929 | -1.233 |
| w7 | 1 | -0.166506 | 3.195 |
| w8 | 0 | 0.040067 | 0.0 |
| w9 | 0 | -0.150261 | 0.0 |
| w10 | 2 | 0.010711 | 4.958 |
| w11 | 10 | -0.027726 | 8.116 |
| w12 | 7 | -0.123654 | -9.022 |
| w14 | 1 | -0.105777 | 5.097 |
| w15 | 1 | -0.133218 | -4.621 |
| w16 | 2 | -0.126828 | -5.163 |
| w17 | 4 | -0.374371 | -6.023 |
| w18 | 6 | -0.107129 | -3.086 |
| w19 | 1 | -0.102608 | -2.354 |
| w20 | 5 | -0.036256 | -1.347 |
| w21 | 9 | -0.054906 | 5.112 |
| w22 | 4 | -0.174022 | -2.826 |
| w23 | 4 | -0.210861 | -5.314 |
| w24 | 15 | 0.111093 | 26.784 |

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 429 prefetch bars (<date> to <date>) -- required_bars=455. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

