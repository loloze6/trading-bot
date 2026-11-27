# Backtest of 032-02.b1.e1.e1.e1.e2.e1_tight-ranges-break-out-further_1d

- Plan: `../../../../../03_test_plan/night7c_rangefail_run/plans/032-02.b1.e1.e1.e1.e2.e1_tight-ranges-break-out-further_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.015289 | 2.71 |
| w2 | 4 | 0.264651 | 57.53 |
| w3 | 6 | 0.086405 | 44.882 |
| w4 | 5 | 0.025617 | -4.397 |
| w5 | 3 | -0.010671 | 27.529 |
| w6 | 6 | 0.089658 | 72.394 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | 0.162857 | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 5 | 0.097014 | 11.574 |
| w11 | 6 | 0.149449 | 36.77 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | -0.056454 | -0.759 |
| w14 | 3 | -0.17279 | -2.543 |
| w15 | 6 | 0.14571 | 33.31 |
| w16 | 8 | -0.016243 | 1.12 |
| w17 | 0 | -0.047832 | 0.0 |
| w18 | 3 | -0.093239 | 2.135 |
| w19 | 2 | 0.014121 | -3.417 |
| w20 | 0 | 0.008016 | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 7 | 0.007215 | 27.456 |
| w23 | 0 | -0.145925 | 0.0 |
| w24 | 3 | 0.200333 | 7.187 |
| w25 | 9 | 0.009007 | 22.972 |
| w26 | 0 | None | 0.0 |
| w27 | 6 | -0.005261 | 13.885 |
| w28 | 2 | -0.082801 | -12.119 |
| w29 | 7 | -0.019296 | -8.248 |
| w30 | 1 | -0.040011 | -4.503 |
| w31 | 4 | -0.025451 | -4.672 |
| w32 | 3 | 0.074984 | 0.514 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.146081 | 0.771 |
| w2 | 2 | 0.0667 | -0.172 |
| w3 | 4 | -0.089636 | -3.245 |
| w4 | 3 | -0.052985 | 32.89 |
| w5 | 4 | -0.048337 | 1.892 |
| w6 | 4 | 0.032474 | 54.829 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | -0.069511 | 9.32 |
| w11 | 2 | 0.022434 | 0.067 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | -0.079312 | 0.0 |
| w14 | 2 | 0.028867 | 2.621 |
| w15 | 2 | -0.003311 | 4.14 |
| w16 | 7 | 0.103198 | 4.43 |
| w17 | 1 | -0.084689 | -10.059 |
| w18 | 2 | 0.06417 | -4.381 |
| w19 | 0 | None | 0.0 |
| w20 | 1 | -0.009839 | -2.573 |
| w21 | 0 | 0.096537 | 0.0 |
| w22 | 4 | -0.157762 | -0.738 |
| w23 | 0 | -0.094155 | 0.0 |
| w24 | 2 | -0.050886 | -0.328 |
| w25 | 3 | 0.036726 | -1.23 |
| w26 | 0 | None | 0.0 |
| w27 | 5 | 0.056541 | 23.183 |
| w28 | 1 | -0.165165 | -7.369 |
| w29 | 2 | 0.064168 | 4.809 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | -0.130065 | -8.993 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 4 | 0.120848 | 53.772 |
| w7 | 0 | 0.183945 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | -0.00113 | 0.0 |
| w10 | 2 | -0.116566 | -3.771 |
| w11 | 0 | 0.061377 | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | 0.053873 | 0.0 |
| w14 | 0 | 0.243997 | 0.0 |
| w15 | 3 | 0.120536 | 86.339 |
| w16 | 4 | 0.322268 | 48.535 |
| w17 | 0 | 0.04232 | 0.0 |
| w18 | 2 | 0.032805 | -9.431 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | -0.107154 | 2.899 |
| w22 | 4 | -0.103261 | -0.974 |
| w23 | 3 | -0.127651 | -8.364 |
| w24 | 3 | 0.19943 | 5.325 |
| w25 | 0 | -0.229981 | 0.0 |
| w26 | 0 | 0.001425 | 0.0 |
| w27 | 1 | -0.026071 | -6.877 |
| w28 | 2 | 0.032892 | -7.084 |
| w29 | 2 | 0.159619 | 1.819 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | 0.339623 | 0.0 |

- BCHUSD: 25 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w8 | 0 | 0.140541 | 0.0 |
| w9 | 0 | -0.01416 | 0.0 |
| w10 | 3 | 0.010093 | 28.83 |
| w11 | 4 | -0.15331 | -13.826 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | -0.077428 | 0.0 |
| w14 | 2 | 0.109961 | 2.47 |
| w15 | 2 | -0.089781 | -2.025 |
| w16 | 7 | 0.142056 | 5.54 |
| w17 | 1 | -0.15657 | -2.603 |
| w18 | 1 | -0.200926 | -1.905 |
| w19 | 0 | -0.045428 | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 3 | -0.018938 | 3.07 |
| w23 | 0 | 0.070948 | 0.0 |
| w24 | 3 | -0.180246 | -1.89 |
| w25 | 3 | 0.168306 | 5.063 |
| w26 | 0 | None | 0.0 |
| w27 | 4 | 0.036623 | 4.256 |
| w28 | 0 | None | 0.0 |
| w29 | 3 | -0.184696 | 14.716 |
| w30 | 2 | -0.137819 | -5.12 |
| w31 | 1 | -0.057365 | -1.349 |
| w32 | 0 | -0.075977 | 0.0 |

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
| w1 | 6 | 0.131815 | 85.384 |
| w2 | 4 | -0.007758 | -2.44 |
| w3 | 0 | None | 0.0 |
| w4 | 6 | 0.265567 | 72.746 |
| w5 | 9 | 0.263769 | 161.06 |
| w6 | 8 | 0.20667 | 52.694 |
| w7 | 2 | 0.189544 | 1.488 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 3 | -0.237289 | -5.243 |
| w11 | 4 | 0.121982 | 11.676 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | 0.022376 | 0.0 |
| w14 | 8 | 0.183015 | 35.668 |
| w15 | 5 | 0.044399 | 11.899 |
| w16 | 4 | 0.038111 | 64.543 |
| w17 | 2 | 0.070316 | -4.407 |
| w18 | 2 | -0.049058 | -0.583 |
| w19 | 3 | 0.032144 | -2.042 |
| w20 | 0 | 0.044098 | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 7 | -0.140835 | 16.665 |
| w23 | 1 | -0.140053 | -1.569 |
| w24 | 1 | -0.063036 | -2.562 |
| w25 | 5 | 0.011272 | 10.565 |
| w26 | 0 | -0.010692 | 0.0 |
| w27 | 2 | -0.046887 | 4.446 |
| w28 | 0 | None | 0.0 |
| w29 | 3 | 0.090776 | 25.295 |
| w30 | 0 | None | 0.0 |
| w31 | 2 | -0.080123 | -5.597 |
| w32 | 0 | 0.157361 | 0.0 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 3 | 0.072728 | 22.834 |
| w11 | 3 | -0.179815 | -10.889 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | -0.044264 | 0.0 |
| w14 | 5 | -0.064093 | 29.653 |
| w15 | 4 | 0.037563 | 3.765 |
| w16 | 11 | 0.029403 | 29.859 |
| w17 | 4 | 0.058811 | 2.354 |
| w18 | 0 | -0.049018 | 0.0 |
| w19 | 0 | -0.061703 | 0.0 |
| w20 | 0 | 0.028768 | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | 0.033393 | -1.338 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | 0.159314 | 0.0 |
| w25 | 3 | 0.044712 | -0.011 |
| w26 | 0 | None | 0.0 |
| w27 | 3 | 0.339604 | 32.242 |
| w28 | 0 | -0.268701 | 0.0 |
| w29 | 2 | 0.044266 | -0.263 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | -0.020054 | 0.0 |

- ATOMUSD: 20 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 3 | 0.077048 | -12.561 |
| w14 | 7 | 0.088645 | 3.447 |
| w15 | 1 | None | -0.03 |
| w16 | 3 | -0.071166 | -7.504 |
| w17 | 3 | 0.048032 | -9.365 |
| w18 | 2 | -0.125452 | 3.364 |
| w19 | 0 | -0.074757 | 0.0 |
| w20 | 2 | 0.062499 | -0.801 |
| w21 | 2 | 0.098723 | -0.167 |
| w22 | 0 | -0.179019 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | -0.137759 | 0.0 |
| w25 | 2 | 0.020559 | 0.611 |
| w26 | 0 | None | 0.0 |
| w27 | 3 | -0.014997 | 24.457 |
| w28 | 0 | None | 0.0 |
| w29 | 1 | -0.033759 | -3.807 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | -0.039368 | 0.0 |
| w32 | 2 | 0.017174 | -0.875 |

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
| w15 | 0 | -0.063852 | 0.0 |
| w16 | 5 | -0.094148 | 5.906 |
| w17 | 0 | -0.007606 | 0.0 |
| w18 | 0 | -0.006082 | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 4 | 0.030919 | -7.539 |
| w22 | 0 | -0.182014 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | 0.103974 | 10.975 |
| w25 | 2 | 0.036274 | 1.524 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | 0.106474 | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | 0.124917 | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | 0.261577 | 0.0 |
| w32 | 0 | -0.06083 | 0.0 |

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
| w15 | 3 | -0.101153 | -4.189 |
| w16 | 5 | 0.173264 | 29.375 |
| w17 | 0 | 0.053326 | 0.0 |
| w18 | 3 | -0.157593 | -9.429 |
| w19 | 2 | 0.012095 | -4.524 |
| w20 | 1 | -0.225105 | -3.246 |
| w21 | 0 | None | 0.0 |
| w22 | 4 | -0.195979 | 5.77 |
| w23 | 7 | 0.015559 | -7.732 |
| w24 | 5 | -0.018296 | 12.504 |
| w25 | 4 | 0.076488 | 15.851 |
| w26 | 4 | 0.137099 | 12.055 |
| w27 | 9 | 0.103577 | 148.064 |
| w28 | 1 | -0.032227 | -0.791 |
| w29 | 6 | -0.085823 | 28.573 |
| w30 | 0 | None | 0.0 |
| w31 | 4 | -0.05708 | 0.007 |
| w32 | 7 | 0.096614 | -17.505 |

- DOTUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 1 | -0.093155 | -4.53 |
| w18 | 2 | -0.091596 | 1.177 |
| w19 | 0 | 0.01097 | 0.0 |
| w20 | 0 | -0.06692 | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | -0.19958 | 0.0 |
| w23 | 0 | -0.05533 | 0.0 |
| w24 | 1 | -0.021927 | -0.389 |
| w25 | 3 | 0.052727 | 1.912 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | 0.088227 | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | 0.133954 | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | -0.058308 | 0.0 |

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
| w20 | 0 | 0.019574 | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 1 | -0.206727 | -5.54 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | 0.015658 | -1.51 |
| w25 | 3 | 0.018118 | 4.615 |
| w26 | 0 | None | 0.0 |
| w27 | 3 | 0.16775 | 8.467 |
| w28 | 0 | None | 0.0 |
| w29 | 3 | -0.006652 | -2.332 |
| w30 | 2 | 0.050735 | -1.287 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | 0.10041 | -0.373 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 0 | -0.263845 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | 0.030471 | 2.126 |
| w25 | 3 | -0.073229 | 25.844 |
| w26 | 1 | -0.098582 | -8.678 |
| w27 | 2 | -0.064724 | -0.738 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | -0.208365 | 0.0 |
| w30 | 1 | -0.025683 | -1.95 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | 0.037747 | 12.126 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 1 | -0.071067 | 0.574 |
| w25 | 3 | -0.055438 | -14.73 |
| w26 | 0 | -0.075092 | 0.0 |
| w27 | 7 | 0.011741 | 7.29 |
| w28 | 2 | 0.05189 | -3.333 |
| w29 | 2 | -0.109364 | -0.892 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | -0.154418 | 0.0 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 7 | 0.370766 | 69.072 |
| w6 | 3 | -0.028714 | 11.733 |
| w7 | 1 | -0.10006 | -3.052 |
| w8 | 0 | -0.108311 | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | 0.021783 | 0.0 |
| w11 | 2 | -0.082701 | 0.326 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | 0.121872 | 0.0 |
| w14 | 5 | -0.030567 | 22.496 |
| w15 | 1 | 0.001834 | -1.454 |
| w16 | 5 | 0.071127 | 8.072 |
| w17 | 2 | 0.054457 | -10.193 |
| w18 | 0 | -0.128505 | 0.0 |
| w19 | 0 | 0.009075 | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 3 | -0.089766 | -12.028 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | -0.162317 | 3.888 |
| w25 | 0 | 0.010583 | 0.0 |
| w26 | 0 | -0.047767 | 0.0 |
| w27 | 0 | 0.072365 | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 1 | 0.066677 | 0.803 |
| w30 | 0 | 0.068067 | 0.0 |
| w31 | 0 | 0.139083 | 0.0 |
| w32 | 2 | 0.156575 | 1.793 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 9 | 0.170721 | 65.271 |
| w6 | 0 | -0.011482 | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | 0.123321 | 8.299 |
| w11 | 4 | 0.041474 | 1.93 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | 0.054901 | 0.0 |
| w14 | 9 | -0.210249 | 19.378 |
| w15 | 5 | -0.171025 | 14.582 |
| w16 | 6 | -0.088431 | 13.471 |
| w17 | 1 | -0.033931 | -12.782 |
| w18 | 0 | None | 0.0 |
| w19 | 1 | -0.01855 | -0.306 |
| w20 | 1 | -0.039123 | -1.362 |
| w21 | 0 | None | 0.0 |
| w22 | 4 | -0.011222 | -3.086 |
| w23 | 0 | -0.009865 | 0.0 |
| w24 | 8 | -0.095672 | -7.705 |
| w25 | 0 | None | 0.0 |
| w26 | 4 | 0.026235 | 5.509 |
| w27 | 4 | 0.010494 | 0.571 |
| w28 | 6 | -0.066907 | -1.971 |
| w29 | 0 | 0.17789 | 0.0 |
| w30 | 4 | -0.129117 | 8.341 |
| w31 | 3 | 0.079591 | -3.011 |
| w32 | 3 | -0.051035 | 3.246 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 0 | -0.059509 | 0.0 |
| w18 | 3 | -0.009786 | -0.117 |
| w19 | 1 | -0.082229 | -9.189 |
| w20 | 0 | -0.046731 | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | -0.202628 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | -0.09705 | -1.174 |
| w25 | 0 | -0.061711 | 0.0 |
| w26 | 0 | -0.029171 | 0.0 |
| w27 | 0 | 0.068448 | 0.0 |
| w28 | 0 | -0.074274 | 0.0 |
| w29 | 2 | -0.085478 | -3.383 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | 0.184378 | 5.378 |

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
| w17 | 2 | -0.313025 | -4.635 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | -0.026237 | 0.0 |
| w20 | 0 | -0.058788 | 0.0 |
| w21 | 0 | -0.106451 | 0.0 |
| w22 | 0 | 0.03827 | 0.0 |
| w23 | 0 | -0.024822 | 0.0 |
| w24 | 2 | -0.046784 | 0.294 |
| w25 | 0 | -0.013504 | 0.0 |
| w26 | 2 | 0.121155 | 0.648 |
| w27 | 6 | 0.016428 | 20.671 |
| w28 | 0 | None | 0.0 |
| w29 | 5 | -0.049504 | -15.667 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | 0.078671 | 0.315 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 0 | None | 0.0 |
| w20 | 0 | 0.082042 | 0.0 |
| w21 | 2 | 0.008431 | -4.476 |
| w22 | 4 | 0.082552 | 18.107 |
| w23 | 2 | 0.119921 | 1.511 |
| w24 | 1 | 0.079082 | 8.274 |
| w25 | 2 | -0.139813 | -6.688 |
| w26 | 0 | -0.125573 | 0.0 |
| w27 | 2 | -0.033423 | -2.365 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | -0.148179 | -2.832 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | 0.082494 | 0.0 |
| w32 | 0 | -0.032488 | 0.0 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 1 | -0.217718 | -1.409 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | -0.168227 | -1.661 |
| w25 | 3 | 0.060612 | 0.859 |
| w26 | 0 | None | 0.0 |
| w27 | 2 | 0.047461 | 1.616 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | 0.068559 | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | 0.129111 | 0.0 |
| w32 | 0 | -0.11707 | 0.0 |

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
| w27 | 3 | 0.06829 | 22.506 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | 0.023585 | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 3 | 0.147955 | 5.899 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 0 | -0.065486 | 0.0 |
| w18 | 0 | 0.188174 | 0.0 |
| w19 | 0 | 0.048919 | 0.0 |
| w20 | 0 | -0.135553 | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | -0.065407 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | -0.105206 | 7.732 |
| w25 | 3 | -0.012666 | -3.49 |
| w26 | 0 | None | 0.0 |
| w27 | 2 | 0.077093 | 10.932 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | -0.20983 | 0.0 |
| w30 | 0 | -0.119434 | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | -0.163405 | 0.0 |

- GRTUSD: 15 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w18 | 1 | -0.106925 | -0.378 |
| w19 | 0 | 0.003095 | 0.0 |
| w20 | 0 | -0.050937 | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | 0.033609 | 9.995 |
| w23 | 0 | -0.136613 | 0.0 |
| w24 | 1 | -0.078315 | -0.576 |
| w25 | 3 | -0.016554 | -0.132 |
| w26 | 0 | None | 0.0 |
| w27 | 2 | -0.03131 | 6.305 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | 0.031283 | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | -0.111122 | 0.0 |

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
| w28 | 0 | 0.019853 | 0.0 |
| w29 | 1 | -0.120661 | -2.09 |
| w30 | 0 | -0.04069 | 0.0 |
| w31 | 0 | 0.177937 | 0.0 |
| w32 | 0 | -0.138852 | 0.0 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 3 | -0.006872 | -2.97 |
| w15 | 2 | 0.107081 | 5.449 |
| w16 | 1 | 0.084901 | 198.701 |
| w17 | 0 | 0.133793 | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | -0.330092 | 0.0 |
| w20 | 2 | 0.017715 | -2.038 |
| w21 | 0 | 0.371821 | 0.0 |
| w22 | 0 | -0.0247 | 0.0 |
| w23 | 0 | 0.185612 | 0.0 |
| w24 | 0 | -0.061944 | 0.0 |
| w25 | 0 | 0.377345 | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 4 | 0.221195 | 14.915 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | 0.194093 | 0.0 |
| w30 | 2 | 0.039053 | -1.803 |
| w31 | 1 | 0.0561 | 0.515 |
| w32 | 1 | 0.023205 | -2.907 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 0 | 0.384651 | 0.0 |
| w26 | 3 | 0.113377 | 7.766 |
| w27 | 4 | 0.243233 | 7.21 |
| w28 | 0 | -0.022416 | 0.0 |
| w29 | 2 | -0.151252 | -6.124 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | -0.036601 | 0.0 |
| w32 | 3 | 0.135788 | -2.351 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

