# Backtest of 058-01.g2.g1.g1.d1.d1_agitated-decline-rejected-rally-fade_1d

- Plan: `../../../../03_test_plan/night8_fallingagitated_run/plans/058-01.g2.g1.g1.d1.d1_agitated-decline-rejected-rally-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.131334 | 0.767 |
| w2 | 10 | 0.122934 | 11.672 |
| w3 | 5 | -0.010684 | -0.055 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.048728 | -3.013 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.10362 | 2.918 |
| w9 | 4 | -0.085266 | -1.418 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | -0.025499 | -0.128 |
| w13 | 9 | 0.140725 | 4.287 |
| w14 | 13 | 0.213351 | 13.44 |
| w15 | 0 | None | 0.0 |
| w16 | 10 | 0.141984 | 5.068 |
| w17 | 0 | None | 0.0 |
| w18 | 18 | 0.132254 | 6.318 |
| w19 | 0 | None | 0.0 |
| w20 | 5 | -0.011327 | -0.355 |
| w21 | 0 | None | 0.0 |
| w22 | 13 | 0.024428 | 0.047 |
| w23 | 0 | None | 0.0 |
| w24 | 7 | -0.000702 | 0.154 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.075757 | -1.017 |
| w2 | 9 | 0.007418 | 0.941 |
| w3 | 5 | 0.009861 | 0.336 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 5 | 0.156517 | 2.051 |
| w9 | 3 | 0.040208 | 0.784 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 22 | 0.097761 | 10.497 |
| w15 | 3 | -0.000169 | -0.144 |
| w16 | 8 | 0.106414 | 1.886 |
| w17 | 1 | -0.029217 | -0.365 |
| w18 | 7 | 0.015638 | 0.087 |
| w19 | 0 | None | 0.0 |
| w20 | 12 | 0.106334 | 3.947 |
| w21 | 6 | 0.000479 | -0.761 |
| w22 | 21 | 0.068113 | 4.947 |
| w23 | 2 | 0.020045 | -0.064 |
| w24 | 7 | -0.069336 | -1.353 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 12 | 0.173987 | 11.89 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 5 | -0.019468 | -0.534 |
| w6 | 1 | -0.135216 | -2.985 |
| w7 | 0 | None | 0.0 |
| w8 | 4 | 0.036018 | -0.118 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | -0.035714 | 0.0 |
| w13 | 4 | -0.037776 | -0.569 |
| w14 | 13 | 0.140018 | 10.684 |
| w15 | 4 | 0.031386 | 0.933 |
| w16 | 8 | 0.167177 | 3.53 |
| w17 | 0 | -0.009055 | 0.0 |
| w18 | 7 | -0.043223 | -1.561 |
| w19 | 0 | None | 0.0 |
| w20 | 9 | 0.051233 | 1.245 |
| w21 | 0 | None | 0.0 |
| w22 | 12 | 0.090233 | 3.901 |
| w23 | 1 | 0.031273 | 0.289 |
| w24 | 8 | -0.049235 | -0.728 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.118028 | 4.379 |
| w2 | 9 | -0.045607 | -2.07 |
| w3 | 1 | 0.020986 | 0.088 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.099555 | -1.806 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.091411 | 0.197 |
| w9 | 2 | 0.057307 | 1.52 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 12 | 0.148453 | 11.511 |
| w15 | 3 | 0.009172 | -0.105 |
| w16 | 10 | 0.164795 | 4.332 |
| w17 | 0 | None | 0.0 |
| w18 | 5 | -0.008834 | -0.424 |
| w19 | 10 | -0.011739 | -1.557 |
| w20 | 2 | 0.007985 | -0.154 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 4 | -0.242733 | -10.916 |
| w24 | 2 | 0.016031 | -0.325 |

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
| w1 | 1 | 0.0449 | 0.276 |
| w2 | 1 | -0.042288 | 13.633 |
| w3 | 0 | 0.023174 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.013003 | -0.345 |
| w8 | 2 | 0.043527 | 0.292 |
| w9 | 3 | 0.084069 | 1.321 |
| w10 | 0 | None | 0.0 |
| w11 | 5 | -0.033904 | -1.741 |
| w12 | 0 | None | 0.0 |
| w14 | 2 | 0.020108 | -0.119 |
| w15 | 3 | -0.041811 | -1.777 |
| w16 | 13 | 0.211216 | 6.44 |
| w17 | 0 | None | 0.0 |
| w18 | 7 | -0.002651 | 0.012 |
| w19 | 1 | -0.003383 | -0.3 |
| w20 | 3 | 0.067003 | 1.449 |
| w21 | 1 | 0.077992 | 0.185 |
| w22 | 8 | 0.069128 | 1.558 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | 0.045419 | 1.09 |

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
| w2 | 13 | 0.300583 | 18.733 |
| w3 | 4 | -0.043982 | -0.564 |
| w4 | 2 | -0.003981 | -0.156 |
| w5 | 4 | -0.28502 | -10.322 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 4 | 0.155119 | 1.627 |
| w9 | 9 | 0.063816 | 3.083 |
| w10 | 1 | -0.015115 | -0.081 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 4 | 0.123228 | 1.306 |
| w14 | 7 | 0.202672 | 6.795 |
| w15 | 3 | 0.103435 | 4.458 |
| w16 | 10 | 0.039037 | 0.554 |
| w17 | 1 | -0.128208 | -2.402 |
| w18 | 7 | 0.03427 | 0.242 |
| w19 | 6 | -0.045309 | -3.108 |
| w20 | 1 | -0.013871 | -0.258 |
| w21 | 1 | -0.022999 | -1.659 |
| w22 | 15 | -0.209436 | -12.021 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

