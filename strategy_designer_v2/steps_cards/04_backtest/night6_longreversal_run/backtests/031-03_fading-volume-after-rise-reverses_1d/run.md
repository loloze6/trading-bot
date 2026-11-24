# Backtest of 031-03_fading-volume-after-rise-reverses_1d

- Plan: `../../../../03_test_plan/night6_longreversal_run/plans/031-03_fading-volume-after-rise-reverses_1d.md`
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
| w4 | 3 | -0.082448 | -1.083 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | 0.097145 | 0.964 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | -0.075007 | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | 0.114807 | -0.416 |
| w11 | 8 | 0.072432 | -4.524 |
| w12 | 0 | None | 0.0 |
| w13 | 5 | 0.027379 | 21.048 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.01643 | 5.315 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | -0.295812 | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 6 | 0.03556 | 10.466 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | 0.174329 | 5.974 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | 0.074075 | 0.447 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | -0.102266 | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 10 | 0.136462 | -49.189 |
| w11 | 6 | 0.216708 | -14.37 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 5 | -0.057323 | 6.803 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 4 | -0.1027 | -9.646 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 7 | -0.06848 | -33.796 |
| w24 | 3 | 0.047035 | 8.9 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 4 | 0.024634 | 7.844 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 11 | -0.168096 | -19.699 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 6 | -0.021024 | -10.581 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | 0.095991 | 9.588 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.043085 | -15.907 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | 0.006443 | 0.0 |
| w19 | 0 | 0.013125 | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 1 | 0.002385 | -0.281 |
| w22 | 3 | -0.002132 | -4.625 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | 0.035155 | 1.135 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 1 | 0.120974 | 1.704 |
| w11 | 2 | -0.014953 | -18.814 |
| w12 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.062552 | 5.25 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.104583 | -4.678 |
| w18 | 3 | 0.05153 | 7.263 |
| w19 | 0 | None | 0.0 |
| w20 | 7 | 0.079039 | -7.118 |
| w21 | 1 | -0.026137 | -0.015 |
| w22 | 7 | 0.092588 | -3.716 |
| w23 | 6 | -0.001916 | 3.29 |
| w24 | 1 | 0.050153 | 1.249 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=455. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | -0.00982 | 0.0 |
| w6 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | 0.216472 | 1.321 |
| w11 | 7 | -0.087823 | -31.417 |
| w12 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | 0.008445 | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | 0.025807 | 2.492 |
| w18 | 3 | 0.135583 | 1.74 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | 0.074799 | 5.568 |
| w22 | 2 | -0.078085 | -0.894 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=455. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=455. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.182547 | 9.7 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | 0.172963 | -7.682 |
| w11 | 10 | -0.119706 | -20.748 |
| w12 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | -0.164725 | 0.0 |
| w16 | 3 | 0.162036 | 18.855 |
| w17 | 0 | None | 0.0 |
| w18 | 4 | -0.066846 | 6.191 |
| w19 | 1 | 0.057888 | 10.039 |
| w20 | 0 | 0.204946 | 0.0 |
| w21 | 2 | 0.044364 | -13.636 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | 0.020495 | -2.346 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=455. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

