# Backtest of 074-01.g1_falling-agitated-wide-up-fade_1d

- Plan: `../../../../03_test_plan/night9_chopdeep_run/plans/074-01.g1_falling-agitated-wide-up-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 9 | 0.107533 | 13.297 |
| w3 | 8 | 0.090263 | 7.025 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.057306 | -5.546 |
| w7 | 0 | None | 0.0 |
| w8 | 3 | 0.066918 | 1.679 |
| w9 | 1 | -0.203102 | -7.861 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 5 | -0.009746 | -0.558 |
| w14 | 7 | 0.188164 | 18.227 |
| w15 | 0 | None | 0.0 |
| w16 | 8 | 0.107838 | 7.155 |
| w17 | 0 | None | 0.0 |
| w18 | 10 | 0.095518 | 7.777 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | 0.094456 | 4.488 |
| w21 | 0 | None | 0.0 |
| w22 | 7 | 0.074837 | 4.282 |
| w23 | 0 | None | 0.0 |
| w24 | 7 | -0.001189 | 0.658 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.027352 | -1.177 |
| w2 | 12 | 0.03017 | 5.026 |
| w3 | 4 | 0.034573 | 1.782 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 3 | 0.12573 | 3.105 |
| w9 | 1 | 0.065362 | 1.55 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 18 | 0.116746 | 22.373 |
| w15 | 0 | None | 0.0 |
| w16 | 6 | 0.077001 | 3.499 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | 0.132919 | 3.071 |
| w19 | 0 | None | 0.0 |
| w20 | 5 | 0.073862 | 4.796 |
| w21 | 6 | 0.051438 | 1.205 |
| w22 | 9 | 0.257032 | 32.576 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | -0.046891 | -1.94 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 6 | 0.178088 | 17.63 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | 0.034792 | 1.957 |
| w6 | 2 | -0.077454 | -4.554 |
| w7 | 0 | None | 0.0 |
| w8 | 3 | -0.028689 | -2.718 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 5 | 0.000373 | 0.119 |
| w14 | 10 | 0.026263 | 4.062 |
| w15 | 2 | 0.048648 | 1.979 |
| w16 | 4 | 0.106182 | 5.534 |
| w17 | 1 | 0.059275 | 1.906 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 9 | 0.05726 | 5.523 |
| w21 | 0 | None | 0.0 |
| w22 | 5 | 0.052953 | 3.678 |
| w23 | 1 | 0.031273 | 0.825 |
| w24 | 4 | 0.05072 | 2.024 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.026851 | 0.894 |
| w2 | 4 | -0.072494 | -5.679 |
| w3 | 1 | 0.018145 | 0.253 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | -0.089725 | -6.171 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.153898 | 2.747 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 7 | 0.151315 | 12.753 |
| w15 | 0 | None | 0.0 |
| w16 | 7 | 0.031772 | 0.214 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 8 | 0.01409 | 0.365 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.256566 | -16.547 |
| w24 | 1 | -0.009284 | -0.831 |

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
| w1 | 2 | 0.111109 | 3.985 |
| w2 | 1 | 0.012744 | 13.471 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.013245 | 0.071 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | 0.066612 | 3.352 |
| w10 | 0 | None | 0.0 |
| w11 | 5 | -0.168469 | -20.228 |
| w12 | 0 | None | 0.0 |
| w14 | 1 | 0.063443 | 2.459 |
| w15 | 1 | -0.066589 | -1.785 |
| w16 | 6 | 0.164421 | 14.525 |
| w17 | 0 | None | 0.0 |
| w18 | 3 | 0.08943 | 4.216 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.039524 | 0.641 |
| w21 | 0 | None | 0.0 |
| w22 | 6 | 0.108576 | 6.029 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | 0.038194 | 2.63 |

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
| w2 | 7 | 0.244539 | 18.241 |
| w3 | 4 | -0.103339 | -5.238 |
| w4 | 1 | 0.139423 | 3.078 |
| w5 | 4 | -0.099717 | -6.821 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.046663 | 0.498 |
| w9 | 7 | 0.155656 | 12.487 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 5 | 0.248273 | 17.316 |
| w15 | 1 | 0.109154 | 4.418 |
| w16 | 12 | 0.072661 | -2.737 |
| w17 | 3 | -0.040465 | -2.104 |
| w18 | 2 | -0.069573 | -2.545 |
| w19 | 11 | -0.078759 | -9.867 |
| w20 | 3 | -0.110537 | -8.49 |
| w21 | 3 | -0.039526 | -6.71 |
| w22 | 8 | 0.04313 | 2.655 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

