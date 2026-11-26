# Backtest of 077-01_choppy-calm-swing-rise-carries_1d

- Plan: `../../../../03_test_plan/night9_chopstretch_run/plans/077-01_choppy-calm-swing-rise-carries_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.099675 | -18.375 |
| w2 | 0 | None | 0.0 |
| w3 | 8 | -0.084039 | -35.045 |
| w4 | 1 | 0.15266 | 30.39 |
| w5 | 1 | 0.052476 | 4.622 |
| w6 | 4 | -0.118134 | -5.891 |
| w7 | 3 | 0.10582 | -11.996 |
| w8 | 2 | -0.066625 | -1.773 |
| w9 | 0 | None | 0.0 |
| w10 | 3 | 0.415315 | 39.901 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | -0.0016 | 2.733 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 4 | -0.012473 | 2.871 |
| w17 | 4 | 0.060654 | 30.485 |
| w18 | 4 | 0.06134 | 16.265 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 9 | -0.114319 | 9.004 |
| w22 | 4 | -0.037778 | -12.871 |
| w23 | 1 | 0.077995 | 3.537 |
| w24 | 7 | -0.118621 | -25.585 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.068102 | 8.269 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | -0.014357 | -5.164 |
| w4 | 4 | 0.040239 | 28.627 |
| w5 | 1 | 0.114813 | 7.942 |
| w6 | 3 | -0.053128 | -6.705 |
| w7 | 3 | -0.025841 | -4.902 |
| w8 | 2 | 0.151295 | -4.271 |
| w9 | 3 | -0.051826 | -26.539 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.071042 | 8.831 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | -0.023494 | -4.281 |
| w17 | 2 | 0.022257 | -0.693 |
| w18 | 1 | 0.081412 | 19.783 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | -0.023457 | -6.235 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.086883 | 36.967 |
| w24 | 1 | -0.329104 | -10.316 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.040678 | -4.39 |
| w2 | 4 | -0.003741 | -3.916 |
| w3 | 2 | 0.093656 | -13.129 |
| w4 | 2 | -0.003949 | 7.813 |
| w5 | 2 | -0.08164 | -1.029 |
| w6 | 1 | 0.005261 | 3.426 |
| w7 | 1 | -0.058273 | -8.767 |
| w8 | 0 | None | 0.0 |
| w9 | 4 | -0.040723 | -3.246 |
| w10 | 2 | -0.006444 | -7.119 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | 0.037533 | 2.422 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 1 | -0.019336 | -0.07 |
| w17 | 4 | -0.086813 | -1.197 |
| w18 | 2 | 0.035533 | 23.817 |
| w19 | 1 | 0.168357 | 16.903 |
| w20 | 0 | None | 0.0 |
| w21 | 6 | -0.038161 | -6.008 |
| w22 | 0 | None | 0.0 |
| w23 | 7 | 0.062208 | 24.675 |
| w24 | 4 | -0.219538 | -24.58 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.091928 | -24.613 |
| w2 | 2 | 0.010454 | -2.328 |
| w3 | 4 | -0.087007 | -19.871 |
| w4 | 4 | -0.010316 | 3.64 |
| w5 | 1 | 0.119861 | 13.244 |
| w6 | 5 | -0.018406 | -3.677 |
| w7 | 1 | -0.064369 | -10.988 |
| w8 | 2 | -0.002487 | -4.025 |
| w9 | 0 | None | 0.0 |
| w10 | 3 | -0.040385 | 20.157 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.053389 | -6.096 |
| w14 | 1 | -0.149543 | -15.926 |
| w15 | 0 | None | 0.0 |
| w16 | 5 | -0.018311 | -8.126 |
| w17 | 0 | None | 0.0 |
| w18 | 7 | 0.026652 | 14.26 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | -0.109871 | 6.658 |
| w21 | 1 | 0.035485 | 36.415 |
| w22 | 1 | 0.149002 | 27.915 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | -0.110298 | -1.793 |

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
| w1 | 5 | -0.050236 | -7.356 |
| w2 | 0 | -0.088963 | 0.0 |
| w3 | 0 | 0.035466 | 0.0 |
| w4 | 0 | 0.014481 | 0.0 |
| w5 | 0 | 0.002705 | 0.0 |
| w6 | 1 | 0.061087 | 10.871 |
| w8 | 2 | -0.098325 | -5.997 |
| w9 | 2 | -0.114358 | -27.43 |
| w10 | 10 | -0.122354 | 1.26 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | 0.000211 | -12.961 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | 0.500358 | 27.771 |
| w16 | 2 | -0.030794 | -1.323 |
| w17 | 1 | 0.05792 | 116.777 |
| w18 | 2 | 0.176729 | 34.579 |
| w19 | 6 | -0.038744 | 2.544 |
| w20 | 0 | None | 0.0 |
| w21 | 6 | -0.026994 | 81.838 |
| w22 | 0 | None | 0.0 |
| w23 | 5 | 0.054501 | 30.828 |
| w24 | 0 | None | 0.0 |

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
| w2 | 1 | -0.019312 | -3.632 |
| w3 | 2 | 0.02333 | -6.732 |
| w4 | 3 | -0.014159 | -13.908 |
| w5 | 0 | None | 0.0 |
| w6 | 5 | 0.016273 | -9.498 |
| w7 | 4 | -0.015431 | -11.546 |
| w8 | 5 | -0.282976 | 7.616 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | 0.097976 | 22.485 |
| w13 | 0 | None | 0.0 |
| w14 | 1 | -0.035342 | -4.22 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.052437 | 17.986 |
| w18 | 4 | 0.045007 | 20.98 |
| w19 | 0 | None | 0.0 |
| w20 | 5 | -0.11119 | -10.815 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.004351 | -4.665 |
| w24 | 4 | -0.007116 | 26.963 |

