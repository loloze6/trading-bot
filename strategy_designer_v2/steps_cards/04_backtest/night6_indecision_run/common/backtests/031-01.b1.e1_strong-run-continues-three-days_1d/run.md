# Backtest of 031-01.b1.e1_strong-run-continues-three-days_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-01.b1.e1_strong-run-continues-three-days_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 49 | -0.066262 | -5.806 |
| w2 | 36 | 0.149432 | 58.462 |
| w3 | 59 | 0.001378 | 62.834 |
| w4 | 54 | -0.038327 | -20.938 |
| w5 | 53 | -0.012643 | 47.993 |
| w6 | 47 | 0.130021 | 88.742 |
| w7 | 38 | 0.03014 | 6.927 |
| w8 | 42 | 0.083055 | 9.181 |
| w9 | 32 | -0.008391 | -18.485 |
| w10 | 35 | 0.030924 | 24.846 |
| w11 | 42 | 0.124947 | 72.719 |
| w12 | 31 | -0.054214 | -17.551 |
| w13 | 56 | -0.013111 | 1.38 |
| w14 | 42 | -0.001729 | 16.084 |
| w15 | 55 | 0.043764 | 49.937 |
| w16 | 50 | 0.066723 | 46.018 |
| w17 | 38 | 0.038905 | -3.789 |
| w18 | 48 | 0.053955 | -10.747 |
| w19 | 35 | -0.038074 | -1.069 |
| w20 | 37 | -0.001031 | -14.709 |
| w21 | 42 | -0.09928 | -19.031 |
| w22 | 40 | 0.107077 | 79.811 |
| w23 | 37 | -0.082748 | -16.282 |
| w24 | 53 | 0.074139 | 59.883 |
| w25 | 41 | 0.083173 | 40.527 |
| w26 | 44 | -0.007529 | -0.41 |
| w27 | 53 | 0.007122 | 33.837 |
| w28 | 41 | -0.070025 | -10.132 |
| w29 | 46 | -0.063309 | 2.595 |
| w30 | 34 | 0.090889 | 1.868 |
| w31 | 37 | -0.043156 | -10.547 |
| w32 | 40 | 0.198839 | 36.056 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 51 | -0.16883 | 2.474 |
| w2 | 40 | -0.041341 | -4.277 |
| w3 | 58 | -0.127888 | -21.401 |
| w4 | 46 | -0.07323 | 18.999 |
| w5 | 43 | -0.018973 | 34.079 |
| w6 | 36 | 0.099746 | 52.245 |
| w7 | 32 | -0.032973 | -0.475 |
| w8 | 36 | -0.007476 | -11.71 |
| w9 | 31 | -0.01042 | -17.926 |
| w10 | 41 | -0.097741 | 2.863 |
| w11 | 38 | 0.075249 | 9.057 |
| w12 | 34 | -0.08112 | -24.799 |
| w13 | 57 | -0.015844 | 10.743 |
| w14 | 40 | 0.066013 | 22.761 |
| w15 | 43 | -0.012644 | 0.771 |
| w16 | 56 | 0.00558 | 28.453 |
| w17 | 34 | 0.071277 | 25.218 |
| w18 | 40 | 0.023585 | -6.371 |
| w19 | 34 | 0.002554 | 1.358 |
| w20 | 37 | -0.094626 | -19.9 |
| w21 | 47 | -0.107317 | -10.232 |
| w22 | 50 | -0.088874 | -7.886 |
| w23 | 32 | 0.014081 | 1.844 |
| w24 | 42 | -0.142598 | -10.316 |
| w25 | 43 | 0.003365 | 12.211 |
| w26 | 32 | 0.001477 | -10.6 |
| w27 | 59 | -0.020151 | 21.105 |
| w28 | 41 | -0.013456 | -12.59 |
| w29 | 45 | 0.009106 | 18.51 |
| w30 | 37 | -0.144981 | -22.094 |
| w31 | 44 | -0.112035 | -19.936 |
| w32 | 33 | 0.08372 | 10.98 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 49 | 0.095596 | 97.193 |
| w7 | 24 | 0.153655 | 15.399 |
| w8 | 27 | -0.058326 | -15.91 |
| w9 | 29 | 0.16402 | 37.728 |
| w10 | 28 | -0.012306 | -3.337 |
| w11 | 32 | 0.061698 | 8.319 |
| w12 | 41 | -0.057812 | -17.507 |
| w13 | 47 | -0.042462 | -6.07 |
| w14 | 36 | 0.24501 | 75.079 |
| w15 | 38 | 0.199477 | 110.685 |
| w16 | 46 | 0.102716 | 91.134 |
| w17 | 32 | 0.067432 | 30.605 |
| w18 | 43 | 0.004325 | -9.368 |
| w19 | 33 | -0.016602 | 2.409 |
| w20 | 13 | -0.010974 | -4.933 |
| w21 | 44 | -0.036017 | -5.314 |
| w22 | 52 | -0.045493 | 9.381 |
| w23 | 30 | -0.001916 | 51.441 |
| w24 | 45 | 0.00235 | 23.743 |
| w25 | 39 | -0.065624 | -17.385 |
| w26 | 44 | 0.084577 | 11.307 |
| w27 | 41 | 0.243483 | 197.092 |
| w28 | 42 | -0.059642 | -6.808 |
| w29 | 29 | 0.154976 | 52.97 |
| w30 | 35 | 0.038704 | -2.914 |
| w31 | 29 | 0.017564 | -3.991 |
| w32 | 32 | 0.136398 | 24.283 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 34 | 0.093994 | 22.017 |
| w8 | 33 | -0.020958 | -8.412 |
| w9 | 22 | 0.196905 | 16.18 |
| w10 | 27 | 0.029797 | 17.18 |
| w11 | 39 | -0.091968 | -17.256 |
| w12 | 36 | -0.029067 | -18.706 |
| w13 | 58 | -0.040792 | 3.796 |
| w14 | 42 | -0.03283 | 1.547 |
| w15 | 41 | -0.093142 | -26.912 |
| w16 | 50 | 0.042049 | 37.704 |
| w17 | 39 | 0.013431 | 11.752 |
| w18 | 43 | 0.001256 | -16.722 |
| w19 | 38 | 0.07153 | -1.209 |
| w20 | 27 | -0.07437 | -20.363 |
| w21 | 40 | -0.192053 | -19.705 |
| w22 | 47 | 0.034422 | 26.815 |
| w23 | 33 | 0.227014 | 73.216 |
| w24 | 41 | 0.023571 | 8.032 |
| w25 | 35 | 0.198639 | 103.798 |
| w26 | 40 | -0.033899 | -8.743 |
| w27 | 49 | -0.040086 | 7.577 |
| w28 | 37 | -0.056973 | -13.452 |
| w29 | 58 | -0.249109 | -25.668 |
| w30 | 48 | -0.111345 | -9.22 |
| w31 | 41 | -0.124455 | -15.428 |
| w32 | 25 | 0.239538 | 44.488 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 48 | 0.107257 | 104.159 |
| w2 | 45 | -0.017843 | 4.452 |
| w3 | 35 | 0.013457 | -3.529 |
| w4 | 44 | 0.152058 | 200.625 |
| w5 | 47 | 0.064607 | 71.896 |
| w6 | 44 | 0.01604 | 23.506 |
| w7 | 39 | 0.148718 | 39.955 |
| w8 | 38 | -0.007089 | -10.954 |
| w9 | 30 | 0.056267 | 0.482 |
| w10 | 39 | 0.023931 | 2.68 |
| w11 | 41 | 0.114527 | 33.719 |
| w12 | 36 | 0.005696 | -7.482 |
| w13 | 60 | -0.021085 | 29.957 |
| w14 | 46 | 0.141602 | 81.489 |
| w15 | 42 | -0.050421 | -0.193 |
| w16 | 55 | -0.029518 | 56.875 |
| w17 | 44 | 0.048694 | 34.275 |
| w18 | 47 | -0.083411 | -17.994 |
| w19 | 40 | 0.03615 | 0.574 |
| w20 | 38 | 0.049837 | -8.686 |
| w21 | 43 | 0.02418 | 4.263 |
| w22 | 46 | 0.001825 | 31.451 |
| w23 | 38 | -0.088978 | -12.042 |
| w24 | 47 | 0.000515 | 25.98 |
| w25 | 42 | 0.155143 | 69.88 |
| w26 | 30 | 0.134503 | 9.664 |
| w27 | 47 | -0.064129 | 1.225 |
| w28 | 35 | -0.147245 | -28.53 |
| w29 | 39 | 0.016352 | 69.497 |
| w30 | 32 | -0.041641 | -9.832 |
| w31 | 38 | -0.066328 | -20.7 |
| w32 | 38 | 0.12883 | 30.293 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 45 | 0.031788 | 26.228 |
| w11 | 34 | -0.055493 | -14.177 |
| w12 | 38 | -0.066169 | -14.554 |
| w13 | 58 | -0.024252 | 11.76 |
| w14 | 46 | 0.047394 | 40.892 |
| w15 | 39 | -0.005907 | 3.334 |
| w16 | 44 | 0.013388 | 79.737 |
| w17 | 52 | 0.012036 | 34.534 |
| w18 | 28 | -0.115708 | -28.931 |
| w19 | 26 | 0.152639 | 24.537 |
| w20 | 42 | -0.070173 | -24.796 |
| w21 | 33 | -0.031884 | -10.566 |
| w22 | 54 | -0.011735 | 25.062 |
| w23 | 32 | -0.116786 | -10.197 |
| w24 | 49 | 0.229272 | 198.046 |
| w25 | 36 | 0.094095 | 7.668 |
| w26 | 31 | 0.034685 | -10.048 |
| w27 | 41 | 0.15185 | 66.873 |
| w28 | 32 | -0.10394 | -14.463 |
| w29 | 38 | 0.086064 | 26.823 |
| w30 | 28 | -0.045023 | -15.46 |
| w31 | 43 | -0.156968 | -20.805 |
| w32 | 31 | 0.181114 | 32.501 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 53 | -0.019425 | 8.567 |
| w13 | 37 | -0.045597 | -24.519 |
| w14 | 54 | 0.047753 | 63.929 |
| w15 | 37 | 0.038039 | 12.181 |
| w16 | 54 | -0.047266 | 29.718 |
| w17 | 51 | -0.019551 | 6.499 |
| w18 | 39 | -0.164264 | -13.586 |
| w19 | 33 | -0.00108 | -4.878 |
| w20 | 40 | -0.039064 | -13.237 |
| w21 | 42 | -0.097537 | -18.774 |
| w22 | 37 | 0.039816 | 18.763 |
| w23 | 29 | -0.138505 | -25.422 |
| w24 | 58 | -0.129821 | -13.213 |
| w25 | 37 | 0.085243 | 5.76 |
| w26 | 35 | -0.071312 | -21.906 |
| w27 | 49 | 0.003367 | 2.599 |
| w28 | 36 | -0.14021 | -26.375 |
| w29 | 42 | -0.052325 | -11.749 |
| w30 | 22 | -0.022026 | -10.926 |
| w31 | 45 | 0.129695 | 10.939 |
| w32 | 37 | 0.013281 | -6.715 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 40 | -0.041759 | -8.033 |
| w16 | 50 | -0.000387 | 33.8 |
| w17 | 48 | -0.12966 | -14.104 |
| w18 | 37 | -0.041093 | -4.892 |
| w19 | 28 | 0.046972 | -6.952 |
| w20 | 40 | -0.099397 | -22.707 |
| w21 | 31 | 0.014069 | -8.713 |
| w22 | 43 | -0.067916 | -9.249 |
| w23 | 27 | -0.046956 | -19.903 |
| w24 | 51 | -0.044801 | 22.841 |
| w25 | 37 | 0.115835 | 16.393 |
| w26 | 31 | 0.068672 | 5.197 |
| w27 | 44 | 0.078471 | 53.955 |
| w28 | 39 | -0.023975 | -10.525 |
| w29 | 34 | 0.100489 | 21.314 |
| w30 | 30 | 0.011729 | -9.692 |
| w31 | 34 | 0.092343 | 7.192 |
| w32 | 32 | -0.020808 | -15.008 |

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
| w15 | 37 | -0.086433 | -15.264 |
| w16 | 48 | 0.0447 | 95.232 |
| w17 | 35 | 0.0525 | 17.829 |
| w18 | 46 | -0.187753 | -29.245 |
| w19 | 34 | 0.051167 | 12.237 |
| w20 | 41 | -0.043065 | -4.89 |
| w21 | 49 | -0.159151 | -21.334 |
| w22 | 49 | -0.108704 | 3.2 |
| w23 | 54 | -0.065646 | -8.189 |
| w24 | 56 | -0.133512 | 9.13 |
| w25 | 46 | 0.132572 | 31.679 |
| w26 | 57 | 0.085429 | 38.682 |
| w27 | 55 | 0.089876 | 122.826 |
| w28 | 50 | -0.230235 | -19.627 |
| w29 | 62 | -0.056295 | 25.577 |
| w30 | 42 | -0.067103 | -17.749 |
| w31 | 59 | -0.089379 | 9.841 |
| w32 | 52 | 0.1016 | 11.605 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 56 | 0.008437 | 30.31 |
| w17 | 48 | -0.041117 | -3.805 |
| w18 | 40 | -0.031969 | -8.561 |
| w19 | 42 | -0.029835 | -8.443 |
| w20 | 39 | -0.004167 | -7.065 |
| w21 | 31 | -0.124924 | -27.099 |
| w22 | 44 | -0.008324 | 23.918 |
| w23 | 29 | -0.096323 | -19.596 |
| w24 | 52 | 0.039522 | 33.042 |
| w25 | 39 | 0.15243 | 22.427 |
| w26 | 41 | -0.007358 | -12.501 |
| w27 | 43 | 0.08578 | 28.292 |
| w28 | 40 | -0.102774 | -19.363 |
| w29 | 39 | 0.014223 | -4.121 |
| w30 | 30 | -0.03032 | -13.657 |
| w31 | 29 | -0.134009 | -23.643 |
| w32 | 30 | 0.106056 | 1.358 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 29 | 0.066827 | -7.418 |
| w21 | 32 | 0.02455 | -8.506 |
| w22 | 49 | 0.036674 | 37.969 |
| w23 | 29 | -0.092779 | -20.555 |
| w24 | 44 | 0.210384 | 150.304 |
| w25 | 34 | 0.074951 | 8.178 |
| w26 | 34 | 0.043725 | -0.496 |
| w27 | 47 | -0.03714 | 3.636 |
| w28 | 39 | -0.116765 | -21.288 |
| w29 | 40 | -0.0255 | -3.892 |
| w30 | 36 | 0.040009 | 0.593 |
| w31 | 39 | -0.124709 | -20.133 |
| w32 | 30 | 0.030301 | 5.99 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 43 | -0.02604 | 12.273 |
| w23 | 35 | -0.032492 | -11.416 |
| w24 | 36 | 0.153827 | 152.754 |
| w25 | 48 | 0.036788 | 23.287 |
| w26 | 32 | 0.045741 | 2.155 |
| w27 | 45 | 0.104319 | 22.447 |
| w28 | 39 | -0.128462 | -26.14 |
| w29 | 34 | 0.018061 | -4.029 |
| w30 | 30 | -0.061353 | -8.839 |
| w31 | 35 | 0.01302 | -4.797 |
| w32 | 37 | 0.057776 | 30.444 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 46 | -0.058842 | 24.46 |
| w25 | 46 | -0.048664 | 8.476 |
| w26 | 29 | 0.096389 | 4.833 |
| w27 | 57 | -0.000979 | 45.263 |
| w28 | 27 | 0.005316 | -1.823 |
| w29 | 32 | -0.001354 | -2.171 |
| w30 | 38 | 0.006496 | -10.666 |
| w31 | 32 | 0.005203 | -6.142 |
| w32 | 37 | 0.158357 | 36.119 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 47 | 0.056289 | 75.579 |
| w6 | 38 | 0.051645 | 27.091 |
| w7 | 38 | 0.032635 | 1.62 |
| w8 | 29 | 0.041581 | -1.298 |
| w9 | 32 | 0.033772 | -14.922 |
| w10 | 34 | 0.127046 | 27.683 |
| w11 | 29 | 0.133012 | 14.5 |
| w12 | 30 | -0.078824 | -20.478 |
| w13 | 60 | 0.106849 | 50.943 |
| w14 | 50 | -0.019383 | 14.563 |
| w15 | 35 | -0.131521 | -35.622 |
| w16 | 49 | 0.127996 | 80.916 |
| w17 | 42 | 0.006514 | 5.646 |
| w18 | 40 | 0.016117 | -4.423 |
| w19 | 41 | 0.033258 | 10.364 |
| w20 | 34 | 0.001982 | -11.915 |
| w21 | 35 | -0.09581 | -24.892 |
| w22 | 51 | -0.055933 | -2.17 |
| w23 | 33 | -0.126354 | -22.292 |
| w24 | 54 | -0.173953 | -15.81 |
| w25 | 45 | 0.146793 | 20.087 |
| w26 | 37 | 0.201977 | 54.34 |
| w27 | 45 | 0.021133 | 36.574 |
| w28 | 37 | -0.117778 | -17.365 |
| w29 | 40 | -0.007093 | 5.533 |
| w30 | 52 | 0.032179 | 112.375 |
| w31 | 36 | -0.089489 | -12.548 |
| w32 | 53 | 0.106042 | 66.765 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 48 | 0.133505 | 149.885 |
| w6 | 44 | 0.033619 | 50.859 |
| w7 | 36 | 0.005293 | 10.06 |
| w8 | 30 | -0.045624 | -6.927 |
| w9 | 29 | 0.004725 | -11.565 |
| w10 | 43 | 0.065045 | 16.3 |
| w11 | 44 | 0.040774 | 7.952 |
| w12 | 34 | -0.069165 | -17.839 |
| w13 | 49 | 0.031757 | 31.857 |
| w14 | 51 | -0.086541 | 10.359 |
| w15 | 49 | -0.102027 | -7.504 |
| w16 | 56 | 0.030079 | 55.676 |
| w17 | 42 | -0.024047 | -8.163 |
| w18 | 37 | -0.003001 | -18.812 |
| w19 | 46 | -0.131098 | -13.175 |
| w20 | 56 | -0.075674 | -19.482 |
| w21 | 54 | -0.261725 | -31.536 |
| w22 | 44 | -0.075448 | -7.841 |
| w23 | 35 | 0.101244 | -3.863 |
| w24 | 57 | -0.164704 | -8.935 |
| w25 | 44 | -0.014787 | -27.004 |
| w26 | 56 | -0.076686 | -0.253 |
| w27 | 46 | 0.043632 | 20.631 |
| w28 | 52 | -0.073918 | 10.178 |
| w29 | 35 | 0.039581 | 14.648 |
| w30 | 57 | -0.139569 | 0.715 |
| w31 | 44 | 0.10876 | 29.148 |
| w32 | 52 | -0.078146 | -0.045 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 41 | -0.120784 | -18.065 |
| w18 | 37 | 0.059655 | 26.933 |
| w19 | 40 | 0.008386 | -9.8 |
| w20 | 39 | -0.083838 | -21.678 |
| w21 | 37 | -0.141704 | -32.18 |
| w22 | 39 | 0.093476 | 44.133 |
| w23 | 39 | -0.07002 | -17.885 |
| w24 | 53 | -0.115285 | -2.982 |
| w25 | 39 | 0.111242 | 6.769 |
| w26 | 43 | -0.038567 | -9.498 |
| w27 | 48 | 0.089247 | 59.234 |
| w28 | 35 | -0.108601 | -9.23 |
| w29 | 39 | 0.081445 | 18.365 |
| w30 | 33 | -0.050043 | -15.137 |
| w31 | 38 | -0.114346 | -21.546 |
| w32 | 38 | 0.120639 | 35.824 |

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
| w17 | 52 | -0.102506 | -16.33 |
| w18 | 36 | -0.056528 | -22.141 |
| w19 | 37 | 0.043586 | -3.542 |
| w20 | 42 | -0.019877 | -6.211 |
| w21 | 41 | -0.121385 | -19.75 |
| w22 | 46 | 0.080561 | 48.605 |
| w23 | 42 | 0.041029 | -8.319 |
| w24 | 45 | -0.087293 | 11.02 |
| w25 | 48 | -0.03419 | -13.061 |
| w26 | 39 | 0.094489 | 29.873 |
| w27 | 50 | -0.044881 | 12.172 |
| w28 | 37 | -0.097279 | -12.463 |
| w29 | 46 | -0.127889 | 15.397 |
| w30 | 31 | -0.039071 | -13.371 |
| w31 | 34 | -0.052857 | -12.001 |
| w32 | 41 | 0.113412 | 33.064 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 36 | 0.032052 | 7.258 |
| w20 | 39 | -0.079374 | -17.525 |
| w21 | 41 | -0.095884 | -13.328 |
| w22 | 46 | 0.059804 | 122.915 |
| w23 | 41 | 0.048821 | 10.211 |
| w24 | 48 | 0.185867 | 203.406 |
| w25 | 42 | -0.068086 | -13.47 |
| w26 | 38 | 0.005555 | -1.135 |
| w27 | 48 | 0.018487 | -3.186 |
| w28 | 31 | -0.090559 | -24.191 |
| w29 | 46 | -0.044324 | -12.154 |
| w30 | 32 | 0.002507 | -9.61 |
| w31 | 40 | -0.087225 | -12.955 |
| w32 | 46 | -0.006045 | 14.0 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 41 | -0.025906 | 12.528 |
| w23 | 32 | -0.066301 | -17.719 |
| w24 | 40 | -0.100368 | 1.859 |
| w25 | 47 | -0.081015 | -19.656 |
| w26 | 33 | 0.038978 | 4.211 |
| w27 | 52 | -0.063082 | -7.916 |
| w28 | 36 | -0.042109 | -14.213 |
| w29 | 33 | 0.048454 | 22.935 |
| w30 | 33 | -0.071106 | -14.248 |
| w31 | 34 | -0.047648 | -7.048 |
| w32 | 34 | 0.18525 | 38.068 |

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
| w27 | 46 | 0.103752 | 42.105 |
| w28 | 37 | -0.241124 | -23.145 |
| w29 | 40 | 0.036706 | 8.948 |
| w30 | 25 | 0.022419 | -9.039 |
| w31 | 36 | -0.121138 | -21.834 |
| w32 | 41 | 0.041947 | 33.731 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 31 | 0.046237 | 7.112 |
| w18 | 31 | -0.046137 | -24.83 |
| w19 | 31 | 0.087162 | 5.791 |
| w20 | 22 | 0.076907 | 6.119 |
| w21 | 35 | -0.149103 | -28.99 |
| w22 | 38 | 0.002554 | 46.561 |
| w23 | 36 | -0.086461 | -18.75 |
| w24 | 51 | -0.145693 | -0.278 |
| w25 | 39 | 0.050595 | 4.659 |
| w26 | 42 | -0.00856 | -7.432 |
| w27 | 44 | -0.040646 | -4.05 |
| w28 | 39 | -0.108406 | -16.914 |
| w29 | 37 | -0.060968 | -15.201 |
| w30 | 32 | -0.0636 | -6.955 |
| w31 | 39 | -0.127386 | -24.758 |
| w32 | 23 | 0.06752 | 3.926 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 38 | 0.020773 | -3.005 |
| w18 | 40 | -0.047453 | -19.019 |
| w19 | 35 | -0.066974 | -17.085 |
| w20 | 33 | -0.026727 | -11.905 |
| w21 | 41 | -0.111085 | -26.064 |
| w22 | 43 | 0.082391 | 82.096 |
| w23 | 36 | -0.053551 | -15.349 |
| w24 | 49 | 0.027134 | 45.31 |
| w25 | 34 | 0.067594 | 30.128 |
| w26 | 30 | 0.0403 | -0.659 |
| w27 | 43 | 0.080927 | 14.824 |
| w28 | 31 | -0.067305 | -15.366 |
| w29 | 39 | -0.000171 | -0.712 |
| w30 | 19 | -0.084896 | -22.363 |
| w31 | 28 | -0.087523 | -19.725 |
| w32 | 26 | 0.189394 | 16.953 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 38 | -0.024168 | -8.834 |
| w29 | 37 | -0.022437 | -1.263 |
| w30 | 38 | -0.085302 | -4.484 |
| w31 | 28 | 0.146572 | 21.999 |
| w32 | 35 | 0.022474 | 10.604 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 37 | 0.071818 | 59.384 |
| w15 | 48 | 0.052175 | 44.035 |
| w16 | 35 | 0.004851 | 264.651 |
| w17 | 38 | 0.038909 | 7.531 |
| w18 | 40 | -0.074434 | -24.548 |
| w19 | 40 | -0.069234 | -13.178 |
| w20 | 38 | -0.022851 | -9.856 |
| w21 | 32 | 0.253426 | 107.431 |
| w22 | 48 | -0.101852 | 8.183 |
| w23 | 41 | -0.081276 | -12.563 |
| w24 | 46 | -0.036129 | 12.482 |
| w25 | 37 | 0.186186 | 81.687 |
| w26 | 38 | -0.073468 | -8.474 |
| w27 | 42 | 0.136302 | 93.403 |
| w28 | 29 | -0.082488 | -16.967 |
| w29 | 36 | 0.053792 | 18.729 |
| w30 | 32 | 0.093085 | 2.472 |
| w31 | 40 | -0.076826 | -9.668 |
| w32 | 30 | 0.113305 | 13.832 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 36 | 0.332326 | 202.494 |
| w26 | 36 | 0.010272 | 3.104 |
| w27 | 36 | 0.091066 | 46.749 |
| w28 | 32 | -0.093276 | -16.471 |
| w29 | 37 | 0.018941 | 5.655 |
| w30 | 37 | -0.003689 | -4.492 |
| w31 | 37 | -0.01603 | 4.657 |
| w32 | 39 | 0.14402 | 21.476 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

