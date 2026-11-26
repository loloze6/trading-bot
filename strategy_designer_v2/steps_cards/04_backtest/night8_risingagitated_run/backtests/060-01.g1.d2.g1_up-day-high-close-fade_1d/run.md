# Backtest of 060-01.g1.d2.g1_up-day-high-close-fade_1d

- Plan: `../../../../03_test_plan/night8_risingagitated_run/plans/060-01.g1.d2.g1_up-day-high-close-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.119449 | 4.792 |
| w2 | 23 | -0.073113 | -4.106 |
| w3 | 16 | 0.015248 | 2.463 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.023034 | -0.231 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | 0.128734 | 4.816 |
| w9 | 10 | -0.024561 | -0.804 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.025417 | 1.443 |
| w13 | 21 | -0.003991 | -0.428 |
| w14 | 16 | 0.169887 | 28.148 |
| w15 | 1 | None | -0.03 |
| w16 | 18 | -0.010759 | -5.325 |
| w17 | 0 | None | 0.0 |
| w18 | 27 | 0.106463 | 15.009 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | 0.016922 | 0.712 |
| w21 | 0 | None | 0.0 |
| w22 | 18 | 0.063185 | 6.099 |
| w23 | 0 | None | 0.0 |
| w24 | 11 | 0.028247 | 5.047 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.004469 | -0.396 |
| w2 | 28 | -0.059962 | -3.74 |
| w3 | 6 | -0.025006 | -2.158 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.049726 | 2.202 |
| w9 | 6 | 0.116768 | 8.728 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 28 | 0.034264 | 14.635 |
| w15 | 6 | 0.074016 | 4.672 |
| w16 | 18 | 0.00554 | -4.551 |
| w17 | 1 | 0.002285 | -0.237 |
| w18 | 14 | 0.005595 | -3.104 |
| w19 | 0 | None | 0.0 |
| w20 | 17 | 0.071089 | 9.0 |
| w21 | 12 | 0.006843 | -3.816 |
| w22 | 26 | 0.136351 | 35.934 |
| w23 | 2 | 0.035962 | 0.176 |
| w24 | 9 | -0.022531 | -0.928 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 26 | 0.120278 | 27.006 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 10 | -0.02962 | -3.93 |
| w6 | 3 | -0.091114 | -4.653 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.025296 | -4.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.079054 | 3.94 |
| w13 | 8 | -0.003013 | -0.112 |
| w14 | 19 | -0.017091 | -1.61 |
| w15 | 7 | 0.072902 | 4.938 |
| w16 | 14 | 0.077198 | 4.667 |
| w17 | 4 | 0.02916 | -0.225 |
| w18 | 13 | 0.04591 | 4.299 |
| w19 | 0 | None | 0.0 |
| w20 | 24 | 0.017745 | 4.241 |
| w21 | 0 | None | 0.0 |
| w22 | 15 | 0.048802 | 4.887 |
| w23 | 1 | 0.031273 | 0.625 |
| w24 | 16 | -0.063131 | -7.076 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.091239 | -13.234 |
| w2 | 18 | -0.10265 | -16.33 |
| w3 | 3 | 0.012471 | -0.083 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | -0.08195 | -8.023 |
| w7 | 0 | None | 0.0 |
| w8 | 8 | 0.091968 | 3.434 |
| w9 | 1 | -0.022634 | -0.341 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 17 | 0.142355 | 23.068 |
| w15 | 3 | -0.018948 | -1.354 |
| w16 | 20 | 0.028559 | -2.89 |
| w17 | 0 | None | 0.0 |
| w18 | 15 | 0.02348 | 1.225 |
| w19 | 19 | -0.087154 | -14.461 |
| w20 | 2 | 0.051711 | 1.127 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 3 | -0.174645 | -15.948 |
| w24 | 5 | 0.042587 | 0.386 |

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
| w1 | 2 | 0.10035 | 4.025 |
| w2 | 1 | 0.093626 | 9.839 |
| w3 | 0 | -0.030569 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.062462 | -3.212 |
| w8 | 3 | -0.009137 | -0.385 |
| w9 | 5 | -0.02519 | -1.446 |
| w10 | 0 | None | 0.0 |
| w11 | 8 | 0.05234 | -0.65 |
| w12 | 0 | None | 0.0 |
| w14 | 5 | 0.032755 | 2.071 |
| w15 | 5 | 0.041544 | 2.851 |
| w16 | 18 | 0.175611 | 20.541 |
| w17 | 0 | None | 0.0 |
| w18 | 9 | 0.09404 | 7.673 |
| w19 | 2 | 0.037876 | 0.882 |
| w20 | 6 | -0.047969 | -10.899 |
| w21 | 2 | 0.112313 | 8.258 |
| w22 | 11 | 0.036988 | 2.106 |
| w23 | 0 | None | 0.0 |
| w24 | 11 | -0.015838 | 0.098 |

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
| w2 | 23 | 0.151554 | 28.51 |
| w3 | 11 | -0.074905 | -7.922 |
| w4 | 5 | 0.046215 | 2.205 |
| w5 | 9 | -0.093441 | -7.903 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.168258 | 6.856 |
| w9 | 19 | 0.002702 | 1.525 |
| w10 | 1 | -0.015115 | -0.552 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 7 | 0.117903 | 8.033 |
| w14 | 12 | 0.078567 | 12.823 |
| w15 | 3 | 0.040491 | 1.826 |
| w16 | 19 | -0.033631 | -16.351 |
| w17 | 4 | 0.002651 | -0.158 |
| w18 | 14 | 0.068953 | 5.97 |
| w19 | 16 | -0.07217 | -12.658 |
| w20 | 8 | -0.047147 | -8.508 |
| w21 | 5 | 0.013272 | -2.526 |
| w22 | 22 | -0.094823 | -14.873 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

