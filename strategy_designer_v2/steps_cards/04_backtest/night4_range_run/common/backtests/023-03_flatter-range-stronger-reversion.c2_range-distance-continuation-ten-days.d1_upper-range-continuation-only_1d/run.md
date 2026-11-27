# Backtest of 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only_1d

- Plan: `../../../../../03_test_plan/night4_range_run/plans/023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | -0.041652 | -3.892 |
| w2 | 19 | 0.128027 | 68.296 |
| w3 | 43 | -0.064706 | 89.745 |
| w4 | 29 | -0.011202 | -24.404 |
| w5 | 30 | 0.027634 | 94.682 |
| w6 | 27 | 0.099174 | 94.709 |
| w7 | 10 | -0.039651 | -3.938 |
| w8 | 10 | 0.072256 | 5.776 |
| w9 | 16 | -0.115814 | -42.832 |
| w10 | 32 | 0.054473 | 41.836 |
| w11 | 30 | 0.012298 | 37.88 |
| w12 | 12 | -0.000632 | -16.398 |
| w13 | 27 | 0.040207 | 33.056 |
| w14 | 31 | -0.029605 | 18.199 |
| w15 | 30 | 0.141118 | 136.051 |
| w16 | 34 | -0.044486 | 25.392 |
| w17 | 25 | 0.092189 | 2.88 |
| w18 | 14 | 0.069201 | -1.085 |
| w19 | 19 | -0.039787 | -11.492 |
| w20 | 14 | 0.046714 | -13.076 |
| w21 | 13 | -0.074459 | -26.889 |
| w22 | 27 | -0.024689 | 56.272 |
| w23 | 13 | 0.074058 | 5.719 |
| w24 | 36 | -0.03199 | 61.039 |
| w25 | 27 | 0.05219 | 33.887 |
| w26 | 24 | -0.056643 | -15.525 |
| w27 | 34 | -0.003413 | 63.409 |
| w28 | 15 | 0.004981 | 1.826 |
| w29 | 37 | 0.04091 | 11.406 |
| w30 | 13 | -0.010035 | -18.719 |
| w31 | 27 | -0.016903 | -3.793 |
| w32 | 22 | 0.109499 | 21.5 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | -0.090919 | 5.108 |
| w2 | 21 | 0.089668 | 17.867 |
| w3 | 23 | -0.194019 | -21.463 |
| w4 | 15 | 0.086057 | 112.303 |
| w5 | 28 | -0.014462 | 73.635 |
| w6 | 27 | 0.10447 | 69.078 |
| w7 | 15 | -0.061396 | -8.156 |
| w8 | 7 | 0.016194 | -13.402 |
| w9 | 9 | -0.204343 | -21.342 |
| w10 | 31 | -0.025435 | 30.378 |
| w11 | 19 | 0.070639 | 15.087 |
| w12 | 15 | -0.00945 | -29.649 |
| w13 | 25 | 0.040418 | 29.953 |
| w14 | 30 | -0.135305 | 12.955 |
| w15 | 20 | -0.022459 | 56.737 |
| w16 | 26 | -0.030564 | 17.225 |
| w17 | 23 | 0.077081 | 4.972 |
| w18 | 17 | 0.098511 | 10.787 |
| w19 | 12 | -0.007821 | -11.799 |
| w20 | 15 | -0.012964 | -6.44 |
| w21 | 15 | -0.08108 | -0.012 |
| w22 | 35 | -0.031438 | -0.727 |
| w23 | 14 | -0.133392 | -15.496 |
| w24 | 31 | -0.144866 | -14.854 |
| w25 | 23 | -0.050373 | 4.62 |
| w26 | 13 | -0.173519 | -24.792 |
| w27 | 36 | -0.025578 | 54.946 |
| w28 | 16 | -0.182781 | -24.271 |
| w29 | 24 | 0.06284 | 31.964 |
| w30 | 12 | -0.179185 | -31.068 |
| w31 | 21 | -0.041912 | -15.963 |
| w32 | 22 | 0.077367 | -1.824 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 18 | 0.164346 | 136.949 |
| w7 | 12 | 0.065776 | 1.854 |
| w8 | 5 | -0.059267 | -9.728 |
| w9 | 17 | 0.031231 | 2.545 |
| w10 | 15 | -0.19495 | -10.231 |
| w11 | 12 | -0.02522 | 7.019 |
| w12 | 12 | -0.04 | -21.393 |
| w13 | 22 | 0.017604 | 17.436 |
| w14 | 20 | 0.055492 | 28.198 |
| w15 | 28 | 0.16094 | 118.736 |
| w16 | 24 | 0.023058 | 72.088 |
| w17 | 21 | -0.006996 | 10.312 |
| w18 | 17 | -0.089098 | -16.276 |
| w19 | 13 | -0.075142 | -10.997 |
| w20 | 11 | -0.01857 | -3.615 |
| w21 | 17 | 0.006677 | 10.768 |
| w22 | 27 | -0.12779 | 19.032 |
| w23 | 21 | -0.092466 | -2.443 |
| w24 | 18 | -0.014554 | 7.008 |
| w25 | 10 | -0.016449 | 12.226 |
| w26 | 22 | -0.051424 | 0.944 |
| w27 | 24 | 0.235002 | 178.806 |
| w28 | 15 | -0.070534 | -10.434 |
| w29 | 21 | 0.1218 | 49.769 |
| w30 | 9 | -0.091313 | -30.451 |
| w31 | 16 | -0.019018 | -15.305 |
| w32 | 12 | 0.068625 | -2.513 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 10 | 0.071293 | 10.902 |
| w8 | 11 | 0.02828 | -9.667 |
| w9 | 12 | -0.076301 | -28.103 |
| w10 | 26 | 0.057607 | 38.419 |
| w11 | 22 | -0.092788 | -7.915 |
| w12 | 15 | 0.009947 | -39.612 |
| w13 | 18 | 0.035315 | 44.706 |
| w14 | 25 | -0.149997 | -5.336 |
| w15 | 19 | -0.114802 | -8.458 |
| w16 | 27 | 0.09784 | 86.382 |
| w17 | 15 | 0.01773 | 6.27 |
| w18 | 17 | -0.028461 | -19.046 |
| w19 | 8 | 0.005087 | -9.689 |
| w20 | 7 | 0.071565 | 3.45 |
| w21 | 15 | -0.168123 | -25.155 |
| w22 | 31 | -0.052459 | 2.52 |
| w23 | 6 | 0.205788 | 78.866 |
| w24 | 26 | -0.192247 | -16.528 |
| w25 | 28 | 0.086959 | 40.724 |
| w26 | 15 | -0.042023 | -28.477 |
| w27 | 18 | -0.024765 | 25.768 |
| w28 | 10 | -0.047802 | -11.766 |
| w29 | 38 | -0.186416 | 22.165 |
| w30 | 21 | -0.18141 | -15.426 |
| w31 | 16 | -0.11059 | -17.561 |
| w32 | 9 | 0.112377 | -22.357 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | 0.212093 | 202.266 |
| w2 | 28 | 0.016849 | 5.609 |
| w3 | 12 | 0.067222 | -4.321 |
| w4 | 39 | 0.015809 | 224.027 |
| w5 | 25 | 0.174353 | 113.311 |
| w6 | 26 | 0.06562 | 68.924 |
| w7 | 16 | 0.133808 | 23.16 |
| w8 | 8 | 0.050257 | -9.626 |
| w9 | 9 | -0.021244 | -10.747 |
| w10 | 23 | 0.002293 | 9.492 |
| w11 | 23 | 0.13357 | 38.206 |
| w12 | 14 | -0.026193 | -21.576 |
| w13 | 23 | 0.05036 | 53.828 |
| w14 | 33 | -0.066533 | 63.149 |
| w15 | 33 | 0.001295 | 26.013 |
| w16 | 36 | -0.043551 | 79.825 |
| w17 | 28 | 0.090389 | 42.085 |
| w18 | 21 | -0.020133 | -9.763 |
| w19 | 15 | 0.006887 | -6.626 |
| w20 | 11 | 0.138654 | 11.989 |
| w21 | 11 | -0.030327 | -7.616 |
| w22 | 33 | -0.071036 | 24.98 |
| w23 | 13 | -0.106401 | -12.014 |
| w24 | 25 | -0.042034 | 20.463 |
| w25 | 19 | 0.109224 | 36.064 |
| w26 | 16 | -0.04015 | -15.55 |
| w27 | 31 | -0.017724 | 11.927 |
| w28 | 3 | -0.031234 | -1.754 |
| w29 | 30 | 0.015166 | 68.344 |
| w30 | 14 | -0.148524 | -23.189 |
| w31 | 24 | -0.062261 | -15.122 |
| w32 | 22 | 0.066415 | 10.792 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 30 | 0.035937 | 43.458 |
| w11 | 9 | -0.125235 | -6.492 |
| w12 | 15 | -0.015606 | -23.276 |
| w13 | 24 | 0.087785 | 59.767 |
| w14 | 35 | -0.066576 | 36.536 |
| w15 | 27 | -0.010207 | 27.661 |
| w16 | 30 | 0.098559 | 101.46 |
| w17 | 22 | 0.084526 | 88.219 |
| w18 | 7 | -0.131555 | -26.532 |
| w19 | 11 | 0.046184 | -10.68 |
| w20 | 13 | -0.024561 | -9.291 |
| w21 | 8 | -0.164571 | -23.385 |
| w22 | 29 | -0.032415 | 13.241 |
| w23 | 5 | -0.021593 | -17.833 |
| w24 | 27 | 0.115045 | 110.957 |
| w25 | 16 | 0.084113 | 6.723 |
| w26 | 9 | -0.07573 | -21.835 |
| w27 | 21 | 0.235959 | 163.668 |
| w28 | 13 | -0.163448 | -18.227 |
| w29 | 20 | -0.013227 | 7.125 |
| w30 | 7 | -0.066395 | -23.866 |
| w31 | 6 | -0.166725 | -18.296 |
| w32 | 19 | 0.04115 | -16.096 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 19 | -0.118934 | 12.197 |
| w13 | 14 | -0.059435 | -20.528 |
| w14 | 28 | -0.010064 | 84.204 |
| w15 | 20 | -0.054621 | -5.674 |
| w16 | 26 | 0.0123 | 76.843 |
| w17 | 21 | 0.034624 | -1.922 |
| w18 | 14 | -0.129617 | 18.301 |
| w19 | 12 | -0.068132 | -21.275 |
| w20 | 20 | 0.010073 | 7.61 |
| w21 | 11 | -0.013606 | -6.495 |
| w22 | 27 | -0.015935 | -1.525 |
| w23 | 4 | -0.128975 | -8.148 |
| w24 | 30 | -0.097011 | 17.882 |
| w25 | 16 | 0.081476 | 6.426 |
| w26 | 4 | -0.093881 | -12.261 |
| w27 | 23 | 0.111181 | 48.399 |
| w28 | 12 | -0.104267 | -13.344 |
| w29 | 21 | -0.071609 | -11.714 |
| w30 | 7 | -0.030113 | -14.128 |
| w31 | 23 | -0.009108 | -11.696 |
| w32 | 17 | -0.047371 | -18.864 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 14 | -0.123938 | -4.894 |
| w16 | 27 | 0.044047 | 87.643 |
| w17 | 15 | -0.059528 | -12.083 |
| w18 | 17 | -0.061548 | 34.777 |
| w19 | 10 | -0.010751 | -14.067 |
| w20 | 12 | -0.081616 | -24.223 |
| w21 | 10 | 0.072224 | -19.226 |
| w22 | 27 | -0.094332 | -18.42 |
| w23 | 4 | -0.091376 | -11.599 |
| w24 | 27 | 0.010216 | 76.072 |
| w25 | 13 | 0.083305 | 8.117 |
| w26 | 13 | -0.061842 | -23.626 |
| w27 | 19 | 0.15162 | 110.817 |
| w28 | 6 | -0.007931 | -1.053 |
| w29 | 22 | 0.081115 | 13.34 |
| w30 | 2 | -0.187621 | -5.952 |
| w31 | 21 | -0.013743 | -13.606 |
| w32 | 15 | -0.021589 | -32.12 |

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
| w15 | 18 | -0.079272 | -2.65 |
| w16 | 32 | -0.018566 | 132.981 |
| w17 | 26 | 0.077956 | 10.878 |
| w18 | 15 | -0.088979 | -10.045 |
| w19 | 13 | 0.031114 | -2.673 |
| w20 | 30 | -0.097668 | -22.274 |
| w21 | 16 | -0.150763 | -38.448 |
| w22 | 38 | -0.128482 | 17.877 |
| w23 | 37 | -0.013171 | -5.068 |
| w24 | 48 | -0.146654 | 34.589 |
| w25 | 23 | 0.12494 | 45.731 |
| w26 | 36 | 0.064462 | 21.209 |
| w27 | 33 | 0.08811 | 141.771 |
| w28 | 15 | -0.218257 | -10.071 |
| w29 | 59 | -0.011896 | 40.412 |
| w30 | 8 | -0.075238 | -11.37 |
| w31 | 40 | 0.025004 | 27.203 |
| w32 | 21 | 0.039412 | 11.778 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 45 | 0.034869 | 45.608 |
| w17 | 15 | 0.033639 | -3.527 |
| w18 | 21 | -0.019208 | 6.451 |
| w19 | 13 | 0.042048 | -3.787 |
| w20 | 10 | 0.042815 | 0.85 |
| w21 | 3 | -0.057902 | -8.64 |
| w22 | 24 | -0.066684 | 5.522 |
| w23 | 11 | -0.057705 | -6.397 |
| w24 | 24 | 0.037093 | 31.234 |
| w25 | 20 | 0.103414 | 14.999 |
| w26 | 14 | -0.098075 | -17.536 |
| w27 | 17 | 0.150001 | 70.393 |
| w28 | 5 | -0.08407 | -10.731 |
| w29 | 18 | -0.007113 | -3.61 |
| w30 | 14 | -0.038632 | -34.658 |
| w31 | 14 | -0.143811 | -20.092 |
| w32 | 10 | 0.006635 | -15.009 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 11 | 0.079028 | 7.226 |
| w21 | 7 | -0.049325 | -16.086 |
| w22 | 19 | -0.009105 | 20.744 |
| w23 | 4 | 0.0122 | -0.953 |
| w24 | 17 | 0.178338 | 112.937 |
| w25 | 20 | 0.023921 | 20.063 |
| w26 | 12 | -0.049848 | -14.179 |
| w27 | 32 | 0.061098 | 41.281 |
| w28 | 7 | -0.044075 | -9.597 |
| w29 | 22 | -0.09827 | -5.883 |
| w30 | 12 | 0.122568 | 10.121 |
| w31 | 19 | -0.049364 | -16.952 |
| w32 | 16 | 0.001913 | -7.049 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 23 | -0.045037 | 2.789 |
| w23 | 5 | -0.069977 | -4.462 |
| w24 | 30 | 0.133138 | 93.127 |
| w25 | 23 | 0.015878 | 33.297 |
| w26 | 23 | -0.00207 | -14.3 |
| w27 | 20 | 0.03786 | 16.706 |
| w28 | 5 | -0.079518 | -9.836 |
| w29 | 18 | -0.005376 | 0.407 |
| w30 | 11 | -0.010672 | -20.543 |
| w31 | 25 | -0.053828 | -13.983 |
| w32 | 18 | 0.051204 | 29.097 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 22 | -0.035946 | 16.812 |
| w25 | 23 | 0.027397 | 24.401 |
| w26 | 14 | -0.089693 | -31.495 |
| w27 | 29 | -0.043497 | 80.037 |
| w28 | 7 | 0.071516 | -1.889 |
| w29 | 21 | 0.02213 | 3.866 |
| w30 | 10 | -0.050979 | -20.469 |
| w31 | 19 | 0.032391 | -9.553 |
| w32 | 13 | 0.114837 | -6.289 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 29 | 0.154704 | 87.732 |
| w6 | 19 | -0.027388 | 19.399 |
| w7 | 12 | -0.022624 | -10.792 |
| w8 | 10 | -0.055151 | -16.153 |
| w9 | 9 | -0.001753 | -25.595 |
| w10 | 22 | 0.010507 | 15.987 |
| w11 | 19 | 0.060581 | 11.373 |
| w12 | 9 | -0.116785 | -26.54 |
| w13 | 24 | 0.093924 | 66.068 |
| w14 | 27 | -0.147309 | 35.923 |
| w15 | 14 | -0.042797 | 3.508 |
| w16 | 30 | 0.032052 | 82.808 |
| w17 | 18 | 0.038178 | -9.366 |
| w18 | 23 | -0.007954 | 6.76 |
| w19 | 15 | 0.031992 | 14.751 |
| w20 | 12 | 0.064279 | 3.802 |
| w21 | 12 | -0.09187 | -19.148 |
| w22 | 19 | -0.108692 | -4.438 |
| w23 | 6 | -0.111937 | -13.25 |
| w24 | 34 | -0.111528 | -3.351 |
| w25 | 14 | 0.110173 | 17.508 |
| w26 | 25 | 0.107684 | 27.86 |
| w27 | 23 | -0.02738 | 27.401 |
| w28 | 8 | -0.143899 | -26.757 |
| w29 | 26 | -0.00981 | -2.641 |
| w30 | 33 | 0.106706 | 215.991 |
| w31 | 16 | 0.00826 | -6.441 |
| w32 | 27 | 0.07481 | 71.554 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 33 | 0.066491 | 123.832 |
| w6 | 21 | 0.090706 | 72.438 |
| w7 | 13 | -0.033475 | -0.979 |
| w8 | 8 | -0.111014 | -11.121 |
| w9 | 8 | -0.041074 | -33.658 |
| w10 | 22 | -0.12617 | 12.768 |
| w11 | 20 | 0.016534 | 7.576 |
| w12 | 11 | -0.014863 | -19.638 |
| w13 | 28 | 0.032933 | 33.444 |
| w14 | 34 | -0.157003 | 32.857 |
| w15 | 30 | -0.079056 | 27.005 |
| w16 | 26 | 0.043028 | 52.844 |
| w17 | 24 | 0.034583 | 6.289 |
| w18 | 17 | -0.214548 | -27.978 |
| w19 | 26 | -0.043818 | -13.821 |
| w20 | 24 | 0.03984 | -3.866 |
| w21 | 21 | -0.082284 | -14.696 |
| w22 | 28 | -0.012305 | 9.136 |
| w23 | 13 | 0.092778 | 6.477 |
| w24 | 41 | -0.152516 | 1.213 |
| w25 | 18 | -0.188821 | -41.092 |
| w26 | 27 | -0.067614 | 10.795 |
| w27 | 41 | -0.065126 | 7.318 |
| w28 | 26 | -0.042292 | 24.663 |
| w29 | 15 | 0.167184 | 39.563 |
| w30 | 40 | -0.123918 | 21.215 |
| w31 | 16 | 0.089362 | 15.954 |
| w32 | 28 | 0.024477 | 27.26 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 16 | -0.149472 | -14.339 |
| w18 | 23 | -0.171418 | 15.815 |
| w19 | 7 | -0.05898 | -25.862 |
| w20 | 12 | -0.019697 | -5.873 |
| w21 | 8 | -0.157942 | -29.322 |
| w22 | 25 | 0.036907 | 16.546 |
| w23 | 9 | 0.008664 | -3.525 |
| w24 | 18 | -0.122143 | 6.965 |
| w25 | 12 | 0.111589 | 12.251 |
| w26 | 19 | -0.047514 | -16.561 |
| w27 | 20 | 0.141232 | 109.945 |
| w28 | 14 | -0.008937 | 2.341 |
| w29 | 18 | 0.098065 | 18.11 |
| w30 | 2 | -0.048877 | -8.713 |
| w31 | 15 | -0.051198 | -23.584 |
| w32 | 23 | 0.054454 | 17.25 |

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
| w17 | 24 | -0.077807 | -13.802 |
| w18 | 14 | -0.086477 | -24.163 |
| w19 | 10 | 0.052745 | -1.871 |
| w20 | 19 | 0.003948 | -4.705 |
| w21 | 11 | -0.025242 | -27.311 |
| w22 | 26 | -0.043984 | 6.211 |
| w23 | 11 | -0.036089 | -3.051 |
| w24 | 28 | -0.126051 | 32.002 |
| w25 | 15 | 0.003038 | 0.819 |
| w26 | 28 | -0.009974 | 6.815 |
| w27 | 33 | -0.036907 | 48.162 |
| w28 | 7 | -0.087841 | -9.772 |
| w29 | 31 | -0.104525 | 11.298 |
| w30 | 11 | -0.136439 | -20.485 |
| w31 | 8 | -0.237038 | -28.142 |
| w32 | 23 | 0.051121 | 15.835 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 7 | -0.076979 | -13.083 |
| w20 | 12 | 0.043301 | 5.151 |
| w21 | 14 | -0.070355 | -5.953 |
| w22 | 34 | 0.014036 | 103.461 |
| w23 | 20 | -0.025945 | -12.031 |
| w24 | 27 | 0.081544 | 241.407 |
| w25 | 10 | -0.044492 | -9.026 |
| w26 | 13 | -0.049676 | -24.572 |
| w27 | 28 | 0.019167 | 18.762 |
| w28 | 4 | -0.054223 | -8.776 |
| w29 | 27 | -0.052984 | -6.29 |
| w30 | 6 | -0.063472 | -19.298 |
| w31 | 12 | -0.01524 | -5.275 |
| w32 | 25 | 0.056993 | 29.658 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 26 | -0.021597 | 19.344 |
| w23 | 13 | -0.173504 | -25.923 |
| w24 | 24 | -0.08296 | 12.902 |
| w25 | 15 | -0.045954 | -13.119 |
| w26 | 10 | -0.032896 | -12.087 |
| w27 | 16 | -0.024767 | 8.447 |
| w28 | 6 | -0.113409 | -15.872 |
| w29 | 20 | 0.052601 | 16.189 |
| w30 | 2 | -0.13113 | -15.233 |
| w31 | 15 | -0.051922 | -9.559 |
| w32 | 18 | 0.078842 | 6.97 |

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
| w27 | 24 | 0.073757 | 44.792 |
| w28 | 8 | -0.058468 | -4.965 |
| w29 | 18 | 0.046875 | 2.808 |
| w30 | 4 | -0.000835 | -11.254 |
| w31 | 9 | -0.123696 | -13.279 |
| w32 | 20 | 0.021381 | 47.224 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 16 | 0.097242 | 14.784 |
| w18 | 5 | 0.068434 | -6.656 |
| w19 | 4 | -0.001304 | -7.399 |
| w20 | 8 | 0.16448 | 17.167 |
| w21 | 1 | -0.081501 | -19.604 |
| w22 | 27 | -0.022877 | 14.384 |
| w23 | 6 | -0.135904 | -15.948 |
| w24 | 31 | -0.06109 | 67.175 |
| w25 | 15 | 0.112336 | 16.648 |
| w26 | 10 | -0.127481 | -28.027 |
| w27 | 22 | 0.089733 | 47.5 |
| w28 | 8 | -0.059401 | -9.183 |
| w29 | 17 | -0.039803 | -13.789 |
| w30 | 8 | -0.099806 | -28.485 |
| w31 | 20 | -0.074315 | -20.93 |
| w32 | 15 | 0.083933 | -15.861 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 17 | 0.048329 | 6.237 |
| w18 | 17 | 0.001045 | 1.453 |
| w19 | 7 | -0.032734 | -10.033 |
| w20 | 10 | 0.057139 | 3.374 |
| w21 | 8 | -0.180758 | -33.839 |
| w22 | 23 | 0.021871 | 39.226 |
| w23 | 8 | -0.148363 | -16.911 |
| w24 | 29 | -0.032358 | 40.17 |
| w25 | 20 | 0.148665 | 38.95 |
| w26 | 15 | -0.042247 | -16.766 |
| w27 | 21 | 0.059312 | 32.063 |
| w28 | 5 | -0.018895 | -7.59 |
| w29 | 15 | 0.028639 | 1.885 |
| w30 | 9 | -0.063702 | -19.554 |
| w31 | 13 | -0.154997 | -23.459 |
| w32 | 12 | -0.018963 | -26.59 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 7 | 0.098472 | 1.664 |
| w29 | 22 | 0.023687 | -0.893 |
| w30 | 11 | -0.083721 | -9.358 |
| w31 | 22 | 0.118899 | 21.874 |
| w32 | 13 | -0.029458 | -0.068 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 22 | 0.054748 | 5.252 |
| w15 | 16 | 0.033262 | 61.965 |
| w16 | 33 | -0.035297 | 473.455 |
| w17 | 15 | 0.08286 | 11.998 |
| w18 | 12 | -0.11531 | -9.551 |
| w19 | 11 | -0.005935 | -9.932 |
| w20 | 10 | 0.038472 | -1.993 |
| w21 | 12 | 0.173101 | 45.222 |
| w22 | 24 | -0.050373 | -2.374 |
| w23 | 10 | 0.006359 | 2.205 |
| w24 | 31 | 0.044431 | 29.714 |
| w25 | 16 | 0.138212 | 78.362 |
| w26 | 12 | -0.048235 | -11.646 |
| w27 | 23 | 0.216116 | 156.245 |
| w28 | 8 | -0.057286 | -10.024 |
| w29 | 22 | 0.042308 | 22.416 |
| w30 | 7 | 0.044818 | -6.395 |
| w31 | 9 | -0.035912 | -9.402 |
| w32 | 14 | 0.114939 | 7.526 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 21 | 0.227107 | 137.743 |
| w26 | 18 | 0.097663 | 8.513 |
| w27 | 25 | 0.143505 | 65.444 |
| w28 | 10 | 0.004863 | -9.46 |
| w29 | 20 | 0.04334 | 12.996 |
| w30 | 3 | -0.046841 | -13.49 |
| w31 | 12 | 0.066601 | 3.187 |
| w32 | 21 | 0.102831 | 12.66 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

