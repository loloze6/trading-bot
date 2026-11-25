# Backtest of 047-01_falling-agitated-scaled-fall-rebound_1d

- Plan: `../../../../03_test_plan/night7_panic_run/plans/047-01_falling-agitated-scaled-fall-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.038854 | -6.757 |
| w2 | 31 | 0.079647 | -16.883 |
| w3 | 27 | 0.257031 | 10.646 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.09751 | 10.798 |
| w7 | 0 | None | 0.0 |
| w8 | 11 | 0.047341 | -0.678 |
| w9 | 15 | -0.062698 | 12.222 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.092316 | 2.186 |
| w13 | 27 | 0.051584 | -6.637 |
| w14 | 17 | 0.198737 | -20.712 |
| w15 | 5 | -0.07784 | -2.517 |
| w16 | 18 | 0.295892 | 24.879 |
| w17 | 0 | None | 0.0 |
| w18 | 42 | 0.155492 | -9.482 |
| w19 | 0 | None | 0.0 |
| w20 | 17 | 0.068403 | -5.033 |
| w21 | 0 | None | 0.0 |
| w22 | 21 | 0.197891 | 15.944 |
| w23 | 0 | None | 0.0 |
| w24 | 21 | 0.073538 | -4.223 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.143697 | -19.399 |
| w2 | 43 | -2.1e-05 | -12.547 |
| w3 | 16 | 0.31732 | 16.126 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 16 | 0.146564 | -3.25 |
| w9 | 16 | 0.063535 | 16.2 |
| w10 | 2 | 0.128783 | 1.267 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 49 | 0.192156 | -0.4 |
| w15 | 9 | 0.023755 | 4.196 |
| w16 | 22 | 0.288667 | 21.538 |
| w17 | 2 | -0.006609 | 0.518 |
| w18 | 16 | 0.033476 | 14.078 |
| w19 | 1 | None | -0.057 |
| w20 | 35 | 0.099951 | -5.521 |
| w21 | 15 | 0.014887 | 3.54 |
| w22 | 43 | 0.062137 | -29.422 |
| w23 | 2 | 0.083426 | 5.054 |
| w24 | 14 | 0.134429 | 7.575 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 36 | 0.073297 | -10.089 |
| w3 | 1 | 0.393083 | 18.306 |
| w4 | 3 | 0.074071 | 8.171 |
| w5 | 10 | 0.004609 | 2.37 |
| w6 | 1 | 0.066606 | 9.245 |
| w7 | 0 | None | 0.0 |
| w8 | 12 | -0.028308 | -1.027 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 6 | 0.059999 | 6.264 |
| w13 | 10 | 0.097039 | -2.784 |
| w14 | 31 | 0.173478 | -10.039 |
| w15 | 16 | 0.146325 | 7.543 |
| w16 | 19 | 0.343119 | 25.931 |
| w17 | 6 | 0.050374 | 4.211 |
| w18 | 22 | 0.149046 | 14.783 |
| w19 | 1 | -0.04248 | 0.453 |
| w20 | 25 | 0.133984 | -5.526 |
| w21 | 2 | 0.047127 | 1.244 |
| w22 | 31 | 0.101071 | -1.787 |
| w23 | 4 | 0.094988 | 5.199 |
| w24 | 30 | -0.044157 | -2.217 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.091373 | -20.656 |
| w2 | 26 | 0.033984 | 3.699 |
| w3 | 4 | 0.137284 | 5.882 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | 0.004465 | 5.331 |
| w7 | 0 | None | 0.0 |
| w8 | 10 | 0.07722 | 1.987 |
| w9 | 3 | 0.035025 | -4.07 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 35 | 0.138399 | -13.608 |
| w15 | 6 | 0.093671 | 3.969 |
| w16 | 25 | 0.299156 | 25.423 |
| w17 | 0 | None | 0.0 |
| w18 | 24 | 0.244798 | 17.27 |
| w19 | 29 | 0.274303 | 27.367 |
| w20 | 4 | 0.269286 | 3.595 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 6 | -0.011931 | 3.826 |
| w24 | 2 | 0.016406 | 0.575 |

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
| w1 | 6 | 0.134935 | 0.884 |
| w2 | 0 | -0.022929 | 0.0 |
| w3 | 0 | 0.031291 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.043222 | 3.897 |
| w8 | 6 | 0.079045 | -1.519 |
| w9 | 8 | 0.088999 | 2.592 |
| w10 | 0 | None | 0.0 |
| w11 | 15 | 0.016487 | 57.359 |
| w12 | 0 | None | 0.0 |
| w14 | 6 | 0.042498 | 0.001 |
| w15 | 8 | 0.02843 | -2.288 |
| w16 | 26 | 0.270352 | 20.096 |
| w17 | 3 | -0.004956 | 1.788 |
| w18 | 18 | 0.037612 | -0.622 |
| w19 | 12 | -0.039776 | -6.881 |
| w20 | 5 | 0.052052 | 6.766 |
| w21 | 7 | -0.012325 | 0.04 |
| w22 | 21 | 0.11842 | 8.656 |
| w23 | 0 | None | 0.0 |
| w24 | 11 | 0.037801 | 5.82 |

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
| w1 | 2 | 0.021729 | 18.65 |
| w2 | 36 | 0.11225 | -16.27 |
| w3 | 15 | 0.254718 | 21.479 |
| w4 | 7 | -0.033653 | 1.588 |
| w5 | 13 | 0.114696 | 30.279 |
| w6 | 0 | None | 0.0 |
| w7 | 2 | -0.063448 | 0.048 |
| w8 | 10 | 0.162026 | 0.026 |
| w9 | 26 | 0.116901 | 4.599 |
| w10 | 1 | -0.048188 | -1.516 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 11 | 0.088375 | -5.123 |
| w14 | 20 | 0.153565 | -19.998 |
| w15 | 9 | -0.048594 | -15.055 |
| w16 | 28 | 0.126204 | 29.526 |
| w17 | 14 | 0.206764 | 30.469 |
| w18 | 23 | 0.152219 | 14.323 |
| w19 | 35 | 0.106716 | 10.361 |
| w20 | 11 | 0.109752 | 27.008 |
| w21 | 6 | 0.002234 | 4.758 |
| w22 | 32 | -0.01598 | -12.844 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

