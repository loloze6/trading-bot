# Backtest of 058-02_quiet-volume-fall-continues_1d

- Plan: `../../../../03_test_plan/night8_fallingcalm_run/plans/058-02_quiet-volume-fall-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.012869 | 6.925 |
| w2 | 3 | 0.188715 | 28.639 |
| w3 | 10 | 0.015239 | -8.465 |
| w4 | 3 | -0.001376 | -0.753 |
| w5 | 7 | -0.057047 | -6.799 |
| w6 | 1 | 0.097483 | 4.896 |
| w7 | 18 | -0.022852 | 0.141 |
| w8 | 6 | 0.047964 | 1.014 |
| w9 | 31 | -0.133797 | -23.62 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | 0.034784 | -0.778 |
| w12 | 9 | -0.014375 | -0.566 |
| w13 | 6 | -0.021149 | -0.466 |
| w14 | 8 | 0.176071 | 45.346 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | -0.096439 | -5.612 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.083692 | -6.826 |
| w21 | 0 | None | 0.0 |
| w22 | 3 | -0.022724 | -7.106 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | 0.17495 | 7.5 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | 0.018772 | 7.94 |
| w2 | 2 | -0.088467 | 7.566 |
| w3 | 11 | -0.006286 | -0.371 |
| w4 | 3 | -0.077838 | -2.23 |
| w5 | 8 | -0.024235 | -3.885 |
| w6 | 20 | 0.032333 | -5.524 |
| w7 | 23 | 0.006688 | 19.152 |
| w8 | 0 | None | 0.0 |
| w9 | 18 | -0.054691 | 0.513 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.022867 | 0.831 |
| w13 | 7 | 0.080488 | 3.939 |
| w14 | 9 | 0.187745 | 25.834 |
| w15 | 8 | 0.086843 | 14.849 |
| w16 | 6 | -0.041164 | -14.475 |
| w17 | 2 | -0.057442 | -1.401 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | -0.003959 | -0.672 |
| w22 | 3 | -0.009176 | 3.312 |
| w23 | 0 | None | 0.0 |
| w24 | 13 | 0.047169 | 6.01 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 41 | -0.070171 | 7.133 |
| w2 | 3 | 0.22342 | 15.09 |
| w3 | 9 | 0.022566 | 0.65 |
| w4 | 3 | -0.114586 | -10.701 |
| w5 | 4 | -0.089777 | 0.317 |
| w6 | 9 | 0.080374 | 5.614 |
| w7 | 29 | -0.01091 | 31.955 |
| w8 | 0 | None | 0.0 |
| w9 | 41 | -0.081111 | 6.28 |
| w10 | 6 | -0.020145 | -4.394 |
| w11 | 0 | None | 0.0 |
| w12 | 7 | -0.006461 | -0.408 |
| w13 | 18 | -0.056279 | -7.219 |
| w14 | 20 | 0.102977 | 26.49 |
| w15 | 8 | 0.072731 | 3.178 |
| w16 | 4 | -0.05586 | -10.262 |
| w17 | 5 | -0.00164 | -3.203 |
| w18 | 11 | 0.02936 | -2.327 |
| w19 | 2 | -0.110343 | -11.13 |
| w20 | 13 | 0.029275 | 7.917 |
| w21 | 6 | -0.021182 | -4.753 |
| w22 | 1 | 0.132707 | 6.468 |
| w23 | 0 | -0.116672 | 0.0 |
| w24 | 17 | -0.042583 | -2.895 |

- XMRUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.165022 | -6.953 |
| w2 | 0 | None | 0.0 |
| w3 | 12 | -0.129259 | -4.968 |
| w4 | 7 | -0.265699 | -12.378 |
| w5 | 8 | -0.104763 | -7.003 |
| w6 | 1 | -0.005066 | -1.933 |
| w8 | 10 | 0.058829 | -1.789 |
| w9 | 26 | -0.076188 | 5.801 |
| w10 | 0 | -0.308113 | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 21 | -0.048507 | -5.097 |
| w14 | 5 | 0.122169 | 34.149 |
| w15 | 5 | 0.031178 | 3.393 |
| w16 | 2 | -0.125166 | -22.969 |
| w17 | 0 | None | 0.0 |
| w18 | 3 | -0.045445 | -2.283 |
| w19 | 0 | None | 0.0 |
| w20 | 5 | -0.084893 | -3.659 |
| w21 | 7 | -0.121771 | -10.452 |
| w22 | 4 | -0.113482 | -6.965 |
| w23 | 7 | 0.061963 | 8.303 |
| w24 | 0 | None | 0.0 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 483 warm-up bars -- required_bars=494. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=494. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 21 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | 0.040405 | 14.452 |
| w2 | 6 | -0.02069 | 22.442 |
| w3 | 0 | 0.013363 | 0.0 |
| w4 | 0 | -0.011516 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 5 | -0.083424 | -2.028 |
| w8 | 20 | -0.050602 | -3.732 |
| w9 | 21 | 0.061442 | 22.411 |
| w10 | 6 | -0.110921 | -17.002 |
| w11 | 0 | None | 0.0 |
| w12 | 8 | -0.046269 | -0.33 |
| w15 | 19 | 0.040996 | 11.868 |
| w16 | 4 | -0.123118 | -18.565 |
| w17 | 3 | -0.051358 | -2.826 |
| w18 | 7 | 0.038461 | -2.309 |
| w19 | 13 | -0.088163 | -10.087 |
| w20 | 15 | 0.122938 | 25.505 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.069334 | -0.851 |
| w23 | 0 | -0.020124 | 0.0 |
| w24 | 29 | -0.044358 | 11.916 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=494. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=494. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 470 warm-up bars -- required_bars=494. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.037952 | -7.193 |
| w2 | 10 | -0.147744 | -15.418 |
| w3 | 36 | 0.053096 | 24.748 |
| w4 | 10 | -0.148786 | -13.006 |
| w5 | 15 | 0.00661 | 20.051 |
| w6 | 8 | -0.059717 | -9.538 |
| w7 | 17 | -0.091396 | -12.619 |
| w8 | 14 | 0.005534 | -1.593 |
| w9 | 25 | -0.089366 | -11.426 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 6 | -0.07766 | -5.699 |
| w14 | 25 | 0.045024 | 11.152 |
| w15 | 4 | 0.076106 | 17.469 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | -0.0611 | -7.098 |
| w18 | 10 | -0.067158 | -7.648 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | 0.031995 | -6.81 |
| w21 | 6 | -0.014057 | -0.495 |
| w22 | 2 | -0.180561 | -2.062 |
| w23 | 12 | -0.098907 | -8.953 |
| w24 | 0 | None | 0.0 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=494. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

