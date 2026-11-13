# Backtest of N2-06_rebound-in-high-volatility_1d_oos

- Plan: `../../../../03_test_plan/overnight_run/plans_oos/N2-06_rebound-in-high-volatility_1d_oos.md`
- Config: `config.json` (a copy of the plan's config)
- Data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds A, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- ADAUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 37 | -0.026802 | -24.391 |
| w2 | 31 | 0.093199 | 17.945 |
| w3 | 28 | 0.09924 | -5.492 |
| w4 | 26 | 0.125848 | 33.196 |
| w5 | 34 | 0.024996 | -9.323 |
| w6 | 24 | 0.113758 | 41.095 |
| w7 | 32 | 0.140823 | 22.792 |
| w8 | 32 | 0.008673 | -12.535 |
| w9 | 24 | -0.053381 | 0.751 |
| w10 | 22 | 0.004892 | -4.32 |
| w11 | 39 | 0.0619 | 12.877 |
| w12 | 42 | 0.057635 | -15.252 |

- AVAXUSD: 11 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w2 | 34 | -0.044075 | -46.178 |
| w3 | 28 | 0.018245 | -25.735 |
| w4 | 24 | 0.00591 | 8.523 |
| w5 | 37 | 0.015264 | -16.461 |
| w6 | 23 | -0.08267 | -4.898 |
| w7 | 25 | 0.137458 | 28.583 |
| w8 | 31 | -0.114956 | -38.907 |
| w9 | 36 | -0.065197 | -11.731 |
| w10 | 30 | -0.035673 | -29.379 |
| w11 | 36 | -0.036365 | -12.823 |
| w12 | 33 | 0.072036 | 4.623 |

- w1 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 11 prefetch bars (<date> to <date>) -- required_bars=120. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- DOGEUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | 0.093194 | 15.821 |
| w2 | 26 | 0.018667 | -29.124 |
| w3 | 19 | 0.04674 | 7.298 |
| w4 | 32 | -0.000329 | -2.742 |
| w5 | 29 | 0.021935 | -10.625 |
| w6 | 26 | 0.082686 | 18.109 |
| w7 | 25 | 0.006808 | 5.324 |
| w8 | 27 | -0.087288 | -28.006 |
| w9 | 20 | -0.110505 | -17.676 |
| w10 | 30 | 0.000772 | -18.231 |
| w11 | 30 | 0.020551 | 11.023 |
| w12 | 29 | 0.079644 | 3.505 |

- LINKUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 32 | -0.014218 | -24.03 |
| w2 | 35 | -0.046436 | -36.915 |
| w3 | 27 | 0.09134 | 2.222 |
| w4 | 32 | 0.034036 | 6.113 |
| w5 | 39 | 0.032287 | -1.91 |
| w6 | 25 | 0.011979 | 14.435 |
| w7 | 28 | 0.129575 | 17.758 |
| w8 | 33 | -0.012141 | -18.666 |
| w9 | 32 | -0.097202 | -19.546 |
| w10 | 25 | -0.05237 | -29.947 |
| w11 | 32 | 0.025373 | 15.848 |
| w12 | 30 | 0.106033 | 8.314 |

- SOLUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | -0.001649 | -25.932 |
| w2 | 38 | 0.012374 | -25.207 |
| w3 | 24 | -0.144705 | -88.806 |
| w4 | 20 | -0.028094 | 0.574 |
| w5 | 36 | -0.059394 | -19.52 |
| w6 | 21 | 0.050036 | 41.714 |
| w7 | 24 | 0.09463 | 24.27 |
| w8 | 35 | 0.010919 | -5.54 |
| w9 | 33 | -0.039432 | -6.512 |
| w10 | 30 | -0.028434 | -20.686 |
| w11 | 34 | -0.001328 | 2.184 |
| w12 | 30 | 0.067719 | -1.073 |

- TRXUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 35 | 0.07021 | 5.542 |
| w2 | 25 | 0.301321 | 98.48 |
| w3 | 22 | 0.070607 | -2.087 |
| w4 | 24 | 0.183334 | 35.873 |
| w5 | 27 | -0.055602 | -9.701 |
| w6 | 20 | 0.129007 | 17.746 |
| w7 | 28 | -0.022798 | -7.265 |
| w8 | 24 | -0.068337 | -7.777 |
| w9 | 22 | -0.045265 | -10.918 |
| w10 | 24 | 0.121662 | 12.635 |
| w11 | 20 | 0.001137 | 1.207 |
| w12 | 27 | 0.068807 | -2.281 |

- UNIUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 37 | -0.033802 | -37.307 |
| w2 | 28 | 0.055368 | 20.702 |
| w3 | 24 | 0.076037 | -2.722 |
| w4 | 31 | 0.036522 | 1.173 |
| w5 | 27 | -0.071544 | -25.834 |
| w6 | 29 | 0.235088 | 65.305 |
| w7 | 23 | -0.117566 | -51.227 |
| w8 | 30 | 0.016598 | -10.615 |
| w9 | 27 | -0.050317 | -10.22 |
| w10 | 33 | 0.11689 | 3.756 |
| w11 | 34 | -0.073892 | -14.428 |
| w12 | 28 | -0.008988 | -8.978 |

- AAVEUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | -0.031655 | -32.176 |
| w2 | 33 | 0.029979 | -7.699 |
| w3 | 25 | 0.070901 | -9.167 |
| w4 | 28 | 0.103745 | 19.419 |
| w5 | 29 | 0.05682 | 5.502 |
| w6 | 24 | -0.029244 | -1.844 |
| w7 | 27 | 0.040319 | -19.326 |
| w8 | 28 | -0.127046 | -28.82 |
| w9 | 28 | 0.089629 | 60.395 |
| w10 | 30 | 0.102874 | 12.049 |
| w11 | 32 | 0.035302 | 13.681 |
| w12 | 26 | 0.005023 | -22.384 |

- INJUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 35 | -0.04893 | -45.456 |
| w2 | 37 | 0.05149 | -19.645 |
| w3 | 17 | 0.130975 | 7.147 |
| w4 | 24 | 0.020162 | 34.178 |
| w5 | 31 | 0.052816 | 4.486 |
| w6 | 24 | 0.036972 | 59.598 |
| w7 | 30 | 0.03584 | -6.207 |
| w8 | 38 | -0.033256 | -29.441 |
| w9 | 37 | -0.060602 | -18.908 |
| w10 | 27 | -0.089919 | -51.157 |
| w11 | 36 | -0.130949 | -31.655 |
| w12 | 37 | 0.018907 | -22.907 |

