# Backtest of 058-01.g2.g1_agitated-decline-upper-wick-fade_1d

- Plan: `../../../../03_test_plan/night8_fallingagitated_run/plans/058-01.g2.g1_agitated-decline-upper-wick-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.131334 | 0.767 |
| w2 | 19 | 0.104559 | 12.109 |
| w3 | 8 | 0.010517 | 0.495 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | -0.045566 | -5.417 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | 0.110327 | 3.13 |
| w9 | 7 | -0.053185 | -1.196 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.050165 | 0.539 |
| w13 | 17 | 0.153792 | 5.986 |
| w14 | 17 | 0.107957 | 10.573 |
| w15 | 1 | None | -0.01 |
| w16 | 21 | 0.086937 | 3.791 |
| w17 | 0 | None | 0.0 |
| w18 | 26 | 0.196195 | 12.375 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | -0.004778 | -0.392 |
| w21 | 0 | None | 0.0 |
| w22 | 18 | 0.004001 | -0.846 |
| w23 | 0 | None | 0.0 |
| w24 | 11 | -0.014236 | 0.524 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.007242 | -0.345 |
| w2 | 18 | -0.004487 | 0.138 |
| w3 | 5 | 0.033348 | 1.171 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 10 | 0.145313 | 2.747 |
| w9 | 5 | -0.053221 | -1.386 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 27 | 0.098546 | 12.286 |
| w15 | 6 | 0.027254 | 0.486 |
| w16 | 16 | 0.082376 | 1.464 |
| w17 | 2 | -0.026495 | -0.398 |
| w18 | 12 | 0.032895 | 0.813 |
| w19 | 0 | None | 0.0 |
| w20 | 17 | 0.114725 | 6.323 |
| w21 | 11 | -0.026238 | -1.869 |
| w22 | 26 | 0.094271 | 6.892 |
| w23 | 2 | 0.033447 | 0.05 |
| w24 | 10 | -0.067906 | -1.344 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 18 | 0.124909 | 9.246 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 9 | -0.014309 | -0.424 |
| w6 | 3 | -0.188753 | -5.248 |
| w7 | 0 | None | 0.0 |
| w8 | 8 | -0.033923 | -2.036 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.147496 | 1.595 |
| w13 | 9 | 0.045216 | 2.067 |
| w14 | 18 | 0.031721 | 3.582 |
| w15 | 6 | 0.057895 | 1.954 |
| w16 | 12 | 0.141388 | 3.403 |
| w17 | 3 | 0.068904 | 1.913 |
| w18 | 13 | 0.007157 | -0.441 |
| w19 | 0 | None | 0.0 |
| w20 | 25 | -0.08632 | -5.457 |
| w21 | 0 | None | 0.0 |
| w22 | 19 | 0.002794 | -0.886 |
| w23 | 1 | 0.031273 | 0.289 |
| w24 | 15 | 0.085221 | 4.172 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.114714 | 4.696 |
| w2 | 14 | -0.027532 | -2.387 |
| w3 | 1 | 0.020986 | 0.088 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 6 | -0.031085 | -2.512 |
| w7 | 0 | None | 0.0 |
| w8 | 4 | 0.154287 | 0.719 |
| w9 | 2 | 0.057307 | 1.52 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 15 | 0.140127 | 11.098 |
| w15 | 4 | -0.009334 | -0.857 |
| w16 | 16 | 0.107844 | 2.697 |
| w17 | 0 | None | 0.0 |
| w18 | 11 | 0.000876 | -0.424 |
| w19 | 14 | -0.007766 | -1.1 |
| w20 | 2 | 0.007985 | -0.154 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 6 | -0.243064 | -10.975 |
| w24 | 4 | -0.070012 | -2.671 |

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
| w1 | 2 | 0.119596 | 1.963 |
| w2 | 1 | 0.027944 | 13.633 |
| w3 | 0 | 0.041388 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | -0.04432 | -1.853 |
| w8 | 2 | 0.043527 | 0.292 |
| w9 | 5 | 0.026249 | 0.454 |
| w10 | 0 | None | 0.0 |
| w11 | 13 | -0.265817 | -24.613 |
| w12 | 0 | None | 0.0 |
| w14 | 3 | 0.026537 | 0.033 |
| w15 | 4 | -0.03793 | -1.719 |
| w16 | 17 | 0.190946 | 6.388 |
| w17 | 0 | None | 0.0 |
| w18 | 10 | 0.067296 | 1.873 |
| w19 | 2 | -0.001528 | -0.354 |
| w20 | 5 | 0.014622 | -1.861 |
| w21 | 1 | 0.077992 | 0.185 |
| w22 | 16 | 0.086556 | 3.039 |
| w23 | 0 | None | 0.0 |
| w24 | 11 | -0.006805 | 0.617 |

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
| w2 | 15 | 0.221044 | 15.113 |
| w3 | 7 | -0.097213 | -2.289 |
| w4 | 3 | -0.016933 | -0.536 |
| w5 | 11 | -0.213568 | -10.236 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | 0.208357 | 2.346 |
| w9 | 14 | 0.096934 | 5.484 |
| w10 | 1 | -0.015115 | -0.081 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 4 | 0.13105 | 1.648 |
| w14 | 13 | 0.129396 | 7.934 |
| w15 | 3 | 0.124877 | 5.222 |
| w16 | 24 | 0.047966 | -2.839 |
| w17 | 3 | -0.072407 | -2.54 |
| w18 | 12 | 0.117919 | 4.436 |
| w19 | 13 | -0.112015 | -8.489 |
| w20 | 5 | -0.004282 | -0.554 |
| w21 | 4 | -0.011873 | -2.346 |
| w22 | 25 | -0.089519 | -5.865 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

