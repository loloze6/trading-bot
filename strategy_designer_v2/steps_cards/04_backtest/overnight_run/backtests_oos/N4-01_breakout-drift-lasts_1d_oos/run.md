# Backtest of N4-01_breakout-drift-lasts_1d_oos

- Plan: `../../../../03_test_plan/overnight_run/plans_oos/N4-01_breakout-drift-lasts_1d_oos.md`
- Config: `config.json` (a copy of the plan's config)
- Data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds A, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- ADAUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.114555 | -70.611 |
| w2 | 24 | -0.022961 | -54.629 |
| w3 | 20 | -0.139111 | -57.193 |
| w4 | 27 | 0.026899 | 79.495 |
| w5 | 21 | -0.032172 | -37.588 |
| w6 | 23 | 0.064792 | 169.184 |
| w7 | 13 | 0.145864 | 43.223 |
| w8 | 18 | -0.142904 | -54.942 |
| w9 | 31 | 0.170688 | 354.773 |
| w10 | 24 | -0.15857 | -79.481 |
| w11 | 28 | 0.074285 | 38.219 |
| w12 | 17 | -0.065069 | -48.344 |

- AVAXUSD: 11 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w2 | 17 | 0.076759 | -7.971 |
| w3 | 20 | -0.104866 | -64.328 |
| w4 | 21 | 0.079794 | 99.28 |
| w5 | 12 | 0.034701 | -13.597 |
| w6 | 22 | 0.101277 | 468.642 |
| w7 | 24 | 0.103646 | 22.982 |
| w8 | 20 | -0.229344 | -77.58 |
| w9 | 33 | 0.064903 | 84.213 |
| w10 | 10 | -0.03363 | -36.282 |
| w11 | 29 | 0.015659 | 0.455 |
| w12 | 12 | 0.108714 | 6.471 |

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
| w1 | 19 | -0.009184 | -35.864 |
| w2 | 8 | 0.009893 | -24.201 |
| w3 | 30 | -0.010013 | -39.744 |
| w4 | 21 | 0.078028 | 40.735 |
| w5 | 9 | 0.112535 | 19.192 |
| w6 | 25 | -0.04707 | 17.812 |
| w7 | 22 | 0.186533 | 190.466 |
| w8 | 19 | -0.142412 | -58.517 |
| w9 | 37 | 0.083682 | 347.994 |
| w10 | 10 | -0.111875 | -50.994 |
| w11 | 32 | 0.07768 | 35.926 |
| w12 | 10 | 0.074891 | 2.382 |

- LINKUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | 0.002818 | -48.965 |
| w2 | 29 | 0.012716 | -44.379 |
| w3 | 30 | -0.061573 | -48.731 |
| w4 | 32 | -0.105706 | -16.144 |
| w5 | 16 | 0.136345 | 35.8 |
| w6 | 27 | -0.044241 | 108.656 |
| w7 | 26 | 0.032706 | -9.986 |
| w8 | 20 | -0.105087 | -51.482 |
| w9 | 33 | -0.043612 | 71.711 |
| w10 | 10 | -0.060723 | -31.709 |
| w11 | 28 | 0.068879 | 107.805 |
| w12 | 11 | -0.030542 | -24.836 |

- SOLUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | 0.017269 | -39.547 |
| w2 | 20 | -0.005993 | -49.442 |
| w3 | 29 | -0.180436 | -92.51 |
| w4 | 37 | -0.094288 | 14.844 |
| w5 | 23 | 0.051381 | 3.55 |
| w6 | 20 | 0.069392 | 766.415 |
| w7 | 23 | 0.129775 | 75.669 |
| w8 | 21 | -0.015381 | -18.835 |
| w9 | 20 | 0.057037 | 77.934 |
| w10 | 12 | 0.033791 | 0.608 |
| w11 | 30 | 0.000403 | 28.397 |
| w12 | 18 | 0.012047 | -24.304 |

- TRXUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.044612 | -27.895 |
| w2 | 29 | 0.0114 | -25.618 |
| w3 | 19 | -0.047416 | -24.496 |
| w4 | 24 | -0.010722 | 20.68 |
| w5 | 36 | -0.036713 | 5.495 |
| w6 | 26 | -0.051308 | 31.31 |
| w7 | 33 | 0.003402 | 9.166 |
| w8 | 23 | 0.035159 | 38.74 |
| w9 | 25 | 0.017926 | 74.576 |
| w10 | 5 | 0.030444 | 5.68 |
| w11 | 35 | -0.131063 | 23.833 |
| w12 | 4 | 0.022279 | -3.126 |

- UNIUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.027777 | -39.675 |
| w2 | 29 | -0.001818 | -27.639 |
| w3 | 26 | -0.092608 | -56.185 |
| w4 | 21 | -0.04261 | -15.048 |
| w5 | 16 | 0.06778 | 5.809 |
| w6 | 28 | -0.086719 | 19.276 |
| w7 | 22 | 0.174689 | 115.562 |
| w8 | 17 | 0.071788 | 4.701 |
| w9 | 24 | -0.049702 | 125.688 |
| w10 | 2 | -0.04246 | -18.797 |
| w11 | 39 | -0.093181 | -0.846 |
| w12 | 12 | -0.097373 | -56.914 |

- AAVEUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | 0.033193 | -32.029 |
| w2 | 33 | -0.075167 | -71.705 |
| w3 | 21 | -0.077025 | -64.249 |
| w4 | 24 | -0.039854 | 8.437 |
| w5 | 25 | -0.053702 | -38.958 |
| w6 | 30 | -0.125994 | 37.077 |
| w7 | 16 | 0.12873 | 34.391 |
| w8 | 31 | -0.135971 | -16.751 |
| w9 | 33 | -0.010295 | 122.177 |
| w10 | 11 | -0.078742 | -39.948 |
| w11 | 30 | -0.021403 | 72.569 |
| w12 | 12 | -0.080639 | -48.013 |

- INJUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | -0.078914 | -76.216 |
| w2 | 10 | 0.098771 | 26.472 |
| w3 | 27 | -0.031127 | -39.04 |
| w4 | 34 | 0.026445 | 716.933 |
| w5 | 26 | -0.033188 | -28.442 |
| w6 | 19 | 0.044584 | 718.937 |
| w7 | 20 | 0.034478 | -27.917 |
| w8 | 27 | -0.146187 | -73.247 |
| w9 | 31 | 0.014963 | 13.663 |
| w10 | 10 | -0.117374 | -68.407 |
| w11 | 34 | -0.006689 | 9.316 |
| w12 | 11 | -0.01239 | -25.801 |

