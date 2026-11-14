# Backtest of N7-01_drift-only-near-high_1d_oos_sized

- Plan: `../../../../03_test_plan/overnight_run/plans_sized/N7-01_drift-only-near-high_1d_oos_sized.md`
- Config: `config.json` (a copy of the plan's config)
- Data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds A, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- ADAUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.02182 | -7.158 |
| w2 | 19 | -0.02623 | -10.686 |
| w3 | 6 | -0.204824 | -19.785 |
| w4 | 28 | 0.035902 | 31.998 |
| w5 | 18 | -0.028135 | -11.853 |
| w6 | 22 | 0.085787 | 104.191 |
| w7 | 14 | 0.131587 | 18.817 |
| w8 | 17 | -0.11486 | -19.546 |
| w9 | 12 | 0.215863 | 117.261 |
| w10 | 14 | -0.160439 | -20.245 |
| w11 | 17 | 0.050005 | 21.654 |
| w12 | 9 | -0.082406 | -12.287 |

- AVAXUSD: 11 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w2 | 14 | 0.069389 | 2.695 |
| w3 | 9 | -0.053227 | -14.237 |
| w4 | 19 | 0.089182 | 43.867 |
| w5 | 6 | -0.032886 | -6.925 |
| w6 | 23 | 0.171733 | 137.872 |
| w7 | 25 | 0.084006 | 11.6 |
| w8 | 12 | -0.158968 | -23.798 |
| w9 | 19 | 0.069659 | 33.076 |
| w10 | 9 | -0.100026 | -12.7 |
| w11 | 19 | -0.019676 | -1.065 |
| w12 | 14 | 0.098885 | 7.9 |

- w1 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 11 prefetch bars (<date> to <date>) -- required_bars=61. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- DOGEUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.016803 | -7.332 |
| w2 | 7 | 0.040751 | -0.069 |
| w3 | 11 | 0.07889 | 38.68 |
| w4 | 27 | 0.034792 | 12.363 |
| w5 | 19 | 0.019863 | -2.871 |
| w6 | 27 | -0.00367 | 13.614 |
| w7 | 27 | 0.165932 | 85.916 |
| w8 | 15 | -0.076018 | -12.792 |
| w9 | 30 | 0.171504 | 115.045 |
| w10 | 6 | -0.082151 | -11.484 |
| w11 | 22 | 0.017726 | 11.442 |
| w12 | 7 | 0.07433 | 3.601 |

- LINKUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.116516 | 8.254 |
| w2 | 15 | 0.020117 | -3.674 |
| w3 | 21 | -0.098387 | -19.157 |
| w4 | 27 | -0.106244 | -9.685 |
| w5 | 16 | 0.069913 | 9.041 |
| w6 | 25 | -0.041921 | 39.025 |
| w7 | 20 | -0.002809 | -6.426 |
| w8 | 15 | 0.00435 | -3.163 |
| w9 | 33 | 0.010307 | 29.364 |
| w10 | 11 | -0.031099 | -5.946 |
| w11 | 28 | 0.018022 | 26.948 |
| w12 | 5 | -0.041222 | -6.257 |

- SOLUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.103085 | 8.215 |
| w2 | 11 | -0.012733 | -8.68 |
| w3 | 13 | -0.096525 | -26.022 |
| w4 | 26 | -0.03656 | 2.868 |
| w5 | 12 | 0.107661 | 13.743 |
| w6 | 36 | 0.067485 | 153.755 |
| w7 | 20 | 0.130008 | 41.634 |
| w8 | 12 | 0.045785 | 8.238 |
| w9 | 23 | 0.028181 | 24.235 |
| w10 | 8 | 0.056484 | 6.924 |
| w11 | 31 | 0.006453 | 14.957 |
| w12 | 13 | 0.007549 | -5.02 |

- TRXUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.014215 | -7.022 |
| w2 | 27 | -0.068021 | -16.187 |
| w3 | 27 | -0.165854 | -29.585 |
| w4 | 32 | -0.052079 | 4.36 |
| w5 | 37 | -0.01524 | 0.695 |
| w6 | 33 | -0.075049 | 24.833 |
| w7 | 27 | 0.053216 | 23.032 |
| w8 | 27 | 0.06654 | 43.286 |
| w9 | 38 | 0.069892 | 132.739 |
| w10 | 13 | -0.043147 | -8.31 |
| w11 | 42 | -0.070059 | 19.025 |
| w12 | 5 | -0.037496 | -5.823 |

- UNIUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.036238 | -4.207 |
| w2 | 24 | 0.014909 | 2.852 |
| w3 | 18 | -0.108432 | -20.076 |
| w4 | 27 | -0.068366 | -13.649 |
| w5 | 20 | 0.030038 | -1.727 |
| w6 | 26 | -0.090411 | 2.135 |
| w7 | 14 | 0.15988 | 55.594 |
| w8 | 12 | -0.033789 | -3.424 |
| w9 | 37 | -0.082475 | 13.835 |
| w10 | 3 | -0.062834 | -5.646 |
| w11 | 28 | -0.13689 | -8.291 |
| w12 | 8 | -0.123712 | -13.13 |

- AAVEUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.067037 | 8.135 |
| w2 | 21 | 0.01679 | -2.142 |
| w3 | 15 | -0.029886 | -11.531 |
| w4 | 19 | -0.028239 | 7.626 |
| w5 | 16 | -0.031139 | -11.623 |
| w6 | 32 | -0.14864 | 8.573 |
| w7 | 15 | 0.054542 | 8.44 |
| w8 | 28 | -0.100577 | -4.981 |
| w9 | 31 | -0.057179 | 17.988 |
| w10 | 10 | -0.065353 | -8.303 |
| w11 | 29 | -0.048748 | 10.317 |
| w12 | 7 | -0.074377 | -7.232 |

- INJUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.09125 | -17.327 |
| w2 | 9 | 0.072758 | 8.683 |
| w3 | 28 | -0.085433 | -14.778 |
| w4 | 38 | 0.023617 | 140.753 |
| w5 | 22 | -0.001277 | -1.159 |
| w6 | 35 | 0.082403 | 197.363 |
| w7 | 24 | -0.038189 | -8.991 |
| w8 | 18 | -0.060621 | -14.588 |
| w9 | 20 | 0.03955 | 12.132 |
| w10 | 3 | -0.043509 | -7.885 |
| w11 | 29 | -0.033142 | 0.428 |
| w12 | 7 | -0.039857 | -7.449 |

