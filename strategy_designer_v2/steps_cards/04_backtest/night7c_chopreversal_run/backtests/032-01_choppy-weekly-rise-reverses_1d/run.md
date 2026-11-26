# Backtest of 032-01_choppy-weekly-rise-reverses_1d

- Plan: `../../../../03_test_plan/night7c_chopreversal_run/plans/032-01_choppy-weekly-rise-reverses_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.000647 | 4.478 |
| w2 | 5 | 0.073594 | 13.97 |
| w3 | 12 | 0.152418 | 12.959 |
| w4 | 9 | -0.090701 | -16.002 |
| w5 | 0 | None | 0.0 |
| w6 | 15 | -0.110522 | -16.346 |
| w7 | 0 | None | 0.0 |
| w8 | 5 | 0.107566 | 2.171 |
| w9 | 5 | -0.062121 | -2.527 |
| w10 | 6 | 0.052903 | 0.135 |
| w11 | 22 | -0.077387 | -27.456 |
| w12 | 12 | -0.163266 | -19.9 |
| w13 | 17 | -0.00642 | 4.803 |
| w14 | 4 | 0.012742 | 6.197 |
| w15 | 25 | -0.137432 | -18.216 |
| w16 | 14 | -0.027041 | -8.986 |
| w17 | 13 | -0.050633 | -20.612 |
| w18 | 16 | 0.061238 | -4.569 |
| w19 | 20 | 0.08794 | -9.182 |
| w20 | 26 | -0.004027 | -8.285 |
| w21 | 6 | 0.013586 | -8.859 |
| w22 | 13 | 0.024644 | -8.84 |
| w23 | 3 | 0.021178 | -3.194 |
| w24 | 10 | -0.040385 | 4.517 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.038562 | 4.633 |
| w2 | 9 | -0.065132 | -3.651 |
| w3 | 12 | -0.033212 | -1.024 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 9 | 0.05003 | -0.172 |
| w7 | 0 | None | 0.0 |
| w8 | 8 | -0.052265 | -1.999 |
| w9 | 5 | 0.044273 | 1.109 |
| w10 | 5 | 0.062179 | 2.385 |
| w11 | 27 | -0.141898 | -51.755 |
| w12 | 8 | -0.037811 | -4.22 |
| w13 | 5 | 0.100187 | 9.904 |
| w14 | 10 | -0.079909 | -0.547 |
| w15 | 10 | -0.005035 | 8.833 |
| w16 | 13 | 0.080534 | 1.726 |
| w17 | 22 | 0.16079 | 14.727 |
| w18 | 13 | -0.02306 | -8.106 |
| w19 | 15 | 0.130816 | 0.792 |
| w20 | 14 | -0.090412 | -19.332 |
| w21 | 20 | 0.066168 | -17.006 |
| w22 | 17 | -0.02325 | 7.309 |
| w23 | 4 | 0.120769 | -0.803 |
| w24 | 10 | 0.011666 | 0.091 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 10 | 0.02157 | 3.092 |
| w3 | 9 | -0.145513 | -16.138 |
| w4 | 6 | 0.037564 | -9.067 |
| w5 | 10 | 0.058101 | 8.244 |
| w6 | 2 | 0.035514 | 1.234 |
| w7 | 0 | None | 0.0 |
| w8 | 22 | 0.053236 | -23.946 |
| w9 | 0 | None | 0.0 |
| w10 | 3 | 0.030726 | -0.667 |
| w11 | 24 | -0.110919 | -27.089 |
| w12 | 9 | 0.025419 | -3.555 |
| w13 | 8 | -0.023731 | -5.297 |
| w14 | 11 | -0.03216 | 15.376 |
| w15 | 17 | -0.083029 | -0.141 |
| w16 | 9 | 0.060345 | 7.39 |
| w17 | 19 | 0.008981 | -24.877 |
| w18 | 12 | -0.145424 | -6.263 |
| w19 | 18 | 0.089334 | -10.477 |
| w20 | 11 | -0.075112 | -4.014 |
| w21 | 22 | -0.042962 | -40.917 |
| w22 | 26 | 0.042132 | 6.911 |
| w23 | 2 | 0.05089 | -2.308 |
| w24 | 12 | 0.098268 | 7.628 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.041468 | 0.666 |
| w2 | 10 | 0.089953 | -4.018 |
| w3 | 10 | -0.037089 | -6.678 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 11 | 0.049486 | -4.634 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | 0.060182 | 2.135 |
| w9 | 0 | None | 0.0 |
| w10 | 5 | 0.120378 | -0.507 |
| w11 | 23 | -0.171188 | -30.928 |
| w12 | 12 | -0.041818 | 1.235 |
| w14 | 6 | 0.006316 | 20.813 |
| w15 | 14 | 0.140095 | 11.948 |
| w16 | 11 | 0.007404 | -5.833 |
| w17 | 19 | 0.123075 | 6.963 |
| w18 | 17 | 0.11366 | 7.825 |
| w19 | 27 | 0.026345 | 12.558 |
| w20 | 16 | 0.046738 | -12.479 |
| w21 | 19 | -0.033214 | -6.165 |
| w22 | 20 | 0.180645 | -0.8 |
| w23 | 9 | 0.092991 | 6.868 |
| w24 | 30 | 0.024742 | -22.64 |

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
| w1 | 1 | 0.080138 | 2.238 |
| w2 | 0 | 0.112777 | 0.0 |
| w3 | 0 | -0.21501 | 0.0 |
| w4 | 0 | -0.027 | 0.0 |
| w5 | 2 | -0.001193 | 1.494 |
| w6 | 5 | 0.010773 | -0.348 |
| w8 | 2 | -0.018708 | 1.931 |
| w9 | 11 | -0.066497 | -1.103 |
| w10 | 0 | None | 0.0 |
| w11 | 24 | 0.021431 | -43.013 |
| w12 | 0 | None | 0.0 |
| w14 | 8 | -0.249184 | -11.91 |
| w15 | 9 | -0.033978 | 4.502 |
| w16 | 18 | 0.052865 | -4.948 |
| w17 | 7 | 0.060167 | 2.686 |
| w18 | 10 | 0.086493 | 0.006 |
| w19 | 16 | 0.099814 | 26.369 |
| w20 | 19 | -0.283084 | -34.622 |
| w21 | 4 | 0.071002 | 2.894 |
| w22 | 28 | -3.2e-05 | 1.001 |
| w23 | 4 | 0.113522 | 5.65 |
| w24 | 4 | -0.034088 | 2.708 |

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
| w1 | 12 | 0.026941 | -15.733 |
| w2 | 10 | 0.08194 | 11.588 |
| w3 | 9 | 0.039524 | -6.24 |
| w4 | 3 | 0.120803 | 0.626 |
| w5 | 14 | -0.069183 | -6.839 |
| w6 | 2 | 0.058677 | 10.591 |
| w7 | 0 | -0.022989 | 0.0 |
| w8 | 3 | 0.020849 | 0.735 |
| w9 | 10 | 0.098879 | 10.475 |
| w10 | 7 | 0.074244 | 1.001 |
| w11 | 21 | -0.343785 | -49.621 |
| w12 | 16 | -0.127757 | 13.008 |
| w13 | 9 | 0.028913 | 10.371 |
| w14 | 3 | 0.085069 | 17.432 |
| w15 | 9 | -0.11287 | -6.21 |
| w16 | 21 | -0.140159 | -46.207 |
| w17 | 19 | 0.112076 | 26.103 |
| w18 | 11 | 0.036873 | 0.06 |
| w19 | 28 | -0.090025 | -10.74 |
| w20 | 10 | -0.239785 | -28.189 |
| w21 | 17 | -0.029456 | -34.66 |
| w22 | 24 | 0.066109 | 9.368 |
| w23 | 5 | -0.057394 | -3.229 |
| w24 | 12 | 0.122507 | -13.811 |

