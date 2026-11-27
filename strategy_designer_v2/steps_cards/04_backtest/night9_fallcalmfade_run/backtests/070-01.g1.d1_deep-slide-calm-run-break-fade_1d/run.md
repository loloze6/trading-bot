# Backtest of 070-01.g1.d1_deep-slide-calm-run-break-fade_1d

- Plan: `../../../../03_test_plan/night9_fallcalmfade_run/plans/070-01.g1.d1_deep-slide-calm-run-break-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.036426 | -1.474 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | -0.010143 | -0.334 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | 0.026377 | 1.469 |
| w6 | 1 | 0.001927 | -0.873 |
| w7 | 2 | 0.023294 | 1.249 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | -0.004012 | 0.199 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.034362 | -2.501 |
| w13 | 2 | 0.062104 | 3.764 |
| w14 | 1 | 0.344202 | 29.379 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.094661 | 5.765 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | 0.04613 | 2.111 |
| w6 | 1 | 0.014374 | 0.024 |
| w7 | 4 | 0.193685 | 20.919 |
| w8 | 0 | None | 0.0 |
| w9 | 1 | -0.019678 | -0.786 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 4 | -0.020053 | -2.829 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.016597 | 0.474 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | 0.056725 | 4.251 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.080587 | 4.502 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.049305 | 1.225 |
| w7 | 5 | 0.065529 | 6.518 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | 0.116507 | 7.805 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | -0.051233 | -2.115 |
| w13 | 4 | -0.14252 | -11.602 |
| w14 | 1 | 0.142633 | 8.321 |
| w15 | 3 | -0.015888 | -1.71 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | -0.000917 | -0.837 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 1 | -0.242602 | -9.797 |
| w5 | 2 | -0.079824 | -5.01 |
| w6 | 1 | -0.013728 | -1.095 |
| w7 | 5 | 0.140771 | 14.46 |
| w8 | 0 | None | 0.0 |
| w9 | 5 | 0.065285 | 7.494 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.055105 | -3.605 |
| w14 | 1 | 0.079312 | 5.252 |
| w15 | 1 | 0.020482 | 0.65 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 1 | -0.000209 | -0.33 |
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
| w1 | 2 | 0.055252 | 4.038 |
| w2 | 0 | -0.167685 | 0.0 |
| w3 | 0 | 0.023536 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w8 | 1 | 0.012021 | 0.592 |
| w9 | 1 | 0.062061 | 3.134 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.008214 | 0.815 |
| w14 | 6 | -0.018541 | -7.891 |
| w15 | 1 | 0.024714 | 1.222 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 1 | 0.01879 | 1.313 |
| w20 | 1 | 0.014091 | 0.432 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | -0.061848 | -3.806 |

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
| w1 | 2 | -0.019163 | -2.195 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | 0.003484 | 0.262 |
| w4 | 1 | -0.060514 | -2.701 |
| w5 | 1 | 0.090316 | 5.907 |
| w6 | 1 | -0.007055 | -0.576 |
| w7 | 4 | 0.03876 | 3.463 |
| w8 | 1 | -0.1749 | -5.399 |
| w9 | 2 | 0.158499 | 11.836 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 5 | 0.012619 | 1.231 |
| w14 | 2 | 0.082663 | 7.416 |
| w15 | 5 | 0.088048 | 7.414 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 1 | -0.052402 | -3.063 |
| w24 | 0 | None | 0.0 |

