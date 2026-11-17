# Backtest of 013-02_follow-through-stronger-near-high_1d

- Plan: `../../../../03_test_plan/night_013_run/plans/013-02_follow-through-stronger-near-high_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | -0.06243 | 0.0 |
| w2 | 0 | 0.001412 | 0.0 |
| w3 | 10 | -0.075652 | -2.728 |
| w4 | 44 | -0.104102 | 25.608 |
| w5 | 30 | 0.003045 | -1.122 |
| w6 | 32 | -0.087679 | 23.48 |
| w7 | 0 | -0.068897 | 0.0 |
| w8 | 30 | -0.002626 | 19.69 |
| w9 | 0 | -0.07259 | 0.0 |
| w10 | 18 | 0.052556 | 24.24 |
| w11 | 25 | 0.021449 | 27.511 |
| w12 | 6 | -0.074753 | -6.441 |
| w13 | 0 | 0.063974 | 0.0 |
| w14 | 5 | -0.258627 | -1.8 |
| w15 | 22 | 0.112311 | 90.919 |
| w16 | 0 | -0.003467 | 0.0 |
| w17 | 29 | 0.095669 | 122.897 |
| w18 | 0 | 0.072256 | 0.0 |
| w19 | 24 | 0.083819 | 37.944 |
| w20 | 4 | -0.123986 | -1.826 |
| w21 | 22 | -0.014256 | 21.883 |
| w22 | 8 | -0.114126 | -6.703 |
| w23 | 34 | -0.083674 | -9.568 |
| w24 | 8 | -0.038386 | -4.762 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | -0.036577 | 0.0 |
| w2 | 0 | 0.07366 | 0.0 |
| w3 | 9 | -0.104329 | -3.635 |
| w4 | 57 | -0.152633 | -6.411 |
| w5 | 61 | -0.098379 | -32.059 |
| w6 | 44 | -0.006827 | 14.893 |
| w7 | 0 | -0.009947 | 0.0 |
| w8 | 27 | -0.132792 | -10.17 |
| w9 | 52 | -0.089575 | -12.274 |
| w10 | 60 | -0.063868 | 48.522 |
| w11 | 42 | -0.038619 | 46.662 |
| w12 | 19 | -0.042275 | -6.575 |
| w13 | 6 | 0.170807 | 24.24 |
| w14 | 0 | -0.08474 | 0.0 |
| w15 | 40 | 0.052806 | 22.109 |
| w16 | 27 | 0.006653 | 26.23 |
| w17 | 32 | -0.054789 | -0.837 |
| w18 | 8 | 0.055725 | 12.963 |
| w19 | 18 | 0.064894 | 29.2 |
| w20 | 2 | -0.043228 | -1.669 |
| w21 | 8 | -0.152422 | -9.296 |
| w22 | 0 | -0.065088 | 0.0 |
| w23 | 17 | -0.068685 | 20.405 |
| w24 | 6 | -0.112732 | -2.976 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | -0.063471 | 0.0 |
| w2 | 30 | -0.061758 | -3.276 |
| w3 | 39 | -0.088631 | -15.489 |
| w4 | 53 | -0.095879 | -23.755 |
| w5 | 41 | -0.271818 | -70.711 |
| w6 | 0 | -0.180037 | 0.0 |
| w7 | 0 | -0.083462 | 0.0 |
| w8 | 53 | -0.156825 | 10.565 |
| w9 | 0 | -0.085309 | 0.0 |
| w10 | 14 | 0.004358 | 8.632 |
| w11 | 22 | 0.01847 | 13.612 |
| w12 | 0 | -0.096812 | 0.0 |
| w13 | 0 | -0.023902 | 0.0 |
| w14 | 0 | -0.252262 | 0.0 |
| w15 | 16 | 0.068047 | 10.744 |
| w16 | 0 | -0.006562 | 0.0 |
| w17 | 50 | 0.035865 | 42.45 |
| w18 | 7 | 0.037303 | 2.601 |
| w19 | 24 | -0.193426 | -18.314 |
| w20 | 7 | -0.129958 | -1.034 |
| w21 | 31 | 0.049357 | 23.935 |
| w22 | 11 | -0.224977 | -9.594 |
| w23 | 3 | -0.170021 | -2.989 |
| w24 | 0 | -0.192145 | 0.0 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | -0.05615 | 0.0 |
| w2 | 62 | -0.119603 | -31.787 |
| w3 | 47 | -0.153518 | -17.02 |
| w4 | 60 | -0.048982 | -15.591 |
| w5 | 58 | 0.062875 | 13.896 |
| w6 | 61 | -0.10538 | -12.37 |
| w7 | 9 | -0.067603 | -2.641 |
| w8 | 33 | -0.115578 | -7.234 |
| w9 | 50 | -0.038308 | 4.014 |
| w10 | 50 | -0.03255 | 20.634 |
| w11 | 22 | -0.024946 | 11.752 |
| w12 | 0 | -0.145877 | 0.0 |
| w14 | 9 | -0.031955 | 3.336 |
| w15 | 64 | -0.080124 | -27.022 |
| w16 | 36 | 0.002377 | 21.828 |
| w17 | 38 | -0.047111 | 4.397 |
| w18 | 7 | -0.005281 | -3.065 |
| w19 | 36 | -0.247496 | -65.536 |
| w20 | 32 | -0.02272 | 3.349 |
| w21 | 31 | -0.055983 | -11.336 |
| w22 | 35 | -0.068698 | 3.074 |
| w23 | 7 | 0.220256 | 60.677 |
| w24 | 15 | -0.144718 | -11.147 |

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 364 prefetch bars (<date> to <date>) -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.146431 | 1.156 |
| w2 | 19 | 0.02758 | 9.954 |
| w3 | 48 | -0.015709 | -2.957 |
| w4 | 55 | -0.130952 | -26.893 |
| w5 | 40 | -0.091782 | -56.279 |
| w6 | 3 | -0.189335 | -4.514 |
| w8 | 55 | -0.206606 | -23.327 |
| w9 | 48 | 0.023687 | 4.977 |
| w10 | 27 | 0.065094 | 30.557 |
| w11 | 10 | 0.023953 | 12.166 |
| w12 | 0 | -0.136757 | 0.0 |
| w14 | 50 | -0.026568 | -11.038 |
| w15 | 45 | -0.037278 | -19.656 |
| w16 | 42 | -0.013185 | 1.954 |
| w17 | 35 | 0.19044 | 133.504 |
| w18 | 2 | -0.112821 | -1.062 |
| w19 | 3 | -0.126584 | -3.36 |
| w20 | 19 | -0.086913 | -14.121 |
| w21 | 46 | 0.288527 | 215.289 |
| w22 | 4 | -0.041517 | -4.459 |
| w23 | 4 | -0.119537 | -11.72 |
| w24 | 0 | -0.084231 | 0.0 |

- w7 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 347 prefetch bars (<date> to <date>) -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 228 prefetch bars (<date> to <date>) -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | 0.042301 | 0.0 |
| w2 | 17 | -0.071061 | -2.719 |
| w3 | 8 | -0.159076 | -0.689 |
| w4 | 30 | -0.096076 | -8.563 |
| w5 | 61 | -0.056128 | -8.895 |
| w6 | 66 | -0.194546 | -45.435 |
| w7 | 0 | -0.074496 | 0.0 |
| w8 | 35 | -0.043399 | -2.539 |
| w9 | 41 | -0.131456 | -4.001 |
| w10 | 37 | 0.004084 | 25.505 |
| w11 | 22 | 0.064074 | 35.532 |
| w12 | 2 | -0.221246 | -1.783 |
| w14 | 0 | -0.101028 | 0.0 |
| w15 | 35 | 0.102211 | 37.375 |
| w16 | 37 | 0.07958 | 53.22 |
| w17 | 2 | -0.186476 | -2.13 |
| w18 | 4 | 0.008122 | 1.572 |
| w19 | 44 | 0.090385 | 36.169 |
| w20 | 35 | 0.029711 | 18.004 |
| w21 | 19 | -0.055845 | -0.074 |
| w22 | 0 | 0.005798 | 0.0 |
| w23 | 0 | -0.127201 | 0.0 |
| w24 | 20 | 0.213545 | 131.332 |

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 429 prefetch bars (<date> to <date>) -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

