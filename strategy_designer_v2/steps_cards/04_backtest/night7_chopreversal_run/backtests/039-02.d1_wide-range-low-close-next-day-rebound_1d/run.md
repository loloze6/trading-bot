# Backtest of 039-02.d1_wide-range-low-close-next-day-rebound_1d

- Plan: `../../../../03_test_plan/night7_chopreversal_run/plans/039-02.d1_wide-range-low-close-next-day-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | -0.031822 | -6.507 |
| w2 | 42 | 0.047265 | -8.431 |
| w3 | 38 | 0.195579 | 21.947 |
| w4 | 20 | 0.078399 | 13.619 |
| w5 | 0 | None | 0.0 |
| w6 | 45 | 0.262796 | 79.631 |
| w7 | 0 | None | 0.0 |
| w8 | 23 | -0.057679 | -3.547 |
| w9 | 27 | 0.013588 | -3.335 |
| w10 | 28 | -0.031843 | 5.301 |
| w11 | 67 | -0.020547 | 16.733 |
| w12 | 31 | 0.141948 | 19.099 |
| w13 | 62 | -0.010249 | -7.111 |
| w14 | 34 | 0.150688 | 9.304 |
| w15 | 61 | -0.101618 | -3.016 |
| w16 | 41 | 0.107778 | 14.52 |
| w17 | 40 | 0.035468 | 23.507 |
| w18 | 63 | 0.023464 | -5.678 |
| w19 | 71 | 0.016588 | 13.133 |
| w20 | 67 | 0.147622 | 22.783 |
| w21 | 33 | 0.066352 | 22.547 |
| w22 | 42 | 0.153901 | 21.656 |
| w23 | 4 | -0.014249 | 0.811 |
| w24 | 45 | 0.024021 | -11.773 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.110875 | -13.267 |
| w2 | 82 | 0.092707 | -5.463 |
| w3 | 39 | 0.260429 | 29.858 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 37 | 0.060572 | 15.928 |
| w7 | 0 | None | 0.0 |
| w8 | 26 | 0.086243 | 10.88 |
| w9 | 21 | 0.065569 | 4.299 |
| w10 | 32 | 0.039594 | 17.693 |
| w11 | 69 | 0.083621 | 55.523 |
| w12 | 17 | 0.053898 | 5.48 |
| w13 | 40 | -0.052617 | -10.43 |
| w14 | 59 | 0.196388 | 18.222 |
| w15 | 36 | 0.057274 | 6.458 |
| w16 | 58 | -0.035929 | -13.744 |
| w17 | 47 | 0.032984 | 10.447 |
| w18 | 56 | 0.030787 | 11.061 |
| w19 | 64 | -0.153471 | -23.922 |
| w20 | 72 | 0.12327 | 3.579 |
| w21 | 55 | 0.051048 | 19.71 |
| w22 | 61 | 0.125429 | -0.878 |
| w23 | 39 | 0.0805 | 33.463 |
| w24 | 36 | 0.016875 | -7.834 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 42 | 0.000111 | -13.952 |
| w3 | 31 | 0.111474 | 16.752 |
| w4 | 21 | -0.013675 | -2.505 |
| w5 | 46 | 0.045704 | -0.152 |
| w6 | 4 | 0.151587 | 7.749 |
| w7 | 0 | None | 0.0 |
| w8 | 78 | 0.142599 | 49.462 |
| w9 | 0 | None | 0.0 |
| w10 | 14 | 0.005753 | 0.611 |
| w11 | 78 | -0.086922 | 0.076 |
| w12 | 38 | -0.031055 | -7.942 |
| w13 | 39 | 0.000464 | -1.082 |
| w14 | 42 | 0.144668 | 9.168 |
| w15 | 53 | 0.080614 | 6.276 |
| w16 | 36 | 0.069974 | 2.971 |
| w17 | 58 | 0.054847 | 20.158 |
| w18 | 47 | 0.108221 | 10.737 |
| w19 | 52 | 0.128778 | 36.937 |
| w20 | 48 | 0.072454 | -3.477 |
| w21 | 56 | -0.041349 | 5.693 |
| w22 | 86 | 0.03075 | -2.985 |
| w23 | 18 | 0.079071 | 8.16 |
| w24 | 38 | -0.050815 | -10.024 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 46 | -0.072078 | -18.115 |
| w2 | 44 | -0.029294 | -10.846 |
| w3 | 21 | 0.097377 | 8.401 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 20 | 0.002106 | -0.965 |
| w7 | 0 | None | 0.0 |
| w8 | 14 | 0.028287 | 0.766 |
| w9 | 4 | -0.00038 | -1.214 |
| w10 | 9 | 0.099684 | 8.087 |
| w11 | 72 | 0.105936 | 58.315 |
| w12 | 21 | -0.005845 | -6.205 |
| w14 | 45 | 0.094887 | -0.976 |
| w15 | 38 | 0.009711 | 1.512 |
| w16 | 48 | 0.062553 | 3.089 |
| w17 | 40 | -0.05342 | -7.794 |
| w18 | 61 | 0.217828 | 37.568 |
| w19 | 84 | 0.229428 | 30.708 |
| w20 | 62 | 0.215844 | 44.588 |
| w21 | 41 | 0.058862 | 9.635 |
| w22 | 58 | 0.050723 | 13.65 |
| w23 | 44 | -0.169861 | -23.03 |
| w24 | 67 | -0.097832 | -4.877 |

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
| w1 | 9 | 0.022115 | -1.051 |
| w2 | 22 | -0.02907 | -18.676 |
| w3 | 0 | 0.088618 | 0.0 |
| w4 | 0 | 0.029553 | 0.0 |
| w5 | 38 | -0.077633 | -4.063 |
| w6 | 26 | -0.018935 | -1.937 |
| w8 | 6 | 0.079622 | 2.361 |
| w9 | 23 | 0.02254 | -0.859 |
| w10 | 11 | 0.03175 | 4.535 |
| w11 | 75 | 0.027449 | 55.334 |
| w12 | 4 | -0.000119 | -0.533 |
| w14 | 27 | 0.184474 | 24.412 |
| w15 | 30 | 0.132079 | 15.346 |
| w16 | 66 | 0.039052 | 0.126 |
| w17 | 46 | 0.038185 | 10.099 |
| w18 | 48 | 0.129553 | 11.295 |
| w19 | 50 | -0.038077 | -8.966 |
| w20 | 46 | -0.007819 | 4.914 |
| w21 | 50 | 0.062398 | 81.194 |
| w22 | 78 | 0.005414 | -2.514 |
| w23 | 14 | 0.091164 | 10.096 |
| w24 | 21 | 0.015238 | -4.748 |

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
| w1 | 27 | 0.216147 | 29.544 |
| w2 | 47 | -0.009119 | -11.096 |
| w3 | 20 | 0.205888 | 14.393 |
| w4 | 11 | -0.013541 | -0.738 |
| w5 | 34 | 0.161799 | 19.97 |
| w6 | 15 | 0.04688 | 3.952 |
| w7 | 9 | -0.04568 | -5.107 |
| w8 | 14 | 0.138898 | 5.251 |
| w9 | 35 | 0.078303 | 1.459 |
| w10 | 32 | -0.133822 | -13.391 |
| w11 | 71 | -0.011043 | 31.662 |
| w12 | 48 | 0.044181 | 6.991 |
| w13 | 42 | 0.060049 | 7.893 |
| w14 | 33 | 0.121728 | 7.073 |
| w15 | 43 | 0.029083 | -2.112 |
| w16 | 85 | 0.060701 | 46.156 |
| w17 | 51 | -0.065949 | -20.534 |
| w18 | 54 | 0.175801 | 32.56 |
| w19 | 84 | 0.158656 | 14.597 |
| w20 | 63 | -0.073888 | -5.087 |
| w21 | 74 | -0.086038 | -0.767 |
| w22 | 81 | -0.075569 | -23.264 |
| w23 | 20 | -0.094705 | -9.108 |
| w24 | 69 | 0.048765 | 69.614 |

