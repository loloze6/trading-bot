# Backtest of 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month_1d

- Plan: `../../../../03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | 0.036659 | 4.427 |
| w2 | 12 | -0.106377 | -1.541 |
| w3 | 14 | 0.035491 | 3.661 |
| w4 | 18 | -0.108165 | -7.125 |
| w5 | 8 | 0.035072 | 1.994 |
| w6 | 18 | 0.002643 | 22.329 |
| w7 | 15 | 0.071859 | 4.078 |
| w8 | 21 | -0.025094 | -1.712 |
| w9 | 9 | -0.029579 | -0.887 |
| w10 | 19 | -0.05272 | 4.347 |
| w11 | 36 | -0.098167 | -1.388 |
| w12 | 19 | 0.02674 | 2.13 |
| w13 | 13 | -0.008449 | 0.238 |
| w14 | 15 | 0.083823 | 12.415 |
| w15 | 26 | -0.077549 | 2.872 |
| w16 | 24 | -0.038291 | -1.732 |
| w17 | 18 | 0.094088 | 48.945 |
| w18 | 12 | -0.045527 | -3.252 |
| w19 | 25 | 0.058617 | 14.637 |
| w20 | 27 | 0.03326 | 3.904 |
| w21 | 34 | 0.049904 | 19.363 |
| w22 | 19 | -0.044237 | -3.353 |
| w23 | 28 | -0.03514 | -2.691 |
| w24 | 12 | -0.018009 | -4.551 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.077164 | -6.359 |
| w2 | 11 | -0.091938 | -2.467 |
| w3 | 13 | 0.056945 | 1.085 |
| w4 | 19 | -0.068599 | -3.661 |
| w5 | 16 | -0.063109 | -5.186 |
| w6 | 21 | -0.004473 | 11.069 |
| w7 | 7 | 0.120283 | 8.58 |
| w8 | 25 | -0.255035 | -12.759 |
| w9 | 16 | -0.085408 | -3.509 |
| w10 | 14 | 0.037162 | 23.31 |
| w11 | 32 | -0.029371 | 19.265 |
| w12 | 25 | -0.016038 | -4.178 |
| w13 | 17 | 0.069824 | 6.175 |
| w14 | 10 | 0.009992 | 3.378 |
| w15 | 13 | 0.020911 | 5.737 |
| w16 | 14 | -0.000357 | 7.953 |
| w17 | 21 | 0.060664 | 21.31 |
| w18 | 21 | -0.002584 | 1.387 |
| w19 | 21 | 0.058359 | 12.208 |
| w20 | 13 | -0.14074 | -7.668 |
| w21 | 24 | 0.118892 | 13.79 |
| w22 | 1 | 0.047881 | 0.585 |
| w23 | 22 | -0.088409 | 2.36 |
| w24 | 6 | -0.053787 | -0.185 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | 0.027998 | 1.293 |
| w2 | 13 | -0.026989 | 1.587 |
| w3 | 20 | -0.005674 | 0.616 |
| w4 | 21 | -0.074297 | -5.315 |
| w5 | 19 | -0.145418 | -13.936 |
| w6 | 28 | -0.089021 | -10.582 |
| w7 | 5 | 0.009731 | 3.228 |
| w8 | 24 | -0.075691 | -1.733 |
| w9 | 11 | -0.010028 | 0.549 |
| w10 | 22 | 0.092773 | 7.899 |
| w11 | 37 | -0.140743 | -5.155 |
| w12 | 24 | -0.073783 | -7.607 |
| w13 | 16 | 0.059963 | 8.457 |
| w14 | 14 | 0.02157 | 2.929 |
| w15 | 16 | 0.037203 | 2.667 |
| w16 | 14 | -0.013707 | -0.483 |
| w17 | 27 | -0.001128 | 13.279 |
| w18 | 17 | -0.023622 | -4.962 |
| w19 | 32 | 0.038294 | 8.226 |
| w20 | 9 | 0.15575 | 6.583 |
| w21 | 30 | 0.034646 | 10.572 |
| w22 | 16 | -0.142336 | -5.539 |
| w23 | 27 | 0.037511 | 4.567 |
| w24 | 9 | -0.249074 | -8.472 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | 0.025607 | -1.011 |
| w2 | 16 | 0.208609 | 8.78 |
| w3 | 16 | -0.101683 | -4.286 |
| w4 | 19 | -0.031625 | -3.956 |
| w5 | 8 | 0.016705 | -1.597 |
| w6 | 33 | -0.137405 | -6.385 |
| w7 | 8 | -0.042933 | -0.981 |
| w8 | 26 | -0.057998 | -0.408 |
| w9 | 5 | -0.0257 | 0.145 |
| w10 | 22 | 0.040827 | 11.499 |
| w11 | 38 | -0.091602 | 0.916 |
| w12 | 15 | 0.071156 | 6.078 |
| w14 | 15 | 0.043379 | 4.431 |
| w15 | 20 | -0.066518 | -3.905 |
| w16 | 17 | 0.037011 | 8.28 |
| w17 | 24 | -0.033386 | 4.245 |
| w18 | 24 | 0.101082 | 7.021 |
| w19 | 11 | -0.238851 | -10.3 |
| w20 | 29 | -0.068917 | -4.116 |
| w21 | 23 | -0.052939 | -2.568 |
| w22 | 29 | 0.032982 | 5.49 |
| w23 | 14 | 0.144156 | 25.903 |
| w24 | 47 | -0.215312 | -23.267 |

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
| w1 | 25 | -0.08021 | 1.133 |
| w2 | 10 | -0.108742 | -2.587 |
| w3 | 15 | 0.030221 | 1.414 |
| w4 | 20 | -0.089923 | -4.075 |
| w5 | 11 | -0.122458 | -15.331 |
| w6 | 17 | 0.000338 | -0.638 |
| w8 | 24 | -0.103258 | -5.288 |
| w9 | 12 | 0.003726 | -1.54 |
| w10 | 13 | 0.146783 | 19.522 |
| w11 | 31 | -0.087524 | 2.107 |
| w12 | 20 | -0.019158 | -1.097 |
| w14 | 12 | -0.054738 | -3.565 |
| w15 | 10 | -0.024415 | -3.438 |
| w16 | 17 | 0.014781 | 3.583 |
| w17 | 19 | 0.183444 | 51.384 |
| w18 | 15 | -0.054256 | -6.907 |
| w19 | 16 | -0.110073 | -6.632 |
| w20 | 14 | -0.050616 | -2.948 |
| w21 | 20 | 0.332634 | 95.927 |
| w22 | 9 | 0.117458 | 3.774 |
| w23 | 29 | 0.010707 | 4.139 |
| w24 | 6 | 0.093644 | 3.028 |

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
| w1 | 19 | -0.035925 | -1.739 |
| w2 | 16 | -0.007538 | -1.329 |
| w3 | 5 | 0.000123 | -0.176 |
| w4 | 20 | -0.023005 | -2.243 |
| w5 | 11 | 0.039739 | 2.028 |
| w6 | 31 | -0.170567 | -15.446 |
| w7 | 16 | 0.017828 | 2.98 |
| w8 | 21 | 0.125556 | 7.434 |
| w9 | 8 | 0.031981 | 0.534 |
| w10 | 25 | -0.025573 | 1.233 |
| w11 | 37 | -0.195877 | 0.828 |
| w12 | 17 | -0.138604 | -15.021 |
| w14 | 7 | 0.044366 | 1.645 |
| w15 | 18 | 0.012142 | -0.113 |
| w16 | 16 | 0.097491 | 17.283 |
| w17 | 15 | -0.132813 | -8.958 |
| w18 | 16 | -0.083587 | -2.609 |
| w19 | 6 | 0.007055 | 1.03 |
| w20 | 13 | 0.052367 | 11.168 |
| w21 | 34 | -0.075141 | 1.717 |
| w22 | 14 | 0.088913 | 6.156 |
| w23 | 23 | 0.110028 | 6.745 |
| w24 | 25 | 0.225831 | 72.356 |

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 429 prefetch bars (<date> to <date>) -- required_bars=455. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

