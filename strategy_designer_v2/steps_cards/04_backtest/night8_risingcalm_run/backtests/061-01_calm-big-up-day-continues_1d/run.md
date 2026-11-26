# Backtest of 061-01_calm-big-up-day-continues_1d

- Plan: `../../../../03_test_plan/night8_risingcalm_run/plans/061-01_calm-big-up-day-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 46 | -0.002986 | -21.611 |
| w2 | 34 | 0.001561 | -20.394 |
| w3 | 32 | 0.158889 | 43.639 |
| w4 | 44 | 0.083218 | -11.181 |
| w5 | 51 | -0.057031 | -21.934 |
| w6 | 27 | 0.077825 | 13.995 |
| w7 | 66 | -0.005585 | 1.797 |
| w8 | 38 | -0.007896 | 25.843 |
| w9 | 43 | -0.077224 | -12.181 |
| w10 | 42 | -0.076299 | -40.062 |
| w11 | 9 | 0.023075 | -16.413 |
| w12 | 32 | 0.010867 | -23.0 |
| w13 | 15 | -0.036181 | 5.615 |
| w14 | 36 | 0.088618 | 5.509 |
| w15 | 8 | 0.083698 | 49.03 |
| w16 | 33 | -0.046969 | -7.015 |
| w17 | 33 | 0.042849 | 58.819 |
| w18 | 12 | 0.037331 | 20.233 |
| w19 | 7 | 0.17026 | 40.973 |
| w20 | 10 | 0.079492 | 15.408 |
| w21 | 39 | 0.189361 | 15.521 |
| w22 | 30 | 0.034726 | -16.052 |
| w23 | 62 | -0.046128 | 9.536 |
| w24 | 32 | 0.093601 | -19.89 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 50 | 0.02956 | -3.701 |
| w2 | 9 | -0.075691 | -23.179 |
| w3 | 34 | 0.141706 | -2.123 |
| w4 | 51 | 0.002561 | -9.576 |
| w5 | 61 | -0.1221 | -0.819 |
| w6 | 47 | -0.010944 | -11.232 |
| w7 | 57 | -0.07564 | 27.859 |
| w8 | 38 | -0.101389 | -20.819 |
| w9 | 44 | 0.017484 | 8.872 |
| w10 | 32 | -0.021143 | 37.531 |
| w11 | 10 | -0.007132 | 22.555 |
| w12 | 41 | -0.103114 | -25.001 |
| w13 | 24 | -0.008565 | 77.322 |
| w14 | 20 | 0.076681 | 35.294 |
| w15 | 38 | 0.050438 | -3.351 |
| w16 | 14 | -0.056156 | 86.95 |
| w17 | 20 | 0.031512 | 35.913 |
| w18 | 16 | -0.062805 | 32.009 |
| w19 | 11 | 0.014165 | 32.549 |
| w20 | 12 | 0.053999 | 10.742 |
| w21 | 26 | 0.085235 | -27.141 |
| w22 | 11 | -0.123324 | -13.561 |
| w23 | 41 | 0.155999 | -34.899 |
| w24 | 30 | 0.082531 | 8.482 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 51 | -0.057302 | -17.057 |
| w2 | 34 | -0.08287 | -28.728 |
| w3 | 39 | 0.09722 | -42.709 |
| w4 | 43 | -0.0101 | -11.036 |
| w5 | 31 | 0.067912 | 2.16 |
| w6 | 59 | -0.060187 | -17.121 |
| w7 | 57 | -0.126085 | 25.429 |
| w8 | 12 | -0.002121 | 16.856 |
| w9 | 53 | -0.001899 | 4.927 |
| w10 | 45 | -0.257318 | -31.789 |
| w11 | 11 | 0.00087 | 3.592 |
| w12 | 34 | 0.085417 | -11.839 |
| w13 | 36 | -0.102089 | 8.243 |
| w14 | 34 | -0.065612 | 44.616 |
| w15 | 27 | 0.181 | 6.527 |
| w16 | 27 | -0.087765 | 32.194 |
| w17 | 22 | -0.014874 | -23.203 |
| w18 | 19 | -0.048685 | 16.057 |
| w19 | 19 | 0.129114 | 2.767 |
| w20 | 28 | -0.023074 | 23.145 |
| w21 | 29 | 0.048658 | 10.9 |
| w22 | 4 | 0.09329 | 7.067 |
| w23 | 56 | -0.04641 | 4.682 |
| w24 | 32 | -0.118689 | 4.859 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.068513 | -14.385 |
| w2 | 24 | -0.07347 | -13.675 |
| w3 | 39 | -0.095576 | -16.105 |
| w4 | 44 | -0.108364 | 8.541 |
| w5 | 53 | 0.04672 | 30.985 |
| w6 | 52 | -0.135672 | -12.402 |
| w7 | 51 | -0.154488 | -15.671 |
| w8 | 40 | -0.124472 | 7.865 |
| w9 | 59 | -0.029578 | -29.542 |
| w10 | 53 | -0.251208 | -0.913 |
| w11 | 7 | -0.073012 | 22.663 |
| w12 | 47 | -0.019792 | -20.866 |
| w14 | 27 | -0.063864 | -9.153 |
| w15 | 17 | 0.146855 | 38.909 |
| w16 | 20 | -0.082409 | 53.845 |
| w17 | 32 | -0.204927 | -5.921 |
| w18 | 22 | 0.004097 | -15.777 |
| w19 | 3 | 0.040615 | -19.723 |
| w20 | 15 | -0.152215 | 2.485 |
| w21 | 40 | 0.126371 | -3.014 |
| w22 | 22 | -0.037956 | 37.516 |
| w23 | 31 | 0.035365 | 23.264 |
| w24 | 15 | -0.007795 | -3.681 |

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
| w1 | 45 | 0.016266 | -24.06 |
| w2 | 5 | -0.091394 | -26.425 |
| w3 | 0 | -0.085841 | 0.0 |
| w4 | 0 | -0.25212 | 0.0 |
| w5 | 12 | -0.044403 | 47.054 |
| w6 | 35 | -0.06403 | 37.321 |
| w8 | 53 | -0.212961 | -16.389 |
| w9 | 39 | 0.01367 | 27.354 |
| w10 | 51 | -0.102063 | -11.852 |
| w11 | 0 | None | 0.0 |
| w12 | 55 | -0.063223 | -23.596 |
| w14 | 30 | 0.010006 | -41.398 |
| w15 | 41 | 0.122322 | -39.145 |
| w16 | 13 | 0.050275 | -9.689 |
| w17 | 31 | 0.112531 | 91.192 |
| w18 | 22 | 0.041525 | 44.546 |
| w19 | 24 | -0.085015 | -14.095 |
| w20 | 18 | -0.111028 | 16.516 |
| w21 | 20 | 0.077113 | 101.019 |
| w22 | 6 | -0.040194 | 8.621 |
| w23 | 53 | 0.011521 | 24.259 |
| w24 | 53 | 0.067933 | -3.022 |

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
| w1 | 37 | 0.118179 | 5.62 |
| w2 | 18 | 0.061789 | -10.904 |
| w3 | 49 | -0.043011 | 10.767 |
| w4 | 47 | -0.133046 | -3.257 |
| w5 | 43 | 0.044776 | 40.874 |
| w6 | 53 | -0.102341 | -22.623 |
| w7 | 52 | -0.077237 | -47.136 |
| w8 | 43 | -0.078969 | 31.604 |
| w9 | 38 | 0.126928 | 15.796 |
| w10 | 40 | -0.052808 | 34.563 |
| w11 | 18 | 0.126414 | 13.689 |
| w12 | 31 | 0.02414 | -36.389 |
| w13 | 27 | -0.010059 | 3.164 |
| w14 | 36 | 0.05614 | -40.921 |
| w15 | 29 | -0.011476 | 17.688 |
| w16 | 0 | None | 0.0 |
| w17 | 27 | -0.026014 | -11.782 |
| w18 | 16 | -0.065272 | 19.827 |
| w19 | 0 | None | 0.0 |
| w20 | 23 | -0.036267 | -0.33 |
| w21 | 22 | 0.130288 | 26.499 |
| w22 | 6 | -0.080628 | 4.658 |
| w23 | 44 | 0.066767 | -18.777 |
| w24 | 13 | -0.091784 | -40.408 |

