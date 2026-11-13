# Backtest of N5-03_high-in-confirmed-uptrend_1d_oos

- Plan: `../../../../03_test_plan/overnight_run/plans_oos/N5-03_high-in-confirmed-uptrend_1d_oos.md`
- Config: `config.json` (a copy of the plan's config)
- Data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds A, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- ADAUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 15 | -0.170668 | -33.4 |
| w5 | 2 | -0.020446 | -2.837 |
| w6 | 33 | 0.110129 | 101.075 |
| w7 | 16 | 0.046164 | 0.735 |
| w8 | 0 | None | 0.0 |
| w9 | 17 | 0.259567 | 346.4 |
| w10 | 8 | -0.160493 | -63.728 |
| w11 | 16 | -0.028159 | -10.307 |
| w12 | 6 | -0.019369 | -10.887 |

- AVAXUSD: 10 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w3 | 0 | None | 0.0 |
| w4 | 22 | -0.074847 | -21.508 |
| w5 | 0 | None | 0.0 |
| w6 | 33 | 0.214614 | 398.945 |
| w7 | 28 | -0.033788 | -32.753 |
| w8 | 0 | None | 0.0 |
| w9 | 17 | 0.085119 | 56.648 |
| w10 | 1 | -0.193893 | -22.517 |
| w11 | 14 | -0.16799 | -40.22 |
| w12 | 8 | 0.133629 | 32.253 |

- w1 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 11 prefetch bars (<date> to <date>) -- required_bars=200. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w2 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 131 prefetch bars (<date> to <date>) -- required_bars=200. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- DOGEUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 19 | 0.157761 | 53.04 |
| w4 | 9 | -0.146381 | -30.929 |
| w5 | 7 | -0.136075 | -16.241 |
| w6 | 25 | -0.006828 | 4.101 |
| w7 | 27 | 0.119124 | 42.17 |
| w8 | 6 | -0.084194 | -20.04 |
| w9 | 33 | 0.170127 | 282.9 |
| w10 | 7 | -0.146967 | -26.764 |
| w11 | 12 | -0.072273 | -22.833 |
| w12 | 8 | 0.052643 | 0.907 |

- LINKUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 5 | -0.200208 | -46.519 |
| w4 | 27 | -0.198286 | -45.623 |
| w5 | 14 | -0.126991 | -24.383 |
| w6 | 26 | 0.014439 | 57.58 |
| w7 | 13 | -0.029843 | -21.588 |
| w8 | 2 | -0.049773 | -7.9 |
| w9 | 26 | 0.03302 | 30.877 |
| w10 | 10 | 0.007849 | -5.687 |
| w11 | 21 | -0.043348 | -10.329 |
| w12 | 6 | -0.132225 | -15.878 |

- SOLUSD: 11 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 3 | -0.075492 | -14.073 |
| w5 | 18 | 0.021834 | -3.44 |
| w6 | 43 | 0.117964 | 521.409 |
| w7 | 35 | 0.094576 | 54.493 |
| w8 | 22 | -0.214305 | -54.899 |
| w9 | 20 | 0.045597 | 35.707 |
| w10 | 8 | -0.133878 | -41.263 |
| w11 | 20 | -0.052974 | -14.275 |
| w12 | 16 | 0.042445 | -3.107 |

- w1 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 198 prefetch bars (<date> to <date>) -- required_bars=200. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- TRXUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 16 | -0.208536 | -60.564 |
| w3 | 0 | None | 0.0 |
| w4 | 37 | -0.215263 | -40.215 |
| w5 | 42 | -0.099702 | -17.646 |
| w6 | 44 | -0.132218 | -5.059 |
| w7 | 20 | 0.089469 | 26.662 |
| w8 | 30 | 0.130513 | 40.243 |
| w9 | 36 | 0.122159 | 101.678 |
| w10 | 19 | -0.204909 | -37.541 |
| w11 | 49 | -0.008347 | 26.618 |
| w12 | 12 | -0.128706 | -10.715 |

- UNIUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 15 | -0.096024 | -32.857 |
| w3 | 7 | 0.019051 | 0.203 |
| w4 | 22 | -0.163229 | -38.864 |
| w5 | 6 | -0.03279 | -14.474 |
| w6 | 28 | -0.109026 | -17.214 |
| w7 | 18 | 0.124965 | 117.663 |
| w8 | 3 | -0.096583 | -21.387 |
| w9 | 35 | -0.029399 | 9.144 |
| w10 | 4 | -0.193203 | -24.624 |
| w11 | 13 | 0.018922 | 46.973 |
| w12 | 1 | -0.093738 | -13.425 |

- AAVEUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.057175 | -17.516 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | -0.111853 | -17.868 |
| w4 | 26 | -0.112111 | -27.651 |
| w5 | 11 | -0.045834 | -15.559 |
| w6 | 36 | -0.039933 | 16.386 |
| w7 | 14 | -0.124719 | -42.051 |
| w8 | 16 | 0.026917 | 13.195 |
| w9 | 44 | -0.041397 | 40.064 |
| w10 | 5 | -0.057706 | -14.844 |
| w11 | 31 | -0.152096 | -34.016 |
| w12 | 1 | -0.143323 | -8.597 |

- INJUSD: 11 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w2 | 0 | None | 0.0 |
| w3 | 3 | -0.05207 | -37.18 |
| w4 | 48 | 0.061414 | 355.191 |
| w5 | 19 | -0.032625 | -19.357 |
| w6 | 35 | 0.171152 | 744.706 |
| w7 | 25 | -0.030323 | -29.759 |
| w8 | 0 | None | 0.0 |
| w9 | 24 | -0.017221 | -11.662 |
| w10 | 3 | -0.114268 | -20.394 |
| w11 | 13 | -0.067882 | -24.569 |
| w12 | 4 | 0.016763 | -4.629 |

- w1 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 144 prefetch bars (<date> to <date>) -- required_bars=200. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

