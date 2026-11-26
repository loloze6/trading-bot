# Backtest of 041-01_agitated-fall-rise-vs-swing-giveback_1d

- Plan: `../../../../03_test_plan/night7_steadydecline_run/plans/041-01_agitated-fall-rise-vs-swing-giveback_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | 0.106813 | 0.0 |
| w2 | 23 | 0.035849 | 10.242 |
| w3 | 15 | 0.025509 | 2.098 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | -0.050413 | -5.032 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.12518 | 2.561 |
| w9 | 7 | -0.164206 | -8.216 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.006249 | -0.264 |
| w13 | 23 | 0.009492 | 1.678 |
| w14 | 18 | 0.167375 | 23.509 |
| w15 | 0 | None | 0.0 |
| w16 | 22 | 0.041562 | 1.21 |
| w17 | 0 | None | 0.0 |
| w18 | 24 | 0.07451 | 7.824 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | 0.065963 | 3.64 |
| w21 | 0 | None | 0.0 |
| w22 | 20 | 0.037823 | 1.784 |
| w23 | 0 | None | 0.0 |
| w24 | 15 | -0.047946 | -2.169 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.017494 | 1.933 |
| w2 | 28 | -0.007029 | 4.891 |
| w3 | 8 | 0.005571 | 0.64 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | 0.05832 | 0.505 |
| w9 | 5 | 0.071009 | 5.767 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 33 | 0.007567 | 7.136 |
| w15 | 7 | 0.047897 | 1.696 |
| w16 | 18 | 0.069365 | 2.391 |
| w17 | 1 | -9e-06 | -0.093 |
| w18 | 17 | -0.017469 | -3.109 |
| w19 | 0 | None | 0.0 |
| w20 | 20 | 0.105562 | 11.498 |
| w21 | 14 | -0.028941 | -6.191 |
| w22 | 28 | 0.250953 | 35.707 |
| w23 | 2 | 0.020845 | -5.026 |
| w24 | 11 | -0.068213 | -2.989 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 31 | 0.21454 | 28.466 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 9 | 0.013824 | 2.634 |
| w6 | 4 | -0.095833 | -5.769 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | -0.002869 | -2.933 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.018306 | -0.197 |
| w13 | 9 | -0.030825 | -1.166 |
| w14 | 19 | -0.028776 | -3.706 |
| w15 | 8 | 0.064949 | 2.96 |
| w16 | 14 | 0.120901 | 6.32 |
| w17 | 4 | 0.013142 | -0.754 |
| w18 | 13 | -0.024629 | -1.73 |
| w19 | 0 | None | 0.0 |
| w20 | 27 | 0.061273 | 6.482 |
| w21 | 0 | None | 0.0 |
| w22 | 20 | 0.03901 | 2.317 |
| w23 | 1 | 0.031273 | 0.825 |
| w24 | 19 | 0.002323 | 0.35 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.015374 | -2.056 |
| w2 | 21 | -0.112841 | -12.049 |
| w3 | 2 | 0.001283 | -0.21 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 7 | -0.101638 | -7.605 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | 0.132403 | 3.19 |
| w9 | 1 | 0.08913 | 0.491 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 18 | 0.060528 | 5.507 |
| w15 | 4 | -0.012313 | -0.445 |
| w16 | 23 | 0.056536 | 0.934 |
| w17 | 0 | None | 0.0 |
| w18 | 14 | 0.012725 | -0.067 |
| w19 | 17 | -0.024087 | -5.398 |
| w20 | 3 | 0.028056 | -0.054 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 6 | -0.219773 | -19.889 |
| w24 | 6 | -0.025351 | -2.958 |

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
| w1 | 2 | 0.089288 | 3.916 |
| w2 | 1 | 0.113146 | 10.927 |
| w3 | 0 | -0.021923 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | -0.038081 | -2.362 |
| w8 | 2 | 0.011817 | 0.233 |
| w9 | 6 | 0.056738 | 4.779 |
| w10 | 0 | None | 0.0 |
| w11 | 12 | -0.202736 | -22.679 |
| w12 | 0 | None | 0.0 |
| w14 | 4 | 0.053292 | 1.857 |
| w15 | 5 | 0.008786 | 0.463 |
| w16 | 18 | 0.199083 | 17.375 |
| w17 | 0 | None | 0.0 |
| w18 | 11 | 0.05216 | 3.277 |
| w19 | 2 | 0.037088 | 0.199 |
| w20 | 9 | -0.044145 | -6.216 |
| w21 | 2 | 0.115973 | 3.354 |
| w22 | 16 | 0.07669 | 4.952 |
| w23 | 0 | None | 0.0 |
| w24 | 13 | -0.023911 | -1.075 |

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
| w1 | 0 | None | 0.0 |
| w2 | 23 | 0.087145 | 8.121 |
| w3 | 13 | -0.143282 | -9.42 |
| w4 | 6 | 0.11005 | 4.174 |
| w5 | 10 | -0.167025 | -9.712 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.126349 | 1.8 |
| w9 | 16 | 0.037994 | 5.227 |
| w10 | 1 | -0.015115 | -0.3 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 7 | 0.137585 | 4.608 |
| w14 | 14 | 0.032957 | 2.252 |
| w15 | 2 | 0.092012 | 0.725 |
| w16 | 28 | 0.00434 | -10.72 |
| w17 | 7 | -0.05038 | -2.617 |
| w18 | 16 | -0.004783 | -0.136 |
| w19 | 24 | -0.078798 | -11.6 |
| w20 | 8 | -0.056034 | -7.66 |
| w21 | 5 | -0.004656 | -3.446 |
| w22 | 32 | 0.006185 | 0.162 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

