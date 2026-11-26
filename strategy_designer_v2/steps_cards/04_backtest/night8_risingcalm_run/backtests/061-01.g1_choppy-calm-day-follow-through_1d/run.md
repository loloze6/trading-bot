# Backtest of 061-01.g1_choppy-calm-day-follow-through_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/061-01.g1_choppy-calm-day-follow-through_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.038389 | -9.528 |
| w2 | 10 | -0.138698 | 19.356 |
| w3 | 18 | 0.145054 | 12.837 |
| w4 | 5 | 0.09597 | 33.151 |
| w5 | 37 | -0.036673 | -17.121 |
| w6 | 13 | 0.023651 | 14.063 |
| w7 | 29 | 0.024811 | 29.871 |
| w8 | 30 | -0.106487 | -14.974 |
| w9 | 19 | 0.048546 | 17.085 |
| w10 | 11 | 0.108388 | 29.581 |
| w11 | 5 | 0.01222 | 3.736 |
| w12 | 2 | 0.145505 | 7.422 |
| w13 | 9 | -0.104409 | -1.433 |
| w14 | 28 | 0.124293 | -9.347 |
| w15 | 0 | None | 0.0 |
| w16 | 8 | 0.007026 | 55.034 |
| w17 | 17 | 0.056006 | 5.362 |
| w18 | 5 | 0.124591 | 8.926 |
| w19 | 0 | None | 0.0 |
| w20 | 10 | 0.072961 | 15.408 |
| w21 | 16 | -0.003598 | -33.632 |
| w22 | 20 | 0.072628 | -0.303 |
| w23 | 29 | 0.028502 | -17.282 |
| w24 | 24 | 0.053637 | -19.551 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.032446 | 9.997 |
| w2 | 6 | 0.019031 | 15.592 |
| w3 | 13 | 0.060528 | -27.0 |
| w4 | 18 | -0.079413 | -16.645 |
| w5 | 36 | -0.045661 | 18.057 |
| w6 | 16 | 0.019965 | 3.22 |
| w7 | 9 | -0.051779 | -10.636 |
| w8 | 14 | 0.116492 | -2.202 |
| w9 | 19 | 0.154661 | -3.426 |
| w10 | 7 | 0.006783 | 2.828 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | -0.065064 | -0.451 |
| w13 | 1 | 0.057662 | 2.026 |
| w14 | 3 | 0.085671 | 13.809 |
| w15 | 2 | 0.062907 | 2.566 |
| w16 | 4 | -0.008251 | -4.627 |
| w17 | 11 | -0.037971 | 12.577 |
| w18 | 6 | 0.010241 | 21.352 |
| w19 | 0 | None | 0.0 |
| w20 | 8 | 0.054395 | 23.75 |
| w21 | 20 | 0.017734 | -26.32 |
| w22 | 2 | -0.050025 | 2.108 |
| w23 | 1 | 0.125739 | 11.054 |
| w24 | 4 | 0.074933 | -10.574 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.035254 | -7.274 |
| w2 | 26 | -0.088829 | -36.654 |
| w3 | 24 | 0.014324 | -39.067 |
| w4 | 14 | 0.055045 | -5.422 |
| w5 | 32 | 0.085235 | 36.953 |
| w6 | 33 | 0.051925 | 1.718 |
| w7 | 11 | -0.059935 | -5.483 |
| w8 | 3 | 0.028529 | 0.741 |
| w9 | 7 | -0.04245 | -6.255 |
| w10 | 33 | -0.154712 | -30.661 |
| w11 | 0 | None | 0.0 |
| w12 | 16 | -0.022747 | -4.309 |
| w13 | 2 | -0.162729 | -11.415 |
| w14 | 12 | 0.002365 | 0.898 |
| w15 | 0 | -0.214259 | 0.0 |
| w16 | 3 | -0.02227 | 2.387 |
| w17 | 7 | 0.000494 | -7.41 |
| w18 | 4 | -0.036665 | 8.815 |
| w19 | 15 | 0.08092 | 10.797 |
| w20 | 13 | -0.069292 | -33.708 |
| w21 | 23 | 0.031012 | -23.121 |
| w22 | 0 | None | 0.0 |
| w23 | 28 | 0.000242 | 23.298 |
| w24 | 11 | -0.130151 | 8.759 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.035163 | -4.521 |
| w2 | 5 | -0.108452 | -6.141 |
| w3 | 27 | -0.058285 | -12.762 |
| w4 | 36 | -0.129897 | -14.269 |
| w5 | 51 | 0.005303 | 34.625 |
| w6 | 29 | 0.019043 | -19.236 |
| w7 | 12 | -0.025514 | -15.575 |
| w8 | 14 | -0.111537 | 5.069 |
| w9 | 13 | -0.152077 | 17.544 |
| w10 | 12 | -0.110877 | 2.428 |
| w11 | 0 | None | 0.0 |
| w12 | 23 | 0.001411 | -17.997 |
| w14 | 18 | -0.019814 | -39.767 |
| w15 | 0 | None | 0.0 |
| w16 | 7 | -0.103742 | -0.276 |
| w17 | 2 | 0.133098 | 2.166 |
| w18 | 7 | 0.014389 | -3.439 |
| w19 | 3 | 0.040615 | -19.723 |
| w20 | 12 | -0.004428 | -11.823 |
| w21 | 30 | 0.056009 | 45.616 |
| w22 | 18 | 0.048524 | 28.523 |
| w23 | 14 | -0.014035 | -27.512 |
| w24 | 8 | 0.038699 | -7.135 |

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
| w1 | 16 | -0.042377 | -2.883 |
| w2 | 0 | -0.079728 | 0.0 |
| w3 | 0 | -0.129583 | 0.0 |
| w4 | 0 | -0.208047 | 0.0 |
| w5 | 8 | -0.058925 | -6.365 |
| w6 | 8 | 0.009415 | 35.638 |
| w8 | 37 | 0.049298 | -14.32 |
| w9 | 17 | -0.012526 | -15.137 |
| w10 | 24 | -0.020431 | -22.995 |
| w11 | 0 | None | 0.0 |
| w12 | 22 | -0.082838 | 5.274 |
| w14 | 1 | 0.123197 | 13.963 |
| w15 | 7 | 0.175701 | -38.972 |
| w16 | 1 | -0.018224 | -0.897 |
| w17 | 12 | -0.026152 | -26.605 |
| w18 | 3 | 0.036174 | 37.811 |
| w19 | 13 | -0.002942 | -16.045 |
| w20 | 8 | -0.103777 | -2.454 |
| w21 | 16 | 0.032957 | 106.455 |
| w22 | 2 | 0.020941 | -0.886 |
| w23 | 36 | -0.00633 | 8.802 |
| w24 | 13 | -0.017563 | -1.176 |

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
| w1 | 5 | 0.095421 | 7.302 |
| w2 | 7 | 0.062026 | -0.26 |
| w3 | 15 | -0.09302 | -3.104 |
| w4 | 28 | -0.151324 | -14.831 |
| w5 | 22 | 0.052928 | -7.624 |
| w6 | 23 | -0.090003 | -34.749 |
| w7 | 5 | 0.166298 | 12.028 |
| w8 | 25 | -0.120193 | -19.951 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | 0.182027 | -1.765 |
| w11 | 0 | None | 0.0 |
| w12 | 20 | 0.010677 | 2.122 |
| w13 | 0 | None | 0.0 |
| w14 | 10 | 0.134092 | 31.221 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 13 | 0.019346 | -24.966 |
| w18 | 2 | -0.022993 | 8.813 |
| w19 | 0 | None | 0.0 |
| w20 | 12 | -0.144733 | -20.002 |
| w21 | 13 | -0.039118 | 28.79 |
| w22 | 2 | 0.042239 | -2.364 |
| w23 | 19 | 0.030002 | -2.001 |
| w24 | 4 | 0.007855 | -4.57 |

