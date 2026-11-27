# Backtest of 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins_1d

- Plan: `../../../../../03_test_plan/night4_range_run/plans/023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 38 | -0.051141 | -3.0 |
| w2 | 28 | 0.200291 | 70.916 |
| w3 | 63 | -0.159983 | 53.062 |
| w4 | 20 | 0.019795 | -21.831 |
| w5 | 28 | 0.048096 | 67.899 |
| w6 | 27 | 0.095358 | 79.262 |
| w7 | 32 | -0.087426 | -12.191 |
| w8 | 16 | 0.049048 | -4.899 |
| w9 | 34 | -0.030107 | -7.289 |
| w10 | 46 | 0.056142 | 22.323 |
| w11 | 25 | 0.064927 | 47.633 |
| w12 | 39 | -0.03545 | 1.959 |
| w13 | 30 | 0.049459 | 15.99 |
| w14 | 28 | -0.046319 | 10.386 |
| w15 | 32 | 0.113189 | 138.072 |
| w16 | 13 | 0.033379 | 33.046 |
| w17 | 31 | 0.077285 | 19.953 |
| w18 | 14 | -0.005852 | -3.406 |
| w19 | 40 | -0.117328 | -14.734 |
| w20 | 27 | 0.025523 | 2.577 |
| w21 | 20 | -0.091679 | -38.478 |
| w22 | 44 | -0.021586 | 65.903 |
| w23 | 18 | 0.044824 | -13.765 |
| w24 | 46 | 0.050334 | 62.625 |
| w25 | 22 | 0.106118 | 44.403 |
| w26 | 40 | -0.089386 | -18.706 |
| w27 | 49 | -0.074969 | 36.09 |
| w28 | 17 | 0.039142 | 5.314 |
| w29 | 33 | -0.014955 | -0.888 |
| w30 | 16 | 0.004694 | 0.898 |
| w31 | 27 | -0.022891 | -13.599 |
| w32 | 34 | 0.078283 | -18.808 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 52 | -0.022736 | 8.278 |
| w2 | 38 | -0.006572 | 1.047 |
| w3 | 50 | -0.114812 | -21.44 |
| w4 | 22 | 0.167214 | 90.511 |
| w5 | 17 | 0.081438 | 30.143 |
| w6 | 23 | 0.072289 | 92.545 |
| w7 | 24 | -0.052612 | -7.543 |
| w8 | 34 | -0.083555 | -11.745 |
| w9 | 47 | -0.044525 | 20.268 |
| w10 | 49 | -0.190317 | -20.44 |
| w11 | 25 | 0.010224 | 6.141 |
| w12 | 43 | -0.030868 | 3.846 |
| w13 | 25 | 0.076991 | 28.666 |
| w14 | 55 | -0.124519 | -5.656 |
| w15 | 27 | -0.034366 | 27.967 |
| w16 | 18 | 0.023902 | 13.211 |
| w17 | 33 | 0.070519 | 5.56 |
| w18 | 12 | 0.188609 | 2.144 |
| w19 | 40 | -0.100253 | -22.588 |
| w20 | 25 | 0.037977 | 20.14 |
| w21 | 25 | -0.047513 | -6.461 |
| w22 | 28 | -0.145866 | -11.96 |
| w23 | 13 | -0.264123 | -35.611 |
| w24 | 34 | -0.123156 | -30.977 |
| w25 | 24 | 0.044553 | 12.032 |
| w26 | 39 | -0.035515 | 18.699 |
| w27 | 41 | -0.073484 | 19.996 |
| w28 | 12 | -0.183866 | -19.998 |
| w29 | 25 | 0.024399 | 27.641 |
| w30 | 29 | -0.159252 | -4.735 |
| w31 | 48 | -0.045294 | 25.472 |
| w32 | 37 | -0.044417 | -45.781 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 19 | 0.226367 | 63.543 |
| w7 | 20 | 0.038803 | 2.315 |
| w8 | 27 | -0.064335 | -7.49 |
| w9 | 22 | 0.047559 | -31.288 |
| w10 | 48 | -0.145323 | -23.753 |
| w11 | 19 | -0.056716 | -12.692 |
| w12 | 33 | -0.01335 | 5.14 |
| w13 | 22 | 0.076054 | 27.834 |
| w14 | 40 | 0.031002 | 35.495 |
| w15 | 21 | 0.160147 | 200.25 |
| w16 | 13 | 0.111937 | 75.477 |
| w17 | 21 | 0.131202 | 28.437 |
| w18 | 11 | -0.057511 | -9.264 |
| w19 | 39 | -0.127821 | -30.042 |
| w20 | 6 | 0.050374 | -2.176 |
| w21 | 16 | 0.028276 | 16.55 |
| w22 | 34 | -0.138929 | -21.747 |
| w23 | 19 | -0.121594 | -20.809 |
| w24 | 17 | 0.077721 | -0.675 |
| w25 | 31 | -0.002555 | 1.493 |
| w26 | 39 | 3.4e-05 | -1.889 |
| w27 | 16 | 0.44602 | 224.938 |
| w28 | 16 | -0.003667 | -4.708 |
| w29 | 10 | 0.14786 | 43.852 |
| w30 | 40 | 0.01123 | -1.304 |
| w31 | 49 | -0.16956 | -44.979 |
| w32 | 41 | 0.02668 | -30.937 |

- BCHUSD: 25 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w8 | 28 | 0.014873 | 0.529 |
| w9 | 32 | -0.107169 | -24.967 |
| w10 | 54 | 0.04298 | 36.104 |
| w11 | 14 | -0.064365 | -9.353 |
| w12 | 29 | 0.02889 | -43.237 |
| w13 | 26 | 0.069283 | 40.487 |
| w14 | 47 | -0.191819 | -24.779 |
| w15 | 27 | -0.12874 | -20.663 |
| w16 | 15 | 0.066729 | 38.951 |
| w17 | 31 | -0.018244 | -0.635 |
| w18 | 10 | 0.010687 | -19.255 |
| w19 | 37 | -0.049569 | -31.309 |
| w20 | 17 | 0.003173 | 0.964 |
| w21 | 56 | -0.169204 | -7.568 |
| w22 | 31 | -0.005175 | -23.852 |
| w23 | 39 | 0.183833 | -30.693 |
| w24 | 24 | -0.079656 | 3.805 |
| w25 | 27 | 0.131592 | 39.555 |
| w26 | 40 | -0.071066 | -12.847 |
| w27 | 57 | -0.127427 | -26.216 |
| w28 | 35 | -0.112768 | -28.59 |
| w29 | 38 | -0.149417 | 4.117 |
| w30 | 32 | -0.154443 | -27.626 |
| w31 | 32 | -0.082445 | -14.971 |
| w32 | 37 | -0.029441 | -4.023 |

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
| w1 | 29 | 0.16723 | 201.416 |
| w2 | 25 | 0.01796 | -2.328 |
| w3 | 23 | 0.011559 | 0.57 |
| w4 | 44 | 0.096858 | 227.269 |
| w5 | 18 | 0.219849 | 144.419 |
| w6 | 26 | 0.069861 | 61.276 |
| w7 | 18 | 0.114813 | 3.287 |
| w8 | 24 | 0.088693 | 19.95 |
| w9 | 39 | -0.051458 | 9.279 |
| w10 | 31 | -0.1318 | -21.018 |
| w11 | 22 | 0.006145 | 24.474 |
| w12 | 46 | -0.036629 | -10.493 |
| w13 | 22 | 0.054028 | 41.882 |
| w14 | 35 | -0.072343 | 71.293 |
| w15 | 25 | 0.002886 | -5.382 |
| w16 | 33 | 0.015129 | 107.114 |
| w17 | 33 | 0.077804 | 42.57 |
| w18 | 12 | -0.060031 | -4.815 |
| w19 | 30 | -0.031279 | -15.792 |
| w20 | 17 | 0.129104 | 27.723 |
| w21 | 24 | -0.06687 | -15.884 |
| w22 | 47 | -0.123617 | 16.461 |
| w23 | 19 | -0.087934 | -25.277 |
| w24 | 47 | 0.013096 | 7.998 |
| w25 | 22 | 0.106533 | 33.846 |
| w26 | 23 | -0.002419 | -2.763 |
| w27 | 50 | -0.079663 | 11.753 |
| w28 | 17 | 0.010723 | 18.52 |
| w29 | 40 | 0.111558 | 75.507 |
| w30 | 16 | -0.007004 | 1.927 |
| w31 | 35 | -0.033919 | -17.307 |
| w32 | 34 | 0.097561 | 36.562 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 45 | -0.014684 | 32.92 |
| w11 | 15 | -0.152303 | -16.433 |
| w12 | 62 | -0.04355 | 14.71 |
| w13 | 22 | 0.069442 | 36.136 |
| w14 | 31 | -0.118834 | 36.611 |
| w15 | 33 | 0.01854 | -23.662 |
| w16 | 35 | 0.143465 | 63.249 |
| w17 | 26 | 0.07083 | 38.309 |
| w18 | 20 | 0.030058 | 13.714 |
| w19 | 37 | -0.024808 | -24.868 |
| w20 | 35 | -0.025106 | -10.241 |
| w21 | 30 | -0.077031 | 5.737 |
| w22 | 33 | -0.122268 | -15.195 |
| w23 | 28 | -0.07719 | -5.902 |
| w24 | 46 | 0.099432 | 109.685 |
| w25 | 14 | 0.055535 | -4.752 |
| w26 | 44 | -0.10887 | -19.195 |
| w27 | 29 | 0.165493 | 56.955 |
| w28 | 7 | -0.262583 | -24.429 |
| w29 | 19 | 0.094796 | 21.313 |
| w30 | 11 | 0.01939 | 13.827 |
| w31 | 59 | -0.190255 | -12.463 |
| w32 | 33 | 0.096301 | 13.719 |

- ATOMUSD: 20 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 17 | -0.027938 | -21.18 |
| w14 | 38 | -0.097038 | 33.173 |
| w15 | 35 | -0.114891 | -18.072 |
| w16 | 21 | 0.087066 | 24.732 |
| w17 | 26 | 0.026005 | 19.006 |
| w18 | 11 | -0.133523 | 34.185 |
| w19 | 27 | -0.017793 | 2.098 |
| w20 | 31 | 0.066667 | 23.337 |
| w21 | 23 | 0.024459 | -6.574 |
| w22 | 27 | -0.090527 | 18.425 |
| w23 | 54 | -0.013175 | 36.17 |
| w24 | 44 | -0.108945 | 8.641 |
| w25 | 10 | 0.054459 | -7.946 |
| w26 | 38 | 0.034471 | 46.742 |
| w27 | 53 | -0.020267 | -5.717 |
| w28 | 30 | -0.104315 | -20.787 |
| w29 | 16 | -0.020241 | -12.009 |
| w30 | 24 | 0.082101 | 38.488 |
| w31 | 41 | -0.082514 | -32.757 |
| w32 | 30 | -0.094246 | -29.635 |

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
| w15 | 32 | -0.147434 | -23.786 |
| w16 | 23 | 0.135408 | 70.368 |
| w17 | 28 | 0.001594 | -3.082 |
| w18 | 9 | -0.019255 | -5.728 |
| w19 | 32 | -0.047905 | -6.301 |
| w20 | 37 | 0.015934 | -2.736 |
| w21 | 11 | -0.128686 | -37.152 |
| w22 | 27 | -0.055138 | -12.8 |
| w23 | 43 | -0.006704 | 8.098 |
| w24 | 59 | -0.015284 | 22.524 |
| w25 | 10 | 0.06598 | -2.879 |
| w26 | 52 | -0.081714 | -22.062 |
| w27 | 39 | 0.064556 | 87.749 |
| w28 | 25 | 0.034454 | 3.977 |
| w29 | 9 | 0.162257 | 31.185 |
| w30 | 26 | 0.00753 | 29.352 |
| w31 | 47 | -0.020909 | -40.205 |
| w32 | 26 | -0.135079 | -28.96 |

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
| w15 | 16 | -0.106134 | 3.773 |
| w16 | 26 | 0.130065 | 60.987 |
| w17 | 27 | 0.060607 | 2.479 |
| w18 | 10 | -0.07781 | -14.917 |
| w19 | 35 | -0.020314 | -5.633 |
| w20 | 24 | -0.249066 | -25.791 |
| w21 | 21 | -0.022222 | -3.012 |
| w22 | 35 | -0.090415 | -7.576 |
| w23 | 32 | -0.024941 | -13.519 |
| w24 | 36 | -0.043048 | 15.246 |
| w25 | 32 | 0.125696 | 25.212 |
| w26 | 34 | -0.045333 | -7.418 |
| w27 | 23 | 0.151375 | 123.657 |
| w28 | 48 | -0.062997 | -12.93 |
| w29 | 47 | -0.053491 | 12.574 |
| w30 | 26 | 0.025051 | 6.017 |
| w31 | 27 | 0.075368 | 20.934 |
| w32 | 31 | 0.051597 | -3.445 |

- DOTUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 14 | 0.032363 | -13.13 |
| w18 | 19 | -0.193982 | -9.927 |
| w19 | 43 | -0.025647 | -18.296 |
| w20 | 26 | 0.026244 | -0.634 |
| w21 | 37 | -0.098888 | -25.67 |
| w22 | 34 | -0.02863 | -9.373 |
| w23 | 33 | -0.093186 | -18.994 |
| w24 | 32 | 0.046995 | 25.568 |
| w25 | 10 | 0.08845 | 8.444 |
| w26 | 44 | -0.081888 | -9.436 |
| w27 | 53 | 0.095843 | 6.178 |
| w28 | 40 | -0.104794 | -3.965 |
| w29 | 25 | 0.070486 | -2.139 |
| w30 | 20 | -0.037454 | -30.692 |
| w31 | 46 | -0.125362 | -32.757 |
| w32 | 48 | -0.101549 | -5.188 |

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
| w20 | 15 | 0.096732 | 14.282 |
| w21 | 29 | -0.120438 | -33.305 |
| w22 | 29 | -0.129283 | -32.983 |
| w23 | 22 | -0.058662 | -10.715 |
| w24 | 38 | 0.181734 | 116.096 |
| w25 | 15 | 0.041967 | 20.57 |
| w26 | 41 | -0.106384 | -9.814 |
| w27 | 35 | 0.027193 | 54.077 |
| w28 | 31 | -0.006572 | 3.98 |
| w29 | 22 | 0.020002 | -11.181 |
| w30 | 14 | 0.075907 | 13.674 |
| w31 | 50 | -0.200956 | -26.174 |
| w32 | 45 | 0.031868 | -19.431 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 28 | -0.133305 | -36.446 |
| w23 | 39 | 0.05061 | 33.049 |
| w24 | 44 | 0.055168 | 118.241 |
| w25 | 13 | 0.091381 | 40.563 |
| w26 | 18 | -0.046312 | -11.468 |
| w27 | 21 | -0.051653 | 34.19 |
| w28 | 32 | -0.08716 | 2.617 |
| w29 | 23 | 0.076235 | -22.325 |
| w30 | 14 | -0.15013 | -28.618 |
| w31 | 46 | -0.08228 | -21.7 |
| w32 | 30 | -0.03788 | 6.356 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 48 | 0.00717 | 6.013 |
| w25 | 20 | -0.067133 | 0.423 |
| w26 | 33 | 0.010778 | -7.761 |
| w27 | 28 | -0.008897 | 55.084 |
| w28 | 24 | 0.105648 | 1.959 |
| w29 | 14 | -0.069266 | -7.437 |
| w30 | 23 | 0.016321 | -3.247 |
| w31 | 25 | -0.122438 | -36.634 |
| w32 | 31 | -0.0364 | -33.395 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 22 | 0.163912 | 130.445 |
| w6 | 16 | -0.010343 | 13.222 |
| w7 | 21 | -0.014991 | -4.412 |
| w8 | 20 | -0.052077 | -27.266 |
| w9 | 35 | -0.067449 | -17.429 |
| w10 | 51 | -0.057729 | 4.877 |
| w11 | 21 | -0.052409 | 2.9 |
| w12 | 42 | -0.021498 | 11.378 |
| w13 | 27 | 0.062001 | 57.071 |
| w14 | 34 | -0.129032 | 21.434 |
| w15 | 29 | -0.072666 | -14.272 |
| w16 | 17 | 0.104131 | 30.507 |
| w17 | 28 | 0.023803 | -5.183 |
| w18 | 24 | -0.132228 | -26.81 |
| w19 | 31 | -0.014603 | -18.0 |
| w20 | 27 | 0.025983 | 2.033 |
| w21 | 34 | -0.095609 | -8.289 |
| w22 | 29 | -0.230098 | -35.636 |
| w23 | 33 | -0.075757 | -20.38 |
| w24 | 40 | -0.129238 | -12.936 |
| w25 | 16 | 0.053236 | 0.015 |
| w26 | 35 | -0.01982 | 2.56 |
| w27 | 26 | -0.01672 | 31.362 |
| w28 | 26 | -0.13518 | -28.969 |
| w29 | 31 | -0.096188 | -7.065 |
| w30 | 22 | 0.147848 | 306.125 |
| w31 | 31 | 0.144818 | 25.673 |
| w32 | 27 | 0.107584 | -11.655 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 18 | 0.146959 | 133.305 |
| w6 | 20 | 0.121276 | 108.893 |
| w7 | 14 | -0.123934 | -14.851 |
| w8 | 37 | -0.033328 | 0.186 |
| w9 | 36 | -0.050002 | -0.994 |
| w10 | 49 | -0.036218 | 2.969 |
| w11 | 15 | 0.062581 | 11.479 |
| w12 | 56 | -0.032195 | -4.784 |
| w13 | 25 | 0.035753 | 16.505 |
| w14 | 40 | -0.249067 | 16.556 |
| w15 | 25 | -0.079149 | 12.004 |
| w16 | 23 | -0.051292 | 3.489 |
| w17 | 29 | 0.028052 | 0.124 |
| w18 | 17 | -0.257993 | -16.119 |
| w19 | 45 | -0.081951 | -5.867 |
| w20 | 20 | 0.020513 | 0.458 |
| w21 | 29 | -0.14569 | -35.578 |
| w22 | 22 | -0.001269 | 7.21 |
| w23 | 24 | -0.005936 | -3.106 |
| w24 | 36 | -0.022854 | 9.273 |
| w25 | 36 | -0.064088 | -10.916 |
| w26 | 29 | -0.047179 | -0.462 |
| w27 | 36 | -0.030523 | -2.997 |
| w28 | 19 | 0.039071 | 19.015 |
| w29 | 33 | 0.180279 | 37.677 |
| w30 | 51 | -0.082526 | -19.82 |
| w31 | 21 | 0.054218 | 21.486 |
| w32 | 28 | 0.056887 | 48.545 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 33 | -0.025737 | -0.786 |
| w18 | 19 | -0.150694 | 6.265 |
| w19 | 31 | -0.100398 | -25.449 |
| w20 | 22 | 0.049739 | -1.397 |
| w21 | 30 | -0.193215 | -40.088 |
| w22 | 27 | -0.093764 | -2.713 |
| w23 | 27 | -0.094397 | -10.233 |
| w24 | 31 | -0.185158 | -30.907 |
| w25 | 11 | 0.062324 | 2.168 |
| w26 | 38 | -0.02604 | -12.465 |
| w27 | 29 | 0.230506 | 124.795 |
| w28 | 23 | -0.031135 | -3.82 |
| w29 | 17 | 0.021184 | 1.519 |
| w30 | 35 | -0.020744 | 9.321 |
| w31 | 38 | -0.163337 | -19.72 |
| w32 | 31 | 0.084526 | 12.938 |

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
| w17 | 24 | -0.039107 | -16.282 |
| w18 | 24 | -0.046653 | 0.335 |
| w19 | 30 | 0.001789 | -10.39 |
| w20 | 27 | -0.00542 | -7.395 |
| w21 | 11 | -0.015787 | -27.398 |
| w22 | 33 | -0.039655 | -6.218 |
| w23 | 29 | -0.077012 | -7.079 |
| w24 | 44 | -0.133753 | -7.67 |
| w25 | 9 | 0.026238 | -1.202 |
| w26 | 47 | -0.047203 | -1.278 |
| w27 | 29 | 0.015413 | 11.143 |
| w28 | 16 | -0.025943 | 1.19 |
| w29 | 33 | 0.03456 | -1.706 |
| w30 | 25 | -0.140576 | -1.259 |
| w31 | 51 | -0.191869 | -14.007 |
| w32 | 34 | -0.035205 | -16.118 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 44 | -0.115275 | -34.067 |
| w20 | 30 | 0.136838 | 49.836 |
| w21 | 13 | 0.005419 | -6.314 |
| w22 | 28 | 0.051099 | 54.627 |
| w23 | 15 | 0.019837 | 2.65 |
| w24 | 37 | 0.072889 | 204.459 |
| w25 | 12 | -0.092631 | -13.566 |
| w26 | 20 | -0.021248 | -7.425 |
| w27 | 31 | -0.077632 | 0.948 |
| w28 | 23 | -0.026248 | 9.155 |
| w29 | 18 | -0.041725 | -16.071 |
| w30 | 18 | 0.02998 | 18.615 |
| w31 | 46 | -0.111574 | -0.802 |
| w32 | 26 | -0.044615 | 18.815 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 18 | -0.047075 | 5.868 |
| w23 | 40 | -0.1498 | -27.423 |
| w24 | 43 | -0.22238 | -43.902 |
| w25 | 17 | 0.024243 | -20.131 |
| w26 | 41 | -0.021028 | 22.042 |
| w27 | 52 | -0.090404 | -18.915 |
| w28 | 9 | -0.001472 | 4.817 |
| w29 | 19 | 0.170776 | -1.205 |
| w30 | 23 | -0.013009 | 5.341 |
| w31 | 32 | 0.045662 | 7.964 |
| w32 | 18 | 0.038779 | -1.843 |

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
| w27 | 42 | -0.04848 | 15.295 |
| w28 | 29 | 0.03005 | 3.503 |
| w29 | 9 | 0.142426 | 21.557 |
| w30 | 20 | 0.028692 | 7.558 |
| w31 | 57 | -0.112391 | -16.405 |
| w32 | 16 | 0.107218 | 8.922 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 21 | 0.039779 | 4.898 |
| w18 | 27 | 0.114355 | 59.554 |
| w19 | 40 | 0.005181 | 9.176 |
| w20 | 30 | 0.175909 | -9.459 |
| w21 | 28 | -0.190025 | -26.656 |
| w22 | 21 | -0.147129 | -28.746 |
| w23 | 38 | -0.05248 | -3.444 |
| w24 | 43 | -0.036149 | 14.91 |
| w25 | 11 | 0.022039 | -20.106 |
| w26 | 39 | -0.105186 | -26.631 |
| w27 | 51 | -0.030068 | -15.211 |
| w28 | 37 | -0.080745 | 1.689 |
| w29 | 14 | 0.066279 | 0.282 |
| w30 | 20 | -0.181358 | -50.978 |
| w31 | 43 | -0.125652 | -13.663 |
| w32 | 24 | 0.008748 | 17.74 |

- GRTUSD: 15 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w18 | 13 | -0.118993 | -17.645 |
| w19 | 35 | -0.033963 | -7.786 |
| w20 | 29 | 0.065997 | -5.455 |
| w21 | 29 | -0.042681 | 3.063 |
| w22 | 32 | 0.030949 | 80.623 |
| w23 | 32 | -0.291212 | -43.379 |
| w24 | 41 | -0.003522 | 0.92 |
| w25 | 16 | 0.103045 | 34.399 |
| w26 | 36 | -0.042992 | -8.186 |
| w27 | 30 | -0.059514 | 55.65 |
| w28 | 27 | -0.0875 | 3.408 |
| w29 | 16 | 0.032179 | -8.558 |
| w30 | 29 | 0.048453 | 31.604 |
| w31 | 53 | -0.166134 | -16.491 |
| w32 | 25 | -0.085994 | -33.495 |

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
| w28 | 33 | 0.011921 | -7.412 |
| w29 | 16 | -0.019177 | -0.992 |
| w30 | 18 | -0.189216 | -7.914 |
| w31 | 41 | 0.013087 | 2.805 |
| w32 | 26 | 0.0146 | 14.218 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 15 | 0.081942 | 11.235 |
| w15 | 33 | 0.095226 | 34.135 |
| w16 | 14 | 0.060852 | 520.047 |
| w17 | 25 | 0.060418 | -4.581 |
| w18 | 19 | -0.091076 | -7.156 |
| w19 | 42 | -0.061205 | -9.126 |
| w20 | 30 | 0.021849 | -3.484 |
| w21 | 9 | 0.284302 | 110.764 |
| w22 | 31 | -0.178458 | -38.526 |
| w23 | 21 | 0.057189 | -3.153 |
| w24 | 31 | 0.034664 | 4.126 |
| w25 | 21 | 0.207219 | 69.232 |
| w26 | 40 | -0.030312 | -8.831 |
| w27 | 40 | 0.121501 | 93.836 |
| w28 | 28 | -0.012981 | 8.236 |
| w29 | 11 | 0.128518 | 25.962 |
| w30 | 18 | 0.003025 | 1.871 |
| w31 | 55 | -0.105206 | -9.8 |
| w32 | 30 | 0.116008 | -28.188 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 12 | 0.252018 | 132.463 |
| w26 | 18 | 0.062335 | 15.558 |
| w27 | 31 | 0.140426 | 37.685 |
| w28 | 30 | 0.03921 | 15.101 |
| w29 | 16 | 0.015247 | -0.876 |
| w30 | 22 | 0.03683 | -5.447 |
| w31 | 26 | 0.038216 | 18.59 |
| w32 | 27 | 0.053539 | -29.377 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

