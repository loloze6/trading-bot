# Backtest of 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days_1d

- Plan: `../../../../../03_test_plan/night4_range_run/plans/023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | -0.125492 | 2.055 |
| w2 | 10 | 0.029541 | 50.856 |
| w3 | 32 | -0.003257 | 72.797 |
| w4 | 20 | -0.028613 | -31.586 |
| w5 | 15 | 0.044268 | 111.321 |
| w6 | 24 | -0.057899 | 63.574 |
| w7 | 3 | -0.065531 | -13.204 |
| w8 | 6 | -0.015198 | -8.831 |
| w9 | 1 | 0.002412 | -3.0 |
| w10 | 15 | 0.016845 | 22.781 |
| w11 | 13 | -0.153381 | 60.475 |
| w12 | 0 | None | 0.0 |
| w13 | 20 | 0.044465 | 20.003 |
| w14 | 22 | -0.038734 | 21.999 |
| w15 | 22 | 0.099687 | 131.447 |
| w16 | 24 | -0.088776 | 7.986 |
| w17 | 8 | 0.056833 | 19.659 |
| w18 | 11 | 0.043975 | -4.697 |
| w19 | 6 | 0.017961 | -16.022 |
| w20 | 5 | 0.027905 | -4.544 |
| w21 | 4 | 0.02081 | -0.194 |
| w22 | 15 | -0.104629 | 16.935 |
| w23 | 5 | -0.033419 | -0.796 |
| w24 | 19 | 0.00778 | 63.377 |
| w25 | 12 | 0.082195 | 49.123 |
| w26 | 7 | -0.065959 | -27.053 |
| w27 | 16 | -0.004129 | 81.719 |
| w28 | 3 | -0.055271 | -8.632 |
| w29 | 22 | -0.04262 | 9.428 |
| w30 | 3 | 0.002418 | -4.375 |
| w31 | 11 | -0.012104 | -6.243 |
| w32 | 17 | 0.088638 | 19.296 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.042719 | -1.934 |
| w2 | 8 | 0.038311 | 0.437 |
| w3 | 11 | -0.093846 | -15.026 |
| w4 | 7 | 0.143676 | 152.029 |
| w5 | 15 | 0.002628 | 30.458 |
| w6 | 11 | 0.113219 | 86.905 |
| w7 | 5 | -0.009077 | -15.707 |
| w8 | 6 | -0.002206 | -6.571 |
| w9 | 0 | None | 0.0 |
| w10 | 21 | -0.076843 | 16.029 |
| w11 | 18 | 0.065414 | 11.049 |
| w12 | 2 | 0.043609 | -4.682 |
| w13 | 14 | -0.000441 | 8.069 |
| w14 | 11 | -0.053661 | 16.013 |
| w15 | 16 | -0.027846 | 61.574 |
| w16 | 22 | -0.144388 | -8.548 |
| w17 | 9 | -0.014322 | -24.027 |
| w18 | 6 | -0.003377 | -0.501 |
| w19 | 5 | -0.04778 | -13.074 |
| w20 | 9 | 0.016465 | -5.266 |
| w21 | 7 | -0.143452 | -21.934 |
| w22 | 20 | -0.059177 | -2.629 |
| w23 | 3 | -0.094206 | -19.645 |
| w24 | 4 | -0.124289 | -16.962 |
| w25 | 9 | 0.11804 | 47.772 |
| w26 | 0 | None | 0.0 |
| w27 | 13 | 0.003208 | 49.253 |
| w28 | 2 | -0.133214 | -9.807 |
| w29 | 18 | -0.034728 | 15.166 |
| w30 | 1 | -0.498227 | -24.786 |
| w31 | 1 | -0.110937 | -2.002 |
| w32 | 9 | -0.086679 | -25.843 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 8 | 0.205928 | 177.012 |
| w7 | 5 | -0.110871 | -14.635 |
| w8 | 4 | -0.0633 | -10.855 |
| w9 | 3 | -0.062098 | -3.684 |
| w10 | 2 | -0.201267 | -8.845 |
| w11 | 6 | 0.020044 | -5.693 |
| w12 | 6 | 0.00795 | -4.756 |
| w13 | 14 | 0.077258 | 26.339 |
| w14 | 6 | 0.125976 | 41.369 |
| w15 | 8 | 0.174253 | 125.898 |
| w16 | 10 | -0.047942 | 52.632 |
| w17 | 7 | 0.066641 | 16.23 |
| w18 | 3 | -0.028838 | -10.328 |
| w19 | 5 | 0.009405 | -6.469 |
| w20 | 7 | -0.024675 | -10.345 |
| w21 | 7 | -0.065354 | 18.735 |
| w22 | 7 | -0.184674 | -9.322 |
| w23 | 8 | -0.099704 | -15.901 |
| w24 | 6 | 0.008757 | 14.557 |
| w25 | 8 | 0.031109 | 9.31 |
| w26 | 3 | -0.166819 | -9.361 |
| w27 | 8 | 0.323367 | 325.512 |
| w28 | 1 | -0.076391 | -1.156 |
| w29 | 9 | 0.018536 | 7.632 |
| w30 | 0 | None | 0.0 |
| w31 | 1 | -0.0409 | -8.575 |
| w32 | 5 | -0.186321 | -21.148 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 2 | -0.087781 | -6.803 |
| w8 | 5 | 0.043271 | -9.549 |
| w9 | 1 | -0.032455 | -40.157 |
| w10 | 8 | 0.106158 | 63.777 |
| w11 | 14 | -0.078064 | 9.287 |
| w12 | 4 | -0.077339 | -10.376 |
| w13 | 7 | 0.071579 | 41.185 |
| w14 | 4 | -0.036244 | 7.834 |
| w15 | 15 | -0.066004 | -19.58 |
| w16 | 12 | -0.119283 | 12.117 |
| w17 | 10 | 0.073955 | 16.717 |
| w18 | 11 | -0.098531 | -26.175 |
| w19 | 5 | -0.095766 | -8.985 |
| w20 | 3 | -0.056665 | -14.615 |
| w21 | 2 | -0.005587 | -10.944 |
| w22 | 9 | -0.033119 | -2.938 |
| w23 | 3 | 0.061612 | 28.281 |
| w24 | 13 | -0.193576 | -10.786 |
| w25 | 9 | 0.164442 | 54.379 |
| w26 | 0 | None | 0.0 |
| w27 | 10 | 0.019369 | 21.906 |
| w28 | 0 | None | 0.0 |
| w29 | 25 | -0.14787 | 6.505 |
| w30 | 6 | -0.175916 | -21.877 |
| w31 | 1 | -0.017298 | -4.02 |
| w32 | 5 | -0.112288 | -24.588 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | 0.137545 | 247.443 |
| w2 | 11 | -0.001387 | 7.68 |
| w3 | 8 | 0.039269 | -6.537 |
| w4 | 32 | 0.047965 | 212.126 |
| w5 | 20 | 0.108203 | 94.287 |
| w6 | 10 | 0.063805 | 53.585 |
| w7 | 8 | 0.073525 | 10.464 |
| w8 | 6 | 0.077628 | -3.083 |
| w9 | 1 | 0.004237 | -13.859 |
| w10 | 17 | -0.276259 | -20.882 |
| w11 | 10 | 0.033662 | 13.899 |
| w12 | 1 | -0.032073 | -9.359 |
| w13 | 13 | 0.053524 | 52.846 |
| w14 | 19 | 0.000534 | 56.117 |
| w15 | 14 | 0.074022 | 54.535 |
| w16 | 24 | 0.019156 | 83.532 |
| w17 | 11 | 0.062047 | 49.213 |
| w18 | 16 | 0.002283 | -9.01 |
| w19 | 8 | -0.036197 | -1.169 |
| w20 | 8 | 0.04359 | 9.596 |
| w21 | 5 | -0.169364 | -24.093 |
| w22 | 8 | -0.075937 | 0.632 |
| w23 | 2 | -0.101374 | -10.446 |
| w24 | 9 | -0.018334 | 41.8 |
| w25 | 10 | 0.039031 | 9.341 |
| w26 | 7 | -0.006928 | -8.792 |
| w27 | 11 | 0.039705 | 23.182 |
| w28 | 0 | None | 0.0 |
| w29 | 18 | 0.008832 | 56.971 |
| w30 | 3 | -0.002689 | -0.793 |
| w31 | 10 | -0.112173 | -18.828 |
| w32 | 14 | 0.037975 | 10.717 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 9 | 0.110751 | 59.882 |
| w11 | 5 | -0.097917 | -3.655 |
| w12 | 2 | -0.078613 | -8.416 |
| w13 | 8 | 0.071997 | 36.174 |
| w14 | 34 | -0.144248 | 24.601 |
| w15 | 9 | -0.122294 | -18.764 |
| w16 | 21 | 0.070587 | 86.763 |
| w17 | 4 | -0.011495 | 52.824 |
| w18 | 2 | -0.081983 | -12.485 |
| w19 | 4 | -0.095577 | -27.603 |
| w20 | 4 | 0.012432 | -18.462 |
| w21 | 0 | None | 0.0 |
| w22 | 11 | -0.05186 | 6.182 |
| w23 | 1 | -0.190477 | -10.118 |
| w24 | 20 | 0.068134 | 158.463 |
| w25 | 12 | 0.030338 | 2.753 |
| w26 | 2 | -0.119266 | -16.668 |
| w27 | 9 | 0.242148 | 118.621 |
| w28 | 1 | -0.110332 | -1.697 |
| w29 | 10 | -0.056992 | -3.966 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 8 | -0.191625 | -36.121 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 6 | 0.004265 | 5.818 |
| w13 | 8 | -0.065148 | 1.963 |
| w14 | 15 | -0.13721 | 6.254 |
| w15 | 6 | -0.28531 | -16.828 |
| w16 | 16 | -0.073016 | 77.366 |
| w17 | 4 | 0.064994 | 1.121 |
| w18 | 10 | 0.008402 | 17.796 |
| w19 | 1 | -0.036851 | -6.884 |
| w20 | 12 | -0.001913 | 1.759 |
| w21 | 8 | -0.123841 | -7.051 |
| w22 | 7 | 0.07108 | 16.633 |
| w23 | 3 | -0.074481 | -0.241 |
| w24 | 11 | -0.149315 | -2.358 |
| w25 | 4 | 0.102647 | 21.414 |
| w26 | 0 | None | 0.0 |
| w27 | 7 | 0.008729 | 42.489 |
| w28 | 1 | -0.078821 | -5.293 |
| w29 | 5 | -0.168289 | -30.275 |
| w30 | 1 | -0.077317 | -7.322 |
| w31 | 9 | -0.184528 | -30.007 |
| w32 | 5 | -0.076526 | 3.984 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 2 | -0.070439 | -3.19 |
| w16 | 17 | 0.025602 | 71.444 |
| w17 | 3 | -0.027359 | 1.512 |
| w18 | 5 | 0.086827 | 44.848 |
| w19 | 1 | -0.096187 | -10.581 |
| w20 | 4 | -0.005558 | -13.011 |
| w21 | 3 | -0.166277 | -40.259 |
| w22 | 15 | -0.007596 | -8.275 |
| w23 | 0 | None | 0.0 |
| w24 | 14 | 0.03388 | 66.098 |
| w25 | 10 | 0.073868 | 2.018 |
| w26 | 0 | None | 0.0 |
| w27 | 7 | 0.167171 | 166.03 |
| w28 | 2 | -0.07702 | -3.098 |
| w29 | 8 | -0.025169 | -15.53 |
| w30 | 0 | None | 0.0 |
| w31 | 7 | -0.073882 | -15.548 |
| w32 | 4 | -0.265564 | -32.233 |

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
| w15 | 4 | 0.084947 | -2.968 |
| w16 | 8 | -0.027773 | 38.015 |
| w17 | 8 | 0.015054 | 9.717 |
| w18 | 10 | -0.172454 | -8.859 |
| w19 | 3 | 0.043459 | -8.218 |
| w20 | 9 | -0.190771 | -24.828 |
| w21 | 6 | -0.142917 | -5.043 |
| w22 | 16 | -0.16308 | -12.016 |
| w23 | 18 | -0.018666 | -26.125 |
| w24 | 29 | -0.105807 | 32.993 |
| w25 | 9 | 0.121129 | 41.869 |
| w26 | 20 | -0.158559 | -16.24 |
| w27 | 16 | 0.049428 | 109.65 |
| w28 | 4 | 0.027355 | -6.055 |
| w29 | 31 | -0.028895 | 36.719 |
| w30 | 3 | -0.144976 | -16.238 |
| w31 | 26 | -0.051737 | 6.883 |
| w32 | 15 | 0.017248 | -2.043 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 16 | 0.148101 | 73.818 |
| w17 | 8 | 0.060161 | 22.788 |
| w18 | 16 | -0.01568 | -5.766 |
| w19 | 7 | -6.6e-05 | -15.571 |
| w20 | 4 | -0.029495 | -9.749 |
| w21 | 0 | None | 0.0 |
| w22 | 11 | -0.018901 | 1.561 |
| w23 | 4 | -0.097811 | -1.592 |
| w24 | 11 | -0.049071 | 53.866 |
| w25 | 7 | 0.069656 | 5.539 |
| w26 | 0 | None | 0.0 |
| w27 | 5 | 0.103313 | 72.648 |
| w28 | 0 | None | 0.0 |
| w29 | 8 | -0.0883 | -22.996 |
| w30 | 5 | -0.135809 | -41.885 |
| w31 | 2 | -0.097492 | -13.833 |
| w32 | 1 | -0.144004 | -7.781 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 11 | 0.070136 | 0.663 |
| w21 | 0 | None | 0.0 |
| w22 | 10 | -0.032535 | 4.637 |
| w23 | 4 | -0.017855 | -3.76 |
| w24 | 17 | 0.171818 | 274.981 |
| w25 | 7 | -0.072345 | 17.173 |
| w26 | 1 | -0.128364 | -15.454 |
| w27 | 14 | -0.025578 | 30.235 |
| w28 | 0 | None | 0.0 |
| w29 | 8 | -0.082905 | 3.636 |
| w30 | 8 | -0.041234 | -27.198 |
| w31 | 5 | -0.190576 | -14.461 |
| w32 | 5 | 0.014228 | -15.969 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 8 | -0.035516 | -4.369 |
| w23 | 3 | 0.032327 | -2.36 |
| w24 | 17 | 0.000338 | 136.187 |
| w25 | 12 | 0.098766 | 42.956 |
| w26 | 6 | -0.003221 | -8.924 |
| w27 | 7 | -0.153351 | -22.391 |
| w28 | 0 | None | 0.0 |
| w29 | 8 | -0.087931 | -16.202 |
| w30 | 1 | -0.05274 | -20.106 |
| w31 | 9 | -0.140062 | -20.003 |
| w32 | 6 | 0.101314 | 15.166 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 8 | -0.084466 | 2.485 |
| w25 | 15 | 0.048988 | 34.685 |
| w26 | 0 | None | 0.0 |
| w27 | 23 | -0.007817 | 72.699 |
| w28 | 5 | 0.01193 | 1.728 |
| w29 | 10 | -0.02557 | -5.411 |
| w30 | 1 | -0.108947 | -6.304 |
| w31 | 5 | -0.094033 | -14.691 |
| w32 | 2 | 0.332594 | 7.197 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 14 | 0.105262 | 92.337 |
| w6 | 9 | -0.035879 | 11.453 |
| w7 | 4 | -0.03809 | -14.344 |
| w8 | 10 | -0.039759 | -24.75 |
| w9 | 2 | -0.005417 | -37.695 |
| w10 | 4 | 0.053937 | -1.554 |
| w11 | 10 | 0.044966 | 20.522 |
| w12 | 0 | None | 0.0 |
| w13 | 9 | 0.144138 | 62.821 |
| w14 | 21 | -0.10525 | 16.271 |
| w15 | 4 | -0.166982 | -4.709 |
| w16 | 11 | -0.228614 | 33.492 |
| w17 | 7 | -0.017367 | -1.631 |
| w18 | 10 | -0.095423 | -22.497 |
| w19 | 8 | -0.030146 | 16.296 |
| w20 | 6 | -0.034069 | -10.965 |
| w21 | 3 | 0.019499 | -6.198 |
| w22 | 12 | -0.091378 | -14.377 |
| w23 | 2 | -0.023321 | -6.283 |
| w24 | 9 | -0.108178 | -21.232 |
| w25 | 5 | -0.009344 | -0.633 |
| w26 | 13 | 0.030493 | 9.898 |
| w27 | 18 | -0.008097 | 32.805 |
| w28 | 1 | -0.047114 | -17.681 |
| w29 | 5 | 0.025259 | 5.907 |
| w30 | 15 | 0.173539 | 316.869 |
| w31 | 5 | 0.08754 | 13.269 |
| w32 | 14 | 0.051678 | 31.26 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 21 | 0.156641 | 127.784 |
| w6 | 15 | 0.048532 | 111.54 |
| w7 | 9 | -0.184379 | -22.85 |
| w8 | 2 | -0.052795 | -16.95 |
| w9 | 3 | -0.023903 | -1.997 |
| w10 | 17 | -0.098291 | 7.512 |
| w11 | 12 | -0.04625 | -9.19 |
| w12 | 5 | -0.026653 | -8.614 |
| w13 | 17 | 0.035588 | 21.871 |
| w14 | 16 | -0.004425 | 34.984 |
| w15 | 15 | -0.035432 | 15.589 |
| w16 | 18 | -0.210309 | 6.3 |
| w17 | 11 | 0.009282 | 2.417 |
| w18 | 5 | -0.081987 | -13.244 |
| w19 | 15 | 0.007772 | -14.333 |
| w20 | 13 | 0.00974 | 5.081 |
| w21 | 9 | -0.090969 | -19.783 |
| w22 | 11 | -0.057293 | 3.949 |
| w23 | 6 | -0.024988 | -6.476 |
| w24 | 23 | -0.102019 | -2.062 |
| w25 | 6 | -0.01252 | -33.399 |
| w26 | 10 | -0.089583 | 14.343 |
| w27 | 10 | -0.088886 | 20.747 |
| w28 | 5 | -0.124381 | -7.562 |
| w29 | 3 | 0.106532 | 19.789 |
| w30 | 16 | -0.198453 | -17.511 |
| w31 | 8 | 0.070475 | 8.842 |
| w32 | 21 | 0.049894 | 50.963 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 3 | -0.051088 | -3.099 |
| w18 | 18 | 0.013677 | -6.452 |
| w19 | 7 | -0.186358 | -39.525 |
| w20 | 11 | 0.025246 | 0.626 |
| w21 | 0 | None | 0.0 |
| w22 | 11 | 0.014647 | 3.638 |
| w23 | 4 | 0.004332 | -7.197 |
| w24 | 8 | -0.136037 | -31.737 |
| w25 | 3 | 0.131859 | 24.755 |
| w26 | 2 | 0.009081 | -1.841 |
| w27 | 7 | 0.130293 | 105.54 |
| w28 | 5 | 0.045175 | 9.634 |
| w29 | 12 | 0.050506 | 9.451 |
| w30 | 0 | None | 0.0 |
| w31 | 6 | -0.061914 | -12.039 |
| w32 | 12 | 0.077549 | 32.072 |

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
| w17 | 15 | -0.193429 | -20.193 |
| w18 | 4 | -0.042673 | -7.927 |
| w19 | 4 | -0.122101 | -1.136 |
| w20 | 10 | 0.0247 | -7.929 |
| w21 | 1 | -0.196589 | -34.52 |
| w22 | 7 | -0.005896 | -3.791 |
| w23 | 1 | 0.039433 | 2.908 |
| w24 | 20 | -0.192913 | 15.844 |
| w25 | 4 | -0.044029 | 16.906 |
| w26 | 9 | -0.170066 | -15.059 |
| w27 | 21 | -0.013227 | 41.184 |
| w28 | 2 | 0.033272 | -2.523 |
| w29 | 17 | 0.012102 | -0.097 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 9 | -0.021641 | 4.438 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 2 | -0.010693 | -2.068 |
| w20 | 4 | 0.143485 | -0.106 |
| w21 | 4 | 0.048964 | -8.572 |
| w22 | 19 | -0.011033 | 142.701 |
| w23 | 3 | 0.078296 | 1.405 |
| w24 | 15 | -0.020862 | 178.452 |
| w25 | 5 | -0.048778 | -16.994 |
| w26 | 3 | -0.144721 | -29.349 |
| w27 | 6 | -0.047182 | -3.176 |
| w28 | 0 | None | 0.0 |
| w29 | 18 | -0.009529 | 10.271 |
| w30 | 1 | -0.088075 | -5.719 |
| w31 | 2 | -0.012933 | -4.604 |
| w32 | 5 | 0.069847 | 46.101 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 10 | 0.025421 | 28.553 |
| w23 | 2 | -0.136099 | -28.548 |
| w24 | 16 | -0.080752 | 27.3 |
| w25 | 4 | -0.15432 | -22.058 |
| w26 | 1 | -0.042657 | -5.23 |
| w27 | 4 | -0.04231 | -15.714 |
| w28 | 0 | None | 0.0 |
| w29 | 8 | 0.002025 | 3.704 |
| w30 | 0 | None | 0.0 |
| w31 | 2 | -0.268291 | -21.756 |
| w32 | 10 | -0.115889 | -13.957 |

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
| w27 | 10 | 0.002281 | 31.286 |
| w28 | 0 | None | 0.0 |
| w29 | 7 | -0.134934 | -14.205 |
| w30 | 1 | -0.096924 | -9.792 |
| w31 | 1 | -0.114572 | -0.042 |
| w32 | 12 | -0.043477 | 26.791 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 5 | -0.00525 | 3.816 |
| w18 | 3 | 0.086736 | -0.034 |
| w19 | 3 | -0.042033 | -15.463 |
| w20 | 4 | 0.013712 | -12.631 |
| w21 | 0 | None | 0.0 |
| w22 | 6 | -0.045715 | 13.752 |
| w23 | 2 | -0.091877 | 3.78 |
| w24 | 11 | -0.009862 | 36.35 |
| w25 | 5 | 0.023464 | 0.076 |
| w26 | 0 | None | 0.0 |
| w27 | 4 | 0.065178 | 37.483 |
| w28 | 0 | None | 0.0 |
| w29 | 7 | -0.099757 | -22.534 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | -0.096324 | -16.343 |
| w32 | 4 | 0.12552 | 4.22 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 1 | 0.004476 | -2.565 |
| w18 | 5 | -0.068523 | -1.59 |
| w19 | 4 | -0.113546 | -13.877 |
| w20 | 4 | -0.047194 | -10.924 |
| w21 | 0 | None | 0.0 |
| w22 | 6 | 0.074613 | 97.319 |
| w23 | 0 | None | 0.0 |
| w24 | 16 | -0.023085 | 39.209 |
| w25 | 7 | 0.14196 | 46.662 |
| w26 | 4 | -0.047338 | 1.783 |
| w27 | 9 | -0.051826 | -11.863 |
| w28 | 0 | None | 0.0 |
| w29 | 9 | -0.004825 | -9.606 |
| w30 | 1 | -0.100406 | -7.911 |
| w31 | 1 | -0.127505 | -6.86 |
| w32 | 5 | -0.022685 | -2.017 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 1 | -0.014514 | -1.059 |
| w29 | 10 | 0.029175 | -9.096 |
| w30 | 0 | None | 0.0 |
| w31 | 11 | 0.098188 | 16.653 |
| w32 | 6 | -0.100679 | -4.959 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 8 | -0.077433 | -15.765 |
| w15 | 5 | 0.106657 | 47.398 |
| w16 | 13 | -0.077641 | 79.171 |
| w17 | 7 | 0.026779 | -10.388 |
| w18 | 7 | -0.013877 | -10.26 |
| w19 | 3 | -0.045111 | -5.225 |
| w20 | 6 | 0.06939 | -8.45 |
| w21 | 3 | 0.225905 | 61.869 |
| w22 | 11 | -0.077093 | -18.947 |
| w23 | 5 | -0.091594 | -9.266 |
| w24 | 15 | -0.038895 | 20.368 |
| w25 | 10 | 0.189188 | 111.683 |
| w26 | 2 | -0.012814 | -5.64 |
| w27 | 12 | 0.139409 | 141.595 |
| w28 | 0 | None | 0.0 |
| w29 | 6 | 0.046964 | 15.342 |
| w30 | 4 | -0.183295 | -36.715 |
| w31 | 3 | 0.091751 | 9.433 |
| w32 | 9 | -0.048009 | -18.687 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 7 | 0.280386 | 259.727 |
| w26 | 10 | 0.007544 | 4.577 |
| w27 | 12 | 0.022448 | 53.128 |
| w28 | 0 | None | 0.0 |
| w29 | 9 | -0.029134 | -17.637 |
| w30 | 0 | None | 0.0 |
| w31 | 8 | -0.095967 | -10.458 |
| w32 | 11 | -0.072444 | -13.621 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

