# Backtest of 064-01.g1.b1_calm-decline-big-rise-next-day-fade_1d

- Plan: `../../../../03_test_plan/night9_fallcalmfade_run/plans/064-01.g1.b1_calm-decline-big-rise-next-day-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.037465 | 2.999 |
| w2 | 6 | -0.088839 | -5.413 |
| w3 | 1 | 0.01027 | 0.478 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | -0.035547 | -0.985 |
| w6 | 0 | None | 0.0 |
| w7 | 7 | -0.097924 | -10.059 |
| w8 | 0 | None | 0.0 |
| w9 | 5 | -0.012628 | -0.364 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | -0.012529 | -1.092 |
| w13 | 2 | 0.071243 | 3.774 |
| w14 | 2 | 0.009147 | 1.9 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | -0.05653 | -7.605 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | 0.039175 | 1.276 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.011988 | -0.738 |
| w2 | 0 | None | 0.0 |
| w3 | 3 | 0.005331 | 0.709 |
| w4 | 2 | 0.04068 | 0.643 |
| w5 | 3 | 0.049477 | 3.706 |
| w6 | 2 | -0.033728 | -3.991 |
| w7 | 6 | 0.055316 | 8.463 |
| w8 | 0 | None | 0.0 |
| w9 | 9 | -0.0028 | -0.282 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 8 | 0.125009 | 15.455 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | 0.017812 | 0.601 |
| w16 | 3 | 0.032894 | 2.42 |
| w17 | 0 | None | 0.0 |
| w18 | 1 | -0.011453 | -0.745 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 1 | 0.025518 | 0.403 |
| w22 | 1 | -0.053546 | -2.633 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | -0.013157 | -0.352 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.040233 | 5.366 |
| w2 | 2 | -0.003852 | 0.091 |
| w3 | 1 | -0.009633 | -0.736 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | 0.025537 | 0.123 |
| w7 | 10 | 0.056549 | 10.995 |
| w8 | 0 | None | 0.0 |
| w9 | 12 | 0.03315 | 4.957 |
| w10 | 1 | 0.066155 | 1.056 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.024478 | 0.666 |
| w13 | 8 | 0.129093 | 16.279 |
| w14 | 3 | 0.074492 | 7.348 |
| w15 | 1 | -0.017908 | -0.691 |
| w16 | 5 | 0.035929 | 0.094 |
| w17 | 1 | -0.027826 | -2.354 |
| w18 | 2 | -0.029477 | -2.119 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.017525 | 1.101 |
| w21 | 1 | -0.023036 | -2.085 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.031444 | -4.235 |
| w24 | 2 | 0.020204 | 1.193 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.114159 | -9.68 |
| w2 | 3 | -0.02914 | -2.515 |
| w3 | 3 | 0.009307 | -0.388 |
| w4 | 2 | -0.229466 | -15.192 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 11 | 0.028425 | 2.956 |
| w8 | 0 | None | 0.0 |
| w9 | 9 | -0.063759 | -6.704 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | 0.026687 | 1.494 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.020175 | -1.479 |
| w16 | 2 | -0.079203 | -9.109 |
| w17 | 0 | None | 0.0 |
| w18 | 1 | -0.007367 | -0.497 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 1 | -0.084127 | -5.903 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.029812 | 1.105 |
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
| w1 | 3 | -0.001355 | 0.474 |
| w2 | 2 | 0.11219 | 7.419 |
| w3 | 0 | 0.031435 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | -0.027775 | 0.0 |
| w6 | 4 | -0.005548 | -3.162 |
| w8 | 4 | 0.185265 | 12.674 |
| w9 | 7 | -0.073228 | -9.831 |
| w10 | 1 | 0.064773 | 2.911 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | -0.144554 | -11.704 |
| w14 | 6 | 0.056804 | 6.258 |
| w15 | 1 | 0.005799 | 0.234 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | -0.024499 | -4.694 |
| w18 | 3 | -0.061148 | -5.196 |
| w19 | 5 | -0.02575 | -4.184 |
| w20 | 3 | 0.118755 | 12.414 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | -0.039099 | -2.323 |

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
| w1 | 7 | -0.117823 | -16.169 |
| w2 | 7 | -0.069094 | -6.508 |
| w3 | 5 | -0.016758 | -0.722 |
| w4 | 8 | 0.026272 | 0.453 |
| w5 | 1 | 0.020698 | 1.207 |
| w6 | 5 | -0.004071 | -2.778 |
| w7 | 11 | 0.072816 | 10.403 |
| w8 | 4 | 0.014185 | 0.468 |
| w9 | 6 | 0.001761 | -1.046 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.000426 | -0.156 |
| w13 | 8 | -0.035909 | -4.899 |
| w14 | 5 | -0.037145 | -1.219 |
| w15 | 2 | 0.044536 | 2.426 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | 0.003498 | -0.047 |
| w18 | 3 | -0.016899 | -1.488 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.003004 | -0.759 |
| w21 | 1 | -0.027612 | -2.034 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.005673 | -1.189 |
| w24 | 0 | None | 0.0 |

