# Backtest of 045-01_rising-market-late-week-gain_1d

- Plan: `../../../../../03_test_plan/night7_panic_run/plans/045-01_rising-market-late-week-gain_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.136058 | -9.7 |
| w2 | 14 | 0.222956 | 69.85 |
| w3 | 14 | 0.045119 | 23.113 |
| w4 | 20 | -0.23864 | -25.897 |
| w5 | 21 | -0.121626 | -5.628 |
| w6 | 20 | -0.035542 | 14.573 |
| w7 | 4 | 0.161507 | 5.654 |
| w8 | 3 | -0.009766 | -0.646 |
| w9 | 0 | None | 0.0 |
| w10 | 7 | 0.031726 | 9.15 |
| w11 | 17 | 0.143358 | 42.874 |
| w12 | 0 | None | 0.0 |
| w13 | 9 | -0.050762 | -7.458 |
| w14 | 19 | -0.081851 | -2.115 |
| w15 | 14 | 0.01933 | 18.819 |
| w16 | 20 | 0.057334 | 15.726 |
| w17 | 9 | 0.132314 | 11.688 |
| w18 | 20 | -0.039143 | -5.687 |
| w19 | 2 | 0.035017 | 1.27 |
| w20 | 1 | -0.233728 | -3.083 |
| w21 | 0 | None | 0.0 |
| w22 | 21 | 0.036651 | 29.064 |
| w23 | 9 | -0.085759 | -8.919 |
| w24 | 13 | -0.006775 | 10.852 |
| w25 | 17 | -0.179413 | -19.939 |
| w26 | 0 | None | 0.0 |
| w27 | 11 | 0.002308 | 11.274 |
| w28 | 4 | 0.071905 | 2.252 |
| w29 | 17 | -0.053785 | -4.297 |
| w30 | 0 | None | 0.0 |
| w31 | 4 | -0.032929 | -1.59 |
| w32 | 9 | -0.036484 | -3.847 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.060452 | -4.152 |
| w2 | 10 | 0.206888 | 43.556 |
| w3 | 2 | -0.114449 | -5.333 |
| w4 | 7 | 0.051026 | 0.599 |
| w5 | 19 | -0.083606 | 0.029 |
| w6 | 17 | 0.103953 | 62.369 |
| w7 | 4 | 0.180211 | 10.697 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 16 | 0.179707 | 39.117 |
| w11 | 15 | 0.238083 | 20.048 |
| w12 | 0 | None | 0.0 |
| w13 | 9 | 0.014073 | 4.065 |
| w14 | 12 | 0.072097 | 13.153 |
| w15 | 15 | 0.13437 | 29.746 |
| w16 | 22 | 0.142893 | 22.316 |
| w17 | 6 | -0.029818 | -3.611 |
| w18 | 15 | -0.088958 | -12.314 |
| w19 | 2 | 0.010033 | -0.184 |
| w20 | 3 | 0.007953 | -0.747 |
| w21 | 13 | -0.043629 | -1.942 |
| w22 | 12 | 0.000785 | 0.502 |
| w23 | 5 | -0.044831 | -4.539 |
| w24 | 8 | -0.054538 | -4.078 |
| w25 | 11 | 0.021665 | 7.781 |
| w26 | 0 | None | 0.0 |
| w27 | 11 | 0.18373 | 54.647 |
| w28 | 8 | 0.035927 | 1.068 |
| w29 | 10 | 0.035832 | 6.235 |
| w30 | 2 | 0.049275 | 1.689 |
| w31 | 1 | -0.019916 | -0.472 |
| w32 | 3 | -0.07006 | -3.819 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 15 | 0.00245 | 10.913 |
| w7 | 6 | 0.051406 | 6.465 |
| w8 | 2 | 0.032832 | 0.399 |
| w9 | 11 | 0.029238 | 3.397 |
| w10 | 3 | 0.06118 | 3.202 |
| w11 | 10 | 0.044612 | 3.208 |
| w12 | 3 | -0.075152 | -2.43 |
| w13 | 6 | -0.059623 | -6.695 |
| w14 | 12 | 0.149702 | 27.774 |
| w15 | 9 | 0.142 | 73.438 |
| w16 | 15 | 0.011042 | 15.206 |
| w17 | 11 | -0.009157 | 1.334 |
| w18 | 11 | -0.021992 | -4.383 |
| w19 | 3 | -0.010012 | -1.835 |
| w20 | 3 | -0.128633 | -3.762 |
| w21 | 11 | 0.069994 | 11.628 |
| w22 | 12 | -0.102254 | -9.811 |
| w23 | 9 | -0.117459 | -9.025 |
| w24 | 13 | -0.023289 | -0.204 |
| w25 | 7 | -0.186483 | -15.062 |
| w26 | 9 | -0.080227 | -7.684 |
| w27 | 9 | 0.359947 | 119.099 |
| w28 | 4 | 0.071926 | 4.159 |
| w29 | 11 | -0.074705 | -9.161 |
| w30 | 1 | 0.02093 | 0.144 |
| w31 | 0 | None | 0.0 |
| w32 | 4 | 0.029668 | 2.395 |

- BCHUSD: 25 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w8 | 7 | 0.046838 | 0.074 |
| w9 | 1 | -0.021321 | -1.081 |
| w10 | 11 | 0.016664 | 4.759 |
| w11 | 12 | 0.191253 | 12.458 |
| w12 | 0 | None | 0.0 |
| w13 | 9 | -0.079333 | -11.558 |
| w14 | 10 | 0.052772 | 6.525 |
| w15 | 10 | 0.093821 | 14.032 |
| w16 | 23 | 0.15453 | 33.925 |
| w17 | 10 | -0.118967 | -9.33 |
| w18 | 8 | -0.112666 | -12.693 |
| w19 | 3 | -0.051141 | -3.305 |
| w20 | 2 | -0.137496 | -2.036 |
| w21 | 3 | 0.074666 | 1.644 |
| w22 | 11 | 0.031977 | 5.132 |
| w23 | 10 | 0.150569 | 32.631 |
| w24 | 10 | 0.006563 | -1.219 |
| w25 | 15 | 0.127187 | 54.91 |
| w26 | 0 | 0.107552 | 0.0 |
| w27 | 12 | 0.152845 | 24.523 |
| w28 | 2 | -0.028177 | -1.527 |
| w29 | 26 | -0.118256 | -12.679 |
| w30 | 4 | 0.056018 | 2.976 |
| w31 | 6 | 0.140687 | 8.246 |
| w32 | 4 | -0.023099 | 2.367 |

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
| w1 | 16 | 0.015009 | 26.242 |
| w2 | 9 | -0.290686 | -30.212 |
| w3 | 7 | 0.033252 | -1.436 |
| w4 | 17 | -0.099908 | 17.167 |
| w5 | 15 | -0.02432 | 8.184 |
| w6 | 19 | 0.047613 | 26.163 |
| w7 | 7 | 0.128719 | 22.012 |
| w8 | 4 | 0.046412 | 0.826 |
| w9 | 0 | None | 0.0 |
| w10 | 14 | 0.095349 | 11.783 |
| w11 | 14 | 0.113133 | 17.013 |
| w12 | 0 | None | 0.0 |
| w13 | 8 | -0.012939 | 3.191 |
| w14 | 19 | 0.107619 | 33.809 |
| w15 | 14 | 0.069503 | 19.793 |
| w16 | 21 | -0.001926 | 13.821 |
| w17 | 13 | -0.005175 | 6.587 |
| w18 | 20 | -0.121871 | -15.744 |
| w19 | 4 | 0.030786 | 0.275 |
| w20 | 6 | -0.162466 | -12.553 |
| w21 | 4 | 0.086143 | 3.721 |
| w22 | 19 | 0.004545 | 9.836 |
| w23 | 4 | -0.087647 | -6.017 |
| w24 | 12 | -0.054639 | -1.308 |
| w25 | 17 | -0.176514 | -21.08 |
| w26 | 4 | 0.04469 | 1.82 |
| w27 | 8 | 0.12683 | 26.214 |
| w28 | 2 | 0.098909 | 3.506 |
| w29 | 21 | -0.10319 | 1.021 |
| w30 | 4 | 0.046263 | 1.051 |
| w31 | 4 | 0.002667 | -0.268 |
| w32 | 5 | 0.042121 | 3.905 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 15 | 0.146541 | 31.642 |
| w11 | 10 | 0.063621 | 3.416 |
| w12 | 0 | None | 0.0 |
| w13 | 8 | -0.074652 | -11.057 |
| w14 | 18 | 0.07215 | 24.689 |
| w15 | 12 | 0.16346 | 26.279 |
| w16 | 17 | 0.231215 | 62.251 |
| w17 | 13 | -0.006246 | 10.136 |
| w18 | 6 | 0.028944 | -1.527 |
| w19 | 1 | 0.026812 | 0.198 |
| w20 | 1 | 0.059295 | 1.079 |
| w21 | 1 | 0.055861 | 1.483 |
| w22 | 12 | -0.044629 | -1.586 |
| w23 | 2 | -0.02341 | -2.998 |
| w24 | 11 | 0.111705 | 50.273 |
| w25 | 16 | -0.10776 | -15.336 |
| w26 | 0 | None | 0.0 |
| w27 | 9 | 0.342632 | 96.117 |
| w28 | 4 | 0.092207 | 4.97 |
| w29 | 8 | 0.025892 | 2.856 |
| w30 | 3 | 0.053855 | 0.633 |
| w31 | 0 | None | 0.0 |
| w32 | 5 | 0.027462 | 1.314 |

- ATOMUSD: 20 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 10 | -0.087833 | -9.275 |
| w14 | 20 | 0.036007 | 19.648 |
| w15 | 8 | 0.139094 | 9.054 |
| w16 | 19 | 0.178533 | 53.767 |
| w17 | 6 | 0.21777 | 31.061 |
| w18 | 11 | 0.018802 | 3.9 |
| w19 | 8 | -0.083979 | -6.585 |
| w20 | 7 | -0.116571 | -14.337 |
| w21 | 11 | 0.155917 | 12.505 |
| w22 | 13 | 0.05915 | 9.364 |
| w23 | 0 | None | 0.0 |
| w24 | 13 | 0.071853 | 15.388 |
| w25 | 9 | -0.188339 | -24.948 |
| w26 | 0 | None | 0.0 |
| w27 | 10 | 0.309583 | 63.287 |
| w28 | 4 | 0.139518 | 3.504 |
| w29 | 5 | 0.191823 | 15.493 |
| w30 | 0 | None | 0.0 |
| w31 | 2 | 0.01605 | 0.287 |
| w32 | 6 | -0.043625 | -6.169 |

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
| w15 | 4 | -0.018269 | -0.702 |
| w16 | 17 | 0.263483 | 73.727 |
| w17 | 6 | 0.044935 | 3.31 |
| w18 | 12 | -0.080542 | -6.5 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.031325 | 0.34 |
| w21 | 4 | 0.13107 | 14.734 |
| w22 | 8 | -0.075711 | -7.549 |
| w23 | 0 | None | 0.0 |
| w24 | 12 | 0.150904 | 42.759 |
| w25 | 12 | -0.218244 | -30.198 |
| w26 | 0 | None | 0.0 |
| w27 | 9 | 0.407433 | 118.55 |
| w28 | 4 | 0.083679 | 2.078 |
| w29 | 18 | -0.041144 | -6.852 |
| w30 | 1 | 0.015749 | -0.098 |
| w31 | 6 | 0.00664 | -0.855 |
| w32 | 8 | 0.070677 | 2.709 |

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
| w15 | 11 | -0.202007 | -19.179 |
| w16 | 20 | 0.062208 | 39.18 |
| w17 | 8 | -0.024383 | 0.035 |
| w18 | 12 | -0.073857 | -8.797 |
| w19 | 3 | -0.047157 | -3.406 |
| w20 | 11 | 0.023318 | -0.588 |
| w21 | 0 | None | 0.0 |
| w22 | 12 | 0.074392 | 16.728 |
| w23 | 10 | 0.067059 | 6.213 |
| w24 | 16 | 0.121687 | 27.005 |
| w25 | 10 | 0.003841 | -1.181 |
| w26 | 8 | -0.007993 | -0.184 |
| w27 | 18 | -0.008155 | 28.378 |
| w28 | 5 | 0.032386 | 0.199 |
| w29 | 21 | -0.125361 | -10.763 |
| w30 | 3 | -0.167832 | -6.214 |
| w31 | 6 | -0.06743 | -7.009 |
| w32 | 4 | 0.035765 | 0.559 |

- DOTUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 4 | 0.018057 | 2.577 |
| w18 | 18 | 0.003551 | -2.261 |
| w19 | 3 | 0.094143 | 1.663 |
| w20 | 2 | 0.012261 | -0.009 |
| w21 | 1 | 0.016439 | 0.018 |
| w22 | 14 | -0.039651 | -2.968 |
| w23 | 1 | 0.027727 | 0.333 |
| w24 | 12 | 0.056529 | 20.138 |
| w25 | 14 | -0.218325 | -30.551 |
| w26 | 0 | None | 0.0 |
| w27 | 8 | 0.271409 | 53.837 |
| w28 | 4 | 0.116881 | 2.28 |
| w29 | 5 | 0.219085 | 14.636 |
| w30 | 3 | -0.004819 | -2.716 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

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
| w20 | 5 | -0.033331 | -4.159 |
| w21 | 2 | -0.013811 | -0.462 |
| w22 | 14 | 0.012957 | 6.061 |
| w23 | 0 | None | 0.0 |
| w24 | 10 | 0.237286 | 78.008 |
| w25 | 13 | -0.076336 | -8.737 |
| w26 | 0 | None | 0.0 |
| w27 | 18 | 0.142598 | 42.36 |
| w28 | 4 | 0.105026 | 3.403 |
| w29 | 11 | 0.129728 | 16.849 |
| w30 | 8 | -0.070634 | -9.895 |
| w31 | 1 | -0.001262 | -0.161 |
| w32 | 3 | -0.013065 | -1.019 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 12 | -0.029903 | -0.206 |
| w23 | 1 | 0.026092 | 0.161 |
| w24 | 12 | 0.098423 | 36.064 |
| w25 | 17 | -0.174904 | -17.109 |
| w26 | 2 | 0.093562 | 0.756 |
| w27 | 15 | 0.087393 | 14.191 |
| w28 | 2 | 0.084296 | 3.617 |
| w29 | 7 | 0.074695 | 7.05 |
| w30 | 3 | 0.008271 | -0.102 |
| w31 | 5 | -0.0289 | -3.455 |
| w32 | 15 | 0.016039 | 12.734 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 13 | 0.0641 | 12.596 |
| w25 | 19 | -0.007515 | 1.244 |
| w26 | 1 | 0.005979 | 0.03 |
| w27 | 20 | 0.093654 | 39.036 |
| w28 | 7 | 0.164461 | 6.687 |
| w29 | 19 | -0.01501 | -1.927 |
| w30 | 2 | 0.02566 | 0.309 |
| w31 | 1 | 0.001769 | -0.031 |
| w32 | 5 | -0.211941 | -10.685 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 14 | -0.111226 | -5.378 |
| w6 | 15 | -0.168196 | -20.765 |
| w7 | 7 | 0.230434 | 17.286 |
| w8 | 6 | 0.016367 | 0.02 |
| w9 | 1 | -0.045298 | -1.556 |
| w10 | 7 | 0.0339 | 2.73 |
| w11 | 14 | 0.146048 | 18.135 |
| w12 | 0 | None | 0.0 |
| w13 | 8 | -0.085839 | -10.239 |
| w14 | 24 | 0.094844 | 24.805 |
| w15 | 5 | 0.113097 | 8.46 |
| w16 | 22 | 0.097052 | 30.641 |
| w17 | 7 | -0.025183 | -2.55 |
| w18 | 13 | -0.129948 | -13.831 |
| w19 | 9 | -0.01351 | -2.114 |
| w20 | 2 | -0.081729 | -1.398 |
| w21 | 1 | 0.028805 | 0.306 |
| w22 | 6 | -0.152046 | -10.381 |
| w23 | 1 | -0.00566 | -0.721 |
| w24 | 13 | 0.012093 | 1.981 |
| w25 | 8 | -0.189969 | -19.366 |
| w26 | 10 | 0.072356 | 11.78 |
| w27 | 14 | 0.084511 | 25.553 |
| w28 | 4 | -0.020543 | -1.276 |
| w29 | 15 | -0.09712 | -11.929 |
| w30 | 14 | 0.139282 | 51.518 |
| w31 | 5 | 0.028845 | 1.181 |
| w32 | 14 | 0.036668 | 23.448 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 18 | -0.005458 | 13.579 |
| w6 | 17 | -0.082205 | -1.973 |
| w7 | 5 | 0.08704 | 7.795 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | 0.016093 | -0.342 |
| w10 | 11 | 0.055705 | 9.347 |
| w11 | 16 | 0.169132 | 24.299 |
| w12 | 0 | None | 0.0 |
| w13 | 9 | -0.058038 | -8.441 |
| w14 | 18 | -0.001513 | 4.841 |
| w15 | 22 | -0.055631 | -2.246 |
| w16 | 21 | 0.08728 | 29.741 |
| w17 | 7 | 0.031166 | 6.602 |
| w18 | 6 | -0.016006 | -2.24 |
| w19 | 9 | -0.018655 | -3.155 |
| w20 | 6 | -0.123436 | -11.06 |
| w21 | 4 | 0.023928 | 0.642 |
| w22 | 6 | 0.216348 | 33.255 |
| w23 | 4 | -0.018865 | -2.656 |
| w24 | 11 | 0.022805 | 3.06 |
| w25 | 1 | -0.137688 | -3.324 |
| w26 | 11 | 0.013319 | 1.721 |
| w27 | 6 | 0.014721 | -0.79 |
| w28 | 11 | -0.030564 | -0.299 |
| w29 | 12 | 0.109465 | 16.935 |
| w30 | 15 | 0.073621 | 11.664 |
| w31 | 8 | -0.135418 | -10.389 |
| w32 | 9 | -0.100251 | -4.224 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 7 | 0.000673 | -0.409 |
| w18 | 26 | -0.183207 | -19.231 |
| w19 | 3 | 0.013671 | -0.192 |
| w20 | 9 | -0.094307 | -9.467 |
| w21 | 4 | 0.010131 | -0.303 |
| w22 | 14 | 0.057465 | 9.943 |
| w23 | 0 | None | 0.0 |
| w24 | 12 | 0.046807 | 9.105 |
| w25 | 8 | -0.194715 | -23.223 |
| w26 | 0 | None | 0.0 |
| w27 | 12 | 0.189464 | 55.989 |
| w28 | 8 | 0.051937 | 2.003 |
| w29 | 20 | -0.035483 | -5.595 |
| w30 | 2 | 0.029011 | 0.183 |
| w31 | 0 | None | 0.0 |
| w32 | 5 | -0.024258 | -2.053 |

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
| w17 | 11 | -0.059062 | -5.201 |
| w18 | 3 | -0.06974 | -3.995 |
| w19 | 6 | 0.051765 | 2.237 |
| w20 | 7 | -0.127861 | -12.9 |
| w21 | 4 | 0.057459 | 1.658 |
| w22 | 13 | -0.003208 | 2.815 |
| w23 | 5 | -0.031009 | -2.707 |
| w24 | 14 | -0.08978 | -3.011 |
| w25 | 10 | -0.209922 | -29.164 |
| w26 | 8 | 0.049385 | 6.752 |
| w27 | 19 | 0.021987 | 15.735 |
| w28 | 5 | 0.060126 | 1.444 |
| w29 | 16 | -0.018948 | 2.67 |
| w30 | 1 | 0.021242 | 0.196 |
| w31 | 0 | None | 0.0 |
| w32 | 9 | 0.12666 | 17.301 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 5 | 0.037896 | 0.693 |
| w20 | 6 | -0.14357 | -7.544 |
| w21 | 12 | 0.090893 | 7.885 |
| w22 | 16 | -0.065167 | 5.368 |
| w23 | 15 | 0.087097 | 6.022 |
| w24 | 12 | 0.054265 | 41.213 |
| w25 | 8 | 0.054395 | 0.137 |
| w26 | 2 | -0.009453 | -0.46 |
| w27 | 15 | 0.137814 | 21.47 |
| w28 | 2 | 0.097646 | 2.959 |
| w29 | 16 | -0.055236 | -7.436 |
| w30 | 3 | 0.068982 | 1.865 |
| w31 | 1 | None | -0.087 |
| w32 | 15 | 0.023192 | 6.611 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 12 | 0.029975 | 11.144 |
| w23 | 2 | 0.039608 | 1.046 |
| w24 | 15 | -0.066702 | -3.204 |
| w25 | 14 | -0.044845 | -5.54 |
| w26 | 3 | -0.104041 | -2.772 |
| w27 | 11 | 0.070974 | 11.544 |
| w28 | 6 | 0.063551 | 1.946 |
| w29 | 12 | 0.191805 | 31.321 |
| w30 | 5 | -0.033211 | -3.104 |
| w31 | 3 | -0.116915 | -5.365 |
| w32 | 13 | -0.029441 | -3.799 |

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
| w27 | 12 | 0.126378 | 27.769 |
| w28 | 6 | 0.125002 | 5.526 |
| w29 | 11 | 0.062163 | 6.01 |
| w30 | 2 | 0.032479 | 0.075 |
| w31 | 0 | None | 0.0 |
| w32 | 19 | -0.102787 | -8.187 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 5 | 0.049014 | 3.397 |
| w18 | 9 | 0.001126 | -0.233 |
| w19 | 1 | 0.002818 | -0.533 |
| w20 | 5 | -0.056962 | -3.461 |
| w21 | 1 | 0.002769 | -0.14 |
| w22 | 15 | 0.001826 | 8.124 |
| w23 | 2 | 0.006149 | -0.476 |
| w24 | 15 | 0.07071 | 17.262 |
| w25 | 16 | -0.125547 | -18.954 |
| w26 | 0 | None | 0.0 |
| w27 | 9 | 0.301441 | 63.03 |
| w28 | 4 | 0.08499 | 1.931 |
| w29 | 2 | 0.140951 | 6.093 |
| w30 | 1 | -0.119434 | -3.718 |
| w31 | 0 | None | 0.0 |
| w32 | 6 | -0.030595 | -3.307 |

- GRTUSD: 15 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w18 | 11 | -0.000866 | -2.691 |
| w19 | 1 | 0.128328 | 1.627 |
| w20 | 3 | -0.019167 | -1.153 |
| w21 | 3 | 0.046333 | 0.655 |
| w22 | 17 | 0.01995 | 18.536 |
| w23 | 0 | None | 0.0 |
| w24 | 14 | 0.047497 | 13.986 |
| w25 | 14 | 0.019373 | 6.083 |
| w26 | 0 | None | 0.0 |
| w27 | 14 | 0.169364 | 30.65 |
| w28 | 4 | 0.140423 | 4.604 |
| w29 | 9 | 0.04497 | 2.979 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | -0.070249 | -3.383 |

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
| w28 | 2 | 0.064738 | 2.026 |
| w29 | 12 | 0.062278 | 5.513 |
| w30 | 4 | 0.18717 | 12.855 |
| w31 | 8 | -0.142283 | -14.293 |
| w32 | 4 | 0.019851 | -2.058 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 21 | -0.036534 | -3.448 |
| w15 | 10 | 0.097361 | 25.596 |
| w16 | 18 | -0.019547 | 57.709 |
| w17 | 10 | -0.041322 | -3.545 |
| w18 | 6 | -0.02279 | -1.82 |
| w19 | 1 | -0.034105 | -0.63 |
| w20 | 4 | -0.038618 | -2.117 |
| w21 | 12 | 0.231049 | 61.143 |
| w22 | 4 | -0.087154 | -4.591 |
| w23 | 2 | 0.058549 | 2.598 |
| w24 | 11 | 0.051869 | 9.434 |
| w25 | 11 | -0.05222 | 2.666 |
| w26 | 0 | None | 0.0 |
| w27 | 13 | 0.084664 | 34.097 |
| w28 | 1 | 0.205081 | 2.854 |
| w29 | 16 | 0.095378 | 15.78 |
| w30 | 6 | 0.124754 | 6.254 |
| w31 | 1 | None | -0.053 |
| w32 | 8 | -0.080487 | -7.867 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 11 | 0.00238 | 15.017 |
| w26 | 9 | -0.077447 | -3.48 |
| w27 | 15 | 0.043351 | 12.281 |
| w28 | 3 | 0.057768 | 1.389 |
| w29 | 13 | -0.030841 | -2.925 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | -0.075543 | -1.908 |
| w32 | 7 | -0.005416 | -1.16 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

