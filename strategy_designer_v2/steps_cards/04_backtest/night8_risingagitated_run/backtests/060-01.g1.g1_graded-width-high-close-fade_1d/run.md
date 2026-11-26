# Backtest of 060-01.g1.g1_graded-width-high-close-fade_1d

- Plan: `../../../../03_test_plan/night8_risingagitated_run/plans/060-01.g1.g1_graded-width-high-close-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.128398 | 1.588 |
| w2 | 27 | -0.022113 | 4.385 |
| w3 | 22 | 0.064172 | 6.024 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.022375 | -0.187 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.042934 | 0.424 |
| w9 | 12 | -0.08413 | -4.83 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.035969 | 0.592 |
| w13 | 19 | 0.0352 | 3.896 |
| w14 | 17 | 0.208484 | 23.96 |
| w15 | 1 | None | -0.014 |
| w16 | 23 | 0.046425 | 0.879 |
| w17 | 0 | None | 0.0 |
| w18 | 26 | -0.086122 | -12.084 |
| w19 | 0 | None | 0.0 |
| w20 | 8 | -0.041343 | -4.641 |
| w21 | 0 | None | 0.0 |
| w22 | 23 | 0.097597 | 7.741 |
| w23 | 0 | None | 0.0 |
| w24 | 16 | 0.060888 | 5.316 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.059116 | 5.334 |
| w2 | 30 | -0.09049 | -9.088 |
| w3 | 8 | 0.017029 | 0.924 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | 0.088385 | 2.302 |
| w9 | 9 | 0.03299 | 2.667 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 35 | 0.067304 | 15.236 |
| w15 | 7 | 0.111011 | 4.664 |
| w16 | 23 | 0.079242 | 2.155 |
| w17 | 2 | 0.006861 | -0.204 |
| w18 | 14 | -0.051462 | -5.746 |
| w19 | 0 | None | 0.0 |
| w20 | 23 | 0.090437 | 10.117 |
| w21 | 14 | 0.010386 | -1.892 |
| w22 | 35 | 0.265724 | 48.913 |
| w23 | 5 | 0.054235 | 0.572 |
| w24 | 11 | -0.052302 | -2.893 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 27 | 0.082011 | 12.735 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 10 | -0.008359 | -0.383 |
| w6 | 3 | -0.064833 | -3.409 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | -0.009682 | -2.629 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | 0.102462 | 1.896 |
| w13 | 8 | -0.112386 | -7.537 |
| w14 | 22 | 0.025396 | 4.244 |
| w15 | 7 | 0.022473 | 0.39 |
| w16 | 18 | 0.120348 | 6.97 |
| w17 | 4 | 0.036744 | 0.294 |
| w18 | 12 | -0.038688 | -2.599 |
| w19 | 1 | 0.042965 | 1.544 |
| w20 | 25 | 0.004695 | -0.26 |
| w21 | 0 | None | 0.0 |
| w22 | 16 | 0.08447 | 7.061 |
| w23 | 1 | 0.031273 | 0.825 |
| w24 | 16 | 0.062124 | 4.028 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.018336 | -2.189 |
| w2 | 18 | -0.149885 | -14.347 |
| w3 | 4 | 0.001577 | -0.445 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 5 | -0.049643 | -4.706 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | 0.137627 | 3.067 |
| w9 | 2 | -0.022023 | -0.36 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 18 | 0.138373 | 13.819 |
| w15 | 3 | 0.012273 | -0.17 |
| w16 | 21 | 0.028254 | -2.218 |
| w17 | 0 | None | 0.0 |
| w18 | 11 | 0.126582 | 5.723 |
| w19 | 22 | -0.06338 | -7.709 |
| w20 | 2 | 0.01665 | -0.269 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 5 | -0.229261 | -16.564 |
| w24 | 3 | 0.022327 | -0.569 |

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
| w1 | 2 | 0.111109 | 3.985 |
| w2 | 1 | 0.106457 | 13.471 |
| w3 | 0 | -0.029995 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.04992 | -3.026 |
| w8 | 3 | 0.025029 | 0.406 |
| w9 | 7 | 0.036193 | 2.327 |
| w10 | 0 | None | 0.0 |
| w11 | 10 | 0.080406 | 2.071 |
| w12 | 0 | None | 0.0 |
| w14 | 5 | 0.020622 | 0.695 |
| w15 | 8 | 0.046837 | 2.338 |
| w16 | 22 | 0.131491 | 10.425 |
| w17 | 1 | 0.018118 | 0.388 |
| w18 | 11 | 0.089839 | 5.18 |
| w19 | 7 | -0.062996 | -3.544 |
| w20 | 9 | -0.071521 | -7.648 |
| w21 | 3 | 0.052522 | 1.557 |
| w22 | 15 | 0.082972 | 5.634 |
| w23 | 0 | None | 0.0 |
| w24 | 14 | 0.004127 | 1.571 |

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
| w2 | 28 | 0.094402 | 10.678 |
| w3 | 16 | -0.093503 | -5.098 |
| w4 | 6 | 0.068612 | 1.79 |
| w5 | 9 | -0.09807 | -7.107 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | 0.169053 | 3.485 |
| w9 | 19 | 0.045723 | 5.268 |
| w10 | 2 | 0.003704 | -0.206 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 8 | 0.087964 | 3.202 |
| w14 | 15 | 0.188604 | 16.332 |
| w15 | 4 | 0.042371 | 1.793 |
| w16 | 27 | 0.073147 | 0.755 |
| w17 | 6 | 0.037339 | 2.17 |
| w18 | 15 | 0.061569 | 4.905 |
| w19 | 25 | -0.099056 | -10.586 |
| w20 | 11 | -0.158101 | -18.027 |
| w21 | 4 | 0.007777 | -1.999 |
| w22 | 29 | -0.044448 | -5.844 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

