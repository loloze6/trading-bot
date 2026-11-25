# Backtest of 047-02_falling-agitated-daily-rise-giveback_1d

- Plan: `../../../../03_test_plan/night7_chopreversal_run/plans/047-02_falling-agitated-daily-rise-giveback_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.10272 | 0.331 |
| w2 | 25 | 0.052322 | 13.654 |
| w3 | 17 | 0.012029 | 1.078 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | -0.047624 | -5.713 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.111627 | 2.304 |
| w9 | 9 | -0.12502 | -6.432 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.006125 | -0.294 |
| w13 | 20 | 0.00824 | 1.487 |
| w14 | 20 | 0.177674 | 31.642 |
| w15 | 0 | None | 0.0 |
| w16 | 22 | 0.045826 | 1.664 |
| w17 | 0 | None | 0.0 |
| w18 | 24 | 0.08446 | 8.923 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | 0.057206 | 3.453 |
| w21 | 0 | None | 0.0 |
| w22 | 20 | 0.043153 | 2.359 |
| w23 | 0 | None | 0.0 |
| w24 | 15 | -0.043422 | -2.052 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.02111 | 2.309 |
| w2 | 29 | -0.007305 | 5.298 |
| w3 | 9 | -0.015466 | -0.885 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | 0.058609 | 0.711 |
| w9 | 6 | 0.069721 | 6.71 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 33 | 0.006593 | 7.428 |
| w15 | 7 | 0.049387 | 2.017 |
| w16 | 20 | 0.062478 | 1.481 |
| w17 | 1 | -6e-06 | -0.091 |
| w18 | 13 | -0.021739 | -2.71 |
| w19 | 0 | None | 0.0 |
| w20 | 20 | 0.099603 | 12.157 |
| w21 | 14 | 0.002968 | -3.644 |
| w22 | 28 | 0.247009 | 38.64 |
| w23 | 2 | 0.020654 | -4.981 |
| w24 | 12 | -0.058486 | -4.022 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 32 | 0.228688 | 36.635 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 9 | 0.007807 | 2.955 |
| w6 | 4 | -0.094477 | -5.697 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | -0.011433 | -4.021 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.018831 | -0.231 |
| w13 | 9 | -0.031486 | -1.184 |
| w14 | 20 | -0.045857 | -6.634 |
| w15 | 8 | 0.068562 | 3.254 |
| w16 | 14 | 0.117322 | 7.113 |
| w17 | 4 | 0.013338 | -0.774 |
| w18 | 11 | -0.026685 | -1.32 |
| w19 | 0 | None | 0.0 |
| w20 | 28 | 0.051033 | 6.824 |
| w21 | 0 | None | 0.0 |
| w22 | 17 | 0.038316 | 1.922 |
| w23 | 1 | 0.031273 | 0.825 |
| w24 | 19 | 0.002093 | -0.205 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.010345 | -1.937 |
| w2 | 21 | -0.129271 | -14.476 |
| w3 | 2 | 0.001128 | -0.301 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 7 | -0.100237 | -8.705 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | 0.123616 | 3.565 |
| w9 | 1 | 0.089224 | 0.499 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 18 | 0.089846 | 11.058 |
| w15 | 4 | -0.009944 | -0.49 |
| w16 | 20 | 0.089173 | 3.778 |
| w17 | 0 | None | 0.0 |
| w18 | 13 | -0.000538 | -0.617 |
| w19 | 21 | -0.066608 | -10.65 |
| w20 | 3 | 0.027846 | -0.062 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 6 | -0.191959 | -19.934 |
| w24 | 6 | -0.022861 | -3.847 |

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
| w1 | 2 | 0.100493 | 4.833 |
| w2 | 1 | 0.129312 | 13.563 |
| w3 | 0 | -0.023751 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | -0.037222 | -1.491 |
| w8 | 2 | 0.010756 | 0.25 |
| w9 | 6 | 0.054768 | 5.108 |
| w10 | 0 | None | 0.0 |
| w11 | 11 | -0.119115 | -14.604 |
| w12 | 0 | None | 0.0 |
| w14 | 4 | 0.055137 | 2.958 |
| w15 | 5 | 0.010807 | 0.55 |
| w16 | 18 | 0.191247 | 20.777 |
| w17 | 0 | None | 0.0 |
| w18 | 9 | 0.033084 | 0.824 |
| w19 | 2 | 0.033686 | 0.164 |
| w20 | 9 | -0.066951 | -8.452 |
| w21 | 2 | 0.116536 | 3.133 |
| w22 | 17 | 0.087056 | 5.263 |
| w23 | 0 | None | 0.0 |
| w24 | 13 | -0.020833 | -0.983 |

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
| w2 | 22 | 0.081479 | 7.833 |
| w3 | 14 | -0.155035 | -12.777 |
| w4 | 6 | 0.102548 | 4.009 |
| w5 | 12 | -0.172837 | -12.674 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.113041 | 1.69 |
| w9 | 16 | 0.041906 | 6.556 |
| w10 | 1 | -0.015115 | -0.228 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 7 | 0.138933 | 4.211 |
| w14 | 16 | 0.066157 | 6.054 |
| w15 | 2 | 0.091075 | 0.651 |
| w16 | 26 | 0.012476 | -10.581 |
| w17 | 7 | -0.048717 | -2.798 |
| w18 | 14 | 0.017351 | 0.575 |
| w19 | 25 | -0.069676 | -10.702 |
| w20 | 8 | -0.056452 | -7.335 |
| w21 | 5 | -0.00417 | -3.576 |
| w22 | 29 | 0.003929 | 2.137 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

