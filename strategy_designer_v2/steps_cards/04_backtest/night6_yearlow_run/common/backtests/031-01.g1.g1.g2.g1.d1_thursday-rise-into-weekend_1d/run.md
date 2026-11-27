# Backtest of 031-01.g1.g1.g2.g1.d1_thursday-rise-into-weekend_1d

- Plan: `../../../../../03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.g2.g1.d1_thursday-rise-into-weekend_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.053435 | 4.118 |
| w2 | 9 | 0.10877 | 27.055 |
| w3 | 23 | 0.130644 | 32.008 |
| w4 | 20 | -0.11275 | -15.936 |
| w5 | 20 | -0.072043 | 4.785 |
| w6 | 21 | 0.061489 | 26.413 |
| w7 | 10 | 0.077057 | 6.933 |
| w8 | 6 | 0.032354 | 3.619 |
| w9 | 6 | -0.01265 | -0.553 |
| w10 | 15 | 0.072112 | 14.743 |
| w11 | 15 | 0.088477 | 28.87 |
| w12 | 7 | -0.108275 | -5.713 |
| w13 | 14 | -0.035947 | -2.357 |
| w14 | 9 | -0.093954 | 6.392 |
| w15 | 20 | -0.011389 | 15.661 |
| w16 | 13 | 0.001831 | 3.589 |
| w17 | 12 | 0.234157 | 23.071 |
| w18 | 9 | 0.106425 | 7.664 |
| w19 | 9 | -0.061407 | -4.676 |
| w20 | 6 | -0.059995 | -4.044 |
| w21 | 9 | 0.103959 | 5.102 |
| w22 | 14 | 0.144316 | 36.481 |
| w23 | 5 | 0.066796 | 2.212 |
| w24 | 21 | 0.016835 | 10.699 |
| w25 | 11 | -0.026497 | -5.276 |
| w26 | 8 | 0.145783 | 16.243 |
| w27 | 13 | 0.051715 | 6.024 |
| w28 | 8 | -0.026438 | -5.422 |
| w29 | 15 | -0.103249 | -7.13 |
| w30 | 8 | -0.268551 | -20.488 |
| w31 | 17 | 0.04172 | -0.682 |
| w32 | 13 | 0.085948 | 1.431 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.009623 | -7.348 |
| w2 | 11 | 0.184994 | 20.361 |
| w3 | 16 | -0.080513 | -3.739 |
| w4 | 12 | -0.167936 | -16.368 |
| w5 | 13 | -0.078684 | -2.293 |
| w6 | 18 | 0.012793 | 44.075 |
| w7 | 8 | 0.075186 | 2.356 |
| w8 | 8 | 0.098512 | 2.711 |
| w9 | 4 | 0.064208 | 1.029 |
| w10 | 17 | 0.044145 | 16.768 |
| w11 | 13 | 0.108248 | 9.61 |
| w12 | 5 | -0.0677 | -3.959 |
| w13 | 14 | 0.029187 | 8.413 |
| w14 | 11 | -0.062829 | 10.419 |
| w15 | 21 | 0.139784 | 34.463 |
| w16 | 17 | 0.101265 | 24.131 |
| w17 | 11 | 0.102334 | 9.438 |
| w18 | 12 | -0.011874 | 0.784 |
| w19 | 5 | -0.125152 | -7.092 |
| w20 | 5 | -0.111979 | -7.296 |
| w21 | 10 | 0.050187 | 12.566 |
| w22 | 17 | 0.077743 | 5.61 |
| w23 | 13 | 0.306651 | 18.443 |
| w24 | 13 | -0.08431 | -0.472 |
| w25 | 11 | 0.004734 | 18.261 |
| w26 | 9 | 0.13786 | 3.845 |
| w27 | 14 | 0.081766 | 35.5 |
| w28 | 11 | 0.069319 | -1.35 |
| w29 | 17 | -0.01342 | 12.705 |
| w30 | 7 | -0.471451 | -31.98 |
| w31 | 12 | 0.055661 | -2.4 |
| w32 | 10 | 0.158136 | 4.684 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 15 | -0.070663 | 0.127 |
| w7 | 8 | 0.137046 | 8.377 |
| w8 | 6 | 0.027684 | 0.156 |
| w9 | 11 | 0.188511 | 14.656 |
| w10 | 7 | 0.169864 | 7.703 |
| w11 | 7 | -0.068793 | -6.539 |
| w12 | 8 | -0.100683 | -8.83 |
| w13 | 15 | 0.007835 | -3.291 |
| w14 | 12 | 0.014131 | 29.144 |
| w15 | 9 | 0.014445 | 98.868 |
| w16 | 13 | -0.025839 | 13.98 |
| w17 | 11 | 0.107522 | 23.16 |
| w18 | 7 | -0.136849 | -7.025 |
| w19 | 8 | -0.073833 | 4.955 |
| w20 | 3 | -0.082088 | 1.666 |
| w21 | 4 | 0.055402 | -2.078 |
| w22 | 13 | 0.043169 | 3.013 |
| w23 | 7 | -0.068444 | -9.37 |
| w24 | 12 | -0.03517 | -1.578 |
| w25 | 8 | -0.072915 | -10.547 |
| w26 | 8 | -0.008211 | 2.273 |
| w27 | 14 | 0.399376 | 126.723 |
| w28 | 6 | -0.049834 | -3.01 |
| w29 | 13 | 0.020305 | 4.89 |
| w30 | 5 | -0.15432 | -5.879 |
| w31 | 12 | 0.039391 | -3.968 |
| w32 | 7 | 0.124886 | 6.015 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 7 | 0.089823 | 10.829 |
| w8 | 9 | -0.010729 | 6.914 |
| w9 | 8 | 0.05239 | -2.485 |
| w10 | 15 | 0.061271 | 12.421 |
| w11 | 9 | -0.118569 | -3.417 |
| w12 | 5 | -0.122017 | -5.172 |
| w13 | 14 | 0.074296 | 3.706 |
| w14 | 10 | 0.016513 | 7.65 |
| w15 | 15 | -0.032864 | -0.538 |
| w16 | 13 | 0.091807 | 31.919 |
| w17 | 11 | 0.009684 | 5.879 |
| w18 | 5 | 0.009236 | 0.024 |
| w19 | 6 | -0.084407 | -7.412 |
| w20 | 5 | -0.002752 | -4.248 |
| w21 | 8 | 0.116265 | 3.218 |
| w22 | 12 | 0.04848 | 6.44 |
| w23 | 8 | 0.485352 | 68.956 |
| w24 | 12 | -0.139357 | -1.452 |
| w25 | 17 | -0.000447 | 46.188 |
| w26 | 8 | 0.008644 | -0.584 |
| w27 | 20 | 0.019493 | 9.948 |
| w28 | 11 | 0.049896 | -0.696 |
| w29 | 20 | -0.072189 | -18.184 |
| w30 | 17 | -0.140315 | -13.326 |
| w31 | 8 | 0.039786 | 2.942 |
| w32 | 7 | 0.068276 | 6.257 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.002368 | 27.877 |
| w2 | 10 | -0.166335 | -31.896 |
| w3 | 7 | 0.037881 | -2.888 |
| w4 | 22 | 0.049617 | 6.783 |
| w5 | 17 | -0.071445 | 3.593 |
| w6 | 13 | -0.016247 | 16.68 |
| w7 | 11 | 0.083231 | 20.091 |
| w8 | 7 | 0.024313 | 1.753 |
| w9 | 7 | 0.149296 | 9.814 |
| w10 | 15 | 0.099676 | 10.444 |
| w11 | 11 | -0.014132 | 7.008 |
| w12 | 8 | -0.099773 | -6.85 |
| w13 | 16 | 0.040944 | 10.652 |
| w14 | 14 | -0.026168 | 42.131 |
| w15 | 15 | -0.032976 | 14.743 |
| w16 | 20 | -0.061317 | 1.387 |
| w17 | 13 | 0.13325 | 30.416 |
| w18 | 12 | -0.03095 | -3.448 |
| w19 | 6 | -0.035825 | -2.415 |
| w20 | 8 | -0.053787 | -3.205 |
| w21 | 5 | 0.160143 | 13.084 |
| w22 | 17 | 0.100929 | 18.442 |
| w23 | 9 | 0.091249 | -0.864 |
| w24 | 15 | -0.091182 | -4.295 |
| w25 | 13 | -0.049257 | -4.45 |
| w26 | 7 | 0.011432 | 3.019 |
| w27 | 16 | 0.078396 | 24.238 |
| w28 | 5 | -0.023641 | -1.204 |
| w29 | 17 | -0.013106 | 11.972 |
| w30 | 4 | -0.349209 | -15.288 |
| w31 | 14 | 0.058374 | 0.731 |
| w32 | 8 | 0.101545 | 3.465 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 18 | 0.223252 | 44.947 |
| w11 | 7 | -0.03521 | -3.288 |
| w12 | 9 | -0.045561 | -3.859 |
| w13 | 19 | 0.002669 | 1.816 |
| w14 | 14 | -0.128428 | 11.488 |
| w15 | 15 | -0.03534 | 27.076 |
| w16 | 18 | 0.03522 | 38.69 |
| w17 | 15 | 0.143015 | 34.504 |
| w18 | 5 | -0.09642 | -3.661 |
| w19 | 4 | -0.035089 | -0.287 |
| w20 | 8 | -0.124519 | -6.531 |
| w21 | 6 | 0.259513 | 11.698 |
| w22 | 18 | 0.179231 | 23.879 |
| w23 | 4 | -0.154606 | -7.552 |
| w24 | 11 | 0.084905 | 32.439 |
| w25 | 9 | -0.01552 | -1.606 |
| w26 | 6 | 0.106708 | 4.849 |
| w27 | 15 | 0.447331 | 95.534 |
| w28 | 11 | -0.052695 | -3.601 |
| w29 | 14 | 0.064086 | 7.085 |
| w30 | 4 | -0.272537 | -9.548 |
| w31 | 8 | 0.021956 | -4.573 |
| w32 | 11 | -0.071903 | -12.219 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 16 | -0.034253 | -2.8 |
| w13 | 11 | -0.091797 | -15.53 |
| w14 | 19 | -0.045488 | 10.996 |
| w15 | 13 | -0.028409 | 4.196 |
| w16 | 14 | 0.168622 | 17.863 |
| w17 | 14 | 0.206222 | 42.059 |
| w18 | 15 | 0.033718 | 10.624 |
| w19 | 8 | -0.071984 | -8.29 |
| w20 | 12 | -0.034787 | -8.495 |
| w21 | 12 | 0.334399 | 16.064 |
| w22 | 15 | 0.185698 | 17.953 |
| w23 | 7 | 0.022821 | -0.632 |
| w24 | 15 | -0.086545 | 8.697 |
| w25 | 10 | -0.105856 | -14.231 |
| w26 | 8 | -0.056815 | -3.551 |
| w27 | 15 | 0.227374 | 45.799 |
| w28 | 4 | -0.118232 | -6.829 |
| w29 | 10 | -0.14501 | -11.445 |
| w30 | 3 | -0.223793 | -7.207 |
| w31 | 14 | 0.224493 | 13.806 |
| w32 | 9 | 0.001281 | 0.786 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 7 | -0.008105 | 6.546 |
| w16 | 15 | 0.292621 | 50.97 |
| w17 | 11 | 0.134089 | 9.711 |
| w18 | 9 | -0.142899 | -8.347 |
| w19 | 6 | -0.007548 | -3.76 |
| w20 | 7 | -0.059661 | -1.994 |
| w21 | 7 | 0.220009 | 19.966 |
| w22 | 15 | 0.159645 | 12.785 |
| w23 | 3 | 0.062532 | 2.467 |
| w24 | 19 | 0.068572 | 34.807 |
| w25 | 11 | -0.014077 | -8.828 |
| w26 | 10 | 0.168483 | 4.968 |
| w27 | 16 | 0.578221 | 122.513 |
| w28 | 10 | 0.013124 | -1.83 |
| w29 | 11 | -0.095222 | -8.874 |
| w30 | 2 | -0.280175 | -12.705 |
| w31 | 12 | 0.19788 | 7.291 |
| w32 | 9 | 0.007339 | -6.544 |

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
| w15 | 9 | -0.155237 | -12.75 |
| w16 | 14 | 0.022359 | 27.257 |
| w17 | 9 | 0.080981 | 12.673 |
| w18 | 12 | -0.099056 | -0.522 |
| w19 | 8 | -0.150129 | -12.796 |
| w20 | 13 | 0.044868 | 1.64 |
| w21 | 9 | -0.032586 | -1.204 |
| w22 | 14 | 0.088794 | 12.467 |
| w23 | 16 | 0.215451 | 32.0 |
| w24 | 20 | 0.062643 | 19.652 |
| w25 | 10 | 0.090973 | 10.223 |
| w26 | 19 | 0.07575 | 14.804 |
| w27 | 13 | 0.017816 | 30.031 |
| w28 | 12 | -0.127614 | -2.482 |
| w29 | 18 | 0.011353 | -1.358 |
| w30 | 3 | -0.172602 | -3.559 |
| w31 | 20 | -0.015382 | 16.104 |
| w32 | 13 | 0.025515 | 0.058 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 19 | -0.001394 | 26.776 |
| w17 | 13 | 0.148743 | 16.961 |
| w18 | 13 | 0.001662 | -0.577 |
| w19 | 8 | -0.042208 | -0.41 |
| w20 | 8 | 0.115108 | 4.225 |
| w21 | 4 | 0.279006 | 9.657 |
| w22 | 12 | 0.090226 | 23.75 |
| w23 | 7 | 0.131994 | 6.481 |
| w24 | 12 | -0.094447 | 15.436 |
| w25 | 11 | -0.030533 | -14.903 |
| w26 | 6 | 0.09456 | 1.929 |
| w27 | 14 | 0.208046 | 74.072 |
| w28 | 5 | -0.066879 | -7.93 |
| w29 | 12 | -0.040049 | -1.898 |
| w30 | 5 | -0.233909 | -16.423 |
| w31 | 12 | 0.04128 | 0.282 |
| w32 | 8 | -0.033776 | -9.604 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 9 | -0.040271 | -1.104 |
| w21 | 5 | 0.208171 | 13.12 |
| w22 | 16 | 0.141881 | 14.273 |
| w23 | 6 | 0.151069 | 2.994 |
| w24 | 14 | 0.087533 | 63.347 |
| w25 | 8 | 0.072114 | -1.102 |
| w26 | 11 | 0.15013 | 6.405 |
| w27 | 20 | 0.303156 | 38.665 |
| w28 | 4 | -0.068549 | -3.817 |
| w29 | 13 | -0.118926 | -3.99 |
| w30 | 5 | -0.067518 | -3.876 |
| w31 | 13 | 0.022308 | -3.829 |
| w32 | 12 | 0.061445 | -7.039 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 15 | 0.158793 | 27.596 |
| w23 | 6 | 0.00811 | 0.785 |
| w24 | 15 | -0.03675 | 33.35 |
| w25 | 13 | -0.116104 | 0.74 |
| w26 | 14 | 0.153347 | 6.253 |
| w27 | 13 | 0.07728 | 16.056 |
| w28 | 4 | -0.031934 | -3.973 |
| w29 | 12 | -0.056312 | -1.407 |
| w30 | 5 | -0.111151 | -6.7 |
| w31 | 16 | -0.058325 | -5.63 |
| w32 | 12 | 0.00754 | 11.214 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 13 | 0.033906 | 18.851 |
| w25 | 15 | 0.055809 | -0.835 |
| w26 | 7 | 0.034517 | 5.118 |
| w27 | 18 | 0.057915 | 17.356 |
| w28 | 10 | -0.018131 | -4.02 |
| w29 | 9 | -0.139468 | -7.935 |
| w30 | 6 | -0.3227 | -21.095 |
| w31 | 12 | 0.047599 | -2.755 |
| w32 | 10 | -0.049119 | -4.563 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 14 | -0.091292 | -5.303 |
| w6 | 10 | -0.256213 | -20.172 |
| w7 | 8 | 0.036176 | 2.663 |
| w8 | 6 | -0.062552 | -3.238 |
| w9 | 6 | -0.058983 | -8.098 |
| w10 | 12 | 0.176676 | 13.163 |
| w11 | 13 | 0.088552 | 4.086 |
| w12 | 7 | -0.077928 | -7.123 |
| w13 | 15 | 0.084689 | 2.258 |
| w14 | 14 | -0.012744 | 30.154 |
| w15 | 12 | -0.073393 | 5.809 |
| w16 | 21 | 0.024645 | 26.632 |
| w17 | 14 | 0.144869 | 13.216 |
| w18 | 10 | -0.10868 | -14.001 |
| w19 | 10 | -0.069299 | -5.74 |
| w20 | 10 | -0.066421 | -4.261 |
| w21 | 7 | -0.024671 | -1.631 |
| w22 | 13 | -0.027427 | -1.005 |
| w23 | 5 | 0.210596 | 8.494 |
| w24 | 18 | -0.018974 | 6.359 |
| w25 | 9 | 0.016505 | 8.641 |
| w26 | 19 | 0.098639 | 14.26 |
| w27 | 15 | -0.046691 | 6.562 |
| w28 | 9 | 0.00145 | -2.266 |
| w29 | 10 | -0.224337 | -8.94 |
| w30 | 17 | 0.064914 | 41.048 |
| w31 | 7 | -0.051509 | -4.392 |
| w32 | 14 | 0.07481 | 24.299 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 19 | 0.026621 | 16.268 |
| w6 | 14 | -0.115901 | 9.882 |
| w7 | 9 | 0.087135 | 5.19 |
| w8 | 5 | 0.155895 | 4.859 |
| w9 | 9 | -0.05015 | -9.664 |
| w10 | 17 | 0.160516 | 14.36 |
| w11 | 12 | 0.004062 | 6.275 |
| w12 | 6 | -0.060834 | -2.852 |
| w13 | 16 | -0.021211 | -3.68 |
| w14 | 16 | -0.084681 | 10.343 |
| w15 | 17 | -0.09061 | 7.528 |
| w16 | 20 | 0.098526 | 37.65 |
| w17 | 13 | 0.107432 | 14.573 |
| w18 | 9 | -0.010346 | -3.624 |
| w19 | 13 | -0.126107 | -1.136 |
| w20 | 11 | -0.070923 | -9.035 |
| w21 | 12 | 0.092756 | 4.295 |
| w22 | 12 | 0.184239 | 19.1 |
| w23 | 6 | 0.178404 | 12.117 |
| w24 | 21 | 0.000429 | -4.091 |
| w25 | 8 | 0.064566 | -0.096 |
| w26 | 20 | -0.045121 | 14.905 |
| w27 | 14 | 0.082027 | 9.757 |
| w28 | 12 | -0.014172 | -5.167 |
| w29 | 10 | 0.104023 | 17.101 |
| w30 | 19 | -0.171807 | -4.762 |
| w31 | 10 | -0.142976 | -15.95 |
| w32 | 15 | 0.014771 | 15.304 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 15 | 0.217901 | 7.803 |
| w18 | 12 | -0.210182 | -16.795 |
| w19 | 6 | -0.051377 | -0.829 |
| w20 | 7 | -0.105767 | -8.142 |
| w21 | 6 | 0.140036 | 4.197 |
| w22 | 14 | 0.324744 | 23.99 |
| w23 | 8 | 0.129821 | 5.659 |
| w24 | 15 | 0.073497 | 14.118 |
| w25 | 10 | 0.005789 | -6.568 |
| w26 | 11 | 0.134394 | 5.848 |
| w27 | 13 | 0.21541 | 74.387 |
| w28 | 8 | -0.16228 | -10.668 |
| w29 | 11 | 0.085993 | 9.43 |
| w30 | 2 | -0.310454 | -26.814 |
| w31 | 10 | 0.06205 | -1.808 |
| w32 | 15 | -0.074843 | -18.531 |

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
| w17 | 13 | 0.080577 | 6.098 |
| w18 | 7 | 0.033116 | -1.577 |
| w19 | 7 | 0.061069 | 0.342 |
| w20 | 7 | -0.095748 | -4.464 |
| w21 | 9 | 0.133999 | 6.579 |
| w22 | 11 | 0.061035 | 5.22 |
| w23 | 10 | 0.299149 | 10.828 |
| w24 | 18 | -0.081195 | -6.338 |
| w25 | 11 | -0.005208 | -3.53 |
| w26 | 15 | 0.03403 | -5.362 |
| w27 | 18 | 0.089608 | 17.157 |
| w28 | 4 | -0.06099 | -3.414 |
| w29 | 18 | -0.03311 | -1.097 |
| w30 | 3 | -0.22224 | -6.108 |
| w31 | 9 | -0.046671 | -13.46 |
| w32 | 13 | 0.223887 | 25.879 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 7 | 0.244741 | 23.841 |
| w20 | 7 | -0.050181 | -8.869 |
| w21 | 10 | 0.100997 | 10.415 |
| w22 | 19 | -0.007889 | 13.994 |
| w23 | 12 | 0.073154 | 5.424 |
| w24 | 22 | 0.062699 | 37.661 |
| w25 | 6 | 0.006485 | -10.115 |
| w26 | 10 | 0.0243 | -4.622 |
| w27 | 19 | 0.165505 | 17.145 |
| w28 | 5 | -0.054083 | -3.002 |
| w29 | 15 | -0.116305 | -4.236 |
| w30 | 2 | -0.254501 | -13.274 |
| w31 | 11 | 0.043216 | 1.849 |
| w32 | 18 | -0.018228 | -3.813 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 18 | 0.205376 | 17.102 |
| w23 | 10 | 0.094313 | -1.363 |
| w24 | 17 | 0.08278 | 15.343 |
| w25 | 7 | 0.095806 | -8.379 |
| w26 | 10 | -0.028081 | -6.054 |
| w27 | 15 | 0.109592 | 11.403 |
| w28 | 10 | 0.052201 | -0.707 |
| w29 | 14 | 0.062379 | 9.383 |
| w30 | 2 | -0.348454 | -8.668 |
| w31 | 9 | 0.017801 | -10.323 |
| w32 | 9 | -0.005579 | -5.899 |

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
| w27 | 19 | 0.191779 | 29.969 |
| w28 | 6 | -0.046955 | -6.739 |
| w29 | 12 | -0.088327 | -6.463 |
| w30 | 3 | -0.069995 | -4.522 |
| w31 | 10 | 0.052199 | -1.956 |
| w32 | 8 | 0.034869 | -4.732 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 10 | 0.182342 | 19.851 |
| w18 | 9 | -0.103559 | -3.927 |
| w19 | 5 | -0.035686 | -7.989 |
| w20 | 6 | 0.087496 | 26.559 |
| w21 | 3 | 0.150796 | 7.936 |
| w22 | 14 | -0.05717 | 15.554 |
| w23 | 9 | -0.030774 | -2.947 |
| w24 | 15 | -0.18254 | 2.543 |
| w25 | 12 | 0.017811 | 6.706 |
| w26 | 9 | 0.210538 | 6.86 |
| w27 | 17 | 0.206728 | 56.111 |
| w28 | 6 | -0.037959 | -3.452 |
| w29 | 11 | -0.051717 | -8.152 |
| w30 | 7 | 0.262964 | -0.868 |
| w31 | 12 | -0.023007 | -8.047 |
| w32 | 8 | 0.291746 | 3.155 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 10 | 0.062147 | 2.433 |
| w18 | 11 | 0.018928 | -4.627 |
| w19 | 7 | -0.124184 | -5.697 |
| w20 | 8 | 0.146258 | 8.258 |
| w21 | 5 | 0.167003 | 7.386 |
| w22 | 17 | 0.12215 | 39.146 |
| w23 | 8 | -0.021447 | -0.517 |
| w24 | 14 | -0.003653 | 10.993 |
| w25 | 11 | 0.031953 | 19.552 |
| w26 | 12 | 0.165178 | 5.23 |
| w27 | 15 | 0.15955 | 24.044 |
| w28 | 4 | 0.02013 | -1.056 |
| w29 | 11 | -0.090107 | -8.453 |
| w30 | 4 | -0.117212 | -6.93 |
| w31 | 11 | 0.116062 | -0.857 |
| w32 | 8 | -0.033399 | -14.728 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 7 | -0.013958 | -3.18 |
| w29 | 13 | 0.048058 | 0.067 |
| w30 | 9 | -0.090898 | -9.165 |
| w31 | 14 | -0.081972 | -3.94 |
| w32 | 8 | -0.035042 | -10.962 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 10 | -0.166502 | -0.506 |
| w15 | 12 | 0.039041 | 50.312 |
| w16 | 14 | 0.063748 | 27.899 |
| w17 | 12 | 0.170069 | 9.08 |
| w18 | 8 | -0.045286 | -6.047 |
| w19 | 7 | -0.053987 | -2.287 |
| w20 | 6 | -0.085905 | -3.317 |
| w21 | 10 | 0.070054 | 61.197 |
| w22 | 16 | 0.003956 | 1.632 |
| w23 | 8 | 0.033363 | 8.483 |
| w24 | 12 | 0.072557 | 1.553 |
| w25 | 13 | 0.093123 | 10.66 |
| w26 | 9 | 0.210276 | 13.496 |
| w27 | 20 | 0.068914 | 39.073 |
| w28 | 5 | 0.017597 | -2.942 |
| w29 | 14 | 0.054772 | 12.056 |
| w30 | 4 | -0.206032 | -11.009 |
| w31 | 11 | 0.035838 | -5.877 |
| w32 | 6 | 0.187689 | 10.897 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 7 | 0.197014 | 28.481 |
| w26 | 12 | 0.071019 | 2.907 |
| w27 | 15 | 0.157702 | 15.915 |
| w28 | 9 | -0.012006 | -3.419 |
| w29 | 7 | -0.055899 | -2.497 |
| w30 | 5 | -0.147875 | -7.188 |
| w31 | 14 | 0.19019 | 7.184 |
| w32 | 10 | 0.332187 | 19.989 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

