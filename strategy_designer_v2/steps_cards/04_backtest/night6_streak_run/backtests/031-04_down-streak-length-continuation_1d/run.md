# Backtest of 031-04_down-streak-length-continuation_1d

- Plan: `../../../../03_test_plan/night6_streak_run/plans/031-04_down-streak-length-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 51 | 0.032343 | 13.426 |
| w2 | 53 | 0.072812 | 67.525 |
| w3 | 58 | -0.000403 | -3.934 |
| w4 | 51 | 0.121605 | -35.452 |
| w5 | 50 | 0.048457 | 12.349 |
| w6 | 51 | -0.033963 | -54.98 |
| w7 | 49 | 0.104202 | 4.03 |
| w8 | 46 | -0.121134 | -38.314 |
| w9 | 49 | -0.060875 | 17.972 |
| w10 | 40 | -0.109531 | -31.742 |
| w11 | 52 | -0.096224 | -55.148 |
| w12 | 53 | -0.046208 | -12.748 |
| w13 | 40 | -0.086896 | 1.523 |
| w14 | 49 | -0.039462 | 53.28 |
| w15 | 49 | 0.084978 | -41.253 |
| w16 | 46 | -0.179024 | -19.338 |
| w17 | 51 | 0.027468 | -72.684 |
| w18 | 50 | -0.127425 | 12.467 |
| w19 | 51 | -0.048614 | -25.673 |
| w20 | 56 | -0.080876 | -23.953 |
| w21 | 53 | -0.054469 | -41.003 |
| w22 | 54 | -0.007898 | -8.721 |
| w23 | 48 | 0.048891 | -23.049 |
| w24 | 54 | -0.007081 | 15.165 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 46 | 0.135105 | 16.054 |
| w2 | 50 | 0.009721 | 23.468 |
| w3 | 47 | -0.030234 | 12.641 |
| w4 | 39 | -0.059018 | -34.789 |
| w5 | 44 | -0.051345 | 15.271 |
| w6 | 43 | 0.023476 | -41.269 |
| w7 | 40 | 0.003939 | 60.526 |
| w8 | 52 | -0.149862 | -26.325 |
| w9 | 55 | -0.035277 | 35.106 |
| w10 | 45 | 0.0483 | -50.941 |
| w11 | 52 | -0.070068 | -75.889 |
| w12 | 59 | -0.053431 | -11.942 |
| w13 | 40 | 0.096882 | 5.474 |
| w14 | 49 | -0.062367 | 67.249 |
| w15 | 53 | 0.038609 | -19.786 |
| w16 | 53 | -0.058376 | -41.709 |
| w17 | 52 | -0.007061 | -51.99 |
| w18 | 51 | -0.148405 | -34.474 |
| w19 | 48 | -0.050132 | -36.805 |
| w20 | 46 | 0.016802 | 30.916 |
| w21 | 45 | -0.055049 | -26.787 |
| w22 | 46 | -0.146189 | 25.761 |
| w23 | 55 | -0.090308 | -60.116 |
| w24 | 60 | 0.048907 | 21.164 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 43 | -0.036914 | 28.383 |
| w2 | 51 | -0.002179 | 36.98 |
| w3 | 57 | -0.034609 | -39.726 |
| w4 | 48 | -0.025406 | -15.523 |
| w5 | 47 | 0.030347 | 11.369 |
| w6 | 59 | -0.083987 | -43.029 |
| w7 | 54 | -0.027459 | 45.865 |
| w8 | 50 | -0.033783 | -48.995 |
| w9 | 52 | -0.017434 | 12.803 |
| w10 | 48 | -0.172727 | -29.782 |
| w11 | 36 | 0.079721 | -38.867 |
| w12 | 58 | 0.055631 | -1.363 |
| w13 | 44 | -0.07647 | -6.278 |
| w14 | 47 | -0.118806 | 85.252 |
| w15 | 40 | 0.012536 | 1.812 |
| w16 | 49 | -0.094303 | -35.527 |
| w17 | 62 | -0.077641 | -65.797 |
| w18 | 37 | -0.153402 | 10.175 |
| w19 | 44 | -0.052005 | -32.103 |
| w20 | 44 | -0.028439 | 21.568 |
| w21 | 58 | -0.14344 | -67.166 |
| w22 | 56 | 0.020577 | -1.487 |
| w23 | 47 | -0.102749 | -28.438 |
| w24 | 53 | -0.068004 | -1.44 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 43 | -0.028303 | -12.038 |
| w2 | 61 | 0.058807 | 6.153 |
| w3 | 58 | -0.212879 | -17.346 |
| w4 | 43 | -0.082594 | -17.232 |
| w5 | 38 | 0.055646 | 29.052 |
| w6 | 46 | -0.091311 | -45.558 |
| w7 | 43 | -0.074636 | 30.315 |
| w8 | 33 | -0.160508 | -40.182 |
| w9 | 45 | -0.068427 | 36.904 |
| w10 | 47 | -0.157248 | -39.515 |
| w11 | 41 | -0.034592 | -57.416 |
| w12 | 54 | -0.018187 | 11.207 |
| w14 | 40 | -0.176978 | 55.351 |
| w15 | 32 | 0.021214 | -16.431 |
| w16 | 39 | 0.00403 | -13.546 |
| w17 | 55 | -0.194618 | -51.989 |
| w18 | 43 | -0.220463 | -11.189 |
| w19 | 51 | -0.061821 | 2.735 |
| w20 | 45 | -0.22478 | -30.263 |
| w21 | 45 | -0.028156 | -25.251 |
| w22 | 46 | -0.065428 | -44.699 |
| w23 | 51 | 0.099672 | 2.577 |
| w24 | 52 | 0.001104 | -45.369 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=457. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 48 | 0.030656 | 25.816 |
| w2 | 8 | 0.036762 | 28.17 |
| w3 | 0 | -0.036091 | 0.0 |
| w4 | 0 | -0.220197 | 0.0 |
| w5 | 8 | -0.126379 | 7.164 |
| w6 | 54 | -0.078939 | -38.712 |
| w8 | 50 | -0.209898 | -10.524 |
| w9 | 54 | -0.013404 | 1.539 |
| w10 | 33 | -0.121603 | -25.237 |
| w11 | 52 | -0.009725 | -67.424 |
| w12 | 57 | -0.109714 | 8.68 |
| w14 | 54 | 0.064107 | -33.617 |
| w15 | 47 | 0.078233 | -25.961 |
| w16 | 46 | -0.130391 | -19.208 |
| w17 | 41 | 0.031129 | -78.904 |
| w18 | 46 | -0.170509 | -15.598 |
| w19 | 48 | -0.116511 | -3.943 |
| w20 | 38 | 0.026166 | 14.098 |
| w21 | 52 | 0.13443 | -65.746 |
| w22 | 50 | 0.016208 | 3.403 |
| w23 | 55 | 0.10695 | -36.114 |
| w24 | 64 | -0.057975 | -3.603 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=457. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=457. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 39 | 0.038931 | -8.545 |
| w2 | 48 | -0.01436 | 17.485 |
| w3 | 54 | -0.136085 | 16.533 |
| w4 | 48 | -0.06031 | -6.36 |
| w5 | 52 | 0.039183 | 51.361 |
| w6 | 60 | -0.130472 | -26.842 |
| w7 | 40 | -0.007168 | 5.499 |
| w8 | 45 | -0.186721 | -31.821 |
| w9 | 52 | 0.037452 | 19.912 |
| w10 | 55 | -0.095738 | -50.939 |
| w11 | 49 | 0.117235 | -62.771 |
| w12 | 50 | 0.039456 | 0.279 |
| w14 | 57 | -0.067087 | 65.216 |
| w15 | 42 | -0.042097 | 0.132 |
| w16 | 51 | 0.012574 | -27.671 |
| w17 | 45 | -0.081568 | -26.478 |
| w18 | 46 | -0.201038 | -8.198 |
| w19 | 56 | 0.03718 | 6.707 |
| w20 | 42 | -0.006985 | -18.758 |
| w21 | 61 | 0.084184 | -50.233 |
| w22 | 53 | -0.002049 | 0.067 |
| w23 | 60 | 0.053523 | -29.315 |
| w24 | 53 | 0.092587 | -77.763 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=457. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

