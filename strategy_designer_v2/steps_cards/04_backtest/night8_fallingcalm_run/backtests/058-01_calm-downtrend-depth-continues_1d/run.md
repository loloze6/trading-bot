# Backtest of 058-01_calm-downtrend-depth-continues_1d

- Plan: `../../../../03_test_plan/night8_fallingcalm_run/plans/058-01_calm-downtrend-depth-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.000116 | 4.77 |
| w2 | 3 | 0.19165 | 27.551 |
| w3 | 15 | 0.044141 | -9.39 |
| w4 | 2 | -0.001441 | -0.377 |
| w5 | 12 | -0.086531 | -10.214 |
| w6 | 2 | 0.100244 | 2.332 |
| w7 | 17 | -0.015662 | 1.172 |
| w8 | 4 | 0.045313 | 0.547 |
| w9 | 29 | -0.118423 | -21.655 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | 0.034784 | -0.772 |
| w12 | 9 | -0.011603 | 0.339 |
| w13 | 11 | -0.020705 | -2.064 |
| w14 | 14 | 0.138701 | 38.437 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | -0.097335 | -5.406 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.083692 | -6.826 |
| w21 | 0 | None | 0.0 |
| w22 | 3 | -0.022724 | -9.502 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | 0.204714 | 16.137 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | -0.004064 | 3.618 |
| w2 | 2 | -0.088467 | 7.566 |
| w3 | 16 | -0.006966 | 0.076 |
| w4 | 3 | -0.078451 | -2.009 |
| w5 | 10 | -0.070815 | -7.501 |
| w6 | 17 | 0.030366 | -5.121 |
| w7 | 22 | 0.008602 | 20.271 |
| w8 | 0 | None | 0.0 |
| w9 | 20 | -0.035333 | 7.227 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.020557 | 0.843 |
| w13 | 15 | 0.053473 | 3.567 |
| w14 | 11 | 0.212499 | 48.526 |
| w15 | 8 | 0.06458 | 8.467 |
| w16 | 5 | -0.041405 | -6.381 |
| w17 | 2 | -0.057376 | -1.854 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | -0.003574 | -0.675 |
| w22 | 5 | -0.005523 | 5.178 |
| w23 | 0 | None | 0.0 |
| w24 | 14 | 0.06828 | 10.393 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 39 | -0.092346 | 1.966 |
| w2 | 3 | 0.265198 | 15.048 |
| w3 | 10 | 0.022162 | 0.295 |
| w4 | 2 | -0.110715 | -6.248 |
| w5 | 4 | -0.077242 | -0.02 |
| w6 | 6 | 0.080197 | 4.721 |
| w7 | 33 | -0.088738 | 8.706 |
| w8 | 0 | None | 0.0 |
| w9 | 34 | -0.079744 | 6.517 |
| w10 | 4 | -0.022693 | -1.885 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | -0.007516 | -0.8 |
| w13 | 16 | -0.048933 | -7.155 |
| w14 | 18 | 0.095455 | 36.192 |
| w15 | 8 | 0.068638 | 3.692 |
| w16 | 2 | -0.055117 | -3.16 |
| w17 | 4 | -0.003831 | -2.564 |
| w18 | 3 | 0.026216 | -1.33 |
| w19 | 3 | -0.110343 | -17.903 |
| w20 | 17 | 0.024316 | 7.49 |
| w21 | 6 | -0.021205 | -3.323 |
| w22 | 2 | 0.107994 | 9.299 |
| w23 | 0 | -0.116672 | 0.0 |
| w24 | 15 | -0.038777 | -2.21 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.15163 | -4.203 |
| w2 | 0 | None | 0.0 |
| w3 | 17 | -0.085177 | -4.83 |
| w4 | 9 | -0.270639 | -11.436 |
| w5 | 8 | -0.105396 | -9.055 |
| w6 | 3 | -0.01857 | -2.643 |
| w7 | 37 | -0.167343 | -10.24 |
| w8 | 3 | 0.057822 | 0.764 |
| w9 | 41 | -0.07809 | 3.265 |
| w10 | 0 | -0.308113 | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 21 | -0.011598 | -1.698 |
| w14 | 6 | 0.137374 | 35.498 |
| w15 | 6 | 0.035732 | 2.516 |
| w16 | 2 | -0.127735 | -18.423 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | -0.045516 | -1.395 |
| w19 | 0 | None | 0.0 |
| w20 | 8 | -0.070971 | -4.057 |
| w21 | 7 | -0.128104 | -9.647 |
| w22 | 4 | -0.123728 | -6.67 |
| w23 | 6 | 0.07215 | 17.216 |
| w24 | 0 | None | 0.0 |

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
| w1 | 20 | 0.028452 | 13.717 |
| w2 | 5 | 0.02156 | 20.595 |
| w3 | 0 | 0.013938 | 0.0 |
| w4 | 0 | -0.008989 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.090336 | -1.098 |
| w8 | 17 | -0.077946 | -3.726 |
| w9 | 28 | 0.041943 | 8.801 |
| w10 | 6 | -0.120335 | -20.206 |
| w11 | 0 | None | 0.0 |
| w12 | 8 | -0.031096 | 0.3 |
| w14 | 22 | -0.057242 | -40.438 |
| w15 | 19 | 0.032056 | 6.229 |
| w16 | 2 | -0.122307 | -6.865 |
| w17 | 2 | -0.04049 | -1.291 |
| w18 | 7 | 0.033923 | 0.324 |
| w19 | 13 | -0.07876 | -10.6 |
| w20 | 9 | 0.130213 | 18.385 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.069772 | -1.65 |
| w23 | 0 | -0.020124 | 0.0 |
| w24 | 31 | -0.069239 | 15.491 |

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
| w1 | 21 | -0.025007 | -5.11 |
| w2 | 7 | -0.136242 | -5.52 |
| w3 | 32 | 0.108485 | 14.302 |
| w4 | 11 | -0.107338 | -14.943 |
| w5 | 21 | 0.02437 | 19.489 |
| w6 | 6 | -0.063198 | -6.802 |
| w7 | 21 | -0.112479 | -11.761 |
| w8 | 11 | 0.001457 | -0.735 |
| w9 | 23 | -0.092148 | -11.67 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.076316 | -1.261 |
| w13 | 13 | 0.027283 | 6.47 |
| w14 | 28 | 0.118151 | 18.638 |
| w15 | 3 | 0.06548 | 8.714 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | -0.076122 | -9.493 |
| w18 | 6 | -0.068695 | -2.284 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | 0.030208 | -6.524 |
| w21 | 4 | -0.024258 | -0.138 |
| w22 | 2 | -0.180561 | -6.125 |
| w23 | 15 | -0.103077 | -15.567 |
| w24 | 0 | None | 0.0 |

