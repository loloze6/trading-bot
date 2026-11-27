# Backtest of 032-02.g1.e2.e1_new-closing-high-continuation_1d

- Plan: `../../../../../03_test_plan/night7c_steadydecline_run/plans/032-02.g1.e2.e1_new-closing-high-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | 0.006443 | 3.923 |
| w2 | 19 | 0.17936 | 53.602 |
| w3 | 36 | -0.048653 | 120.573 |
| w4 | 24 | 0.02197 | -28.142 |
| w5 | 23 | 0.024265 | 139.835 |
| w6 | 22 | 0.122927 | 120.649 |
| w7 | 6 | -0.056248 | -4.047 |
| w8 | 16 | 0.065277 | 7.735 |
| w9 | 18 | -0.059175 | -45.75 |
| w10 | 30 | 0.009499 | 45.175 |
| w11 | 24 | 0.046313 | 68.655 |
| w12 | 14 | 0.000806 | -29.248 |
| w13 | 19 | 0.039116 | 35.778 |
| w14 | 25 | 0.010985 | 11.258 |
| w15 | 24 | 0.114087 | 195.587 |
| w16 | 22 | 0.069468 | 23.492 |
| w17 | 20 | 0.073861 | 8.229 |
| w18 | 16 | 0.045639 | -6.615 |
| w19 | 23 | -0.049078 | -13.041 |
| w20 | 21 | 0.067153 | -38.54 |
| w21 | 15 | -0.001721 | -30.28 |
| w22 | 31 | -0.049317 | 66.745 |
| w23 | 15 | 0.063357 | 4.617 |
| w24 | 34 | 0.010809 | 84.935 |
| w25 | 22 | 0.077244 | 40.909 |
| w26 | 18 | -0.070897 | -26.117 |
| w27 | 27 | -0.018064 | 67.513 |
| w28 | 13 | -0.099962 | 10.519 |
| w29 | 35 | 0.014029 | 10.666 |
| w30 | 14 | 0.033296 | -13.554 |
| w31 | 26 | 0.011463 | -10.33 |
| w32 | 31 | 0.076031 | 23.104 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | -0.023038 | 11.802 |
| w2 | 21 | 0.020873 | -13.145 |
| w3 | 28 | -0.200162 | -24.171 |
| w4 | 25 | 0.076572 | 134.091 |
| w5 | 23 | 0.084831 | 76.536 |
| w6 | 20 | 0.093404 | 157.38 |
| w7 | 8 | -0.048246 | -7.028 |
| w8 | 5 | 0.06974 | -12.015 |
| w9 | 11 | -0.195144 | -44.42 |
| w10 | 22 | -0.042321 | 56.328 |
| w11 | 15 | 0.054729 | 16.2 |
| w12 | 11 | -0.014615 | -33.564 |
| w13 | 16 | 0.039146 | 44.312 |
| w14 | 26 | -0.098233 | 13.081 |
| w15 | 13 | -0.043441 | 74.67 |
| w16 | 17 | 0.054029 | 20.546 |
| w17 | 11 | 0.031899 | -6.753 |
| w18 | 20 | 0.130221 | 3.347 |
| w19 | 10 | 0.023769 | -34.87 |
| w20 | 9 | 0.011688 | 0.679 |
| w21 | 14 | -0.070702 | 8.678 |
| w22 | 20 | -0.072529 | 4.988 |
| w23 | 11 | -0.116887 | -19.872 |
| w24 | 28 | -0.203216 | -14.133 |
| w25 | 20 | -0.005763 | 0.34 |
| w26 | 14 | -0.210766 | -19.318 |
| w27 | 25 | -0.05197 | 56.761 |
| w28 | 12 | -0.099419 | -15.14 |
| w29 | 18 | 0.001614 | 33.668 |
| w30 | 17 | -0.117385 | -36.087 |
| w31 | 15 | -0.021793 | -18.797 |
| w32 | 24 | 0.09763 | -1.67 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 20 | 0.15079 | 149.1 |
| w7 | 8 | 0.101214 | 6.508 |
| w8 | 10 | -0.004467 | -14.771 |
| w9 | 10 | 0.098041 | 14.391 |
| w10 | 13 | -0.148553 | -2.063 |
| w11 | 17 | 0.017929 | 2.238 |
| w12 | 16 | -0.05168 | -23.243 |
| w13 | 16 | 0.077119 | 26.51 |
| w14 | 29 | 0.059391 | 27.763 |
| w15 | 13 | 0.141739 | 225.403 |
| w16 | 21 | 0.103901 | 140.626 |
| w17 | 13 | 0.074324 | 24.399 |
| w18 | 19 | -0.087324 | -18.103 |
| w19 | 12 | -0.081232 | -13.311 |
| w20 | 11 | 0.053476 | 0.378 |
| w21 | 18 | 0.035263 | 18.334 |
| w22 | 26 | -0.153396 | 26.675 |
| w23 | 12 | -0.09278 | -3.468 |
| w24 | 20 | 0.040254 | 22.428 |
| w25 | 15 | 0.000732 | 9.053 |
| w26 | 17 | -0.04226 | -2.964 |
| w27 | 21 | 0.375706 | 349.248 |
| w28 | 13 | -0.091195 | -11.999 |
| w29 | 24 | 0.133932 | 60.398 |
| w30 | 10 | -0.049089 | -29.755 |
| w31 | 16 | -0.088369 | -26.351 |
| w32 | 18 | 0.027546 | -20.285 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 4 | -0.009068 | 5.492 |
| w8 | 7 | 0.102332 | -2.118 |
| w9 | 6 | -0.081617 | -36.689 |
| w10 | 20 | 0.078008 | 60.572 |
| w11 | 14 | -0.131827 | -15.297 |
| w12 | 10 | -0.00284 | -29.158 |
| w13 | 18 | 0.040678 | 60.208 |
| w14 | 25 | -0.109225 | -15.22 |
| w15 | 22 | -0.087288 | 1.823 |
| w16 | 17 | 0.110036 | 91.09 |
| w17 | 15 | -0.030179 | 3.758 |
| w18 | 15 | 0.012407 | -30.088 |
| w19 | 11 | 0.016789 | -4.863 |
| w20 | 9 | 0.109629 | 8.017 |
| w21 | 12 | -0.254153 | -31.542 |
| w22 | 22 | 0.04527 | -3.408 |
| w23 | 5 | 0.309947 | 103.135 |
| w24 | 28 | -0.13316 | -7.235 |
| w25 | 27 | 0.114988 | 42.52 |
| w26 | 15 | -0.115992 | -34.743 |
| w27 | 23 | -0.04564 | 19.483 |
| w28 | 11 | -0.109051 | -22.127 |
| w29 | 31 | -0.166714 | 23.886 |
| w30 | 25 | -0.152391 | -18.974 |
| w31 | 16 | -0.045063 | -19.564 |
| w32 | 13 | 0.144477 | -9.067 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | 0.206989 | 232.659 |
| w2 | 32 | 0.048696 | 8.059 |
| w3 | 7 | 0.091893 | 1.813 |
| w4 | 35 | 0.131785 | 379.183 |
| w5 | 24 | 0.205425 | 164.612 |
| w6 | 16 | 0.078008 | 85.586 |
| w7 | 12 | 0.155509 | 30.304 |
| w8 | 6 | 0.072275 | -8.705 |
| w9 | 6 | -0.043666 | -14.174 |
| w10 | 17 | 0.015121 | 13.786 |
| w11 | 20 | 0.123241 | 58.668 |
| w12 | 11 | -0.112693 | -24.116 |
| w13 | 21 | 0.079602 | 75.045 |
| w14 | 23 | -0.05304 | 84.316 |
| w15 | 28 | -0.02894 | 27.715 |
| w16 | 20 | -0.007027 | 105.644 |
| w17 | 12 | 0.089732 | 62.1 |
| w18 | 18 | -0.060538 | 1.043 |
| w19 | 13 | -0.006368 | -11.984 |
| w20 | 13 | 0.153971 | 16.538 |
| w21 | 13 | 0.019786 | -0.773 |
| w22 | 31 | -0.143237 | 34.72 |
| w23 | 16 | -0.161782 | -22.087 |
| w24 | 36 | -0.012556 | 32.534 |
| w25 | 23 | 0.12297 | 34.174 |
| w26 | 13 | -0.057854 | -8.853 |
| w27 | 24 | -0.093114 | 17.294 |
| w28 | 3 | -0.082486 | -4.331 |
| w29 | 29 | 0.05168 | 73.123 |
| w30 | 15 | -0.110597 | -31.747 |
| w31 | 23 | 0.016013 | -15.62 |
| w32 | 23 | -0.003983 | 23.124 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 21 | 0.035615 | 49.623 |
| w11 | 19 | -0.084064 | -16.572 |
| w12 | 13 | -0.058832 | -33.143 |
| w13 | 11 | 0.086668 | 87.627 |
| w14 | 25 | -0.101581 | 56.77 |
| w15 | 22 | -0.037486 | 31.825 |
| w16 | 29 | 0.142175 | 118.581 |
| w17 | 14 | 0.100517 | 61.247 |
| w18 | 8 | -0.159395 | -28.09 |
| w19 | 11 | 0.111675 | -9.778 |
| w20 | 17 | -0.120524 | -16.258 |
| w21 | 4 | -0.241002 | -29.266 |
| w22 | 22 | -0.065706 | 14.031 |
| w23 | 6 | 0.086186 | -42.024 |
| w24 | 22 | 0.106918 | 213.208 |
| w25 | 13 | 0.09069 | 3.469 |
| w26 | 10 | -0.039037 | -16.9 |
| w27 | 25 | 0.17754 | 167.246 |
| w28 | 9 | -0.166068 | -21.793 |
| w29 | 19 | 0.051859 | 12.573 |
| w30 | 12 | -0.008364 | -20.354 |
| w31 | 13 | -0.173334 | -30.682 |
| w32 | 23 | 0.073877 | -14.521 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 18 | -0.076389 | 10.097 |
| w13 | 16 | -0.031479 | -19.759 |
| w14 | 17 | -0.017698 | 72.963 |
| w15 | 17 | -0.208763 | -2.545 |
| w16 | 20 | 0.09307 | 58.481 |
| w17 | 18 | 0.05999 | 10.561 |
| w18 | 7 | -0.171909 | 23.959 |
| w19 | 15 | -0.112777 | -24.059 |
| w20 | 12 | 0.014967 | 9.427 |
| w21 | 10 | 0.015269 | -8.366 |
| w22 | 18 | -0.091507 | 13.469 |
| w23 | 10 | -0.011353 | -4.353 |
| w24 | 24 | -0.186722 | 28.935 |
| w25 | 14 | 0.066889 | -0.956 |
| w26 | 4 | 0.001298 | 0.364 |
| w27 | 19 | 0.068495 | 73.453 |
| w28 | 8 | -0.230531 | -29.935 |
| w29 | 17 | -0.0229 | -3.968 |
| w30 | 8 | -0.022899 | -13.097 |
| w31 | 19 | 0.035287 | -1.896 |
| w32 | 17 | 0.014401 | -18.151 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 13 | -0.108706 | -12.757 |
| w16 | 19 | 0.092257 | 81.541 |
| w17 | 19 | -0.012408 | 4.165 |
| w18 | 16 | -0.06533 | 39.348 |
| w19 | 10 | -0.009704 | -30.306 |
| w20 | 8 | 0.03737 | -3.225 |
| w21 | 7 | 0.03605 | -20.956 |
| w22 | 20 | -0.022631 | -11.089 |
| w23 | 8 | -0.040662 | -17.904 |
| w24 | 26 | 0.013053 | 139.841 |
| w25 | 10 | 0.124638 | 8.748 |
| w26 | 11 | -0.154354 | -43.098 |
| w27 | 22 | 0.131115 | 255.438 |
| w28 | 7 | 0.026454 | 5.448 |
| w29 | 13 | 0.142906 | 36.796 |
| w30 | 0 | None | 0.0 |
| w31 | 20 | -0.021207 | -19.622 |
| w32 | 14 | -0.041533 | -31.206 |

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
| w15 | 13 | -0.044093 | 11.999 |
| w16 | 20 | 0.04728 | 105.527 |
| w17 | 11 | 0.032049 | 26.792 |
| w18 | 21 | -0.072885 | -15.258 |
| w19 | 12 | 0.024704 | 8.937 |
| w20 | 25 | -0.113429 | -32.363 |
| w21 | 18 | -0.077253 | -39.754 |
| w22 | 25 | -0.061945 | 33.575 |
| w23 | 32 | -0.025649 | -12.271 |
| w24 | 41 | -0.022418 | 37.086 |
| w25 | 27 | 0.138203 | 39.881 |
| w26 | 29 | 0.018212 | 28.391 |
| w27 | 30 | 0.124567 | 149.075 |
| w28 | 22 | -0.102853 | -20.173 |
| w29 | 47 | -0.032582 | 39.526 |
| w30 | 13 | -0.006954 | -16.066 |
| w31 | 40 | 0.076175 | 36.451 |
| w32 | 36 | 0.046183 | 9.641 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 31 | -0.012454 | 77.256 |
| w17 | 16 | 0.031111 | -1.26 |
| w18 | 7 | -0.157077 | -0.081 |
| w19 | 17 | 0.015443 | -29.1 |
| w20 | 13 | 0.014256 | -5.457 |
| w21 | 5 | -0.05625 | -15.042 |
| w22 | 22 | -0.029776 | 13.358 |
| w23 | 13 | -0.055642 | -10.333 |
| w24 | 19 | 0.03534 | 46.223 |
| w25 | 16 | 0.081786 | 1.306 |
| w26 | 10 | -0.066943 | -17.435 |
| w27 | 25 | 0.105047 | 87.816 |
| w28 | 8 | -0.168612 | -33.223 |
| w29 | 19 | 0.039353 | 2.932 |
| w30 | 12 | 0.010545 | -28.514 |
| w31 | 15 | -0.105934 | -33.683 |
| w32 | 13 | -0.084959 | -31.076 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 16 | 0.12077 | 11.409 |
| w21 | 7 | -0.117514 | -24.336 |
| w22 | 14 | -0.033838 | 12.214 |
| w23 | 6 | 0.027988 | -3.503 |
| w24 | 23 | 0.156322 | 177.237 |
| w25 | 12 | 0.034386 | 27.463 |
| w26 | 9 | -0.068437 | -17.821 |
| w27 | 28 | 0.060691 | 60.53 |
| w28 | 7 | -0.067222 | -7.591 |
| w29 | 20 | -0.007502 | -5.935 |
| w30 | 6 | 0.176633 | 12.046 |
| w31 | 18 | -0.014614 | -17.685 |
| w32 | 18 | -0.046994 | -10.992 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 15 | -0.123327 | 19.198 |
| w23 | 9 | 0.03468 | -1.346 |
| w24 | 20 | 0.049419 | 147.212 |
| w25 | 6 | 0.008873 | 53.252 |
| w26 | 12 | -0.053302 | -18.42 |
| w27 | 19 | 0.007758 | 30.227 |
| w28 | 3 | -0.110914 | -19.295 |
| w29 | 19 | 0.023465 | 2.87 |
| w30 | 12 | -0.017419 | -20.58 |
| w31 | 23 | -0.027974 | -12.112 |
| w32 | 17 | -0.011256 | 41.517 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 20 | -0.042248 | 13.667 |
| w25 | 11 | -0.038405 | 23.861 |
| w26 | 9 | -0.086192 | -28.736 |
| w27 | 20 | -0.009519 | 92.706 |
| w28 | 7 | 0.121727 | 20.552 |
| w29 | 19 | -0.03851 | 5.318 |
| w30 | 10 | 0.006637 | -25.942 |
| w31 | 17 | -0.012033 | -14.902 |
| w32 | 17 | 0.052062 | -19.289 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 26 | 0.157744 | 121.276 |
| w6 | 21 | -0.025983 | 8.073 |
| w7 | 11 | -0.038285 | -15.431 |
| w8 | 12 | -0.032384 | -22.755 |
| w9 | 9 | -0.067342 | -36.464 |
| w10 | 20 | -0.066716 | 10.738 |
| w11 | 12 | -0.007955 | 12.145 |
| w12 | 8 | -0.129949 | -42.914 |
| w13 | 22 | 0.03465 | 80.764 |
| w14 | 26 | -0.144488 | 35.999 |
| w15 | 11 | -0.062292 | 7.22 |
| w16 | 24 | 0.131367 | 62.723 |
| w17 | 14 | 0.020089 | 0.613 |
| w18 | 18 | -0.042052 | 5.982 |
| w19 | 12 | 0.075961 | 29.32 |
| w20 | 9 | 0.051949 | -10.38 |
| w21 | 5 | -0.072898 | -11.167 |
| w22 | 14 | -0.130627 | -4.699 |
| w23 | 12 | -0.08902 | -18.551 |
| w24 | 24 | -0.071838 | 3.764 |
| w25 | 9 | 0.070479 | 10.817 |
| w26 | 22 | 0.08159 | 37.524 |
| w27 | 23 | -0.017008 | 36.963 |
| w28 | 9 | -0.197367 | -27.334 |
| w29 | 20 | -0.051954 | -8.008 |
| w30 | 20 | 0.122747 | 340.498 |
| w31 | 14 | 0.123941 | 16.333 |
| w32 | 18 | 0.07695 | 71.298 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 27 | 0.117884 | 137.632 |
| w6 | 18 | 0.129497 | 121.136 |
| w7 | 6 | 0.02714 | -2.178 |
| w8 | 6 | 0.023126 | -3.217 |
| w9 | 8 | -0.059375 | -38.396 |
| w10 | 20 | -0.140865 | 14.265 |
| w11 | 27 | 0.049687 | 1.934 |
| w12 | 11 | -0.053895 | -39.756 |
| w13 | 16 | 0.007785 | 32.262 |
| w14 | 23 | -0.227932 | 37.417 |
| w15 | 26 | -0.086416 | 23.37 |
| w16 | 18 | 0.015179 | 59.675 |
| w17 | 14 | 0.035191 | 9.232 |
| w18 | 17 | -0.187773 | -29.156 |
| w19 | 20 | -0.074803 | -20.095 |
| w20 | 14 | 0.038548 | -4.996 |
| w21 | 17 | -0.049903 | -12.148 |
| w22 | 23 | -0.026813 | 3.163 |
| w23 | 19 | 0.015392 | -8.472 |
| w24 | 40 | -0.075392 | 9.249 |
| w25 | 14 | -0.173705 | -47.418 |
| w26 | 19 | -0.029236 | 19.4 |
| w27 | 33 | -0.063871 | 10.354 |
| w28 | 27 | -0.064745 | 18.673 |
| w29 | 19 | 0.178051 | 23.088 |
| w30 | 38 | -0.103104 | 22.356 |
| w31 | 13 | 0.127578 | 25.743 |
| w32 | 28 | 0.02164 | 61.648 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 17 | -0.089795 | -7.32 |
| w18 | 20 | -0.160647 | 16.59 |
| w19 | 8 | 0.020388 | -15.405 |
| w20 | 10 | -0.022345 | -5.467 |
| w21 | 9 | -0.167596 | -38.125 |
| w22 | 17 | -0.041469 | 32.847 |
| w23 | 6 | -0.008749 | -1.233 |
| w24 | 21 | -0.117869 | -1.251 |
| w25 | 10 | 0.069914 | 9.52 |
| w26 | 13 | -0.059193 | -24.892 |
| w27 | 14 | 0.173015 | 266.877 |
| w28 | 10 | -0.005137 | 12.429 |
| w29 | 15 | 0.131871 | 17.933 |
| w30 | 1 | -0.015136 | -16.044 |
| w31 | 14 | -0.011068 | -24.873 |
| w32 | 25 | 0.068695 | 33.867 |

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
| w17 | 18 | -0.033865 | -15.04 |
| w18 | 18 | -0.066912 | -31.415 |
| w19 | 12 | 0.081004 | -11.543 |
| w20 | 10 | -0.052656 | -27.828 |
| w21 | 18 | 0.010502 | -24.55 |
| w22 | 12 | -0.069102 | 6.971 |
| w23 | 8 | 0.069971 | 6.35 |
| w24 | 21 | -0.070388 | 45.078 |
| w25 | 13 | 0.048272 | 6.048 |
| w26 | 29 | 0.026361 | 21.047 |
| w27 | 30 | 0.003311 | 42.829 |
| w28 | 5 | -0.045456 | -6.478 |
| w29 | 27 | -0.033366 | 8.396 |
| w30 | 7 | -0.082208 | -16.836 |
| w31 | 8 | -0.197694 | -31.567 |
| w32 | 22 | 0.043718 | 11.377 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 11 | -0.085577 | -15.666 |
| w20 | 8 | 0.067703 | -4.496 |
| w21 | 17 | -0.069581 | -9.414 |
| w22 | 24 | 0.060507 | 141.548 |
| w23 | 15 | -0.067941 | -18.104 |
| w24 | 18 | 0.104535 | 311.284 |
| w25 | 11 | -0.053748 | -12.049 |
| w26 | 8 | 0.00227 | -4.576 |
| w27 | 22 | -0.036517 | 12.335 |
| w28 | 4 | -0.032516 | -7.984 |
| w29 | 30 | -0.020727 | -7.067 |
| w30 | 10 | -0.031614 | -22.994 |
| w31 | 12 | -0.061124 | -10.443 |
| w32 | 20 | -0.003134 | 23.051 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 20 | -0.055465 | 13.63 |
| w23 | 10 | -0.178595 | -33.045 |
| w24 | 20 | -0.173426 | 48.288 |
| w25 | 11 | -0.000644 | -4.135 |
| w26 | 9 | 0.001313 | -15.814 |
| w27 | 22 | -0.072215 | 9.214 |
| w28 | 7 | -0.099021 | -18.097 |
| w29 | 21 | 0.070247 | 14.464 |
| w30 | 9 | -0.076544 | -21.08 |
| w31 | 19 | 0.055104 | -8.053 |
| w32 | 12 | 0.113526 | 21.755 |

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
| w27 | 21 | 0.020041 | 45.94 |
| w28 | 8 | -0.042479 | -9.104 |
| w29 | 17 | 0.071955 | 14.402 |
| w30 | 8 | -0.060554 | -13.829 |
| w31 | 12 | -0.12933 | -22.296 |
| w32 | 15 | 0.099145 | 54.865 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 9 | 0.073117 | 9.113 |
| w18 | 4 | 0.13232 | 1.444 |
| w19 | 9 | 0.050228 | -10.8 |
| w20 | 7 | 0.21108 | 42.222 |
| w21 | 10 | -0.082943 | -41.152 |
| w22 | 17 | -0.022932 | 22.296 |
| w23 | 10 | -0.060644 | -9.666 |
| w24 | 22 | -0.025429 | 107.09 |
| w25 | 10 | 0.144132 | 25.886 |
| w26 | 4 | -0.150551 | -31.142 |
| w27 | 17 | 0.061583 | 62.525 |
| w28 | 6 | -0.097887 | -21.76 |
| w29 | 13 | -0.031953 | -0.653 |
| w30 | 10 | -0.105557 | -33.392 |
| w31 | 18 | -0.122223 | -32.185 |
| w32 | 13 | 0.092713 | -13.146 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 10 | 0.046563 | 2.266 |
| w18 | 17 | 0.008061 | -5.066 |
| w19 | 5 | 0.049102 | -1.232 |
| w20 | 10 | 0.05632 | -0.386 |
| w21 | 7 | -0.159011 | -40.673 |
| w22 | 19 | 0.022706 | 82.612 |
| w23 | 7 | -0.1908 | -31.649 |
| w24 | 16 | 0.017843 | 53.578 |
| w25 | 10 | 0.164375 | 57.909 |
| w26 | 7 | -0.020656 | -16.78 |
| w27 | 17 | 0.034132 | 53.593 |
| w28 | 4 | -0.035023 | -8.014 |
| w29 | 14 | 0.035624 | 3.547 |
| w30 | 8 | -0.04405 | -24.647 |
| w31 | 15 | -0.132817 | -38.704 |
| w32 | 15 | -0.022784 | -13.857 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 8 | 0.067819 | -8.089 |
| w29 | 15 | -0.010643 | -1.17 |
| w30 | 15 | -0.025975 | -6.558 |
| w31 | 16 | 0.109846 | 3.288 |
| w32 | 12 | -0.07004 | -10.523 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 16 | 0.088347 | 7.006 |
| w15 | 14 | 0.05584 | 74.319 |
| w16 | 20 | 0.044108 | 790.369 |
| w17 | 11 | 0.094076 | 0.981 |
| w18 | 13 | -0.02926 | -8.482 |
| w19 | 13 | -0.014953 | -28.056 |
| w20 | 6 | 0.050345 | -1.114 |
| w21 | 7 | 0.253563 | 69.59 |
| w22 | 23 | -0.001241 | -4.76 |
| w23 | 11 | 0.112753 | 6.176 |
| w24 | 27 | 0.094862 | 32.981 |
| w25 | 17 | 0.143872 | 104.657 |
| w26 | 12 | -0.115752 | -25.14 |
| w27 | 26 | 0.15925 | 174.513 |
| w28 | 5 | -0.064698 | -13.658 |
| w29 | 16 | 0.088505 | 21.5 |
| w30 | 9 | 0.09322 | 0.37 |
| w31 | 20 | -0.015019 | -11.84 |
| w32 | 17 | 0.122277 | 1.078 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 9 | 0.199005 | 158.092 |
| w26 | 14 | 0.073232 | 7.216 |
| w27 | 21 | 0.140613 | 66.381 |
| w28 | 6 | -0.08874 | -7.431 |
| w29 | 15 | 0.034298 | 6.806 |
| w30 | 6 | -0.031248 | -23.683 |
| w31 | 14 | 0.113029 | 16.578 |
| w32 | 20 | 0.080234 | -1.762 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

