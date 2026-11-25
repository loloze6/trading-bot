# Backtest of 059-01_calm-decline-continues-return_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/059-01_calm-decline-continues-return_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 38 | -0.084035 | -6.734 |
| w2 | 16 | 0.082082 | 34.088 |
| w3 | 19 | 0.05517 | 5.193 |
| w4 | 21 | -0.036153 | -12.87 |
| w5 | 45 | -0.085471 | -7.141 |
| w6 | 7 | -0.137707 | -7.918 |
| w7 | 44 | -0.019627 | -0.386 |
| w8 | 12 | -0.064486 | -6.535 |
| w9 | 30 | -0.166596 | -34.025 |
| w10 | 19 | -0.051032 | -8.09 |
| w11 | 8 | -0.007627 | -5.405 |
| w12 | 33 | 0.060754 | 2.617 |
| w13 | 11 | -0.0563 | -1.684 |
| w14 | 25 | 0.07284 | 35.114 |
| w15 | 2 | -0.081178 | 0.065 |
| w16 | 13 | 0.054406 | 12.723 |
| w17 | 13 | 0.093797 | -0.271 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 14 | 0.066873 | 10.78 |
| w21 | 14 | -0.032078 | -9.717 |
| w22 | 20 | -0.042423 | -12.355 |
| w23 | 27 | -0.11429 | -12.422 |
| w24 | 19 | -0.018333 | -5.997 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 39 | -0.011485 | 11.449 |
| w2 | 8 | 0.10671 | 20.083 |
| w3 | 17 | 0.042487 | -0.662 |
| w4 | 13 | 0.001435 | -7.809 |
| w5 | 41 | -0.069934 | 0.14 |
| w6 | 21 | -0.038758 | -15.573 |
| w7 | 37 | 0.01907 | 29.152 |
| w8 | 10 | -0.021231 | -2.466 |
| w9 | 36 | -0.079266 | -7.141 |
| w10 | 17 | -0.076301 | -11.234 |
| w11 | 3 | -0.080906 | -7.201 |
| w12 | 24 | -0.049585 | -0.644 |
| w13 | 13 | 0.163829 | 27.992 |
| w14 | 11 | 0.140087 | 25.971 |
| w15 | 25 | 0.014503 | -1.219 |
| w16 | 0 | 0.006171 | 0.0 |
| w17 | 0 | 0.003397 | 0.0 |
| w18 | 3 | -0.03047 | -4.329 |
| w19 | 0 | None | 0.0 |
| w20 | 15 | 0.041647 | 3.396 |
| w21 | 11 | -0.107705 | -21.283 |
| w22 | 10 | -0.056473 | 3.299 |
| w23 | 13 | -0.045375 | -8.286 |
| w24 | 24 | -0.064256 | -6.709 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 48 | -0.151457 | -7.633 |
| w2 | 18 | -0.005775 | 7.877 |
| w3 | 35 | -0.029798 | -8.99 |
| w4 | 13 | 0.035938 | 2.62 |
| w5 | 24 | 0.045774 | 21.716 |
| w6 | 36 | -0.044552 | -20.717 |
| w7 | 42 | -0.013371 | 27.328 |
| w8 | 0 | -0.030166 | 0.0 |
| w9 | 44 | -0.101555 | -6.25 |
| w10 | 29 | -0.044754 | -19.361 |
| w11 | 3 | -0.07076 | -5.866 |
| w12 | 10 | -0.060842 | -0.504 |
| w13 | 23 | 0.011922 | 8.295 |
| w14 | 27 | 0.040085 | 17.058 |
| w15 | 23 | 0.161362 | 15.544 |
| w16 | 4 | -0.089002 | -2.299 |
| w17 | 2 | -0.029661 | -1.49 |
| w18 | 10 | -0.021655 | -3.586 |
| w19 | 10 | -0.109884 | -23.18 |
| w20 | 22 | 0.025883 | 12.347 |
| w21 | 19 | -0.002363 | -15.763 |
| w22 | 4 | 0.098922 | 8.302 |
| w23 | 25 | -0.095031 | -12.16 |
| w24 | 24 | -0.086137 | -11.318 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.110042 | -9.708 |
| w2 | 13 | -0.125872 | -9.117 |
| w3 | 40 | -0.110578 | -18.655 |
| w4 | 37 | -0.077951 | -10.782 |
| w5 | 59 | -0.045475 | -1.535 |
| w6 | 20 | -0.056861 | -3.526 |
| w7 | 51 | 0.007109 | 6.172 |
| w8 | 23 | -0.094563 | -7.677 |
| w9 | 52 | -0.065174 | 0.759 |
| w10 | 18 | -0.082577 | -9.825 |
| w11 | 4 | -0.061995 | -3.526 |
| w12 | 39 | -0.092254 | -5.751 |
| w14 | 14 | 0.092442 | 37.041 |
| w15 | 18 | -0.038169 | -8.171 |
| w16 | 2 | -0.10895 | -8.336 |
| w17 | 9 | -0.050099 | -2.59 |
| w18 | 3 | -0.035219 | -4.316 |
| w19 | 1 | 0.108698 | 8.115 |
| w20 | 12 | -0.028696 | -12.656 |
| w21 | 21 | 0.019428 | -10.408 |
| w22 | 10 | -0.000822 | -12.865 |
| w23 | 15 | 0.124189 | 32.966 |
| w24 | 4 | -0.104902 | -6.757 |

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
| w1 | 33 | 0.015463 | 19.8 |
| w2 | 7 | -0.036072 | 18.213 |
| w3 | 0 | 0.023611 | 0.0 |
| w4 | 0 | -0.068615 | 0.0 |
| w5 | 15 | 0.108432 | -2.076 |
| w6 | 16 | -0.161817 | -18.224 |
| w8 | 35 | -0.092083 | -5.499 |
| w9 | 34 | 0.003409 | 13.907 |
| w10 | 35 | 0.011624 | -5.981 |
| w11 | 0 | None | 0.0 |
| w12 | 35 | -0.009973 | 10.845 |
| w14 | 22 | 0.031601 | -27.884 |
| w15 | 33 | 0.073189 | 12.874 |
| w16 | 3 | -0.059946 | -0.95 |
| w17 | 15 | -0.053701 | -14.404 |
| w18 | 10 | -0.018196 | -3.996 |
| w19 | 14 | -0.029687 | -7.124 |
| w20 | 30 | 0.059699 | 15.277 |
| w21 | 13 | 0.025959 | -10.018 |
| w22 | 0 | None | 0.0 |
| w23 | 35 | -0.056326 | -11.034 |
| w24 | 44 | -0.198797 | -0.487 |

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
| w1 | 34 | 0.066258 | 9.216 |
| w2 | 13 | -0.017381 | -2.255 |
| w3 | 44 | 0.018915 | 9.346 |
| w4 | 28 | -0.08365 | -9.719 |
| w5 | 38 | 0.074214 | 42.131 |
| w6 | 24 | -0.115361 | -22.709 |
| w7 | 41 | -0.068455 | -6.615 |
| w8 | 28 | -0.026914 | -7.348 |
| w9 | 23 | 0.020304 | 2.526 |
| w10 | 11 | -0.140866 | -6.711 |
| w11 | 4 | -0.083078 | -7.639 |
| w12 | 6 | -0.048352 | -8.385 |
| w13 | 19 | 0.064212 | 13.553 |
| w14 | 27 | 0.088333 | 9.453 |
| w15 | 26 | 0.034355 | 11.711 |
| w16 | 0 | None | 0.0 |
| w17 | 16 | -0.017462 | -2.492 |
| w18 | 6 | -0.038647 | -3.754 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | -0.006302 | -4.759 |
| w21 | 14 | -0.086602 | -11.812 |
| w22 | 2 | -0.086187 | -4.13 |
| w23 | 22 | -0.028116 | -7.814 |
| w24 | 6 | -0.108978 | -7.092 |

