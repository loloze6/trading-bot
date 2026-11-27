# Backtest of 074-01.b1.d3.d2.d1_falling-market-deep-run-fade_1d

- Plan: `../../../../../03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.d3.d2.d1_falling-market-deep-run-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.048239 | -0.381 |
| w2 | 1 | 0.051654 | 0.383 |
| w3 | 1 | -0.194109 | -0.907 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 9 | 0.172467 | 13.987 |
| w8 | 7 | 0.132034 | 11.332 |
| w9 | 8 | 0.261749 | 42.358 |
| w10 | 3 | 0.035172 | 0.377 |
| w11 | 0 | None | 0.0 |
| w12 | 13 | -0.037885 | -2.618 |
| w13 | 6 | 0.148349 | 6.247 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 13 | 0.136087 | 8.586 |
| w18 | 5 | -0.027363 | -2.141 |
| w19 | 8 | 0.0 | -0.829 |
| w20 | 14 | 0.15613 | 17.632 |
| w21 | 11 | 0.025197 | 2.49 |
| w22 | 0 | 0.007594 | 0.0 |
| w23 | 3 | -0.085699 | -1.124 |
| w24 | 2 | -0.018646 | -2.784 |
| w25 | 0 | None | 0.0 |
| w26 | 4 | 0.021049 | 0.909 |
| w27 | 0 | None | 0.0 |
| w28 | 6 | -0.080538 | -5.815 |
| w29 | 0 | None | 0.0 |
| w30 | 7 | 0.012485 | 1.194 |
| w31 | 9 | 0.046283 | 6.02 |
| w32 | 8 | -0.034731 | -2.443 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.067449 | -0.15 |
| w2 | 6 | -0.024996 | -1.651 |
| w3 | 0 | -0.056642 | 0.0 |
| w4 | 3 | -0.012294 | -2.748 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.035821 | -0.691 |
| w7 | 10 | 0.061226 | 4.867 |
| w8 | 19 | 0.227247 | 32.672 |
| w9 | 13 | 0.170065 | 23.44 |
| w10 | 1 | 0.119168 | 1.179 |
| w11 | 6 | -0.021423 | -1.991 |
| w12 | 14 | -0.025645 | -3.789 |
| w13 | 7 | 0.138066 | 5.348 |
| w14 | 2 | -0.090959 | -1.189 |
| w15 | 3 | 0.0053 | -1.151 |
| w16 | 0 | None | 0.0 |
| w17 | 7 | -0.051466 | -2.918 |
| w18 | 3 | 0.005783 | 0.175 |
| w19 | 15 | 0.064122 | 4.939 |
| w20 | 10 | 0.038105 | 5.128 |
| w21 | 3 | 0.083001 | 1.028 |
| w22 | 0 | None | 0.0 |
| w23 | 4 | -0.035732 | -2.164 |
| w24 | 8 | -0.003724 | -2.058 |
| w25 | 0 | None | 0.0 |
| w26 | 12 | 0.105564 | 9.399 |
| w27 | 1 | -0.023316 | -1.255 |
| w28 | 7 | 0.048166 | 3.087 |
| w29 | 1 | 0.059732 | 1.285 |
| w30 | 11 | -0.027456 | -2.292 |
| w31 | 16 | 0.025016 | 3.265 |
| w32 | 8 | 0.027193 | 1.781 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 1 | -0.01392 | -0.727 |
| w7 | 7 | -0.052916 | -5.641 |
| w8 | 13 | 0.033522 | 7.42 |
| w9 | 9 | 0.084731 | 7.51 |
| w10 | 8 | 0.063688 | 2.625 |
| w11 | 7 | -0.039528 | -3.441 |
| w12 | 8 | 0.116427 | 8.67 |
| w13 | 4 | 0.14864 | 5.876 |
| w14 | 1 | -0.000396 | -0.284 |
| w15 | 3 | -0.006253 | -1.642 |
| w16 | 4 | -0.046965 | -2.876 |
| w17 | 9 | -0.020084 | -1.136 |
| w18 | 7 | -0.016278 | 0.095 |
| w19 | 7 | 0.052019 | 4.467 |
| w20 | 5 | -0.166441 | 12.498 |
| w21 | 5 | 0.037429 | 1.459 |
| w22 | 0 | 0.04434 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | 0.013972 | -0.313 |
| w25 | 6 | 0.052951 | 4.923 |
| w26 | 9 | 0.140503 | 12.513 |
| w27 | 1 | 0.11319 | 3.95 |
| w28 | 4 | 0.066921 | 2.61 |
| w29 | 1 | 0.010489 | 0.018 |
| w30 | 16 | -0.061845 | -5.285 |
| w31 | 9 | 0.057858 | 5.796 |
| w32 | 9 | -0.004537 | -1.749 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 10 | 0.08273 | 4.457 |
| w8 | 11 | 0.128844 | 12.287 |
| w9 | 16 | 0.012694 | 2.791 |
| w10 | 6 | 0.05627 | 0.945 |
| w11 | 7 | 0.076895 | 1.246 |
| w12 | 11 | -0.083376 | -9.048 |
| w13 | 5 | 0.056399 | 0.57 |
| w14 | 2 | -0.026469 | -1.801 |
| w15 | 3 | -0.000271 | -0.654 |
| w16 | 0 | None | 0.0 |
| w17 | 8 | -0.005644 | -0.684 |
| w18 | 7 | -0.064967 | -4.779 |
| w19 | 11 | 0.137216 | 10.891 |
| w20 | 14 | 0.147194 | 16.5 |
| w21 | 8 | -0.018635 | -1.639 |
| w22 | 2 | 0.0605 | 1.779 |
| w23 | 4 | 0.076748 | 4.557 |
| w24 | 3 | 0.060242 | 1.224 |
| w25 | 0 | None | 0.0 |
| w26 | 14 | 0.131696 | 12.871 |
| w27 | 1 | -0.085254 | -3.556 |
| w28 | 14 | -0.109563 | -12.551 |
| w29 | 0 | None | 0.0 |
| w30 | 4 | 0.021419 | 0.419 |
| w31 | 8 | -0.048203 | -6.203 |
| w32 | 10 | 0.110012 | 12.595 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 4 | -0.122159 | -5.223 |
| w3 | 8 | 0.038674 | 6.569 |
| w4 | 0 | -0.003206 | 0.0 |
| w5 | 0 | 0.048136 | 0.0 |
| w6 | 1 | 0.045824 | 0.269 |
| w7 | 8 | 0.059703 | 4.136 |
| w8 | 11 | 0.23363 | 29.247 |
| w9 | 16 | 0.191537 | 33.31 |
| w10 | 2 | 0.078125 | 1.107 |
| w11 | 7 | 0.038352 | 1.837 |
| w12 | 8 | 0.054646 | 3.756 |
| w13 | 7 | 0.022476 | 0.411 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.076134 | -2.856 |
| w16 | 0 | None | 0.0 |
| w17 | 6 | -0.022516 | -1.043 |
| w18 | 1 | 0.020562 | 0.86 |
| w19 | 8 | -0.008063 | -0.646 |
| w20 | 11 | 0.040535 | 5.082 |
| w21 | 8 | -0.004944 | -0.487 |
| w22 | 0 | 0.008954 | 0.0 |
| w23 | 2 | -0.081051 | -3.106 |
| w24 | 4 | 0.00066 | -2.795 |
| w25 | 0 | None | 0.0 |
| w26 | 9 | 0.050884 | 4.925 |
| w27 | 2 | -0.017326 | -1.353 |
| w28 | 11 | 0.17276 | 18.754 |
| w29 | 0 | 0.021924 | 0.0 |
| w30 | 12 | 0.000824 | 1.102 |
| w31 | 8 | 0.047937 | 4.352 |
| w32 | 6 | -0.008881 | -0.995 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 1 | 0.071006 | 1.119 |
| w11 | 7 | -0.069512 | -4.762 |
| w12 | 9 | 0.025361 | 1.393 |
| w13 | 5 | 0.142073 | 4.981 |
| w14 | 0 | None | 0.0 |
| w15 | 7 | 0.086341 | 3.626 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | 0.056219 | 2.036 |
| w18 | 12 | 0.107666 | 14.328 |
| w19 | 12 | 0.022837 | 1.855 |
| w20 | 10 | 0.043936 | 5.254 |
| w21 | 14 | -0.005483 | -0.151 |
| w22 | 0 | -0.00314 | 0.0 |
| w23 | 8 | 0.133635 | 11.426 |
| w24 | 6 | 0.037752 | -2.774 |
| w25 | 3 | 0.037385 | 1.498 |
| w26 | 18 | 0.107457 | 10.883 |
| w27 | 3 | -0.0447 | -3.933 |
| w28 | 13 | -0.047528 | -9.364 |
| w29 | 6 | -0.02401 | -2.437 |
| w30 | 13 | -0.068055 | -4.494 |
| w31 | 13 | -0.045351 | -4.644 |
| w32 | 7 | -0.020216 | -2.969 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 4 | 0.021104 | -1.628 |
| w13 | 8 | 0.028954 | 2.754 |
| w14 | 3 | -0.068271 | -6.073 |
| w15 | 5 | -0.015889 | -1.146 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | 0.030309 | -0.595 |
| w18 | 8 | 0.045849 | 1.659 |
| w19 | 6 | 0.077944 | 5.867 |
| w20 | 8 | 0.15637 | 15.153 |
| w21 | 6 | 0.004467 | -0.508 |
| w22 | 4 | 0.08481 | 2.622 |
| w23 | 12 | -0.047666 | -4.901 |
| w24 | 6 | -0.027464 | -9.573 |
| w25 | 4 | -0.03097 | -4.506 |
| w26 | 18 | -0.037987 | -4.118 |
| w27 | 4 | -0.089996 | -10.462 |
| w28 | 10 | -0.020762 | -3.803 |
| w29 | 2 | -0.006639 | -0.9 |
| w30 | 14 | -0.068097 | -4.901 |
| w31 | 10 | -0.087735 | -8.91 |
| w32 | 9 | 0.025512 | 0.261 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 9 | 0.042867 | 1.416 |
| w16 | 0 | 0.056292 | 0.0 |
| w17 | 8 | -0.059634 | -4.961 |
| w18 | 4 | -0.082727 | -6.562 |
| w19 | 16 | 0.141593 | 14.877 |
| w20 | 13 | 0.009052 | -0.825 |
| w21 | 8 | 0.096213 | 5.808 |
| w22 | 6 | -0.134754 | -12.724 |
| w23 | 15 | 0.091833 | 11.513 |
| w24 | 5 | -0.000873 | -6.25 |
| w25 | 1 | 0.034646 | 1.682 |
| w26 | 19 | 0.128067 | 11.534 |
| w27 | 5 | 0.069372 | 3.252 |
| w28 | 13 | -0.063068 | -7.317 |
| w29 | 6 | -0.001497 | -1.954 |
| w30 | 17 | 0.002401 | 1.583 |
| w31 | 14 | -0.032184 | -6.752 |
| w32 | 10 | -0.030282 | -4.155 |

- w14 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_ALGOUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- TRXUSD: 18 of 18 windows run. w1 to w14 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 4 | -0.028662 | -3.878 |
| w16 | 0 | None | 0.0 |
| w17 | 7 | -0.185533 | -7.823 |
| w18 | 3 | 0.045264 | 1.598 |
| w19 | 10 | 0.144822 | 10.293 |
| w20 | 3 | -0.094728 | -5.73 |
| w21 | 10 | 0.137226 | 9.729 |
| w22 | 0 | 0.072275 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 1 | 0.044272 | 1.331 |
| w26 | 1 | -0.07441 | -1.006 |
| w27 | 0 | None | 0.0 |
| w28 | 4 | -0.019384 | -2.637 |
| w29 | 0 | None | 0.0 |
| w30 | 7 | -0.015911 | -2.052 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | -0.017096 | 0.0 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 1 | -0.120467 | -9.606 |
| w17 | 10 | 0.110697 | 7.143 |
| w18 | 4 | -0.064583 | -2.506 |
| w19 | 10 | 0.128804 | 10.224 |
| w20 | 12 | -0.056222 | -4.003 |
| w21 | 14 | -0.148383 | -18.94 |
| w22 | 1 | 0.027427 | 0.601 |
| w23 | 11 | -0.015526 | -3.022 |
| w24 | 9 | 0.003483 | -10.741 |
| w25 | 3 | 0.018298 | -0.094 |
| w26 | 17 | -0.132576 | -14.614 |
| w27 | 5 | -0.026393 | -4.308 |
| w28 | 15 | 0.098316 | 8.964 |
| w29 | 6 | -0.059378 | -5.242 |
| w30 | 13 | -0.07416 | -7.759 |
| w31 | 16 | -0.054328 | -5.578 |
| w32 | 15 | 0.10596 | 10.689 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 10 | 0.024315 | 5.702 |
| w21 | 14 | 0.067986 | 4.19 |
| w22 | 1 | 0.041356 | 1.933 |
| w23 | 10 | 0.050673 | 4.901 |
| w24 | 6 | -0.009956 | -10.822 |
| w25 | 4 | 0.054948 | 2.53 |
| w26 | 17 | 0.056918 | 4.718 |
| w27 | 1 | -0.065421 | -1.029 |
| w28 | 14 | 0.045978 | 3.986 |
| w29 | 3 | -0.022063 | -1.239 |
| w30 | 12 | -0.084942 | -5.335 |
| w31 | 12 | -0.021469 | -1.526 |
| w32 | 8 | -0.003777 | -0.422 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 7 | -0.006106 | -1.26 |
| w23 | 13 | -0.066131 | -4.573 |
| w24 | 10 | 0.034707 | -6.84 |
| w25 | 1 | -0.034355 | -3.091 |
| w26 | 10 | 0.073026 | 5.863 |
| w27 | 4 | 0.086907 | 3.267 |
| w28 | 14 | -0.042551 | -4.11 |
| w29 | 2 | -0.065885 | -3.004 |
| w30 | 12 | -0.101556 | -12.437 |
| w31 | 12 | -0.008085 | -0.503 |
| w32 | 6 | 0.080001 | 3.878 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 7 | 0.062883 | 2.504 |
| w25 | 2 | 0.023195 | 0.621 |
| w26 | 16 | 0.009269 | 0.182 |
| w27 | 0 | None | 0.0 |
| w28 | 9 | 0.003643 | -0.875 |
| w29 | 3 | -0.01817 | -0.899 |
| w30 | 17 | -0.068515 | -3.409 |
| w31 | 10 | 0.019422 | 2.813 |
| w32 | 8 | -0.080689 | -7.989 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 3 | 0.027311 | -0.347 |
| w6 | 1 | -0.024338 | -0.499 |
| w7 | 8 | 0.061528 | 5.403 |
| w8 | 13 | 0.053065 | 5.974 |
| w9 | 14 | 0.12822 | 18.512 |
| w10 | 7 | -0.056573 | -4.746 |
| w11 | 6 | 0.113214 | 6.499 |
| w12 | 15 | -0.011459 | -0.315 |
| w13 | 7 | 0.093489 | 3.469 |
| w14 | 1 | -0.015115 | -0.131 |
| w15 | 7 | -0.037024 | -2.368 |
| w16 | 0 | None | 0.0 |
| w17 | 11 | 0.035695 | 0.931 |
| w18 | 1 | -0.028359 | -0.75 |
| w19 | 10 | 0.013855 | 1.567 |
| w20 | 16 | 0.305349 | 26.782 |
| w21 | 16 | 0.104633 | 13.634 |
| w22 | 7 | -0.008249 | -2.033 |
| w23 | 9 | 0.000999 | 1.594 |
| w24 | 5 | -0.019155 | -2.605 |
| w25 | 8 | -0.140504 | -10.501 |
| w26 | 7 | 0.037204 | 0.605 |
| w27 | 3 | -0.031469 | -2.898 |
| w28 | 9 | 0.040366 | 2.892 |
| w29 | 5 | -0.060626 | -6.129 |
| w30 | 0 | None | 0.0 |
| w31 | 12 | -0.168478 | -14.391 |
| w32 | 1 | -0.004179 | -0.18 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 0 | 0.046081 | 0.0 |
| w6 | 4 | 0.030946 | 0.348 |
| w7 | 13 | 0.182127 | 11.989 |
| w8 | 16 | 0.208793 | 18.915 |
| w9 | 14 | 0.112105 | 10.85 |
| w10 | 2 | 0.045466 | 0.306 |
| w11 | 3 | 0.022373 | 0.586 |
| w12 | 15 | 0.010784 | 2.166 |
| w13 | 5 | 0.050986 | 1.612 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 6 | -0.055742 | -2.296 |
| w18 | 5 | -0.001297 | -0.565 |
| w19 | 7 | 0.150509 | 13.009 |
| w20 | 11 | 0.001064 | -2.151 |
| w21 | 5 | 0.047115 | 1.204 |
| w22 | 3 | -0.280661 | -11.785 |
| w23 | 4 | -0.125015 | -7.508 |
| w24 | 4 | -0.050111 | -2.004 |
| w25 | 8 | 0.005275 | 1.532 |
| w26 | 2 | 0.076009 | 2.096 |
| w27 | 2 | -0.011384 | -2.035 |
| w28 | 0 | None | 0.0 |
| w29 | 5 | -0.239764 | -21.453 |
| w30 | 0 | -0.000853 | 0.0 |
| w31 | 9 | -0.024841 | -2.314 |
| w32 | 2 | 0.024657 | -0.075 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 15 | -0.029245 | -7.351 |
| w18 | 0 | None | 0.0 |
| w19 | 13 | -0.031814 | -1.392 |
| w20 | 8 | -0.157898 | -15.667 |
| w21 | 16 | 0.095686 | 10.655 |
| w22 | 3 | 0.060352 | 2.454 |
| w23 | 10 | 0.195756 | 22.982 |
| w24 | 5 | -0.04578 | -8.024 |
| w25 | 6 | 0.028425 | 0.463 |
| w26 | 17 | 0.174273 | 23.936 |
| w27 | 2 | 0.003501 | -1.729 |
| w28 | 9 | -0.050724 | -6.578 |
| w29 | 4 | -0.000963 | -0.854 |
| w30 | 16 | -0.100923 | -8.584 |
| w31 | 14 | -0.055441 | -4.821 |
| w32 | 4 | -0.059224 | -4.837 |

- w16 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_CRVUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- AAVEUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 11 | -0.091888 | -4.288 |
| w18 | 11 | -0.037506 | -5.288 |
| w19 | 10 | 0.118163 | 9.89 |
| w20 | 9 | -0.081602 | -5.434 |
| w21 | 13 | 0.089035 | 6.806 |
| w22 | 4 | 0.036736 | 1.147 |
| w23 | 7 | -0.012624 | -1.171 |
| w24 | 3 | 0.024929 | -1.097 |
| w25 | 1 | 0.001209 | 0.137 |
| w26 | 7 | 0.050131 | 0.408 |
| w27 | 0 | None | 0.0 |
| w28 | 13 | 0.014315 | 1.528 |
| w29 | 1 | -0.004348 | -0.079 |
| w30 | 13 | -0.056276 | -4.65 |
| w31 | 14 | -0.084453 | -7.227 |
| w32 | 9 | 0.106479 | 6.954 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 11 | 0.036185 | 4.435 |
| w20 | 12 | 0.123927 | 18.412 |
| w21 | 4 | 0.043556 | 1.486 |
| w22 | 0 | -0.031689 | 0.0 |
| w23 | 3 | 0.018917 | 0.891 |
| w24 | 5 | 0.059784 | -0.47 |
| w25 | 3 | 0.026529 | 0.75 |
| w26 | 13 | 0.096091 | 7.827 |
| w27 | 4 | 0.090324 | 3.104 |
| w28 | 14 | -0.050744 | -6.865 |
| w29 | 1 | 0.015325 | 0.444 |
| w30 | 17 | 0.045618 | 7.71 |
| w31 | 15 | -0.05883 | -6.834 |
| w32 | 4 | -0.155163 | -17.646 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 3 | 0.062456 | 1.962 |
| w23 | 13 | 0.107305 | 6.421 |
| w24 | 6 | -0.023012 | -7.765 |
| w25 | 3 | 0.057639 | 2.321 |
| w26 | 14 | 0.053812 | 3.771 |
| w27 | 4 | 0.076624 | 2.978 |
| w28 | 9 | 0.07239 | 6.888 |
| w29 | 5 | -0.252732 | -20.46 |
| w30 | 13 | -0.07422 | -4.532 |
| w31 | 16 | 0.047206 | 4.991 |
| w32 | 4 | 0.036304 | 0.324 |

- w21 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_LDOUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- ONDOUSD: 6 of 6 windows run. w1 to w26 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w27 | 3 | 0.071045 | 2.523 |
| w28 | 11 | 0.046269 | 3.95 |
| w29 | 5 | -0.091393 | -4.535 |
| w30 | 15 | 0.016744 | 5.508 |
| w31 | 13 | -0.00426 | -0.475 |
| w32 | 3 | -0.334296 | -22.856 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 7 | -0.102111 | -5.63 |
| w18 | 12 | -0.01694 | -2.305 |
| w19 | 10 | 0.035548 | 3.167 |
| w20 | 13 | 0.094017 | 9.44 |
| w21 | 10 | 0.022644 | 2.245 |
| w22 | 2 | 0.039136 | 1.242 |
| w23 | 11 | -0.008728 | -1.961 |
| w24 | 6 | 0.028753 | -3.427 |
| w25 | 1 | 0.027557 | 0.182 |
| w26 | 15 | 0.10798 | 9.555 |
| w27 | 4 | 0.039084 | 2.817 |
| w28 | 15 | -0.096009 | -8.877 |
| w29 | 3 | -0.048344 | -2.491 |
| w30 | 15 | -0.1325 | -24.201 |
| w31 | 15 | -0.026873 | -4.683 |
| w32 | 13 | -0.099832 | -13.031 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 14 | 0.120063 | 9.702 |
| w18 | 5 | -0.05877 | -2.056 |
| w19 | 15 | 0.105684 | 7.898 |
| w20 | 13 | 0.163014 | 20.664 |
| w21 | 12 | 0.107034 | 10.795 |
| w22 | 2 | 0.006602 | -0.422 |
| w23 | 10 | 0.023438 | 0.277 |
| w24 | 8 | -0.044817 | -13.672 |
| w25 | 0 | None | 0.0 |
| w26 | 17 | 0.128206 | 12.601 |
| w27 | 4 | -0.03151 | -1.007 |
| w28 | 11 | -0.017786 | -1.712 |
| w29 | 3 | -0.028773 | -1.928 |
| w30 | 18 | -0.015909 | 0.107 |
| w31 | 17 | 0.009954 | -0.956 |
| w32 | 13 | 0.043118 | 4.548 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 17 | 0.0905 | 8.593 |
| w29 | 3 | -0.078621 | -1.002 |
| w30 | 7 | 0.021879 | 2.424 |
| w31 | 8 | -0.034517 | -4.76 |
| w32 | 14 | 0.065016 | 3.329 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 0 | None | 0.0 |
| w15 | 9 | 0.054944 | 3.686 |
| w16 | 1 | 0.016188 | 0.168 |
| w17 | 8 | -0.105761 | -6.091 |
| w18 | 7 | 0.028656 | 1.914 |
| w19 | 10 | 0.028544 | 3.169 |
| w20 | 11 | -0.18184 | -11.619 |
| w21 | 10 | 0.033557 | 0.668 |
| w22 | 4 | -0.158439 | -9.537 |
| w23 | 6 | 0.101021 | 7.821 |
| w24 | 7 | 0.031931 | 0.164 |
| w25 | 1 | -0.023624 | -2.833 |
| w26 | 16 | -0.107116 | -10.999 |
| w27 | 3 | -0.021818 | -1.861 |
| w28 | 12 | 0.010306 | 2.886 |
| w29 | 3 | -0.019546 | -1.142 |
| w30 | 12 | -0.02956 | -0.33 |
| w31 | 12 | -0.001304 | -0.889 |
| w32 | 11 | -0.133329 | -11.956 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 4 | 0.029854 | -0.556 |
| w26 | 5 | 0.074612 | 3.486 |
| w27 | 4 | -0.047299 | -2.395 |
| w28 | 13 | 0.001862 | -0.301 |
| w29 | 1 | -0.038936 | -2.467 |
| w30 | 16 | -0.053712 | -4.537 |
| w31 | 9 | -0.032744 | -4.663 |
| w32 | 6 | -0.026399 | -4.154 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

