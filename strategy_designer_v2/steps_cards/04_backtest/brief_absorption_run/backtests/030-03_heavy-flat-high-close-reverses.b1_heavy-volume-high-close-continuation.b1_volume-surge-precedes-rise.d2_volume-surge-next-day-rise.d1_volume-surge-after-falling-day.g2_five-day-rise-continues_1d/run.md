# Backtest of 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g2_five-day-rise-continues_1d

- Plan: `../../../../03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g2_five-day-rise-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 36 | -0.056529 | -0.906 |
| w2 | 40 | 0.000604 | -14.202 |
| w3 | 44 | -0.11876 | -16.042 |
| w4 | 38 | 0.074371 | 70.054 |
| w5 | 31 | -0.023521 | -9.792 |
| w6 | 55 | 0.081349 | 67.227 |
| w7 | 29 | 0.064961 | -1.011 |
| w8 | 39 | -0.013538 | 10.369 |
| w9 | 25 | -0.035989 | -13.598 |
| w10 | 38 | -0.015815 | 12.548 |
| w11 | 47 | 0.103729 | 67.297 |
| w12 | 36 | 0.090488 | -3.34 |
| w13 | 35 | 0.035714 | 3.278 |
| w14 | 20 | -0.033587 | -11.937 |
| w15 | 39 | 0.058645 | 66.309 |
| w16 | 56 | -0.024489 | 4.888 |
| w17 | 51 | 0.046789 | 50.751 |
| w18 | 43 | 0.008406 | -10.886 |
| w19 | 42 | 0.072702 | 47.674 |
| w20 | 45 | 0.004407 | -0.411 |
| w21 | 54 | 0.036598 | 36.25 |
| w22 | 45 | -0.077608 | -9.205 |
| w23 | 42 | -0.093821 | -5.018 |
| w24 | 42 | 0.053616 | -1.524 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 36 | 0.037737 | 1.968 |
| w2 | 38 | 0.03644 | -11.698 |
| w3 | 37 | 0.004173 | 1.084 |
| w4 | 48 | -0.036103 | 19.044 |
| w5 | 35 | -0.114029 | -13.119 |
| w6 | 43 | -0.028258 | 24.699 |
| w7 | 36 | -0.018932 | -13.157 |
| w8 | 40 | 0.040011 | 4.288 |
| w9 | 35 | -0.003579 | -6.589 |
| w10 | 42 | 0.134422 | 68.502 |
| w11 | 55 | -0.080666 | 50.088 |
| w12 | 39 | -0.065452 | -12.331 |
| w13 | 40 | 0.125476 | 25.952 |
| w14 | 28 | 0.009944 | -1.587 |
| w15 | 38 | 0.106632 | 30.223 |
| w16 | 61 | -0.031157 | 24.5 |
| w17 | 50 | -0.124494 | -12.444 |
| w18 | 44 | -0.02673 | 19.548 |
| w19 | 40 | 0.151286 | 81.741 |
| w20 | 35 | 0.121531 | 11.297 |
| w21 | 51 | -0.058259 | 7.409 |
| w22 | 30 | -0.086983 | -21.09 |
| w23 | 40 | -0.002244 | 49.554 |
| w24 | 29 | -0.051228 | -11.761 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 35 | 0.003546 | 2.622 |
| w2 | 34 | -0.078526 | -18.578 |
| w3 | 40 | -0.077807 | -2.803 |
| w4 | 54 | -0.108618 | -9.186 |
| w5 | 28 | 0.019251 | -1.529 |
| w6 | 39 | -0.178372 | -10.233 |
| w7 | 25 | -0.014098 | -9.107 |
| w8 | 34 | -0.072852 | 4.67 |
| w9 | 30 | -0.083925 | -18.775 |
| w10 | 34 | 0.034938 | 14.705 |
| w11 | 53 | 0.003543 | 31.45 |
| w12 | 35 | -0.018504 | -8.788 |
| w13 | 24 | -0.01674 | 2.369 |
| w14 | 31 | -0.014031 | -13.134 |
| w15 | 37 | 0.070904 | 8.821 |
| w16 | 51 | -0.031824 | 2.015 |
| w17 | 43 | -0.021608 | -2.115 |
| w18 | 34 | 0.007139 | 13.722 |
| w19 | 41 | 0.026642 | 19.901 |
| w20 | 30 | 0.036944 | 0.967 |
| w21 | 50 | -0.00826 | 28.944 |
| w22 | 40 | -0.012715 | -13.224 |
| w23 | 44 | -0.034976 | 4.05 |
| w24 | 30 | -0.132313 | -16.465 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 43 | -0.137113 | -15.107 |
| w2 | 51 | -0.052393 | -15.066 |
| w3 | 43 | -0.282953 | -18.486 |
| w4 | 48 | -0.165833 | -18.473 |
| w5 | 32 | 0.168025 | 3.581 |
| w6 | 57 | -0.184383 | -15.286 |
| w7 | 27 | -0.03846 | -8.288 |
| w8 | 48 | 0.074559 | 16.56 |
| w9 | 33 | -0.070128 | -13.763 |
| w10 | 51 | -0.14776 | -4.137 |
| w11 | 53 | 0.002547 | 72.974 |
| w12 | 34 | -0.014949 | -12.533 |
| w14 | 29 | 0.010151 | -10.122 |
| w15 | 44 | 0.008602 | 1.993 |
| w16 | 47 | 0.036969 | 38.38 |
| w17 | 53 | -0.126435 | -12.066 |
| w18 | 51 | -0.076376 | -13.175 |
| w19 | 47 | 0.001974 | -36.627 |
| w20 | 55 | -0.076244 | 0.164 |
| w21 | 44 | 0.016322 | 16.101 |
| w22 | 51 | -0.063438 | 11.761 |
| w23 | 34 | 0.034668 | 10.272 |
| w24 | 53 | -0.181842 | -6.105 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=462. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | -0.049664 | -5.339 |
| w2 | 1 | -0.024706 | -5.938 |
| w3 | 0 | -0.006417 | 0.0 |
| w4 | 0 | -0.034461 | 0.0 |
| w5 | 4 | -0.032802 | -0.603 |
| w6 | 41 | -0.005342 | 18.799 |
| w8 | 29 | -0.048603 | -7.993 |
| w9 | 38 | -0.066712 | -20.693 |
| w10 | 36 | 0.217248 | 53.704 |
| w11 | 43 | 0.051251 | 73.476 |
| w12 | 19 | -0.02585 | -3.923 |
| w14 | 26 | 0.145836 | 33.871 |
| w15 | 34 | 0.105837 | 22.026 |
| w16 | 47 | -0.081124 | -5.895 |
| w17 | 45 | 0.212205 | 90.362 |
| w18 | 30 | -0.050504 | 3.357 |
| w19 | 39 | -0.104818 | -18.989 |
| w20 | 39 | 0.091051 | 21.79 |
| w21 | 39 | 0.303508 | 249.268 |
| w22 | 37 | -0.069067 | -12.044 |
| w23 | 34 | 0.115652 | 25.536 |
| w24 | 26 | 0.010058 | -4.827 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=462. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=462. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 36 | 0.046667 | 14.441 |
| w2 | 36 | 0.006536 | -14.13 |
| w3 | 28 | -0.077841 | -13.098 |
| w4 | 53 | -0.093809 | -2.957 |
| w5 | 36 | -0.091813 | -24.235 |
| w6 | 56 | -0.207196 | -21.547 |
| w7 | 29 | 0.051899 | -0.303 |
| w8 | 37 | 0.133041 | 22.394 |
| w9 | 34 | -0.088884 | -24.124 |
| w10 | 49 | -0.064369 | 3.801 |
| w11 | 47 | 0.105771 | 82.336 |
| w12 | 45 | 0.01813 | -6.644 |
| w14 | 35 | 0.0058 | -17.366 |
| w15 | 21 | 0.164772 | 28.173 |
| w16 | 51 | 0.126996 | 65.357 |
| w17 | 36 | -0.147109 | -34.642 |
| w18 | 34 | -0.066716 | -6.42 |
| w19 | 46 | 0.163373 | 24.211 |
| w20 | 33 | 0.20449 | 51.621 |
| w21 | 44 | 0.028628 | 37.678 |
| w22 | 37 | -0.152747 | -19.693 |
| w23 | 33 | -0.045581 | -2.236 |
| w24 | 49 | 0.04385 | 126.576 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 429 warm-up bars -- required_bars=462. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

