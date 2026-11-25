# Backtest of 032-02_monthly-low-exhaustion-rebound_1d

- Plan: `../../../../03_test_plan/night7_panic_run/plans/032-02_monthly-low-exhaustion-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 7 | -0.03222 | -16.111 |
| w3 | 1 | 0.356697 | 7.167 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | 0.09751 | 5.065 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | -0.00774 | 15.216 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | 0.092316 | 0.0 |
| w13 | 2 | 0.083999 | 2.848 |
| w14 | 8 | 0.116499 | -3.148 |
| w15 | 0 | 0.007665 | 0.0 |
| w16 | 2 | 0.264057 | 7.043 |
| w17 | 0 | None | 0.0 |
| w18 | 12 | 0.255507 | 1.396 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.126664 | 4.256 |
| w21 | 0 | None | 0.0 |
| w22 | 4 | 0.174259 | 5.484 |
| w23 | 0 | None | 0.0 |
| w24 | 7 | -0.022534 | -4.837 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 9 | -0.039906 | -16.036 |
| w3 | 2 | 0.423086 | 8.243 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | -0.00373 | -2.303 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 19 | 0.018364 | -6.686 |
| w15 | 2 | 0.047609 | -1.652 |
| w16 | 2 | 0.310162 | 4.159 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | 0.044897 | 4.775 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.005104 | -1.186 |
| w21 | 2 | 0.051606 | 1.444 |
| w22 | 18 | 0.066836 | -10.896 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | 0.047878 | -0.81 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 11 | -0.077161 | -16.114 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 5 | 0.008062 | 0.546 |
| w6 | 2 | 0.066606 | 2.632 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | 0.087978 | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 9 | 0.048244 | -1.61 |
| w15 | 4 | 0.201295 | -1.677 |
| w16 | 2 | 0.355445 | 5.698 |
| w17 | 0 | 0.067662 | 0.0 |
| w18 | 4 | 0.252738 | 2.753 |
| w19 | 0 | None | 0.0 |
| w20 | 5 | 0.078016 | 1.295 |
| w21 | 0 | None | 0.0 |
| w22 | 6 | 0.068248 | 1.572 |
| w23 | 0 | None | 0.0 |
| w24 | 9 | 0.124506 | 4.748 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.038972 | 2.079 |
| w2 | 4 | -0.040888 | 3.27 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | 0.035627 | -4.035 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 12 | 0.058016 | 4.687 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | 0.216863 | 5.894 |
| w17 | 0 | None | 0.0 |
| w18 | 4 | 0.485929 | 8.737 |
| w19 | 5 | 0.4394 | 13.382 |
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
| w2 | 0 | -0.027525 | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | 0.043222 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 2 | 0.011409 | 2.972 |
| w15 | 2 | 0.071904 | -1.338 |
| w16 | 2 | 0.274054 | 5.659 |
| w17 | 0 | 0.039852 | 0.0 |
| w18 | 2 | -0.010967 | 7.151 |
| w19 | 3 | -0.010835 | -0.392 |
| w20 | 2 | 0.073124 | 1.392 |
| w21 | 2 | 0.016047 | 1.206 |
| w22 | 4 | 0.168147 | 1.397 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | 0.074604 | 11.288 |

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
| w2 | 13 | 0.050129 | -6.154 |
| w3 | 2 | 0.295707 | 13.55 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | 0.069216 | 5.777 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | -0.063448 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 5 | 0.125804 | 11.381 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 11 | 0.124691 | -2.274 |
| w15 | 4 | -0.016233 | -3.168 |
| w16 | 2 | 0.088818 | 10.527 |
| w17 | 4 | 0.192118 | 4.691 |
| w18 | 8 | 0.234778 | 2.686 |
| w19 | 5 | 0.064426 | 0.761 |
| w20 | 4 | -0.006267 | -0.281 |
| w21 | 0 | None | 0.0 |
| w22 | 7 | 0.038397 | -1.086 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

