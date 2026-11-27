# Backtest of 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains_1d

- Plan: `../../../../03_test_plan/seeded_a4_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: XRP, TRX, ZEC, CRV, FIL, TAO, PEPE, BTC as XRPUSD, TRXUSD, ZECUSD, CRVUSD, FILUSD, TAOUSD, PEPEUSD, BTCUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- XRPUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5 (the coin's first 90 days); w20 (a hole of 2 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 47 | 0.102583 | 13.127 |
| w7 | 46 | 0.129594 | 4.569 |
| w8 | 65 | 0.136456 | 5.887 |
| w9 | 47 | 0.195889 | 12.137 |
| w10 | 50 | -0.000233 | -3.38 |
| w11 | 37 | 0.072743 | 4.535 |
| w12 | 43 | -0.039172 | -1.98 |
| w13 | 42 | -0.01023 | -0.365 |
| w14 | 49 | 0.100051 | 3.054 |
| w15 | 41 | 0.206296 | 30.898 |
| w16 | 45 | -0.029632 | -5.867 |
| w17 | 38 | 0.213073 | 12.787 |
| w18 | 52 | 0.011003 | 3.077 |
| w19 | 56 | 0.068468 | 0.776 |
| w21 | 42 | 0.13218 | 12.918 |
| w22 | 47 | 0.078446 | 4.766 |
| w23 | 52 | -0.084379 | -19.783 |
| w24 | 51 | -0.018859 | -7.104 |
| w25 | 50 | -0.132951 | -9.953 |
| w26 | 53 | 0.049132 | 3.533 |
| w27 | 36 | 0.172987 | 22.739 |
| w28 | 42 | -0.032724 | -3.842 |
| w29 | 41 | 0.134959 | 11.966 |
| w30 | 46 | -0.05358 | -2.289 |
| w31 | 46 | 0.010235 | 1.985 |
| w32 | 47 | 0.088518 | 7.509 |

- TRXUSD: 18 of 32 windows run. 14 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 38 | 0.048109 | 1.068 |
| w16 | 51 | 0.026037 | 2.281 |
| w17 | 44 | 0.225475 | 13.978 |
| w18 | 49 | -0.014858 | 2.199 |
| w19 | 44 | -0.017701 | -6.089 |
| w20 | 41 | -0.012685 | -4.445 |
| w21 | 47 | 0.009921 | -0.525 |
| w22 | 61 | 0.050021 | 0.421 |
| w23 | 56 | -0.02697 | -3.884 |
| w24 | 64 | 0.166003 | 6.04 |
| w25 | 69 | 0.068397 | 0.36 |
| w26 | 67 | 0.19527 | 12.749 |
| w27 | 45 | 0.092428 | 24.418 |
| w28 | 60 | 0.109939 | 2.826 |
| w29 | 51 | -0.064675 | -9.008 |
| w30 | 70 | 0.064548 | -0.589 |
| w31 | 58 | 0.036664 | -2.021 |
| w32 | 79 | -0.042805 | -5.477 |

- ZECUSD: 28 of 32 windows run. 4 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 56 | 0.021255 | -0.376 |
| w6 | 48 | 0.131757 | 8.668 |
| w7 | 43 | 0.079338 | 1.865 |
| w8 | 60 | 0.141826 | 9.564 |
| w9 | 55 | -0.042972 | -4.246 |
| w10 | 41 | 0.070242 | 0.981 |
| w11 | 64 | 0.022609 | 1.003 |
| w12 | 61 | 0.107393 | 7.141 |
| w13 | 46 | 0.018272 | 3.161 |
| w14 | 66 | -0.033366 | -6.647 |
| w15 | 49 | 0.08864 | 5.158 |
| w16 | 52 | 0.01022 | -5.969 |
| w17 | 54 | 0.227771 | 18.073 |
| w18 | 40 | 0.097885 | 3.388 |
| w19 | 52 | 0.107924 | 7.464 |
| w20 | 51 | 0.018953 | 1.728 |
| w21 | 57 | -0.011995 | -4.274 |
| w22 | 51 | 0.179525 | 13.295 |
| w23 | 62 | -0.102857 | -6.94 |
| w24 | 67 | -0.001528 | -5.399 |
| w25 | 47 | 0.005598 | -0.599 |
| w26 | 61 | 0.025275 | -1.65 |
| w27 | 56 | 0.054791 | 6.88 |
| w28 | 64 | 0.117301 | 6.06 |
| w29 | 71 | 0.100017 | 7.99 |
| w30 | 39 | 0.27198 | 18.072 |
| w31 | 52 | 0.083843 | -2.101 |
| w32 | 39 | 0.034916 | 4.465 |

- CRVUSD: 16 of 32 windows run. 15 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 40 | 0.06003 | 0.27 |
| w18 | 48 | -0.051206 | -6.437 |
| w19 | 44 | 0.087457 | 2.882 |
| w20 | 52 | 0.040796 | 0.306 |
| w21 | 62 | 0.04934 | -1.603 |
| w22 | 48 | -0.010012 | -5.087 |
| w23 | 56 | -0.001066 | -2.623 |
| w24 | 55 | 0.110484 | 8.361 |
| w25 | 37 | 0.193003 | 16.064 |
| w26 | 60 | -0.010248 | -3.669 |
| w27 | 50 | 0.134802 | 5.976 |
| w28 | 46 | 0.063533 | 2.106 |
| w29 | 47 | 0.114085 | 8.545 |
| w30 | 43 | 0.017848 | 0.722 |
| w31 | 51 | 0.029961 | -2.932 |
| w32 | 38 | 0.141428 | 11.429 |

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
| w17 | 50 | 0.127633 | 3.901 |
| w18 | 51 | 0.033684 | -0.131 |
| w19 | 60 | 0.001847 | -1.18 |
| w20 | 57 | 0.011653 | 5.787 |
| w21 | 60 | -0.067141 | -5.639 |
| w22 | 41 | 0.044367 | 5.718 |
| w23 | 65 | -0.087296 | -9.326 |
| w24 | 46 | -0.01193 | -1.048 |
| w25 | 28 | 0.150804 | 15.828 |
| w26 | 68 | 0.134371 | 4.962 |
| w27 | 60 | 0.09861 | 7.789 |
| w28 | 56 | -0.102023 | -4.534 |
| w29 | 62 | -0.004488 | -4.564 |
| w30 | 47 | 0.143378 | 14.826 |
| w31 | 46 | -0.05569 | -4.245 |
| w32 | 55 | -0.010469 | -1.819 |

- TAOUSD: 5 of 32 windows run. 27 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18, w19, w20, w21, w22, w23, w24, w25, w26, w27 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 46 | 0.076739 | 5.235 |
| w29 | 51 | -0.032557 | -2.569 |
| w30 | 33 | 0.107643 | 7.426 |
| w31 | 46 | 0.033899 | 0.249 |
| w32 | 48 | -0.045819 | 1.248 |

- PEPEUSD: 8 of 32 windows run. 23 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18, w19, w20, w21, w22, w23 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 46 | 0.23931 | 35.087 |
| w26 | 51 | 0.088703 | 3.527 |
| w27 | 37 | 0.183281 | 17.501 |
| w28 | 52 | -0.099121 | -5.87 |
| w29 | 42 | 0.068953 | 2.429 |
| w30 | 49 | 0.163053 | 9.055 |
| w31 | 45 | 0.059343 | 0.297 |
| w32 | 57 | 0.067724 | 4.007 |

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
| w1 | 45 | -0.076654 | -4.147 |
| w2 | 42 | 0.043987 | 2.389 |
| w3 | 56 | 0.093167 | 5.008 |
| w4 | 40 | -0.163558 | -15.537 |
| w5 | 31 | 0.145978 | 5.407 |
| w6 | 46 | -0.030016 | -2.296 |
| w7 | 29 | -0.083101 | -3.738 |
| w8 | 52 | 0.119598 | 4.837 |
| w9 | 41 | -0.048162 | -1.529 |
| w10 | 38 | 0.093026 | 4.931 |
| w11 | 42 | 0.086461 | 4.413 |
| w12 | 49 | 0.082813 | 1.981 |
| w13 | 40 | -0.058625 | -9.221 |
| w14 | 48 | -0.001747 | 2.296 |
| w15 | 49 | 0.005297 | 0.057 |
| w16 | 46 | -0.07601 | -4.461 |
| w17 | 36 | 0.190519 | 9.077 |
| w18 | 53 | 0.007082 | -0.663 |
| w19 | 59 | -0.029122 | 0.107 |
| w20 | 44 | -0.091624 | -7.121 |
| w21 | 57 | 0.006913 | 1.42 |
| w22 | 48 | 0.214192 | 18.276 |
| w23 | 58 | 0.043627 | 1.34 |
| w24 | 55 | 0.095636 | 1.118 |
| w25 | 43 | -0.021359 | -2.193 |
| w26 | 62 | 0.039425 | 4.203 |
| w27 | 46 | 0.138456 | 7.43 |
| w28 | 62 | -0.047117 | -6.006 |
| w29 | 57 | 0.000146 | 0.008 |
| w30 | 67 | -0.056858 | -3.858 |
| w31 | 41 | -0.090453 | -8.804 |
| w32 | 53 | 0.003139 | 0.027 |

