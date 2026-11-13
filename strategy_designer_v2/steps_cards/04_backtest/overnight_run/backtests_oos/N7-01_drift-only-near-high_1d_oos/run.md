# Backtest of N7-01_drift-only-near-high_1d_oos

- Plan: `../../../../03_test_plan/overnight_run/plans_oos/N7-01_drift-only-near-high_1d_oos.md`
- Config: `config.json` (a copy of the plan's config)
- Data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds A, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- ADAUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.02182 | -23.457 |
| w2 | 19 | -0.02623 | -32.55 |
| w3 | 6 | -0.204824 | -34.1 |
| w4 | 27 | 0.035902 | 57.856 |
| w5 | 18 | -0.028135 | -21.188 |
| w6 | 21 | 0.085787 | 118.163 |
| w7 | 15 | 0.131587 | 36.35 |
| w8 | 16 | -0.11486 | -34.566 |
| w9 | 14 | 0.215863 | 285.722 |
| w10 | 14 | -0.160439 | -69.038 |
| w11 | 17 | 0.050005 | 19.049 |
| w12 | 9 | -0.082406 | -23.589 |

- AVAXUSD: 11 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w2 | 14 | 0.069389 | 4.955 |
| w3 | 9 | -0.053227 | -28.566 |
| w4 | 19 | 0.089182 | 78.929 |
| w5 | 6 | -0.032886 | -11.866 |
| w6 | 20 | 0.171733 | 379.716 |
| w7 | 21 | 0.084006 | 21.695 |
| w8 | 14 | -0.158968 | -45.945 |
| w9 | 21 | 0.069659 | 75.655 |
| w10 | 9 | -0.100026 | -33.45 |
| w11 | 23 | -0.019676 | -9.288 |
| w12 | 13 | 0.098885 | 14.009 |

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
| w1 | 12 | -0.016803 | -18.992 |
| w2 | 7 | 0.040751 | -1.848 |
| w3 | 12 | 0.07889 | 11.153 |
| w4 | 31 | 0.034792 | 12.986 |
| w5 | 19 | 0.019863 | -5.023 |
| w6 | 27 | -0.00367 | 15.332 |
| w7 | 26 | 0.165932 | 132.632 |
| w8 | 18 | -0.076018 | -30.255 |
| w9 | 27 | 0.171504 | 329.681 |
| w10 | 6 | -0.082151 | -27.636 |
| w11 | 25 | 0.017726 | 4.164 |
| w12 | 8 | 0.07433 | 6.198 |

- LINKUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.116516 | 20.074 |
| w2 | 15 | 0.020117 | -13.745 |
| w3 | 21 | -0.098387 | -44.355 |
| w4 | 27 | -0.106244 | -19.994 |
| w5 | 17 | 0.069913 | 8.01 |
| w6 | 25 | -0.041921 | 59.619 |
| w7 | 22 | -0.002809 | -11.535 |
| w8 | 17 | 0.00435 | -11.267 |
| w9 | 33 | 0.010307 | 50.833 |
| w10 | 13 | -0.031099 | -20.121 |
| w11 | 25 | 0.018022 | 37.433 |
| w12 | 7 | -0.041222 | -13.194 |

- SOLUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.103085 | 18.476 |
| w2 | 11 | -0.012733 | -25.649 |
| w3 | 13 | -0.096525 | -49.471 |
| w4 | 29 | -0.03656 | 17.031 |
| w5 | 12 | 0.107661 | 25.822 |
| w6 | 35 | 0.067485 | 471.716 |
| w7 | 17 | 0.130008 | 76.317 |
| w8 | 13 | 0.045785 | 18.948 |
| w9 | 24 | 0.028181 | 40.941 |
| w10 | 9 | 0.056484 | 14.963 |
| w11 | 28 | 0.006453 | 21.814 |
| w12 | 13 | 0.007549 | -12.642 |

- TRXUSD: 11 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.014215 | -13.749 |
| w2 | 27 | -0.068021 | -39.781 |
| w3 | 26 | -0.165854 | -31.449 |
| w4 | 31 | -0.052079 | -0.215 |
| w5 | 35 | -0.01524 | 2.907 |
| w6 | 28 | -0.075049 | 14.254 |
| w7 | 24 | 0.053216 | 17.238 |
| w8 | 22 | 0.06654 | 33.671 |
| w9 | 37 | 0.069892 | 68.467 |
| w11 | 34 | -0.070059 | 16.926 |
| w12 | 5 | -0.037496 | -4.582 |

- w10 not run: the engine stopped.

```
  File "/usr/local/lib/python3.13/json/decoder.py", line 361, in raw_decode
    obj, end = self.scan_once(s, idx)
               ~~~~~~~~~~~~~~^^^^^^^^
json.decoder.JSONDecodeError: Invalid control character at: line 485 column 44 (char 16419)
```

- UNIUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.036238 | -10.297 |
| w2 | 26 | 0.014909 | -1.774 |
| w3 | 18 | -0.108432 | -41.943 |
| w4 | 26 | -0.068366 | -23.636 |
| w5 | 20 | 0.030038 | -4.947 |
| w6 | 26 | -0.090411 | 2.907 |
| w7 | 14 | 0.15988 | 121.08 |
| w8 | 14 | -0.033789 | -25.562 |
| w9 | 41 | -0.082475 | 45.117 |
| w10 | 3 | -0.062834 | -14.712 |
| w11 | 31 | -0.13689 | -31.3 |
| w12 | 8 | -0.123712 | -44.396 |

- AAVEUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.067037 | -6.494 |
| w2 | 27 | 0.01679 | -19.482 |
| w3 | 15 | -0.029886 | -28.202 |
| w4 | 20 | -0.028239 | 1.57 |
| w5 | 18 | -0.031139 | -20.462 |
| w6 | 34 | -0.14864 | 3.682 |
| w7 | 16 | 0.054542 | 6.951 |
| w8 | 27 | -0.100577 | -12.283 |
| w9 | 36 | -0.057179 | 42.733 |
| w10 | 10 | -0.065353 | -26.478 |
| w11 | 28 | -0.048748 | 30.568 |
| w12 | 7 | -0.074377 | -17.397 |

- INJUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.09125 | -60.09 |
| w2 | 12 | 0.072758 | 13.615 |
| w3 | 27 | -0.085433 | -48.113 |
| w4 | 32 | 0.023617 | 493.941 |
| w5 | 23 | -0.001277 | -11.935 |
| w6 | 34 | 0.082403 | 531.952 |
| w7 | 24 | -0.038189 | -35.314 |
| w8 | 19 | -0.060621 | -38.62 |
| w9 | 23 | 0.03955 | 24.099 |
| w10 | 3 | -0.043509 | -22.341 |
| w11 | 33 | -0.033142 | -10.131 |
| w12 | 7 | -0.039857 | -18.245 |

