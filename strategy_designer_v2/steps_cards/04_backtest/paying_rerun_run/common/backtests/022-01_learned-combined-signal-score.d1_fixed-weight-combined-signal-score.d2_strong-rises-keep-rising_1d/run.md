# Backtest of 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d2_strong-rises-keep-rising_1d

- Plan: `../../../../../03_test_plan/night3_learned_run/plans/022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d2_strong-rises-keep-rising_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | -0.025383 | 3.052 |
| w2 | 26 | 0.060381 | 51.237 |
| w3 | 35 | 0.03297 | 77.162 |
| w4 | 32 | -0.133128 | -19.902 |
| w5 | 16 | 0.077237 | 146.97 |
| w6 | 33 | 0.011937 | 114.984 |
| w7 | 10 | -0.117673 | -13.6 |
| w8 | 11 | 0.013938 | -1.292 |
| w9 | 7 | -0.07507 | -16.669 |
| w10 | 30 | 0.039223 | 47.892 |
| w11 | 36 | -0.016606 | 30.876 |
| w12 | 16 | -0.035017 | -6.607 |
| w13 | 29 | -0.014788 | 23.818 |
| w14 | 26 | -0.008174 | 25.839 |
| w15 | 27 | 0.156139 | 179.095 |
| w16 | 34 | -0.07381 | 12.74 |
| w17 | 13 | 0.087549 | 13.431 |
| w18 | 16 | 0.054072 | 9.909 |
| w19 | 23 | -0.101815 | -18.591 |
| w20 | 15 | 0.038136 | -2.958 |
| w21 | 18 | -0.17592 | -35.749 |
| w22 | 22 | -0.057903 | 41.608 |
| w23 | 4 | 0.0319 | 2.263 |
| w24 | 35 | 0.032549 | 56.024 |
| w25 | 14 | 0.097304 | 46.331 |
| w26 | 26 | -0.139977 | -30.54 |
| w27 | 34 | 0.038842 | 71.823 |
| w28 | 12 | -0.023271 | -1.775 |
| w29 | 29 | 0.011811 | 2.568 |
| w30 | 7 | -0.00892 | -4.317 |
| w31 | 25 | -0.041308 | -11.127 |
| w32 | 16 | 0.094322 | 16.273 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | -0.061012 | 11.394 |
| w2 | 7 | 0.027271 | 10.473 |
| w3 | 32 | -0.138662 | -31.542 |
| w4 | 32 | 0.132048 | 110.218 |
| w5 | 32 | -0.055516 | 19.131 |
| w6 | 21 | 0.030883 | 69.802 |
| w7 | 13 | -0.08352 | -6.946 |
| w8 | 7 | -0.002288 | -5.095 |
| w9 | 5 | -0.146416 | -4.996 |
| w10 | 36 | -0.045489 | 25.324 |
| w11 | 15 | 0.107572 | 20.177 |
| w12 | 14 | -0.105407 | -10.741 |
| w13 | 25 | 0.041794 | 23.903 |
| w14 | 21 | 0.038802 | 34.859 |
| w15 | 30 | 0.036405 | 71.154 |
| w16 | 35 | -0.120755 | 9.365 |
| w17 | 14 | 0.051097 | 4.991 |
| w18 | 23 | 0.057989 | 3.449 |
| w19 | 15 | -0.059343 | -11.032 |
| w20 | 18 | 0.02002 | -0.319 |
| w21 | 16 | -0.073187 | -5.259 |
| w22 | 27 | -0.03265 | -0.228 |
| w23 | 19 | -0.166624 | -36.285 |
| w24 | 21 | -0.125493 | -15.496 |
| w25 | 27 | 0.060075 | 36.995 |
| w26 | 5 | -0.159908 | -7.824 |
| w27 | 39 | 0.004747 | 31.942 |
| w28 | 21 | -0.248942 | -21.41 |
| w29 | 18 | 0.0846 | 43.448 |
| w30 | 11 | -0.2605 | -29.016 |
| w31 | 13 | -0.030762 | -6.71 |
| w32 | 24 | -0.088934 | -16.009 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 35 | 0.126211 | 122.148 |
| w7 | 7 | -0.032591 | -8.769 |
| w8 | 3 | -0.024977 | -5.533 |
| w9 | 14 | -0.019282 | -5.994 |
| w10 | 32 | -0.21215 | -23.787 |
| w11 | 8 | 0.010082 | -5.09 |
| w12 | 16 | -0.032334 | -15.144 |
| w13 | 35 | -0.046014 | -0.978 |
| w14 | 17 | 0.128412 | 56.271 |
| w15 | 13 | 0.184904 | 151.767 |
| w16 | 16 | -0.032846 | 48.989 |
| w17 | 11 | 0.072256 | 24.007 |
| w18 | 21 | -0.135487 | -12.366 |
| w19 | 26 | -0.138104 | -21.984 |
| w20 | 19 | 0.035576 | -1.177 |
| w21 | 10 | 0.073298 | 26.438 |
| w22 | 18 | -0.06599 | 0.685 |
| w23 | 14 | -0.113415 | -24.276 |
| w24 | 17 | -0.015372 | 7.845 |
| w25 | 16 | 0.027473 | 10.706 |
| w26 | 11 | -0.020945 | -0.589 |
| w27 | 19 | 0.304478 | 233.384 |
| w28 | 7 | -0.257177 | -7.0 |
| w29 | 29 | 0.03349 | 38.641 |
| w30 | 2 | -0.021644 | -3.403 |
| w31 | 17 | -0.118271 | -23.035 |
| w32 | 10 | 0.063095 | 14.055 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 6 | -0.010878 | -5.645 |
| w8 | 7 | 0.018036 | -6.359 |
| w9 | 6 | -0.114829 | -21.795 |
| w10 | 31 | 0.027853 | 40.693 |
| w11 | 15 | -0.121785 | -7.522 |
| w12 | 12 | -0.018236 | -5.413 |
| w13 | 14 | 0.076031 | 48.148 |
| w14 | 13 | 0.039993 | 12.607 |
| w15 | 33 | -0.128284 | -14.864 |
| w16 | 26 | -0.026687 | 55.653 |
| w17 | 14 | 0.072624 | 23.517 |
| w18 | 20 | -0.120044 | -25.049 |
| w19 | 17 | -0.085792 | -19.955 |
| w20 | 16 | 0.004231 | -7.807 |
| w21 | 9 | -0.157988 | -20.548 |
| w22 | 17 | -0.010568 | 12.6 |
| w23 | 5 | 0.164601 | 72.269 |
| w24 | 39 | -0.156592 | -8.449 |
| w25 | 26 | 0.062625 | 76.872 |
| w26 | 6 | -0.259522 | -23.317 |
| w27 | 30 | 0.020489 | 13.22 |
| w28 | 8 | -0.064689 | -15.564 |
| w29 | 60 | -0.171332 | -0.467 |
| w30 | 32 | -0.057959 | 3.635 |
| w31 | 8 | -0.057011 | -7.248 |
| w32 | 13 | -0.0896 | -27.739 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | 0.170979 | 235.25 |
| w2 | 23 | 0.004568 | 10.773 |
| w3 | 12 | 0.075917 | 0.091 |
| w4 | 43 | 0.013963 | 269.308 |
| w5 | 25 | 0.123928 | 114.564 |
| w6 | 18 | 0.12614 | 93.276 |
| w7 | 16 | 0.088757 | 22.708 |
| w8 | 6 | 0.081364 | 1.738 |
| w9 | 8 | -0.143285 | -5.583 |
| w10 | 33 | -0.210971 | -19.664 |
| w11 | 15 | 0.071063 | 24.838 |
| w12 | 12 | -0.201939 | -24.607 |
| w13 | 18 | 0.009145 | 47.321 |
| w14 | 29 | 0.008023 | 52.91 |
| w15 | 29 | 0.080582 | 49.707 |
| w16 | 27 | 0.043729 | 90.748 |
| w17 | 18 | -0.000577 | 15.352 |
| w18 | 15 | 0.053164 | 8.005 |
| w19 | 19 | 0.00123 | -2.633 |
| w20 | 19 | 0.092783 | 13.361 |
| w21 | 17 | -0.110015 | -26.751 |
| w22 | 25 | -0.035636 | 27.715 |
| w23 | 11 | -0.029673 | -10.003 |
| w24 | 30 | 0.011313 | 30.531 |
| w25 | 20 | 0.028951 | 20.912 |
| w26 | 6 | -0.019651 | -5.512 |
| w27 | 26 | 0.039314 | 20.851 |
| w28 | 0 | -0.012846 | 0.0 |
| w29 | 23 | -0.021014 | 95.459 |
| w30 | 5 | -0.017219 | -3.984 |
| w31 | 23 | -0.07337 | -14.166 |
| w32 | 24 | 0.042323 | 3.843 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 27 | 0.045788 | 52.569 |
| w11 | 16 | -0.027236 | -4.186 |
| w12 | 18 | -0.081688 | -11.503 |
| w13 | 19 | 0.058703 | 53.839 |
| w14 | 46 | -0.165052 | 10.045 |
| w15 | 19 | 0.034765 | 18.784 |
| w16 | 22 | 0.09534 | 125.015 |
| w17 | 18 | 0.020414 | 47.923 |
| w18 | 5 | -0.093451 | -11.723 |
| w19 | 15 | -0.078355 | -32.226 |
| w20 | 16 | -0.014161 | -10.074 |
| w21 | 4 | -0.144329 | -3.217 |
| w22 | 19 | -0.05175 | 12.675 |
| w23 | 10 | -0.07837 | -6.289 |
| w24 | 15 | 0.07033 | 155.647 |
| w25 | 15 | 0.056731 | -1.277 |
| w26 | 12 | -0.118276 | -18.599 |
| w27 | 28 | 0.205495 | 119.577 |
| w28 | 6 | -0.236724 | -15.052 |
| w29 | 27 | -0.053957 | 7.146 |
| w30 | 7 | -0.012747 | -3.606 |
| w31 | 7 | -0.159086 | -6.439 |
| w32 | 29 | -0.062895 | -16.171 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 30 | -0.118533 | 2.753 |
| w13 | 32 | -0.110341 | -27.338 |
| w14 | 25 | -0.05669 | 35.053 |
| w15 | 22 | -0.256589 | -31.472 |
| w16 | 18 | 0.062975 | 72.983 |
| w17 | 12 | 0.055138 | 11.597 |
| w18 | 15 | 0.035214 | 11.078 |
| w19 | 15 | -0.014177 | -15.291 |
| w20 | 36 | 0.08344 | 4.748 |
| w21 | 23 | -0.125317 | -23.657 |
| w22 | 13 | 0.071339 | 25.109 |
| w23 | 7 | 0.001476 | -1.364 |
| w24 | 30 | -0.088938 | 7.088 |
| w25 | 17 | 0.051494 | 5.336 |
| w26 | 0 | 0.036603 | 0.0 |
| w27 | 21 | 0.135518 | 44.862 |
| w28 | 7 | -0.1733 | -12.935 |
| w29 | 24 | -0.109489 | -21.722 |
| w30 | 4 | -0.005653 | -3.765 |
| w31 | 13 | -0.097253 | -17.891 |
| w32 | 29 | -0.084645 | -26.573 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 15 | -0.075506 | -16.576 |
| w16 | 23 | 0.033389 | 82.761 |
| w17 | 10 | 0.029259 | 9.913 |
| w18 | 14 | 0.086806 | 39.799 |
| w19 | 13 | -0.174895 | -17.399 |
| w20 | 12 | 0.013396 | 0.285 |
| w21 | 18 | -0.060647 | -35.864 |
| w22 | 22 | -0.0196 | -2.864 |
| w23 | 3 | -0.124825 | -0.614 |
| w24 | 32 | 0.041246 | 72.394 |
| w25 | 16 | 0.064996 | 2.696 |
| w26 | 8 | -0.119162 | -13.234 |
| w27 | 25 | 0.167997 | 119.654 |
| w28 | 3 | -0.023799 | -2.845 |
| w29 | 22 | 0.038322 | 21.062 |
| w30 | 0 | None | 0.0 |
| w31 | 21 | -0.042542 | -18.988 |
| w32 | 16 | -0.165853 | -26.726 |

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
| w15 | 19 | -0.042415 | -15.795 |
| w16 | 35 | -0.074315 | 84.679 |
| w17 | 6 | 0.064531 | 15.631 |
| w18 | 30 | -0.181655 | -28.35 |
| w19 | 12 | -0.089643 | -20.254 |
| w20 | 30 | -0.062728 | -27.032 |
| w21 | 19 | -0.097719 | -10.671 |
| w22 | 27 | -0.060963 | 0.49 |
| w23 | 34 | -0.060549 | -2.476 |
| w24 | 42 | -0.082346 | 31.367 |
| w25 | 21 | 0.121073 | 36.476 |
| w26 | 26 | -0.069268 | 8.629 |
| w27 | 32 | 0.045384 | 196.741 |
| w28 | 24 | -0.051563 | -7.829 |
| w29 | 39 | 0.012354 | 53.128 |
| w30 | 6 | -0.018408 | -6.67 |
| w31 | 34 | -0.033148 | 13.783 |
| w32 | 36 | -0.074239 | -2.757 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 26 | 0.129014 | 67.589 |
| w17 | 13 | -0.07091 | -18.47 |
| w18 | 18 | -0.039496 | -14.24 |
| w19 | 15 | -0.034492 | -13.114 |
| w20 | 14 | 0.021101 | -4.723 |
| w21 | 6 | -0.241416 | -22.809 |
| w22 | 23 | 0.001548 | 13.491 |
| w23 | 13 | 0.044777 | -2.183 |
| w24 | 21 | 0.041402 | 57.665 |
| w25 | 18 | 0.034123 | -3.396 |
| w26 | 11 | -0.094174 | -13.785 |
| w27 | 21 | 0.139744 | 59.553 |
| w28 | 1 | -0.072236 | -0.424 |
| w29 | 22 | -0.00471 | 5.776 |
| w30 | 20 | -0.011367 | -24.941 |
| w31 | 15 | -0.143346 | -13.643 |
| w32 | 10 | -0.117638 | -19.341 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 21 | 0.073405 | 5.511 |
| w21 | 7 | -0.1514 | -20.811 |
| w22 | 23 | -0.001724 | 15.255 |
| w23 | 6 | 0.035694 | -1.135 |
| w24 | 18 | 0.221464 | 308.008 |
| w25 | 23 | -0.016402 | -7.274 |
| w26 | 5 | -0.111642 | -9.92 |
| w27 | 39 | -0.065223 | 15.028 |
| w28 | 3 | -0.035851 | -2.761 |
| w29 | 28 | -0.108133 | -7.843 |
| w30 | 12 | 0.034053 | -0.466 |
| w31 | 20 | -0.115202 | -19.678 |
| w32 | 11 | 0.010003 | -2.317 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 16 | 0.001061 | 9.822 |
| w23 | 8 | 0.037888 | -0.688 |
| w24 | 24 | 0.101045 | 152.612 |
| w25 | 22 | 0.078364 | 39.796 |
| w26 | 22 | -0.075653 | -9.141 |
| w27 | 30 | -0.083088 | -8.174 |
| w28 | 0 | -0.182421 | 0.0 |
| w29 | 20 | -0.017695 | 7.317 |
| w30 | 17 | -0.044465 | -14.637 |
| w31 | 25 | -0.093729 | -19.042 |
| w32 | 23 | 0.041272 | 41.012 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 23 | -0.001372 | 19.707 |
| w25 | 30 | 0.018711 | 11.334 |
| w26 | 13 | -0.118748 | -12.486 |
| w27 | 36 | -0.055273 | 64.647 |
| w28 | 7 | 0.036708 | 2.965 |
| w29 | 13 | 0.020864 | 2.461 |
| w30 | 6 | -0.023729 | -9.698 |
| w31 | 17 | -0.082185 | -14.433 |
| w32 | 22 | -0.065472 | -10.795 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 21 | 0.202319 | 164.319 |
| w6 | 23 | -0.060463 | 22.062 |
| w7 | 10 | 0.044828 | -6.89 |
| w8 | 19 | -0.046789 | -9.87 |
| w9 | 4 | -0.097438 | -18.556 |
| w10 | 19 | -0.004123 | 11.688 |
| w11 | 24 | 0.062785 | 5.672 |
| w12 | 1 | -0.103089 | -0.956 |
| w13 | 20 | 0.07378 | 70.52 |
| w14 | 47 | -0.119093 | 5.094 |
| w15 | 21 | -0.112278 | -14.185 |
| w16 | 38 | -0.217537 | 19.448 |
| w17 | 15 | 0.029049 | 10.74 |
| w18 | 23 | -0.037269 | -8.24 |
| w19 | 16 | 0.000284 | -5.765 |
| w20 | 15 | 0.018243 | -6.704 |
| w21 | 10 | -0.044371 | -5.007 |
| w22 | 33 | -0.038668 | -10.503 |
| w23 | 10 | 0.071444 | 1.042 |
| w24 | 42 | -0.117534 | -18.136 |
| w25 | 6 | 0.035633 | 7.843 |
| w26 | 28 | 0.072553 | 21.932 |
| w27 | 36 | 0.005401 | 28.615 |
| w28 | 8 | -0.100883 | -16.971 |
| w29 | 19 | 0.009897 | -2.365 |
| w30 | 25 | 0.160817 | 357.681 |
| w31 | 13 | 0.062933 | 16.267 |
| w32 | 24 | 0.05207 | 44.24 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 28 | 0.091485 | 169.565 |
| w6 | 17 | 0.040215 | 100.909 |
| w7 | 14 | -0.101933 | -16.685 |
| w8 | 12 | -0.075016 | -12.474 |
| w9 | 17 | -0.047731 | -19.252 |
| w10 | 32 | -0.086641 | 8.443 |
| w11 | 31 | -0.073281 | -4.165 |
| w12 | 11 | 0.002554 | -4.948 |
| w13 | 26 | 0.003749 | 26.485 |
| w14 | 32 | 0.028659 | 42.168 |
| w15 | 19 | -0.009324 | 19.228 |
| w16 | 25 | -0.051243 | 33.348 |
| w17 | 21 | 0.012332 | -0.308 |
| w18 | 13 | -0.116474 | -10.237 |
| w19 | 22 | -0.0072 | -19.053 |
| w20 | 24 | -0.018461 | -14.014 |
| w21 | 24 | -0.10741 | -31.635 |
| w22 | 25 | -0.00465 | -0.026 |
| w23 | 8 | 0.031707 | 3.246 |
| w24 | 51 | -0.056072 | 1.53 |
| w25 | 18 | -0.242937 | -41.696 |
| w26 | 32 | 0.029489 | 15.196 |
| w27 | 29 | -0.002694 | -7.357 |
| w28 | 35 | -0.022657 | 17.87 |
| w29 | 10 | 0.125629 | 34.829 |
| w30 | 50 | -0.119073 | 10.628 |
| w31 | 25 | -0.034627 | -7.938 |
| w32 | 31 | 0.061799 | 53.378 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 14 | -0.073104 | -13.201 |
| w18 | 36 | -0.166257 | 5.028 |
| w19 | 19 | -0.090102 | -24.297 |
| w20 | 12 | 0.079128 | 10.259 |
| w21 | 9 | -0.2925 | -33.974 |
| w22 | 17 | 0.032167 | 16.866 |
| w23 | 9 | 0.02374 | -6.951 |
| w24 | 29 | -0.150309 | -17.992 |
| w25 | 11 | 0.123018 | 19.579 |
| w26 | 14 | -0.104586 | -17.008 |
| w27 | 21 | 0.133752 | 126.464 |
| w28 | 20 | 0.000611 | 5.187 |
| w29 | 20 | 0.079416 | 21.932 |
| w30 | 0 | -0.013244 | 0.0 |
| w31 | 14 | -0.012839 | -5.921 |
| w32 | 25 | 0.11849 | 50.864 |

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
| w17 | 29 | -0.077586 | -16.608 |
| w18 | 19 | -0.048607 | -10.398 |
| w19 | 19 | -0.097658 | -9.759 |
| w20 | 20 | 0.041097 | -0.681 |
| w21 | 13 | -0.203586 | -38.629 |
| w22 | 12 | 0.004383 | 10.362 |
| w23 | 7 | 0.020887 | -2.834 |
| w24 | 40 | -0.110695 | 3.929 |
| w25 | 23 | 0.075103 | 8.359 |
| w26 | 34 | -0.135568 | -17.023 |
| w27 | 34 | 0.007967 | 75.405 |
| w28 | 4 | -0.008946 | -1.11 |
| w29 | 26 | -0.066704 | 11.081 |
| w30 | 10 | -0.022329 | -11.605 |
| w31 | 7 | -0.205441 | -12.181 |
| w32 | 16 | -0.039766 | -8.646 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 21 | -0.148116 | -15.769 |
| w20 | 14 | -0.016726 | -4.942 |
| w21 | 12 | 0.016564 | -1.383 |
| w22 | 21 | 0.043576 | 154.664 |
| w23 | 16 | -0.061999 | -9.036 |
| w24 | 31 | 0.011363 | 171.631 |
| w25 | 19 | -0.097215 | -14.744 |
| w26 | 15 | -0.008978 | -9.982 |
| w27 | 33 | -0.034375 | 2.674 |
| w28 | 2 | -0.143851 | -2.603 |
| w29 | 37 | -0.032896 | 9.986 |
| w30 | 3 | -0.059355 | -5.123 |
| w31 | 8 | -0.02306 | -8.112 |
| w32 | 14 | 0.078741 | 36.924 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 19 | 0.080447 | 24.815 |
| w23 | 11 | -0.068333 | -12.003 |
| w24 | 23 | -0.00411 | 28.759 |
| w25 | 21 | -0.061239 | -10.465 |
| w26 | 14 | -0.053536 | 1.018 |
| w27 | 20 | -0.050526 | -10.223 |
| w28 | 5 | -0.034128 | -3.53 |
| w29 | 31 | -0.034945 | 11.377 |
| w30 | 5 | -0.019629 | -0.979 |
| w31 | 18 | 0.00851 | -10.325 |
| w32 | 17 | -0.016726 | -3.216 |

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
| w27 | 33 | -0.054538 | 26.209 |
| w28 | 2 | -0.068651 | -4.56 |
| w29 | 24 | -0.054231 | 9.199 |
| w30 | 9 | -0.061445 | -13.164 |
| w31 | 6 | -0.093127 | -3.513 |
| w32 | 17 | 0.018568 | 34.98 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 7 | 0.046414 | 5.465 |
| w18 | 10 | -0.076816 | 5.854 |
| w19 | 9 | -0.13646 | -23.78 |
| w20 | 7 | 0.017761 | -6.757 |
| w21 | 5 | -0.220396 | -23.412 |
| w22 | 18 | -0.038944 | 12.904 |
| w23 | 16 | -0.006756 | -4.715 |
| w24 | 31 | -0.02107 | 30.726 |
| w25 | 16 | 0.039164 | -2.173 |
| w26 | 5 | -0.207619 | -5.946 |
| w27 | 31 | 0.023465 | 14.118 |
| w28 | 0 | -0.159334 | 0.0 |
| w29 | 17 | -0.039255 | -4.136 |
| w30 | 13 | -0.184928 | -21.757 |
| w31 | 18 | -0.044362 | -14.979 |
| w32 | 18 | -0.060647 | -9.803 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 4 | 0.04909 | 6.992 |
| w18 | 17 | -0.002261 | -6.469 |
| w19 | 12 | -0.083383 | -10.032 |
| w20 | 13 | 0.032268 | -3.339 |
| w21 | 2 | -0.108241 | -3.075 |
| w22 | 15 | 0.09612 | 123.099 |
| w23 | 10 | -0.031547 | -12.608 |
| w24 | 23 | 0.042482 | 60.922 |
| w25 | 12 | 0.198426 | 71.963 |
| w26 | 14 | -0.080975 | -6.583 |
| w27 | 33 | -0.089726 | -9.383 |
| w28 | 1 | -0.086543 | -1.867 |
| w29 | 23 | 0.002794 | -0.906 |
| w30 | 3 | -0.051252 | -5.383 |
| w31 | 7 | -0.11546 | -8.158 |
| w32 | 15 | -0.066379 | -13.663 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 8 | 0.02745 | -4.661 |
| w29 | 16 | 0.018434 | -2.343 |
| w30 | 8 | -0.010185 | -10.754 |
| w31 | 12 | 0.092984 | 20.008 |
| w32 | 10 | 0.023048 | 1.097 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 20 | 0.02916 | 13.323 |
| w15 | 22 | 0.069112 | 73.766 |
| w16 | 12 | -0.028607 | 195.328 |
| w17 | 13 | 0.053072 | 3.399 |
| w18 | 19 | -0.050476 | -5.706 |
| w19 | 17 | -0.030556 | -13.455 |
| w20 | 17 | -0.004928 | -11.792 |
| w21 | 11 | 0.021658 | 31.782 |
| w22 | 22 | -0.10323 | -7.092 |
| w23 | 22 | 0.044739 | -0.11 |
| w24 | 27 | 0.053353 | 44.293 |
| w25 | 12 | 0.230829 | 117.03 |
| w26 | 15 | -0.137466 | -19.958 |
| w27 | 19 | 0.184456 | 214.17 |
| w28 | 2 | -0.09332 | -1.303 |
| w29 | 26 | -0.016593 | 14.016 |
| w30 | 16 | -0.007575 | -4.23 |
| w31 | 10 | 0.026887 | -1.999 |
| w32 | 7 | 0.036731 | -3.334 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 11 | 0.29388 | 207.312 |
| w26 | 13 | -0.035349 | -4.856 |
| w27 | 23 | 0.057043 | 58.066 |
| w28 | 8 | -0.014351 | -0.43 |
| w29 | 18 | 0.022957 | 6.035 |
| w30 | 4 | -0.042026 | -6.148 |
| w31 | 19 | -0.07719 | -16.601 |
| w32 | 16 | 0.055605 | 10.636 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

