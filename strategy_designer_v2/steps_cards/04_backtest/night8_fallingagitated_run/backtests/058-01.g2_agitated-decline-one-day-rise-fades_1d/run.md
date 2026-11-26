# Backtest of 058-01.g2_agitated-decline-one-day-rise-fades_1d

- Plan: `../../../../03_test_plan/night8_fallingagitated_run/plans/058-01.g2_agitated-decline-one-day-rise-fades_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | 0.106813 | 0.0 |
| w2 | 25 | 0.035849 | 11.594 |
| w3 | 20 | 0.025509 | 10.342 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | -0.050413 | -6.026 |
| w7 | 0 | None | 0.0 |
| w8 | 8 | 0.12518 | 1.062 |
| w9 | 9 | -0.164206 | -7.702 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.006249 | 3.249 |
| w13 | 19 | 0.009492 | -5.052 |
| w14 | 16 | 0.167375 | 22.412 |
| w15 | 0 | None | 0.0 |
| w16 | 24 | 0.041562 | -4.315 |
| w17 | 0 | None | 0.0 |
| w18 | 29 | 0.07451 | 6.831 |
| w19 | 0 | None | 0.0 |
| w20 | 9 | 0.065963 | -10.535 |
| w21 | 0 | None | 0.0 |
| w22 | 20 | 0.037823 | -7.742 |
| w23 | 0 | None | 0.0 |
| w24 | 16 | -0.047946 | 3.512 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.017494 | 11.141 |
| w2 | 32 | -0.007029 | -13.054 |
| w3 | 13 | 0.005571 | 7.331 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 8 | 0.05832 | 1.553 |
| w9 | 7 | 0.071009 | -2.887 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 34 | 0.007567 | -5.581 |
| w15 | 7 | 0.047897 | 1.311 |
| w16 | 21 | 0.069365 | -3.446 |
| w17 | 2 | -9e-06 | 0.686 |
| w18 | 18 | -0.017469 | -3.563 |
| w19 | 0 | None | 0.0 |
| w20 | 21 | 0.105562 | -14.841 |
| w21 | 14 | -0.028941 | -1.04 |
| w22 | 29 | 0.250953 | 44.111 |
| w23 | 3 | 0.020845 | -1.728 |
| w24 | 15 | -0.068213 | 0.93 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 30 | 0.21454 | 9.325 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 11 | 0.013824 | 7.212 |
| w6 | 4 | -0.095833 | -10.019 |
| w7 | 0 | None | 0.0 |
| w8 | 10 | -0.002869 | -1.942 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.018306 | 1.177 |
| w13 | 7 | -0.030825 | -11.999 |
| w14 | 19 | -0.028776 | -3.811 |
| w15 | 7 | 0.064949 | 12.934 |
| w16 | 14 | 0.120901 | 4.676 |
| w17 | 4 | 0.013142 | 0.548 |
| w18 | 16 | -0.024629 | 0.264 |
| w19 | 0 | None | 0.0 |
| w20 | 29 | 0.061273 | -9.517 |
| w21 | 0 | None | 0.0 |
| w22 | 24 | 0.03901 | -7.639 |
| w23 | 1 | 0.031273 | 4.086 |
| w24 | 22 | 0.002323 | 1.832 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.015374 | -18.391 |
| w2 | 25 | -0.112841 | -14.779 |
| w3 | 1 | 0.001283 | -1.294 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 8 | -0.101638 | -6.29 |
| w7 | 0 | None | 0.0 |
| w8 | 10 | 0.132403 | 0.348 |
| w9 | 1 | 0.08913 | 0.412 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 22 | 0.060528 | 0.34 |
| w15 | 5 | -0.012313 | -2.144 |
| w16 | 23 | 0.056536 | -9.176 |
| w17 | 0 | None | 0.0 |
| w18 | 15 | 0.012725 | 2.616 |
| w19 | 21 | -0.024087 | -3.193 |
| w20 | 4 | 0.028056 | -2.829 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 7 | -0.219773 | -9.153 |
| w24 | 7 | -0.025351 | -7.839 |

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
| w1 | 2 | 0.089288 | 3.43 |
| w2 | 5 | 0.113146 | 12.655 |
| w3 | 0 | -0.021923 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 6 | -0.038081 | -2.688 |
| w8 | 3 | 0.011817 | 1.123 |
| w9 | 7 | 0.056738 | 3.399 |
| w10 | 0 | None | 0.0 |
| w11 | 14 | -0.202736 | -22.742 |
| w12 | 0 | None | 0.0 |
| w14 | 5 | 0.053292 | 2.028 |
| w15 | 5 | 0.008786 | 0.442 |
| w16 | 18 | 0.199083 | 15.951 |
| w17 | 0 | None | 0.0 |
| w18 | 13 | 0.05216 | 6.432 |
| w19 | 3 | 0.037088 | 0.5 |
| w20 | 8 | -0.044145 | -15.637 |
| w21 | 2 | 0.115973 | 2.013 |
| w22 | 15 | 0.07669 | 4.42 |
| w23 | 0 | None | 0.0 |
| w24 | 15 | -0.023911 | -1.454 |

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
| w2 | 23 | 0.087145 | 3.198 |
| w3 | 16 | -0.143282 | -8.535 |
| w4 | 7 | 0.11005 | 3.557 |
| w5 | 12 | -0.167025 | -15.581 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 10 | 0.126349 | 2.445 |
| w9 | 17 | 0.037994 | 8.916 |
| w10 | 2 | -0.015115 | 0.819 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 7 | 0.137585 | 6.596 |
| w14 | 16 | 0.032957 | -4.733 |
| w15 | 2 | 0.092012 | 1.31 |
| w16 | 29 | 0.00434 | -22.355 |
| w17 | 6 | -0.05038 | -5.055 |
| w18 | 18 | -0.004783 | 2.648 |
| w19 | 27 | -0.078798 | -16.285 |
| w20 | 8 | -0.056034 | -20.214 |
| w21 | 8 | -0.004656 | -5.209 |
| w22 | 34 | 0.006185 | 7.704 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

