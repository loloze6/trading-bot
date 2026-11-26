# Backtest of 051-01_falling-agitated-scaled-fall-next-day-rebound_1d

- Plan: `../../../../03_test_plan/night7_panic_run/plans/051-01_falling-agitated-scaled-fall-next-day-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.038854 | -3.728 |
| w2 | 26 | 0.079647 | -0.93 |
| w3 | 19 | 0.257031 | 16.858 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.09751 | 5.213 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.047341 | 1.821 |
| w9 | 11 | -0.062698 | -7.113 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.092316 | 4.104 |
| w13 | 22 | 0.051584 | 3.818 |
| w14 | 21 | 0.198737 | 20.149 |
| w15 | 5 | -0.07784 | -3.215 |
| w16 | 13 | 0.295892 | 20.887 |
| w17 | 0 | None | 0.0 |
| w18 | 36 | 0.155492 | 16.93 |
| w19 | 0 | None | 0.0 |
| w20 | 12 | 0.068403 | 1.923 |
| w21 | 0 | None | 0.0 |
| w22 | 21 | 0.197891 | 19.449 |
| w23 | 0 | None | 0.0 |
| w24 | 20 | 0.073538 | 2.142 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.143697 | -11.693 |
| w2 | 37 | -2.1e-05 | -11.879 |
| w3 | 12 | 0.31732 | 22.473 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 12 | 0.146564 | 7.212 |
| w9 | 11 | 0.063535 | 2.306 |
| w10 | 1 | 0.128783 | 1.533 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 39 | 0.192156 | 22.275 |
| w15 | 6 | 0.023755 | 1.049 |
| w16 | 17 | 0.288667 | 19.706 |
| w17 | 1 | -0.006609 | 0.02 |
| w18 | 12 | 0.033476 | 3.895 |
| w19 | 1 | None | -0.057 |
| w20 | 23 | 0.099951 | 0.698 |
| w21 | 10 | 0.014887 | 2.1 |
| w22 | 39 | 0.062137 | -3.919 |
| w23 | 1 | 0.083426 | 0.125 |
| w24 | 11 | 0.134429 | 7.227 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 29 | 0.073297 | 2.498 |
| w3 | 1 | 0.393083 | 19.101 |
| w4 | 2 | 0.074071 | 3.034 |
| w5 | 8 | 0.004609 | -1.753 |
| w6 | 1 | 0.066606 | 2.334 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | -0.028308 | 0.008 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | 0.059999 | 2.873 |
| w13 | 7 | 0.097039 | 3.356 |
| w14 | 28 | 0.173478 | 14.017 |
| w15 | 11 | 0.146325 | 11.681 |
| w16 | 13 | 0.343119 | 24.368 |
| w17 | 3 | 0.050374 | 2.263 |
| w18 | 21 | 0.149046 | 9.272 |
| w19 | 1 | -0.04248 | -0.509 |
| w20 | 21 | 0.133984 | 7.615 |
| w21 | 1 | 0.047127 | 1.197 |
| w22 | 23 | 0.101071 | 7.28 |
| w23 | 3 | 0.094988 | 3.004 |
| w24 | 29 | -0.044157 | -7.752 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.091373 | -11.921 |
| w2 | 22 | 0.033984 | -1.189 |
| w3 | 2 | 0.137284 | 3.933 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | 0.004465 | 0.264 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | 0.07722 | 3.227 |
| w9 | 2 | 0.035025 | 0.552 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 29 | 0.138399 | 8.495 |
| w15 | 3 | 0.093671 | 4.015 |
| w16 | 17 | 0.299156 | 18.671 |
| w17 | 0 | None | 0.0 |
| w18 | 19 | 0.244798 | 22.298 |
| w19 | 21 | 0.274303 | 30.04 |
| w20 | 2 | 0.269286 | 5.429 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 6 | -0.011931 | -1.448 |
| w24 | 1 | 0.016406 | 0.009 |

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
| w1 | 4 | 0.134935 | 3.225 |
| w2 | 0 | -0.022929 | 0.0 |
| w3 | 0 | 0.031291 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.043222 | 1.56 |
| w8 | 4 | 0.079045 | 2.293 |
| w9 | 6 | 0.088999 | 2.97 |
| w10 | 0 | None | 0.0 |
| w11 | 8 | 0.016487 | 3.63 |
| w12 | 0 | None | 0.0 |
| w14 | 5 | 0.042498 | 2.167 |
| w15 | 6 | 0.02843 | 1.352 |
| w16 | 20 | 0.270352 | 22.571 |
| w17 | 2 | -0.004956 | -0.686 |
| w18 | 12 | 0.037612 | 2.012 |
| w19 | 12 | -0.039776 | -7.262 |
| w20 | 5 | 0.052052 | 4.986 |
| w21 | 5 | -0.012325 | 3.092 |
| w22 | 21 | 0.11842 | 9.259 |
| w23 | 0 | None | 0.0 |
| w24 | 10 | 0.037801 | -0.489 |

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
| w1 | 1 | 0.021729 | 0.746 |
| w2 | 33 | 0.11225 | 5.512 |
| w3 | 9 | 0.254718 | 14.074 |
| w4 | 6 | -0.033653 | -1.173 |
| w5 | 9 | 0.114696 | 7.776 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | -0.063448 | -1.484 |
| w8 | 8 | 0.162026 | 3.887 |
| w9 | 22 | 0.116901 | 6.679 |
| w10 | 3 | -0.048188 | 0.695 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 10 | 0.088375 | 3.122 |
| w14 | 22 | 0.153565 | 10.841 |
| w15 | 10 | -0.048594 | -5.531 |
| w16 | 22 | 0.126204 | 13.993 |
| w17 | 8 | 0.206764 | 17.719 |
| w18 | 20 | 0.152219 | 12.538 |
| w19 | 30 | 0.106716 | 7.512 |
| w20 | 11 | 0.109752 | 11.326 |
| w21 | 5 | 0.002234 | 0.788 |
| w22 | 25 | -0.01598 | -8.857 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

