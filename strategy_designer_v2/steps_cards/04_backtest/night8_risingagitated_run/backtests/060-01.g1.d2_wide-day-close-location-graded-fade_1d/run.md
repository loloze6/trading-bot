# Backtest of 060-01.g1.d2_wide-day-close-location-graded-fade_1d

- Plan: `../../../../03_test_plan/night8_risingagitated_run/plans/060-01.g1.d2_wide-day-close-location-graded-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 10 | 0.063838 | 7.775 |
| w3 | 9 | 0.093314 | 6.718 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.035091 | 0.533 |
| w9 | 2 | -0.204345 | -7.991 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 7 | -0.020389 | -1.338 |
| w14 | 6 | 0.130335 | 12.947 |
| w15 | 0 | None | 0.0 |
| w16 | 7 | 0.03816 | 1.242 |
| w17 | 0 | None | 0.0 |
| w18 | 10 | 0.092831 | 7.888 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | 0.091751 | 3.946 |
| w21 | 0 | None | 0.0 |
| w22 | 7 | 0.051781 | 2.362 |
| w23 | 0 | None | 0.0 |
| w24 | 9 | 0.025903 | 2.638 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.028676 | -1.481 |
| w2 | 11 | 0.059919 | 8.215 |
| w3 | 4 | 0.053998 | 2.089 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 3 | 0.109399 | 3.33 |
| w9 | 2 | -0.011923 | -0.632 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 15 | 0.031482 | 9.211 |
| w15 | 0 | None | 0.0 |
| w16 | 5 | 0.078379 | 3.591 |
| w17 | 0 | None | 0.0 |
| w18 | 3 | 0.11494 | 3.548 |
| w19 | 0 | None | 0.0 |
| w20 | 7 | 0.114962 | 10.906 |
| w21 | 7 | 0.040633 | 0.61 |
| w22 | 13 | 0.294438 | 42.053 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | -0.045586 | -2.284 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 6 | -0.06862 | -2.349 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | 0.032699 | 0.97 |
| w6 | 2 | 0.003624 | -0.595 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.000823 | -0.508 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | -0.047797 | -1.676 |
| w14 | 11 | 0.028792 | 2.137 |
| w15 | 1 | -0.000973 | -0.138 |
| w16 | 5 | 0.097407 | 4.563 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | -0.1013 | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 10 | 0.105567 | 8.714 |
| w21 | 0 | None | 0.0 |
| w22 | 4 | 0.111133 | 5.787 |
| w23 | 1 | 0.031273 | 0.415 |
| w24 | 3 | -0.023638 | -0.978 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.017354 | -1.134 |
| w2 | 4 | -0.02868 | -2.399 |
| w3 | 1 | 0.017085 | 0.411 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | -0.095184 | -6.769 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.145601 | 3.452 |
| w9 | 0 | -0.011145 | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 6 | 0.131074 | 9.297 |
| w15 | 0 | None | 0.0 |
| w16 | 6 | 0.032773 | 0.37 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 9 | -0.024743 | -2.564 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.163226 | -9.717 |
| w24 | 1 | -0.009284 | -1.269 |

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
| w1 | 2 | 0.079767 | 2.558 |
| w2 | 0 | 0.024172 | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.013245 | 0.028 |
| w8 | 0 | None | 0.0 |
| w9 | 4 | 0.060193 | 4.276 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | 0.113433 | 2.606 |
| w12 | 0 | None | 0.0 |
| w14 | 1 | 0.061601 | 2.54 |
| w15 | 0 | -0.066589 | 0.0 |
| w16 | 7 | 0.139723 | 12.366 |
| w17 | 0 | None | 0.0 |
| w18 | 3 | 0.148036 | 5.593 |
| w19 | 2 | -0.128472 | -3.575 |
| w20 | 1 | -0.021193 | -0.744 |
| w21 | 1 | 0.000951 | -0.526 |
| w22 | 6 | 0.108992 | 5.969 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | 0.018746 | 1.576 |

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
| w2 | 7 | 0.09732 | 4.71 |
| w3 | 3 | -0.101443 | -3.788 |
| w4 | 1 | 0.139423 | 4.984 |
| w5 | 4 | -0.093102 | -3.974 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.046663 | 0.327 |
| w9 | 8 | 0.124824 | 8.048 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 6 | 0.190919 | 13.938 |
| w15 | 0 | None | 0.0 |
| w16 | 13 | 0.062159 | -0.722 |
| w17 | 2 | -0.025862 | -1.013 |
| w18 | 2 | -0.069933 | -1.827 |
| w19 | 10 | -0.064331 | -7.88 |
| w20 | 4 | -0.158529 | -15.965 |
| w21 | 2 | -0.047514 | -4.425 |
| w22 | 9 | 0.039884 | 1.908 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

