# Backtest of 032-01_volatile-decline-low-cascade_1d

- Plan: `../../../../03_test_plan/night7c_panic_run/plans/032-01_volatile-decline-low-cascade_1d.md`
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
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | 0.010271 | 0.134 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | -0.009543 | 0.0 |
| w13 | 0 | -0.145261 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | -0.264057 | -6.575 |
| w17 | 2 | -0.05905 | 0.12 |
| w18 | 2 | -0.211666 | -2.044 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.075964 | -2.691 |
| w21 | 0 | 0.002471 | 0.0 |
| w22 | 1 | 0.117064 | -1.756 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | -0.013069 | 0.942 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | 0.081763 | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | -0.242576 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | -0.244059 | 0.0 |
| w13 | 2 | -0.06637 | -8.406 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | -0.033315 | 0.0 |
| w16 | 2 | -0.310358 | -5.897 |
| w17 | 0 | -0.098442 | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | 0.081623 | 1.675 |
| w21 | 0 | -0.051606 | 0.0 |
| w22 | 2 | -0.080348 | -1.906 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | -0.123004 | 1.564 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | 0.221308 | -2.133 |
| w5 | 0 | -0.057056 | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.044961 | 1.16 |
| w13 | 2 | -0.008636 | -1.454 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | 0.072374 | 0.316 |
| w16 | 3 | -0.340083 | -3.397 |
| w17 | 2 | -0.096161 | -8.14 |
| w18 | 0 | -0.169854 | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | -0.07032 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | 0.048307 | 0.0 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 1 | 0.171798 | 1.519 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | -0.12051 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.007322 | -0.198 |
| w16 | 3 | -0.205354 | 1.07 |
| w17 | 2 | -0.114735 | -5.946 |
| w18 | 2 | -0.499806 | -6.705 |
| w19 | 5 | -0.470614 | -13.175 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | -0.165377 | 0.0 |
| w23 | 4 | -0.103092 | -0.019 |
| w24 | 0 | None | 0.0 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | 0.005544 | -0.065 |
| w6 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | -0.304736 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | 0.02075 | 0.0 |
| w16 | 4 | -0.276171 | 0.518 |
| w17 | 2 | -0.325799 | 0.345 |
| w18 | 0 | -0.148535 | 0.0 |
| w19 | 0 | 0.307497 | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=365. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

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
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | 0.088998 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.147648 | 2.489 |
| w16 | 2 | -0.072459 | -8.349 |
| w17 | 4 | -0.181058 | -6.894 |
| w18 | 0 | -0.274456 | 0.0 |
| w19 | 2 | -0.013329 | 2.904 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | -0.022289 | 0.0 |
| w22 | 2 | -0.077292 | -1.052 |
| w23 | 0 | -0.130563 | 0.0 |
| w24 | 0 | 0.072654 | 0.0 |

