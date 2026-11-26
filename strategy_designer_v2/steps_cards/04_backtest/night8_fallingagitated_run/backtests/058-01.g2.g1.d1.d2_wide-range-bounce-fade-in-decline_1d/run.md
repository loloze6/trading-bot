# Backtest of 058-01.g2.g1.d1.d2_wide-range-bounce-fade-in-decline_1d

- Plan: `../../../../03_test_plan/night8_fallingagitated_run/plans/058-01.g2.g1.d1.d2_wide-range-bounce-fade-in-decline_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | 0.127341 | 0.0 |
| w2 | 8 | 0.143392 | 15.168 |
| w3 | 8 | 0.081319 | 5.451 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.048728 | -3.189 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | 0.104898 | 0.0 |
| w9 | 3 | 0.181309 | 2.101 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.041124 | 0.945 |
| w13 | 5 | 0.092383 | 5.354 |
| w14 | 9 | 0.183956 | 21.262 |
| w15 | 1 | None | -0.009 |
| w16 | 2 | 0.142504 | 5.36 |
| w17 | 0 | None | 0.0 |
| w18 | 13 | 0.063021 | 5.673 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.003857 | 0.031 |
| w21 | 0 | None | 0.0 |
| w22 | 4 | 0.073346 | 3.138 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | 0.084888 | 3.495 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | 0.098065 | 0.0 |
| w2 | 9 | 0.032055 | 3.328 |
| w3 | 6 | 0.036465 | 2.15 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | 0.193994 | 0.0 |
| w9 | 2 | 0.059803 | 1.849 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 13 | 0.046538 | 7.355 |
| w15 | 3 | 0.025631 | 0.612 |
| w16 | 3 | -0.070778 | -1.349 |
| w17 | 0 | -0.010315 | 0.0 |
| w18 | 7 | -0.060286 | -2.305 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | 0.084698 | 3.06 |
| w21 | 2 | -0.058624 | -2.205 |
| w22 | 10 | 0.073722 | 7.222 |
| w23 | 1 | 0.021772 | 0.013 |
| w24 | 4 | 0.001042 | 0.535 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 8 | 0.042898 | 5.666 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 3 | -0.057737 | -0.997 |
| w6 | 1 | -0.135216 | -3.074 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.073591 | 0.155 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.034613 | 0.556 |
| w13 | 3 | 0.059646 | 1.3 |
| w14 | 8 | 0.1513 | 14.698 |
| w15 | 3 | -0.003932 | -0.326 |
| w16 | 1 | 0.129089 | 4.625 |
| w17 | 0 | -0.009055 | 0.0 |
| w18 | 9 | -0.043717 | -1.538 |
| w19 | 0 | None | 0.0 |
| w20 | 9 | 0.094181 | 5.017 |
| w21 | 0 | None | 0.0 |
| w22 | 7 | 0.060633 | 2.472 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | -0.023531 | -0.001 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.093014 | 3.636 |
| w2 | 7 | -0.039382 | -4.088 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.082713 | -0.979 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.050979 | 0.24 |
| w9 | 2 | 0.051195 | 1.506 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 11 | 0.095992 | 11.543 |
| w15 | 1 | 0.037169 | 0.644 |
| w16 | 5 | 0.030859 | 0.488 |
| w17 | 0 | None | 0.0 |
| w18 | 5 | -0.059257 | -1.392 |
| w19 | 5 | 0.029498 | 2.26 |
| w20 | 1 | 0.017314 | 0.038 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 1 | -0.130193 | -2.136 |
| w24 | 0 | 0.006245 | 0.0 |

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
| w1 | 1 | 0.110467 | 2.126 |
| w2 | 1 | -0.031295 | 18.026 |
| w3 | 0 | -0.015238 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.03955 | -1.322 |
| w8 | 0 | 0.003667 | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 6 | -0.044179 | -2.607 |
| w12 | 0 | None | 0.0 |
| w14 | 2 | 0.043171 | 1.119 |
| w15 | 2 | -0.060042 | -2.707 |
| w16 | 5 | 0.138222 | 5.225 |
| w17 | 0 | None | 0.0 |
| w18 | 5 | 0.058064 | 2.392 |
| w19 | 3 | 0.002372 | -0.205 |
| w20 | 2 | 0.06374 | 0.197 |
| w21 | 1 | 0.112248 | 0.922 |
| w22 | 2 | -0.030152 | -1.033 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | 0.000156 | 0.638 |

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
| w2 | 9 | 0.305614 | 26.513 |
| w3 | 5 | -0.073542 | -2.441 |
| w4 | 2 | 0.014465 | 0.038 |
| w5 | 6 | -0.165006 | -8.908 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.110481 | 0.135 |
| w9 | 5 | 0.093432 | 6.1 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 4 | 0.097977 | 1.283 |
| w14 | 5 | 0.154476 | 11.377 |
| w15 | 2 | 0.098764 | 4.246 |
| w16 | 9 | 0.10121 | 3.492 |
| w17 | 1 | 0.051212 | 0.204 |
| w18 | 10 | 0.034542 | 2.183 |
| w19 | 7 | 0.022751 | 1.101 |
| w20 | 5 | 0.071423 | 3.889 |
| w21 | 1 | -0.04257 | -2.427 |
| w22 | 11 | -0.037749 | -3.832 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

