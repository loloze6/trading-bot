# Backtest of N1-04_rebound-after-large-drop_1d_oos

- Plan: `../../../../03_test_plan/overnight_run/plans_oos/N1-04_rebound-after-large-drop_1d_oos.md`
- Config: `config.json` (a copy of the plan's config)
- Data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds A, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- ADAUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 35 | -0.043552 | -31.72 |
| w2 | 31 | 0.016542 | -19.611 |
| w3 | 32 | 0.007805 | -29.615 |
| w4 | 24 | 0.110029 | 28.98 |
| w5 | 33 | -0.032046 | -22.834 |
| w6 | 24 | 0.080572 | 31.874 |
| w7 | 29 | 0.15827 | 30.388 |
| w8 | 35 | 0.012762 | -14.076 |
| w9 | 24 | -0.076986 | -10.691 |
| w10 | 27 | 0.036649 | 13.157 |
| w11 | 38 | 0.023649 | 0.5 |
| w12 | 39 | 0.052276 | -16.479 |

- AVAXUSD: 11 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w2 | 33 | -0.075998 | -53.796 |
| w3 | 32 | 0.043786 | -24.045 |
| w4 | 24 | -0.052688 | -7.304 |
| w5 | 38 | 0.012294 | -18.389 |
| w6 | 24 | -0.084077 | -0.827 |
| w7 | 26 | 0.140769 | 34.677 |
| w8 | 30 | -0.112862 | -38.513 |
| w9 | 34 | -0.065711 | -13.751 |
| w10 | 30 | -0.09703 | -47.296 |
| w11 | 39 | -0.050884 | -17.222 |
| w12 | 31 | 0.062762 | 4.598 |

- w1 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 11 prefetch bars (<date> to <date>) -- required_bars=24. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- DOGEUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | 0.102081 | 19.464 |
| w2 | 28 | -0.014246 | -38.487 |
| w3 | 27 | 0.081488 | 24.752 |
| w4 | 32 | -0.033374 | -10.879 |
| w5 | 30 | 0.0228 | -10.949 |
| w6 | 28 | 0.064895 | 14.705 |
| w7 | 28 | 0.028595 | 17.231 |
| w8 | 28 | -0.062131 | -26.448 |
| w9 | 23 | -0.134778 | -24.713 |
| w10 | 26 | 0.006383 | -17.773 |
| w11 | 30 | -0.000964 | -0.77 |
| w12 | 31 | 0.08241 | 7.965 |

- LINKUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 37 | -0.051133 | -37.677 |
| w2 | 34 | -0.065186 | -41.256 |
| w3 | 32 | 0.071683 | -4.22 |
| w4 | 29 | 0.027296 | 4.638 |
| w5 | 29 | -0.036944 | -17.632 |
| w6 | 26 | -0.018878 | 7.048 |
| w7 | 29 | 0.123106 | 17.387 |
| w8 | 32 | -0.025876 | -23.23 |
| w9 | 27 | -0.105943 | -18.431 |
| w10 | 26 | -0.03775 | -28.474 |
| w11 | 33 | -0.066202 | -10.337 |
| w12 | 31 | 0.10924 | 13.968 |

- SOLUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 37 | -0.021566 | -32.62 |
| w2 | 37 | -0.022872 | -35.275 |
| w3 | 28 | -0.119721 | -86.84 |
| w4 | 22 | -0.023722 | -0.65 |
| w5 | 38 | -0.109363 | -33.381 |
| w6 | 19 | 0.008146 | 21.144 |
| w7 | 26 | 0.098475 | 28.925 |
| w8 | 35 | -0.01835 | -14.939 |
| w9 | 30 | -0.019618 | -2.01 |
| w10 | 30 | -0.018952 | -15.411 |
| w11 | 35 | -0.064004 | -11.13 |
| w12 | 31 | 0.070674 | -0.358 |

- TRXUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 33 | 0.038441 | -1.777 |
| w2 | 26 | 0.204194 | 62.65 |
| w3 | 24 | 0.125103 | 4.553 |
| w4 | 28 | 0.152608 | 31.122 |
| w5 | 30 | -0.059904 | -10.487 |
| w6 | 22 | 0.187278 | 26.032 |
| w7 | 30 | -0.03468 | -8.542 |
| w8 | 24 | -0.028563 | -2.235 |
| w9 | 25 | -0.0282 | -2.707 |
| w10 | 33 | 0.077106 | 6.707 |
| w11 | 21 | 0.014556 | 2.34 |
| w12 | 28 | 0.085205 | -1.828 |

- UNIUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 38 | -0.047697 | -42.563 |
| w2 | 31 | -0.001126 | -8.042 |
| w3 | 28 | 0.089213 | 3.679 |
| w4 | 33 | 0.064951 | 11.048 |
| w5 | 33 | -0.108371 | -33.347 |
| w6 | 24 | 0.171101 | 49.172 |
| w7 | 23 | -0.131897 | -54.233 |
| w8 | 33 | 0.012965 | -10.634 |
| w9 | 28 | -0.046092 | -9.744 |
| w10 | 35 | 0.089227 | -11.455 |
| w11 | 34 | -0.036304 | -3.578 |
| w12 | 29 | 0.002013 | -4.477 |

- AAVEUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | -0.042689 | -32.366 |
| w2 | 33 | -0.045918 | -38.1 |
| w3 | 31 | 0.127278 | 7.47 |
| w4 | 28 | 0.097023 | 19.888 |
| w5 | 32 | -0.050265 | -25.502 |
| w6 | 24 | -0.030251 | 0.716 |
| w7 | 27 | 0.051743 | -18.575 |
| w8 | 34 | -0.120854 | -20.289 |
| w9 | 27 | 0.079009 | 43.723 |
| w10 | 31 | 0.1089 | 13.339 |
| w11 | 32 | 0.046921 | 24.448 |
| w12 | 30 | -0.012645 | -28.732 |

- INJUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 38 | -0.043842 | -44.82 |
| w2 | 33 | 0.040432 | -23.212 |
| w3 | 22 | 0.099412 | -2.677 |
| w4 | 17 | 0.102292 | 60.477 |
| w5 | 37 | 0.012818 | -2.355 |
| w6 | 21 | 0.021215 | 38.319 |
| w7 | 33 | 0.011767 | -15.19 |
| w8 | 37 | 0.046727 | -12.359 |
| w9 | 36 | -0.066525 | -23.229 |
| w10 | 28 | -0.068214 | -45.613 |
| w11 | 36 | -0.137592 | -34.367 |
| w12 | 35 | 0.037522 | -19.261 |

