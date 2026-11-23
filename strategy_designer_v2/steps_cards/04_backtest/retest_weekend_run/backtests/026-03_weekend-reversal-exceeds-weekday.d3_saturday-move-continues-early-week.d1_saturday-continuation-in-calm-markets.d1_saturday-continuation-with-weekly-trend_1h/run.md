# Backtest of 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend_1h

- Plan: `../../../../03_test_plan/retest_weekend_run/plans/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.021641 | -2.555 |
| w2 | 11 | 0.004759 | 23.598 |
| w3 | 16 | -0.016001 | -12.93 |
| w4 | 14 | 0.005575 | 1.6 |
| w5 | 19 | 0.010315 | 1.358 |
| w6 | 8 | 0.026976 | 28.276 |
| w7 | 17 | -0.002389 | 9.07 |
| w8 | 12 | 0.025687 | 21.579 |
| w9 | 9 | 0.016804 | 18.232 |
| w10 | 10 | 0.009987 | 18.445 |
| w11 | 4 | -0.017042 | 3.594 |
| w12 | 13 | 0.03714 | -7.36 |
| w13 | 6 | 0.003483 | -2.063 |
| w14 | 13 | -0.006943 | 14.409 |
| w15 | 3 | -0.003166 | 17.346 |
| w16 | 14 | -2.1e-05 | -6.264 |
| w17 | 14 | 0.001806 | 6.981 |
| w18 | 5 | 0.030305 | 11.37 |
| w19 | 2 | 0.01976 | 3.68 |
| w20 | 0 | None | 0.0 |
| w21 | 9 | -0.019354 | 10.939 |
| w22 | 11 | -0.013063 | 2.322 |
| w23 | 21 | 0.020193 | -8.919 |
| w24 | 6 | -0.003881 | -1.303 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.043299 | 3.187 |
| w2 | 9 | 0.031412 | 17.467 |
| w3 | 15 | -0.031555 | -0.333 |
| w4 | 11 | 0.034662 | 6.62 |
| w5 | 19 | 0.008563 | 1.179 |
| w6 | 8 | 0.017766 | 12.29 |
| w7 | 0 | -0.001678 | 0.0 |
| w8 | 10 | 0.020003 | 0.74 |
| w9 | 17 | 0.015998 | 20.323 |
| w10 | 12 | 0.017692 | 2.986 |
| w11 | 2 | -0.009766 | 2.407 |
| w12 | 10 | 0.047157 | -1.91 |
| w13 | 0 | -0.010483 | 0.0 |
| w14 | 0 | -0.003834 | 0.0 |
| w15 | 8 | -0.005234 | 15.787 |
| w16 | 6 | 0.013221 | 2.278 |
| w17 | 10 | -0.029304 | 7.888 |
| w18 | 10 | -0.007605 | 3.836 |
| w19 | 4 | 0.00734 | 7.974 |
| w20 | 2 | -0.001322 | 0.541 |
| w21 | 7 | 0.003337 | 3.377 |
| w22 | 0 | None | 0.0 |
| w23 | 17 | -0.006081 | -1.994 |
| w24 | 6 | 0.01199 | -1.826 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.039912 | 10.366 |
| w2 | 10 | 0.03871 | 14.517 |
| w3 | 14 | 0.009951 | -12.582 |
| w4 | 15 | -0.028788 | 1.151 |
| w5 | 9 | -0.011901 | 2.514 |
| w6 | 20 | 0.02697 | 10.282 |
| w7 | 0 | -0.004499 | 0.0 |
| w8 | 2 | -0.034119 | -0.804 |
| w9 | 13 | -0.000359 | 5.662 |
| w10 | 17 | -0.005164 | 22.803 |
| w11 | 0 | None | 0.0 |
| w12 | 8 | 0.029289 | -6.561 |
| w13 | 0 | -0.008813 | 0.0 |
| w14 | 0 | -0.025946 | 0.0 |
| w15 | 6 | 0.006146 | 6.2 |
| w16 | 6 | -0.006138 | 7.975 |
| w17 | 8 | 0.007344 | -2.651 |
| w18 | 11 | 0.001631 | 11.293 |
| w19 | 6 | 0.009568 | -4.519 |
| w20 | 3 | 0.003279 | 2.614 |
| w21 | 14 | 0.001056 | -9.109 |
| w22 | 2 | 0.019089 | 1.1 |
| w23 | 16 | 0.030628 | -6.64 |
| w24 | 12 | 0.008304 | -1.273 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.00212 | 1.895 |
| w2 | 4 | 0.019665 | 1.587 |
| w3 | 22 | -0.0094 | -10.766 |
| w4 | 19 | 0.030704 | -4.364 |
| w5 | 12 | -0.023048 | 1.931 |
| w6 | 16 | -0.033598 | -8.365 |
| w7 | 0 | 0.020786 | 0.0 |
| w8 | 12 | -0.020679 | 16.401 |
| w9 | 14 | 0.005814 | 3.234 |
| w10 | 28 | 0.001446 | -3.318 |
| w11 | 0 | None | 0.0 |
| w12 | 18 | 0.032741 | -23.405 |
| w14 | 0 | 0.000857 | 0.0 |
| w15 | 12 | -0.017129 | 8.291 |
| w16 | 2 | -0.012675 | 0.659 |
| w17 | 8 | -0.018637 | 4.853 |
| w18 | 8 | 0.023228 | 4.307 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.0775 | 1.65 |
| w21 | 11 | -0.001059 | -2.605 |
| w22 | 8 | 0.037525 | 15.733 |
| w23 | 6 | 0.005152 | 1.063 |
| w24 | 8 | -0.003341 | -2.834 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 7757 warm-up bars -- required_bars=9480. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | 0.041679 | 22.138 |
| w2 | 4 | 0.021643 | 23.799 |
| w3 | 0 | 0.012614 | 0.0 |
| w4 | 0 | -0.00218 | 0.0 |
| w5 | 0 | -0.003623 | 0.0 |
| w6 | 10 | 0.072435 | 15.129 |
| w8 | 11 | -0.02747 | 4.008 |
| w9 | 8 | 0.011475 | 14.449 |
| w10 | 22 | -0.003838 | 7.771 |
| w11 | 0 | None | 0.0 |
| w12 | 13 | 0.036199 | -7.235 |
| w14 | 0 | -0.002909 | 0.0 |
| w15 | 12 | 0.000655 | 22.63 |
| w16 | 6 | -0.000187 | -0.157 |
| w17 | 9 | 0.015135 | 5.694 |
| w18 | 15 | 0.005821 | 10.21 |
| w19 | 2 | -0.00877 | -6.983 |
| w20 | 7 | 0.022205 | 18.974 |
| w21 | 12 | 0.003841 | 10.768 |
| w22 | 0 | None | 0.0 |
| w23 | 22 | -0.010449 | -0.491 |
| w24 | 14 | -0.019243 | 1.507 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 8280 warm-up bars -- required_bars=9480. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 5455 warm-up bars -- required_bars=9480. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.013348 | 4.298 |
| w2 | 12 | 0.007947 | 9.55 |
| w3 | 16 | -0.014087 | -5.773 |
| w4 | 25 | -0.011928 | -10.237 |
| w5 | 10 | -0.003986 | -0.505 |
| w6 | 19 | 0.008721 | 0.087 |
| w7 | 0 | -0.007422 | 0.0 |
| w8 | 8 | 0.026626 | -1.783 |
| w9 | 6 | -0.015768 | 3.888 |
| w10 | 12 | 0.023495 | 1.441 |
| w11 | 4 | 0.030934 | 0.933 |
| w12 | 13 | -0.022061 | -19.44 |
| w14 | 0 | -0.005979 | 0.0 |
| w15 | 12 | 0.016177 | 19.882 |
| w16 | 4 | -0.016877 | 20.798 |
| w17 | 8 | -0.007372 | 20.959 |
| w18 | 9 | -0.008055 | 4.561 |
| w19 | 4 | 0.010839 | -3.869 |
| w20 | 2 | 0.001134 | 2.974 |
| w21 | 7 | 0.003538 | 4.555 |
| w22 | 6 | 0.054261 | -1.104 |
| w23 | 23 | 0.01236 | -10.249 |
| w24 | 6 | -0.010954 | 3.069 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 9318 warm-up bars -- required_bars=9480. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

