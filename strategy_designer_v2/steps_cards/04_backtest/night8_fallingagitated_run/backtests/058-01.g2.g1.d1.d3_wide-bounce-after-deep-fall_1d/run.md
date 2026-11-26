# Backtest of 058-01.g2.g1.d1.d3_wide-bounce-after-deep-fall_1d

- Plan: `../../../../03_test_plan/night8_fallingagitated_run/plans/058-01.g2.g1.d1.d3_wide-bounce-after-deep-fall_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.128914 | 4.312 |
| w2 | 15 | 0.07954 | 9.633 |
| w3 | 14 | 0.011955 | 0.443 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.058456 | -3.995 |
| w7 | 0 | None | 0.0 |
| w8 | 5 | 0.012568 | -0.326 |
| w9 | 7 | -0.081359 | -4.246 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.038825 | 0.453 |
| w13 | 13 | 0.105663 | 7.297 |
| w14 | 14 | 0.130961 | 17.105 |
| w15 | 1 | None | -0.025 |
| w16 | 12 | 0.106597 | 5.555 |
| w17 | 0 | None | 0.0 |
| w18 | 23 | 0.167065 | 18.374 |
| w19 | 0 | None | 0.0 |
| w20 | 7 | 0.047099 | 2.171 |
| w21 | 0 | None | 0.0 |
| w22 | 9 | 0.136475 | 8.727 |
| w23 | 0 | None | 0.0 |
| w24 | 8 | -0.046751 | -1.755 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.004726 | -0.69 |
| w2 | 20 | -0.060952 | -5.164 |
| w3 | 8 | 0.014806 | 0.762 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 5 | 0.057967 | 0.905 |
| w9 | 4 | 0.048895 | 1.925 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 18 | 0.047755 | 8.752 |
| w15 | 4 | 0.024375 | 0.576 |
| w16 | 12 | 0.057816 | 1.272 |
| w17 | 1 | -0.01685 | -0.429 |
| w18 | 10 | 0.067415 | 2.247 |
| w19 | 0 | None | 0.0 |
| w20 | 17 | 0.093894 | 9.01 |
| w21 | 6 | -0.027672 | -2.455 |
| w22 | 21 | 0.222066 | 27.909 |
| w23 | 1 | 0.021772 | 0.026 |
| w24 | 9 | -0.071255 | -2.808 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 20 | 0.102245 | 15.079 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 7 | -0.07702 | -3.916 |
| w6 | 1 | -0.133437 | -5.164 |
| w7 | 0 | None | 0.0 |
| w8 | 4 | 0.09201 | 1.408 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | 0.108992 | 2.236 |
| w13 | 5 | 0.035117 | 0.827 |
| w14 | 14 | 0.056428 | 6.035 |
| w15 | 6 | 0.031727 | 0.942 |
| w16 | 9 | 0.155657 | 7.438 |
| w17 | 1 | 0.001341 | -0.162 |
| w18 | 11 | 0.04107 | 2.125 |
| w19 | 0 | None | 0.0 |
| w20 | 15 | 0.06038 | 5.314 |
| w21 | 0 | None | 0.0 |
| w22 | 11 | 0.091124 | 7.052 |
| w23 | 1 | 0.031273 | 0.385 |
| w24 | 14 | -0.022195 | -1.026 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.100827 | 4.576 |
| w2 | 13 | -0.126837 | -11.715 |
| w3 | 2 | 0.028512 | 0.483 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | -0.156095 | -5.404 |
| w7 | 0 | None | 0.0 |
| w8 | 5 | 0.005451 | -0.54 |
| w9 | 2 | 0.049363 | 2.01 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 15 | 0.093974 | 9.321 |
| w15 | 3 | 0.002354 | -0.231 |
| w16 | 12 | 0.083307 | 2.937 |
| w17 | 0 | None | 0.0 |
| w18 | 10 | 0.030431 | 0.968 |
| w19 | 12 | -0.018197 | -4.009 |
| w20 | 2 | 0.050342 | 0.764 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 3 | -0.289049 | -20.729 |
| w24 | 3 | -0.018404 | -1.18 |

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
| w1 | 2 | 0.116195 | 2.574 |
| w2 | 1 | -0.034656 | 17.251 |
| w3 | 0 | -0.06846 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.066423 | -3.435 |
| w8 | 3 | -0.002466 | -0.057 |
| w9 | 3 | 0.071354 | 2.94 |
| w10 | 0 | None | 0.0 |
| w11 | 8 | -0.252938 | -15.546 |
| w12 | 0 | None | 0.0 |
| w14 | 3 | 0.05018 | 1.855 |
| w15 | 4 | -0.018224 | -0.965 |
| w16 | 12 | 0.157694 | 8.888 |
| w17 | 0 | None | 0.0 |
| w18 | 10 | 0.111419 | 6.209 |
| w19 | 3 | 0.006955 | -0.244 |
| w20 | 5 | -0.000579 | -1.844 |
| w21 | 2 | 0.117427 | 4.633 |
| w22 | 10 | 0.09951 | 4.331 |
| w23 | 0 | None | 0.0 |
| w24 | 10 | 0.010125 | 1.412 |

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
| w2 | 16 | 0.207463 | 20.392 |
| w3 | 8 | -0.129729 | -6.206 |
| w4 | 4 | 0.090484 | 1.959 |
| w5 | 8 | -0.156772 | -9.703 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 5 | 0.091069 | 1.171 |
| w9 | 11 | 0.002073 | 0.417 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 5 | 0.097126 | 2.8 |
| w14 | 10 | 0.091919 | 8.085 |
| w15 | 4 | 0.108716 | 3.561 |
| w16 | 13 | 0.041489 | -1.3 |
| w17 | 2 | 0.039886 | 0.822 |
| w18 | 15 | 0.069116 | 4.911 |
| w19 | 15 | -0.106539 | -9.61 |
| w20 | 6 | 0.064509 | 3.125 |
| w21 | 3 | -0.066961 | -3.735 |
| w22 | 16 | -0.110067 | -9.914 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

