# Backtest of 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d2_momentum-inside-90-day-rises_1d

- Plan: `../../../../../03_test_plan/night3_learned_run/plans/022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d2_momentum-inside-90-day-rises_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 37 | -0.027521 | 0.523 |
| w2 | 39 | 0.063287 | 36.391 |
| w3 | 34 | 0.029802 | 69.884 |
| w4 | 56 | -0.167999 | -34.832 |
| w5 | 36 | 0.034787 | 109.432 |
| w6 | 48 | -0.000479 | 80.637 |
| w7 | 25 | 0.075109 | -2.666 |
| w8 | 7 | -0.031587 | -4.614 |
| w9 | 13 | -0.050018 | -5.745 |
| w10 | 25 | 0.051003 | 36.583 |
| w11 | 51 | -0.033015 | 22.836 |
| w12 | 10 | -0.078015 | -3.086 |
| w13 | 22 | 0.074326 | 19.814 |
| w14 | 32 | 0.029951 | 9.618 |
| w15 | 33 | 0.129252 | 137.404 |
| w16 | 40 | -0.073681 | 11.442 |
| w17 | 14 | 0.054646 | 12.796 |
| w18 | 41 | 0.049114 | 13.063 |
| w19 | 16 | -0.093904 | -9.377 |
| w20 | 2 | -0.047323 | 10.005 |
| w21 | 4 | 0.22144 | 5.495 |
| w22 | 27 | -0.062784 | 35.788 |
| w23 | 45 | 0.013636 | -2.196 |
| w24 | 23 | 0.054288 | 49.482 |
| w25 | 31 | 0.103486 | 39.289 |
| w26 | 36 | -0.108806 | -20.879 |
| w27 | 35 | 0.038353 | 67.668 |
| w28 | 22 | -0.018316 | 4.367 |
| w29 | 54 | -0.00242 | 4.409 |
| w30 | 14 | -0.049847 | -10.836 |
| w31 | 0 | None | 0.0 |
| w32 | 23 | 0.055159 | 24.974 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | -0.023523 | 17.429 |
| w2 | 32 | 0.025507 | 12.195 |
| w3 | 27 | -0.112646 | -27.73 |
| w4 | 28 | -0.009325 | -0.509 |
| w5 | 45 | -0.04841 | 25.787 |
| w6 | 41 | 0.024848 | 56.266 |
| w7 | 21 | -0.051931 | -6.073 |
| w8 | 5 | 0.011888 | -2.376 |
| w9 | 0 | None | 0.0 |
| w10 | 26 | -0.013431 | 24.455 |
| w11 | 40 | 0.073542 | 15.127 |
| w12 | 0 | None | 0.0 |
| w13 | 22 | 0.087443 | 19.417 |
| w14 | 24 | 0.0127 | 5.137 |
| w15 | 42 | 0.014812 | 18.154 |
| w16 | 50 | -0.111308 | 5.112 |
| w17 | 19 | 0.018233 | 6.021 |
| w18 | 48 | 0.020512 | -8.817 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 36 | -0.031954 | -9.153 |
| w22 | 60 | -0.048395 | -8.028 |
| w23 | 26 | -0.099517 | -22.544 |
| w24 | 26 | -0.250774 | -19.487 |
| w25 | 42 | 0.030136 | 22.82 |
| w26 | 12 | -0.043101 | -1.066 |
| w27 | 33 | 0.020518 | 29.154 |
| w28 | 26 | -0.159213 | -12.627 |
| w29 | 29 | 0.055488 | 24.498 |
| w30 | 21 | -0.121572 | -19.793 |
| w31 | 0 | None | 0.0 |
| w32 | 14 | 0.001651 | 3.876 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 34 | 0.198655 | 129.974 |
| w7 | 12 | -0.051235 | -5.915 |
| w8 | 2 | -0.09697 | -8.562 |
| w9 | 24 | -0.091866 | -20.866 |
| w10 | 15 | -0.2381 | -26.175 |
| w11 | 36 | 0.035232 | -2.608 |
| w12 | 6 | -0.085033 | -5.791 |
| w13 | 14 | -0.042074 | -1.739 |
| w14 | 32 | 0.14095 | 58.785 |
| w15 | 28 | 0.175339 | 116.934 |
| w16 | 27 | 0.042758 | 61.73 |
| w17 | 25 | -0.065723 | -3.905 |
| w18 | 30 | -0.144031 | -13.585 |
| w19 | 12 | 0.053933 | 10.634 |
| w20 | 2 | -0.055117 | 5.379 |
| w21 | 38 | 0.075028 | 4.305 |
| w22 | 17 | -0.091271 | -7.646 |
| w23 | 32 | -0.060339 | -16.024 |
| w24 | 35 | -0.187523 | -24.727 |
| w25 | 28 | -0.110373 | -6.533 |
| w26 | 17 | -0.056131 | -9.857 |
| w27 | 36 | 0.292101 | 187.621 |
| w28 | 21 | -0.057472 | -4.532 |
| w29 | 33 | 0.054051 | 25.668 |
| w30 | 20 | 0.103265 | 3.874 |
| w31 | 0 | None | 0.0 |
| w32 | 7 | -0.082256 | -5.759 |

- BCHUSD: 25 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w8 | 10 | 0.003108 | -2.324 |
| w9 | 2 | -0.075219 | -11.445 |
| w10 | 15 | 0.135097 | 61.822 |
| w11 | 30 | -0.007001 | -2.07 |
| w12 | 0 | None | 0.0 |
| w13 | 26 | 0.138371 | 62.942 |
| w14 | 25 | 0.016199 | -6.934 |
| w15 | 35 | -0.044076 | -2.5 |
| w16 | 44 | -0.0025 | 51.432 |
| w17 | 15 | 0.048948 | 13.171 |
| w18 | 32 | -0.146505 | -28.792 |
| w19 | 3 | 0.018609 | 4.934 |
| w20 | 2 | -0.078219 | 3.353 |
| w21 | 15 | 0.062196 | 4.157 |
| w22 | 40 | 0.010663 | 14.569 |
| w23 | 13 | 0.15764 | 77.804 |
| w24 | 44 | -0.098434 | -9.36 |
| w25 | 39 | 0.039903 | 36.997 |
| w26 | 15 | -0.042683 | -8.501 |
| w27 | 18 | 0.102422 | 45.385 |
| w28 | 15 | 0.084564 | 11.197 |
| w29 | 58 | -0.127235 | 2.792 |
| w30 | 37 | -0.076856 | 3.841 |
| w31 | 20 | -0.020269 | -8.231 |
| w32 | 2 | -0.0628 | -2.962 |

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
| w1 | 28 | 0.167238 | 230.046 |
| w2 | 43 | -0.061959 | -11.3 |
| w3 | 20 | -0.017055 | 7.609 |
| w4 | 27 | 0.099554 | 220.002 |
| w5 | 34 | 0.113055 | 94.844 |
| w6 | 31 | 0.092121 | 79.52 |
| w7 | 27 | 0.077364 | 19.425 |
| w8 | 7 | -0.112267 | -12.579 |
| w9 | 0 | None | 0.0 |
| w10 | 32 | -0.081787 | -6.128 |
| w11 | 34 | 0.068006 | 26.67 |
| w12 | 2 | 0.015259 | -0.512 |
| w13 | 26 | 0.027407 | 48.073 |
| w14 | 32 | 0.019498 | 52.142 |
| w15 | 45 | 0.049607 | 42.631 |
| w16 | 41 | 0.028663 | 83.923 |
| w17 | 32 | -0.032999 | -0.504 |
| w18 | 51 | -0.006479 | 1.271 |
| w19 | 10 | -0.024678 | 4.449 |
| w20 | 2 | -0.025234 | 3.385 |
| w21 | 16 | 0.026632 | 4.918 |
| w22 | 41 | -0.084873 | 18.982 |
| w23 | 39 | -0.052345 | 3.888 |
| w24 | 26 | -0.011412 | 22.277 |
| w25 | 36 | 0.04547 | 14.865 |
| w26 | 25 | -0.037408 | -3.357 |
| w27 | 14 | 0.097363 | 42.921 |
| w28 | 16 | -0.001822 | 7.074 |
| w29 | 39 | -0.086063 | 24.584 |
| w30 | 23 | -0.03072 | -1.123 |
| w31 | 0 | None | 0.0 |
| w32 | 18 | 0.132544 | 56.543 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 27 | 0.076413 | 55.095 |
| w11 | 24 | -0.049492 | -5.288 |
| w12 | 0 | None | 0.0 |
| w13 | 15 | 0.127453 | 68.88 |
| w14 | 38 | -0.059297 | 15.736 |
| w15 | 28 | 0.032268 | 7.454 |
| w16 | 34 | 0.088592 | 97.742 |
| w17 | 48 | -0.031684 | 35.281 |
| w18 | 19 | -0.134115 | -17.036 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | 0.008785 | -15.741 |
| w21 | 1 | 0.070498 | 4.634 |
| w22 | 36 | -0.040993 | -0.174 |
| w23 | 11 | 0.040894 | 14.011 |
| w24 | 20 | 0.048656 | 92.928 |
| w25 | 32 | 0.086507 | 13.948 |
| w26 | 0 | None | 0.0 |
| w27 | 17 | 0.272642 | 3.921 |
| w28 | 13 | -0.001251 | -1.711 |
| w29 | 29 | -0.057088 | -16.367 |
| w30 | 21 | 0.141768 | 11.206 |
| w31 | 0 | None | 0.0 |
| w32 | 5 | -0.026263 | -3.097 |

- ATOMUSD: 20 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 31 | -0.013113 | 11.039 |
| w14 | 39 | -0.062262 | -6.414 |
| w15 | 42 | -0.174349 | -36.221 |
| w16 | 32 | 0.036535 | 74.133 |
| w17 | 7 | 0.021667 | 29.528 |
| w18 | 36 | 0.020673 | 6.819 |
| w19 | 19 | -0.019625 | -4.111 |
| w20 | 11 | 0.05442 | -1.088 |
| w21 | 39 | -0.111091 | -23.761 |
| w22 | 35 | 0.017762 | 8.966 |
| w23 | 0 | None | 0.0 |
| w24 | 23 | -0.095431 | 4.255 |
| w25 | 46 | 0.057001 | 17.242 |
| w26 | 1 | 0.070132 | 2.421 |
| w27 | 14 | 0.128848 | 51.874 |
| w28 | 10 | 0.075426 | 5.937 |
| w29 | 28 | -0.099601 | -21.03 |
| w30 | 23 | 0.000391 | -3.386 |
| w31 | 3 | 0.165085 | 6.828 |
| w32 | 19 | 0.017451 | -5.443 |

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
| w15 | 15 | -0.143352 | -18.533 |
| w16 | 39 | 0.018374 | 58.494 |
| w17 | 17 | 0.054262 | 15.933 |
| w18 | 39 | 0.075351 | 37.63 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 25 | -0.08174 | -36.202 |
| w22 | 18 | -0.083637 | -16.941 |
| w23 | 0 | None | 0.0 |
| w24 | 27 | 0.065571 | 77.665 |
| w25 | 32 | 0.105222 | 14.797 |
| w26 | 2 | -0.045 | -0.292 |
| w27 | 21 | 0.219799 | 81.081 |
| w28 | 11 | 0.07189 | 8.291 |
| w29 | 24 | 0.048597 | 9.077 |
| w30 | 22 | -0.002742 | 4.569 |
| w31 | 2 | 0.086768 | -4.258 |
| w32 | 29 | 0.043991 | 1.698 |

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
| w15 | 45 | 0.022959 | -5.143 |
| w16 | 41 | -0.068452 | 59.78 |
| w17 | 16 | -0.030969 | 2.822 |
| w18 | 48 | -0.182972 | -26.506 |
| w19 | 3 | -0.032291 | -9.199 |
| w20 | 43 | -0.027334 | -28.682 |
| w21 | 4 | 0.109753 | 8.282 |
| w22 | 58 | -0.174008 | -10.034 |
| w23 | 63 | -0.088399 | -12.803 |
| w24 | 54 | -0.063676 | 30.885 |
| w25 | 42 | 0.093645 | 28.47 |
| w26 | 43 | -0.031093 | 9.748 |
| w27 | 50 | 0.05431 | 198.343 |
| w28 | 32 | -0.091628 | -6.103 |
| w29 | 58 | -0.015077 | 35.122 |
| w30 | 21 | -0.045201 | -4.107 |
| w31 | 44 | -0.055654 | -7.763 |
| w32 | 40 | 0.002155 | 0.934 |

- DOTUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 20 | -0.176656 | -27.331 |
| w18 | 47 | 0.017657 | 0.089 |
| w19 | 3 | -0.033295 | 7.791 |
| w20 | 2 | -0.042132 | -5.759 |
| w21 | 2 | 0.144322 | 8.342 |
| w22 | 36 | -0.061768 | -8.33 |
| w23 | 0 | None | 0.0 |
| w24 | 22 | 0.034121 | 37.97 |
| w25 | 35 | 0.06807 | 5.868 |
| w26 | 3 | -0.04689 | 0.019 |
| w27 | 17 | 0.148665 | 69.566 |
| w28 | 10 | 0.071605 | 7.275 |
| w29 | 16 | 0.020115 | -13.333 |
| w30 | 15 | 0.032491 | -15.591 |
| w31 | 0 | None | 0.0 |
| w32 | 7 | -0.001198 | -4.221 |

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
| w20 | 0 | 0.121572 | 0.0 |
| w21 | 10 | 0.094914 | 4.752 |
| w22 | 34 | -0.076154 | 5.913 |
| w23 | 0 | None | 0.0 |
| w24 | 13 | 0.20325 | 167.572 |
| w25 | 39 | 0.044293 | -0.96 |
| w26 | 2 | 0.032589 | 0.163 |
| w27 | 34 | -0.035405 | 3.323 |
| w28 | 15 | 0.017522 | 6.794 |
| w29 | 32 | -0.052128 | -20.625 |
| w30 | 24 | 0.014253 | -2.239 |
| w31 | 0 | None | 0.0 |
| w32 | 11 | -0.050113 | -0.242 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 28 | -0.100803 | -13.359 |
| w23 | 0 | None | 0.0 |
| w24 | 23 | 0.03707 | 62.557 |
| w25 | 32 | 0.088988 | 34.958 |
| w26 | 21 | -0.024124 | 2.417 |
| w27 | 30 | -0.049755 | -20.342 |
| w28 | 15 | 0.010159 | 11.462 |
| w29 | 22 | -0.068782 | -12.47 |
| w30 | 25 | -0.05494 | -17.571 |
| w31 | 0 | None | 0.0 |
| w32 | 44 | 0.094493 | 33.001 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 28 | -0.144995 | 3.47 |
| w25 | 45 | 0.033552 | 5.328 |
| w26 | 1 | -0.083025 | -6.228 |
| w27 | 31 | -0.069496 | 60.332 |
| w28 | 21 | 0.053693 | 9.045 |
| w29 | 38 | 0.009812 | 4.262 |
| w30 | 19 | 0.065544 | -2.746 |
| w31 | 0 | None | 0.0 |
| w32 | 17 | -0.009041 | 6.777 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 30 | 0.151136 | 115.931 |
| w6 | 40 | -0.078738 | -1.9 |
| w7 | 30 | -0.044075 | 0.447 |
| w8 | 2 | -0.007327 | 2.585 |
| w9 | 0 | None | 0.0 |
| w10 | 18 | 0.042497 | 11.831 |
| w11 | 40 | 0.07133 | 9.808 |
| w12 | 0 | None | 0.0 |
| w13 | 16 | 0.133046 | 72.88 |
| w14 | 39 | -0.058555 | 10.728 |
| w15 | 30 | -0.119951 | -17.707 |
| w16 | 55 | -0.215821 | 4.822 |
| w17 | 17 | 0.001187 | 2.725 |
| w18 | 49 | 0.000434 | -5.347 |
| w19 | 24 | 0.057114 | 10.504 |
| w20 | 5 | 0.086861 | 7.645 |
| w21 | 5 | 0.144508 | 8.79 |
| w22 | 9 | -0.235589 | -1.927 |
| w23 | 0 | None | 0.0 |
| w24 | 32 | -0.144515 | -20.714 |
| w25 | 12 | -0.009656 | 11.832 |
| w26 | 21 | 0.083103 | 31.468 |
| w27 | 55 | -0.000249 | 13.772 |
| w28 | 10 | 0.133264 | 11.661 |
| w29 | 35 | 0.030308 | -13.927 |
| w30 | 25 | 0.179773 | 260.161 |
| w31 | 12 | 0.001179 | -4.905 |
| w32 | 43 | 0.020779 | 31.825 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 53 | 0.066288 | 131.378 |
| w6 | 26 | 0.066527 | 104.078 |
| w7 | 20 | -0.149821 | -15.143 |
| w8 | 2 | -0.043735 | -6.064 |
| w9 | 4 | 0.074464 | -5.879 |
| w10 | 27 | 0.028146 | 17.052 |
| w11 | 55 | -0.064208 | -9.168 |
| w12 | 0 | None | 0.0 |
| w13 | 26 | 0.121225 | 57.41 |
| w14 | 33 | 0.028131 | 38.029 |
| w15 | 47 | -0.059911 | 7.723 |
| w16 | 41 | -0.051227 | 40.464 |
| w17 | 29 | 0.010257 | -2.733 |
| w18 | 32 | -0.07836 | -17.182 |
| w19 | 20 | 0.032433 | 2.311 |
| w20 | 16 | -0.168492 | -2.426 |
| w21 | 39 | -0.043051 | -7.777 |
| w22 | 45 | -0.009378 | -0.71 |
| w23 | 28 | 0.09093 | 15.44 |
| w24 | 41 | -0.090128 | -15.561 |
| w25 | 12 | -0.003143 | -32.909 |
| w26 | 60 | -0.032435 | -0.553 |
| w27 | 41 | -0.020388 | -15.85 |
| w28 | 58 | -0.07786 | -1.342 |
| w29 | 29 | 0.125592 | 44.05 |
| w30 | 49 | -0.229803 | -21.706 |
| w31 | 19 | 0.051261 | 3.24 |
| w32 | 27 | 0.068067 | 43.581 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 21 | -0.02311 | -8.341 |
| w18 | 48 | -0.184434 | -13.418 |
| w19 | 10 | 0.001543 | -12.52 |
| w20 | 2 | 0.033193 | -2.392 |
| w21 | 8 | -0.00401 | 0.984 |
| w22 | 20 | -0.016883 | 4.694 |
| w23 | 0 | None | 0.0 |
| w24 | 22 | -0.159492 | -16.069 |
| w25 | 29 | 0.143498 | 33.881 |
| w26 | 0 | None | 0.0 |
| w27 | 22 | 0.180095 | 99.87 |
| w28 | 10 | 0.041202 | 1.341 |
| w29 | 41 | 0.055964 | 16.456 |
| w30 | 11 | 0.007865 | 4.61 |
| w31 | 0 | None | 0.0 |
| w32 | 14 | 0.110714 | 31.322 |

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
| w17 | 15 | -0.195389 | -32.353 |
| w18 | 30 | -0.099836 | -21.908 |
| w19 | 3 | 0.040168 | 4.058 |
| w20 | 8 | 0.093486 | 7.022 |
| w21 | 13 | -0.047782 | -1.275 |
| w22 | 29 | -0.127808 | 0.7 |
| w23 | 8 | 0.015627 | -5.365 |
| w24 | 31 | -0.05094 | 3.146 |
| w25 | 39 | 0.095014 | 23.405 |
| w26 | 38 | -0.081593 | -17.831 |
| w27 | 55 | 0.000491 | 27.369 |
| w28 | 22 | 0.050791 | 12.415 |
| w29 | 43 | -0.214448 | -28.085 |
| w30 | 21 | 0.000154 | 0.643 |
| w31 | 0 | None | 0.0 |
| w32 | 14 | -0.014453 | 3.925 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 4 | 0.099974 | 24.394 |
| w20 | 3 | 0.127947 | 12.403 |
| w21 | 36 | -0.04396 | -6.813 |
| w22 | 28 | -0.038621 | 111.733 |
| w23 | 44 | -0.118271 | -15.591 |
| w24 | 30 | 0.079877 | 153.324 |
| w25 | 24 | -0.08103 | -8.493 |
| w26 | 4 | -0.012428 | -15.916 |
| w27 | 34 | 0.001693 | -19.865 |
| w28 | 12 | -0.07076 | 4.551 |
| w29 | 45 | -0.075849 | -14.63 |
| w30 | 23 | -0.096809 | 6.821 |
| w31 | 0 | None | 0.0 |
| w32 | 31 | 0.069823 | 28.205 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 39 | 0.022628 | 8.699 |
| w23 | 5 | -0.235678 | -23.86 |
| w24 | 20 | -0.066049 | 15.897 |
| w25 | 46 | -0.093774 | -14.685 |
| w26 | 0 | None | 0.0 |
| w27 | 15 | -0.022821 | 11.041 |
| w28 | 17 | -0.078346 | -6.46 |
| w29 | 25 | -0.034967 | 5.253 |
| w30 | 16 | -0.001284 | -2.489 |
| w31 | 0 | None | 0.0 |
| w32 | 17 | -0.018912 | -2.168 |

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
| w27 | 17 | 0.060456 | 40.587 |
| w28 | 16 | 0.052982 | 5.195 |
| w29 | 25 | 0.03062 | 2.399 |
| w30 | 25 | -0.163162 | -16.275 |
| w31 | 0 | None | 0.0 |
| w32 | 38 | 0.025987 | 34.444 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 12 | 0.001487 | 5.86 |
| w18 | 28 | -0.187153 | -17.095 |
| w19 | 3 | 0.094208 | 7.643 |
| w20 | 3 | -0.003494 | -9.267 |
| w21 | 7 | 0.071025 | 5.193 |
| w22 | 31 | -0.066269 | 3.194 |
| w23 | 2 | -0.000242 | 0.69 |
| w24 | 26 | 0.010546 | 25.014 |
| w25 | 45 | 0.069033 | 2.785 |
| w26 | 6 | 0.004654 | 0.57 |
| w27 | 27 | 0.06738 | -3.56 |
| w28 | 12 | 0.024494 | 3.654 |
| w29 | 7 | -0.025104 | -7.479 |
| w30 | 13 | -0.12704 | -10.657 |
| w31 | 1 | -0.075048 | -10.201 |
| w32 | 7 | -0.070009 | -11.156 |

- GRTUSD: 15 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w18 | 35 | 0.005479 | -13.291 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | -0.027274 | -5.949 |
| w21 | 8 | 0.037997 | 11.874 |
| w22 | 23 | 0.062891 | 83.581 |
| w23 | 3 | 0.01005 | 2.006 |
| w24 | 20 | 0.007739 | 35.194 |
| w25 | 30 | 0.158664 | 65.448 |
| w26 | 13 | -0.090646 | -4.043 |
| w27 | 23 | 0.024721 | -4.014 |
| w28 | 13 | 0.007712 | 5.41 |
| w29 | 19 | -0.027118 | -2.668 |
| w30 | 15 | 0.045021 | 7.228 |
| w31 | 0 | None | 0.0 |
| w32 | 9 | -0.127891 | -14.011 |

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
| w28 | 1 | 0.176553 | 8.994 |
| w29 | 29 | -0.060597 | -9.129 |
| w30 | 9 | -0.067637 | -18.156 |
| w31 | 7 | -0.007639 | -1.227 |
| w32 | 15 | -0.033395 | -9.152 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 32 | 0.023306 | -5.315 |
| w15 | 27 | 0.0005 | 13.227 |
| w16 | 18 | -0.014943 | 203.292 |
| w17 | 13 | 0.084621 | -2.237 |
| w18 | 23 | 0.020895 | -1.432 |
| w19 | 4 | -0.416739 | -18.69 |
| w20 | 1 | -0.125027 | -17.357 |
| w21 | 25 | 0.041323 | 45.232 |
| w22 | 31 | -0.111417 | -17.998 |
| w23 | 11 | -0.089669 | -8.971 |
| w24 | 30 | -0.024409 | 16.576 |
| w25 | 33 | 0.181098 | 93.903 |
| w26 | 15 | -0.114875 | -9.388 |
| w27 | 19 | 0.168739 | 139.541 |
| w28 | 10 | 0.028176 | 2.31 |
| w29 | 33 | -0.09423 | -19.159 |
| w30 | 20 | 0.004903 | 4.83 |
| w31 | 0 | None | 0.0 |
| w32 | 9 | 0.018663 | -4.202 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 29 | 0.278898 | 202.149 |
| w26 | 30 | -0.032616 | -9.389 |
| w27 | 26 | 0.067921 | 36.446 |
| w28 | 10 | 0.104319 | 11.532 |
| w29 | 28 | -0.035919 | -3.478 |
| w30 | 5 | 0.009183 | -6.732 |
| w31 | 1 | 0.01863 | 0.826 |
| w32 | 8 | -0.124987 | -15.94 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

