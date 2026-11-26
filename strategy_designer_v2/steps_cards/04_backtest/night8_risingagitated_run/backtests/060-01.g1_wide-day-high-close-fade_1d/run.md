# Backtest of 060-01.g1_wide-day-high-close-fade_1d

- Plan: `../../../../03_test_plan/night8_risingagitated_run/plans/060-01.g1_wide-day-high-close-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 4 | 0.101583 | 8.107 |
| w3 | 2 | 0.139876 | 7.066 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 1 | -0.203102 | -7.861 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 1 | 0.022061 | 0.621 |
| w14 | 2 | 0.189338 | 10.622 |
| w15 | 0 | None | 0.0 |
| w16 | 3 | 0.112177 | 5.623 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | -0.054215 | -2.536 |
| w19 | 0 | None | 0.0 |
| w20 | 1 | 0.047264 | 1.779 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | 0.015583 | -0.359 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | -0.114841 | -2.828 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.005949 | 0.045 |
| w2 | 4 | 0.091211 | 9.036 |
| w3 | 1 | 0.013444 | 0.536 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 4 | 0.047278 | 5.31 |
| w15 | 0 | None | 0.0 |
| w16 | 3 | 0.082528 | 3.672 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 1 | 0.080179 | 3.108 |
| w21 | 1 | 0.100622 | 2.707 |
| w22 | 4 | 0.27195 | 27.853 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | -0.06507 | -2.066 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 2 | 0.169674 | 9.74 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.065486 | 1.649 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 1 | -0.057445 | -1.885 |
| w14 | 2 | 0.133199 | 6.284 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | 0.103579 | 4.695 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 1 | 0.02204 | 0.606 |
| w21 | 0 | None | 0.0 |
| w22 | 3 | 0.119958 | 8.029 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- XMRUSD: 23 of 24 windows run.

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
| w14 | 2 | 0.118827 | 5.221 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | 0.060334 | 2.277 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 1 | 0.03075 | 1.078 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 1 | -0.043341 | -1.879 |
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
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w14 | 1 | 0.063443 | 2.459 |
| w15 | 0 | None | 0.0 |
| w16 | 3 | 0.141053 | 10.919 |
| w17 | 0 | None | 0.0 |
| w18 | 1 | -0.059039 | -2.003 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 1 | 0.069899 | 2.418 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | 0.14683 | 5.67 |

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
| w2 | 3 | 0.076111 | 3.619 |
| w3 | 2 | -0.071919 | -2.967 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | -0.059444 | -2.525 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | 0.064033 | 3.348 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 5 | 0.124365 | 8.684 |
| w17 | 1 | -0.068676 | -2.187 |
| w18 | 1 | -0.055762 | -1.733 |
| w19 | 3 | -0.018523 | -2.697 |
| w20 | 2 | -0.296732 | -21.247 |
| w21 | 1 | -0.013639 | -2.353 |
| w22 | 2 | 0.018932 | -0.068 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

