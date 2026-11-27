# Backtest of 031-02.b1.b1.b1.d1.g2_wide-day-after-strong-month_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.d1.g2_wide-day-after-strong-month_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.068494 | -2.137 |
| w2 | 10 | 0.037067 | 46.722 |
| w3 | 26 | 0.113046 | 47.347 |
| w4 | 15 | -0.213531 | -18.58 |
| w5 | 21 | 0.050132 | 61.485 |
| w6 | 26 | 0.109459 | 89.503 |
| w7 | 1 | -0.058018 | -6.53 |
| w8 | 6 | 0.169007 | 8.296 |
| w9 | 2 | -0.128533 | -3.592 |
| w10 | 10 | -0.035458 | -1.206 |
| w11 | 19 | -0.042397 | 24.133 |
| w12 | 4 | 0.159718 | 3.33 |
| w13 | 24 | -0.042493 | 3.135 |
| w14 | 10 | -0.008233 | 2.357 |
| w15 | 21 | 0.015586 | 38.306 |
| w16 | 16 | 0.012013 | 9.838 |
| w17 | 8 | 0.051033 | 6.11 |
| w18 | 9 | -0.097681 | -2.564 |
| w19 | 2 | -0.101487 | -3.551 |
| w20 | 8 | 0.062728 | -1.421 |
| w21 | 5 | -0.018531 | -7.067 |
| w22 | 18 | 0.072437 | 29.732 |
| w23 | 6 | 0.107026 | 14.261 |
| w24 | 20 | 0.035139 | 40.752 |
| w25 | 14 | -0.003593 | 24.544 |
| w26 | 13 | -0.040468 | -9.626 |
| w27 | 20 | 0.095057 | 30.185 |
| w28 | 9 | -0.012864 | -2.885 |
| w29 | 14 | 0.014981 | 5.953 |
| w30 | 6 | 0.081583 | -5.347 |
| w31 | 7 | -0.050433 | -6.495 |
| w32 | 7 | 0.20601 | 29.306 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.014626 | 10.162 |
| w2 | 14 | -0.08656 | -29.056 |
| w3 | 13 | -0.101028 | -17.325 |
| w4 | 20 | -0.027391 | -14.907 |
| w5 | 20 | -0.003087 | 11.056 |
| w6 | 17 | 0.199538 | 84.761 |
| w7 | 5 | 0.023453 | 0.043 |
| w8 | 5 | -0.077993 | -7.48 |
| w9 | 4 | -0.115049 | -8.877 |
| w10 | 15 | -0.003351 | 14.091 |
| w11 | 13 | -0.067148 | -5.976 |
| w12 | 5 | 0.054402 | -1.351 |
| w13 | 16 | -0.033204 | 1.584 |
| w14 | 15 | -0.010882 | 17.286 |
| w15 | 27 | 0.136836 | 23.584 |
| w16 | 24 | -0.170065 | -10.621 |
| w17 | 10 | 0.080344 | -5.817 |
| w18 | 11 | -0.01046 | -19.908 |
| w19 | 2 | -0.085065 | -5.851 |
| w20 | 7 | 0.021605 | -2.008 |
| w21 | 14 | -0.021106 | -6.537 |
| w22 | 13 | -0.117057 | 4.622 |
| w23 | 4 | 0.082119 | -1.877 |
| w24 | 13 | -0.131045 | -13.906 |
| w25 | 13 | 0.020711 | 12.448 |
| w26 | 7 | -0.042977 | -5.804 |
| w27 | 22 | 0.027286 | 41.424 |
| w28 | 9 | -0.060564 | -5.124 |
| w29 | 14 | 0.174544 | 20.973 |
| w30 | 5 | -0.312104 | -26.892 |
| w31 | 2 | -0.077403 | -2.273 |
| w32 | 12 | 0.048671 | 1.415 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 19 | 0.073637 | 68.777 |
| w7 | 7 | 0.021606 | 1.651 |
| w8 | 1 | -0.005816 | -0.274 |
| w9 | 9 | 0.183877 | 13.006 |
| w10 | 8 | -0.060614 | -2.227 |
| w11 | 6 | -0.09449 | -17.631 |
| w12 | 9 | -0.082042 | -8.385 |
| w13 | 11 | -0.090005 | -8.209 |
| w14 | 13 | 0.187187 | 57.452 |
| w15 | 8 | 0.261164 | 117.914 |
| w16 | 10 | -0.107682 | -4.634 |
| w17 | 8 | 0.087936 | 24.508 |
| w18 | 7 | 0.01444 | -0.428 |
| w19 | 10 | 0.133101 | 1.309 |
| w20 | 1 | -0.041414 | -3.993 |
| w21 | 7 | 0.170328 | 27.095 |
| w22 | 15 | -0.101966 | -1.985 |
| w23 | 11 | -0.124269 | -11.038 |
| w24 | 15 | 0.011294 | -9.663 |
| w25 | 11 | -0.105542 | -21.762 |
| w26 | 7 | -0.034797 | 8.137 |
| w27 | 15 | 0.210902 | 155.147 |
| w28 | 8 | -0.141689 | -3.158 |
| w29 | 12 | 0.157382 | 33.3 |
| w30 | 4 | -0.202863 | -3.381 |
| w31 | 8 | -0.151791 | -19.844 |
| w32 | 7 | 0.231002 | 16.107 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 2 | 0.164016 | 26.585 |
| w8 | 6 | 0.013674 | -6.477 |
| w9 | 11 | 0.032158 | -1.134 |
| w10 | 17 | 0.066458 | 3.8 |
| w11 | 11 | -0.091716 | -2.451 |
| w12 | 6 | 0.023629 | -2.256 |
| w13 | 12 | -0.114725 | 8.087 |
| w14 | 13 | 0.069916 | 20.482 |
| w15 | 19 | -0.049621 | -17.117 |
| w16 | 14 | -0.035342 | 6.665 |
| w17 | 13 | 0.002836 | 11.336 |
| w18 | 6 | -0.236936 | -16.152 |
| w19 | 5 | -0.036975 | -5.071 |
| w20 | 5 | -0.095778 | -8.889 |
| w21 | 9 | 0.064836 | -14.037 |
| w22 | 8 | 0.104512 | 19.089 |
| w23 | 5 | 0.359366 | 70.585 |
| w24 | 17 | -0.08066 | -5.13 |
| w25 | 14 | -0.145019 | -5.58 |
| w26 | 5 | 0.064256 | -2.864 |
| w27 | 15 | -0.013218 | 2.53 |
| w28 | 3 | 0.010925 | -2.544 |
| w29 | 17 | -0.113385 | -8.686 |
| w30 | 11 | -0.14883 | -10.406 |
| w31 | 4 | -0.053245 | -6.104 |
| w32 | 7 | 0.049576 | 5.082 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | 0.108496 | 90.039 |
| w2 | 15 | -0.065939 | -13.219 |
| w3 | 7 | -0.04389 | 0.49 |
| w4 | 18 | 0.222898 | 144.395 |
| w5 | 21 | 0.000572 | 32.498 |
| w6 | 15 | 0.19008 | 87.444 |
| w7 | 9 | -0.094421 | -0.984 |
| w8 | 4 | 0.016912 | 3.779 |
| w9 | 7 | 0.075763 | 2.302 |
| w10 | 12 | -0.112482 | -9.793 |
| w11 | 9 | 0.026848 | 5.657 |
| w12 | 8 | -0.132209 | -8.429 |
| w13 | 21 | -0.026597 | 30.99 |
| w14 | 12 | 0.103431 | 62.408 |
| w15 | 25 | 0.036676 | 17.923 |
| w16 | 19 | 0.073534 | 41.143 |
| w17 | 13 | -0.010035 | -13.33 |
| w18 | 12 | 0.01462 | 2.661 |
| w19 | 6 | -0.036481 | -11.94 |
| w20 | 6 | 0.031 | 6.105 |
| w21 | 12 | -0.011289 | 1.201 |
| w22 | 17 | 0.11117 | 35.491 |
| w23 | 10 | -0.076016 | -3.839 |
| w24 | 21 | -0.074974 | -5.445 |
| w25 | 17 | 0.000315 | 9.914 |
| w26 | 10 | 0.059757 | 6.008 |
| w27 | 16 | -0.092461 | 5.783 |
| w28 | 2 | -0.081286 | -0.544 |
| w29 | 23 | 0.152716 | 33.577 |
| w30 | 3 | -0.050136 | -4.807 |
| w31 | 8 | -0.076742 | -13.725 |
| w32 | 3 | 0.1482 | 10.047 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 16 | 0.039518 | 14.967 |
| w11 | 8 | -0.098781 | -1.249 |
| w12 | 8 | 0.011594 | -4.474 |
| w13 | 24 | 0.01973 | 25.819 |
| w14 | 20 | 0.115124 | 29.006 |
| w15 | 12 | 0.112927 | 6.311 |
| w16 | 19 | 0.047491 | 55.177 |
| w17 | 15 | 0.151287 | 46.435 |
| w18 | 3 | -0.099023 | -2.616 |
| w19 | 7 | 0.028608 | -3.045 |
| w20 | 9 | -0.069076 | -6.4 |
| w21 | 4 | -0.106716 | -7.517 |
| w22 | 17 | 0.090376 | 27.571 |
| w23 | 5 | -0.172866 | -12.367 |
| w24 | 14 | 0.176184 | 113.786 |
| w25 | 9 | 0.02574 | -2.91 |
| w26 | 4 | -0.029212 | -3.759 |
| w27 | 15 | 0.079302 | 89.003 |
| w28 | 5 | -0.164027 | -7.42 |
| w29 | 17 | 0.015906 | -2.723 |
| w30 | 1 | -0.08594 | -0.702 |
| w31 | 3 | -0.110228 | -9.195 |
| w32 | 21 | 0.126062 | 8.772 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 7 | 0.023368 | 0.315 |
| w13 | 17 | -0.055948 | -11.913 |
| w14 | 22 | 0.243185 | 93.099 |
| w15 | 7 | -0.098938 | 1.491 |
| w16 | 22 | -0.02806 | 10.835 |
| w17 | 13 | 0.108753 | 0.637 |
| w18 | 7 | -0.014055 | 11.723 |
| w19 | 7 | -0.02827 | -4.784 |
| w20 | 8 | -0.071566 | -8.732 |
| w21 | 14 | 0.101016 | 3.984 |
| w22 | 16 | 0.032199 | 16.563 |
| w23 | 2 | 0.085059 | 4.164 |
| w24 | 22 | -0.068052 | -9.314 |
| w25 | 11 | 0.093756 | 23.579 |
| w26 | 2 | -0.038929 | -2.63 |
| w27 | 14 | -0.039098 | -3.625 |
| w28 | 1 | 0.134088 | 3.072 |
| w29 | 19 | 0.147103 | 7.502 |
| w30 | 0 | None | 0.0 |
| w31 | 9 | -0.15333 | -14.428 |
| w32 | 11 | 0.031796 | -0.083 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 7 | -0.020804 | -7.702 |
| w16 | 18 | -0.077338 | 17.339 |
| w17 | 14 | 0.128531 | 3.268 |
| w18 | 10 | 0.108917 | 33.148 |
| w19 | 6 | -0.040689 | -8.671 |
| w20 | 6 | -0.054394 | -8.079 |
| w21 | 7 | -0.047118 | -12.223 |
| w22 | 16 | 0.056374 | 12.725 |
| w23 | 0 | None | 0.0 |
| w24 | 14 | 0.046538 | 53.71 |
| w25 | 17 | 0.165134 | 10.472 |
| w26 | 2 | -0.025345 | -0.861 |
| w27 | 12 | 0.103017 | 105.166 |
| w28 | 4 | 0.087786 | 0.128 |
| w29 | 13 | -0.03981 | 23.197 |
| w30 | 0 | -0.021626 | 0.0 |
| w31 | 10 | 0.110813 | 1.653 |
| w32 | 9 | 0.075061 | 5.637 |

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
| w15 | 6 | -0.05723 | -18.116 |
| w16 | 17 | -0.037164 | 6.465 |
| w17 | 3 | 0.021026 | 7.074 |
| w18 | 14 | -0.041186 | -20.401 |
| w19 | 10 | 0.095492 | 2.112 |
| w20 | 7 | 0.041322 | -0.707 |
| w21 | 10 | -0.120834 | -7.637 |
| w22 | 10 | -0.056343 | 13.271 |
| w23 | 16 | 0.027239 | -11.798 |
| w24 | 25 | 0.130259 | 28.526 |
| w25 | 9 | -0.085651 | -4.501 |
| w26 | 12 | 0.107592 | 17.321 |
| w27 | 17 | 0.160079 | 93.639 |
| w28 | 8 | -0.106566 | 3.296 |
| w29 | 20 | -0.047384 | -10.945 |
| w30 | 0 | None | 0.0 |
| w31 | 24 | -0.242922 | -0.293 |
| w32 | 12 | 0.14602 | 3.648 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 19 | 0.160771 | 51.332 |
| w17 | 17 | 0.025183 | 18.065 |
| w18 | 14 | 0.037785 | 4.156 |
| w19 | 8 | 0.049867 | 5.36 |
| w20 | 6 | -0.08099 | -6.677 |
| w21 | 6 | -0.271799 | -20.87 |
| w22 | 16 | -0.013164 | -1.043 |
| w23 | 2 | 0.070551 | 1.943 |
| w24 | 9 | -0.021365 | 5.359 |
| w25 | 16 | 0.036365 | 15.58 |
| w26 | 2 | 0.018684 | -3.317 |
| w27 | 12 | 0.058788 | 16.594 |
| w28 | 1 | -0.291029 | -2.939 |
| w29 | 14 | 0.143261 | 13.811 |
| w30 | 9 | 0.023791 | -9.626 |
| w31 | 5 | -0.116565 | -12.736 |
| w32 | 7 | 0.10728 | 4.463 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 7 | 0.042245 | 3.153 |
| w21 | 8 | -0.087331 | -12.326 |
| w22 | 9 | 0.054638 | 20.747 |
| w23 | 8 | 0.049723 | -2.599 |
| w24 | 17 | 0.193944 | 89.135 |
| w25 | 8 | 0.107511 | 12.784 |
| w26 | 6 | -0.065693 | -11.04 |
| w27 | 15 | -0.002958 | 1.994 |
| w28 | 2 | 0.025523 | 0.234 |
| w29 | 17 | 0.067496 | 12.219 |
| w30 | 7 | 0.025728 | -6.764 |
| w31 | 8 | -0.034751 | -9.052 |
| w32 | 10 | 0.099603 | 2.168 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 11 | 0.117348 | 28.892 |
| w23 | 5 | 0.119501 | -0.076 |
| w24 | 23 | 0.201186 | 78.751 |
| w25 | 16 | -0.068971 | 30.014 |
| w26 | 8 | 0.022254 | -4.41 |
| w27 | 15 | -0.107802 | 7.819 |
| w28 | 1 | -0.047262 | -0.943 |
| w29 | 9 | 0.008552 | 4.305 |
| w30 | 13 | -0.006114 | -7.867 |
| w31 | 5 | -0.087778 | -6.784 |
| w32 | 13 | -0.194807 | 9.443 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 19 | -0.034456 | -1.755 |
| w25 | 8 | -0.023631 | 8.143 |
| w26 | 5 | -0.074676 | -12.35 |
| w27 | 24 | 0.083301 | 36.361 |
| w28 | 9 | 0.166767 | 13.992 |
| w29 | 13 | 0.019662 | -1.646 |
| w30 | 7 | 0.068479 | -3.389 |
| w31 | 5 | -0.060976 | -7.913 |
| w32 | 8 | 0.279464 | 34.546 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 18 | 0.11271 | 33.06 |
| w6 | 18 | 0.06033 | 11.107 |
| w7 | 9 | 0.033557 | 3.617 |
| w8 | 8 | -0.049212 | -8.845 |
| w9 | 3 | -0.064547 | -10.115 |
| w10 | 8 | 0.018183 | -0.946 |
| w11 | 8 | -0.006974 | -2.218 |
| w12 | 8 | -0.104255 | -11.069 |
| w13 | 19 | 0.057771 | 44.251 |
| w14 | 17 | -0.076244 | -9.701 |
| w15 | 11 | 0.002465 | -0.769 |
| w16 | 22 | 0.017765 | 9.3 |
| w17 | 16 | 0.08829 | 1.131 |
| w18 | 17 | 0.012441 | 9.539 |
| w19 | 8 | 0.017089 | 4.24 |
| w20 | 3 | 0.055112 | -0.247 |
| w21 | 7 | 0.072891 | -2.282 |
| w22 | 10 | -0.029487 | 0.179 |
| w23 | 5 | -0.08864 | -14.738 |
| w24 | 11 | -0.080838 | -1.208 |
| w25 | 10 | 0.030509 | 17.346 |
| w26 | 17 | 0.08106 | 7.602 |
| w27 | 24 | -0.082319 | 22.996 |
| w28 | 8 | -0.125532 | -14.254 |
| w29 | 13 | -0.025911 | 9.02 |
| w30 | 21 | 0.287449 | 184.563 |
| w31 | 6 | -0.006894 | -2.194 |
| w32 | 14 | 0.136108 | 33.422 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 13 | 0.070497 | 76.363 |
| w6 | 15 | 0.00729 | 14.461 |
| w7 | 7 | 0.02742 | 4.861 |
| w8 | 2 | -0.064369 | -1.188 |
| w9 | 6 | 0.040371 | -20.937 |
| w10 | 17 | -0.036211 | 6.985 |
| w11 | 17 | -0.155272 | -25.124 |
| w12 | 5 | -0.153117 | -10.936 |
| w13 | 18 | 0.019772 | 28.0 |
| w14 | 15 | -0.122587 | -15.074 |
| w15 | 11 | -0.130703 | -1.47 |
| w16 | 19 | -0.083168 | 22.157 |
| w17 | 10 | 0.03137 | -5.559 |
| w18 | 4 | -0.15758 | -11.08 |
| w19 | 13 | -0.168769 | -19.129 |
| w20 | 8 | 0.057782 | 3.162 |
| w21 | 6 | -0.025662 | -3.721 |
| w22 | 7 | 0.046625 | 5.077 |
| w23 | 5 | 0.026971 | 0.243 |
| w24 | 21 | -0.015848 | -2.092 |
| w25 | 4 | 0.053388 | 5.796 |
| w26 | 14 | 0.289939 | 24.944 |
| w27 | 4 | -0.06229 | 7.233 |
| w28 | 8 | -0.002798 | 2.094 |
| w29 | 8 | -0.180208 | -10.996 |
| w30 | 14 | -0.13263 | -13.694 |
| w31 | 9 | -0.094415 | -19.322 |
| w32 | 14 | 0.007425 | 34.532 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 12 | 0.027079 | 6.534 |
| w18 | 14 | 0.007175 | 13.44 |
| w19 | 11 | 0.017842 | -5.688 |
| w20 | 12 | -0.081499 | -3.844 |
| w21 | 2 | -0.164995 | -13.997 |
| w22 | 10 | 0.044621 | 15.537 |
| w23 | 7 | 0.06039 | 0.316 |
| w24 | 16 | 0.162006 | 27.657 |
| w25 | 13 | 0.100635 | 32.296 |
| w26 | 9 | 0.036571 | 2.559 |
| w27 | 12 | 0.177918 | 122.848 |
| w28 | 7 | -0.047478 | -0.96 |
| w29 | 8 | 0.287625 | 54.254 |
| w30 | 1 | -0.068748 | -0.559 |
| w31 | 7 | -0.04759 | -5.246 |
| w32 | 18 | 0.10274 | 28.291 |

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
| w17 | 13 | 0.100054 | 5.49 |
| w18 | 10 | -0.07203 | 2.236 |
| w19 | 5 | 0.04473 | 2.599 |
| w20 | 12 | 0.033637 | -6.28 |
| w21 | 10 | -0.048659 | -26.118 |
| w22 | 11 | 0.179618 | 42.003 |
| w23 | 7 | -0.183592 | -11.364 |
| w24 | 30 | -0.053698 | 7.381 |
| w25 | 10 | 0.184455 | 27.718 |
| w26 | 14 | -0.005236 | -1.499 |
| w27 | 17 | 0.012494 | 10.96 |
| w28 | 4 | 0.049212 | 0.481 |
| w29 | 18 | 0.032287 | 10.504 |
| w30 | 0 | None | 0.0 |
| w31 | 6 | -0.089465 | -19.86 |
| w32 | 8 | 0.124032 | 11.735 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 5 | -0.223204 | -16.627 |
| w20 | 9 | 0.070988 | -7.806 |
| w21 | 11 | 0.07668 | 5.4 |
| w22 | 21 | -0.04438 | 28.141 |
| w23 | 9 | 0.06961 | -5.568 |
| w24 | 22 | 0.180307 | 132.535 |
| w25 | 10 | 0.04085 | -8.692 |
| w26 | 10 | -0.083611 | -17.992 |
| w27 | 13 | 0.024913 | -0.801 |
| w28 | 8 | 0.01853 | -2.492 |
| w29 | 16 | -0.073804 | -18.239 |
| w30 | 1 | 0.009782 | -2.899 |
| w31 | 8 | -0.087361 | -21.518 |
| w32 | 14 | 0.005467 | 44.159 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 10 | -0.028755 | 15.902 |
| w23 | 12 | -0.001484 | -7.61 |
| w24 | 19 | -0.092065 | -12.371 |
| w25 | 10 | -0.036116 | -10.894 |
| w26 | 8 | 0.002868 | -2.664 |
| w27 | 18 | -0.062241 | 15.017 |
| w28 | 3 | -0.168616 | -12.636 |
| w29 | 22 | 0.051928 | 1.637 |
| w30 | 1 | -0.05049 | -0.648 |
| w31 | 17 | -0.037837 | -12.116 |
| w32 | 10 | -0.078284 | -7.598 |

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
| w27 | 18 | 0.148495 | 37.244 |
| w28 | 6 | -0.047545 | -6.382 |
| w29 | 12 | -0.036386 | -8.393 |
| w30 | 4 | 0.057148 | -0.382 |
| w31 | 4 | -0.182027 | -11.285 |
| w32 | 14 | 0.272933 | 71.16 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 6 | 0.02101 | 4.392 |
| w18 | 3 | -0.095605 | -9.03 |
| w19 | 6 | 0.137876 | 9.706 |
| w20 | 4 | 0.04187 | -0.637 |
| w21 | 4 | -0.020053 | -3.927 |
| w22 | 17 | 0.07609 | 27.515 |
| w23 | 7 | -0.134142 | -13.539 |
| w24 | 14 | -0.102201 | 15.788 |
| w25 | 11 | 0.148442 | 19.95 |
| w26 | 6 | -0.020742 | -5.896 |
| w27 | 18 | 0.074339 | 12.147 |
| w28 | 1 | -0.252709 | -1.159 |
| w29 | 11 | -0.013293 | -13.615 |
| w30 | 5 | 0.252125 | 21.594 |
| w31 | 10 | -0.037527 | -16.356 |
| w32 | 6 | -0.018865 | -4.73 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 4 | 0.116775 | 22.897 |
| w18 | 7 | -0.147548 | -21.648 |
| w19 | 6 | 0.137404 | -5.195 |
| w20 | 10 | 0.003247 | -6.719 |
| w21 | 7 | -0.095895 | -10.976 |
| w22 | 17 | -0.026873 | 77.806 |
| w23 | 7 | 0.126242 | -3.285 |
| w24 | 16 | 0.103711 | 28.03 |
| w25 | 9 | 0.169619 | 62.256 |
| w26 | 8 | -0.008779 | -4.809 |
| w27 | 15 | -0.129922 | 6.462 |
| w28 | 2 | 0.064295 | -1.264 |
| w29 | 15 | 0.11778 | -3.868 |
| w30 | 5 | -0.055938 | -1.806 |
| w31 | 6 | -0.198293 | -6.119 |
| w32 | 15 | -0.068823 | -3.732 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 3 | 0.016325 | -0.888 |
| w29 | 14 | 0.016275 | 0.582 |
| w30 | 3 | 0.109212 | 3.229 |
| w31 | 10 | -0.059559 | -6.724 |
| w32 | 11 | 0.087375 | 19.376 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 11 | 0.230187 | 38.214 |
| w15 | 16 | -0.028328 | 35.417 |
| w16 | 15 | 0.049209 | 195.627 |
| w17 | 10 | 0.023677 | 9.351 |
| w18 | 6 | -0.074699 | -7.342 |
| w19 | 7 | 0.036144 | 4.914 |
| w20 | 4 | -0.17022 | -11.925 |
| w21 | 6 | 0.201088 | 67.551 |
| w22 | 12 | 0.083836 | 0.879 |
| w23 | 9 | -0.028049 | -0.897 |
| w24 | 16 | -0.017535 | -4.87 |
| w25 | 8 | 0.233119 | 68.84 |
| w26 | 5 | 0.04454 | -6.361 |
| w27 | 16 | 0.161466 | 74.425 |
| w28 | 4 | -0.148148 | -2.695 |
| w29 | 17 | 0.068029 | 22.193 |
| w30 | 7 | -0.045431 | -8.658 |
| w31 | 8 | -0.043393 | -11.227 |
| w32 | 5 | 0.302868 | 23.368 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 13 | 0.286893 | 135.329 |
| w26 | 10 | 0.09494 | 17.283 |
| w27 | 12 | 0.224595 | 42.029 |
| w28 | 5 | -0.011583 | -3.305 |
| w29 | 12 | 0.091051 | 11.789 |
| w30 | 2 | 0.013982 | -1.379 |
| w31 | 11 | 0.056959 | -8.835 |
| w32 | 10 | 0.214931 | 14.561 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

