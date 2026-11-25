# Backtest of 047-01_falling-agitated-daily-fall-rebound_1d

- Plan: `../../../../03_test_plan/night7_chopreversal_run/plans/047-01_falling-agitated-daily-fall-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.049992 | -4.841 |
| w2 | 26 | 0.098307 | 1.538 |
| w3 | 21 | 0.221885 | 17.863 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.09751 | 5.213 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.053858 | 1.898 |
| w9 | 11 | -0.056481 | -7.412 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.092316 | 4.104 |
| w13 | 23 | 0.057524 | 4.373 |
| w14 | 20 | 0.178107 | 20.34 |
| w15 | 5 | -0.076779 | -2.268 |
| w16 | 17 | 0.292311 | 30.531 |
| w17 | 0 | None | 0.0 |
| w18 | 36 | 0.147653 | 16.485 |
| w19 | 0 | None | 0.0 |
| w20 | 12 | 0.06515 | 2.228 |
| w21 | 0 | None | 0.0 |
| w22 | 21 | 0.198666 | 23.452 |
| w23 | 0 | None | 0.0 |
| w24 | 20 | 0.064434 | 1.5 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.146887 | -12.956 |
| w2 | 37 | 0.009671 | -11.998 |
| w3 | 12 | 0.306604 | 22.805 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 12 | 0.161359 | 9.257 |
| w9 | 11 | 0.061904 | 2.672 |
| w10 | 1 | 0.123616 | 0.837 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 41 | 0.175631 | 18.8 |
| w15 | 6 | 0.018806 | 0.802 |
| w16 | 17 | 0.256054 | 23.777 |
| w17 | 1 | -0.006609 | 0.023 |
| w18 | 12 | 0.029131 | 2.734 |
| w19 | 1 | None | -0.057 |
| w20 | 25 | 0.072971 | -3.487 |
| w21 | 10 | 0.020188 | 2.47 |
| w22 | 39 | 0.058039 | -4.152 |
| w23 | 1 | 0.069586 | 0.125 |
| w24 | 11 | 0.138373 | 7.931 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 32 | 0.089917 | 4.519 |
| w3 | 1 | 0.393083 | 19.101 |
| w4 | 2 | 0.074184 | 3.047 |
| w5 | 8 | 0.005633 | -1.388 |
| w6 | 1 | 0.066606 | 2.17 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | -0.018863 | 0.553 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | 0.062104 | 3.413 |
| w13 | 7 | 0.090372 | 3.19 |
| w14 | 27 | 0.178808 | 17.087 |
| w15 | 11 | 0.143663 | 11.998 |
| w16 | 14 | 0.320704 | 29.702 |
| w17 | 3 | 0.054105 | 2.569 |
| w18 | 20 | 0.184815 | 12.501 |
| w19 | 1 | -0.042242 | -0.662 |
| w20 | 23 | 0.133164 | 8.685 |
| w21 | 1 | 0.047127 | 1.252 |
| w22 | 23 | 0.094799 | 6.177 |
| w23 | 3 | 0.096411 | 2.879 |
| w24 | 30 | -0.025494 | -7.709 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.092802 | -12.879 |
| w2 | 23 | 0.0454 | 0.082 |
| w3 | 2 | 0.140704 | 5.68 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | 0.004668 | 0.286 |
| w7 | 0 | None | 0.0 |
| w8 | 10 | 0.085102 | 3.852 |
| w9 | 2 | 0.03494 | 0.551 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 29 | 0.129872 | 8.001 |
| w15 | 3 | 0.092036 | 4.26 |
| w16 | 15 | 0.305978 | 25.686 |
| w17 | 0 | None | 0.0 |
| w18 | 20 | 0.265563 | 22.248 |
| w19 | 22 | 0.298948 | 32.454 |
| w20 | 2 | 0.25915 | 5.891 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 7 | 0.00288 | -0.645 |
| w24 | 2 | 0.018243 | 0.621 |

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
| w1 | 4 | 0.135099 | 4.491 |
| w2 | 0 | -0.001701 | 0.0 |
| w3 | 0 | 0.032731 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.043222 | 1.072 |
| w8 | 4 | 0.086274 | 2.678 |
| w9 | 6 | 0.085259 | 3.681 |
| w10 | 0 | None | 0.0 |
| w11 | 8 | 0.017222 | 3.349 |
| w12 | 0 | None | 0.0 |
| w14 | 7 | 0.015058 | 0.619 |
| w15 | 5 | 0.029966 | 1.58 |
| w16 | 23 | 0.270589 | 30.547 |
| w17 | 2 | 0.004451 | -0.512 |
| w18 | 13 | 0.016034 | 0.581 |
| w19 | 12 | -0.040558 | -7.502 |
| w20 | 5 | 0.055604 | 4.917 |
| w21 | 5 | -0.01078 | 3.136 |
| w22 | 21 | 0.079661 | 6.379 |
| w23 | 0 | None | 0.0 |
| w24 | 9 | 0.058369 | 2.127 |

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
| w1 | 1 | 0.021729 | 0.962 |
| w2 | 33 | 0.119486 | 6.518 |
| w3 | 9 | 0.209174 | 15.479 |
| w4 | 6 | -0.033887 | -1.441 |
| w5 | 11 | 0.109046 | 9.641 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | -0.063448 | -1.688 |
| w8 | 8 | 0.160206 | 3.965 |
| w9 | 23 | 0.125429 | 7.101 |
| w10 | 3 | -0.048169 | 0.53 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 10 | 0.090937 | 2.984 |
| w14 | 22 | 0.166226 | 14.654 |
| w15 | 10 | -0.046369 | -4.973 |
| w16 | 22 | 0.126785 | 16.333 |
| w17 | 8 | 0.212933 | 18.349 |
| w18 | 20 | 0.179887 | 13.474 |
| w19 | 34 | 0.07389 | 3.519 |
| w20 | 9 | 0.111773 | 11.527 |
| w21 | 5 | 0.002833 | 0.906 |
| w22 | 25 | -0.017708 | -8.624 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

