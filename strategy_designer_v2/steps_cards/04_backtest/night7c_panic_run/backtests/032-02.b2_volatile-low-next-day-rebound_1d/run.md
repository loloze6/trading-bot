# Backtest of 032-02.b2_volatile-low-next-day-rebound_1d

- Plan: `../../../../03_test_plan/night7c_panic_run/plans/032-02.b2_volatile-low-next-day-rebound_1d.md`
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
| w9 | 1 | -0.010271 | -0.104 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | 0.009543 | 0.0 |
| w13 | 0 | 0.145261 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 1 | 0.264057 | 9.289 |
| w17 | 1 | 0.05905 | 0.853 |
| w18 | 1 | 0.211666 | 3.369 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.075964 | 1.107 |
| w21 | 0 | -0.002471 | 0.0 |
| w22 | 1 | -0.117064 | -1.228 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | 0.013069 | -0.184 |

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
| w13 | 1 | 0.06637 | 0.236 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | 0.033315 | 0.0 |
| w16 | 1 | 0.310358 | 5.655 |
| w17 | 0 | 0.098442 | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | -0.081623 | -1.514 |
| w21 | 0 | 0.051606 | 0.0 |
| w22 | 1 | 0.080348 | 0.578 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | 0.123004 | 0.698 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 1 | -0.221308 | -1.289 |
| w5 | 0 | 0.057056 | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | -0.044961 | -0.47 |
| w13 | 1 | 0.008636 | 0.155 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | -0.072374 | -0.353 |
| w16 | 3 | 0.340083 | 5.403 |
| w17 | 1 | 0.096161 | 0.712 |
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
| w2 | 1 | -0.171798 | -2.822 |
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
| w15 | 1 | -0.007322 | 0.318 |
| w16 | 3 | 0.205354 | 3.801 |
| w17 | 1 | 0.114735 | 0.752 |
| w18 | 1 | 0.499806 | 6.936 |
| w19 | 3 | 0.470614 | 23.252 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | 0.165377 | 0.0 |
| w23 | 2 | 0.103092 | 2.787 |
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
| w5 | 1 | -0.005544 | -0.017 |
| w6 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | 0.304736 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | -0.02075 | 0.0 |
| w16 | 2 | 0.276171 | 7.134 |
| w17 | 1 | 0.325799 | 2.507 |
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
| w15 | 1 | 0.147648 | 0.775 |
| w16 | 1 | 0.072459 | 0.808 |
| w17 | 2 | 0.181058 | 2.661 |
| w18 | 0 | 0.274456 | 0.0 |
| w19 | 2 | 0.013329 | 0.71 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | 0.022289 | 0.0 |
| w22 | 1 | 0.077292 | 0.811 |
| w23 | 0 | 0.130563 | 0.0 |
| w24 | 0 | -0.072654 | 0.0 |

