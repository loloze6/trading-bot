# Backtest of 058-02_agitated-rise-swing-scaled-giveback_1d

- Plan: `../../../../03_test_plan/night8_risingagitated_run/plans/058-02_agitated-rise-swing-scaled-giveback_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.10727 | -8.073 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | -0.032018 | 5.889 |
| w4 | 17 | -0.004676 | -8.92 |
| w5 | 0 | None | 0.0 |
| w6 | 23 | 0.078122 | -14.132 |
| w7 | 0 | None | 0.0 |
| w8 | 10 | 0.057955 | 0.025 |
| w9 | 0 | None | 0.0 |
| w10 | 13 | 0.308088 | 6.926 |
| w11 | 34 | -0.057217 | -31.812 |
| w12 | 5 | -0.197895 | -26.805 |
| w13 | 2 | 0.103632 | 1.597 |
| w14 | 0 | None | 0.0 |
| w15 | 37 | 0.040438 | -18.69 |
| w16 | 0 | None | 0.0 |
| w17 | 18 | -0.069949 | -24.855 |
| w18 | 1 | 0.083102 | 0.728 |
| w19 | 21 | 0.074105 | -15.894 |
| w20 | 0 | None | 0.0 |
| w21 | 11 | 0.0287 | -8.954 |
| w22 | 2 | -0.004569 | -0.535 |
| w23 | 1 | 0.063978 | -0.238 |
| w24 | 0 | None | 0.0 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 3 | -0.010377 | 0.567 |
| w3 | 3 | 0.015966 | 0.971 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 22 | 0.174971 | 14.478 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.032204 | 0.615 |
| w9 | 0 | None | 0.0 |
| w10 | 8 | 0.110393 | 3.231 |
| w11 | 39 | -0.018247 | -40.479 |
| w12 | 7 | 0.025231 | -3.613 |
| w13 | 11 | -0.081898 | -15.02 |
| w14 | 0 | None | 0.0 |
| w15 | 10 | 0.058898 | 5.551 |
| w16 | 6 | 0.04573 | 3.635 |
| w17 | 19 | 0.121473 | 4.413 |
| w18 | 7 | -0.073855 | -17.992 |
| w19 | 12 | 0.142128 | 37.409 |
| w20 | 6 | 0.016341 | -0.571 |
| w21 | 24 | -0.028241 | -18.01 |
| w22 | 5 | 0.012332 | 4.748 |
| w23 | 14 | 0.061722 | -6.393 |
| w24 | 2 | 0.041386 | 3.284 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 9 | 0.009145 | -4.591 |
| w4 | 0 | None | 0.0 |
| w5 | 5 | 0.08573 | 8.763 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 26 | 0.051877 | -18.334 |
| w9 | 0 | None | 0.0 |
| w10 | 9 | 0.098109 | 7.121 |
| w11 | 29 | 0.020929 | -22.363 |
| w12 | 2 | -0.020519 | -0.637 |
| w13 | 0 | 0.14014 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 14 | -0.062168 | -14.085 |
| w16 | 2 | -0.032422 | -0.183 |
| w17 | 22 | -0.035755 | -28.172 |
| w18 | 9 | -0.01286 | -1.61 |
| w19 | 13 | 0.028662 | -9.459 |
| w20 | 0 | None | 0.0 |
| w21 | 29 | -0.009318 | -23.085 |
| w22 | 19 | 0.122986 | 8.488 |
| w23 | 1 | 0.062504 | 1.719 |
| w24 | 0 | None | 0.0 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.009645 | -3.946 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | 0.085029 | 2.398 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 4 | 0.121198 | 1.073 |
| w11 | 24 | 0.014586 | -23.411 |
| w12 | 2 | 0.007804 | -1.642 |
| w14 | 0 | None | 0.0 |
| w15 | 12 | 0.142038 | 12.528 |
| w16 | 4 | 0.036479 | -0.482 |
| w17 | 25 | 0.121955 | 2.493 |
| w18 | 5 | 0.07194 | 2.213 |
| w19 | 0 | 0.094677 | 0.0 |
| w20 | 11 | -0.062041 | -13.251 |
| w21 | 10 | 0.135056 | 11.678 |
| w22 | 27 | 0.060106 | -9.538 |
| w23 | 8 | 0.00357 | -3.248 |
| w24 | 40 | 0.103081 | -4.779 |

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
| w2 | 0 | None | 0.0 |
| w3 | 0 | 0.051252 | 0.0 |
| w4 | 0 | 0.15102 | 0.0 |
| w5 | 6 | 0.083519 | 3.213 |
| w6 | 8 | 0.101626 | 11.72 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | 0.081696 | 0.777 |
| w10 | 5 | -0.017659 | -4.528 |
| w11 | 25 | -0.061108 | -48.291 |
| w12 | 0 | None | 0.0 |
| w14 | 5 | 0.0794 | 2.012 |
| w15 | 12 | 0.048547 | -0.841 |
| w16 | 6 | -0.025885 | -3.499 |
| w17 | 7 | -0.108702 | -19.548 |
| w18 | 2 | 0.225153 | 5.121 |
| w19 | 2 | 0.173221 | 5.79 |
| w20 | 12 | 0.033254 | -2.76 |
| w21 | 16 | -0.358239 | -72.983 |
| w22 | 15 | 0.047705 | 4.063 |
| w23 | 1 | 0.128713 | 1.509 |
| w24 | 0 | None | 0.0 |

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
| w1 | 7 | -0.014471 | -0.786 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.27558 | 6.932 |
| w7 | 0 | 0.115252 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 8 | 0.170359 | 14.14 |
| w11 | 35 | -0.059225 | -45.659 |
| w12 | 5 | 0.062057 | 1.259 |
| w13 | 9 | 0.120906 | 4.611 |
| w14 | 0 | None | 0.0 |
| w15 | 10 | 0.007222 | -11.388 |
| w16 | 13 | -0.077525 | -23.364 |
| w17 | 10 | 0.125963 | 12.233 |
| w18 | 9 | 0.044476 | 1.77 |
| w19 | 7 | 0.042226 | 1.432 |
| w20 | 20 | -0.082594 | -20.236 |
| w21 | 22 | 0.014952 | -19.032 |
| w22 | 1 | 0.031226 | -0.328 |
| w23 | 6 | -0.085237 | -10.872 |
| w24 | 37 | -0.161971 | -77.445 |

