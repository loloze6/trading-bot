# Backtest of 058-01.g2.g1.g1.d1.d2_first-up-day-fade-concave_1d

- Plan: `../../../../03_test_plan/night8_fallingagitated_run/plans/058-01.g2.g1.g1.d1.d2_first-up-day-fade-concave_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.127213 | 1.244 |
| w2 | 17 | 0.145563 | 17.09 |
| w3 | 14 | 0.015088 | 0.474 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.048728 | -3.138 |
| w7 | 0 | None | 0.0 |
| w8 | 8 | 0.106256 | 2.725 |
| w9 | 7 | -0.143673 | -6.168 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | -0.025499 | -0.483 |
| w13 | 13 | 0.076226 | 5.073 |
| w14 | 14 | 0.221914 | 23.586 |
| w15 | 0 | None | 0.0 |
| w16 | 14 | 0.143273 | 7.3 |
| w17 | 0 | None | 0.0 |
| w18 | 22 | 0.093747 | 8.631 |
| w19 | 0 | None | 0.0 |
| w20 | 5 | 0.029735 | 1.236 |
| w21 | 0 | None | 0.0 |
| w22 | 15 | 0.051011 | 1.942 |
| w23 | 0 | None | 0.0 |
| w24 | 9 | -0.00595 | 0.497 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.03026 | -1.098 |
| w2 | 20 | 0.042231 | 7.392 |
| w3 | 7 | 0.018391 | 1.054 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | 0.048862 | 0.733 |
| w9 | 5 | 0.077932 | 3.397 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 26 | 0.120444 | 20.83 |
| w15 | 5 | 0.002503 | -0.351 |
| w16 | 13 | 0.09674 | 2.996 |
| w17 | 1 | -0.029217 | -0.234 |
| w18 | 8 | -0.002578 | -0.633 |
| w19 | 0 | None | 0.0 |
| w20 | 16 | 0.104787 | 8.176 |
| w21 | 6 | 0.043234 | 0.659 |
| w22 | 21 | 0.221412 | 28.913 |
| w23 | 2 | 0.022981 | -0.066 |
| w24 | 7 | -0.075971 | -3.952 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 20 | 0.125789 | 14.925 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 6 | -0.023737 | -0.965 |
| w6 | 1 | -0.135216 | -2.818 |
| w7 | 0 | None | 0.0 |
| w8 | 5 | 0.017526 | -1.04 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | -0.035714 | -0.421 |
| w13 | 6 | -0.042593 | -1.467 |
| w14 | 15 | 0.114786 | 12.958 |
| w15 | 5 | 0.027419 | 0.74 |
| w16 | 12 | 0.153585 | 7.261 |
| w17 | 1 | -0.009055 | -0.146 |
| w18 | 11 | -0.012556 | -0.841 |
| w19 | 0 | None | 0.0 |
| w20 | 14 | 0.105558 | 8.606 |
| w21 | 0 | None | 0.0 |
| w22 | 14 | 0.072583 | 4.676 |
| w23 | 1 | 0.031273 | 0.572 |
| w24 | 12 | -0.050921 | -2.141 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.065592 | 2.114 |
| w2 | 14 | -0.054963 | -4.869 |
| w3 | 3 | 0.015862 | 0.046 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.106103 | -3.296 |
| w7 | 0 | None | 0.0 |
| w8 | 8 | 0.063229 | 0.393 |
| w9 | 2 | 0.050092 | 1.405 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 17 | 0.173515 | 19.071 |
| w15 | 3 | 0.025396 | 0.272 |
| w16 | 14 | 0.121251 | 4.719 |
| w17 | 0 | None | 0.0 |
| w18 | 10 | -0.031455 | -1.219 |
| w19 | 12 | -0.017224 | -2.769 |
| w20 | 3 | 0.031122 | 0.009 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 4 | -0.292595 | -18.401 |
| w24 | 4 | 0.039741 | 0.059 |

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
| w1 | 1 | 0.0449 | 1.067 |
| w2 | 1 | 0.022861 | 16.475 |
| w3 | 0 | -6.7e-05 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.013003 | -0.427 |
| w8 | 3 | 0.01321 | 0.16 |
| w9 | 4 | 0.101681 | 4.284 |
| w10 | 0 | None | 0.0 |
| w11 | 6 | -0.01485 | -2.071 |
| w12 | 0 | None | 0.0 |
| w14 | 4 | 0.037969 | 1.007 |
| w15 | 4 | -0.001822 | -0.145 |
| w16 | 17 | 0.213507 | 12.28 |
| w17 | 0 | None | 0.0 |
| w18 | 9 | 0.025979 | 1.06 |
| w19 | 2 | 0.017067 | -0.024 |
| w20 | 5 | 0.04571 | 0.758 |
| w21 | 2 | 0.108331 | 2.25 |
| w22 | 10 | 0.069459 | 2.834 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | 0.083625 | 4.238 |

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
| w2 | 20 | 0.302472 | 29.127 |
| w3 | 8 | -0.079355 | -2.95 |
| w4 | 4 | 0.101783 | 2.331 |
| w5 | 4 | -0.202762 | -12.634 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.147809 | 2.052 |
| w9 | 12 | 0.03585 | 2.753 |
| w10 | 1 | -0.015115 | -0.164 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 6 | 0.138419 | 2.944 |
| w14 | 11 | 0.140562 | 11.05 |
| w15 | 3 | 0.082248 | 2.756 |
| w16 | 15 | 0.004404 | -3.958 |
| w17 | 4 | -0.026952 | -0.639 |
| w18 | 12 | 0.081918 | 3.266 |
| w19 | 14 | -0.093582 | -9.139 |
| w20 | 6 | -0.095022 | -9.119 |
| w21 | 2 | -0.012201 | -1.44 |
| w22 | 18 | -0.14404 | -12.391 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

