# Backtest of 032-01_monthly-low-break-cascade_1d

- Plan: `../../../../03_test_plan/night7_panic_run/plans/032-01_monthly-low-break-cascade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 9 | 0.03222 | 15.002 |
| w3 | 2 | -0.356697 | -8.667 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.09751 | -5.037 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | 0.00774 | -14.378 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | -0.092316 | 0.0 |
| w13 | 2 | -0.083999 | -2.821 |
| w14 | 10 | -0.116499 | 1.063 |
| w15 | 0 | -0.007665 | 0.0 |
| w16 | 2 | -0.264057 | -7.903 |
| w17 | 0 | None | 0.0 |
| w18 | 12 | -0.255507 | -2.212 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | -0.126664 | -4.217 |
| w21 | 0 | None | 0.0 |
| w22 | 4 | -0.174259 | -5.462 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | 0.022534 | 4.607 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 9 | 0.039906 | 16.035 |
| w3 | 2 | -0.423086 | -8.7 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | 0.00373 | 2.169 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 19 | -0.018364 | 2.512 |
| w15 | 2 | -0.047609 | 1.593 |
| w16 | 2 | -0.310162 | -4.55 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | -0.044897 | -4.759 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | 0.005104 | 0.496 |
| w21 | 2 | -0.051606 | -1.462 |
| w22 | 18 | -0.066836 | 9.469 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | -0.047878 | 0.555 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 11 | 0.077161 | 14.51 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 5 | -0.008062 | -0.762 |
| w6 | 2 | -0.066606 | -2.698 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | -0.087978 | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 9 | -0.048244 | 0.603 |
| w15 | 4 | -0.201295 | 1.59 |
| w16 | 2 | -0.355445 | -5.925 |
| w17 | 0 | -0.067662 | 0.0 |
| w18 | 4 | -0.252738 | -2.973 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.078016 | -2.372 |
| w21 | 0 | None | 0.0 |
| w22 | 6 | -0.068248 | -1.865 |
| w23 | 0 | None | 0.0 |
| w24 | 9 | -0.124506 | -4.938 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.038972 | -1.112 |
| w2 | 4 | 0.040888 | -5.38 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | -0.035627 | 3.836 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 13 | -0.058016 | -6.113 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | -0.216863 | -5.949 |
| w17 | 0 | None | 0.0 |
| w18 | 4 | -0.485929 | -9.239 |
| w19 | 5 | -0.4394 | -15.628 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
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
| w2 | 0 | 0.027525 | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | -0.043222 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 2 | -0.011409 | -10.445 |
| w15 | 2 | -0.071904 | 1.297 |
| w16 | 2 | -0.274054 | -6.117 |
| w17 | 0 | -0.039852 | 0.0 |
| w18 | 2 | 0.010967 | -7.113 |
| w19 | 3 | 0.010835 | 0.201 |
| w20 | 2 | -0.073124 | -1.434 |
| w21 | 2 | -0.016047 | -1.257 |
| w22 | 4 | -0.168147 | -1.428 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | -0.074604 | -11.511 |

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
| w2 | 13 | -0.050129 | 5.739 |
| w3 | 2 | -0.295707 | -13.419 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | -0.069216 | -5.905 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | 0.063448 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 5 | -0.125804 | -11.195 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 11 | -0.124691 | 1.708 |
| w15 | 4 | 0.016233 | 3.154 |
| w16 | 2 | -0.088818 | -7.567 |
| w17 | 4 | -0.192118 | -4.623 |
| w18 | 8 | -0.234778 | -2.854 |
| w19 | 5 | -0.064426 | -1.362 |
| w20 | 4 | 0.006267 | 0.058 |
| w21 | 0 | None | 0.0 |
| w22 | 7 | -0.038397 | 0.89 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

