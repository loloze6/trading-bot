# Backtest of 031-03.b1.b1.e2.e2_raw-scaled-rise-continuation_1d

- Plan: `../../../../../03_test_plan/night6_streak_run/plans/031-03.b1.b1.e2.e2_raw-scaled-rise-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.178423 | -8.166 |
| w2 | 3 | 0.052657 | 24.586 |
| w3 | 2 | -0.000706 | 11.026 |
| w4 | 2 | -0.012716 | -16.24 |
| w5 | 8 | -0.049109 | 21.584 |
| w6 | 8 | 0.130788 | 100.07 |
| w7 | 2 | -0.047725 | -1.11 |
| w8 | 1 | 0.059404 | 7.934 |
| w9 | 0 | None | 0.0 |
| w10 | 1 | 0.007752 | 4.424 |
| w11 | 5 | 0.064561 | 29.01 |
| w12 | 1 | 0.03345 | -1.261 |
| w13 | 0 | None | 0.0 |
| w14 | 3 | 0.044594 | 8.552 |
| w15 | 16 | -0.084176 | 43.098 |
| w16 | 7 | 0.053203 | 25.367 |
| w17 | 3 | -0.012797 | -10.934 |
| w18 | 1 | 0.046357 | 3.986 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 7 | 0.073594 | 39.93 |
| w23 | 1 | 0.033251 | 2.645 |
| w24 | 4 | 0.027744 | 19.183 |
| w25 | 2 | 0.074182 | 21.975 |
| w26 | 3 | -0.016653 | 1.138 |
| w27 | 3 | 0.149051 | 30.867 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | -0.077769 | 0.482 |
| w30 | 2 | -0.044305 | -16.916 |
| w31 | 0 | None | 0.0 |
| w32 | 1 | 0.096568 | 12.715 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.058008 | -5.403 |
| w2 | 4 | -0.028094 | -33.646 |
| w3 | 2 | -0.114192 | -1.123 |
| w4 | 1 | 0.054932 | 9.326 |
| w5 | 5 | 0.009189 | 7.291 |
| w6 | 5 | 0.101699 | 46.789 |
| w7 | 4 | -0.042677 | -4.047 |
| w8 | 0 | None | 0.0 |
| w9 | 1 | -0.076061 | -2.041 |
| w10 | 2 | -0.125785 | -9.66 |
| w11 | 1 | -0.114461 | -7.275 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | -0.080635 | 13.154 |
| w14 | 3 | 0.057103 | 8.212 |
| w15 | 4 | -0.136037 | -9.946 |
| w16 | 6 | -0.144615 | -5.63 |
| w17 | 6 | -0.065259 | -9.22 |
| w18 | 3 | -0.201687 | -33.89 |
| w19 | 1 | -0.079199 | -10.707 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | -0.232049 | -20.567 |
| w22 | 0 | None | 0.0 |
| w23 | 4 | -0.040214 | -11.111 |
| w24 | 0 | None | 0.0 |
| w25 | 4 | -0.053579 | 17.962 |
| w26 | 0 | None | 0.0 |
| w27 | 6 | -0.078451 | -13.105 |
| w28 | 0 | None | 0.0 |
| w29 | 8 | -0.06903 | -2.077 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 4 | -0.124915 | -14.834 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 4 | 0.171998 | 38.094 |
| w7 | 6 | 0.074732 | 16.104 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | 0.037579 | 4.866 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | -0.108049 | -4.729 |
| w12 | 0 | None | 0.0 |
| w13 | 1 | -0.072619 | -8.636 |
| w14 | 2 | 0.153411 | 28.221 |
| w15 | 4 | 0.256148 | 183.514 |
| w16 | 4 | 0.01189 | 16.326 |
| w17 | 5 | 0.012976 | 11.457 |
| w18 | 1 | -0.163017 | -13.891 |
| w19 | 2 | -0.08744 | -6.559 |
| w20 | 0 | None | 0.0 |
| w21 | 1 | -0.073138 | -6.972 |
| w22 | 5 | -0.105039 | -2.51 |
| w23 | 3 | -0.107775 | -3.463 |
| w24 | 3 | 0.019866 | 18.021 |
| w25 | 2 | -0.110499 | -4.425 |
| w26 | 1 | 0.126473 | 21.206 |
| w27 | 6 | 0.373968 | 235.124 |
| w28 | 1 | -0.015296 | -1.271 |
| w29 | 1 | 0.107835 | 23.299 |
| w30 | 0 | None | 0.0 |
| w31 | 2 | -0.127688 | -12.518 |
| w32 | 2 | 0.07672 | 9.974 |

- BCHUSD: 25 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w8 | 0 | None | 0.0 |
| w9 | 2 | -0.108323 | -18.921 |
| w10 | 1 | -0.050639 | -3.224 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | 0.009235 | 0.4 |
| w13 | 4 | -0.078051 | 24.442 |
| w14 | 3 | 0.028147 | 9.022 |
| w15 | 2 | -0.193706 | -18.653 |
| w16 | 7 | -0.157741 | 11.711 |
| w17 | 5 | -0.075251 | -6.153 |
| w18 | 2 | 0.061858 | -18.687 |
| w19 | 1 | -0.045042 | -0.048 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 5 | -0.065351 | -9.131 |
| w23 | 2 | 0.321726 | 84.37 |
| w24 | 0 | None | 0.0 |
| w25 | 3 | -0.138902 | -2.918 |
| w26 | 0 | None | 0.0 |
| w27 | 2 | -0.057012 | -5.087 |
| w28 | 1 | -0.115479 | -11.676 |
| w29 | 0 | None | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | -0.097709 | -12.903 |

- w7 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_BCHUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.070131 | 59.077 |
| w2 | 4 | -0.179195 | -28.564 |
| w3 | 0 | None | 0.0 |
| w4 | 9 | 0.046126 | 40.68 |
| w5 | 11 | 0.081401 | 56.384 |
| w6 | 6 | 0.022834 | 12.121 |
| w7 | 11 | -0.001349 | 54.931 |
| w8 | 0 | None | 0.0 |
| w9 | 1 | -0.067761 | 4.02 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | 0.087224 | 11.841 |
| w12 | 2 | -0.057788 | -30.643 |
| w13 | 2 | 0.015884 | 19.275 |
| w14 | 4 | 0.084873 | 41.732 |
| w15 | 4 | -0.119022 | -9.12 |
| w16 | 4 | 0.112965 | 35.539 |
| w17 | 6 | 0.02353 | 7.843 |
| w18 | 1 | -0.015117 | -17.867 |
| w19 | 2 | 0.069308 | -4.197 |
| w20 | 2 | 0.022377 | -5.382 |
| w21 | 2 | -0.041442 | -6.221 |
| w22 | 3 | 0.062866 | 20.293 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | -0.03955 | -7.819 |
| w25 | 4 | 0.10259 | 20.075 |
| w26 | 3 | 0.034072 | 0.419 |
| w27 | 1 | -0.036847 | -2.239 |
| w28 | 0 | None | 0.0 |
| w29 | 5 | 0.019249 | 37.36 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 1 | 0.054341 | 7.329 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 2 | -0.02535 | 13.817 |
| w11 | 2 | -0.102832 | -8.861 |
| w12 | 0 | None | 0.0 |
| w13 | 4 | 0.006301 | 5.426 |
| w14 | 3 | 0.052353 | 14.784 |
| w15 | 1 | 0.02733 | 5.251 |
| w16 | 4 | 0.143184 | 51.657 |
| w17 | 5 | 0.110689 | 5.682 |
| w18 | 0 | None | 0.0 |
| w19 | 1 | 0.045364 | 2.524 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 1 | -0.006588 | 3.914 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | 0.145787 | 105.454 |
| w25 | 2 | -0.056204 | -0.917 |
| w26 | 3 | -0.080276 | -5.281 |
| w27 | 6 | 0.219562 | 96.049 |
| w28 | 0 | None | 0.0 |
| w29 | 7 | 0.077965 | 13.155 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 4 | -0.055455 | -20.228 |

- ATOMUSD: 20 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 0 | None | 0.0 |
| w14 | 2 | 0.024323 | 47.238 |
| w15 | 0 | None | 0.0 |
| w16 | 6 | 0.106755 | 18.119 |
| w17 | 1 | -0.079759 | -13.329 |
| w18 | 5 | -0.028243 | 20.438 |
| w19 | 4 | 0.013789 | 1.431 |
| w20 | 0 | None | 0.0 |
| w21 | 1 | -0.018858 | -13.063 |
| w22 | 1 | 0.006141 | 2.498 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | 0.042295 | 25.047 |
| w25 | 4 | -0.064713 | 14.771 |
| w26 | 0 | None | 0.0 |
| w27 | 7 | -0.002858 | 28.961 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | None | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 6 | -0.047378 | -8.351 |
| w32 | 4 | -0.14068 | -13.105 |

- w12 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_ATOMUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 1 | -0.167876 | -9.15 |
| w16 | 6 | 0.144089 | 58.379 |
| w17 | 3 | 0.00888 | -6.026 |
| w18 | 2 | 0.01179 | 43.771 |
| w19 | 2 | -0.077944 | -1.319 |
| w20 | 0 | None | 0.0 |
| w21 | 6 | -0.218196 | -44.222 |
| w22 | 4 | -0.021456 | -2.495 |
| w23 | 4 | -0.124491 | -13.506 |
| w24 | 9 | -0.049275 | 43.858 |
| w25 | 3 | -0.092443 | 1.068 |
| w26 | 0 | None | 0.0 |
| w27 | 10 | 0.191584 | 116.327 |
| w28 | 0 | None | 0.0 |
| w29 | 3 | 0.007119 | 22.865 |
| w30 | 0 | None | 0.0 |
| w31 | 1 | -0.093207 | -9.045 |
| w32 | 2 | -0.130829 | -9.423 |

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
| w15 | 4 | -0.172379 | -15.291 |
| w16 | 4 | 0.088859 | 36.212 |
| w17 | 2 | 0.03909 | -4.284 |
| w18 | 2 | -0.024078 | -15.38 |
| w19 | 4 | -0.076913 | -19.685 |
| w20 | 2 | -0.390422 | -13.058 |
| w21 | 0 | None | 0.0 |
| w22 | 4 | -0.111649 | -8.924 |
| w23 | 3 | -0.031143 | -6.314 |
| w24 | 4 | -0.159902 | -11.707 |
| w25 | 1 | -0.007995 | 3.366 |
| w26 | 3 | 0.145234 | 22.314 |
| w27 | 8 | -0.114272 | -9.503 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | 0.034027 | 0.33 |
| w30 | 0 | None | 0.0 |
| w31 | 2 | -0.136956 | -12.673 |
| w32 | 3 | -0.010587 | -11.787 |

- DOTUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 7 | 0.015234 | 2.395 |
| w18 | 2 | -0.003917 | -10.46 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 3 | 0.009317 | 18.125 |
| w23 | 2 | -0.120019 | -1.026 |
| w24 | 9 | -0.106994 | 27.088 |
| w25 | 3 | 0.017356 | 13.946 |
| w26 | 0 | None | 0.0 |
| w27 | 6 | 0.070972 | 22.786 |
| w28 | 0 | None | 0.0 |
| w29 | 3 | -0.062282 | -2.088 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | -0.066233 | -9.421 |

- w16 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_DOTUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 0 | None | 0.0 |
| w21 | 2 | -0.061967 | 1.292 |
| w22 | 1 | 0.01531 | 5.932 |
| w23 | 0 | None | 0.0 |
| w24 | 15 | 0.105681 | 77.796 |
| w25 | 2 | -0.191593 | -1.338 |
| w26 | 3 | -0.08235 | -21.743 |
| w27 | 5 | 0.021934 | 25.532 |
| w28 | 0 | None | 0.0 |
| w29 | 6 | -0.027671 | 15.503 |
| w30 | 2 | 0.067725 | 5.787 |
| w31 | 0 | None | 0.0 |
| w32 | 4 | -0.149947 | -12.161 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 3 | 0.084274 | 24.167 |
| w23 | 2 | -0.00685 | 5.692 |
| w24 | 7 | -0.091415 | 39.377 |
| w25 | 3 | 0.018408 | 33.124 |
| w26 | 4 | 0.087913 | 1.357 |
| w27 | 3 | 7.3e-05 | -6.988 |
| w28 | 0 | None | 0.0 |
| w29 | 3 | -0.090963 | -4.435 |
| w30 | 1 | -0.155486 | -14.489 |
| w31 | 0 | None | 0.0 |
| w32 | 7 | 0.039756 | 1.992 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 7 | -0.169195 | -6.169 |
| w25 | 4 | -0.12772 | -11.128 |
| w26 | 5 | -0.132855 | -11.565 |
| w27 | 5 | -0.031632 | 17.217 |
| w28 | 1 | 0.027282 | 2.54 |
| w29 | 2 | -0.05178 | -4.826 |
| w30 | 0 | None | 0.0 |
| w31 | 2 | 0.00989 | -4.24 |
| w32 | 3 | -0.189723 | -28.803 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 1 | 0.033519 | 9.362 |
| w6 | 2 | -0.009032 | -4.665 |
| w7 | 3 | -0.033527 | 7.42 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 3 | -0.051779 | -0.269 |
| w11 | 4 | -0.047964 | -7.713 |
| w12 | 0 | None | 0.0 |
| w13 | 3 | 0.138689 | 48.368 |
| w14 | 2 | 0.014148 | 30.775 |
| w15 | 1 | -0.161368 | -10.44 |
| w16 | 5 | -0.063312 | 3.88 |
| w17 | 2 | 0.062965 | -1.849 |
| w18 | 2 | -0.140507 | -20.397 |
| w19 | 5 | 0.028274 | 7.656 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 4 | 0.00647 | 5.524 |
| w24 | 3 | -0.070856 | -15.88 |
| w25 | 3 | -0.077036 | 2.111 |
| w26 | 5 | -0.022255 | 5.556 |
| w27 | 7 | -0.103936 | 2.902 |
| w28 | 0 | None | 0.0 |
| w29 | 1 | -0.205026 | -0.701 |
| w30 | 5 | 0.259541 | 126.285 |
| w31 | 1 | 0.060666 | 5.578 |
| w32 | 2 | 0.007515 | 11.79 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 7 | -0.014521 | 5.642 |
| w6 | 10 | -0.038514 | 18.714 |
| w7 | 3 | -0.062499 | -2.764 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | -0.184278 | -19.659 |
| w10 | 3 | -0.120924 | -4.326 |
| w11 | 3 | -0.168605 | -19.97 |
| w12 | 0 | None | 0.0 |
| w13 | 7 | -0.098491 | -18.652 |
| w14 | 2 | 0.003351 | 27.978 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | -0.013444 | 7.379 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 1 | -0.073052 | -16.62 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 3 | 0.00448 | -13.36 |
| w23 | 1 | 0.163996 | 18.223 |
| w24 | 2 | -0.055285 | -4.308 |
| w25 | 0 | None | 0.0 |
| w26 | 4 | -0.049489 | -10.441 |
| w27 | 4 | -0.118722 | -14.576 |
| w28 | 1 | 0.15409 | 10.8 |
| w29 | 8 | 0.016061 | 18.884 |
| w30 | 2 | -0.187509 | -6.77 |
| w31 | 2 | -0.105444 | -14.815 |
| w32 | 1 | 0.147203 | 10.84 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 3 | 0.013279 | -13.829 |
| w18 | 4 | -0.137519 | -16.05 |
| w19 | 0 | None | 0.0 |
| w20 | 1 | -0.004507 | -7.9 |
| w21 | 0 | None | 0.0 |
| w22 | 1 | 0.094109 | 17.074 |
| w23 | 0 | None | 0.0 |
| w24 | 7 | -0.266097 | -19.642 |
| w25 | 5 | -0.1223 | 11.575 |
| w26 | 1 | -0.001436 | 2.609 |
| w27 | 8 | 0.11485 | 126.737 |
| w28 | 1 | -0.06722 | -3.985 |
| w29 | 2 | 0.231264 | 42.584 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 7 | -0.187392 | -32.123 |

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
| w17 | 4 | -0.088414 | -3.593 |
| w18 | 2 | 0.004885 | -1.255 |
| w19 | 4 | -0.048177 | -5.063 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 1 | 0.190239 | 43.627 |
| w23 | 2 | -0.25984 | 4.354 |
| w24 | 5 | -0.075801 | -8.154 |
| w25 | 6 | -0.050146 | 3.525 |
| w26 | 2 | -0.005726 | 0.755 |
| w27 | 5 | 0.023768 | 13.9 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | -0.087817 | -7.454 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 7 | -0.06622 | 0.702 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 1 | -0.150561 | -9.129 |
| w20 | 1 | -0.061887 | -4.894 |
| w21 | 0 | None | 0.0 |
| w22 | 7 | -0.046994 | 44.989 |
| w23 | 0 | None | 0.0 |
| w24 | 12 | 0.226385 | 172.437 |
| w25 | 0 | None | 0.0 |
| w26 | 3 | -0.041614 | -4.398 |
| w27 | 1 | -0.003172 | 0.125 |
| w28 | 0 | None | 0.0 |
| w29 | 3 | -0.133428 | -6.146 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 5 | -0.045181 | -15.471 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 1 | 0.129814 | 20.156 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | -0.109082 | -14.294 |
| w25 | 3 | -0.188081 | -5.344 |
| w26 | 2 | 0.053578 | -1.291 |
| w27 | 2 | 0.036387 | -9.143 |
| w28 | 0 | None | 0.0 |
| w29 | 3 | -0.072879 | -13.118 |
| w30 | 0 | None | 0.0 |
| w31 | 1 | -0.044322 | -11.332 |
| w32 | 9 | 0.067397 | 9.599 |

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
| w27 | 5 | -0.015001 | -3.629 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | -0.127768 | 2.841 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | 0.123552 | 33.904 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 2 | -0.077556 | -1.122 |
| w18 | 1 | -0.277961 | -19.113 |
| w19 | 2 | 0.029149 | -10.727 |
| w20 | 4 | 0.08363 | 0.198 |
| w21 | 0 | None | 0.0 |
| w22 | 6 | -0.076927 | 9.065 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | -0.036655 | 25.927 |
| w25 | 3 | -0.044002 | -29.587 |
| w26 | 0 | None | 0.0 |
| w27 | 8 | 0.000437 | 16.074 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | None | 0.0 |
| w30 | 1 | -0.148362 | -11.349 |
| w31 | 0 | None | 0.0 |
| w32 | 1 | -0.170334 | -16.329 |

- GRTUSD: 15 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 6 | 0.044399 | 20.525 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | 0.065581 | 31.113 |
| w25 | 3 | 0.014651 | 8.768 |
| w26 | 0 | None | 0.0 |
| w27 | 9 | -0.064714 | -16.155 |
| w28 | 1 | -0.092838 | -6.045 |
| w29 | 1 | -0.161819 | -8.859 |
| w30 | 0 | None | 0.0 |
| w31 | 2 | 0.012544 | -2.17 |
| w32 | 3 | -0.002095 | -14.746 |

- w17 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_GRTUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 2 | 0.0437 | 1.383 |
| w29 | 1 | -0.017827 | -4.192 |
| w30 | 2 | -0.167093 | -11.453 |
| w31 | 4 | -0.016875 | 5.244 |
| w32 | 3 | -0.102133 | -15.981 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 2 | 0.079139 | 10.764 |
| w15 | 5 | -0.198374 | -11.665 |
| w16 | 8 | -0.014367 | 111.037 |
| w17 | 3 | -0.085324 | -9.342 |
| w18 | 0 | None | 0.0 |
| w19 | 3 | -0.25628 | -16.37 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | 0.205559 | 69.61 |
| w22 | 1 | -0.0247 | -13.6 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | -0.057128 | -0.534 |
| w25 | 4 | 0.146683 | 39.858 |
| w26 | 2 | -0.106395 | -4.436 |
| w27 | 5 | 0.177533 | 85.139 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | -0.056906 | 10.155 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 4 | 0.073405 | 5.815 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 6 | 0.346006 | 157.64 |
| w26 | 4 | -0.035518 | 1.163 |
| w27 | 4 | 0.116415 | 17.092 |
| w28 | 0 | None | 0.0 |
| w29 | 3 | -0.013075 | 4.617 |
| w30 | 0 | None | 0.0 |
| w31 | 1 | -0.0066 | -2.317 |
| w32 | 1 | -0.089533 | -8.632 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

