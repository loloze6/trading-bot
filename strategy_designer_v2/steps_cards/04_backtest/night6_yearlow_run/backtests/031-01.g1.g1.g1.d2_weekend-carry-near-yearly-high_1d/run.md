# Backtest of 031-01.g1.g1.g1.d2_weekend-carry-near-yearly-high_1d

- Plan: `../../../../03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.g1.d2_weekend-carry-near-yearly-high_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.00573 | 1.419 |
| w2 | 11 | 0.004401 | -1.691 |
| w3 | 9 | 0.015387 | -0.235 |
| w4 | 17 | -0.049174 | 9.205 |
| w5 | 9 | -0.055273 | -7.693 |
| w6 | 19 | -0.020565 | 12.823 |
| w7 | 0 | 0.006483 | 0.0 |
| w8 | 21 | 0.040315 | 2.121 |
| w9 | 10 | 0.102167 | 3.564 |
| w10 | 17 | 0.095181 | 4.76 |
| w11 | 15 | 0.06512 | 7.232 |
| w12 | 13 | -0.003698 | 2.828 |
| w13 | 2 | 0.07372 | -5.776 |
| w14 | 4 | 0.006436 | 0.297 |
| w15 | 16 | 0.05017 | 30.855 |
| w16 | 20 | -0.042266 | 1.051 |
| w17 | 17 | 0.055262 | 20.581 |
| w18 | 5 | 0.011937 | 0.054 |
| w19 | 16 | -0.059261 | 4.425 |
| w20 | 12 | 0.01977 | 1.21 |
| w21 | 20 | -0.092571 | 9.982 |
| w22 | 10 | -0.007098 | -7.08 |
| w23 | 20 | -0.005835 | 9.296 |
| w24 | 9 | 0.001626 | 2.278 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.049943 | -0.415 |
| w2 | 8 | 0.064377 | 0.486 |
| w3 | 10 | -0.008795 | -3.224 |
| w4 | 15 | -0.07307 | 5.014 |
| w5 | 15 | -0.20697 | -12.54 |
| w6 | 18 | -0.009985 | 14.393 |
| w7 | 8 | 0.085822 | -3.159 |
| w8 | 17 | 0.047696 | -1.412 |
| w9 | 9 | 0.026294 | 1.45 |
| w10 | 18 | 0.243073 | 32.618 |
| w11 | 20 | -0.067027 | 23.25 |
| w12 | 12 | -0.007721 | 1.077 |
| w13 | 6 | 0.100568 | 5.22 |
| w14 | 10 | 0.075126 | -2.134 |
| w15 | 10 | 0.096147 | 10.866 |
| w16 | 20 | -0.026851 | 7.061 |
| w17 | 23 | 0.067054 | 27.837 |
| w18 | 7 | 0.072046 | 5.0 |
| w19 | 11 | -0.011295 | 8.982 |
| w20 | 11 | 0.038659 | 3.504 |
| w21 | 17 | 0.017403 | 6.851 |
| w22 | 8 | 0.084394 | 0.989 |
| w23 | 17 | 0.019442 | 21.033 |
| w24 | 13 | 0.006202 | 0.039 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.081611 | 2.3 |
| w2 | 9 | 0.043194 | 1.841 |
| w3 | 14 | 0.051355 | -0.135 |
| w4 | 17 | -0.018948 | 3.498 |
| w5 | 11 | -0.145528 | -21.403 |
| w6 | 16 | 0.015038 | 0.674 |
| w7 | 5 | 0.063357 | -5.32 |
| w8 | 23 | 0.11328 | 10.897 |
| w9 | 8 | 0.044035 | 1.853 |
| w10 | 19 | 0.125545 | 8.488 |
| w11 | 18 | 0.117332 | 7.958 |
| w12 | 14 | 0.02792 | -3.818 |
| w13 | 8 | 0.007984 | 0.878 |
| w14 | 7 | 0.003562 | 1.094 |
| w15 | 12 | 0.109577 | 16.511 |
| w16 | 20 | -0.006498 | 1.332 |
| w17 | 21 | 0.104225 | 17.92 |
| w18 | 9 | -0.022673 | 8.27 |
| w19 | 14 | -0.029322 | -1.26 |
| w20 | 9 | 0.019868 | -3.128 |
| w21 | 16 | 0.057697 | 28.093 |
| w22 | 10 | -0.099969 | -10.856 |
| w23 | 17 | 0.029716 | 12.146 |
| w24 | 11 | 0.124899 | 0.028 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.08655 | 3.392 |
| w2 | 11 | -0.051719 | -1.229 |
| w3 | 15 | 0.013847 | -3.914 |
| w4 | 11 | 0.022326 | 10.823 |
| w5 | 10 | 0.012055 | 3.597 |
| w6 | 18 | -0.016533 | 8.832 |
| w7 | 7 | 0.041459 | 0.404 |
| w8 | 14 | -0.016346 | 1.144 |
| w9 | 9 | 0.01787 | 5.265 |
| w10 | 16 | 0.071172 | 10.905 |
| w11 | 19 | 0.133824 | 15.795 |
| w12 | 8 | 0.025619 | -0.479 |
| w14 | 12 | -0.045174 | 0.734 |
| w15 | 13 | 0.0644 | 4.464 |
| w16 | 19 | -0.065945 | 6.101 |
| w17 | 24 | 0.164274 | 38.725 |
| w18 | 9 | 0.012309 | 2.199 |
| w19 | 11 | -0.023831 | 0.523 |
| w20 | 21 | 0.148009 | 16.746 |
| w21 | 15 | 0.025565 | 16.837 |
| w22 | 12 | -0.143145 | -17.444 |
| w23 | 11 | 0.101175 | 16.357 |
| w24 | 23 | 0.177964 | 20.07 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.11514 | 1.301 |
| w2 | 0 | 0.047419 | 0.0 |
| w3 | 0 | -0.069728 | 0.0 |
| w4 | 0 | -0.090605 | 0.0 |
| w5 | 0 | -0.081361 | 0.0 |
| w6 | 15 | -0.073093 | 4.426 |
| w8 | 9 | -0.004175 | -5.149 |
| w9 | 7 | 0.010845 | -0.878 |
| w10 | 16 | 0.265913 | 22.765 |
| w11 | 20 | 0.148029 | 19.785 |
| w12 | 12 | 0.058337 | 1.944 |
| w14 | 13 | 0.031538 | 5.745 |
| w15 | 11 | 0.036942 | 5.345 |
| w16 | 18 | -0.046233 | -7.016 |
| w17 | 15 | 0.235164 | 57.738 |
| w18 | 9 | 0.040319 | 6.504 |
| w19 | 7 | 0.021419 | -0.006 |
| w20 | 14 | 0.084835 | 6.682 |
| w21 | 17 | 0.239499 | 60.868 |
| w22 | 12 | 0.040739 | -7.722 |
| w23 | 14 | -0.007859 | 4.506 |
| w24 | 8 | 0.009516 | -1.522 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.081356 | 10.007 |
| w2 | 8 | 0.002017 | -2.529 |
| w3 | 9 | 0.011359 | -5.41 |
| w4 | 14 | 0.009341 | 0.939 |
| w5 | 5 | -0.054525 | -6.418 |
| w6 | 14 | 0.097343 | 16.287 |
| w7 | 11 | -0.036748 | 1.115 |
| w8 | 12 | 0.024877 | 0.685 |
| w9 | 8 | -0.014473 | -2.471 |
| w10 | 19 | 0.168579 | 8.635 |
| w11 | 20 | 0.108163 | 19.337 |
| w12 | 14 | -0.034385 | -2.444 |
| w14 | 8 | -0.046999 | -1.118 |
| w15 | 10 | -0.017314 | -4.711 |
| w16 | 14 | -0.144451 | -8.709 |
| w17 | 13 | 0.145545 | 11.626 |
| w18 | 11 | -0.057986 | -4.27 |
| w19 | 8 | 0.124214 | 4.189 |
| w20 | 19 | 0.009395 | 0.643 |
| w21 | 16 | 0.073076 | 12.96 |
| w22 | 9 | -0.031414 | -2.296 |
| w23 | 19 | 0.143304 | 3.556 |
| w24 | 21 | 0.103519 | 25.372 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=456. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

