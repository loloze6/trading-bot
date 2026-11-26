# Backtest of 064-01_rising-agitated-volume-shrink-rises_1d

- Plan: `../../../../03_test_plan/night8_fallingcalm_run/plans/064-01_rising-agitated-volume-shrink-rises_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | 0.032018 | -5.523 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.090392 | -0.856 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 7 | -0.088089 | 0.167 |
| w11 | 19 | -0.003793 | 16.55 |
| w12 | 8 | 0.019112 | 1.43 |
| w13 | 10 | -0.057561 | -8.324 |
| w14 | 0 | None | 0.0 |
| w15 | 13 | -0.041653 | 2.284 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | 0.014538 | 0.436 |
| w18 | 1 | -0.068577 | -0.342 |
| w19 | 17 | -0.009076 | 23.719 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | 0.010685 | 0.22 |
| w23 | 1 | -0.063978 | 0.021 |
| w24 | 0 | None | 0.0 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 5 | 0.033496 | -0.443 |
| w3 | 6 | 0.017704 | -4.56 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | -0.028009 | -0.582 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 4 | -0.051695 | 0.514 |
| w11 | 12 | -0.104251 | 13.247 |
| w12 | 8 | 0.043873 | 4.801 |
| w13 | 5 | 0.092979 | 5.688 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.079795 | -16.314 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.130443 | 2.238 |
| w18 | 0 | None | 0.0 |
| w19 | 17 | -0.059346 | 2.721 |
| w20 | 5 | 0.000835 | 0.127 |
| w21 | 1 | -0.025638 | -0.083 |
| w22 | 6 | 0.006528 | -3.644 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | -0.031492 | -1.344 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 10 | 0.069741 | 8.803 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 19 | 0.075459 | 27.869 |
| w12 | 0 | None | 0.0 |
| w13 | 10 | -0.195607 | -13.035 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 1 | -0.128306 | -1.589 |
| w17 | 3 | -0.058897 | -2.414 |
| w18 | 0 | None | 0.0 |
| w19 | 3 | -0.033317 | -1.463 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | -0.061863 | -1.938 |
| w22 | 9 | 0.08791 | 1.558 |
| w23 | 1 | -0.020808 | -0.049 |
| w24 | 2 | 0.067185 | 0.754 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | -0.06048 | -0.23 |
| w11 | 10 | -0.123664 | -5.089 |
| w12 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | -0.072154 | -2.183 |
| w16 | 6 | -0.123269 | -7.512 |
| w17 | 8 | 0.026225 | 5.991 |
| w18 | 0 | None | 0.0 |
| w19 | 3 | -0.065461 | -1.417 |
| w20 | 10 | 0.080393 | 9.854 |
| w21 | 0 | None | 0.0 |
| w22 | 11 | 0.031089 | 8.528 |
| w23 | 9 | -0.021652 | -2.863 |
| w24 | 9 | -0.034319 | 3.046 |

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
| w3 | 0 | -0.290796 | 0.0 |
| w4 | 0 | -0.007142 | 0.0 |
| w5 | 1 | -0.018902 | -0.322 |
| w6 | 5 | 0.009159 | -0.797 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 17 | -0.030104 | 33.447 |
| w12 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 6 | -0.04368 | -5.386 |
| w18 | 4 | -0.011607 | 0.635 |
| w19 | 1 | -0.248171 | -5.204 |
| w20 | 1 | -0.004905 | -0.009 |
| w21 | 3 | -0.103732 | -1.216 |
| w22 | 6 | 0.111992 | 5.623 |
| w23 | 1 | -0.039443 | -0.195 |
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
| w1 | 0 | None | 0.0 |
| w2 | 1 | -0.14364 | -2.748 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | -0.086393 | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 3 | -0.068484 | -3.031 |
| w11 | 14 | 0.115943 | 28.604 |
| w12 | 0 | None | 0.0 |
| w13 | 5 | -0.085957 | -2.008 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 5 | -0.270424 | -25.238 |
| w17 | 1 | -0.034542 | -0.961 |
| w18 | 0 | None | 0.0 |
| w19 | 6 | -0.192346 | -12.819 |
| w20 | 1 | -0.069806 | -3.342 |
| w21 | 6 | -0.096703 | -1.209 |
| w22 | 5 | -0.036466 | -1.687 |
| w23 | 3 | 0.14175 | 14.747 |
| w24 | 9 | -0.02493 | 15.013 |

