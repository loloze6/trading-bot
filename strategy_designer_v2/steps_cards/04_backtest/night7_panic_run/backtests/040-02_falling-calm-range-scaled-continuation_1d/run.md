# Backtest of 040-02_falling-calm-range-scaled-continuation_1d

- Plan: `../../../../03_test_plan/night7_panic_run/plans/040-02_falling-calm-range-scaled-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | 0.033828 | 3.01 |
| w2 | 8 | 0.166487 | 35.622 |
| w3 | 20 | 0.149205 | -5.485 |
| w4 | 0 | 0.006236 | 0.0 |
| w5 | 9 | -0.035873 | -16.22 |
| w6 | 13 | 0.037364 | -3.693 |
| w7 | 24 | -0.07202 | -2.041 |
| w8 | 7 | 0.032765 | 0.148 |
| w9 | 40 | -0.295319 | -43.867 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | 0.034784 | 4.836 |
| w12 | 10 | -0.050289 | -5.12 |
| w13 | 7 | 0.061351 | 5.584 |
| w14 | 12 | 0.017395 | 11.526 |
| w15 | 0 | None | 0.0 |
| w16 | 4 | -0.031919 | -4.624 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | -0.04871 | 3.072 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.022724 | -4.229 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | 0.216519 | 8.478 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | 0.204098 | 27.703 |
| w2 | 2 | -0.088467 | 12.316 |
| w3 | 18 | 0.160633 | -1.663 |
| w4 | 0 | -0.02418 | 0.0 |
| w5 | 8 | -0.126891 | -8.263 |
| w6 | 14 | 0.055734 | 1.051 |
| w7 | 33 | 0.041977 | 29.157 |
| w8 | 0 | None | 0.0 |
| w9 | 35 | -0.095682 | -13.861 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | 0.028693 | 1.906 |
| w13 | 19 | 0.125395 | 19.92 |
| w14 | 9 | 0.12898 | 26.865 |
| w15 | 16 | -0.000592 | 2.992 |
| w16 | 6 | -0.075392 | -13.665 |
| w17 | 9 | -0.030038 | -3.769 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | 0.071398 | 3.883 |
| w22 | 6 | -0.040093 | 3.15 |
| w23 | 0 | None | 0.0 |
| w24 | 23 | 0.065909 | 2.949 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 38 | 0.123664 | 27.827 |
| w2 | 6 | 0.059558 | 8.674 |
| w3 | 15 | -0.031041 | -3.076 |
| w4 | 4 | -0.127949 | -18.913 |
| w5 | 2 | 0.009015 | 0.017 |
| w6 | 21 | 0.021846 | -3.573 |
| w7 | 62 | -0.001102 | 20.426 |
| w8 | 0 | None | 0.0 |
| w9 | 58 | 0.010856 | 5.367 |
| w10 | 8 | -0.010213 | -3.885 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | -0.005091 | -0.325 |
| w13 | 21 | 0.059401 | 12.045 |
| w14 | 21 | 0.058362 | 24.945 |
| w15 | 9 | 0.045096 | 3.145 |
| w16 | 9 | -0.077524 | -13.952 |
| w17 | 13 | 0.011996 | -1.531 |
| w18 | 12 | -0.009469 | -7.61 |
| w19 | 4 | -0.109264 | -7.648 |
| w20 | 22 | -0.003621 | 1.508 |
| w21 | 4 | -0.037946 | -3.452 |
| w22 | 2 | -0.042534 | -0.906 |
| w23 | 0 | None | 0.0 |
| w24 | 14 | -0.017286 | -1.427 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.095252 | 1.519 |
| w2 | 8 | -0.105053 | -3.167 |
| w3 | 17 | 0.000406 | -1.365 |
| w4 | 12 | -0.263468 | -24.036 |
| w5 | 12 | -0.088381 | -12.53 |
| w6 | 11 | -0.083815 | -9.286 |
| w7 | 61 | -0.060243 | -8.699 |
| w8 | 4 | 0.02673 | 0.028 |
| w9 | 46 | -0.012414 | 12.891 |
| w10 | 3 | -0.12754 | -5.718 |
| w11 | 0 | None | 0.0 |
| w12 | 19 | -0.047921 | -8.602 |
| w14 | 13 | 0.033135 | 13.147 |
| w15 | 8 | 0.081631 | 2.626 |
| w16 | 4 | -0.097602 | -10.715 |
| w17 | 0 | None | 0.0 |
| w18 | 6 | -0.057495 | -8.933 |
| w19 | 0 | None | 0.0 |
| w20 | 7 | -0.128221 | -12.598 |
| w21 | 4 | -0.007489 | -5.074 |
| w22 | 4 | -0.057278 | -5.43 |
| w23 | 13 | 0.047058 | 9.75 |
| w24 | 2 | 0.002278 | 0.128 |

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
| w1 | 24 | 0.123255 | 23.92 |
| w2 | 7 | -0.068787 | 14.8 |
| w3 | 0 | 0.039373 | 0.0 |
| w4 | 0 | -0.053459 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 10 | 0.079291 | 3.873 |
| w8 | 27 | -0.211188 | -9.406 |
| w9 | 35 | 0.097055 | 21.744 |
| w10 | 7 | -0.007436 | 2.274 |
| w11 | 0 | None | 0.0 |
| w12 | 17 | -0.016907 | -2.733 |
| w14 | 23 | 0.001454 | -6.607 |
| w15 | 20 | -0.044188 | -6.262 |
| w16 | 4 | -0.014674 | -0.995 |
| w17 | 11 | -0.003474 | -0.738 |
| w18 | 13 | -0.019897 | -4.851 |
| w19 | 16 | -0.039468 | -10.349 |
| w20 | 18 | 0.037209 | 10.051 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.009903 | -6.665 |
| w24 | 43 | 0.002168 | 17.945 |

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
| w1 | 24 | 0.122389 | 8.044 |
| w2 | 10 | -0.102858 | -12.889 |
| w3 | 39 | 0.113286 | 16.407 |
| w4 | 12 | -0.08401 | -3.154 |
| w5 | 18 | 0.049508 | 8.289 |
| w6 | 16 | 0.02333 | 0.378 |
| w7 | 40 | -0.120019 | -14.068 |
| w8 | 26 | -0.127905 | -12.155 |
| w9 | 29 | 0.120509 | 20.688 |
| w10 | 2 | -0.081071 | -1.785 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.012328 | -2.549 |
| w13 | 20 | 0.072989 | 19.939 |
| w14 | 22 | 0.066332 | 23.423 |
| w15 | 11 | -0.009104 | 0.031 |
| w16 | 0 | None | 0.0 |
| w17 | 21 | -0.024237 | -15.458 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 12 | 0.122737 | 2.01 |
| w21 | 7 | 0.027246 | -6.936 |
| w22 | 2 | -0.180561 | -3.045 |
| w23 | 19 | -0.040598 | -9.184 |
| w24 | 0 | None | 0.0 |

