# Backtest of 032-02_volatile-decline-low-rebound_1d

- Plan: `../../../../03_test_plan/night7c_panic_run/plans/032-02_volatile-decline-low-rebound_1d.md`
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
| w9 | 2 | -0.010271 | -0.284 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | 0.009543 | 0.0 |
| w13 | 0 | 0.145261 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | 0.264057 | 5.929 |
| w17 | 2 | 0.05905 | -0.171 |
| w18 | 2 | 0.211666 | 1.911 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | 0.075964 | 3.662 |
| w21 | 0 | -0.002471 | 0.0 |
| w22 | 1 | -0.117064 | 1.728 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | 0.013069 | -1.067 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | -0.081763 | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | 0.242576 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | 0.244059 | 0.0 |
| w13 | 2 | 0.06637 | 7.527 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | 0.033315 | 0.0 |
| w16 | 2 | 0.310358 | 2.164 |
| w17 | 0 | 0.098442 | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | -0.081623 | -1.996 |
| w21 | 0 | 0.051606 | 0.0 |
| w22 | 2 | 0.080348 | -0.678 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | 0.123004 | -1.616 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | -0.221308 | 2.101 |
| w5 | 0 | 0.057056 | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.044961 | -1.191 |
| w13 | 2 | 0.008636 | 1.447 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | -0.072374 | -0.336 |
| w16 | 3 | 0.340083 | 3.033 |
| w17 | 2 | 0.096161 | 10.946 |
| w18 | 0 | 0.169854 | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | 0.07032 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | -0.048307 | 0.0 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 1 | -0.171798 | -1.561 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | 0.12051 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.007322 | 0.139 |
| w16 | 3 | 0.205354 | -1.607 |
| w17 | 2 | 0.114735 | 8.794 |
| w18 | 2 | 0.499806 | 6.583 |
| w19 | 5 | 0.470614 | 9.501 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | 0.165377 | 0.0 |
| w23 | 4 | 0.103092 | -0.495 |
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
| w5 | 2 | -0.005544 | 0.053 |
| w6 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | 0.304736 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | -0.02075 | 0.0 |
| w16 | 4 | 0.276171 | -1.405 |
| w17 | 2 | 0.325799 | -0.512 |
| w18 | 0 | 0.148535 | 0.0 |
| w19 | 0 | -0.307497 | 0.0 |
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
| w13 | 0 | -0.088998 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.147648 | -2.564 |
| w16 | 2 | 0.072459 | 7.694 |
| w17 | 4 | 0.181058 | 7.052 |
| w18 | 0 | 0.274456 | 0.0 |
| w19 | 2 | 0.013329 | -2.976 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | 0.022289 | 0.0 |
| w22 | 2 | 0.077292 | 1.023 |
| w23 | 0 | 0.130563 | 0.0 |
| w24 | 0 | -0.072654 | 0.0 |

