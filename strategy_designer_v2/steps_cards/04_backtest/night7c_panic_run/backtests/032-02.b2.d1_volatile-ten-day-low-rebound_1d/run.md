# Backtest of 032-02.b2.d1_volatile-ten-day-low-rebound_1d

- Plan: `../../../../03_test_plan/night7c_panic_run/plans/032-02.b2.d1_volatile-ten-day-low-rebound_1d.md`
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
| w5 | 1 | 0.028464 | 0.741 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | -0.0702 | -6.734 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.044687 | 2.524 |
| w13 | 6 | 0.04104 | 2.366 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.036732 | 3.014 |
| w16 | 1 | 0.264057 | 10.95 |
| w17 | 1 | 0.05905 | 3.835 |
| w18 | 4 | 0.125781 | 10.321 |
| w19 | 3 | 0.059482 | 3.912 |
| w20 | 6 | 0.063791 | 6.611 |
| w21 | 2 | 0.069075 | 4.311 |
| w22 | 2 | -0.068963 | -7.517 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | 0.092241 | 6.731 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.081763 | -3.756 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 2 | 0.230273 | 10.963 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | -0.015633 | 0.188 |
| w12 | 2 | 0.207119 | 12.222 |
| w13 | 5 | 0.081332 | 7.36 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.081691 | -7.022 |
| w16 | 2 | 0.230252 | 14.191 |
| w17 | 2 | 0.141954 | 8.316 |
| w18 | 4 | 0.049113 | 5.506 |
| w19 | 2 | -0.016881 | -0.688 |
| w20 | 5 | -0.106029 | -21.881 |
| w21 | 1 | 0.051606 | 2.199 |
| w22 | 4 | 0.079482 | 5.104 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | -0.045938 | -7.504 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | -0.119022 | -9.581 |
| w5 | 4 | 0.058621 | 4.344 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | 0.030587 | 2.947 |
| w12 | 3 | 0.079489 | 5.421 |
| w13 | 3 | -0.107945 | -8.7 |
| w14 | 0 | None | 0.0 |
| w15 | 5 | -0.016327 | -2.781 |
| w16 | 3 | 0.239656 | 12.241 |
| w17 | 2 | 0.090426 | 7.364 |
| w18 | 2 | 0.128544 | 8.032 |
| w19 | 2 | -0.110333 | -5.69 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 4 | 0.074335 | 4.79 |
| w23 | 2 | 0.122142 | 7.575 |
| w24 | 5 | -0.039922 | -5.504 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 1 | -0.208177 | -16.102 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | 0.047113 | 2.75 |
| w12 | 1 | 0.106861 | 5.197 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | 0.045402 | 3.787 |
| w16 | 4 | 0.137672 | 11.467 |
| w17 | 0 | None | 0.0 |
| w18 | 3 | 0.288122 | 21.273 |
| w19 | 6 | 0.357751 | 50.877 |
| w20 | 1 | 0.01435 | 0.788 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | 0.202877 | 12.413 |
| w23 | 5 | 0.057055 | 1.534 |
| w24 | 1 | 0.066053 | 2.695 |

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
| w5 | 2 | 0.012914 | 3.147 |
| w6 | 1 | 0.043222 | 1.56 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.304736 | 4.036 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.020115 | -1.072 |
| w16 | 3 | 0.219319 | 18.015 |
| w17 | 4 | 0.214942 | 22.406 |
| w18 | 3 | 0.199115 | 10.776 |
| w19 | 3 | -0.121915 | -9.779 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 4 | 0.0086 | 0.861 |
| w23 | 1 | 0.073824 | 3.076 |
| w24 | 2 | 0.093775 | 4.285 |

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
| w2 | 1 | -0.018361 | -0.999 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | None | -0.15 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | 0.082787 | 4.417 |
| w12 | 1 | 0.063014 | 2.348 |
| w13 | 2 | -0.014765 | -2.171 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.066252 | 2.743 |
| w16 | 4 | 0.063296 | 5.73 |
| w17 | 4 | 0.176623 | 14.84 |
| w18 | 4 | 0.271709 | 22.915 |
| w19 | 7 | 0.055289 | 2.285 |
| w20 | 0 | None | 0.0 |
| w21 | 4 | -0.030682 | -2.341 |
| w22 | 3 | -0.153095 | -14.536 |
| w23 | 3 | 0.101778 | 7.181 |
| w24 | 1 | -0.036693 | -0.591 |

