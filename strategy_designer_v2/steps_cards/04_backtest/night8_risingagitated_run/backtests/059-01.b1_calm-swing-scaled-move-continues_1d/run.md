# Backtest of 059-01.b1_calm-swing-scaled-move-continues_1d

- Plan: `../../../../03_test_plan/night8_risingagitated_run/plans/059-01.b1_calm-swing-scaled-move-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 46 | -0.109964 | -21.464 |
| w2 | 36 | 0.062747 | 14.643 |
| w3 | 33 | -0.068311 | -14.448 |
| w4 | 35 | 0.013554 | 29.541 |
| w5 | 68 | -0.054309 | -14.617 |
| w6 | 33 | 0.073042 | 39.887 |
| w7 | 57 | 0.006743 | 2.255 |
| w8 | 33 | 0.070316 | 32.73 |
| w9 | 35 | -0.082728 | -23.703 |
| w10 | 38 | 0.106911 | 31.429 |
| w11 | 20 | -0.061222 | -11.022 |
| w12 | 48 | -0.11365 | -21.182 |
| w13 | 24 | -0.010593 | -1.24 |
| w14 | 38 | 0.08868 | 36.789 |
| w15 | 12 | 0.215551 | 41.412 |
| w16 | 37 | 0.01714 | -0.273 |
| w17 | 19 | 0.094797 | 76.157 |
| w18 | 12 | 0.107175 | 19.389 |
| w19 | 1 | 0.165847 | 48.752 |
| w20 | 17 | 0.073934 | 15.469 |
| w21 | 39 | -0.04388 | 17.121 |
| w22 | 38 | -0.054587 | -16.753 |
| w23 | 51 | 0.05376 | 12.606 |
| w24 | 34 | -0.047352 | -3.627 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 39 | 0.036247 | 23.242 |
| w2 | 10 | 0.087144 | 17.736 |
| w3 | 35 | -0.06189 | -24.606 |
| w4 | 49 | -0.032846 | 11.091 |
| w5 | 61 | -0.143881 | -22.24 |
| w6 | 34 | 0.055146 | -0.05 |
| w7 | 47 | 0.059102 | 39.664 |
| w8 | 43 | -0.05149 | -4.315 |
| w9 | 42 | -0.059075 | -27.502 |
| w10 | 36 | 0.097803 | 71.873 |
| w11 | 14 | -0.091445 | 11.938 |
| w12 | 48 | -0.027245 | -6.965 |
| w13 | 22 | 0.130759 | 28.37 |
| w14 | 22 | 0.081237 | 29.251 |
| w15 | 39 | 0.091641 | 23.747 |
| w16 | 21 | 0.093839 | 61.531 |
| w17 | 28 | 0.057171 | 31.858 |
| w18 | 13 | 0.064852 | 15.33 |
| w19 | 6 | 0.224378 | 63.576 |
| w20 | 18 | 0.036208 | -3.156 |
| w21 | 32 | -0.261079 | -42.215 |
| w22 | 16 | -0.02263 | 0.119 |
| w23 | 26 | -0.006604 | 25.873 |
| w24 | 35 | -0.003896 | -8.955 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 58 | -0.171891 | -38.599 |
| w2 | 36 | 0.01904 | -0.532 |
| w3 | 47 | -0.08526 | -29.641 |
| w4 | 39 | -0.011242 | 2.65 |
| w5 | 37 | 0.092828 | 20.234 |
| w6 | 55 | -0.106623 | -33.501 |
| w7 | 55 | 0.019201 | 30.377 |
| w8 | 18 | 0.015844 | 16.959 |
| w9 | 57 | -0.101273 | -23.855 |
| w10 | 47 | -0.095352 | 0.225 |
| w11 | 5 | 0.012597 | -5.479 |
| w12 | 33 | -0.045399 | -7.232 |
| w13 | 35 | -0.043096 | -5.555 |
| w14 | 40 | 0.005362 | 4.85 |
| w15 | 28 | 0.088331 | 12.955 |
| w16 | 37 | 0.016781 | 9.964 |
| w17 | 18 | -0.063018 | 0.473 |
| w18 | 20 | 0.036147 | 8.248 |
| w19 | 20 | 0.012999 | -1.111 |
| w20 | 32 | 0.014668 | 10.971 |
| w21 | 27 | -0.090174 | -21.709 |
| w22 | 3 | 0.131089 | 6.44 |
| w23 | 44 | 0.068351 | 15.335 |
| w24 | 38 | -0.260227 | -39.446 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 32 | -0.266698 | -33.168 |
| w2 | 30 | 0.005097 | -2.369 |
| w3 | 53 | -0.124787 | -31.089 |
| w4 | 64 | -0.030572 | -13.733 |
| w5 | 62 | -0.002381 | 8.372 |
| w6 | 56 | -0.103995 | -1.051 |
| w7 | 47 | -0.003076 | 13.057 |
| w8 | 44 | -0.010012 | 5.925 |
| w9 | 58 | -0.081643 | -18.412 |
| w10 | 42 | -0.026985 | 30.004 |
| w11 | 11 | 0.05247 | 16.655 |
| w12 | 58 | -0.068627 | -22.99 |
| w14 | 30 | 0.089698 | 35.974 |
| w15 | 26 | 0.020235 | 1.156 |
| w16 | 29 | -0.034329 | -4.303 |
| w17 | 32 | -0.02545 | 6.954 |
| w18 | 20 | 0.030693 | 5.194 |
| w19 | 1 | 0.119439 | 1.675 |
| w20 | 24 | -0.114507 | -16.019 |
| w21 | 41 | 0.092016 | -8.373 |
| w22 | 29 | -0.028858 | -5.141 |
| w23 | 23 | 0.216432 | 80.806 |
| w24 | 12 | -0.120207 | 3.211 |

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
| w1 | 54 | -0.019156 | 0.746 |
| w2 | 5 | -0.028382 | 16.124 |
| w3 | 0 | -0.010749 | 0.0 |
| w4 | 0 | -0.03154 | 0.0 |
| w5 | 14 | -0.012979 | -46.002 |
| w6 | 39 | 0.07782 | 21.238 |
| w8 | 48 | -0.131529 | -16.46 |
| w9 | 49 | 0.006265 | 5.154 |
| w10 | 54 | 0.053013 | 28.894 |
| w11 | 0 | None | 0.0 |
| w12 | 58 | -0.093776 | -12.684 |
| w14 | 34 | -0.052507 | -42.323 |
| w15 | 44 | -0.036405 | -6.576 |
| w16 | 18 | 0.020731 | -3.189 |
| w17 | 28 | 0.150374 | 91.52 |
| w18 | 25 | 0.090168 | 27.041 |
| w19 | 32 | -0.017005 | -0.747 |
| w20 | 32 | 0.009423 | -4.744 |
| w21 | 24 | -0.026597 | 50.619 |
| w22 | 6 | -0.027514 | -0.427 |
| w23 | 56 | 0.058959 | 31.967 |
| w24 | 46 | -0.074469 | 12.652 |

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
| w1 | 51 | -0.048694 | -20.99 |
| w2 | 26 | -0.068738 | -15.455 |
| w3 | 58 | -0.041596 | -0.147 |
| w4 | 53 | -0.093256 | -21.879 |
| w5 | 31 | 0.096564 | 29.923 |
| w6 | 57 | -0.107479 | -24.349 |
| w7 | 54 | -0.100426 | -17.79 |
| w8 | 50 | 0.026992 | -0.161 |
| w9 | 25 | -0.048283 | -17.091 |
| w10 | 36 | 0.09857 | 36.174 |
| w11 | 12 | -0.004662 | 12.62 |
| w12 | 28 | 0.022532 | 1.526 |
| w13 | 25 | 0.094836 | 23.807 |
| w14 | 43 | -0.017662 | -16.457 |
| w15 | 35 | 0.048743 | 17.027 |
| w16 | 0 | None | 0.0 |
| w17 | 23 | -0.018467 | -7.611 |
| w18 | 18 | 0.038751 | 6.961 |
| w19 | 0 | None | 0.0 |
| w20 | 22 | -0.043109 | -10.509 |
| w21 | 21 | -0.118371 | -21.37 |
| w22 | 5 | -0.121185 | -12.759 |
| w23 | 45 | -0.036515 | -21.584 |
| w24 | 12 | -0.059271 | 18.216 |

