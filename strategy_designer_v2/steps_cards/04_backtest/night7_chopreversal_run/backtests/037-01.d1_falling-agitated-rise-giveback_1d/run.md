# Backtest of 037-01.d1_falling-agitated-rise-giveback_1d

- Plan: `../../../../03_test_plan/night7_chopreversal_run/plans/037-01.d1_falling-agitated-rise-giveback_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | 0.106813 | 0.0 |
| w2 | 13 | 0.037904 | 3.548 |
| w3 | 12 | -0.078641 | -3.696 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | -0.0182 | -1.935 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | 0.135681 | 2.062 |
| w9 | 6 | -0.003737 | -0.317 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.006249 | -0.264 |
| w13 | 14 | 0.016265 | 1.686 |
| w14 | 12 | 0.160101 | 10.773 |
| w15 | 0 | None | 0.0 |
| w16 | 15 | 0.033067 | 0.084 |
| w17 | 0 | None | 0.0 |
| w18 | 17 | 0.067244 | 3.102 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | 0.004012 | -0.174 |
| w21 | 0 | None | 0.0 |
| w22 | 15 | -0.082797 | -4.577 |
| w23 | 0 | None | 0.0 |
| w24 | 10 | 0.122953 | 5.523 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.02246 | 0.821 |
| w2 | 16 | 0.040195 | 4.662 |
| w3 | 6 | 0.001195 | 0.319 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 5 | -0.138092 | -2.795 |
| w9 | 2 | 0.086804 | 2.06 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 17 | 0.063125 | 3.937 |
| w15 | 6 | 0.022503 | 0.435 |
| w16 | 11 | -0.003747 | -1.423 |
| w17 | 1 | -9e-06 | -0.093 |
| w18 | 14 | 0.039066 | 0.889 |
| w19 | 0 | None | 0.0 |
| w20 | 12 | 0.118206 | 4.705 |
| w21 | 12 | 0.031789 | -1.78 |
| w22 | 20 | 0.030729 | 3.551 |
| w23 | 2 | 0.020845 | -5.026 |
| w24 | 7 | 0.052965 | 4.019 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 21 | 0.025582 | 2.313 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 8 | -0.015964 | 0.57 |
| w6 | 2 | -0.223404 | -4.932 |
| w7 | 0 | None | 0.0 |
| w8 | 4 | 0.015905 | -0.86 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.018306 | -0.197 |
| w13 | 8 | 0.012838 | 0.756 |
| w14 | 9 | 0.085338 | 4.456 |
| w15 | 6 | 0.099003 | 3.289 |
| w16 | 10 | 0.050822 | 0.425 |
| w17 | 4 | 0.013142 | -0.754 |
| w18 | 12 | 0.008857 | -0.201 |
| w19 | 0 | None | 0.0 |
| w20 | 19 | -0.105547 | -5.39 |
| w21 | 0 | None | 0.0 |
| w22 | 18 | 0.011642 | 0.002 |
| w23 | 0 | None | 0.0 |
| w24 | 16 | 0.066483 | 3.138 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.013854 | -0.248 |
| w2 | 15 | -0.059085 | -4.587 |
| w3 | 2 | 0.001283 | -0.21 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 5 | -0.065305 | -3.341 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.026901 | -0.149 |
| w9 | 1 | 0.08913 | 0.491 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 12 | 0.2022 | 11.436 |
| w15 | 4 | -0.012313 | -0.445 |
| w16 | 18 | 0.031544 | -0.279 |
| w17 | 0 | None | 0.0 |
| w18 | 13 | 0.042438 | 0.937 |
| w19 | 12 | -0.020126 | -2.712 |
| w20 | 3 | 0.028056 | -0.054 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 3 | -0.00689 | -0.346 |
| w24 | 5 | -0.02979 | -1.885 |

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
| w1 | 1 | 0.110467 | 2.156 |
| w2 | 1 | 0.202498 | 10.927 |
| w3 | 0 | -0.021923 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | -0.038081 | -2.362 |
| w8 | 2 | 0.011817 | 0.233 |
| w9 | 3 | -0.017642 | 2.253 |
| w10 | 0 | None | 0.0 |
| w11 | 11 | -0.185506 | -19.705 |
| w12 | 0 | None | 0.0 |
| w14 | 3 | 0.006087 | -0.081 |
| w15 | 4 | 0.060226 | 2.918 |
| w16 | 12 | 0.072036 | 1.738 |
| w17 | 0 | None | 0.0 |
| w18 | 9 | 0.13573 | 5.302 |
| w19 | 2 | 0.037088 | 0.199 |
| w20 | 8 | -0.038351 | -5.072 |
| w21 | 2 | 0.115973 | 3.354 |
| w22 | 11 | -0.007586 | -0.642 |
| w23 | 0 | None | 0.0 |
| w24 | 8 | -0.006167 | 0.138 |

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
| w2 | 17 | 0.120206 | 6.492 |
| w3 | 9 | -0.140929 | -5.212 |
| w4 | 5 | -0.010316 | -0.675 |
| w5 | 9 | -0.153334 | -6.723 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | 0.119237 | 1.349 |
| w9 | 11 | 0.066838 | 3.855 |
| w10 | 1 | -0.015115 | -0.3 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 7 | 0.137585 | 4.608 |
| w14 | 8 | 0.202404 | 8.654 |
| w15 | 2 | 0.092012 | 0.725 |
| w16 | 20 | -0.027663 | -6.797 |
| w17 | 6 | -0.000293 | -0.245 |
| w18 | 15 | 0.051233 | 2.353 |
| w19 | 15 | -0.106888 | -6.602 |
| w20 | 5 | -0.029629 | -2.012 |
| w21 | 4 | 0.01298 | -0.996 |
| w22 | 22 | -0.126438 | -7.217 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

