# Backtest of 064-01_calm-decline-big-rise-fades_1d

- Plan: `../../../../03_test_plan/night9_fallcalmfade_run/plans/064-01_calm-decline-big-rise-fades_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.007112 | -5.668 |
| w2 | 4 | -0.155314 | -3.992 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 3 | -0.185128 | -7.821 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | 0.028208 | -9.856 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | 0.059237 | 7.64 |
| w6 | 2 | -0.023237 | -7.656 |
| w7 | 3 | 0.083669 | 7.674 |
| w8 | 0 | None | 0.0 |
| w9 | 1 | 0.085567 | 3.407 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | -0.001303 | -4.035 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | -0.011453 | -4.411 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.07381 | -1.52 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 2 | 0.14625 | 11.902 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | 0.034934 | 0.044 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | -0.008689 | -0.867 |
| w17 | 2 | -0.027826 | -10.514 |
| w18 | 2 | -0.030672 | -3.828 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.065812 | -9.342 |
| w24 | 0 | None | 0.0 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.088675 | -0.996 |
| w2 | 2 | 0.009394 | -1.324 |
| w3 | 1 | 0.114512 | 2.414 |
| w4 | 2 | -0.041797 | 1.59 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | None | -0.076 |
| w8 | 0 | None | 0.0 |
| w9 | 5 | 0.017516 | 2.591 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.054704 | -1.837 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | 0.016986 | -12.318 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | -0.007367 | -3.391 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | -0.084127 | -7.138 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
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
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | -0.007181 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.053473 | 2.752 |
| w8 | 1 | 0.101809 | 2.986 |
| w9 | 2 | -0.268005 | -6.099 |
| w10 | 2 | 0.064773 | -11.753 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 5 | -0.092425 | -36.753 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | -0.010225 | -0.372 |
| w18 | 4 | -0.049457 | -3.941 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.109413 | 4.57 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

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
| w1 | 2 | -0.004572 | -4.791 |
| w2 | 2 | -0.059367 | -1.006 |
| w3 | 1 | -0.005078 | 4.025 |
| w4 | 2 | -0.060514 | 1.364 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 2 | 0.016042 | -2.836 |
| w8 | 4 | -0.021424 | -0.929 |
| w9 | 3 | 0.092116 | 1.334 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | -0.06634 | -3.525 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | 0.099848 | 7.734 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | -0.018254 | 2.173 |
| w18 | 2 | -0.021306 | -1.694 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | 0.008748 | -1.989 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 1 | 0.022327 | 4.631 |
| w24 | 0 | None | 0.0 |

