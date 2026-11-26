# Backtest of 058-01_choppy-agitated-weekly-rise-continues_1d

- Plan: `../../../../03_test_plan/night8_choppyagitated_run/plans/058-01_choppy-agitated-weekly-rise-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.009713 | -7.582 |
| w2 | 0 | None | 0.0 |
| w3 | 4 | -0.234457 | -12.919 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 5 | 0.011411 | -1.322 |
| w10 | 2 | 0.036189 | 6.106 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | 0.030415 | 0.0 |
| w13 | 5 | -0.007516 | 4.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | -0.038478 | 0.0 |
| w16 | 5 | -0.039774 | -2.2 |
| w17 | 4 | -0.066728 | -0.185 |
| w18 | 4 | -0.221348 | -8.419 |
| w19 | 6 | 0.086224 | 23.927 |
| w20 | 26 | -0.015976 | 5.487 |
| w21 | 8 | -0.017257 | 8.428 |
| w22 | 2 | -0.032003 | -6.538 |
| w23 | 3 | -0.021178 | 3.159 |
| w24 | 5 | -0.001494 | -1.927 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 6 | 0.024805 | 3.511 |
| w3 | 4 | 0.006216 | 0.699 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | -0.031056 | 0.368 |
| w9 | 1 | 0.008806 | -2.941 |
| w10 | 3 | -0.060854 | -0.392 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | -0.024651 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.008666 | -3.702 |
| w16 | 3 | -0.055623 | -0.11 |
| w17 | 3 | -0.045922 | -1.946 |
| w18 | 0 | -0.100917 | 0.0 |
| w19 | 6 | 0.027577 | 14.767 |
| w20 | 8 | 0.039258 | 11.261 |
| w21 | 0 | None | 0.0 |
| w22 | 3 | -0.033811 | -3.13 |
| w23 | 2 | 0.120412 | 12.492 |
| w24 | 3 | -0.037604 | -1.844 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | 0.174671 | 18.405 |
| w4 | 7 | -0.037363 | 8.401 |
| w5 | 4 | 0.021472 | -0.966 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.081102 | 0.501 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 4 | 0.077947 | 0.211 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | -0.074241 | -1.791 |
| w16 | 2 | -0.014689 | -1.501 |
| w17 | 0 | -0.002405 | 0.0 |
| w18 | 0 | -0.036092 | 0.0 |
| w19 | 10 | -0.072703 | -6.455 |
| w20 | 4 | -0.061168 | -0.953 |
| w21 | 8 | -0.044457 | -5.878 |
| w22 | 7 | 0.015018 | -4.53 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | -0.043725 | -3.731 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.111749 | -3.919 |
| w2 | 8 | -0.01697 | 5.16 |
| w3 | 9 | 0.032963 | 5.083 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 4 | 0.050603 | 1.982 |
| w12 | 8 | 0.070718 | 4.389 |
| w14 | 3 | 0.048903 | -0.178 |
| w15 | 6 | 0.045031 | -2.809 |
| w16 | 2 | 0.120614 | 1.846 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | 0.03513 | -0.653 |
| w19 | 22 | -0.071687 | -18.887 |
| w20 | 12 | -0.051799 | 6.185 |
| w21 | 12 | -0.033654 | 8.923 |
| w22 | 6 | 0.016867 | 4.605 |
| w23 | 2 | -0.237409 | -8.399 |
| w24 | 5 | -0.052692 | -5.885 |

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
| w1 | 1 | -0.038189 | -2.283 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | 0.357506 | 0.0 |
| w4 | 0 | 0.201581 | 0.0 |
| w5 | 5 | -0.000136 | -1.86 |
| w6 | 1 | -0.048796 | -0.052 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | 0.02807 | -1.843 |
| w10 | 0 | None | 0.0 |
| w11 | 9 | 0.02171 | 2.074 |
| w12 | 0 | None | 0.0 |
| w14 | 2 | 0.301119 | 14.312 |
| w15 | 0 | None | 0.0 |
| w16 | 9 | -0.016079 | -1.606 |
| w17 | 2 | 0.001577 | 1.033 |
| w18 | 1 | -0.103951 | -0.623 |
| w19 | 8 | -0.013951 | 0.372 |
| w20 | 2 | 0.285723 | 42.077 |
| w21 | 4 | -0.071002 | -3.086 |
| w22 | 10 | 0.002098 | -3.998 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | -0.117285 | -9.147 |

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
| w1 | 7 | -0.065787 | 8.017 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 6 | -0.064922 | -12.956 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 1 | -0.264663 | -11.853 |
| w10 | 2 | -0.084245 | -0.321 |
| w11 | 0 | None | 0.0 |
| w12 | 9 | 0.038719 | -1.209 |
| w13 | 2 | -0.008212 | -4.479 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.010774 | -0.754 |
| w16 | 4 | 0.152394 | 77.757 |
| w17 | 6 | -0.066895 | -2.777 |
| w18 | 3 | 0.036483 | -0.581 |
| w19 | 9 | 0.068882 | 17.703 |
| w20 | 7 | 0.152137 | 21.104 |
| w21 | 6 | -0.05246 | -1.19 |
| w22 | 6 | 0.006706 | -3.003 |
| w23 | 2 | -0.00946 | 6.021 |
| w24 | 2 | -0.005767 | 8.645 |

