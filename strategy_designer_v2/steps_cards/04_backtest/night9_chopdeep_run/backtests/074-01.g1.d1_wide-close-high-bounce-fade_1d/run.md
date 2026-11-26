# Backtest of 074-01.g1.d1_wide-close-high-bounce-fade_1d

- Plan: `../../../../03_test_plan/night9_chopdeep_run/plans/074-01.g1.d1_wide-close-high-bounce-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 7 | 0.072459 | 4.764 |
| w3 | 8 | 0.121314 | 6.613 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | 0.038741 | 0.0 |
| w9 | 1 | -0.203102 | -7.861 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 4 | 0.041917 | 1.769 |
| w14 | 6 | 0.184131 | 12.483 |
| w15 | 0 | None | 0.0 |
| w16 | 4 | 0.091919 | 5.381 |
| w17 | 0 | None | 0.0 |
| w18 | 6 | 0.019446 | 1.509 |
| w19 | 0 | None | 0.0 |
| w20 | 1 | 0.052729 | 1.779 |
| w21 | 0 | None | 0.0 |
| w22 | 6 | 0.077534 | 3.727 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | -0.01549 | -0.29 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.020116 | -0.669 |
| w2 | 8 | 0.075415 | 9.14 |
| w3 | 2 | 0.023678 | 0.942 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 3 | 0.127406 | 1.481 |
| w9 | 1 | 0.065362 | 0.6 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 13 | 0.077074 | 9.095 |
| w15 | 0 | None | 0.0 |
| w16 | 5 | 0.082908 | 3.429 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | 0.085967 | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | 0.085228 | 4.194 |
| w21 | 5 | 0.103338 | 3.078 |
| w22 | 7 | 0.283187 | 29.877 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | -0.052559 | -1.71 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 4 | 0.263189 | 23.825 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | 0.034792 | 1.337 |
| w6 | 2 | 0.002531 | -0.279 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.000431 | -0.926 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | -0.054119 | -1.898 |
| w14 | 8 | 0.075449 | 8.606 |
| w15 | 1 | -0.000973 | -0.016 |
| w16 | 4 | 0.108755 | 5.122 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | 0.020033 | 0.767 |
| w21 | 0 | None | 0.0 |
| w22 | 3 | 0.070639 | 4.251 |
| w23 | 1 | 0.031273 | 0.825 |
| w24 | 1 | 0.042081 | 0.645 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.03387 | 0.901 |
| w2 | 4 | -0.12364 | -5.557 |
| w3 | 0 | 0.018145 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | -0.015449 | -1.051 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.141868 | 1.05 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 5 | 0.122586 | 5.0 |
| w15 | 0 | None | 0.0 |
| w16 | 4 | 0.066804 | 2.491 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 5 | 0.021734 | 0.77 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.251441 | -19.646 |
| w24 | 1 | -0.009284 | -0.519 |

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
| w1 | 2 | 0.111284 | 2.346 |
| w2 | 1 | 0.005904 | 10.858 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.013245 | 0.02 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | 0.063166 | 1.554 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | 0.106921 | 5.101 |
| w12 | 0 | None | 0.0 |
| w14 | 1 | 0.063443 | 1.791 |
| w15 | 1 | -0.066589 | -0.394 |
| w16 | 6 | 0.168023 | 12.792 |
| w17 | 0 | None | 0.0 |
| w18 | 3 | -0.001686 | -0.091 |
| w19 | 0 | None | 0.0 |
| w20 | 1 | -0.021193 | -1.714 |
| w21 | 0 | None | 0.0 |
| w22 | 3 | 0.088842 | 3.075 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | 0.087626 | 4.302 |

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
| w2 | 5 | 0.133418 | 7.12 |
| w3 | 4 | -0.085068 | -3.421 |
| w4 | 1 | 0.139423 | 1.84 |
| w5 | 3 | -0.099455 | -6.016 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.046663 | 0.174 |
| w9 | 4 | 0.13719 | 6.863 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 4 | 0.193845 | 7.844 |
| w15 | 0 | None | 0.0 |
| w16 | 10 | 0.131586 | 7.034 |
| w17 | 2 | -0.069141 | -2.182 |
| w18 | 1 | -0.057122 | -1.381 |
| w19 | 7 | -0.054569 | -5.081 |
| w20 | 2 | -0.130596 | -8.126 |
| w21 | 1 | -0.013639 | -2.353 |
| w22 | 7 | 0.093937 | 5.968 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

