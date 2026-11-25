# Backtest of 034-01.d2_falling-agitated-low-close-rebound_1d

- Plan: `../../../../03_test_plan/night7_steadydecline_run/plans/034-01.d2_falling-agitated-low-close-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.025751 | 0.996 |
| w2 | 45 | -0.032347 | -2.533 |
| w3 | 35 | 0.148724 | 8.539 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | 0.098868 | -3.53 |
| w7 | 0 | None | 0.0 |
| w8 | 12 | 0.120397 | 0.606 |
| w9 | 13 | -0.080548 | -1.485 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.074628 | 1.147 |
| w13 | 38 | 0.073384 | 0.306 |
| w14 | 32 | 0.251535 | 7.354 |
| w15 | 3 | -0.078691 | -0.333 |
| w16 | 36 | 0.16137 | 5.592 |
| w17 | 0 | None | 0.0 |
| w18 | 51 | -0.028233 | -3.45 |
| w19 | 0 | None | 0.0 |
| w20 | 15 | 0.130254 | 4.527 |
| w21 | 0 | None | 0.0 |
| w22 | 32 | 0.213958 | 7.937 |
| w23 | 0 | None | 0.0 |
| w24 | 25 | 0.034288 | 0.688 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.065848 | -2.24 |
| w2 | 47 | -0.098118 | -7.58 |
| w3 | 15 | 0.124462 | 2.241 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 14 | 0.041334 | -0.372 |
| w9 | 13 | 0.097144 | 1.813 |
| w10 | 1 | 0.108835 | 0.557 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 57 | 0.105983 | 2.572 |
| w15 | 13 | 0.126095 | 2.399 |
| w16 | 34 | 0.142601 | 5.082 |
| w17 | 2 | 0.023732 | 0.211 |
| w18 | 22 | -0.046063 | -2.511 |
| w19 | 1 | None | -0.009 |
| w20 | 41 | 0.139027 | 4.889 |
| w21 | 17 | 0.024207 | 0.343 |
| w22 | 50 | 0.201538 | 8.882 |
| w23 | 3 | 0.126496 | 9.608 |
| w24 | 18 | -0.025001 | -2.256 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 54 | 0.065497 | 3.77 |
| w3 | 1 | 0.393083 | 2.226 |
| w4 | 2 | 0.068518 | 0.615 |
| w5 | 15 | -0.016631 | -1.348 |
| w6 | 2 | 0.022324 | -0.166 |
| w7 | 0 | None | 0.0 |
| w8 | 12 | -0.0043 | 6.4 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.071858 | 0.827 |
| w13 | 13 | -0.066904 | -1.631 |
| w14 | 33 | 0.057237 | -4.998 |
| w15 | 17 | 0.140273 | 3.429 |
| w16 | 31 | 0.258245 | 8.914 |
| w17 | 6 | 0.029939 | 0.621 |
| w18 | 31 | 0.015729 | -1.231 |
| w19 | 1 | 0.04743 | 0.414 |
| w20 | 45 | 0.055934 | 2.072 |
| w21 | 1 | 0.047127 | 0.368 |
| w22 | 30 | 0.116002 | 2.866 |
| w23 | 2 | 0.077306 | 0.619 |
| w24 | 29 | -0.113648 | -3.686 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.132613 | -6.121 |
| w2 | 34 | -0.04774 | -3.373 |
| w3 | 4 | 0.119466 | 1.707 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 6 | -0.033053 | -0.267 |
| w7 | 0 | None | 0.0 |
| w8 | 13 | 0.103818 | 0.72 |
| w9 | 2 | 0.020057 | -0.465 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 38 | 0.175571 | 1.693 |
| w15 | 8 | 0.07318 | 1.268 |
| w16 | 32 | 0.188507 | 6.774 |
| w17 | 0 | None | 0.0 |
| w18 | 32 | 0.141647 | 5.465 |
| w19 | 33 | 0.081418 | 4.395 |
| w20 | 4 | 0.246018 | 3.331 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 10 | -0.059465 | -2.289 |
| w24 | 7 | 0.044959 | 1.089 |

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
| w1 | 3 | 0.081462 | 0.903 |
| w2 | 0 | 0.046918 | 0.0 |
| w3 | 0 | -0.033407 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | -0.027351 | 0.0 |
| w8 | 7 | 0.042628 | 0.211 |
| w9 | 8 | 0.049082 | 1.703 |
| w10 | 0 | None | 0.0 |
| w11 | 17 | 0.080434 | 5.387 |
| w12 | 0 | None | 0.0 |
| w14 | 7 | -0.024912 | -1.119 |
| w15 | 7 | 0.089889 | 2.25 |
| w16 | 38 | 0.237145 | 12.025 |
| w17 | 2 | 0.017105 | 17.366 |
| w18 | 23 | 0.050316 | 2.499 |
| w19 | 13 | -0.064573 | -3.315 |
| w20 | 12 | -0.004487 | -0.702 |
| w21 | 6 | 0.031716 | 9.13 |
| w22 | 30 | 0.099064 | 2.998 |
| w23 | 0 | None | 0.0 |
| w24 | 18 | -0.026628 | -0.88 |

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
| w1 | 1 | 0.021729 | 0.241 |
| w2 | 38 | 0.02731 | 0.698 |
| w3 | 20 | 0.023261 | 0.661 |
| w4 | 9 | 0.04767 | 0.985 |
| w5 | 19 | 0.012332 | 0.151 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | -0.063448 | -0.485 |
| w8 | 13 | 0.229 | 2.35 |
| w9 | 31 | -0.042208 | -2.117 |
| w10 | 4 | -0.057716 | 3.32 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 15 | 0.115917 | 2.768 |
| w14 | 35 | 0.165917 | 5.569 |
| w15 | 13 | -0.056273 | -1.69 |
| w16 | 42 | 0.067028 | 3.31 |
| w17 | 14 | 0.213112 | 4.782 |
| w18 | 27 | 0.021679 | -0.477 |
| w19 | 42 | -0.00297 | -4.586 |
| w20 | 18 | -0.055717 | -2.955 |
| w21 | 9 | 0.000941 | 1.072 |
| w22 | 43 | -0.061506 | -0.75 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

