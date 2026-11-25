# Backtest of 041-02_agitated-fall-rise-vs-range-giveback_1d

- Plan: `../../../../03_test_plan/night7_steadydecline_run/plans/041-02_agitated-fall-rise-vs-range-giveback_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.106713 | 1.248 |
| w2 | 29 | 0.03883 | 17.085 |
| w3 | 16 | 0.001492 | 0.273 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.038516 | -6.099 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | 0.137152 | 4.643 |
| w9 | 11 | -0.091946 | -6.087 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.002086 | -0.244 |
| w13 | 22 | -0.011508 | -1.789 |
| w14 | 19 | 0.197942 | 39.946 |
| w15 | 1 | None | -0.005 |
| w16 | 23 | 0.033505 | 0.216 |
| w17 | 0 | None | 0.0 |
| w18 | 29 | 0.080697 | 10.669 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | 0.042164 | 2.89 |
| w21 | 0 | None | 0.0 |
| w22 | 22 | 0.035331 | 1.952 |
| w23 | 0 | None | 0.0 |
| w24 | 14 | -0.005053 | 1.38 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.003947 | -0.357 |
| w2 | 29 | 0.013868 | 7.325 |
| w3 | 9 | -0.003219 | -0.106 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | 0.034821 | -1.329 |
| w9 | 6 | 0.086147 | 7.024 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 35 | 0.024936 | 11.731 |
| w15 | 7 | 0.04577 | 2.427 |
| w16 | 20 | 0.060466 | 1.685 |
| w17 | 1 | 0.00021 | -0.184 |
| w18 | 16 | 0.012747 | -1.741 |
| w19 | 0 | None | 0.0 |
| w20 | 21 | 0.115985 | 17.923 |
| w21 | 13 | -0.021589 | -7.064 |
| w22 | 32 | 0.194541 | 46.673 |
| w23 | 3 | 0.02164 | -0.202 |
| w24 | 12 | -0.046227 | -3.581 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 31 | 0.188011 | 42.12 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 10 | -0.006258 | -0.97 |
| w6 | 3 | -0.17265 | -12.743 |
| w7 | 0 | None | 0.0 |
| w8 | 8 | -0.004418 | -4.798 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | 0.020778 | 0.445 |
| w13 | 11 | -0.012345 | -0.793 |
| w14 | 19 | -0.020798 | -2.536 |
| w15 | 8 | 0.073663 | 4.221 |
| w16 | 17 | 0.111535 | 7.74 |
| w17 | 5 | 0.013504 | -1.723 |
| w18 | 16 | -0.007482 | -0.754 |
| w19 | 0 | None | 0.0 |
| w20 | 29 | 0.015144 | 3.698 |
| w21 | 0 | None | 0.0 |
| w22 | 25 | 0.019258 | 0.791 |
| w23 | 1 | 0.031273 | 0.825 |
| w24 | 18 | 0.022002 | 1.95 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.00702 | -2.897 |
| w2 | 23 | -0.101586 | -14.682 |
| w3 | 3 | 0.001646 | -0.467 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 5 | -0.086816 | -9.183 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | 0.107869 | 4.736 |
| w9 | 1 | 0.089323 | 1.079 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 19 | 0.119731 | 19.032 |
| w15 | 4 | -0.013649 | -0.865 |
| w16 | 22 | 0.060796 | 1.16 |
| w17 | 0 | None | 0.0 |
| w18 | 17 | 0.027668 | 1.266 |
| w19 | 20 | -0.068465 | -13.001 |
| w20 | 3 | 0.02981 | -0.099 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 6 | -0.17624 | -20.08 |
| w24 | 6 | -0.050259 | -7.201 |

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
| w1 | 2 | 0.110329 | 6.159 |
| w2 | 1 | 0.157589 | 18.026 |
| w3 | 0 | -0.016306 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | -0.053258 | -4.611 |
| w8 | 2 | -0.002329 | -0.108 |
| w9 | 7 | 0.043964 | 4.415 |
| w10 | 0 | None | 0.0 |
| w11 | 9 | -0.175123 | -29.183 |
| w12 | 0 | None | 0.0 |
| w14 | 5 | 0.041866 | 3.091 |
| w15 | 5 | 0.023679 | 2.099 |
| w16 | 22 | 0.178147 | 23.639 |
| w17 | 0 | None | 0.0 |
| w18 | 12 | 0.087259 | 8.05 |
| w19 | 3 | 0.029039 | 0.211 |
| w20 | 10 | -0.044363 | -11.068 |
| w21 | 2 | 0.117282 | 6.933 |
| w22 | 18 | 0.061842 | 4.687 |
| w23 | 0 | None | 0.0 |
| w24 | 11 | -0.016795 | -0.392 |

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
| w2 | 23 | 0.081034 | 11.442 |
| w3 | 14 | -0.13126 | -12.899 |
| w4 | 6 | 0.062855 | 3.048 |
| w5 | 11 | -0.210717 | -24.268 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | 0.13813 | 5.133 |
| w9 | 18 | 0.044533 | 8.717 |
| w10 | 1 | -0.015115 | -0.745 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 8 | 0.136313 | 10.925 |
| w14 | 16 | 0.083507 | 9.12 |
| w15 | 4 | 0.093756 | 2.578 |
| w16 | 23 | -0.025463 | -18.796 |
| w17 | 7 | -0.046334 | -3.335 |
| w18 | 15 | 0.045794 | 4.495 |
| w19 | 22 | -0.112028 | -21.72 |
| w20 | 7 | -0.047988 | -9.248 |
| w21 | 4 | -0.005048 | -6.005 |
| w22 | 33 | -0.038719 | -6.626 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

