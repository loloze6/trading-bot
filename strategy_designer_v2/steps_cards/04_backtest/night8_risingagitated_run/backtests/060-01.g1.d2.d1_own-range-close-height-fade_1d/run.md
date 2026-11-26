# Backtest of 060-01.g1.d2.d1_own-range-close-height-fade_1d

- Plan: `../../../../03_test_plan/night8_risingagitated_run/plans/060-01.g1.d2.d1_own-range-close-height-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 9 | 0.069995 | 9.756 |
| w3 | 8 | 0.100964 | 9.028 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.038604 | 0.651 |
| w9 | 1 | -0.203664 | -7.861 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 7 | -0.019593 | -1.586 |
| w14 | 6 | 0.121326 | 15.001 |
| w15 | 0 | None | 0.0 |
| w16 | 6 | 0.050456 | 2.587 |
| w17 | 0 | None | 0.0 |
| w18 | 10 | 0.107023 | 10.208 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | 0.092991 | 4.669 |
| w21 | 0 | None | 0.0 |
| w22 | 7 | 0.038381 | 1.721 |
| w23 | 0 | None | 0.0 |
| w24 | 9 | 0.006549 | 1.403 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.032396 | -1.912 |
| w2 | 10 | 0.067512 | 9.929 |
| w3 | 3 | 0.062838 | 2.897 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 3 | 0.119919 | 4.204 |
| w9 | 2 | -0.023966 | -1.264 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 14 | 0.043223 | 13.367 |
| w15 | 0 | None | 0.0 |
| w16 | 5 | 0.07672 | 3.886 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | 0.118119 | 4.113 |
| w19 | 0 | None | 0.0 |
| w20 | 7 | 0.109956 | 12.515 |
| w21 | 6 | 0.051424 | 1.609 |
| w22 | 13 | 0.276629 | 45.693 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | -0.040802 | -2.277 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 6 | -0.089922 | -6.06 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | 0.034661 | 0.91 |
| w6 | 2 | -0.003371 | -0.996 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.042874 | 1.352 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | -0.047733 | -1.864 |
| w14 | 8 | 0.034684 | 2.945 |
| w15 | 1 | -0.000973 | -0.148 |
| w16 | 4 | 0.105449 | 5.766 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | -0.1013 | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 9 | 0.089521 | 9.737 |
| w21 | 0 | None | 0.0 |
| w22 | 4 | 0.104354 | 6.612 |
| w23 | 1 | 0.031273 | 0.418 |
| w24 | 3 | -0.024435 | -0.922 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.029412 | -1.79 |
| w2 | 5 | -0.02991 | -3.51 |
| w3 | 1 | 0.018023 | 0.514 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | -0.088812 | -6.165 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.145087 | 3.775 |
| w9 | 0 | -0.011145 | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 6 | 0.135362 | 10.381 |
| w15 | 0 | None | 0.0 |
| w16 | 5 | 0.038448 | 0.983 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 8 | -0.020686 | -1.854 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.149128 | -8.696 |
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
| w1 | 2 | 0.061068 | 2.422 |
| w2 | 0 | 0.029324 | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.013245 | 0.017 |
| w8 | 0 | None | 0.0 |
| w9 | 4 | 0.058157 | 5.037 |
| w10 | 0 | None | 0.0 |
| w11 | 3 | 0.132883 | 3.704 |
| w12 | 0 | None | 0.0 |
| w14 | 1 | 0.063315 | 3.078 |
| w15 | 0 | -0.066589 | 0.0 |
| w16 | 6 | 0.153822 | 14.786 |
| w17 | 0 | None | 0.0 |
| w18 | 3 | 0.147934 | 6.824 |
| w19 | 2 | -0.133475 | -4.687 |
| w20 | 1 | -0.021193 | -0.646 |
| w21 | 1 | 0.000951 | -0.27 |
| w22 | 6 | 0.099777 | 6.988 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | 0.015967 | 1.642 |

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
| w2 | 5 | 0.121583 | 8.677 |
| w3 | 4 | -0.096851 | -3.576 |
| w4 | 1 | 0.139423 | 4.984 |
| w5 | 4 | -0.083782 | -3.874 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.046663 | 0.244 |
| w9 | 8 | 0.12833 | 8.711 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 5 | 0.167281 | 13.894 |
| w15 | 0 | None | 0.0 |
| w16 | 13 | 0.065701 | -1.125 |
| w17 | 3 | -0.039294 | -2.144 |
| w18 | 2 | -0.069799 | -2.059 |
| w19 | 10 | -0.058055 | -8.322 |
| w20 | 4 | -0.162935 | -17.951 |
| w21 | 2 | -0.050951 | -5.124 |
| w22 | 6 | 0.026304 | 1.641 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

