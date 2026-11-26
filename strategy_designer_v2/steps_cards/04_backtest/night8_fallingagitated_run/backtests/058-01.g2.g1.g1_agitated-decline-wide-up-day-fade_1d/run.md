# Backtest of 058-01.g2.g1.g1_agitated-decline-wide-up-day-fade_1d

- Plan: `../../../../03_test_plan/night8_fallingagitated_run/plans/058-01.g2.g1.g1_agitated-decline-wide-up-day-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.127213 | 1.244 |
| w2 | 25 | 0.102646 | 17.459 |
| w3 | 17 | 0.042381 | 3.07 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.043155 | -5.622 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | 0.124597 | 3.302 |
| w9 | 10 | -0.135453 | -5.922 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.035515 | 0.709 |
| w13 | 18 | 0.085095 | 6.872 |
| w14 | 19 | 0.170642 | 25.461 |
| w15 | 1 | None | -0.015 |
| w16 | 23 | 0.05914 | 2.371 |
| w17 | 0 | None | 0.0 |
| w18 | 28 | 0.14875 | 14.807 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | 0.042867 | 2.072 |
| w21 | 0 | None | 0.0 |
| w22 | 19 | 0.047685 | 1.88 |
| w23 | 0 | None | 0.0 |
| w24 | 14 | 0.006322 | 1.665 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.001681 | 0.319 |
| w2 | 29 | 0.025496 | 5.219 |
| w3 | 8 | 0.019971 | 1.126 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 8 | 0.101637 | 2.543 |
| w9 | 6 | 0.044346 | 2.504 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 34 | 0.077933 | 17.855 |
| w15 | 7 | 0.049097 | 1.798 |
| w16 | 22 | 0.062118 | 0.499 |
| w17 | 1 | -0.014649 | -0.278 |
| w18 | 13 | 0.013695 | -1.032 |
| w19 | 0 | None | 0.0 |
| w20 | 21 | 0.122584 | 10.882 |
| w21 | 9 | -0.012529 | -2.701 |
| w22 | 28 | 0.236274 | 33.213 |
| w23 | 2 | 0.034659 | 0.073 |
| w24 | 11 | -0.054297 | -2.815 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 26 | 0.190118 | 25.242 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 9 | 0.000678 | 0.172 |
| w6 | 3 | -0.12616 | -5.169 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | -0.005352 | -2.625 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | 0.098229 | 2.328 |
| w13 | 10 | -0.00061 | 0.106 |
| w14 | 20 | 0.019727 | 3.938 |
| w15 | 7 | 0.066412 | 2.897 |
| w16 | 16 | 0.137093 | 6.046 |
| w17 | 4 | 0.068157 | 1.303 |
| w18 | 15 | 0.032937 | 1.385 |
| w19 | 0 | None | 0.0 |
| w20 | 19 | -0.002448 | 0.191 |
| w21 | 0 | None | 0.0 |
| w22 | 20 | 0.039705 | 2.465 |
| w23 | 1 | 0.031273 | 0.572 |
| w24 | 17 | 0.035961 | 1.816 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.014367 | -0.174 |
| w2 | 19 | -0.107492 | -11.242 |
| w3 | 3 | 0.015862 | 0.046 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 5 | -0.066927 | -4.222 |
| w7 | 0 | None | 0.0 |
| w8 | 10 | 0.13396 | 1.927 |
| w9 | 2 | 0.050092 | 1.405 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 20 | 0.155904 | 20.453 |
| w15 | 5 | -0.007951 | -0.579 |
| w16 | 22 | 0.071287 | 1.256 |
| w17 | 0 | None | 0.0 |
| w18 | 11 | 0.047241 | 1.609 |
| w19 | 17 | -0.02108 | -3.614 |
| w20 | 3 | 0.031122 | 0.009 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 5 | -0.261322 | -19.361 |
| w24 | 7 | -0.039697 | -2.51 |

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
| w1 | 2 | 0.104782 | 3.221 |
| w2 | 1 | 0.078591 | 16.475 |
| w3 | 0 | -0.004877 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.049998 | -2.748 |
| w8 | 3 | 0.01321 | 0.16 |
| w9 | 6 | 0.042611 | 2.347 |
| w10 | 0 | None | 0.0 |
| w11 | 14 | -0.181114 | -23.252 |
| w12 | 0 | None | 0.0 |
| w14 | 4 | 0.04189 | 1.263 |
| w15 | 5 | 0.000348 | -0.038 |
| w16 | 21 | 0.22228 | 17.011 |
| w17 | 0 | None | 0.0 |
| w18 | 10 | 0.091119 | 5.064 |
| w19 | 3 | 0.013293 | -0.053 |
| w20 | 8 | -0.021008 | -4.969 |
| w21 | 2 | 0.108331 | 2.25 |
| w22 | 16 | 0.084898 | 4.585 |
| w23 | 0 | None | 0.0 |
| w24 | 11 | -0.002289 | 0.829 |

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
| w2 | 26 | 0.20944 | 22.701 |
| w3 | 15 | -0.120136 | -5.514 |
| w4 | 4 | 0.069704 | 1.778 |
| w5 | 11 | -0.189971 | -13.851 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 8 | 0.207764 | 3.328 |
| w9 | 16 | 0.070258 | 6.996 |
| w10 | 1 | -0.015115 | -0.164 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 7 | 0.137789 | 3.654 |
| w14 | 16 | 0.107683 | 12.055 |
| w15 | 4 | 0.112003 | 3.952 |
| w16 | 28 | 0.022515 | -7.969 |
| w17 | 5 | -0.049285 | -1.903 |
| w18 | 16 | 0.079626 | 5.17 |
| w19 | 23 | -0.133114 | -14.824 |
| w20 | 9 | -0.088081 | -9.655 |
| w21 | 6 | -0.029697 | -7.026 |
| w22 | 28 | -0.060138 | -7.216 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

