# Backtest of 074-01.b1.g2_calm-downtrend-relief-fade_1d

- Plan: `../../../../03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.g2_calm-downtrend-relief-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.059482 | -5.479 |
| w2 | 4 | 0.017951 | 2.873 |
| w3 | 10 | -0.046802 | -5.27 |
| w4 | 1 | 0.006236 | -0.282 |
| w5 | 3 | 0.012675 | 0.951 |
| w6 | 3 | 0.02453 | -0.523 |
| w7 | 7 | 0.046748 | 6.774 |
| w8 | 1 | 0.034372 | 0.721 |
| w9 | 8 | 0.002337 | 1.542 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.016258 | -2.031 |
| w13 | 5 | 0.086103 | 7.071 |
| w14 | 5 | 0.087928 | 19.654 |
| w15 | 0 | None | 0.0 |
| w16 | 1 | 0.059636 | 4.713 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | 0.014226 | 0.546 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.036762 | 3.922 |
| w2 | 0 | None | 0.0 |
| w3 | 5 | -0.016097 | -1.264 |
| w4 | 1 | -0.02418 | -0.326 |
| w5 | 2 | -0.066009 | -3.414 |
| w6 | 6 | 0.003754 | -3.889 |
| w7 | 9 | 0.166108 | 27.416 |
| w8 | 0 | None | 0.0 |
| w9 | 8 | 0.049675 | 7.846 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.020562 | 0.86 |
| w13 | 5 | -0.059864 | -7.741 |
| w14 | 5 | 0.12667 | 19.539 |
| w15 | 5 | 0.029872 | 1.587 |
| w16 | 2 | 0.05245 | 5.334 |
| w17 | 2 | -0.066086 | -5.002 |
| w18 | 1 | -0.011453 | -0.745 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.047902 | -2.753 |
| w23 | 0 | None | 0.0 |
| w24 | 7 | 0.030471 | 4.211 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.072611 | 9.072 |
| w2 | 1 | 0.056333 | 2.763 |
| w3 | 3 | 0.078862 | 5.762 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 7 | 0.05377 | 1.095 |
| w7 | 17 | 0.075336 | 16.303 |
| w8 | 0 | None | 0.0 |
| w9 | 14 | -0.089842 | -13.309 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | -0.02153 | -1.383 |
| w13 | 6 | -0.109542 | -12.272 |
| w14 | 7 | 0.203133 | 34.613 |
| w15 | 5 | -0.005393 | -1.443 |
| w16 | 3 | 0.019494 | 2.909 |
| w17 | 3 | 0.00477 | -1.964 |
| w18 | 2 | -0.001891 | 0.381 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.026275 | -2.806 |
| w21 | 1 | -0.023316 | -2.295 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.00994 | -2.634 |
| w24 | 4 | 0.016042 | 1.183 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.03964 | 2.675 |
| w2 | 2 | 0.080295 | 5.242 |
| w3 | 4 | -0.007207 | -1.911 |
| w4 | 2 | -0.242783 | -13.725 |
| w5 | 2 | -0.079824 | -5.01 |
| w6 | 2 | -0.020543 | -2.542 |
| w7 | 14 | 0.266071 | 43.316 |
| w8 | 1 | 0.039484 | 0.839 |
| w9 | 14 | -0.076113 | -9.617 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.002102 | -1.157 |
| w14 | 4 | 0.017713 | 2.905 |
| w15 | 4 | 0.012875 | -0.07 |
| w16 | 1 | 0.017783 | 0.707 |
| w17 | 0 | None | 0.0 |
| w18 | 1 | -0.007367 | -0.497 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.047366 | 1.318 |
| w21 | 2 | -0.01988 | -2.988 |
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
| w1 | 6 | 0.046476 | 6.224 |
| w2 | 1 | -0.139633 | -1.187 |
| w3 | 0 | 0.019225 | 0.0 |
| w4 | 0 | 0.038604 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 5 | -0.039649 | -6.121 |
| w8 | 7 | 0.080328 | 5.48 |
| w9 | 6 | 0.063997 | 7.561 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | -0.043561 | -3.115 |
| w14 | 9 | 0.022598 | -2.881 |
| w15 | 6 | -0.020077 | -3.346 |
| w16 | 1 | 0.052938 | 2.586 |
| w17 | 3 | -0.008684 | -2.664 |
| w18 | 5 | 0.052543 | 4.625 |
| w19 | 5 | 0.09506 | 12.918 |
| w20 | 5 | 0.088116 | 11.099 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 1 | 0.010489 | 0.07 |
| w24 | 11 | -0.097849 | -10.546 |

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
| w1 | 7 | 0.037114 | 4.555 |
| w2 | 3 | -0.024817 | -1.535 |
| w3 | 11 | 0.10146 | 18.678 |
| w4 | 4 | -0.022646 | -2.244 |
| w5 | 4 | 0.08134 | 10.037 |
| w6 | 5 | -0.058053 | -8.58 |
| w7 | 12 | 0.069309 | 11.591 |
| w8 | 8 | -0.071369 | -8.274 |
| w9 | 10 | -0.058671 | -5.707 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | -0.028359 | -1.816 |
| w13 | 6 | -0.012497 | -1.907 |
| w14 | 11 | 0.054012 | 14.082 |
| w15 | 5 | 0.092262 | 6.939 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | -0.02594 | -3.139 |
| w18 | 2 | -0.023357 | -1.623 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | 0.025489 | 0.547 |
| w21 | 2 | -0.132658 | -11.725 |
| w22 | 0 | None | 0.0 |
| w23 | 4 | -0.038762 | -5.359 |
| w24 | 0 | None | 0.0 |

