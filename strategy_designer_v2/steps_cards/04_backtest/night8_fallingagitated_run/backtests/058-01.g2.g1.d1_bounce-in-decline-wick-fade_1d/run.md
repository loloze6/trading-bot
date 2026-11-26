# Backtest of 058-01.g2.g1.d1_bounce-in-decline-wick-fade_1d

- Plan: `../../../../03_test_plan/night8_fallingagitated_run/plans/058-01.g2.g1.d1_bounce-in-decline-wick-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.131334 | 0.767 |
| w2 | 8 | 0.090338 | 8.004 |
| w3 | 5 | 0.016916 | 0.434 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.048728 | -3.013 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.202327 | 0.81 |
| w9 | 2 | 0.110094 | 1.089 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.050165 | 0.539 |
| w13 | 5 | 0.148928 | 4.106 |
| w14 | 10 | 0.134502 | 8.88 |
| w15 | 1 | None | -0.01 |
| w16 | 5 | 0.100061 | 2.541 |
| w17 | 0 | None | 0.0 |
| w18 | 13 | 0.116217 | 6.619 |
| w19 | 0 | None | 0.0 |
| w20 | 5 | -0.051454 | -1.176 |
| w21 | 0 | None | 0.0 |
| w22 | 5 | 0.076295 | 1.961 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | 0.06809 | 1.203 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | 0.098065 | 0.0 |
| w2 | 7 | -0.002627 | -0.878 |
| w3 | 5 | 0.035644 | 1.171 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.320134 | 1.622 |
| w9 | 3 | 0.046118 | 1.031 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 13 | 0.020369 | 2.768 |
| w15 | 2 | 0.030154 | 0.329 |
| w16 | 5 | -0.027092 | -0.898 |
| w17 | 2 | -0.026495 | -0.398 |
| w18 | 6 | -0.015497 | -0.327 |
| w19 | 0 | None | 0.0 |
| w20 | 8 | 0.076569 | 3.081 |
| w21 | 2 | -0.064699 | -1.9 |
| w22 | 13 | 0.018288 | 1.921 |
| w23 | 1 | 0.021772 | 0.014 |
| w24 | 5 | -0.036238 | -0.572 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 7 | 0.151489 | 10.185 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 3 | -0.048393 | -0.87 |
| w6 | 1 | -0.135216 | -2.985 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | 0.12881 | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | 0.015749 | 0.0 |
| w13 | 3 | 0.087823 | 2.083 |
| w14 | 8 | 0.137368 | 11.012 |
| w15 | 4 | -0.028988 | -0.66 |
| w16 | 2 | 0.134736 | 1.702 |
| w17 | 0 | -0.009055 | 0.0 |
| w18 | 7 | -0.044814 | -1.595 |
| w19 | 0 | None | 0.0 |
| w20 | 7 | -0.085016 | -3.123 |
| w21 | 0 | None | 0.0 |
| w22 | 10 | 0.079217 | 3.298 |
| w23 | 0 | None | 0.0 |
| w24 | 7 | -0.041437 | -0.734 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.117284 | 4.343 |
| w2 | 6 | -0.053123 | -2.601 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.082713 | -1.413 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.029116 | 0.215 |
| w9 | 2 | 0.057307 | 1.52 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 10 | 0.082646 | 6.435 |
| w15 | 3 | 0.009172 | -0.105 |
| w16 | 4 | 0.036068 | 0.456 |
| w17 | 0 | None | 0.0 |
| w18 | 3 | -0.077525 | -0.776 |
| w19 | 6 | 0.013596 | 0.844 |
| w20 | 0 | 0.017314 | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.130193 | -3.237 |
| w24 | 3 | 0.000654 | -0.476 |

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
| w1 | 1 | 0.110467 | 1.706 |
| w2 | 1 | -0.121649 | 13.633 |
| w3 | 0 | 0.027157 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.040077 | -1.075 |
| w8 | 1 | 0.003667 | 0.017 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 5 | -0.073586 | -2.652 |
| w12 | 0 | None | 0.0 |
| w14 | 1 | 0.002479 | -0.276 |
| w15 | 2 | -0.062688 | -1.935 |
| w16 | 5 | 0.071799 | 1.516 |
| w17 | 0 | None | 0.0 |
| w18 | 7 | -0.004221 | -0.0 |
| w19 | 2 | -0.001528 | -0.354 |
| w20 | 1 | 0.062234 | -0.147 |
| w21 | 0 | 0.112248 | 0.0 |
| w22 | 3 | 0.018321 | 0.224 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | -0.103753 | -1.908 |

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
| w2 | 7 | 0.284457 | 15.721 |
| w3 | 3 | -0.124989 | -1.614 |
| w4 | 1 | 0.023462 | 0.16 |
| w5 | 4 | -0.249575 | -7.563 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 3 | 0.145994 | 1.263 |
| w9 | 6 | 0.061355 | 2.433 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 4 | 0.085807 | 1.266 |
| w14 | 6 | 0.071737 | 3.338 |
| w15 | 3 | 0.103435 | 4.458 |
| w16 | 9 | 0.068048 | 1.542 |
| w17 | 0 | 0.051212 | 0.0 |
| w18 | 9 | 0.082693 | 2.679 |
| w19 | 4 | 0.017283 | 0.631 |
| w20 | 2 | 0.007378 | -0.306 |
| w21 | 1 | -0.04257 | -2.631 |
| w22 | 11 | -0.033263 | -1.288 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

