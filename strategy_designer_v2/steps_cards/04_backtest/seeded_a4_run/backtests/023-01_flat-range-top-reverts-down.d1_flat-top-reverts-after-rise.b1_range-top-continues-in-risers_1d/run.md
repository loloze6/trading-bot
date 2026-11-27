# Backtest of 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers_1d

- Plan: `../../../../03_test_plan/seeded_a4_run/plans/023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: XRP, TRX, ZEC, CRV, FIL, TAO, PEPE, BTC as XRPUSD, TRXUSD, ZECUSD, CRVUSD, FILUSD, TAOUSD, PEPEUSD, BTCUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- XRPUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5 (the coin's first 90 days); w20 (a hole of 2 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 41 | 0.168424 | -18.853 |
| w7 | 27 | 0.01548 | 5.83 |
| w8 | 2 | -0.078838 | -4.246 |
| w9 | 30 | 0.018483 | 8.967 |
| w10 | 16 | -0.171316 | -17.42 |
| w11 | 52 | 0.04163 | 20.637 |
| w12 | 4 | -0.057608 | -9.275 |
| w13 | 12 | 0.064047 | 18.44 |
| w14 | 27 | 0.116901 | 44.635 |
| w15 | 42 | 0.172931 | 90.882 |
| w16 | 42 | 0.069497 | 42.918 |
| w17 | 45 | -0.086721 | -16.92 |
| w18 | 41 | -0.1025 | -12.99 |
| w19 | 15 | 0.090214 | 7.92 |
| w21 | 47 | 0.054155 | 22.942 |
| w22 | 23 | -0.167205 | -24.313 |
| w23 | 41 | 0.010567 | 1.26 |
| w24 | 45 | -0.241557 | -27.01 |
| w25 | 34 | -0.054073 | -3.367 |
| w26 | 23 | -0.050071 | -0.056 |
| w27 | 43 | 0.19592 | 111.781 |
| w28 | 34 | -0.036159 | -6.087 |
| w29 | 40 | 0.083659 | 35.618 |
| w30 | 24 | -0.076221 | -18.984 |
| w31 | 0 | None | 0.0 |
| w32 | 12 | -0.102457 | -14.597 |

- TRXUSD: 18 of 32 windows run. 14 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 54 | -0.007488 | -2.512 |
| w16 | 64 | -0.042064 | 45.97 |
| w17 | 40 | -0.047182 | -5.258 |
| w18 | 51 | -0.132302 | -33.042 |
| w19 | 5 | -0.107638 | -5.739 |
| w20 | 41 | -0.046154 | -20.164 |
| w21 | 3 | 0.044911 | 3.932 |
| w22 | 57 | -0.273628 | -10.39 |
| w23 | 65 | 8e-05 | -1.468 |
| w24 | 60 | -0.176844 | 3.972 |
| w25 | 55 | 0.122011 | 23.196 |
| w26 | 39 | 0.070595 | 18.413 |
| w27 | 63 | 0.074807 | 68.406 |
| w28 | 35 | -0.187556 | -8.788 |
| w29 | 71 | -0.017263 | 26.491 |
| w30 | 26 | 0.013706 | 9.771 |
| w31 | 41 | -0.017368 | 18.847 |
| w32 | 43 | 0.078167 | 8.575 |

- ZECUSD: 28 of 32 windows run. 4 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 54 | 0.145205 | 98.319 |
| w6 | 38 | -0.06369 | 1.961 |
| w7 | 34 | -0.027178 | -1.383 |
| w8 | 2 | -0.007327 | 1.815 |
| w9 | 0 | None | 0.0 |
| w10 | 23 | 0.061341 | 16.941 |
| w11 | 51 | 0.086772 | 17.121 |
| w12 | 0 | None | 0.0 |
| w13 | 34 | 0.163735 | 48.625 |
| w14 | 43 | -0.100568 | 4.765 |
| w15 | 34 | -0.040656 | -13.913 |
| w16 | 58 | -0.00791 | 50.31 |
| w17 | 18 | -0.019707 | -4.97 |
| w18 | 53 | 0.057633 | -13.463 |
| w19 | 32 | 0.092745 | 22.35 |
| w20 | 7 | 0.046796 | 8.991 |
| w21 | 6 | 0.10316 | 6.831 |
| w22 | 19 | -0.212759 | -17.657 |
| w23 | 0 | None | 0.0 |
| w24 | 36 | -0.216069 | -29.197 |
| w25 | 16 | 0.049199 | 21.763 |
| w26 | 28 | 0.08219 | 30.621 |
| w27 | 49 | -0.00711 | 14.049 |
| w28 | 15 | 0.123509 | 21.261 |
| w29 | 50 | 0.094066 | 11.39 |
| w30 | 52 | 0.126693 | 156.072 |
| w31 | 17 | -0.010923 | -4.17 |
| w32 | 54 | -0.017769 | 11.428 |

- CRVUSD: 16 of 32 windows run. 15 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 20 | -0.292603 | -28.549 |
| w18 | 64 | -0.156682 | -12.729 |
| w19 | 11 | 0.085828 | 2.633 |
| w20 | 3 | 0.087356 | -2.965 |
| w21 | 17 | -0.004395 | 4.521 |
| w22 | 50 | -0.081803 | -20.209 |
| w23 | 0 | None | 0.0 |
| w24 | 26 | -0.230984 | -22.081 |
| w25 | 40 | 0.117316 | 37.266 |
| w26 | 0 | None | 0.0 |
| w27 | 33 | 0.141869 | 46.213 |
| w28 | 23 | 0.040287 | 0.415 |
| w29 | 52 | 0.061557 | 23.553 |
| w30 | 24 | -0.111395 | -11.194 |
| w31 | 0 | None | 0.0 |
| w32 | 25 | 0.044881 | 14.912 |

- w16 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_CRVUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- FILUSD: 16 of 32 windows run. 16 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 27 | 0.012672 | 8.389 |
| w18 | 31 | -0.084514 | -9.821 |
| w19 | 3 | 0.087615 | 5.236 |
| w20 | 3 | -0.012354 | -4.698 |
| w21 | 14 | 0.053402 | 9.697 |
| w22 | 43 | -0.08401 | -8.682 |
| w23 | 2 | -0.000242 | 3.098 |
| w24 | 30 | -0.046365 | 14.958 |
| w25 | 46 | 0.114458 | 24.344 |
| w26 | 6 | 0.010107 | 2.169 |
| w27 | 31 | 0.091236 | -14.404 |
| w28 | 17 | 0.038906 | 10.396 |
| w29 | 6 | 0.043852 | -0.338 |
| w30 | 11 | -0.071598 | -17.446 |
| w31 | 2 | -0.106447 | -9.738 |
| w32 | 13 | 0.038055 | 7.538 |

- TAOUSD: 5 of 32 windows run. 27 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18, w19, w20, w21, w22, w23, w24, w25, w26, w27 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 1 | 0.176553 | 2.598 |
| w29 | 39 | -0.056127 | -13.565 |
| w30 | 15 | -0.106863 | -14.065 |
| w31 | 16 | -0.022162 | -3.484 |
| w32 | 22 | 0.011496 | -8.722 |

- PEPEUSD: 8 of 32 windows run. 23 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18, w19, w20, w21, w22, w23 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 52 | 0.189038 | 92.486 |
| w26 | 52 | 0.059763 | 11.627 |
| w27 | 36 | 0.119609 | 31.948 |
| w28 | 19 | 0.051309 | 19.32 |
| w29 | 35 | -0.004837 | -5.27 |
| w30 | 10 | 0.020698 | -3.557 |
| w31 | 0 | -0.031624 | 0.0 |
| w32 | 10 | -0.097977 | -10.164 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 40 | -0.07392 | -6.536 |
| w2 | 53 | 0.110792 | 67.294 |
| w3 | 38 | -0.013604 | 45.625 |
| w4 | 37 | -0.061275 | -20.367 |
| w5 | 55 | 0.048049 | 87.967 |
| w6 | 39 | 0.059097 | 94.681 |
| w7 | 30 | 0.055565 | 4.497 |
| w8 | 6 | -0.056066 | -2.96 |
| w9 | 15 | -0.070312 | -8.432 |
| w10 | 23 | 0.098996 | 38.89 |
| w11 | 56 | 0.000722 | 25.924 |
| w12 | 12 | -0.17708 | -17.593 |
| w13 | 21 | 0.068458 | 14.185 |
| w14 | 48 | -0.029662 | -1.382 |
| w15 | 46 | 0.137127 | 110.591 |
| w16 | 56 | -0.060276 | 4.299 |
| w17 | 14 | -0.028101 | 0.652 |
| w18 | 52 | 0.050123 | 9.031 |
| w19 | 13 | -0.013166 | -2.746 |
| w20 | 2 | -0.044357 | 9.484 |
| w21 | 5 | -0.078203 | -4.834 |
| w22 | 44 | -0.078971 | 10.444 |
| w23 | 60 | 0.021059 | 16.339 |
| w24 | 34 | 0.013803 | 36.041 |
| w25 | 51 | 0.04336 | 21.018 |
| w26 | 34 | -0.071939 | -3.213 |
| w27 | 40 | -0.012668 | 52.54 |
| w28 | 26 | -0.064537 | -3.022 |
| w29 | 65 | 0.015785 | 8.839 |
| w30 | 24 | -0.08417 | -19.491 |
| w31 | 0 | None | 0.0 |
| w32 | 20 | 0.073787 | 17.94 |

