# Backtest of N4-04_dip-rebound-spans-days_1d_oos

- Plan: `../../../../03_test_plan/overnight_run/plans_oos/N4-04_dip-rebound-spans-days_1d_oos.md`
- Config: `config.json` (a copy of the plan's config)
- Data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds A, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- ADAUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.031607 | -6.516 |
| w2 | 2 | -0.031951 | -6.503 |
| w3 | 2 | 0.106481 | 9.291 |
| w4 | 9 | 0.028409 | 7.864 |
| w5 | 0 | 0.000644 | 0.0 |
| w6 | 17 | 0.132472 | 51.387 |
| w7 | 9 | 0.082458 | 8.269 |
| w8 | 1 | -0.128358 | -2.05 |
| w9 | 6 | 0.022152 | 14.389 |
| w10 | 5 | -0.039625 | -10.449 |
| w11 | 20 | -0.059161 | -18.096 |
| w12 | 2 | -0.022304 | -5.623 |

- AVAXUSD: 11 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w2 | 2 | -0.05909 | -12.196 |
| w3 | 0 | None | 0.0 |
| w4 | 11 | 0.009725 | 5.707 |
| w5 | 0 | None | 0.0 |
| w6 | 13 | -0.008321 | 12.607 |
| w7 | 9 | 0.171595 | 37.636 |
| w8 | 0 | -0.071904 | 0.0 |
| w9 | 23 | -0.110678 | -27.089 |
| w10 | 1 | -0.153213 | -14.008 |
| w11 | 18 | -0.097528 | -23.322 |
| w12 | 8 | -0.04072 | -11.946 |

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
| w1 | 1 | 0.031562 | 0.274 |
| w2 | 2 | -0.008314 | -12.306 |
| w3 | 14 | -0.002268 | -14.834 |
| w4 | 0 | 0.056618 | 0.0 |
| w5 | 9 | -0.02648 | -5.694 |
| w6 | 16 | 0.109222 | 29.071 |
| w7 | 13 | -0.026845 | -23.109 |
| w8 | 0 | -0.093096 | 0.0 |
| w9 | 17 | -0.042056 | 3.38 |
| w10 | 3 | -0.032272 | -8.531 |
| w11 | 16 | -0.066757 | -17.085 |
| w12 | 5 | -0.066808 | -14.537 |

- LINKUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.052156 | -2.377 |
| w2 | 4 | -0.055153 | -11.353 |
| w3 | 7 | 0.01398 | -2.112 |
| w4 | 18 | -0.084584 | -16.831 |
| w5 | 13 | -0.054388 | -12.907 |
| w6 | 22 | -0.009309 | 9.115 |
| w7 | 14 | -0.101112 | -18.749 |
| w8 | 0 | -0.062027 | 0.0 |
| w9 | 22 | -0.013576 | 5.57 |
| w10 | 3 | 0.081448 | 11.206 |
| w11 | 19 | 0.089408 | 35.322 |
| w12 | 2 | -0.005612 | -1.701 |

- SOLUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.104864 | -11.453 |
| w2 | 5 | -0.051039 | -8.548 |
| w3 | 0 | -0.040673 | 0.0 |
| w4 | 14 | 0.037207 | 17.117 |
| w5 | 11 | 0.048423 | 5.02 |
| w6 | 21 | 0.030025 | 41.565 |
| w7 | 15 | 0.043982 | 8.764 |
| w8 | 9 | -0.046754 | -8.479 |
| w9 | 15 | 0.083264 | 17.082 |
| w10 | 2 | -0.118875 | -9.765 |
| w11 | 21 | -0.064544 | -17.196 |
| w12 | 7 | -0.065618 | -14.145 |

- TRXUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.108389 | -12.516 |
| w2 | 15 | 0.332619 | 96.234 |
| w3 | 2 | -0.187633 | -3.141 |
| w4 | 16 | 0.088476 | 13.618 |
| w5 | 21 | 0.011777 | -1.476 |
| w6 | 20 | -0.045135 | -4.887 |
| w7 | 14 | -0.003535 | -1.688 |
| w8 | 18 | -0.043633 | -4.878 |
| w9 | 29 | -0.06646 | -17.42 |
| w10 | 6 | 0.072674 | 6.121 |
| w11 | 26 | -0.033027 | -1.697 |
| w12 | 4 | 0.11458 | 4.056 |

- UNIUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.081297 | 4.538 |
| w2 | 11 | 0.12197 | 29.956 |
| w3 | 4 | 0.029143 | 1.96 |
| w4 | 9 | -0.051031 | -14.112 |
| w5 | 10 | -0.076239 | -17.192 |
| w6 | 19 | 0.223003 | 59.333 |
| w7 | 15 | -0.069617 | -28.318 |
| w8 | 0 | -0.039608 | 0.0 |
| w9 | 24 | -0.021997 | -2.42 |
| w10 | 3 | -0.088004 | -8.342 |
| w11 | 28 | -0.22728 | -63.343 |
| w12 | 2 | -0.019385 | -0.876 |

- AAVEUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.083325 | 10.457 |
| w2 | 5 | 0.166323 | 6.666 |
| w3 | 1 | 0.07048 | 1.704 |
| w4 | 11 | 0.060635 | 12.088 |
| w5 | 10 | -0.00533 | -5.954 |
| w6 | 25 | -0.1226 | -18.937 |
| w7 | 10 | 0.191902 | 47.244 |
| w8 | 9 | -0.190205 | -37.519 |
| w9 | 32 | 0.044044 | 43.727 |
| w10 | 2 | -0.164555 | -29.77 |
| w11 | 26 | -0.067515 | -12.253 |
| w12 | 2 | -0.016237 | -5.57 |

- INJUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.028266 | 1.703 |
| w2 | 8 | -0.023714 | -15.945 |
| w3 | 6 | 0.061874 | 9.124 |
| w4 | 25 | 0.03698 | 65.479 |
| w5 | 8 | 0.081989 | 14.919 |
| w6 | 16 | -0.000934 | 25.771 |
| w7 | 12 | 0.02217 | -7.699 |
| w8 | 4 | -0.161059 | -32.389 |
| w9 | 17 | 0.105765 | 39.747 |
| w10 | 0 | None | 0.0 |
| w11 | 17 | -0.160082 | -44.922 |
| w12 | 1 | -0.052917 | -1.454 |

