# Backtest of 058-02_choppy-agitated-weekly-fall-continues_1d

- Plan: `../../../../03_test_plan/night8_choppyagitated_run/plans/058-02_choppy-agitated-weekly-fall-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.125319 | -2.896 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | 0.055106 | -0.175 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | -0.013046 | 0.0 |
| w10 | 2 | 0.063421 | -0.74 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | -0.079185 | -13.623 |
| w13 | 3 | 0.125559 | 4.58 |
| w14 | 0 | None | 0.0 |
| w15 | 6 | 0.026585 | -3.075 |
| w16 | 4 | 0.354553 | 36.88 |
| w17 | 9 | -0.036584 | -12.264 |
| w18 | 2 | -0.160509 | 3.631 |
| w19 | 7 | 0.011258 | -11.006 |
| w20 | 18 | -0.092684 | 1.895 |
| w21 | 9 | -0.028435 | -5.137 |
| w22 | 1 | 0.290044 | 4.603 |
| w23 | 0 | -0.112478 | 0.0 |
| w24 | 19 | 0.034265 | 10.928 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | -0.016856 | 0.0 |
| w3 | 12 | 0.131337 | 4.606 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | 0.066636 | -0.532 |
| w9 | 4 | 0.021921 | -1.53 |
| w10 | 2 | 0.045078 | -2.997 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.052158 | -3.313 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.029507 | 7.332 |
| w16 | 2 | 0.135025 | 0.476 |
| w17 | 2 | -0.150454 | -2.311 |
| w18 | 5 | 0.102503 | 2.882 |
| w19 | 4 | -0.025818 | -6.865 |
| w20 | 10 | -0.086242 | -11.135 |
| w21 | 0 | None | 0.0 |
| w22 | 6 | -0.145048 | -1.846 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | 0.136696 | -4.807 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 10 | 0.086277 | -1.041 |
| w4 | 10 | -0.13205 | -4.03 |
| w5 | 5 | -0.160325 | -3.957 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 4 | -0.03387 | -0.904 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | 0.050448 | -0.192 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.199226 | -2.834 |
| w16 | 1 | 0.426079 | 14.802 |
| w17 | 7 | -0.012747 | -3.489 |
| w18 | 5 | 0.093632 | -1.932 |
| w19 | 11 | -0.055534 | -9.386 |
| w20 | 4 | 0.038141 | 0.594 |
| w21 | 13 | -0.057618 | -26.785 |
| w22 | 13 | 0.110093 | -5.357 |
| w23 | 4 | 0.031101 | -2.069 |
| w24 | 0 | None | 0.0 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.040181 | 2.224 |
| w2 | 5 | 0.237181 | -3.465 |
| w3 | 3 | 0.082984 | 1.7 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | -0.150205 | -7.782 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 4 | -0.072546 | -8.737 |
| w12 | 4 | -0.24004 | -12.298 |
| w14 | 2 | -0.026237 | -0.092 |
| w15 | 6 | -0.003578 | 1.115 |
| w16 | 3 | 0.368892 | 19.522 |
| w17 | 0 | None | 0.0 |
| w18 | 6 | -0.066365 | -8.798 |
| w19 | 21 | 0.043938 | -5.67 |
| w20 | 4 | -0.134399 | -4.613 |
| w21 | 7 | 0.045224 | -2.134 |
| w22 | 9 | -0.009318 | -16.295 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | -0.018028 | -17.087 |

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
| w1 | 2 | -0.101054 | -1.511 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | -0.157285 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 9 | -0.009731 | -9.047 |
| w6 | 5 | 0.015793 | 0.72 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | -0.025295 | -1.251 |
| w10 | 0 | None | 0.0 |
| w11 | 5 | 0.082212 | -2.36 |
| w12 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 6 | -0.076266 | -2.189 |
| w16 | 7 | 0.1752 | 3.466 |
| w17 | 7 | -0.137197 | -4.348 |
| w18 | 0 | None | 0.0 |
| w19 | 13 | -0.055835 | -1.726 |
| w20 | 6 | -0.237809 | -10.879 |
| w21 | 9 | 0.056065 | -2.478 |
| w22 | 12 | -0.1138 | -19.896 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | -0.004076 | 0.0 |

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
| w1 | 1 | -0.276305 | -0.071 |
| w2 | 2 | -0.066395 | 3.062 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 5 | -0.02251 | 0.808 |
| w6 | 4 | -0.018844 | -7.098 |
| w7 | 2 | -0.003282 | 1.892 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 10 | -0.071957 | -13.838 |
| w12 | 5 | -0.012075 | -4.595 |
| w13 | 3 | -0.189759 | -8.026 |
| w14 | 0 | None | 0.0 |
| w15 | 9 | 0.023018 | -4.297 |
| w16 | 0 | None | 0.0 |
| w17 | 15 | -0.060841 | -7.61 |
| w18 | 5 | -0.125918 | -4.694 |
| w19 | 7 | -0.071064 | -11.003 |
| w20 | 5 | 0.067248 | 13.609 |
| w21 | 0 | None | 0.0 |
| w22 | 13 | 0.039619 | -6.21 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | -0.002679 | 0.0 |

