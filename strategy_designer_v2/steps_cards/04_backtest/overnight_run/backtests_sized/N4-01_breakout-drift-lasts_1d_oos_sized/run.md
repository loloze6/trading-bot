# Backtest of N4-01_breakout-drift-lasts_1d_oos_sized

- Plan: `../../../../03_test_plan/overnight_run/plans_sized/N4-01_breakout-drift-lasts_1d_oos_sized.md`
- Config: `config.json` (a copy of the plan's config)
- Data: ADA, AVAX, DOGE, LINK, SOL, TRX, UNI, AAVE, INJ as ADAUSD, AVAXUSD, DOGEUSD, LINKUSD, SOLUSD, TRXUSD, UNIUSD, AAVEUSD, INJUSD; 1d bars; folds A, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- ADAUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.114555 | -32.917 |
| w2 | 21 | -0.022961 | -21.858 |
| w3 | 17 | -0.139111 | -34.87 |
| w4 | 25 | 0.026899 | 46.069 |
| w5 | 19 | -0.032172 | -24.816 |
| w6 | 24 | 0.064792 | 136.424 |
| w7 | 12 | 0.145864 | 20.994 |
| w8 | 16 | -0.142904 | -34.817 |
| w9 | 29 | 0.170688 | 142.037 |
| w10 | 20 | -0.15857 | -22.1 |
| w11 | 24 | 0.074285 | 30.834 |
| w12 | 15 | -0.065069 | -25.267 |

- AVAXUSD: 11 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w2 | 13 | 0.076759 | -1.502 |
| w3 | 16 | -0.104866 | -38.57 |
| w4 | 16 | 0.079794 | 57.836 |
| w5 | 11 | 0.034701 | -8.037 |
| w6 | 22 | 0.101277 | 182.856 |
| w7 | 25 | 0.103646 | 21.353 |
| w8 | 15 | -0.229344 | -46.935 |
| w9 | 27 | 0.064903 | 57.679 |
| w10 | 7 | -0.03363 | -12.126 |
| w11 | 24 | 0.015659 | 11.121 |
| w12 | 12 | 0.108714 | 4.051 |

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
| w1 | 16 | -0.009184 | -10.363 |
| w2 | 5 | 0.009893 | -8.291 |
| w3 | 26 | -0.010013 | 24.525 |
| w4 | 19 | 0.078028 | 25.26 |
| w5 | 9 | 0.112535 | 15.336 |
| w6 | 27 | -0.04707 | 15.432 |
| w7 | 18 | 0.186533 | 118.035 |
| w8 | 16 | -0.142412 | -33.586 |
| w9 | 34 | 0.083682 | 130.729 |
| w10 | 9 | -0.111875 | -22.346 |
| w11 | 22 | 0.07768 | 29.816 |
| w12 | 8 | 0.074891 | 2.869 |

- LINKUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.002818 | -16.48 |
| w2 | 21 | 0.012716 | -14.814 |
| w3 | 29 | -0.061573 | -21.343 |
| w4 | 33 | -0.105706 | -2.55 |
| w5 | 14 | 0.136345 | 25.804 |
| w6 | 27 | -0.044241 | 67.414 |
| w7 | 22 | 0.032706 | 0.657 |
| w8 | 16 | -0.105087 | -29.196 |
| w9 | 34 | -0.043612 | 38.873 |
| w10 | 10 | -0.060723 | -10.429 |
| w11 | 20 | 0.068879 | 55.597 |
| w12 | 10 | -0.030542 | -13.775 |

- SOLUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.017269 | -11.995 |
| w2 | 15 | -0.005993 | -16.648 |
| w3 | 26 | -0.180436 | -61.346 |
| w4 | 32 | -0.094288 | 15.705 |
| w5 | 20 | 0.051381 | -2.317 |
| w6 | 16 | 0.069392 | 207.896 |
| w7 | 22 | 0.129775 | 40.57 |
| w8 | 15 | -0.015381 | -3.487 |
| w9 | 20 | 0.057037 | 44.135 |
| w10 | 9 | 0.033791 | 1.537 |
| w11 | 28 | 0.000403 | 17.188 |
| w12 | 19 | 0.012047 | -11.126 |

- TRXUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.044612 | -17.833 |
| w2 | 29 | 0.0114 | -9.035 |
| w3 | 20 | -0.047416 | -25.173 |
| w4 | 23 | -0.010722 | 22.351 |
| w5 | 38 | -0.036713 | 6.869 |
| w6 | 29 | -0.051308 | 42.346 |
| w7 | 32 | 0.003402 | 15.776 |
| w8 | 25 | 0.035159 | 40.178 |
| w9 | 29 | 0.017926 | 135.78 |
| w10 | 7 | 0.030444 | 4.123 |
| w11 | 39 | -0.131063 | 30.575 |
| w12 | 4 | 0.022279 | -0.511 |

- UNIUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.027777 | -17.186 |
| w2 | 23 | -0.001818 | -0.534 |
| w3 | 23 | -0.092608 | -23.682 |
| w4 | 19 | -0.04261 | -5.308 |
| w5 | 16 | 0.06778 | 5.192 |
| w6 | 27 | -0.086719 | 10.693 |
| w7 | 18 | 0.174689 | 64.474 |
| w8 | 12 | 0.071788 | 14.597 |
| w9 | 27 | -0.049702 | 38.49 |
| w10 | 1 | -0.04246 | -6.901 |
| w11 | 30 | -0.093181 | 11.834 |
| w12 | 9 | -0.097373 | -17.061 |

- AAVEUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.033193 | -5.839 |
| w2 | 26 | -0.075167 | -18.385 |
| w3 | 16 | -0.077025 | -27.938 |
| w4 | 24 | -0.039854 | 14.886 |
| w5 | 21 | -0.053702 | -26.179 |
| w6 | 31 | -0.125994 | 28.813 |
| w7 | 14 | 0.12873 | 22.689 |
| w8 | 29 | -0.135971 | -6.917 |
| w9 | 30 | -0.010295 | 48.911 |
| w10 | 12 | -0.078742 | -13.737 |
| w11 | 33 | -0.021403 | 23.59 |
| w12 | 10 | -0.080639 | -21.059 |

- INJUSD: 12 of 12 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | -0.078914 | -28.475 |
| w2 | 7 | 0.098771 | 11.382 |
| w3 | 26 | -0.031127 | -8.853 |
| w4 | 29 | 0.026445 | 190.899 |
| w5 | 23 | -0.033188 | -5.905 |
| w6 | 23 | 0.044584 | 254.99 |
| w7 | 14 | 0.034478 | -0.449 |
| w8 | 22 | -0.146187 | -33.636 |
| w9 | 29 | 0.014963 | 11.538 |
| w10 | 7 | -0.117374 | -28.562 |
| w11 | 31 | -0.006689 | 9.59 |
| w12 | 10 | -0.01239 | -13.419 |

