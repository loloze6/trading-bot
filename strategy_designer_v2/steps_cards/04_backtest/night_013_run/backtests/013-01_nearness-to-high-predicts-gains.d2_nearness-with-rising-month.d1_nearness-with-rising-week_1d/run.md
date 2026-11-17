# Backtest of 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week_1d

- Plan: `../../../../03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | 0.004853 | -0.312 |
| w2 | 15 | -0.115731 | -1.737 |
| w3 | 18 | -0.008269 | -1.043 |
| w4 | 32 | 0.02331 | 19.377 |
| w5 | 12 | 0.04436 | 2.271 |
| w6 | 39 | -0.003859 | 24.02 |
| w7 | 21 | 0.178611 | 13.624 |
| w8 | 37 | -9.5e-05 | 5.089 |
| w9 | 14 | 0.035123 | 1.059 |
| w10 | 41 | -0.04098 | 4.873 |
| w11 | 51 | -0.068074 | 5.711 |
| w12 | 31 | -0.019682 | -1.931 |
| w13 | 17 | -0.067076 | -5.593 |
| w14 | 15 | 0.063527 | 13.037 |
| w15 | 40 | 0.032323 | 14.827 |
| w16 | 34 | -0.003301 | 2.597 |
| w17 | 31 | 0.0654 | 63.72 |
| w18 | 21 | -0.002229 | -1.822 |
| w19 | 37 | 0.03088 | 11.48 |
| w20 | 26 | 0.127794 | 12.009 |
| w21 | 49 | 0.003287 | 13.508 |
| w22 | 23 | -0.036421 | -4.195 |
| w23 | 45 | -0.026179 | 0.497 |
| w24 | 15 | 0.025833 | 1.189 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | -0.083835 | -6.952 |
| w2 | 14 | -0.029512 | -0.814 |
| w3 | 16 | 0.161978 | 7.581 |
| w4 | 44 | -0.039192 | 5.032 |
| w5 | 23 | -0.146571 | -13.595 |
| w6 | 39 | -0.039735 | 10.584 |
| w7 | 8 | 0.106883 | 6.899 |
| w8 | 34 | -0.133595 | -12.131 |
| w9 | 16 | -0.065536 | -4.646 |
| w10 | 42 | 0.045289 | 26.993 |
| w11 | 55 | -0.022022 | 21.562 |
| w12 | 46 | -0.091689 | -11.744 |
| w13 | 24 | 0.093072 | 12.389 |
| w14 | 12 | -0.023579 | 1.219 |
| w15 | 19 | 0.081023 | 8.113 |
| w16 | 29 | 0.008683 | 12.288 |
| w17 | 44 | -0.047266 | 5.792 |
| w18 | 31 | 0.08503 | 20.633 |
| w19 | 32 | 0.077158 | 20.405 |
| w20 | 12 | -0.034401 | -3.791 |
| w21 | 34 | 0.089813 | 13.561 |
| w22 | 0 | 0.047881 | 0.0 |
| w23 | 40 | -0.041456 | 9.142 |
| w24 | 12 | -0.021243 | -4.019 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.019095 | -1.076 |
| w2 | 18 | -0.032164 | 0.193 |
| w3 | 27 | 0.057743 | 5.77 |
| w4 | 36 | -0.131384 | -8.673 |
| w5 | 20 | -0.135921 | -12.091 |
| w6 | 41 | -0.110217 | -12.607 |
| w7 | 9 | -0.007958 | 1.157 |
| w8 | 38 | -0.093583 | -3.636 |
| w9 | 15 | 0.024222 | 0.067 |
| w10 | 33 | 0.060223 | 7.816 |
| w11 | 50 | -0.077688 | -1.047 |
| w12 | 34 | -0.081281 | -11.38 |
| w13 | 21 | -0.024796 | -0.488 |
| w14 | 14 | -0.016528 | 0.175 |
| w15 | 35 | 0.008002 | 1.065 |
| w16 | 32 | 0.022542 | 5.145 |
| w17 | 37 | -0.038682 | 5.171 |
| w18 | 25 | 0.063457 | 6.487 |
| w19 | 39 | -0.000206 | 5.044 |
| w20 | 15 | 0.200416 | 7.741 |
| w21 | 47 | 0.00492 | 7.714 |
| w22 | 25 | -0.112306 | -7.776 |
| w23 | 40 | 0.039259 | 7.575 |
| w24 | 12 | -0.162227 | -10.783 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 42 | -0.107845 | -14.175 |
| w2 | 22 | 0.155792 | 9.483 |
| w3 | 13 | -0.144351 | -9.405 |
| w4 | 32 | -0.022339 | -5.127 |
| w5 | 11 | 0.055902 | 4.165 |
| w6 | 44 | -0.09151 | -4.424 |
| w7 | 14 | -0.110429 | -3.045 |
| w8 | 39 | -0.081622 | -5.427 |
| w9 | 9 | 0.070407 | 1.33 |
| w10 | 45 | -0.024459 | 6.514 |
| w11 | 50 | -0.020352 | 13.163 |
| w12 | 18 | -0.082183 | -4.623 |
| w14 | 22 | -0.010977 | 2.943 |
| w15 | 37 | -0.045743 | -4.142 |
| w16 | 29 | 0.006315 | 6.909 |
| w17 | 43 | -0.084806 | 1.261 |
| w18 | 34 | 0.139994 | 9.895 |
| w19 | 17 | -0.134251 | -6.107 |
| w20 | 38 | -0.058082 | -3.436 |
| w21 | 45 | -0.08618 | -9.294 |
| w22 | 35 | -0.006189 | 8.141 |
| w23 | 27 | 0.102235 | 19.431 |
| w24 | 64 | -0.202524 | -23.644 |

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
| w1 | 30 | -0.149856 | -5.465 |
| w2 | 19 | -0.070551 | -2.88 |
| w3 | 20 | 0.061294 | 8.604 |
| w4 | 31 | -0.058881 | -4.691 |
| w5 | 23 | -0.078704 | -7.61 |
| w6 | 29 | 0.08335 | 12.296 |
| w8 | 34 | -0.113588 | -9.447 |
| w9 | 21 | -0.037978 | -4.019 |
| w10 | 31 | 0.163648 | 27.132 |
| w11 | 39 | -0.001146 | 21.308 |
| w12 | 21 | -0.065003 | -3.451 |
| w14 | 22 | 0.071737 | 4.873 |
| w15 | 24 | -0.031011 | -4.393 |
| w16 | 28 | 0.038173 | 7.444 |
| w17 | 28 | 0.218551 | 89.302 |
| w18 | 22 | -0.012804 | 0.302 |
| w19 | 27 | -0.120334 | -11.644 |
| w20 | 20 | -0.046834 | -1.806 |
| w21 | 24 | 0.360933 | 143.535 |
| w22 | 16 | 0.073237 | 2.89 |
| w23 | 37 | 0.04565 | 9.777 |
| w24 | 7 | -0.023486 | -1.077 |

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
| w1 | 22 | -0.046411 | -3.513 |
| w2 | 17 | 0.026439 | 0.652 |
| w3 | 8 | -0.020803 | -0.046 |
| w4 | 31 | -0.163671 | -13.703 |
| w5 | 15 | -0.104362 | -3.642 |
| w6 | 38 | -0.094246 | -10.748 |
| w7 | 20 | -0.001516 | -2.513 |
| w8 | 29 | 0.108116 | 11.359 |
| w9 | 7 | 0.01227 | 0.036 |
| w10 | 53 | -0.046177 | 1.696 |
| w11 | 47 | -0.012844 | 16.919 |
| w12 | 32 | -0.111388 | -16.879 |
| w14 | 6 | 0.02699 | 1.235 |
| w15 | 34 | 0.004624 | -2.729 |
| w16 | 30 | 0.153283 | 31.786 |
| w17 | 31 | -0.131106 | -13.028 |
| w18 | 25 | -0.065077 | -7.969 |
| w19 | 25 | 0.101722 | 9.237 |
| w20 | 36 | 0.113435 | 19.509 |
| w21 | 34 | -0.098824 | -1.331 |
| w22 | 17 | 0.049797 | 1.917 |
| w23 | 32 | 0.089325 | 7.196 |
| w24 | 33 | 0.21641 | 95.992 |

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 429 prefetch bars (<date> to <date>) -- required_bars=455. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

