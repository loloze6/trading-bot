# Backtest of 058-01.g2.d1_volume-dry-up-at-the-lows_1d

- Plan: `../../../../03_test_plan/night8_fallingcalm_run/plans/058-01.g2.d1_volume-dry-up-at-the-lows_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | 0.115383 | 11.756 |
| w2 | 7 | 0.094308 | 50.023 |
| w3 | 18 | -0.011663 | -17.677 |
| w4 | 2 | 0.014685 | -2.591 |
| w5 | 8 | -0.022727 | -4.475 |
| w6 | 6 | 0.074585 | -1.384 |
| w7 | 22 | -0.067142 | 2.148 |
| w8 | 3 | 0.057465 | 2.417 |
| w9 | 36 | -0.291933 | -47.76 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | 0.034784 | -6.927 |
| w12 | 3 | -0.032191 | -0.468 |
| w13 | 14 | -0.026421 | -6.255 |
| w14 | 12 | -0.011494 | 37.053 |
| w15 | 0 | None | 0.0 |
| w16 | 8 | -0.123276 | -20.426 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | -0.036061 | -4.478 |
| w21 | 0 | None | 0.0 |
| w22 | 3 | -0.022724 | -4.421 |
| w23 | 0 | None | 0.0 |
| w24 | 8 | 0.130356 | 17.994 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | 0.12594 | 24.418 |
| w2 | 2 | -0.088467 | 7.566 |
| w3 | 18 | -0.061679 | -10.124 |
| w4 | 3 | -0.04728 | -4.748 |
| w5 | 8 | -0.011923 | -0.978 |
| w6 | 15 | -0.002146 | -11.11 |
| w7 | 24 | 0.11724 | 50.978 |
| w8 | 0 | None | 0.0 |
| w9 | 37 | -0.113389 | -14.985 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | 0.007199 | 0.442 |
| w13 | 18 | 0.155125 | 24.796 |
| w14 | 11 | 0.071922 | 23.85 |
| w15 | 12 | 0.082669 | 12.118 |
| w16 | 4 | -0.059276 | -7.062 |
| w17 | 10 | -0.019718 | -9.116 |
| w18 | 4 | -0.03474 | -7.621 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 9 | 0.042516 | -5.962 |
| w22 | 6 | -0.048666 | 1.816 |
| w23 | 0 | None | 0.0 |
| w24 | 25 | 0.018428 | 9.729 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 39 | 0.002012 | -0.295 |
| w2 | 8 | 0.121657 | 29.879 |
| w3 | 13 | -0.020328 | -1.728 |
| w4 | 5 | -0.122577 | -13.826 |
| w5 | 4 | -0.047105 | -0.635 |
| w6 | 6 | 0.033074 | 0.772 |
| w7 | 43 | 0.086447 | 42.728 |
| w8 | 0 | None | 0.0 |
| w9 | 44 | -0.117449 | -2.466 |
| w10 | 10 | -0.012877 | -4.537 |
| w11 | 0 | None | 0.0 |
| w12 | 7 | -0.012089 | -8.784 |
| w13 | 14 | 0.000469 | -1.05 |
| w14 | 14 | 0.056481 | 31.736 |
| w15 | 4 | 0.122974 | 16.018 |
| w16 | 10 | -0.052232 | -15.252 |
| w17 | 4 | -0.019414 | -7.669 |
| w18 | 8 | -0.035107 | -11.802 |
| w19 | 6 | -0.077995 | -10.661 |
| w20 | 17 | 0.013618 | 8.85 |
| w21 | 3 | -0.039471 | -8.661 |
| w22 | 1 | 0.127037 | 11.477 |
| w23 | 5 | -0.16482 | -6.749 |
| w24 | 10 | -0.02902 | -2.67 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.145861 | -24.428 |
| w2 | 6 | -0.054375 | -3.1 |
| w3 | 22 | -0.102391 | -9.656 |
| w4 | 4 | -0.223357 | -12.69 |
| w5 | 9 | -0.14937 | -9.46 |
| w6 | 5 | -0.132742 | -7.826 |
| w7 | 35 | 0.095013 | 27.411 |
| w8 | 5 | 0.054932 | 0.79 |
| w9 | 37 | -0.10957 | -6.571 |
| w10 | 4 | -0.150996 | -2.236 |
| w11 | 0 | None | 0.0 |
| w12 | 25 | -0.053884 | -3.472 |
| w14 | 8 | 0.059106 | 18.568 |
| w15 | 7 | 0.099642 | 11.066 |
| w16 | 6 | -0.123922 | -31.011 |
| w17 | 0 | None | 0.0 |
| w18 | 4 | -0.08006 | -13.405 |
| w19 | 0 | None | 0.0 |
| w20 | 9 | -0.142768 | -8.761 |
| w21 | 6 | -0.030131 | -15.014 |
| w22 | 6 | -0.117211 | -12.516 |
| w23 | 14 | 0.034609 | -2.466 |
| w24 | 4 | 0.011251 | -0.647 |

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
| w1 | 25 | 0.091873 | 28.641 |
| w2 | 6 | 0.07714 | 24.281 |
| w3 | 0 | 0.067015 | 0.0 |
| w4 | 0 | -0.018384 | 0.0 |
| w5 | 0 | -0.027775 | 0.0 |
| w6 | 10 | 0.013549 | -5.506 |
| w8 | 26 | -0.055966 | -7.399 |
| w9 | 34 | 0.039969 | -7.69 |
| w10 | 9 | -0.078104 | -8.792 |
| w11 | 0 | None | 0.0 |
| w12 | 16 | -0.05222 | -1.318 |
| w14 | 14 | 0.045133 | -10.211 |
| w15 | 12 | 0.07037 | 15.142 |
| w16 | 4 | -0.139086 | -11.736 |
| w17 | 10 | -0.016851 | -7.235 |
| w18 | 8 | -0.020116 | -5.532 |
| w19 | 14 | -0.099428 | -12.345 |
| w20 | 18 | 0.081962 | 20.35 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.071363 | -1.866 |
| w23 | 2 | 0.034237 | -1.006 |
| w24 | 30 | 0.052913 | 34.459 |

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
| w1 | 17 | 0.082775 | 8.88 |
| w2 | 8 | -0.162053 | -10.439 |
| w3 | 28 | 0.021046 | 26.916 |
| w4 | 18 | -0.077852 | -12.323 |
| w5 | 19 | 0.024614 | 21.125 |
| w6 | 7 | 0.022726 | -0.339 |
| w7 | 29 | -0.069378 | -4.652 |
| w8 | 15 | 0.042489 | -1.55 |
| w9 | 33 | 0.046458 | -5.427 |
| w10 | 2 | -0.081071 | 1.495 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.067481 | -5.928 |
| w13 | 17 | 0.113308 | 19.252 |
| w14 | 19 | 0.022716 | 17.902 |
| w15 | 13 | 0.053206 | 11.44 |
| w16 | 0 | None | 0.0 |
| w17 | 14 | -0.013546 | -9.165 |
| w18 | 7 | -0.068338 | -7.428 |
| w19 | 0 | None | 0.0 |
| w20 | 14 | -0.069079 | -18.787 |
| w21 | 6 | -0.033487 | -11.788 |
| w22 | 2 | -0.180561 | -4.687 |
| w23 | 18 | -0.076145 | -22.1 |
| w24 | 0 | None | 0.0 |

