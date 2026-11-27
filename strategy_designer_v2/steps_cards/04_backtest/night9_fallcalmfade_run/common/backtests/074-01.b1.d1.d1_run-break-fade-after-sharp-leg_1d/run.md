# Backtest of 074-01.b1.d1.d1_run-break-fade-after-sharp-leg_1d

- Plan: `../../../../../03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.d1.d1_run-break-fade-after-sharp-leg_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 1 | 0.054168 | 0.231 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 7 | 0.20709 | 12.091 |
| w8 | 6 | 0.134084 | 10.61 |
| w9 | 8 | 0.210628 | 32.377 |
| w10 | 2 | 0.076117 | 0.992 |
| w11 | 0 | None | 0.0 |
| w12 | 9 | 0.0605 | 4.236 |
| w13 | 4 | -0.017919 | -0.055 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 8 | 0.198663 | 8.741 |
| w18 | 3 | -0.02516 | -1.68 |
| w19 | 6 | 0.006322 | 0.343 |
| w20 | 6 | 0.1444 | 13.647 |
| w21 | 10 | 0.059274 | 3.622 |
| w22 | 1 | 0.006236 | -0.064 |
| w23 | 1 | 0.00221 | 0.059 |
| w24 | 2 | -0.040313 | -1.115 |
| w25 | 0 | None | 0.0 |
| w26 | 1 | 0.060436 | 2.749 |
| w27 | 0 | None | 0.0 |
| w28 | 3 | -0.010627 | -0.835 |
| w29 | 0 | None | 0.0 |
| w30 | 4 | 0.066951 | 4.397 |
| w31 | 8 | 0.02637 | 4.193 |
| w32 | 5 | -0.005232 | -0.705 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.005451 | -0.08 |
| w2 | 3 | -0.035999 | -1.969 |
| w3 | 0 | None | 0.0 |
| w4 | 1 | -0.037338 | -4.47 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | -0.022028 | 0.0 |
| w7 | 5 | -0.025616 | -1.516 |
| w8 | 10 | 0.228659 | 28.493 |
| w9 | 9 | 0.231562 | 34.36 |
| w10 | 1 | 0.122608 | 1.653 |
| w11 | 5 | -0.031986 | -3.093 |
| w12 | 10 | -0.019203 | -2.371 |
| w13 | 3 | 0.106195 | 2.479 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.001942 | -0.705 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | 0.041186 | 1.021 |
| w18 | 1 | 0.020911 | 0.345 |
| w19 | 10 | 0.046194 | 3.131 |
| w20 | 7 | 0.033316 | 5.175 |
| w21 | 2 | 0.070614 | 1.026 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.053036 | -2.141 |
| w24 | 6 | -0.030587 | -2.418 |
| w25 | 0 | None | 0.0 |
| w26 | 9 | 0.108717 | 9.258 |
| w27 | 0 | None | 0.0 |
| w28 | 5 | 0.057613 | 3.854 |
| w29 | 1 | -0.08089 | -0.932 |
| w30 | 8 | -0.064007 | -3.552 |
| w31 | 11 | 0.021341 | 2.793 |
| w32 | 6 | 0.01248 | 0.335 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 2 | -0.005461 | -0.541 |
| w7 | 5 | -0.019176 | -1.614 |
| w8 | 9 | 0.037773 | 6.851 |
| w9 | 7 | 0.034176 | 0.665 |
| w10 | 3 | 0.027887 | 0.786 |
| w11 | 4 | -0.023749 | -2.233 |
| w12 | 5 | 0.087529 | 6.917 |
| w13 | 3 | 0.105308 | 2.657 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.004177 | -0.985 |
| w16 | 0 | None | 0.0 |
| w17 | 6 | 0.09007 | 4.127 |
| w18 | 3 | -0.000905 | 0.556 |
| w19 | 5 | 0.078617 | 6.923 |
| w20 | 4 | -0.168174 | 9.935 |
| w21 | 3 | 0.038189 | 1.794 |
| w22 | 1 | 0.038604 | 0.299 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | 0.009433 | -0.578 |
| w25 | 6 | 0.040005 | 2.616 |
| w26 | 4 | 0.139354 | 11.552 |
| w27 | 1 | 0.112248 | 2.928 |
| w28 | 3 | 0.064071 | 1.26 |
| w29 | 0 | None | 0.0 |
| w30 | 11 | -0.142187 | -9.117 |
| w31 | 9 | 0.026326 | 3.004 |
| w32 | 5 | 0.010349 | -0.15 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 8 | 0.065865 | 2.92 |
| w8 | 6 | 0.11835 | 10.009 |
| w9 | 11 | 0.030392 | 4.659 |
| w10 | 2 | 0.087928 | 0.876 |
| w11 | 5 | 0.037418 | -0.306 |
| w12 | 7 | 0.134508 | 8.543 |
| w13 | 3 | 0.046636 | 0.933 |
| w14 | 1 | -0.028 | -1.949 |
| w15 | 2 | -0.000658 | -0.507 |
| w16 | 0 | None | 0.0 |
| w17 | 6 | 0.071679 | 3.578 |
| w18 | 6 | -0.055174 | -3.524 |
| w19 | 9 | 0.105371 | 8.681 |
| w20 | 9 | 0.186997 | 18.267 |
| w21 | 5 | -0.001243 | -1.105 |
| w22 | 3 | 0.03486 | 0.303 |
| w23 | 1 | 0.062406 | 4.678 |
| w24 | 3 | 0.068432 | 1.318 |
| w25 | 0 | None | 0.0 |
| w26 | 8 | 0.107957 | 8.841 |
| w27 | 1 | -0.085641 | -2.51 |
| w28 | 6 | -0.115928 | -7.815 |
| w29 | 0 | None | 0.0 |
| w30 | 3 | 0.007965 | -0.935 |
| w31 | 4 | -0.047729 | -5.086 |
| w32 | 10 | 0.153908 | 16.917 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 2 | -0.085867 | -2.36 |
| w3 | 8 | 0.071846 | 8.274 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | 0.00021 | -0.142 |
| w6 | 0 | None | 0.0 |
| w7 | 4 | -0.003297 | -1.19 |
| w8 | 7 | 0.19482 | 22.559 |
| w9 | 13 | 0.259848 | 46.887 |
| w10 | 1 | 0.206206 | 1.229 |
| w11 | 4 | 0.042921 | 1.213 |
| w12 | 7 | 0.117024 | 7.645 |
| w13 | 1 | -0.009268 | -0.017 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.067106 | -2.063 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | 0.040874 | 0.941 |
| w18 | 1 | 0.020562 | 0.86 |
| w19 | 6 | 0.014656 | 0.846 |
| w20 | 5 | 0.066154 | 5.281 |
| w21 | 6 | -0.007429 | 0.107 |
| w22 | 1 | -0.02418 | -0.169 |
| w23 | 1 | -0.139094 | -4.181 |
| w24 | 5 | -0.001343 | -2.121 |
| w25 | 0 | None | 0.0 |
| w26 | 5 | 0.06427 | 5.571 |
| w27 | 1 | -0.022874 | -1.045 |
| w28 | 8 | 0.022047 | 2.286 |
| w29 | 0 | None | 0.0 |
| w30 | 8 | 0.035772 | 3.072 |
| w31 | 7 | 0.034203 | 3.374 |
| w32 | 3 | -0.006606 | -0.758 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 1 | 0.07901 | 0.847 |
| w11 | 6 | -0.003651 | -0.085 |
| w12 | 6 | 0.007022 | 0.258 |
| w13 | 2 | 0.131895 | 3.583 |
| w14 | 0 | None | 0.0 |
| w15 | 5 | 0.115167 | 4.483 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.067594 | 1.761 |
| w18 | 8 | 0.139206 | 16.692 |
| w19 | 11 | -0.002434 | -0.715 |
| w20 | 8 | 0.010446 | 2.626 |
| w21 | 14 | -0.04269 | -4.52 |
| w22 | 0 | None | 0.0 |
| w23 | 5 | -0.035287 | -2.087 |
| w24 | 4 | 0.028039 | -2.721 |
| w25 | 2 | 0.037872 | 1.63 |
| w26 | 11 | 0.129232 | 12.134 |
| w27 | 1 | -0.038371 | -2.286 |
| w28 | 10 | 0.007557 | -2.083 |
| w29 | 2 | 0.016462 | 0.0 |
| w30 | 12 | -0.080378 | -4.886 |
| w31 | 9 | -0.051484 | -3.385 |
| w32 | 4 | -0.055411 | -3.938 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 3 | 0.013989 | -1.351 |
| w13 | 4 | 0.034196 | 2.836 |
| w14 | 2 | -0.077829 | -6.026 |
| w15 | 5 | 0.038292 | 1.222 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | -0.065169 | -3.525 |
| w18 | 3 | 0.11551 | 7.996 |
| w19 | 3 | 0.04633 | 3.111 |
| w20 | 8 | 0.135162 | 12.698 |
| w21 | 4 | 0.029449 | 0.959 |
| w22 | 3 | 0.086138 | 3.16 |
| w23 | 9 | -0.150395 | -11.369 |
| w24 | 8 | -0.02464 | -10.261 |
| w25 | 3 | -0.020832 | -3.525 |
| w26 | 12 | -0.020733 | -1.849 |
| w27 | 3 | -0.058436 | -4.076 |
| w28 | 9 | -0.011831 | -1.944 |
| w29 | 0 | None | 0.0 |
| w30 | 12 | -0.086948 | -6.357 |
| w31 | 5 | -0.111022 | -7.073 |
| w32 | 5 | 0.098463 | 4.876 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 5 | 0.05388 | 1.536 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | -0.044211 | -2.12 |
| w18 | 2 | -0.003244 | -1.122 |
| w19 | 11 | 0.157434 | 15.019 |
| w20 | 10 | -0.032938 | -1.035 |
| w21 | 6 | 0.108591 | 6.077 |
| w22 | 4 | -0.029359 | -4.216 |
| w23 | 11 | 0.010671 | 2.644 |
| w24 | 4 | -0.015139 | -6.721 |
| w25 | 0 | 0.035659 | 0.0 |
| w26 | 12 | 0.09283 | 6.629 |
| w27 | 2 | -0.020434 | -2.467 |
| w28 | 7 | -0.043865 | -4.086 |
| w29 | 2 | 0.01344 | 0.028 |
| w30 | 12 | 0.032483 | 3.556 |
| w31 | 10 | -0.029515 | -4.827 |
| w32 | 7 | -0.02716 | -3.223 |

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
| w15 | 2 | -0.06297 | -4.631 |
| w16 | 0 | None | 0.0 |
| w17 | 6 | -0.148785 | -6.286 |
| w18 | 4 | 0.030773 | 1.568 |
| w19 | 5 | 0.158863 | 9.372 |
| w20 | 1 | -0.100653 | -4.279 |
| w21 | 7 | 0.078372 | 4.4 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 2 | 0.017246 | -0.013 |
| w26 | 1 | -0.07441 | -0.779 |
| w27 | 0 | None | 0.0 |
| w28 | 4 | -0.019978 | -1.765 |
| w29 | 0 | None | 0.0 |
| w30 | 7 | 0.031281 | 1.562 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 1 | -0.120467 | -8.079 |
| w17 | 6 | 0.033947 | 0.993 |
| w18 | 2 | -0.047881 | -0.656 |
| w19 | 7 | 0.144294 | 7.805 |
| w20 | 7 | -0.001613 | 1.276 |
| w21 | 10 | -0.076677 | -8.95 |
| w22 | 1 | 0.026313 | 0.601 |
| w23 | 3 | -0.064236 | -4.308 |
| w24 | 7 | 0.005375 | -8.386 |
| w25 | 3 | 0.03128 | 0.65 |
| w26 | 10 | -0.084562 | -9.148 |
| w27 | 3 | -0.029614 | -4.863 |
| w28 | 9 | 0.083188 | 5.713 |
| w29 | 3 | -0.065711 | -2.693 |
| w30 | 10 | -0.092973 | -6.633 |
| w31 | 11 | 0.019258 | 1.712 |
| w32 | 10 | 0.107589 | 7.119 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 8 | 0.035683 | 7.052 |
| w21 | 11 | 0.189667 | 14.243 |
| w22 | 1 | 0.049737 | 1.933 |
| w23 | 7 | 0.035384 | 2.247 |
| w24 | 4 | 0.022631 | -3.098 |
| w25 | 3 | 0.068307 | 2.75 |
| w26 | 13 | 0.030252 | 0.858 |
| w27 | 1 | -0.12289 | -0.999 |
| w28 | 11 | 0.040808 | 3.68 |
| w29 | 1 | 0.038766 | 0.265 |
| w30 | 9 | -0.10063 | -6.234 |
| w31 | 8 | -0.04807 | -2.65 |
| w32 | 4 | 0.02998 | 1.629 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 5 | 0.064313 | 2.569 |
| w23 | 5 | -0.164073 | -6.424 |
| w24 | 6 | 0.029439 | -3.29 |
| w25 | 1 | -0.034355 | -0.651 |
| w26 | 5 | 0.060034 | 3.838 |
| w27 | 3 | 0.026707 | 0.165 |
| w28 | 11 | -0.05026 | -4.655 |
| w29 | 2 | -0.022763 | -0.31 |
| w30 | 11 | -0.094478 | -8.993 |
| w31 | 7 | -0.004064 | -0.062 |
| w32 | 4 | 0.11399 | 5.456 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 6 | 0.018411 | -0.599 |
| w25 | 2 | 0.021965 | 0.674 |
| w26 | 14 | 0.066886 | 6.565 |
| w27 | 0 | None | 0.0 |
| w28 | 10 | 0.004485 | -0.726 |
| w29 | 0 | 0.019547 | 0.0 |
| w30 | 11 | -0.054823 | -3.026 |
| w31 | 7 | 0.006583 | 1.341 |
| w32 | 5 | -0.128884 | -9.31 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 2 | 0.047056 | 0.807 |
| w6 | 0 | None | 0.0 |
| w7 | 5 | 0.021298 | 1.358 |
| w8 | 8 | 0.012818 | 1.099 |
| w9 | 11 | 0.137134 | 13.479 |
| w10 | 6 | -0.089505 | -3.05 |
| w11 | 5 | 0.111777 | 4.394 |
| w12 | 11 | 0.035596 | 4.068 |
| w13 | 1 | 0.115526 | 3.698 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | 0.02692 | 1.151 |
| w16 | 0 | None | 0.0 |
| w17 | 6 | 0.07031 | 2.298 |
| w18 | 1 | -0.028359 | -0.388 |
| w19 | 6 | 0.032713 | 2.326 |
| w20 | 8 | 0.265242 | 18.258 |
| w21 | 9 | -0.072375 | -4.944 |
| w22 | 2 | 0.031972 | 0.979 |
| w23 | 4 | 0.067305 | 5.85 |
| w24 | 3 | -0.021929 | -1.622 |
| w25 | 3 | -0.138601 | -4.062 |
| w26 | 4 | 0.037949 | 1.138 |
| w27 | 1 | -0.027612 | -1.543 |
| w28 | 6 | 0.052948 | 2.54 |
| w29 | 2 | -0.054887 | -4.338 |
| w30 | 0 | None | 0.0 |
| w31 | 9 | -0.122931 | -8.312 |
| w32 | 1 | 0.004339 | -0.126 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.00467 | -0.214 |
| w7 | 5 | 0.199856 | 11.016 |
| w8 | 11 | 0.242682 | 18.541 |
| w9 | 8 | 0.039588 | 4.822 |
| w10 | 3 | 0.070035 | 0.954 |
| w11 | 3 | 0.027731 | 0.778 |
| w12 | 9 | 0.119481 | 9.06 |
| w13 | 3 | 0.057461 | 1.415 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | -0.040005 | -1.223 |
| w18 | 4 | 0.013275 | 0.059 |
| w19 | 7 | 0.132538 | 9.531 |
| w20 | 5 | 0.031285 | 0.237 |
| w21 | 4 | 0.058197 | 1.802 |
| w22 | 1 | -0.242602 | -8.492 |
| w23 | 2 | -0.098741 | -4.635 |
| w24 | 3 | -0.047277 | -3.769 |
| w25 | 6 | 0.010184 | -0.046 |
| w26 | 0 | -0.015292 | 0.0 |
| w27 | 2 | 0.01645 | 0.34 |
| w28 | 0 | None | 0.0 |
| w29 | 3 | -0.143608 | -9.972 |
| w30 | 0 | None | 0.0 |
| w31 | 4 | 0.030058 | 0.956 |
| w32 | 2 | 0.011831 | -0.112 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 8 | -0.001767 | -1.545 |
| w18 | 0 | None | 0.0 |
| w19 | 8 | -0.012793 | -0.388 |
| w20 | 8 | -0.138255 | -12.123 |
| w21 | 11 | 0.067518 | 5.489 |
| w22 | 2 | -0.024493 | -1.943 |
| w23 | 6 | 0.200878 | 17.672 |
| w24 | 4 | -0.033517 | -4.713 |
| w25 | 4 | 0.038486 | 0.842 |
| w26 | 10 | 0.170443 | 21.008 |
| w27 | 1 | 0.00392 | -1.115 |
| w28 | 5 | -0.005623 | -1.103 |
| w29 | 2 | -0.002083 | -0.25 |
| w30 | 12 | -0.170966 | -12.579 |
| w31 | 11 | -0.019574 | -1.019 |
| w32 | 3 | -0.076647 | -6.788 |

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
| w17 | 5 | 0.039328 | 1.22 |
| w18 | 6 | -0.04222 | -5.19 |
| w19 | 8 | 0.087041 | 6.726 |
| w20 | 4 | -0.101395 | -6.184 |
| w21 | 8 | 0.097642 | 6.635 |
| w22 | 4 | 0.052182 | 2.259 |
| w23 | 7 | -0.050103 | -4.152 |
| w24 | 3 | 0.036198 | -0.241 |
| w25 | 2 | -0.002151 | -0.116 |
| w26 | 4 | 0.055216 | 1.111 |
| w27 | 0 | None | 0.0 |
| w28 | 6 | 0.087338 | 6.766 |
| w29 | 0 | None | 0.0 |
| w30 | 9 | -0.058584 | -4.717 |
| w31 | 10 | -0.064287 | -4.475 |
| w32 | 5 | 0.09134 | 5.587 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 5 | 0.00902 | 1.925 |
| w20 | 6 | 0.098016 | 11.706 |
| w21 | 3 | 0.053248 | 2.247 |
| w22 | 0 | -0.012228 | 0.0 |
| w23 | 2 | 0.04494 | 0.976 |
| w24 | 3 | 0.021499 | -2.988 |
| w25 | 3 | 0.047235 | 1.846 |
| w26 | 8 | 0.127811 | 8.527 |
| w27 | 1 | 0.134121 | 0.658 |
| w28 | 11 | -0.060683 | -5.314 |
| w29 | 1 | 0.026341 | 0.142 |
| w30 | 11 | 0.045853 | 6.28 |
| w31 | 11 | -0.040781 | -3.807 |
| w32 | 3 | -0.222629 | -18.841 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 2 | 0.050548 | 1.863 |
| w23 | 6 | 0.028796 | 0.799 |
| w24 | 5 | -0.031688 | -6.389 |
| w25 | 2 | 0.065913 | 1.955 |
| w26 | 7 | 0.082677 | 6.4 |
| w27 | 3 | -0.022861 | -1.65 |
| w28 | 7 | 0.083474 | 5.088 |
| w29 | 3 | -0.312012 | -13.587 |
| w30 | 9 | -0.059944 | -3.76 |
| w31 | 9 | -0.0118 | -1.075 |
| w32 | 2 | 0.055008 | 1.734 |

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
| w27 | 2 | 0.004256 | -0.829 |
| w28 | 9 | -0.029976 | -2.704 |
| w29 | 3 | -0.035032 | -1.119 |
| w30 | 12 | 0.014413 | 4.464 |
| w31 | 11 | -0.030855 | -1.636 |
| w32 | 3 | -0.152803 | -5.639 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 6 | -0.160482 | -6.646 |
| w18 | 8 | -0.013726 | -1.761 |
| w19 | 8 | 0.037158 | 3.37 |
| w20 | 8 | 0.072745 | 6.217 |
| w21 | 8 | 0.030612 | 2.716 |
| w22 | 2 | 0.033747 | 0.813 |
| w23 | 6 | -0.034825 | -2.075 |
| w24 | 4 | 0.010073 | -4.33 |
| w25 | 1 | 0.037665 | 0.236 |
| w26 | 8 | 0.110645 | 8.15 |
| w27 | 3 | -0.057162 | -2.318 |
| w28 | 9 | -0.062357 | -4.164 |
| w29 | 1 | -0.039195 | -0.708 |
| w30 | 10 | -0.074195 | -13.847 |
| w31 | 10 | 0.037578 | 2.481 |
| w32 | 7 | -0.071123 | -5.66 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 7 | 0.322119 | 13.665 |
| w18 | 1 | 0.002301 | 0.03 |
| w19 | 8 | 0.114754 | 9.562 |
| w20 | 9 | -0.127479 | -11.883 |
| w21 | 8 | 0.028342 | 2.404 |
| w22 | 2 | 0.017963 | 0.139 |
| w23 | 4 | -0.007892 | -0.729 |
| w24 | 7 | -0.015657 | -8.803 |
| w25 | 0 | None | 0.0 |
| w26 | 10 | 0.146448 | 11.895 |
| w27 | 2 | -0.067775 | -2.984 |
| w28 | 8 | 0.00343 | 1.052 |
| w29 | 3 | 0.026795 | 0.259 |
| w30 | 13 | -0.029893 | -2.055 |
| w31 | 11 | 0.001346 | -0.179 |
| w32 | 9 | 0.049128 | 4.076 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 12 | 0.060601 | 3.869 |
| w29 | 0 | None | 0.0 |
| w30 | 5 | 0.031601 | 3.478 |
| w31 | 6 | 0.047834 | 3.199 |
| w32 | 8 | 0.074604 | 4.733 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 0 | None | 0.0 |
| w15 | 4 | 0.063571 | 3.906 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | -0.150456 | -6.654 |
| w18 | 3 | 0.003183 | 0.603 |
| w19 | 10 | 0.033831 | 2.089 |
| w20 | 7 | -0.226647 | -15.542 |
| w21 | 5 | 0.018599 | -0.215 |
| w22 | 2 | -0.133721 | -7.598 |
| w23 | 3 | 0.090159 | 4.534 |
| w24 | 5 | 0.003226 | -3.021 |
| w25 | 1 | -0.021996 | -0.683 |
| w26 | 10 | -0.115772 | -10.192 |
| w27 | 1 | -0.024862 | -0.407 |
| w28 | 11 | 0.014733 | 2.519 |
| w29 | 2 | -0.005959 | -0.359 |
| w30 | 10 | -0.012109 | 0.77 |
| w31 | 9 | -0.035642 | -2.006 |
| w32 | 7 | -0.151345 | -11.985 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 3 | 0.021078 | -0.604 |
| w26 | 6 | 0.070892 | 2.983 |
| w27 | 2 | -0.043783 | -2.249 |
| w28 | 9 | -0.024834 | -1.785 |
| w29 | 1 | -0.038296 | -1.568 |
| w30 | 12 | -0.008099 | 0.236 |
| w31 | 7 | -0.009485 | -1.463 |
| w32 | 4 | -0.039034 | -4.071 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

