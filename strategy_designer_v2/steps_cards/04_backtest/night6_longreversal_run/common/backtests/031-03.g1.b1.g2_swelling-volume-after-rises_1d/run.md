# Backtest of 031-03.g1.b1.g2_swelling-volume-after-rises_1d

- Plan: `../../../../../03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.g2_swelling-volume-after-rises_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.001528 | 3.384 |
| w2 | 13 | 0.053602 | 42.777 |
| w3 | 19 | -0.048726 | 34.331 |
| w4 | 14 | -0.121601 | -30.133 |
| w5 | 17 | 0.004547 | 57.295 |
| w6 | 10 | 0.036124 | 43.694 |
| w7 | 4 | 0.093256 | 3.816 |
| w8 | 9 | -0.072715 | -16.93 |
| w9 | 2 | -0.023716 | -0.673 |
| w10 | 13 | -0.016822 | 8.077 |
| w11 | 19 | 0.027942 | 20.68 |
| w12 | 11 | -0.026844 | -13.896 |
| w13 | 16 | -0.061508 | 8.721 |
| w14 | 17 | 0.032997 | 9.085 |
| w15 | 22 | 0.083311 | 93.302 |
| w16 | 11 | 0.019587 | 13.494 |
| w17 | 13 | 0.0624 | -0.014 |
| w18 | 8 | 0.163296 | 21.149 |
| w19 | 6 | -0.017275 | 2.658 |
| w20 | 4 | 0.024146 | 0.232 |
| w21 | 9 | -0.181951 | -16.739 |
| w22 | 23 | 0.052145 | 34.402 |
| w23 | 12 | 0.102431 | 1.441 |
| w24 | 27 | 0.026653 | 110.688 |
| w25 | 23 | -0.070139 | -3.381 |
| w26 | 8 | 0.050019 | -10.879 |
| w27 | 11 | 0.166957 | 65.55 |
| w28 | 6 | -0.046417 | -1.72 |
| w29 | 18 | -0.163316 | -17.636 |
| w30 | 9 | -0.011588 | -24.215 |
| w31 | 7 | 0.030252 | -12.817 |
| w32 | 7 | 0.032898 | -1.345 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.100994 | -16.707 |
| w2 | 9 | -0.081243 | 18.731 |
| w3 | 24 | -0.111104 | -7.572 |
| w4 | 11 | -0.070641 | 128.275 |
| w5 | 20 | -0.107827 | 17.733 |
| w6 | 15 | -0.051748 | 6.322 |
| w7 | 7 | 0.035327 | -1.54 |
| w8 | 9 | 0.001859 | -12.477 |
| w9 | 6 | 0.016035 | -4.669 |
| w10 | 15 | -0.0699 | 0.992 |
| w11 | 14 | 0.11423 | 11.908 |
| w12 | 6 | 0.074086 | -1.097 |
| w13 | 13 | 0.006534 | 15.295 |
| w14 | 17 | -0.018658 | 32.473 |
| w15 | 21 | 0.039254 | 58.933 |
| w16 | 17 | -0.057587 | 5.039 |
| w17 | 11 | 0.052021 | 0.719 |
| w18 | 13 | -0.124125 | -32.274 |
| w19 | 7 | -0.162919 | -9.134 |
| w20 | 4 | -0.069148 | -3.274 |
| w21 | 11 | -0.197973 | 1.373 |
| w22 | 11 | 0.065294 | 13.732 |
| w23 | 16 | -0.041895 | -11.142 |
| w24 | 30 | -0.022994 | -1.64 |
| w25 | 13 | -0.043 | 11.669 |
| w26 | 6 | 0.029366 | -3.768 |
| w27 | 19 | 0.123421 | 53.709 |
| w28 | 6 | -0.11327 | -7.923 |
| w29 | 12 | -0.042844 | 3.693 |
| w30 | 8 | -0.144529 | -39.043 |
| w31 | 2 | -0.023369 | -0.074 |
| w32 | 20 | -0.117896 | -23.02 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 24 | 0.024453 | 28.484 |
| w7 | 9 | 0.067533 | -5.748 |
| w8 | 9 | 0.082388 | -20.431 |
| w9 | 14 | 0.129119 | 17.839 |
| w10 | 15 | -0.085888 | -9.731 |
| w11 | 7 | 0.077608 | 4.813 |
| w12 | 9 | -0.258585 | -22.65 |
| w13 | 12 | -0.08756 | -26.894 |
| w14 | 16 | 0.102113 | 51.551 |
| w15 | 12 | 0.245105 | 220.606 |
| w16 | 16 | 0.027975 | 34.853 |
| w17 | 16 | 0.035317 | 17.972 |
| w18 | 9 | -0.066011 | -12.032 |
| w19 | 5 | -0.066459 | 6.399 |
| w20 | 3 | -0.066231 | 0.715 |
| w21 | 8 | 0.149923 | 32.715 |
| w22 | 13 | 0.172107 | 66.994 |
| w23 | 16 | -0.031687 | -3.239 |
| w24 | 16 | 0.091614 | 24.654 |
| w25 | 12 | 0.022105 | 13.589 |
| w26 | 10 | 0.161 | 33.595 |
| w27 | 18 | 0.357472 | 227.969 |
| w28 | 9 | -0.027523 | -2.432 |
| w29 | 13 | 0.031384 | 15.411 |
| w30 | 2 | -0.135339 | -1.526 |
| w31 | 11 | -0.070029 | -19.347 |
| w32 | 15 | 0.132353 | -3.614 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 8 | 0.078286 | 7.012 |
| w8 | 4 | 0.168692 | -6.19 |
| w9 | 15 | -0.082515 | -48.734 |
| w10 | 18 | 0.033671 | 68.145 |
| w11 | 13 | 0.030809 | -1.735 |
| w12 | 11 | 0.056823 | 0.758 |
| w13 | 9 | 0.028607 | 29.713 |
| w14 | 9 | -0.034208 | -10.949 |
| w15 | 20 | -0.042284 | 13.518 |
| w16 | 20 | 0.026705 | 42.507 |
| w17 | 6 | -0.272186 | -8.989 |
| w18 | 11 | -0.11214 | -35.175 |
| w19 | 9 | -0.001349 | -4.109 |
| w20 | 5 | 0.039813 | -0.065 |
| w21 | 10 | -0.204883 | -17.077 |
| w22 | 18 | 0.022643 | 1.247 |
| w23 | 10 | 0.271242 | 78.707 |
| w24 | 24 | -0.207633 | -9.064 |
| w25 | 20 | -0.072868 | 24.244 |
| w26 | 10 | 0.032943 | -13.44 |
| w27 | 15 | 0.09877 | 47.138 |
| w28 | 8 | -0.055835 | -22.96 |
| w29 | 22 | -0.032468 | 15.995 |
| w30 | 19 | 0.021475 | -7.082 |
| w31 | 8 | 0.024403 | -17.842 |
| w32 | 4 | -0.093619 | -37.121 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | 0.057605 | 89.537 |
| w2 | 13 | -0.189209 | -12.74 |
| w3 | 10 | -0.029626 | -11.058 |
| w4 | 21 | 0.083736 | 125.84 |
| w5 | 17 | -0.041886 | 53.985 |
| w6 | 15 | 0.139022 | 37.489 |
| w7 | 9 | -0.051969 | -4.813 |
| w8 | 4 | 0.020127 | -3.622 |
| w9 | 5 | -0.041635 | -4.012 |
| w10 | 22 | -0.022673 | 5.476 |
| w11 | 14 | 0.156971 | 20.593 |
| w12 | 12 | -0.18896 | -12.516 |
| w13 | 24 | -0.051941 | 2.365 |
| w14 | 13 | 0.105324 | 40.657 |
| w15 | 20 | 0.069979 | 24.616 |
| w16 | 17 | 0.096131 | 60.894 |
| w17 | 16 | 0.104557 | 25.857 |
| w18 | 18 | -0.037956 | -11.549 |
| w19 | 7 | -0.017915 | -3.518 |
| w20 | 6 | 0.085053 | 3.61 |
| w21 | 7 | -0.119493 | -25.177 |
| w22 | 19 | -0.025767 | 10.544 |
| w23 | 9 | -0.083899 | 1.299 |
| w24 | 26 | -0.031354 | 29.238 |
| w25 | 18 | 0.146344 | 45.038 |
| w26 | 9 | 0.020494 | -12.249 |
| w27 | 16 | 0.049964 | 26.094 |
| w28 | 4 | -0.036326 | -19.096 |
| w29 | 24 | -0.025141 | 29.627 |
| w30 | 5 | 0.012206 | -5.069 |
| w31 | 7 | 0.018663 | -17.014 |
| w32 | 9 | -0.013566 | 3.908 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 19 | 0.052821 | 49.385 |
| w11 | 10 | 0.0851 | 4.269 |
| w12 | 11 | -0.054283 | -15.061 |
| w13 | 22 | 0.030991 | 40.114 |
| w14 | 26 | -0.061445 | 19.17 |
| w15 | 8 | 0.083863 | 42.487 |
| w16 | 20 | 0.057994 | 47.409 |
| w17 | 17 | -0.105583 | 25.538 |
| w18 | 4 | -0.098537 | -16.947 |
| w19 | 12 | -0.133217 | -28.869 |
| w20 | 11 | -0.031108 | -0.474 |
| w21 | 6 | -0.007115 | -14.376 |
| w22 | 17 | 0.019032 | 26.109 |
| w23 | 5 | -0.044199 | -5.874 |
| w24 | 25 | -0.015616 | 74.27 |
| w25 | 17 | 0.05162 | 6.522 |
| w26 | 12 | 0.029906 | -3.804 |
| w27 | 14 | 0.360812 | 201.431 |
| w28 | 8 | -0.100651 | -19.819 |
| w29 | 19 | 0.115237 | 27.162 |
| w30 | 4 | -0.097579 | -17.128 |
| w31 | 13 | -0.130348 | -12.257 |
| w32 | 17 | -0.163849 | -8.471 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 23 | 0.012606 | 5.251 |
| w13 | 16 | -0.087387 | -8.307 |
| w14 | 24 | 0.051381 | 35.306 |
| w15 | 14 | -0.075273 | 13.691 |
| w16 | 14 | -0.076152 | 21.975 |
| w17 | 8 | 0.031528 | 10.843 |
| w18 | 15 | 0.048784 | 11.918 |
| w19 | 13 | -0.004499 | -6.82 |
| w20 | 12 | -0.017497 | 7.443 |
| w21 | 11 | -0.162938 | 0.045 |
| w22 | 21 | -0.069771 | -0.689 |
| w23 | 5 | -0.03198 | -6.625 |
| w24 | 23 | -0.009883 | 30.606 |
| w25 | 11 | 0.129922 | 24.274 |
| w26 | 9 | -0.145946 | -17.103 |
| w27 | 9 | 0.220234 | 75.897 |
| w28 | 9 | -0.001915 | -2.611 |
| w29 | 21 | -0.033325 | -4.332 |
| w30 | 6 | 0.022431 | -15.222 |
| w31 | 20 | 0.012844 | -13.762 |
| w32 | 17 | -0.020916 | -7.883 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 4 | 0.039125 | 9.341 |
| w16 | 25 | -0.063257 | 12.056 |
| w17 | 13 | 0.06473 | 17.267 |
| w18 | 8 | 0.010253 | 16.047 |
| w19 | 10 | -0.076489 | -20.42 |
| w20 | 7 | -0.211969 | -37.848 |
| w21 | 14 | -0.077318 | -18.804 |
| w22 | 16 | 0.046346 | -2.389 |
| w23 | 7 | 0.004565 | -7.467 |
| w24 | 22 | 0.069257 | 68.164 |
| w25 | 15 | 0.084033 | 16.551 |
| w26 | 6 | 0.11271 | 0.711 |
| w27 | 17 | 0.324664 | 186.393 |
| w28 | 5 | -0.030437 | -11.545 |
| w29 | 15 | -0.095821 | 13.779 |
| w30 | 6 | -0.11368 | -26.34 |
| w31 | 9 | 0.132387 | 12.37 |
| w32 | 14 | -0.165089 | -4.891 |

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
| w15 | 13 | -0.014665 | -0.213 |
| w16 | 21 | -0.041813 | 30.293 |
| w17 | 12 | 0.03578 | 12.108 |
| w18 | 11 | 0.052216 | -9.901 |
| w19 | 8 | -0.115001 | -20.586 |
| w20 | 4 | 0.044983 | 1.743 |
| w21 | 8 | -0.077911 | -25.638 |
| w22 | 13 | -0.192118 | 5.598 |
| w23 | 16 | -0.105639 | -5.965 |
| w24 | 21 | -0.082497 | 33.003 |
| w25 | 13 | 0.00185 | 4.159 |
| w26 | 15 | 0.032818 | 7.033 |
| w27 | 13 | -0.078754 | 30.739 |
| w28 | 11 | -0.080318 | -1.769 |
| w29 | 21 | -0.009313 | 22.597 |
| w30 | 12 | -0.05024 | -9.0 |
| w31 | 25 | -0.027959 | 5.171 |
| w32 | 18 | 0.068558 | 7.302 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 11 | 0.129371 | 42.04 |
| w17 | 13 | -0.035862 | -3.126 |
| w18 | 12 | 0.026768 | -0.354 |
| w19 | 6 | 0.010918 | -8.137 |
| w20 | 14 | 0.005686 | 2.784 |
| w21 | 12 | -0.00257 | -22.198 |
| w22 | 15 | -0.094388 | -1.184 |
| w23 | 5 | -0.013619 | 5.773 |
| w24 | 14 | -0.014506 | 36.788 |
| w25 | 11 | 0.119447 | 15.636 |
| w26 | 8 | 0.055283 | -9.823 |
| w27 | 12 | 0.279069 | 114.46 |
| w28 | 3 | -0.262569 | -3.095 |
| w29 | 13 | -0.088398 | -16.638 |
| w30 | 11 | -0.119183 | -25.772 |
| w31 | 10 | -0.035943 | -6.586 |
| w32 | 10 | -0.082868 | -13.068 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 9 | 0.025869 | 5.173 |
| w21 | 8 | -0.179852 | -19.029 |
| w22 | 17 | -0.048457 | 1.991 |
| w23 | 7 | -0.058543 | -7.076 |
| w24 | 29 | 0.031021 | 120.956 |
| w25 | 11 | 0.096535 | 12.977 |
| w26 | 6 | -0.101373 | -12.04 |
| w27 | 20 | 0.091874 | 66.279 |
| w28 | 3 | -0.025167 | 1.528 |
| w29 | 20 | -0.111043 | -12.719 |
| w30 | 4 | 0.011491 | -21.664 |
| w31 | 17 | 0.039936 | -6.481 |
| w32 | 13 | -0.09607 | -12.657 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 23 | -0.094243 | 3.51 |
| w23 | 5 | -0.040196 | -23.379 |
| w24 | 17 | 0.138894 | 125.422 |
| w25 | 18 | 0.186931 | 52.368 |
| w26 | 5 | 5.5e-05 | 11.116 |
| w27 | 18 | 0.070252 | 18.066 |
| w28 | 4 | 0.060634 | -6.046 |
| w29 | 10 | -0.091236 | -19.221 |
| w30 | 8 | -0.132625 | -34.102 |
| w31 | 10 | 0.129905 | 30.753 |
| w32 | 9 | 0.063218 | 35.213 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 19 | 0.005799 | 24.054 |
| w25 | 10 | 0.015488 | 32.439 |
| w26 | 8 | -0.046959 | -15.316 |
| w27 | 21 | 0.046105 | 37.003 |
| w28 | 9 | -0.015133 | 8.32 |
| w29 | 12 | 0.049579 | 11.015 |
| w30 | 10 | -0.079876 | -8.412 |
| w31 | 12 | -0.061919 | -15.235 |
| w32 | 9 | -0.127946 | -26.148 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 18 | -0.002627 | 82.403 |
| w6 | 17 | -0.145664 | -9.571 |
| w7 | 8 | -0.083648 | -9.778 |
| w8 | 14 | -0.035099 | -14.13 |
| w9 | 14 | -0.069063 | -21.035 |
| w10 | 19 | 0.133451 | 24.916 |
| w11 | 12 | 0.071384 | -0.505 |
| w12 | 15 | -0.053254 | -24.287 |
| w13 | 10 | 0.065841 | 33.798 |
| w14 | 16 | 0.040161 | 48.647 |
| w15 | 19 | 0.067927 | -0.024 |
| w16 | 21 | -0.12915 | 7.653 |
| w17 | 16 | -0.271299 | -21.436 |
| w18 | 14 | -0.044945 | -11.615 |
| w19 | 11 | 0.131169 | 15.466 |
| w20 | 6 | -0.011492 | 5.233 |
| w21 | 7 | -0.057454 | -29.717 |
| w22 | 11 | -0.176404 | -29.419 |
| w23 | 5 | 0.018992 | -35.394 |
| w24 | 30 | -0.062976 | 0.947 |
| w25 | 9 | 0.164169 | 21.131 |
| w26 | 16 | 0.166408 | 27.058 |
| w27 | 13 | 0.025579 | 62.406 |
| w28 | 12 | 0.039494 | -5.802 |
| w29 | 13 | -0.02745 | -3.629 |
| w30 | 16 | 0.195098 | 209.539 |
| w31 | 15 | -0.099116 | -6.457 |
| w32 | 7 | 0.015939 | 6.766 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 22 | 0.060003 | 51.618 |
| w6 | 17 | 0.037324 | 22.1 |
| w7 | 9 | -0.192656 | -22.975 |
| w8 | 8 | 0.027387 | 2.933 |
| w9 | 5 | 0.073415 | -0.053 |
| w10 | 13 | 0.043422 | 24.518 |
| w11 | 14 | -0.046737 | -1.466 |
| w12 | 5 | 0.079291 | -1.603 |
| w13 | 14 | -0.007186 | 16.613 |
| w14 | 24 | -0.047221 | 26.274 |
| w15 | 29 | 0.02898 | 30.183 |
| w16 | 15 | -0.155989 | -6.39 |
| w17 | 17 | -0.023004 | -3.073 |
| w18 | 13 | -0.066988 | -15.154 |
| w19 | 15 | 0.048402 | 7.737 |
| w20 | 11 | 0.056657 | 2.641 |
| w21 | 10 | 0.029833 | -18.525 |
| w22 | 11 | 0.012593 | -6.012 |
| w23 | 8 | 0.017276 | -2.801 |
| w24 | 27 | -0.094224 | -10.731 |
| w25 | 7 | -0.056807 | 8.103 |
| w26 | 17 | 0.073984 | 19.635 |
| w27 | 10 | -0.004135 | 43.913 |
| w28 | 10 | 0.109131 | 34.637 |
| w29 | 14 | 0.123441 | -1.844 |
| w30 | 20 | -0.189445 | 3.862 |
| w31 | 18 | -0.161626 | -15.003 |
| w32 | 10 | 0.025949 | 5.091 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 10 | -0.064568 | -6.216 |
| w18 | 24 | -0.145331 | -11.504 |
| w19 | 10 | -0.114982 | -22.536 |
| w20 | 9 | -0.075626 | -22.91 |
| w21 | 9 | -0.031864 | -30.995 |
| w22 | 24 | 0.073793 | 16.554 |
| w23 | 5 | -0.009345 | 1.299 |
| w24 | 23 | -0.097448 | 10.904 |
| w25 | 13 | 0.186085 | 35.371 |
| w26 | 13 | -0.027104 | -6.132 |
| w27 | 12 | 0.2508 | 148.964 |
| w28 | 7 | -0.005731 | 16.299 |
| w29 | 8 | -0.016639 | -7.705 |
| w30 | 7 | -0.131398 | -8.515 |
| w31 | 8 | 0.070862 | -0.121 |
| w32 | 17 | -0.093471 | -15.041 |

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
| w17 | 9 | -0.138177 | -11.692 |
| w18 | 11 | 0.02578 | -27.287 |
| w19 | 7 | 0.014212 | -3.19 |
| w20 | 9 | -0.024736 | 11.262 |
| w21 | 6 | -0.007407 | -18.481 |
| w22 | 17 | 0.128741 | 28.808 |
| w23 | 5 | 0.076156 | 7.211 |
| w24 | 21 | 0.00786 | 34.238 |
| w25 | 10 | 0.182925 | 27.446 |
| w26 | 19 | -0.146598 | 14.718 |
| w27 | 19 | -0.132056 | 15.488 |
| w28 | 7 | -0.093267 | -13.865 |
| w29 | 26 | -0.049425 | -3.524 |
| w30 | 2 | 0.013748 | -0.594 |
| w31 | 6 | -0.077769 | -19.112 |
| w32 | 14 | -0.002922 | 10.832 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 12 | -0.041827 | -2.317 |
| w20 | 9 | -0.015543 | -8.322 |
| w21 | 13 | -0.166857 | -12.806 |
| w22 | 22 | 0.011767 | 121.501 |
| w23 | 12 | -0.189202 | -8.057 |
| w24 | 25 | 0.136042 | 190.934 |
| w25 | 9 | -0.009334 | 5.942 |
| w26 | 11 | -0.139418 | -23.935 |
| w27 | 13 | 0.07929 | 14.7 |
| w28 | 6 | -0.062025 | -2.771 |
| w29 | 15 | -0.170183 | -14.482 |
| w30 | 1 | -0.01328 | -2.431 |
| w31 | 17 | -0.016343 | -7.522 |
| w32 | 14 | 0.032146 | 36.224 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 11 | 0.180263 | 47.306 |
| w23 | 12 | -0.045617 | -5.352 |
| w24 | 20 | -0.036418 | 22.406 |
| w25 | 13 | 0.047246 | -14.778 |
| w26 | 10 | -0.048834 | -12.052 |
| w27 | 18 | -0.12257 | 10.949 |
| w28 | 11 | -0.026338 | -14.256 |
| w29 | 14 | -0.114012 | -6.258 |
| w30 | 5 | -0.110031 | -5.513 |
| w31 | 13 | 0.065813 | 13.22 |
| w32 | 16 | 0.129458 | 5.838 |

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
| w27 | 19 | -0.004498 | 2.498 |
| w28 | 4 | -0.018232 | -2.126 |
| w29 | 14 | -0.074761 | -10.791 |
| w30 | 6 | -0.073846 | -1.671 |
| w31 | 7 | -0.096469 | -12.754 |
| w32 | 21 | 0.097109 | 31.566 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 12 | 0.12122 | 17.365 |
| w18 | 5 | -0.03538 | -12.071 |
| w19 | 6 | -0.047869 | -18.858 |
| w20 | 7 | 0.190514 | 36.972 |
| w21 | 11 | 0.036461 | -15.2 |
| w22 | 20 | -0.077819 | 2.311 |
| w23 | 11 | -0.048169 | -4.304 |
| w24 | 20 | -0.034327 | 50.254 |
| w25 | 12 | 0.148123 | 19.962 |
| w26 | 8 | -0.001544 | -12.252 |
| w27 | 11 | 0.207356 | 90.2 |
| w28 | 0 | 0.075327 | 0.0 |
| w29 | 13 | -0.106842 | -23.637 |
| w30 | 2 | 0.058526 | -2.517 |
| w31 | 11 | -0.020389 | -9.83 |
| w32 | 10 | -0.110763 | -1.465 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 14 | 0.029644 | 5.048 |
| w18 | 7 | 0.087287 | -6.099 |
| w19 | 10 | 0.11863 | 6.334 |
| w20 | 11 | 0.034659 | 2.935 |
| w21 | 10 | -0.182838 | -35.488 |
| w22 | 19 | -0.003217 | 37.284 |
| w23 | 12 | -0.048426 | -17.197 |
| w24 | 16 | 0.067914 | 59.632 |
| w25 | 11 | 0.154494 | 34.9 |
| w26 | 10 | 0.024463 | -19.141 |
| w27 | 20 | 0.140486 | 60.139 |
| w28 | 4 | 0.114109 | 6.075 |
| w29 | 17 | 0.039195 | 0.488 |
| w30 | 9 | -0.080139 | -34.636 |
| w31 | 10 | -0.033057 | -8.859 |
| w32 | 11 | -0.08272 | -30.37 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 5 | 0.108964 | 10.597 |
| w29 | 9 | -0.093823 | -17.223 |
| w30 | 8 | 0.025225 | 12.952 |
| w31 | 14 | 0.036672 | 5.03 |
| w32 | 12 | -0.008601 | 2.857 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 12 | -0.029288 | -0.22 |
| w15 | 15 | -0.048563 | 9.499 |
| w16 | 20 | 0.042324 | 183.138 |
| w17 | 16 | 0.000508 | 0.591 |
| w18 | 9 | -0.017715 | -12.857 |
| w19 | 13 | -0.064716 | -18.348 |
| w20 | 9 | -0.120203 | -18.726 |
| w21 | 8 | 0.057015 | 12.218 |
| w22 | 17 | -0.039645 | 5.788 |
| w23 | 9 | 0.106907 | 8.695 |
| w24 | 15 | 0.011443 | 49.885 |
| w25 | 15 | 0.193946 | 93.722 |
| w26 | 7 | 0.017159 | -4.025 |
| w27 | 19 | 0.208618 | 195.14 |
| w28 | 3 | -0.109815 | -19.421 |
| w29 | 11 | -0.003059 | 9.801 |
| w30 | 6 | -0.112497 | -3.658 |
| w31 | 17 | -0.039189 | -9.953 |
| w32 | 18 | -0.076641 | -19.488 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 17 | 0.359073 | 286.388 |
| w26 | 17 | 0.037327 | -3.105 |
| w27 | 15 | 0.020662 | 27.418 |
| w28 | 6 | 0.016125 | 1.183 |
| w29 | 15 | -0.009886 | -2.808 |
| w30 | 6 | -0.132967 | -9.713 |
| w31 | 14 | -0.021033 | -4.834 |
| w32 | 16 | -0.098417 | -9.465 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

