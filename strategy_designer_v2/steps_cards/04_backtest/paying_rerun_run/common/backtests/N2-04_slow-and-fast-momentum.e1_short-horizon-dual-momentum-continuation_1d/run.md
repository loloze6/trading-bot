# Backtest of N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1d

- Plan: `../../../../../03_test_plan/validation_run/plans/N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | -0.019215 | 1.942 |
| w2 | 27 | 0.087856 | 53.195 |
| w3 | 32 | 0.01751 | 82.435 |
| w4 | 25 | -0.137871 | -13.966 |
| w5 | 30 | 0.042089 | 102.925 |
| w6 | 26 | 0.072523 | 116.581 |
| w7 | 1 | -0.073653 | -0.679 |
| w8 | 11 | -0.03092 | -3.543 |
| w9 | 7 | -0.080372 | -7.703 |
| w10 | 18 | 0.055394 | 29.723 |
| w11 | 35 | 0.084691 | 64.454 |
| w12 | 1 | -0.02118 | -0.124 |
| w13 | 18 | -0.044243 | -1.087 |
| w14 | 37 | -0.070956 | 7.928 |
| w15 | 22 | 0.135544 | 142.926 |
| w16 | 28 | -0.022599 | 22.828 |
| w17 | 10 | 0.066926 | 8.683 |
| w18 | 21 | -0.006826 | -1.843 |
| w19 | 8 | 0.019794 | 0.488 |
| w20 | 3 | -0.0234 | -1.36 |
| w21 | 8 | -0.155938 | -14.137 |
| w22 | 31 | -0.094145 | 38.762 |
| w23 | 5 | 0.053 | 4.884 |
| w24 | 25 | 0.062063 | 65.112 |
| w25 | 19 | 0.056731 | 38.438 |
| w26 | 11 | -0.088319 | -5.931 |
| w27 | 29 | 0.045484 | 62.077 |
| w28 | 9 | -0.064787 | -5.591 |
| w29 | 34 | 0.016668 | 4.355 |
| w30 | 7 | -0.030197 | -6.105 |
| w31 | 10 | -0.009084 | -3.742 |
| w32 | 18 | 0.139165 | 24.596 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.008542 | -0.949 |
| w2 | 9 | 0.098704 | 30.037 |
| w3 | 21 | -0.11492 | -18.649 |
| w4 | 28 | 0.096763 | 56.712 |
| w5 | 33 | 0.05064 | 35.113 |
| w6 | 26 | 0.093548 | 106.434 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 1 | -0.07255 | -1.274 |
| w10 | 23 | -0.011335 | 30.759 |
| w11 | 22 | 0.020985 | 1.447 |
| w12 | 0 | None | 0.0 |
| w13 | 14 | -0.003839 | 5.858 |
| w14 | 33 | 0.006566 | 11.856 |
| w15 | 26 | 0.007707 | 21.652 |
| w16 | 32 | -0.069477 | 11.853 |
| w17 | 19 | -0.083359 | -17.868 |
| w18 | 29 | -0.135259 | -24.982 |
| w19 | 8 | -0.010047 | -3.33 |
| w20 | 5 | -0.002718 | -1.151 |
| w21 | 27 | -0.016411 | -4.622 |
| w22 | 31 | -0.042931 | -1.713 |
| w23 | 16 | -0.084272 | -16.051 |
| w24 | 27 | -0.122522 | -11.325 |
| w25 | 24 | -0.020264 | 9.286 |
| w26 | 2 | -0.06438 | -1.06 |
| w27 | 28 | 0.005885 | 23.68 |
| w28 | 18 | -0.06186 | -6.18 |
| w29 | 21 | 0.00373 | 11.932 |
| w30 | 8 | -0.383484 | -15.301 |
| w31 | 9 | 0.001719 | -2.175 |
| w32 | 16 | -0.005518 | -2.803 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 26 | 0.17203 | 125.917 |
| w7 | 5 | -0.075123 | -4.331 |
| w8 | 2 | -0.01808 | -0.975 |
| w9 | 11 | -0.116409 | -9.84 |
| w10 | 11 | -0.063165 | -9.997 |
| w11 | 16 | -0.014151 | -2.919 |
| w12 | 8 | -0.010545 | -3.847 |
| w13 | 17 | -0.043617 | -4.856 |
| w14 | 17 | 0.150928 | 52.203 |
| w15 | 14 | 0.187 | 124.785 |
| w16 | 21 | -0.017466 | 50.564 |
| w17 | 17 | -0.020871 | 2.689 |
| w18 | 17 | -0.14854 | -11.055 |
| w19 | 17 | -0.084295 | -11.213 |
| w20 | 5 | -0.038775 | -2.856 |
| w21 | 16 | -0.005784 | 1.906 |
| w22 | 25 | -0.073371 | -6.59 |
| w23 | 10 | -0.081613 | -12.384 |
| w24 | 21 | -0.057651 | 4.803 |
| w25 | 18 | -0.162585 | -21.756 |
| w26 | 17 | -0.080636 | -7.798 |
| w27 | 13 | 0.290905 | 235.162 |
| w28 | 7 | -0.062865 | -3.052 |
| w29 | 23 | -0.006309 | 8.985 |
| w30 | 2 | -0.001973 | 0.077 |
| w31 | 4 | -0.021522 | -2.027 |
| w32 | 8 | 0.030778 | 4.945 |

- BCHUSD: 25 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w8 | 6 | 0.025368 | -1.322 |
| w9 | 6 | -0.062093 | -9.97 |
| w10 | 11 | 0.150958 | 54.572 |
| w11 | 19 | -0.00475 | -2.047 |
| w12 | 5 | -0.05817 | -5.118 |
| w13 | 13 | -0.028885 | 1.872 |
| w14 | 28 | 0.003618 | 2.277 |
| w15 | 24 | -0.1603 | -26.764 |
| w16 | 34 | 0.00824 | 55.796 |
| w17 | 21 | -0.052446 | -8.192 |
| w18 | 12 | -0.239327 | -19.759 |
| w19 | 5 | -0.043257 | -8.694 |
| w20 | 1 | -0.019052 | -1.187 |
| w21 | 6 | -0.084514 | -6.013 |
| w22 | 29 | -0.012392 | 5.362 |
| w23 | 6 | 0.178372 | 63.653 |
| w24 | 24 | -0.262107 | -25.518 |
| w25 | 34 | 0.014977 | 46.376 |
| w26 | 3 | -0.025505 | -0.529 |
| w27 | 22 | 0.023652 | 14.968 |
| w28 | 8 | 0.019172 | 0.55 |
| w29 | 56 | -0.185531 | -4.703 |
| w30 | 22 | -0.143163 | -13.459 |
| w31 | 10 | -0.034128 | -5.734 |
| w32 | 6 | -0.02364 | -1.688 |

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
| w1 | 20 | 0.21213 | 250.261 |
| w2 | 20 | -0.165586 | -16.637 |
| w3 | 19 | 0.076631 | -0.024 |
| w4 | 27 | 0.107108 | 247.456 |
| w5 | 20 | 0.082047 | 65.186 |
| w6 | 24 | 0.107747 | 82.528 |
| w7 | 9 | 0.035992 | 15.129 |
| w8 | 4 | -0.104748 | -4.261 |
| w9 | 1 | -0.020515 | -0.523 |
| w10 | 24 | 0.015902 | 6.373 |
| w11 | 24 | 0.079901 | 23.438 |
| w12 | 7 | -0.008866 | -1.674 |
| w13 | 13 | 0.010523 | 25.46 |
| w14 | 33 | 0.078689 | 70.142 |
| w15 | 26 | 0.008631 | 24.286 |
| w16 | 25 | 0.033686 | 73.169 |
| w17 | 17 | 0.005818 | 11.544 |
| w18 | 35 | -0.167186 | -22.081 |
| w19 | 8 | 0.056915 | 3.701 |
| w20 | 8 | -0.043699 | -5.284 |
| w21 | 8 | -0.07809 | -7.237 |
| w22 | 34 | -0.10974 | 9.581 |
| w23 | 15 | -0.141567 | -12.317 |
| w24 | 24 | -0.022916 | 23.943 |
| w25 | 24 | 0.026158 | 15.463 |
| w26 | 7 | 0.005736 | -1.148 |
| w27 | 19 | 0.050953 | 26.777 |
| w28 | 1 | -0.122584 | -0.606 |
| w29 | 35 | -0.101218 | 32.148 |
| w30 | 5 | -0.086522 | -2.231 |
| w31 | 15 | -0.060355 | -10.012 |
| w32 | 9 | 0.09403 | 15.956 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 22 | 0.105249 | 50.84 |
| w11 | 17 | -0.116614 | -10.548 |
| w12 | 0 | None | 0.0 |
| w13 | 10 | 0.004915 | 21.314 |
| w14 | 29 | 0.011157 | 46.274 |
| w15 | 15 | 0.077525 | 27.353 |
| w16 | 23 | 0.146285 | 130.541 |
| w17 | 20 | 0.040129 | 33.522 |
| w18 | 5 | -0.089657 | -8.395 |
| w19 | 2 | 0.007887 | -3.114 |
| w20 | 6 | -0.024416 | -3.732 |
| w21 | 5 | -0.019163 | -2.872 |
| w22 | 26 | -0.100466 | -1.031 |
| w23 | 1 | -0.015525 | -0.326 |
| w24 | 17 | 0.122288 | 142.384 |
| w25 | 17 | -0.049885 | -10.74 |
| w26 | 3 | -0.12962 | -4.187 |
| w27 | 13 | 0.258525 | 161.458 |
| w28 | 8 | -0.180308 | -9.314 |
| w29 | 27 | -0.110154 | -14.836 |
| w30 | 7 | -0.055652 | -3.783 |
| w31 | 0 | None | 0.0 |
| w32 | 15 | 0.013578 | -0.145 |

- ATOMUSD: 20 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 19 | -0.13478 | -17.98 |
| w14 | 27 | 0.002865 | 32.539 |
| w15 | 24 | -0.045683 | -1.294 |
| w16 | 33 | 0.04038 | 47.498 |
| w17 | 19 | 0.046513 | 15.739 |
| w18 | 21 | -0.020069 | 0.159 |
| w19 | 12 | -0.032946 | -8.472 |
| w20 | 15 | 0.000552 | -3.53 |
| w21 | 18 | -0.011059 | -5.419 |
| w22 | 19 | -0.038585 | -1.557 |
| w23 | 0 | None | 0.0 |
| w24 | 24 | 0.011366 | 27.29 |
| w25 | 12 | -0.00187 | -3.929 |
| w26 | 0 | None | 0.0 |
| w27 | 13 | 0.154099 | 59.053 |
| w28 | 3 | -0.177954 | -2.004 |
| w29 | 24 | -0.064771 | -13.023 |
| w30 | 3 | -0.001516 | -0.594 |
| w31 | 9 | -0.173499 | -11.27 |
| w32 | 15 | -0.000111 | -6.221 |

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
| w15 | 10 | -0.081782 | -11.853 |
| w16 | 23 | 0.058799 | 78.493 |
| w17 | 17 | -0.073627 | -11.161 |
| w18 | 17 | 0.063709 | 33.419 |
| w19 | 2 | -0.124057 | -5.05 |
| w20 | 6 | -0.034679 | -3.187 |
| w21 | 14 | -0.044891 | -16.706 |
| w22 | 12 | -0.057432 | -5.537 |
| w23 | 1 | -0.114469 | -1.877 |
| w24 | 14 | 0.097223 | 91.2 |
| w25 | 17 | -0.05993 | -14.178 |
| w26 | 2 | -0.052245 | -1.991 |
| w27 | 15 | 0.196181 | 127.692 |
| w28 | 5 | -0.130814 | -3.796 |
| w29 | 22 | -0.117374 | -15.679 |
| w30 | 0 | None | 0.0 |
| w31 | 11 | -0.077811 | -8.956 |
| w32 | 17 | -0.10418 | -14.046 |

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
| w15 | 27 | -0.14224 | -23.579 |
| w16 | 36 | -0.030762 | 64.044 |
| w17 | 15 | -0.007136 | -0.193 |
| w18 | 22 | -0.153074 | -19.682 |
| w19 | 8 | 0.003579 | -1.585 |
| w20 | 27 | -0.037362 | -8.722 |
| w21 | 4 | -0.066336 | -2.221 |
| w22 | 33 | -0.043064 | 2.923 |
| w23 | 34 | -0.046473 | -1.258 |
| w24 | 38 | -0.129309 | 19.816 |
| w25 | 24 | 0.071002 | 21.656 |
| w26 | 32 | -0.019253 | 17.808 |
| w27 | 33 | 0.058864 | 194.315 |
| w28 | 18 | -0.090067 | -9.867 |
| w29 | 42 | -0.094796 | 27.815 |
| w30 | 6 | -0.130731 | -3.208 |
| w31 | 31 | -0.076455 | 5.154 |
| w32 | 19 | 0.093416 | 13.413 |

- DOTUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 17 | -0.042156 | -5.945 |
| w18 | 24 | -0.03588 | -9.459 |
| w19 | 8 | 0.020714 | -2.678 |
| w20 | 6 | -0.037245 | -5.512 |
| w21 | 4 | -0.070701 | -3.721 |
| w22 | 23 | -0.154095 | -11.927 |
| w23 | 3 | -0.073667 | -1.849 |
| w24 | 17 | 0.08094 | 58.672 |
| w25 | 25 | -0.042282 | -11.677 |
| w26 | 0 | None | 0.0 |
| w27 | 10 | 0.133522 | 58.976 |
| w28 | 1 | -0.092556 | -0.936 |
| w29 | 17 | -0.038139 | -6.849 |
| w30 | 9 | -0.076006 | -9.389 |
| w31 | 0 | 0.028614 | 0.0 |
| w32 | 4 | -0.138571 | -6.947 |

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
| w20 | 10 | -0.026265 | -6.106 |
| w21 | 1 | -0.1288 | -4.237 |
| w22 | 21 | 0.004747 | 13.126 |
| w23 | 0 | None | 0.0 |
| w24 | 18 | 0.18281 | 177.248 |
| w25 | 14 | 0.010305 | 0.538 |
| w26 | 3 | -0.014532 | -0.876 |
| w27 | 22 | -0.001831 | 18.358 |
| w28 | 2 | -0.050703 | -1.566 |
| w29 | 34 | -0.081689 | -11.021 |
| w30 | 20 | 0.080269 | 3.34 |
| w31 | 6 | -0.06119 | -3.974 |
| w32 | 9 | 0.030153 | 1.453 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 13 | -0.080692 | -2.772 |
| w23 | 0 | None | 0.0 |
| w24 | 15 | 0.144767 | 135.669 |
| w25 | 24 | -0.006052 | 11.724 |
| w26 | 12 | -0.017836 | -2.623 |
| w27 | 25 | -0.026962 | 1.019 |
| w28 | 0 | None | 0.0 |
| w29 | 22 | -0.062188 | -10.023 |
| w30 | 16 | -0.06493 | -10.8 |
| w31 | 11 | -0.013903 | -3.308 |
| w32 | 25 | 0.040741 | 25.773 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 25 | -0.01715 | 10.203 |
| w25 | 35 | 0.058479 | 21.743 |
| w26 | 4 | -0.174316 | -9.447 |
| w27 | 32 | -0.024789 | 65.483 |
| w28 | 9 | -0.042865 | -3.391 |
| w29 | 23 | -0.069986 | -11.609 |
| w30 | 1 | 0.044209 | 0.215 |
| w31 | 6 | -0.138775 | -7.856 |
| w32 | 20 | -0.06721 | -5.608 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 19 | 0.069211 | 63.407 |
| w6 | 31 | -0.010437 | 18.504 |
| w7 | 10 | -0.048123 | -3.272 |
| w8 | 7 | -0.125837 | -5.77 |
| w9 | 4 | -0.023067 | -2.718 |
| w10 | 13 | 0.102635 | 20.859 |
| w11 | 31 | 0.081969 | 12.836 |
| w12 | 0 | None | 0.0 |
| w13 | 10 | 0.067146 | 37.588 |
| w14 | 38 | -0.068986 | 11.109 |
| w15 | 15 | 0.020225 | -0.041 |
| w16 | 35 | -0.135967 | 15.645 |
| w17 | 17 | -0.078041 | -13.43 |
| w18 | 25 | -0.064407 | -10.311 |
| w19 | 8 | -0.002625 | -2.202 |
| w20 | 4 | -0.062405 | -5.589 |
| w21 | 1 | -0.01663 | -0.278 |
| w22 | 24 | -0.12191 | -13.16 |
| w23 | 2 | -0.067906 | -1.591 |
| w24 | 25 | -0.080495 | -9.699 |
| w25 | 9 | 0.020181 | -0.891 |
| w26 | 18 | 0.046786 | 22.017 |
| w27 | 20 | -0.001146 | 18.55 |
| w28 | 9 | -0.161056 | -10.264 |
| w29 | 25 | 0.046713 | 10.897 |
| w30 | 32 | 0.174951 | 250.967 |
| w31 | 8 | 0.023532 | 1.418 |
| w32 | 19 | 0.088259 | 54.906 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 38 | 0.063922 | 102.73 |
| w6 | 17 | 0.027971 | 78.132 |
| w7 | 7 | -0.015961 | 0.277 |
| w8 | 0 | None | 0.0 |
| w9 | 7 | -0.160419 | -9.31 |
| w10 | 25 | 0.010208 | 13.528 |
| w11 | 30 | -0.076308 | -10.518 |
| w12 | 0 | None | 0.0 |
| w13 | 18 | -0.025066 | 8.446 |
| w14 | 37 | -0.017418 | 31.449 |
| w15 | 40 | -0.063141 | 7.522 |
| w16 | 32 | -0.057861 | 29.467 |
| w17 | 17 | -0.031897 | -9.054 |
| w18 | 15 | -0.195113 | -19.496 |
| w19 | 26 | -0.003395 | -1.921 |
| w20 | 4 | -0.076702 | -6.387 |
| w21 | 16 | -0.117648 | -13.325 |
| w22 | 19 | 0.043524 | 9.775 |
| w23 | 13 | 0.002711 | -2.677 |
| w24 | 31 | -0.136912 | -8.214 |
| w25 | 1 | -0.040605 | -0.408 |
| w26 | 20 | -0.041867 | 0.215 |
| w27 | 24 | 0.053423 | 15.616 |
| w28 | 30 | 0.12799 | 27.106 |
| w29 | 10 | 0.095881 | 26.94 |
| w30 | 51 | -0.158033 | -6.695 |
| w31 | 17 | -0.036782 | -4.971 |
| w32 | 20 | 0.115053 | 61.039 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 21 | -0.163757 | -19.11 |
| w18 | 54 | -0.203495 | -16.099 |
| w19 | 5 | -0.120323 | -7.262 |
| w20 | 13 | -0.154273 | -15.31 |
| w21 | 3 | 0.000261 | -0.553 |
| w22 | 18 | 0.029569 | 15.741 |
| w23 | 2 | -0.060946 | -2.155 |
| w24 | 26 | -0.089892 | -6.744 |
| w25 | 12 | -0.000594 | -5.828 |
| w26 | 7 | -0.090047 | -5.674 |
| w27 | 19 | 0.183954 | 131.959 |
| w28 | 19 | 0.026275 | 1.913 |
| w29 | 27 | -0.027373 | -0.512 |
| w30 | 0 | None | 0.0 |
| w31 | 6 | -0.033522 | -2.308 |
| w32 | 26 | 0.057474 | 16.097 |

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
| w17 | 19 | -0.104686 | -18.642 |
| w18 | 7 | -0.195341 | -10.027 |
| w19 | 9 | 0.067993 | 8.655 |
| w20 | 7 | -0.055023 | -6.963 |
| w21 | 9 | -0.117887 | -9.618 |
| w22 | 17 | 0.01165 | 10.523 |
| w23 | 12 | -0.019707 | -3.54 |
| w24 | 29 | -0.130928 | 2.134 |
| w25 | 18 | -0.075782 | -19.137 |
| w26 | 24 | 0.057742 | 18.41 |
| w27 | 43 | -0.030515 | 39.176 |
| w28 | 4 | -0.017001 | -1.05 |
| w29 | 36 | -0.095442 | 3.375 |
| w30 | 2 | -0.120957 | -2.321 |
| w31 | 2 | -0.040456 | -1.551 |
| w32 | 12 | 0.008579 | 4.324 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 8 | -0.011648 | -2.736 |
| w20 | 10 | -0.049458 | -8.689 |
| w21 | 27 | -0.102805 | -15.362 |
| w22 | 30 | -0.021487 | 92.013 |
| w23 | 18 | -0.017365 | -2.124 |
| w24 | 19 | 0.139924 | 229.681 |
| w25 | 20 | -0.153408 | -13.798 |
| w26 | 9 | -0.08315 | -6.745 |
| w27 | 27 | -0.020277 | -1.621 |
| w28 | 0 | None | 0.0 |
| w29 | 36 | -0.09272 | -10.439 |
| w30 | 3 | 0.045408 | -0.397 |
| w31 | 4 | -0.020198 | -3.923 |
| w32 | 23 | 0.034461 | 32.392 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 23 | 0.037917 | 21.063 |
| w23 | 11 | -0.096709 | -8.446 |
| w24 | 26 | -0.012992 | 22.508 |
| w25 | 21 | -0.009789 | -7.293 |
| w26 | 4 | -0.160806 | -5.302 |
| w27 | 22 | -0.012564 | 7.604 |
| w28 | 9 | -0.122021 | -6.375 |
| w29 | 24 | -0.055445 | -1.888 |
| w30 | 2 | -0.163671 | -1.895 |
| w31 | 12 | -0.018453 | -4.063 |
| w32 | 16 | -0.118141 | -13.266 |

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
| w27 | 17 | 0.098007 | 50.371 |
| w28 | 4 | -0.063113 | -2.924 |
| w29 | 30 | -0.142135 | -17.869 |
| w30 | 5 | 0.051657 | 0.058 |
| w31 | 3 | -0.052377 | -0.927 |
| w32 | 23 | -0.00712 | 20.794 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 8 | 0.004114 | -1.968 |
| w18 | 8 | -0.038537 | -9.299 |
| w19 | 3 | 0.004276 | -3.549 |
| w20 | 9 | -0.086262 | -14.03 |
| w21 | 5 | -0.119339 | -5.658 |
| w22 | 24 | -0.09226 | -0.026 |
| w23 | 3 | -0.087954 | -2.06 |
| w24 | 25 | -0.050793 | 25.396 |
| w25 | 26 | 0.018182 | -0.325 |
| w26 | 0 | None | 0.0 |
| w27 | 19 | 0.108272 | 39.821 |
| w28 | 4 | -0.08372 | -1.908 |
| w29 | 14 | -0.133381 | -12.459 |
| w30 | 4 | -0.187843 | -8.746 |
| w31 | 5 | -0.015055 | -2.926 |
| w32 | 17 | -0.152687 | -17.655 |

- GRTUSD: 15 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w18 | 15 | -0.044355 | -9.667 |
| w19 | 7 | 0.039227 | 0.729 |
| w20 | 5 | -0.059103 | -8.303 |
| w21 | 7 | -0.11566 | -6.822 |
| w22 | 27 | 0.079401 | 85.287 |
| w23 | 4 | -0.131722 | -4.273 |
| w24 | 27 | 0.035393 | 48.606 |
| w25 | 23 | 0.164124 | 55.965 |
| w26 | 0 | None | 0.0 |
| w27 | 19 | 0.05435 | 19.557 |
| w28 | 2 | -0.02796 | -0.893 |
| w29 | 16 | -0.089687 | -10.52 |
| w30 | 2 | 0.043839 | 0.19 |
| w31 | 0 | None | 0.0 |
| w32 | 7 | -0.044794 | -8.357 |

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
| w28 | 3 | -0.056442 | -1.993 |
| w29 | 21 | -0.00868 | -5.445 |
| w30 | 13 | 0.009104 | -2.199 |
| w31 | 9 | -0.074183 | -8.741 |
| w32 | 11 | 0.002524 | -1.144 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 34 | -0.108847 | 8.549 |
| w15 | 19 | 0.057924 | 40.456 |
| w16 | 13 | -0.080763 | 117.329 |
| w17 | 15 | 0.013985 | -4.147 |
| w18 | 9 | -0.16936 | -8.821 |
| w19 | 4 | -0.028368 | -2.992 |
| w20 | 7 | -0.021553 | -5.593 |
| w21 | 16 | 0.031923 | 34.592 |
| w22 | 10 | -0.067478 | -4.542 |
| w23 | 9 | -0.034136 | -4.604 |
| w24 | 27 | 0.013988 | 21.412 |
| w25 | 15 | 0.097126 | 52.03 |
| w26 | 4 | -0.062325 | -1.55 |
| w27 | 15 | 0.208924 | 193.182 |
| w28 | 2 | -0.095782 | -1.055 |
| w29 | 27 | -0.130612 | -15.517 |
| w30 | 13 | 0.014366 | -2.178 |
| w31 | 6 | 0.099719 | 6.391 |
| w32 | 11 | -0.069279 | -15.411 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 12 | 0.242181 | 117.925 |
| w26 | 9 | 0.04526 | 4.991 |
| w27 | 25 | 0.011631 | 31.375 |
| w28 | 2 | -0.004015 | -0.939 |
| w29 | 18 | 0.059 | 10.016 |
| w30 | 0 | None | 0.0 |
| w31 | 13 | -0.074806 | -7.776 |
| w32 | 12 | 0.021782 | 4.941 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

