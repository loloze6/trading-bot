# Backtest of 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades_1d

- Plan: `../../../../03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.127146 | 11.586 |
| w2 | 9 | -0.059767 | -48.146 |
| w3 | 11 | 0.089104 | -1.028 |
| w4 | 6 | -0.024278 | 3.465 |
| w5 | 4 | 0.06477 | -1.333 |
| w6 | 2 | -0.049458 | 1.182 |
| w7 | 6 | 0.067603 | -1.376 |
| w8 | 6 | -0.031554 | 1.771 |
| w9 | 9 | 0.075268 | -4.69 |
| w10 | 6 | -0.052202 | 0.063 |
| w11 | 9 | 0.001559 | 5.342 |
| w12 | 18 | 0.056444 | 2.945 |
| w13 | 5 | 0.054719 | 0.238 |
| w14 | 15 | 0.116837 | -35.978 |
| w15 | 6 | 0.045515 | 3.797 |
| w16 | 7 | 0.012748 | -14.197 |
| w17 | 2 | -0.095581 | 2.01 |
| w18 | 9 | -0.057214 | -25.714 |
| w19 | 18 | -0.058633 | 0.084 |
| w20 | 21 | 0.189837 | 49.209 |
| w21 | 7 | 0.099161 | 22.13 |
| w22 | 26 | 0.100104 | 15.189 |
| w23 | 11 | -0.041919 | -2.161 |
| w24 | 21 | -0.001973 | -27.634 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.007526 | -17.622 |
| w2 | 5 | -0.067683 | -45.838 |
| w3 | 8 | 0.092566 | 2.487 |
| w4 | 6 | 0.093851 | 10.955 |
| w5 | 10 | 0.07337 | 0.927 |
| w6 | 5 | -0.035541 | 5.824 |
| w7 | 4 | 0.043156 | -36.102 |
| w8 | 4 | 0.036994 | 4.54 |
| w9 | 8 | 0.042929 | -5.061 |
| w10 | 4 | 0.003872 | 2.28 |
| w11 | 5 | -0.043845 | 0.151 |
| w12 | 19 | 0.127116 | 14.391 |
| w13 | 6 | -0.04213 | -4.431 |
| w14 | 5 | 0.047876 | -35.275 |
| w15 | 6 | 0.022761 | 7.435 |
| w16 | 5 | 0.014791 | 10.026 |
| w17 | 9 | -0.003219 | 4.176 |
| w18 | 2 | -0.031719 | -0.772 |
| w19 | 15 | -0.035351 | 3.052 |
| w20 | 16 | -0.042571 | -29.356 |
| w21 | 8 | 0.134381 | 54.683 |
| w22 | 14 | 0.080705 | -34.898 |
| w23 | 6 | -0.089531 | -0.064 |
| w24 | 17 | 0.061179 | -6.152 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.097664 | -8.254 |
| w2 | 6 | -0.020691 | -27.943 |
| w3 | 9 | 0.057998 | 14.623 |
| w4 | 10 | 0.128508 | 9.925 |
| w5 | 10 | 0.027989 | 2.225 |
| w6 | 10 | 0.150089 | 20.164 |
| w7 | 3 | 0.038454 | -39.95 |
| w8 | 7 | 0.130607 | 15.674 |
| w9 | 6 | 0.034905 | -15.443 |
| w10 | 12 | 0.078988 | 14.862 |
| w11 | 6 | 0.09864 | 6.867 |
| w12 | 8 | 0.003708 | -4.299 |
| w13 | 9 | 0.091839 | 14.849 |
| w14 | 12 | 0.047733 | -36.486 |
| w15 | 7 | -0.043965 | 0.09 |
| w16 | 4 | -0.018129 | 0.284 |
| w17 | 4 | -0.083599 | -0.204 |
| w18 | 8 | -0.01451 | -8.83 |
| w19 | 12 | 0.001328 | 4.739 |
| w20 | 16 | 0.184401 | 1.417 |
| w21 | 8 | 0.132474 | 28.043 |
| w22 | 16 | 0.053722 | 2.213 |
| w23 | 11 | 0.090438 | 17.667 |
| w24 | 13 | 0.158245 | 4.207 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.060469 | 7.992 |
| w2 | 9 | 0.193988 | 19.652 |
| w3 | 7 | 0.081347 | 3.089 |
| w4 | 3 | 0.046918 | 4.443 |
| w5 | 7 | 0.007539 | -4.126 |
| w6 | 7 | 0.006882 | 1.19 |
| w7 | 4 | 0.03131 | -19.243 |
| w8 | 4 | 0.010359 | 3.411 |
| w9 | 3 | 0.036524 | -10.714 |
| w10 | 7 | 0.116457 | 9.008 |
| w11 | 6 | -0.032997 | 3.33 |
| w12 | 10 | 0.129921 | 7.114 |
| w14 | 6 | 0.053375 | -31.518 |
| w15 | 12 | 0.105522 | 11.054 |
| w16 | 6 | 0.061158 | 14.376 |
| w17 | 11 | 0.189515 | 12.082 |
| w18 | 6 | 0.101866 | 22.89 |
| w19 | 23 | 0.207671 | 18.245 |
| w20 | 13 | 0.109563 | 21.679 |
| w21 | 14 | 0.067434 | 16.297 |
| w22 | 19 | 0.147437 | 21.451 |
| w23 | 8 | -0.053352 | -26.604 |
| w24 | 6 | 0.023018 | 7.086 |

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
| w1 | 10 | 0.090053 | 2.313 |
| w2 | 5 | -0.063612 | -37.086 |
| w3 | 7 | -0.00373 | 4.072 |
| w4 | 6 | 0.146609 | 29.945 |
| w5 | 7 | 0.010698 | 15.002 |
| w6 | 12 | 0.09732 | 18.061 |
| w8 | 10 | 0.18122 | 13.963 |
| w9 | 7 | -0.03996 | -13.841 |
| w10 | 6 | 0.023859 | 10.731 |
| w11 | 7 | -0.065879 | 8.84 |
| w12 | 10 | 0.076908 | -2.57 |
| w14 | 7 | 0.006835 | 10.406 |
| w15 | 6 | 0.062429 | 11.382 |
| w16 | 5 | 0.043737 | 13.387 |
| w17 | 11 | -0.104928 | -4.188 |
| w18 | 14 | -0.008665 | 2.253 |
| w19 | 11 | -0.020649 | -8.135 |
| w20 | 12 | 0.018593 | 4.176 |
| w21 | 8 | -0.112647 | 7.534 |
| w22 | 21 | 0.174883 | 25.732 |
| w23 | 11 | 0.002497 | 5.161 |
| w24 | 16 | 0.103546 | -15.491 |

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
| w1 | 7 | -0.016151 | -0.346 |
| w2 | 6 | 0.043161 | -14.541 |
| w3 | 4 | 0.059747 | -19.702 |
| w4 | 9 | 0.133183 | 16.803 |
| w5 | 8 | 0.047434 | -10.481 |
| w6 | 6 | 0.096164 | 10.411 |
| w7 | 6 | 0.062279 | -4.945 |
| w8 | 9 | 0.11018 | 14.692 |
| w9 | 9 | 0.076335 | -14.341 |
| w10 | 4 | 0.157605 | 10.105 |
| w11 | 4 | 0.018732 | 8.87 |
| w12 | 3 | -0.007316 | 0.993 |
| w14 | 6 | 0.123114 | -29.653 |
| w15 | 3 | -0.043173 | -0.183 |
| w16 | 6 | -0.062864 | 2.86 |
| w17 | 9 | 0.072579 | 5.119 |
| w18 | 8 | -0.000462 | -6.321 |
| w19 | 6 | -0.010491 | -7.256 |
| w20 | 6 | -0.00684 | 5.125 |
| w21 | 5 | -0.011293 | 10.949 |
| w22 | 16 | 0.205321 | 22.065 |
| w23 | 7 | 0.140565 | 29.706 |
| w24 | 5 | -0.024824 | 11.442 |

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 429 prefetch bars (<date> to <date>) -- required_bars=455. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

