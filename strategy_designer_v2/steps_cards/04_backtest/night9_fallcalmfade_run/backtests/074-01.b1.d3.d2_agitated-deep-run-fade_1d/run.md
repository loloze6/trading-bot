# Backtest of 074-01.b1.d3.d2_agitated-deep-run-fade_1d

- Plan: `../../../../03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.d3.d2_agitated-deep-run-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.127084 | 7.975 |
| w2 | 5 | 0.067253 | 8.723 |
| w3 | 7 | -0.020771 | -1.599 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.048728 | -3.129 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | 0.119954 | 0.0 |
| w9 | 5 | -0.065017 | -3.829 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 5 | 0.173727 | 11.863 |
| w14 | 4 | 0.083484 | 6.459 |
| w15 | 0 | None | 0.0 |
| w16 | 3 | -0.047537 | -0.914 |
| w17 | 0 | None | 0.0 |
| w18 | 10 | 0.203467 | 14.574 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.047892 | 2.212 |
| w21 | 0 | None | 0.0 |
| w22 | 4 | 0.017434 | 0.362 |
| w23 | 0 | None | 0.0 |
| w24 | 7 | 0.000339 | 0.738 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.079625 | -5.747 |
| w2 | 7 | 0.01558 | 1.971 |
| w3 | 5 | -0.051045 | -2.995 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.088181 | 2.046 |
| w9 | 2 | 0.062817 | 2.692 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 12 | 0.166114 | 27.287 |
| w15 | 1 | -0.02011 | -0.421 |
| w16 | 4 | -0.066481 | -2.148 |
| w17 | 1 | -0.029217 | -0.364 |
| w18 | 4 | 0.028764 | 0.831 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | 0.050954 | 5.974 |
| w21 | 3 | -0.017228 | -1.531 |
| w22 | 8 | 0.227644 | 26.582 |
| w23 | 0 | 0.021934 | 0.0 |
| w24 | 4 | -0.015093 | -0.408 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 8 | 0.0082 | 3.49 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | -0.060481 | -2.843 |
| w6 | 1 | -0.135216 | -4.58 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.122608 | 2.572 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | 0.009879 | 0.28 |
| w14 | 8 | 0.100416 | 7.588 |
| w15 | 2 | -0.075424 | -3.814 |
| w16 | 3 | 0.127856 | 4.912 |
| w17 | 0 | None | 0.0 |
| w18 | 8 | -0.029481 | -1.025 |
| w19 | 0 | None | 0.0 |
| w20 | 5 | 0.135191 | 10.546 |
| w21 | 0 | None | 0.0 |
| w22 | 6 | 0.05251 | 3.998 |
| w23 | 1 | 0.031273 | 0.089 |
| w24 | 9 | -0.074554 | -6.155 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.130496 | 9.082 |
| w2 | 6 | -0.038076 | -4.264 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.082713 | -1.28 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.037271 | 0.228 |
| w9 | 1 | 0.09161 | 3.409 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 7 | 0.076475 | 4.753 |
| w15 | 1 | 0.030433 | 0.098 |
| w16 | 4 | 0.037272 | 0.849 |
| w17 | 0 | None | 0.0 |
| w18 | 4 | -0.046192 | -2.119 |
| w19 | 7 | -0.014788 | -0.496 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 3 | -0.31311 | -23.321 |
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
| w1 | 0 | 0.0449 | 0.0 |
| w2 | 1 | -0.020579 | 18.026 |
| w3 | 0 | 0.00473 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.013003 | -0.86 |
| w8 | 0 | 0.061173 | 0.0 |
| w9 | 0 | 0.086999 | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | -0.029333 | -0.391 |
| w12 | 0 | None | 0.0 |
| w14 | 2 | 0.024718 | 1.04 |
| w15 | 2 | -0.044301 | -2.583 |
| w16 | 5 | 0.099506 | 4.98 |
| w17 | 0 | None | 0.0 |
| w18 | 5 | 0.051041 | 1.913 |
| w19 | 2 | -0.012694 | -1.195 |
| w20 | 1 | 0.098439 | 1.549 |
| w21 | 1 | 0.112248 | 7.981 |
| w22 | 4 | 0.076065 | 3.327 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | 0.017672 | 1.22 |

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
| w2 | 6 | 0.361371 | 31.582 |
| w3 | 4 | -0.092198 | -3.869 |
| w4 | 2 | 0.016153 | 0.095 |
| w5 | 1 | -0.370947 | -3.865 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | 0.086455 | 0.0 |
| w9 | 6 | 0.10635 | 7.255 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 1 | 0.080817 | 2.909 |
| w14 | 5 | 0.196861 | 13.814 |
| w15 | 3 | 0.089333 | 2.885 |
| w16 | 4 | 0.116862 | 5.422 |
| w17 | 1 | 0.051212 | 1.184 |
| w18 | 6 | 0.146219 | 5.994 |
| w19 | 9 | -0.102103 | -10.621 |
| w20 | 5 | 0.067598 | 4.165 |
| w21 | 1 | 0.02023 | 0.097 |
| w22 | 7 | 0.02199 | 1.765 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

