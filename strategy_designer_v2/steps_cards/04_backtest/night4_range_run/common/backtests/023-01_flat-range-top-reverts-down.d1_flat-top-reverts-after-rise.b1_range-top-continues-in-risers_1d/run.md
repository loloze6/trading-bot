# Backtest of 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers_1d

- Plan: `../../../../../03_test_plan/night4_range_run/plans/023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

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

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | -0.045175 | 23.746 |
| w2 | 46 | 0.061038 | 15.883 |
| w3 | 26 | -0.130845 | -16.776 |
| w4 | 47 | -0.020483 | -32.25 |
| w5 | 63 | -0.021788 | 47.454 |
| w6 | 55 | 0.049754 | 45.462 |
| w7 | 30 | -0.028316 | -7.193 |
| w8 | 5 | 0.050416 | -0.218 |
| w9 | 0 | None | 0.0 |
| w10 | 32 | -0.012412 | 22.708 |
| w11 | 48 | 0.059065 | 26.343 |
| w12 | 0 | None | 0.0 |
| w13 | 26 | 0.118548 | 13.572 |
| w14 | 42 | -0.029315 | -5.03 |
| w15 | 58 | 0.016041 | 16.268 |
| w16 | 51 | -0.06475 | -5.116 |
| w17 | 15 | 0.066786 | 5.656 |
| w18 | 57 | 0.052316 | 7.87 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 35 | -0.049865 | -16.963 |
| w22 | 57 | 0.009402 | 15.411 |
| w23 | 23 | -0.066464 | -15.785 |
| w24 | 35 | -0.258554 | -27.679 |
| w25 | 52 | -0.061793 | -8.999 |
| w26 | 18 | -0.135365 | -5.767 |
| w27 | 43 | -0.006209 | 4.323 |
| w28 | 35 | -0.203164 | -25.417 |
| w29 | 31 | 0.040264 | 29.637 |
| w30 | 27 | -0.13034 | -27.667 |
| w31 | 0 | None | 0.0 |
| w32 | 9 | 0.044721 | 6.417 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

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
| w20 | 2 | -0.067296 | 3.938 |
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

- BCHUSD: 25 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w8 | 15 | 0.032874 | -1.476 |
| w9 | 1 | -0.067821 | -9.341 |
| w10 | 25 | 0.113313 | 39.994 |
| w11 | 40 | -0.006376 | 0.28 |
| w12 | 0 | None | 0.0 |
| w13 | 32 | 0.161623 | 67.27 |
| w14 | 40 | -0.030677 | -14.21 |
| w15 | 29 | -0.066851 | 2.298 |
| w16 | 65 | 0.063126 | 40.966 |
| w17 | 19 | 0.102222 | 13.173 |
| w18 | 30 | -0.021912 | -11.095 |
| w19 | 7 | 0.007037 | 4.994 |
| w20 | 2 | -0.062625 | 3.55 |
| w21 | 19 | 0.000539 | -0.929 |
| w22 | 49 | -0.041571 | -5.678 |
| w23 | 23 | 0.150611 | 71.145 |
| w24 | 52 | -0.180564 | -37.424 |
| w25 | 51 | 0.070494 | 23.169 |
| w26 | 25 | -0.071771 | -14.652 |
| w27 | 28 | 0.076293 | 2.108 |
| w28 | 20 | 0.024244 | 10.095 |
| w29 | 59 | -0.185809 | 0.405 |
| w30 | 37 | -0.151803 | -29.72 |
| w31 | 24 | -0.036732 | -6.99 |
| w32 | 2 | -0.0628 | -7.191 |

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
| w1 | 49 | 0.206316 | 207.997 |
| w2 | 48 | -0.009326 | -2.597 |
| w3 | 19 | -0.0069 | 17.538 |
| w4 | 32 | 0.080657 | 140.836 |
| w5 | 42 | 0.151909 | 113.598 |
| w6 | 48 | 0.041342 | 55.424 |
| w7 | 31 | 0.101051 | 18.683 |
| w8 | 9 | -0.079592 | -8.939 |
| w9 | 0 | None | 0.0 |
| w10 | 35 | -0.040656 | -2.346 |
| w11 | 46 | 0.11951 | 48.628 |
| w12 | 2 | 0.015259 | -1.051 |
| w13 | 26 | 0.104098 | 50.164 |
| w14 | 45 | -0.004086 | 46.13 |
| w15 | 69 | 0.006408 | 3.562 |
| w16 | 53 | -0.056513 | 60.661 |
| w17 | 45 | -0.034911 | -0.543 |
| w18 | 59 | -0.090201 | -13.084 |
| w19 | 14 | 0.047362 | 12.541 |
| w20 | 2 | -0.029219 | 4.269 |
| w21 | 10 | -7.8e-05 | 3.436 |
| w22 | 48 | -0.106109 | -2.135 |
| w23 | 43 | -0.027359 | 19.163 |
| w24 | 27 | -0.089077 | 15.622 |
| w25 | 58 | 0.025987 | 1.63 |
| w26 | 33 | -0.034084 | -20.586 |
| w27 | 32 | 0.025694 | -29.912 |
| w28 | 26 | -0.060179 | 2.182 |
| w29 | 37 | -0.042634 | 37.807 |
| w30 | 39 | -0.11332 | -10.903 |
| w31 | 0 | None | 0.0 |
| w32 | 21 | 0.133204 | 57.833 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 34 | 0.042605 | 36.196 |
| w11 | 33 | -0.159401 | -17.566 |
| w12 | 0 | None | 0.0 |
| w13 | 24 | 0.161772 | 47.982 |
| w14 | 46 | 0.039996 | 31.637 |
| w15 | 36 | -0.014398 | -10.966 |
| w16 | 50 | 0.053425 | 82.297 |
| w17 | 55 | -0.037623 | 31.324 |
| w18 | 39 | -0.162357 | -23.274 |
| w19 | 0 | None | 0.0 |
| w20 | 5 | 0.018246 | -9.041 |
| w21 | 2 | -0.131564 | -3.245 |
| w22 | 43 | -0.014003 | 3.673 |
| w23 | 10 | 0.057123 | 27.369 |
| w24 | 19 | 0.108352 | 75.128 |
| w25 | 49 | 0.056583 | 14.025 |
| w26 | 0 | None | 0.0 |
| w27 | 26 | 0.232607 | 131.035 |
| w28 | 26 | 0.007066 | -3.557 |
| w29 | 33 | -0.004919 | -6.296 |
| w30 | 17 | -0.075149 | -23.641 |
| w31 | 0 | None | 0.0 |
| w32 | 5 | -0.028417 | -1.54 |

- ATOMUSD: 20 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 32 | -0.050154 | -14.267 |
| w14 | 47 | 0.058284 | 55.909 |
| w15 | 38 | 0.020706 | -19.823 |
| w16 | 65 | -0.04376 | 22.496 |
| w17 | 14 | -0.001512 | 5.587 |
| w18 | 46 | -0.053461 | -7.689 |
| w19 | 25 | -0.112431 | -4.23 |
| w20 | 14 | -0.019485 | -12.489 |
| w21 | 37 | 0.010807 | -18.785 |
| w22 | 41 | -0.040565 | -16.138 |
| w23 | 0 | None | 0.0 |
| w24 | 26 | -0.134073 | -3.389 |
| w25 | 50 | 0.042116 | 15.509 |
| w26 | 1 | 0.071652 | 1.098 |
| w27 | 26 | 0.130721 | 41.328 |
| w28 | 17 | 0.030184 | 11.067 |
| w29 | 37 | -0.05395 | -22.382 |
| w30 | 22 | -0.017355 | -9.611 |
| w31 | 3 | 0.165434 | 3.511 |
| w32 | 14 | 0.100314 | -2.044 |

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
| w15 | 18 | -0.093127 | -19.373 |
| w16 | 61 | 0.016357 | 28.641 |
| w17 | 17 | -0.058307 | -1.926 |
| w18 | 48 | -0.073339 | -4.534 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 18 | -0.009312 | -21.247 |
| w22 | 28 | -0.191782 | -18.665 |
| w23 | 0 | None | 0.0 |
| w24 | 24 | 0.055939 | 50.591 |
| w25 | 51 | 0.083869 | 13.687 |
| w26 | 5 | -0.060212 | -1.66 |
| w27 | 31 | 0.15444 | 13.613 |
| w28 | 23 | 0.050398 | 10.851 |
| w29 | 32 | 0.026071 | 13.091 |
| w30 | 22 | -0.099507 | 0.864 |
| w31 | 2 | 0.086768 | -2.377 |
| w32 | 34 | 0.082748 | -15.887 |

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

- DOTUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 17 | -0.125261 | -23.547 |
| w18 | 55 | 0.005872 | 6.378 |
| w19 | 3 | -0.04199 | 6.227 |
| w20 | 1 | -0.042132 | -4.234 |
| w21 | 2 | 0.136809 | 6.886 |
| w22 | 38 | -0.099826 | -15.018 |
| w23 | 0 | None | 0.0 |
| w24 | 23 | 0.036727 | 22.96 |
| w25 | 56 | 0.075785 | 24.221 |
| w26 | 5 | -0.083012 | -1.325 |
| w27 | 19 | 0.159236 | 41.132 |
| w28 | 15 | 0.023969 | 10.448 |
| w29 | 14 | 0.073565 | 2.246 |
| w30 | 22 | -0.024874 | -6.946 |
| w31 | 0 | None | 0.0 |
| w32 | 8 | -0.029939 | -0.546 |

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
| w20 | 1 | 0.121572 | 7.842 |
| w21 | 10 | 0.097277 | 5.256 |
| w22 | 47 | -0.070589 | 8.311 |
| w23 | 0 | None | 0.0 |
| w24 | 12 | 0.194765 | 82.217 |
| w25 | 65 | 0.067021 | 18.241 |
| w26 | 5 | 0.004596 | -1.893 |
| w27 | 39 | 0.066654 | 23.37 |
| w28 | 20 | 0.019159 | 7.894 |
| w29 | 36 | -0.098479 | -15.27 |
| w30 | 24 | 0.158045 | 34.734 |
| w31 | 0 | None | 0.0 |
| w32 | 15 | -0.025439 | -1.474 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 43 | -0.090259 | -15.612 |
| w23 | 0 | None | 0.0 |
| w24 | 27 | 0.059518 | 39.63 |
| w25 | 56 | 0.033689 | 30.165 |
| w26 | 31 | 0.033854 | 5.381 |
| w27 | 32 | 0.04175 | -9.112 |
| w28 | 20 | 0.029685 | 17.395 |
| w29 | 25 | -0.046059 | -17.913 |
| w30 | 20 | -0.037924 | -16.581 |
| w31 | 0 | None | 0.0 |
| w32 | 63 | 0.0801 | -9.759 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 24 | -0.121901 | 1.08 |
| w25 | 52 | 0.060973 | 42.189 |
| w26 | 1 | -0.083025 | -8.106 |
| w27 | 45 | -0.066841 | 23.009 |
| w28 | 24 | 0.045338 | 7.192 |
| w29 | 54 | 0.034212 | 7.738 |
| w30 | 21 | -0.083905 | -22.095 |
| w31 | 0 | None | 0.0 |
| w32 | 18 | 0.176854 | 52.211 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

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

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 67 | 0.068465 | 96.66 |
| w6 | 46 | 0.060837 | 32.409 |
| w7 | 31 | -0.053778 | -3.423 |
| w8 | 2 | -0.04999 | -1.317 |
| w9 | 9 | 0.063511 | 2.621 |
| w10 | 31 | 0.015784 | 6.868 |
| w11 | 60 | -0.037481 | 8.41 |
| w12 | 0 | None | 0.0 |
| w13 | 33 | 0.145471 | 51.881 |
| w14 | 52 | -0.061651 | 9.458 |
| w15 | 59 | -0.097106 | -4.769 |
| w16 | 58 | 0.01073 | 8.314 |
| w17 | 28 | 0.072174 | 18.128 |
| w18 | 32 | -0.119214 | -25.204 |
| w19 | 17 | 0.045282 | 8.353 |
| w20 | 15 | -0.105158 | -8.039 |
| w21 | 37 | -0.133776 | -14.62 |
| w22 | 57 | 0.015967 | 11.281 |
| w23 | 37 | 0.113204 | 18.945 |
| w24 | 49 | -0.144333 | -19.431 |
| w25 | 11 | -0.014172 | -24.208 |
| w26 | 64 | -0.084276 | -28.781 |
| w27 | 45 | -0.097301 | -15.985 |
| w28 | 63 | -0.082307 | -8.579 |
| w29 | 33 | 0.124506 | 59.416 |
| w30 | 51 | -0.249814 | -29.144 |
| w31 | 14 | 0.292113 | 61.914 |
| w32 | 27 | -0.005979 | 37.806 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

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

- AAVEUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 13 | -0.174371 | -31.133 |
| w18 | 29 | -0.103031 | -34.171 |
| w19 | 6 | 0.070967 | 5.364 |
| w20 | 8 | 0.069187 | 8.085 |
| w21 | 21 | -0.057539 | -1.03 |
| w22 | 45 | -0.165644 | -8.326 |
| w23 | 9 | 0.057466 | 0.171 |
| w24 | 44 | -0.113178 | 2.101 |
| w25 | 42 | -0.003771 | -4.013 |
| w26 | 34 | 0.004258 | 3.943 |
| w27 | 65 | -0.05436 | -15.06 |
| w28 | 35 | -0.045895 | 6.474 |
| w29 | 48 | -0.164434 | -25.854 |
| w30 | 17 | -0.017384 | 5.792 |
| w31 | 0 | None | 0.0 |
| w32 | 14 | 0.049974 | -19.713 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 2 | 0.099005 | 19.455 |
| w20 | 3 | 0.106395 | 1.95 |
| w21 | 42 | -0.082969 | -13.231 |
| w22 | 53 | -0.015941 | 85.388 |
| w23 | 55 | -0.08636 | -17.684 |
| w24 | 38 | 0.111853 | 140.696 |
| w25 | 43 | -0.057974 | -17.928 |
| w26 | 3 | -0.00844 | -11.715 |
| w27 | 43 | 0.053156 | -2.793 |
| w28 | 21 | -0.02338 | 10.11 |
| w29 | 41 | -0.068232 | -12.06 |
| w30 | 18 | -0.10345 | -14.46 |
| w31 | 0 | None | 0.0 |
| w32 | 47 | 0.038437 | 17.732 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 57 | -0.085861 | -6.098 |
| w23 | 5 | -0.093923 | -18.994 |
| w24 | 27 | -0.110397 | 2.701 |
| w25 | 53 | -0.049016 | -29.726 |
| w26 | 0 | None | 0.0 |
| w27 | 22 | -0.026325 | 12.869 |
| w28 | 28 | -0.149057 | -22.198 |
| w29 | 23 | 0.00845 | -11.83 |
| w30 | 28 | -0.114607 | -6.422 |
| w31 | 0 | None | 0.0 |
| w32 | 16 | 0.035794 | -0.708 |

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
| w27 | 22 | 0.140917 | 51.81 |
| w28 | 30 | -0.014186 | 9.268 |
| w29 | 28 | 0.064458 | 4.896 |
| w30 | 26 | -0.129866 | -16.81 |
| w31 | 0 | None | 0.0 |
| w32 | 49 | -0.011617 | 30.151 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

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

- GRTUSD: 15 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w18 | 46 | -0.011791 | 6.726 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | -0.027274 | -4.011 |
| w21 | 13 | 0.001196 | 14.35 |
| w22 | 44 | 0.019315 | 52.348 |
| w23 | 4 | 0.00316 | 3.482 |
| w24 | 32 | -0.043483 | 25.882 |
| w25 | 48 | 0.112578 | 32.092 |
| w26 | 18 | -0.089992 | -2.455 |
| w27 | 25 | 0.121696 | -2.276 |
| w28 | 14 | -0.008915 | 2.737 |
| w29 | 15 | 0.023396 | -2.504 |
| w30 | 15 | 0.045398 | -3.508 |
| w31 | 0 | None | 0.0 |
| w32 | 8 | -0.110808 | -7.638 |

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
| w28 | 1 | 0.176553 | 2.598 |
| w29 | 39 | -0.056127 | -13.565 |
| w30 | 15 | -0.106863 | -14.065 |
| w31 | 16 | -0.022162 | -3.484 |
| w32 | 22 | 0.011496 | -8.722 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 45 | 0.037848 | -12.582 |
| w15 | 29 | 0.034347 | -5.306 |
| w16 | 61 | -0.017939 | 325.168 |
| w17 | 42 | 0.058949 | 3.948 |
| w18 | 21 | -0.00172 | 0.763 |
| w19 | 4 | -0.312643 | -13.094 |
| w20 | 1 | -0.125027 | -17.357 |
| w21 | 39 | 0.096511 | 52.293 |
| w22 | 37 | -0.076538 | -9.677 |
| w23 | 9 | -0.111029 | -10.59 |
| w24 | 34 | -0.040275 | 6.888 |
| w25 | 63 | 0.109283 | 58.267 |
| w26 | 20 | -0.141717 | -11.155 |
| w27 | 34 | 0.218668 | 112.33 |
| w28 | 20 | -0.007115 | 0.002 |
| w29 | 32 | -0.043222 | -15.336 |
| w30 | 25 | -0.032867 | -20.821 |
| w31 | 0 | None | 0.0 |
| w32 | 19 | 0.040384 | 5.178 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

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

