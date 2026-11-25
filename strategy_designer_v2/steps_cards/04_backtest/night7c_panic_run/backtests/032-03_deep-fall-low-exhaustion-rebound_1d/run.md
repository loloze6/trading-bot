# Backtest of 032-03_deep-fall-low-exhaustion-rebound_1d

- Plan: `../../../../03_test_plan/night7c_panic_run/plans/032-03_deep-fall-low-exhaustion-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 4 | 0.008546 | 1.928 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 8 | 0.081025 | 46.774 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | 0.161331 | 5.828 |
| w12 | 6 | 0.119625 | 0.111 |
| w13 | 18 | 0.023975 | -1.288 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | 0.007665 | 0.0 |
| w16 | 2 | 0.264057 | 6.93 |
| w17 | 4 | 0.033167 | 1.002 |
| w18 | 11 | 0.115461 | 6.29 |
| w19 | 5 | 0.056803 | 6.296 |
| w20 | 13 | 0.01072 | 0.026 |
| w21 | 2 | -0.013762 | 2.291 |
| w22 | 7 | -0.014413 | -1.751 |
| w23 | 0 | None | 0.0 |
| w24 | 7 | -0.062699 | -19.156 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.081763 | 5.555 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 5 | 0.156383 | 2.134 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 9 | 0.140612 | 3.226 |
| w13 | 19 | -0.065413 | -11.288 |
| w14 | 0 | None | 0.0 |
| w15 | 5 | -0.021462 | 5.578 |
| w16 | 5 | 0.169459 | -3.669 |
| w17 | 4 | 0.206321 | 1.652 |
| w18 | 8 | 0.188882 | 13.068 |
| w19 | 2 | 0.13918 | 2.667 |
| w20 | 13 | 0.153189 | 7.849 |
| w21 | 2 | 0.070768 | 1.038 |
| w22 | 17 | 0.11662 | -12.774 |
| w23 | 0 | None | 0.0 |
| w24 | 10 | -0.049791 | -14.486 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 3 | -0.096691 | -0.84 |
| w5 | 6 | 0.008094 | 2.72 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | 0.122274 | 0.0 |
| w12 | 13 | 0.063881 | -1.933 |
| w13 | 16 | -0.037098 | -4.904 |
| w14 | 0 | None | 0.0 |
| w15 | 15 | 0.057896 | -4.249 |
| w16 | 5 | 0.01523 | -4.074 |
| w17 | 6 | 0.036876 | -0.332 |
| w18 | 8 | 0.168849 | 10.078 |
| w19 | 2 | 0.059313 | 1.425 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | 0.008639 | 0.0 |
| w22 | 6 | 0.021955 | -14.275 |
| w23 | 0 | None | 0.0 |
| w24 | 12 | 0.104433 | 24.028 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 3 | -0.116668 | -4.922 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.028319 | -0.32 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 4 | 0.11589 | 9.869 |
| w12 | 6 | 0.156897 | 2.607 |
| w14 | 0 | None | 0.0 |
| w15 | 5 | -0.004018 | 2.532 |
| w16 | 6 | -0.105729 | -17.316 |
| w17 | 4 | 0.118121 | 4.362 |
| w18 | 8 | 0.372728 | 7.882 |
| w19 | 11 | 0.282075 | 8.726 |
| w20 | 2 | 0.218827 | 1.311 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | 0.165377 | 2.628 |
| w23 | 13 | -0.017454 | 1.927 |
| w24 | 0 | None | 0.0 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 7 | -0.039786 | 3.507 |
| w6 | 4 | 0.026441 | 1.444 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | 0.052485 | 1.578 |
| w14 | 0 | None | 0.0 |
| w15 | 9 | 0.005762 | 0.221 |
| w16 | 6 | 0.255532 | -17.226 |
| w17 | 11 | 0.115192 | 0.318 |
| w18 | 5 | 0.084051 | 9.441 |
| w19 | 12 | 0.01674 | -12.207 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 8 | 0.071376 | 13.019 |
| w23 | 2 | 0.074484 | 6.34 |
| w24 | 2 | 0.137334 | 13.118 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | None | -0.084 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.063014 | 0.017 |
| w13 | 7 | 0.088254 | -3.748 |
| w14 | 0 | None | 0.0 |
| w15 | 5 | 0.001026 | 0.309 |
| w16 | 7 | -0.128744 | -0.547 |
| w17 | 14 | 0.21353 | 35.882 |
| w18 | 9 | 0.248329 | 10.858 |
| w19 | 4 | -0.096856 | -18.337 |
| w20 | 0 | None | 0.0 |
| w21 | 6 | 0.040326 | 4.473 |
| w22 | 10 | -0.07478 | -8.13 |
| w23 | 3 | 0.058033 | -0.527 |
| w24 | 0 | -0.01357 | 0.0 |

