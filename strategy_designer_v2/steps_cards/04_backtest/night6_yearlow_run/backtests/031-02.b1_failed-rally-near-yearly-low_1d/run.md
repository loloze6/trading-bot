# Backtest of 031-02.b1_failed-rally-near-yearly-low_1d

- Plan: `../../../../03_test_plan/night6_yearlow_run/plans/031-02.b1_failed-rally-near-yearly-low_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.036732 | 1.234 |
| w2 | 2 | 0.126486 | 11.991 |
| w3 | 3 | 0.107174 | 6.232 |
| w4 | 7 | -0.173603 | -1.736 |
| w5 | 3 | -0.065948 | -4.438 |
| w6 | 2 | 0.022633 | 17.263 |
| w7 | 2 | -0.011339 | 4.968 |
| w8 | 2 | -0.010728 | -12.873 |
| w9 | 1 | -0.043537 | -6.336 |
| w10 | 3 | -0.058983 | -0.103 |
| w11 | 3 | -0.01596 | 25.626 |
| w12 | 1 | 0.038562 | 2.635 |
| w13 | 1 | -0.067902 | -4.167 |
| w14 | 3 | 0.007005 | 30.057 |
| w15 | 2 | -0.11166 | 6.805 |
| w16 | 1 | 0.004309 | 0.112 |
| w17 | 3 | 0.147484 | 32.549 |
| w18 | 1 | -0.099666 | -6.019 |
| w19 | 4 | 0.006616 | 5.09 |
| w20 | 2 | -0.017629 | -3.157 |
| w21 | 0 | -0.174507 | 0.0 |
| w22 | 1 | 0.016617 | 0.06 |
| w23 | 2 | -0.190388 | -3.441 |
| w24 | 1 | -0.007538 | 4.447 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.040709 | 1.899 |
| w2 | 2 | 0.030076 | 9.355 |
| w3 | 5 | 0.06346 | 7.815 |
| w4 | 4 | -0.22159 | -0.466 |
| w5 | 5 | -0.027632 | 0.414 |
| w6 | 1 | -0.12822 | 1.645 |
| w7 | 1 | 0.123453 | 5.652 |
| w8 | 5 | -0.133508 | -6.914 |
| w9 | 1 | -0.043928 | -2.789 |
| w10 | 2 | 0.074242 | 14.576 |
| w11 | 2 | -0.053758 | 38.371 |
| w12 | 1 | -0.049636 | 0.566 |
| w13 | 2 | 0.009759 | -0.092 |
| w14 | 1 | 0.01013 | 10.815 |
| w15 | 2 | 0.034696 | 3.278 |
| w16 | 3 | 0.127609 | -4.576 |
| w17 | 2 | -0.018349 | 9.671 |
| w18 | 2 | -0.115835 | -5.612 |
| w19 | 3 | -0.07043 | -0.528 |
| w20 | 5 | -0.03099 | -6.069 |
| w21 | 2 | -0.163452 | -6.597 |
| w22 | 1 | -0.063503 | 0.171 |
| w23 | 2 | -0.058062 | 14.7 |
| w24 | 3 | -0.021884 | -3.471 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.072656 | 5.831 |
| w2 | 2 | 0.092298 | 11.015 |
| w3 | 9 | -0.025361 | 0.399 |
| w4 | 3 | -0.125746 | 2.733 |
| w5 | 6 | -0.09898 | -4.178 |
| w6 | 1 | 0.006933 | -1.255 |
| w7 | 3 | 0.037188 | 5.523 |
| w8 | 7 | -0.135583 | -15.206 |
| w9 | 0 | None | 0.0 |
| w10 | 5 | -0.080823 | -7.862 |
| w11 | 1 | None | 17.243 |
| w12 | 2 | -0.021002 | -3.094 |
| w13 | 3 | -0.073018 | -3.514 |
| w14 | 1 | 0.072465 | 13.321 |
| w15 | 3 | 0.096955 | -1.674 |
| w16 | 2 | 0.088402 | 2.39 |
| w17 | 2 | 0.111162 | 19.702 |
| w18 | 2 | -0.116932 | -7.312 |
| w19 | 6 | -0.105638 | -8.198 |
| w20 | 0 | -0.047678 | 0.0 |
| w21 | 8 | -0.001104 | 2.094 |
| w22 | 2 | 0.056027 | 1.09 |
| w23 | 5 | -0.117919 | -0.856 |
| w24 | 0 | -0.150849 | 0.0 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.011882 | 1.685 |
| w2 | 2 | 0.054086 | 1.451 |
| w3 | 1 | -0.077899 | -0.089 |
| w4 | 4 | -0.108086 | -2.619 |
| w5 | 1 | 0.007898 | 1.739 |
| w6 | 3 | -0.129412 | -3.928 |
| w7 | 1 | 0.118531 | 4.172 |
| w8 | 2 | -0.01525 | -6.095 |
| w9 | 2 | 0.000503 | -5.1 |
| w10 | 3 | 0.008476 | 9.002 |
| w11 | 4 | -0.12758 | 31.849 |
| w12 | 6 | 0.100427 | 5.089 |
| w14 | 5 | 0.064164 | 16.098 |
| w15 | 7 | -0.153855 | -11.2 |
| w16 | 3 | -0.029113 | -3.953 |
| w17 | 1 | -0.118882 | 17.747 |
| w18 | 2 | -0.140377 | -8.535 |
| w19 | 2 | -0.064856 | -0.46 |
| w20 | 6 | -0.206997 | -0.168 |
| w21 | 7 | -0.043222 | 0.5 |
| w22 | 9 | 0.010116 | 5.295 |
| w23 | 2 | 0.05977 | 2.597 |
| w24 | 3 | -0.157862 | 2.144 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.101321 | 8.775 |
| w2 | 0 | 0.040685 | 0.0 |
| w3 | 0 | 0.086518 | 0.0 |
| w4 | 0 | -0.091681 | 0.0 |
| w5 | 2 | -0.18483 | -1.933 |
| w6 | 3 | -0.08462 | 0.151 |
| w8 | 6 | -0.001826 | -0.096 |
| w9 | 3 | -0.003088 | 1.188 |
| w10 | 7 | -0.006975 | 11.135 |
| w11 | 4 | -0.058881 | 15.077 |
| w12 | 4 | -0.136119 | -5.919 |
| w14 | 2 | -0.043418 | -2.6 |
| w15 | 5 | -0.183935 | -11.002 |
| w16 | 6 | -0.056354 | -1.578 |
| w17 | 8 | -0.001332 | 41.397 |
| w18 | 4 | -0.125678 | -6.113 |
| w19 | 3 | -0.021616 | -2.613 |
| w20 | 6 | -0.15597 | 3.317 |
| w21 | 6 | 0.172581 | 45.978 |
| w22 | 6 | -0.026132 | -1.02 |
| w23 | 7 | -0.103004 | 1.211 |
| w24 | 0 | 0.10973 | 0.0 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.080468 | 2.657 |
| w2 | 2 | 0.114041 | 3.942 |
| w3 | 6 | -0.045875 | 7.653 |
| w4 | 1 | -0.175867 | -4.66 |
| w5 | 5 | -0.066353 | -3.277 |
| w6 | 4 | -0.228331 | -7.956 |
| w7 | 1 | 0.024428 | 2.934 |
| w8 | 6 | -0.126746 | -10.998 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | -0.031593 | 10.082 |
| w11 | 3 | -0.170444 | 22.997 |
| w12 | 7 | -0.042562 | -11.233 |
| w14 | 1 | 0.074728 | 12.88 |
| w15 | 5 | 0.03826 | -2.805 |
| w16 | 2 | -0.051486 | -0.38 |
| w17 | 6 | -0.190122 | -5.929 |
| w18 | 2 | -0.098614 | -6.857 |
| w19 | 4 | -0.050987 | -4.409 |
| w20 | 3 | 0.029331 | -1.241 |
| w21 | 3 | -0.023751 | 19.797 |
| w22 | 1 | -0.057246 | -2.271 |
| w23 | 7 | -0.058868 | -1.273 |
| w24 | 5 | -0.017023 | 30.242 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

