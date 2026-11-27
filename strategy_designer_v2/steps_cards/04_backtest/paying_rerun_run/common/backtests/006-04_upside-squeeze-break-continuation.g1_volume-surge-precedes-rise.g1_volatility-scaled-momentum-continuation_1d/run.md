# Backtest of 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d

- Plan: `../../../../../03_test_plan/hold_paying_run/plans/006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | 0.064529 | 10.53 |
| w2 | 18 | 0.122671 | 57.254 |
| w3 | 46 | -0.028939 | 57.466 |
| w4 | 32 | 0.014653 | 15.289 |
| w5 | 34 | -0.003662 | 66.219 |
| w6 | 34 | 0.124963 | 129.858 |
| w7 | 22 | 0.008504 | 1.237 |
| w8 | 25 | 0.041242 | -11.231 |
| w9 | 22 | -0.10928 | -23.561 |
| w10 | 31 | 0.059062 | 34.064 |
| w11 | 19 | 0.103728 | 66.164 |
| w12 | 19 | 0.0237 | -3.722 |
| w13 | 29 | -0.004121 | 15.015 |
| w14 | 29 | 0.032443 | 26.633 |
| w15 | 34 | 0.019407 | 89.675 |
| w16 | 31 | -0.019201 | 24.202 |
| w17 | 31 | 0.042026 | 6.754 |
| w18 | 23 | 0.073755 | -3.987 |
| w19 | 25 | -0.011558 | 1.665 |
| w20 | 26 | -0.066138 | -24.869 |
| w21 | 27 | -0.047288 | -21.682 |
| w22 | 34 | 0.027311 | 50.719 |
| w23 | 16 | 0.023579 | -13.038 |
| w24 | 38 | -0.072908 | 31.587 |
| w25 | 18 | 0.11834 | 57.505 |
| w26 | 33 | 0.01645 | -7.22 |
| w27 | 36 | 0.081744 | 55.322 |
| w28 | 19 | -0.002425 | -6.76 |
| w29 | 36 | -0.004789 | -5.099 |
| w30 | 19 | -0.043676 | -20.92 |
| w31 | 37 | -0.025142 | -14.822 |
| w32 | 28 | 0.096278 | 7.17 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | -0.041853 | 0.808 |
| w2 | 26 | -0.04288 | -8.146 |
| w3 | 34 | -0.15183 | -23.039 |
| w4 | 35 | 0.088751 | 72.52 |
| w5 | 29 | -0.099895 | 25.967 |
| w6 | 26 | 0.118074 | 99.618 |
| w7 | 15 | -0.003897 | 6.172 |
| w8 | 14 | -0.061709 | -19.127 |
| w9 | 18 | -0.105379 | -25.702 |
| w10 | 25 | -0.081494 | 4.305 |
| w11 | 25 | -0.033529 | 4.516 |
| w12 | 24 | 0.079678 | 2.307 |
| w13 | 28 | 0.010813 | 17.773 |
| w14 | 26 | -0.027176 | 0.83 |
| w15 | 29 | -0.042324 | 6.62 |
| w16 | 31 | -0.011774 | 28.965 |
| w17 | 22 | 0.079272 | 14.091 |
| w18 | 29 | -0.065883 | -7.319 |
| w19 | 22 | 0.036788 | -2.312 |
| w20 | 22 | 0.007588 | -5.276 |
| w21 | 26 | -0.050118 | 13.892 |
| w22 | 36 | -0.011875 | 12.494 |
| w23 | 18 | -0.056847 | -15.928 |
| w24 | 25 | -0.072587 | -9.263 |
| w25 | 29 | -0.018961 | 10.044 |
| w26 | 18 | -0.024908 | -2.119 |
| w27 | 28 | -0.013793 | 26.956 |
| w28 | 23 | -0.043342 | -10.133 |
| w29 | 23 | 0.044108 | 15.583 |
| w30 | 20 | -0.217429 | -47.469 |
| w31 | 33 | -0.062541 | -16.949 |
| w32 | 30 | -0.023089 | -21.895 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 33 | 0.115485 | 100.47 |
| w7 | 16 | 0.152641 | 22.248 |
| w8 | 9 | -0.021288 | -7.633 |
| w9 | 17 | 0.146674 | 39.519 |
| w10 | 16 | -0.121255 | -20.876 |
| w11 | 19 | 0.013402 | 17.654 |
| w12 | 20 | 0.04725 | 2.126 |
| w13 | 32 | -0.018842 | 8.198 |
| w14 | 21 | 0.156067 | 47.83 |
| w15 | 18 | 0.230068 | 183.338 |
| w16 | 32 | 0.067426 | 82.188 |
| w17 | 18 | 0.179987 | 46.995 |
| w18 | 28 | 0.005991 | -15.64 |
| w19 | 18 | 0.0716 | 9.061 |
| w20 | 10 | -0.066833 | -9.665 |
| w21 | 29 | -0.009887 | 4.721 |
| w22 | 23 | -0.033996 | 18.886 |
| w23 | 11 | -0.014793 | 13.16 |
| w24 | 26 | 0.01852 | 22.724 |
| w25 | 23 | -0.030569 | -2.99 |
| w26 | 18 | 0.0521 | 11.735 |
| w27 | 19 | 0.273875 | 240.997 |
| w28 | 29 | -0.0667 | -12.241 |
| w29 | 21 | 0.13149 | 35.208 |
| w30 | 23 | -0.07781 | -19.011 |
| w31 | 21 | 0.016436 | -5.017 |
| w32 | 21 | 0.051311 | -3.175 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 10 | 0.198198 | 56.648 |
| w8 | 16 | -0.011405 | -14.479 |
| w9 | 20 | 0.003941 | -12.298 |
| w10 | 19 | 0.035017 | 37.882 |
| w11 | 25 | -0.018367 | 3.015 |
| w12 | 19 | 0.0542 | -0.177 |
| w13 | 25 | 0.073826 | 48.187 |
| w14 | 25 | 0.011984 | 2.489 |
| w15 | 37 | -0.129406 | -20.89 |
| w16 | 26 | 0.107248 | 87.016 |
| w17 | 29 | 0.03246 | 16.601 |
| w18 | 28 | -0.121126 | -23.493 |
| w19 | 18 | 0.103417 | 6.149 |
| w20 | 16 | 0.095096 | 3.497 |
| w21 | 31 | -0.09828 | -13.976 |
| w22 | 29 | -0.013635 | 5.734 |
| w23 | 17 | 0.306526 | 122.94 |
| w24 | 26 | -0.124992 | -9.448 |
| w25 | 18 | 0.136842 | 71.508 |
| w26 | 20 | -0.033039 | -16.422 |
| w27 | 37 | -0.047451 | 14.87 |
| w28 | 21 | -0.155051 | -27.583 |
| w29 | 49 | -0.101917 | -10.847 |
| w30 | 34 | -0.180266 | -25.897 |
| w31 | 30 | -0.110073 | -21.993 |
| w32 | 17 | 0.034115 | -8.573 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | 0.101033 | 123.991 |
| w2 | 28 | -0.062529 | -2.352 |
| w3 | 20 | 0.006413 | -4.69 |
| w4 | 42 | 0.063501 | 192.138 |
| w5 | 31 | 0.114402 | 92.359 |
| w6 | 18 | 0.009691 | 41.132 |
| w7 | 21 | 0.139119 | 48.099 |
| w8 | 14 | -0.065537 | -13.964 |
| w9 | 17 | 0.040933 | -6.513 |
| w10 | 24 | 0.036376 | 16.083 |
| w11 | 26 | 0.137869 | 49.496 |
| w12 | 11 | -0.071961 | -17.978 |
| w13 | 30 | -0.000622 | 41.975 |
| w14 | 26 | -0.012444 | 45.014 |
| w15 | 32 | -0.111235 | -7.027 |
| w16 | 39 | 0.036106 | 74.667 |
| w17 | 16 | 0.124478 | 44.259 |
| w18 | 48 | -0.045047 | -6.736 |
| w19 | 18 | 0.094076 | 17.009 |
| w20 | 22 | 0.004085 | -4.145 |
| w21 | 22 | 0.06853 | 10.238 |
| w22 | 33 | 0.008298 | 25.429 |
| w23 | 17 | -0.084309 | -17.665 |
| w24 | 34 | -0.062787 | 4.214 |
| w25 | 16 | 0.162894 | 79.195 |
| w26 | 12 | 0.013225 | 10.485 |
| w27 | 30 | -0.009267 | 17.827 |
| w28 | 19 | -0.10033 | -23.584 |
| w29 | 28 | 0.057255 | 57.681 |
| w30 | 20 | -0.091949 | -15.71 |
| w31 | 24 | -0.041071 | -21.309 |
| w32 | 25 | 0.011821 | -5.551 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 29 | 0.104882 | 65.475 |
| w11 | 23 | -0.122943 | -15.86 |
| w12 | 24 | -0.000516 | -9.528 |
| w13 | 23 | 0.058134 | 47.89 |
| w14 | 25 | -0.021465 | 35.389 |
| w15 | 24 | -0.022691 | 5.372 |
| w16 | 28 | 0.16464 | 125.832 |
| w17 | 26 | 0.151691 | 110.322 |
| w18 | 14 | -0.113539 | -12.436 |
| w19 | 17 | 0.040562 | -0.729 |
| w20 | 20 | -0.013633 | -1.216 |
| w21 | 12 | -0.097106 | -13.752 |
| w22 | 39 | -0.013104 | 21.547 |
| w23 | 27 | -0.28868 | -35.673 |
| w24 | 15 | 0.154917 | 147.718 |
| w25 | 18 | 0.059245 | 5.107 |
| w26 | 16 | -0.171724 | -27.705 |
| w27 | 26 | 0.248515 | 116.171 |
| w28 | 20 | -0.118296 | -13.904 |
| w29 | 16 | 0.106356 | 27.14 |
| w30 | 19 | -0.031005 | -12.539 |
| w31 | 25 | -0.076951 | -18.826 |
| w32 | 16 | -0.100957 | -24.699 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 39 | -0.078266 | -10.466 |
| w13 | 28 | -0.052177 | -14.672 |
| w14 | 23 | -0.00114 | 57.34 |
| w15 | 28 | -0.118309 | -16.787 |
| w16 | 26 | 0.01754 | 32.688 |
| w17 | 32 | 0.051887 | 12.185 |
| w18 | 22 | -0.047677 | -6.562 |
| w19 | 24 | -0.070725 | -13.559 |
| w20 | 29 | -0.122289 | -23.418 |
| w21 | 20 | 0.04018 | 8.466 |
| w22 | 27 | -0.035905 | -2.8 |
| w23 | 15 | -0.003283 | -4.557 |
| w24 | 30 | -0.040893 | 20.234 |
| w25 | 15 | 0.07854 | -2.957 |
| w26 | 13 | -0.127365 | -26.627 |
| w27 | 28 | 0.092071 | 40.006 |
| w28 | 14 | -0.013834 | -3.774 |
| w29 | 19 | -0.046237 | -18.379 |
| w30 | 12 | -0.098636 | -14.22 |
| w31 | 25 | 0.050861 | 1.471 |
| w32 | 27 | -0.029104 | -24.661 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 18 | -0.140873 | -23.308 |
| w16 | 31 | -0.013046 | 37.869 |
| w17 | 34 | 0.006338 | -8.61 |
| w18 | 31 | 0.063216 | 15.202 |
| w19 | 10 | 0.106013 | 2.859 |
| w20 | 24 | -0.022704 | -9.82 |
| w21 | 12 | -0.007055 | -8.145 |
| w22 | 26 | -0.033297 | -7.619 |
| w23 | 14 | -0.078567 | -11.905 |
| w24 | 31 | 0.003843 | 44.892 |
| w25 | 14 | 0.140192 | 27.751 |
| w26 | 21 | -0.041422 | -20.108 |
| w27 | 25 | 0.231921 | 138.63 |
| w28 | 15 | -0.022774 | -5.01 |
| w29 | 17 | -0.010602 | -7.004 |
| w30 | 17 | -0.08351 | -17.487 |
| w31 | 13 | 0.021661 | 3.673 |
| w32 | 24 | -0.197999 | -35.341 |

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
| w15 | 27 | 0.003872 | -2.949 |
| w16 | 33 | 0.035838 | 78.746 |
| w17 | 18 | 0.138116 | 38.484 |
| w18 | 26 | -0.130711 | -24.256 |
| w19 | 19 | 0.015591 | -7.635 |
| w20 | 25 | -0.21925 | -23.552 |
| w21 | 33 | -0.161807 | -19.817 |
| w22 | 30 | -0.126284 | -12.301 |
| w23 | 36 | -0.031967 | -10.219 |
| w24 | 34 | -0.079283 | 25.473 |
| w25 | 26 | 0.098293 | 31.412 |
| w26 | 41 | 0.066642 | 43.268 |
| w27 | 33 | -0.06557 | 12.9 |
| w28 | 44 | -0.121962 | -26.286 |
| w29 | 46 | -0.073904 | 17.268 |
| w30 | 30 | -0.050786 | -12.945 |
| w31 | 30 | 0.008549 | 12.029 |
| w32 | 37 | -0.033307 | -6.592 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 16 | -0.010997 | 43.35 |
| w17 | 19 | 0.099142 | 24.104 |
| w18 | 28 | -0.093591 | -20.574 |
| w19 | 23 | 0.020168 | -8.843 |
| w20 | 18 | -0.012598 | -6.888 |
| w21 | 20 | -0.049168 | -17.306 |
| w22 | 27 | -0.055882 | 5.289 |
| w23 | 18 | 0.079991 | -2.552 |
| w24 | 28 | 0.031333 | 50.857 |
| w25 | 21 | 0.116384 | 17.087 |
| w26 | 24 | -0.13493 | -28.779 |
| w27 | 29 | 0.095923 | 33.29 |
| w28 | 15 | 0.0315 | 1.141 |
| w29 | 17 | 0.002855 | -13.383 |
| w30 | 16 | 0.038746 | -2.553 |
| w31 | 18 | -0.047676 | -14.846 |
| w32 | 13 | -0.057658 | -20.954 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 23 | 0.017672 | -2.711 |
| w21 | 15 | 0.005716 | 2.436 |
| w22 | 35 | 0.01591 | 33.698 |
| w23 | 17 | -0.085348 | -15.666 |
| w24 | 26 | 0.186521 | 204.01 |
| w25 | 22 | 0.021009 | -3.18 |
| w26 | 19 | -0.110136 | -17.351 |
| w27 | 41 | -0.020507 | 11.3 |
| w28 | 21 | -0.073645 | -15.408 |
| w29 | 22 | -0.016754 | -5.121 |
| w30 | 12 | 0.064197 | 1.152 |
| w31 | 24 | -0.061406 | -19.444 |
| w32 | 16 | 0.038605 | 3.37 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 28 | 0.010047 | 16.17 |
| w23 | 17 | 0.011478 | -8.286 |
| w24 | 34 | -0.034303 | 78.332 |
| w25 | 18 | -0.035087 | 11.727 |
| w26 | 22 | -0.022824 | -6.034 |
| w27 | 27 | 0.040813 | 21.009 |
| w28 | 21 | -0.029443 | -7.898 |
| w29 | 21 | -0.013316 | -13.539 |
| w30 | 22 | -0.060598 | -14.835 |
| w31 | 24 | -0.019416 | -8.537 |
| w32 | 20 | 0.023451 | 24.957 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 30 | -0.080459 | 3.542 |
| w25 | 34 | -0.060521 | -11.998 |
| w26 | 21 | -0.097333 | -14.452 |
| w27 | 29 | 0.006231 | 64.798 |
| w28 | 21 | 0.02515 | -0.009 |
| w29 | 25 | -0.022118 | -4.01 |
| w30 | 19 | 0.003672 | -10.831 |
| w31 | 21 | 0.023982 | -3.369 |
| w32 | 26 | 0.053943 | 13.039 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 24 | 0.134018 | 103.075 |
| w6 | 25 | 0.041777 | 17.993 |
| w7 | 18 | 0.041838 | 7.526 |
| w8 | 22 | -0.167315 | -25.84 |
| w9 | 20 | -0.126711 | -30.761 |
| w10 | 19 | 0.050235 | 13.142 |
| w11 | 20 | 0.015643 | 6.458 |
| w12 | 21 | -0.048608 | -16.365 |
| w13 | 34 | 0.084898 | 57.922 |
| w14 | 31 | -0.048384 | 11.869 |
| w15 | 30 | -0.117033 | -25.699 |
| w16 | 18 | 0.108635 | 89.297 |
| w17 | 25 | 0.108757 | 27.916 |
| w18 | 25 | -0.19584 | -35.901 |
| w19 | 31 | 0.05317 | 11.808 |
| w20 | 20 | 0.004034 | -14.785 |
| w21 | 21 | -0.010102 | -10.987 |
| w22 | 33 | -0.099407 | -6.006 |
| w23 | 17 | 0.040184 | -0.677 |
| w24 | 42 | -0.129117 | -15.929 |
| w25 | 20 | 0.129716 | 5.915 |
| w26 | 28 | 0.06402 | 28.613 |
| w27 | 21 | -0.042748 | 7.618 |
| w28 | 29 | -0.129876 | -9.2 |
| w29 | 35 | -0.089548 | -18.552 |
| w30 | 31 | 0.132262 | 179.444 |
| w31 | 19 | 0.007267 | -1.547 |
| w32 | 29 | 0.043617 | 46.448 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 33 | 0.030763 | 99.071 |
| w6 | 15 | 0.150719 | 108.65 |
| w7 | 17 | -0.006605 | 1.723 |
| w8 | 17 | 0.02726 | -3.264 |
| w9 | 20 | -0.072807 | -26.828 |
| w10 | 24 | 0.018127 | 18.124 |
| w11 | 23 | 0.066886 | 22.376 |
| w12 | 29 | -0.082129 | -9.046 |
| w13 | 31 | 0.019797 | 39.131 |
| w14 | 29 | -0.044752 | 32.747 |
| w15 | 39 | -0.124262 | -7.141 |
| w16 | 28 | 0.017553 | 62.865 |
| w17 | 28 | 0.012029 | -3.15 |
| w18 | 20 | -0.022792 | -16.701 |
| w19 | 42 | -0.180725 | -18.582 |
| w20 | 34 | 0.035608 | -1.523 |
| w21 | 38 | -0.166053 | -24.063 |
| w22 | 31 | -0.097471 | -17.382 |
| w23 | 7 | 0.124191 | 14.179 |
| w24 | 37 | -0.103799 | -12.063 |
| w25 | 25 | -0.075201 | -34.262 |
| w26 | 36 | 0.043629 | 24.293 |
| w27 | 38 | -0.006199 | -5.839 |
| w28 | 40 | 0.006817 | 21.59 |
| w29 | 26 | 0.085522 | 21.6 |
| w30 | 35 | -0.146721 | -14.253 |
| w31 | 21 | -0.005591 | 10.655 |
| w32 | 36 | 0.014569 | 42.772 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 39 | -0.003992 | -6.819 |
| w18 | 32 | -0.088448 | -8.136 |
| w19 | 21 | 0.028051 | -7.261 |
| w20 | 23 | -0.021494 | 4.081 |
| w21 | 15 | -0.056218 | -9.378 |
| w22 | 20 | 0.097945 | 25.75 |
| w23 | 20 | 0.028009 | -5.351 |
| w24 | 17 | 0.050771 | 24.293 |
| w25 | 15 | 0.11556 | 10.582 |
| w26 | 12 | 0.032255 | -5.955 |
| w27 | 21 | 0.237975 | 174.558 |
| w28 | 20 | 0.014116 | 4.671 |
| w29 | 19 | 0.162339 | 32.37 |
| w30 | 15 | -0.112777 | -19.646 |
| w31 | 24 | -0.069457 | -19.61 |
| w32 | 25 | -0.108035 | -7.778 |

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
| w17 | 25 | -0.05361 | -12.061 |
| w18 | 20 | -0.014931 | -22.624 |
| w19 | 14 | 0.019308 | -4.405 |
| w20 | 27 | 0.000712 | -2.926 |
| w21 | 20 | -0.042094 | -16.3 |
| w22 | 24 | 0.041225 | 9.962 |
| w23 | 21 | 0.10295 | 3.221 |
| w24 | 39 | -0.030199 | 10.061 |
| w25 | 21 | -0.014712 | -6.002 |
| w26 | 29 | -0.108832 | -13.22 |
| w27 | 25 | -0.019579 | 26.463 |
| w28 | 15 | 0.009513 | -1.341 |
| w29 | 47 | -0.065784 | -0.3 |
| w30 | 19 | -0.021125 | -13.238 |
| w31 | 19 | -0.093839 | -15.388 |
| w32 | 33 | 0.00701 | 16.937 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 19 | 0.079128 | 15.272 |
| w20 | 23 | -0.025053 | -16.882 |
| w21 | 26 | -0.154809 | -20.89 |
| w22 | 33 | -0.040676 | 90.494 |
| w23 | 21 | -0.037881 | -8.685 |
| w24 | 40 | 0.10347 | 186.143 |
| w25 | 18 | -0.073521 | -17.545 |
| w26 | 29 | -0.072776 | -19.29 |
| w27 | 33 | 0.000742 | 7.467 |
| w28 | 21 | -0.011637 | -11.129 |
| w29 | 34 | 0.00135 | -16.226 |
| w30 | 16 | -0.054415 | -17.457 |
| w31 | 27 | -0.030349 | -15.893 |
| w32 | 37 | -0.036059 | 13.202 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 28 | 0.040686 | 34.411 |
| w23 | 21 | -0.077526 | -16.498 |
| w24 | 33 | -0.137644 | -15.648 |
| w25 | 21 | -0.101912 | -27.804 |
| w26 | 20 | -0.046632 | -17.046 |
| w27 | 22 | -0.040628 | -0.595 |
| w28 | 23 | -0.062856 | -20.111 |
| w29 | 20 | -0.008963 | -2.976 |
| w30 | 18 | -0.074832 | -11.154 |
| w31 | 25 | -0.005296 | -9.214 |
| w32 | 24 | 0.147447 | 34.881 |

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
| w27 | 34 | 0.05338 | 40.176 |
| w28 | 21 | -0.089967 | -27.154 |
| w29 | 26 | 0.014659 | -3.5 |
| w30 | 8 | 0.028187 | -6.943 |
| w31 | 22 | -0.098417 | -22.989 |
| w32 | 28 | -0.008384 | 27.11 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 21 | 0.12484 | 24.33 |
| w18 | 19 | -0.063436 | -15.431 |
| w19 | 8 | 0.118973 | 13.012 |
| w20 | 11 | 0.028718 | -5.638 |
| w21 | 18 | -0.083655 | -15.988 |
| w22 | 27 | -0.035578 | 10.732 |
| w23 | 17 | -0.064297 | -16.236 |
| w24 | 35 | -0.06096 | 17.389 |
| w25 | 15 | 0.077111 | 12.674 |
| w26 | 22 | -0.06176 | -16.039 |
| w27 | 28 | 0.015631 | 10.327 |
| w28 | 20 | -0.022915 | -5.339 |
| w29 | 20 | -0.052609 | -21.785 |
| w30 | 24 | -0.129933 | -31.195 |
| w31 | 26 | -0.006826 | -11.295 |
| w32 | 28 | -0.081277 | -21.547 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 17 | 0.152824 | 39.1 |
| w18 | 24 | -0.080452 | -19.208 |
| w19 | 13 | -0.024991 | -11.757 |
| w20 | 30 | -0.03766 | -17.987 |
| w21 | 20 | -0.065621 | -18.953 |
| w22 | 29 | 0.050813 | 76.04 |
| w23 | 21 | -0.189219 | -40.654 |
| w24 | 31 | -0.038318 | 41.834 |
| w25 | 22 | 0.092858 | 38.821 |
| w26 | 25 | -0.107688 | -18.313 |
| w27 | 25 | 0.060287 | 11.225 |
| w28 | 17 | 0.025976 | -6.634 |
| w29 | 15 | -0.039644 | -18.748 |
| w30 | 9 | -0.029084 | -11.33 |
| w31 | 26 | -0.074488 | -18.295 |
| w32 | 11 | 0.004165 | -11.931 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 23 | 0.087951 | -4.998 |
| w29 | 20 | 0.030329 | 0.311 |
| w30 | 27 | -0.175098 | -30.3 |
| w31 | 17 | 0.222682 | 53.232 |
| w32 | 24 | 0.016451 | 0.708 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 25 | 0.004291 | 46.831 |
| w15 | 25 | 0.027573 | 31.373 |
| w16 | 21 | -0.011734 | 233.047 |
| w17 | 23 | -0.011486 | 4.276 |
| w18 | 21 | -0.112399 | -23.942 |
| w19 | 21 | -0.031517 | -5.478 |
| w20 | 17 | 0.017264 | -3.441 |
| w21 | 22 | 0.150256 | 84.741 |
| w22 | 34 | -0.153528 | -4.707 |
| w23 | 23 | -0.034668 | -10.95 |
| w24 | 34 | -0.025258 | 0.378 |
| w25 | 22 | 0.155786 | 99.518 |
| w26 | 25 | -0.015621 | -4.374 |
| w27 | 34 | 0.18632 | 140.501 |
| w28 | 18 | -0.161272 | -27.715 |
| w29 | 19 | 0.102736 | 22.51 |
| w30 | 10 | 0.050075 | 2.161 |
| w31 | 25 | -0.029282 | -0.74 |
| w32 | 15 | 0.116083 | 14.202 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 18 | 0.282033 | 184.987 |
| w26 | 20 | 0.038382 | 5.345 |
| w27 | 38 | 0.130703 | 66.202 |
| w28 | 20 | 0.041932 | -6.127 |
| w29 | 17 | 0.025348 | -1.782 |
| w30 | 18 | -0.007815 | -14.152 |
| w31 | 23 | -0.008334 | -5.536 |
| w32 | 21 | -0.000505 | -5.483 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

