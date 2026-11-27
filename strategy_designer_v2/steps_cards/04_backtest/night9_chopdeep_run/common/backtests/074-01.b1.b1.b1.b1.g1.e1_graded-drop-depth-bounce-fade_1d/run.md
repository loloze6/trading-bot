# Backtest of 074-01.b1.b1.b1.b1.g1.e1_graded-drop-depth-bounce-fade_1d

- Plan: `../../../../../03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1.b1.g1.e1_graded-drop-depth-bounce-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.014971 | -0.642 |
| w2 | 1 | 0.009835 | 0.069 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 4 | 0.001238 | 0.031 |
| w8 | 4 | 0.071109 | 3.923 |
| w9 | 9 | 0.292056 | 48.774 |
| w10 | 1 | -0.04599 | -0.18 |
| w11 | 0 | None | 0.0 |
| w12 | 5 | -0.113291 | -6.334 |
| w13 | 4 | 0.166431 | 8.553 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 8 | 0.148829 | 13.392 |
| w18 | 0 | None | 0.0 |
| w19 | 4 | 0.009391 | 0.791 |
| w20 | 7 | 0.098745 | 13.138 |
| w21 | 10 | 0.056771 | 3.975 |
| w22 | 0 | None | 0.0 |
| w23 | 3 | -0.103447 | -3.204 |
| w24 | 3 | -0.098747 | -4.455 |
| w25 | 0 | None | 0.0 |
| w26 | 4 | 0.022298 | 0.296 |
| w27 | 0 | None | 0.0 |
| w28 | 5 | 0.133883 | 9.807 |
| w29 | 0 | None | 0.0 |
| w30 | 4 | 0.006788 | 0.775 |
| w31 | 8 | 0.08891 | 10.126 |
| w32 | 4 | -0.005854 | -1.001 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.01167 | 0.127 |
| w2 | 1 | -0.030208 | -1.286 |
| w3 | 0 | None | 0.0 |
| w4 | 1 | -0.009084 | -3.386 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.022028 | -0.706 |
| w7 | 7 | 0.053556 | 4.351 |
| w8 | 7 | 0.111203 | 11.323 |
| w9 | 8 | 0.125136 | 16.175 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | -0.017817 | -0.932 |
| w12 | 10 | 0.052659 | 5.175 |
| w13 | 4 | 0.105788 | 3.581 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | -0.027826 | -2.226 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | -0.038607 | -2.109 |
| w18 | 0 | None | 0.0 |
| w19 | 4 | 0.121014 | 4.784 |
| w20 | 5 | 0.160906 | 18.912 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | 0.034792 | 0.0 |
| w24 | 2 | -0.132242 | -6.363 |
| w25 | 0 | None | 0.0 |
| w26 | 9 | 0.03526 | 3.901 |
| w27 | 0 | None | 0.0 |
| w28 | 3 | 0.050946 | 3.14 |
| w29 | 2 | -0.013839 | -1.063 |
| w30 | 6 | 0.001214 | 0.127 |
| w31 | 8 | 0.013596 | 2.348 |
| w32 | 2 | -0.035445 | -2.497 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 1 | -0.020487 | -2.003 |
| w7 | 3 | -0.037129 | -2.262 |
| w8 | 8 | -0.014912 | 1.953 |
| w9 | 5 | 0.096898 | 6.333 |
| w10 | 2 | 0.104671 | 3.279 |
| w11 | 4 | -0.023223 | -2.469 |
| w12 | 4 | 0.058376 | 5.034 |
| w13 | 4 | 0.159931 | 6.134 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | 0.001957 | -0.256 |
| w16 | 2 | -0.360121 | -5.592 |
| w17 | 4 | 0.074621 | 3.262 |
| w18 | 3 | 0.02155 | 1.771 |
| w19 | 2 | 0.057955 | 2.704 |
| w20 | 4 | 0.050081 | 17.726 |
| w21 | 3 | 0.000863 | -0.36 |
| w22 | 1 | 0.038604 | 0.899 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | 0.031967 | 0.424 |
| w25 | 4 | -0.019418 | -3.162 |
| w26 | 4 | 0.109614 | 11.214 |
| w27 | 0 | None | 0.0 |
| w28 | 3 | 0.108212 | 5.104 |
| w29 | 0 | None | 0.0 |
| w30 | 8 | -0.076577 | -6.059 |
| w31 | 8 | 0.089439 | 7.111 |
| w32 | 3 | -0.052809 | -3.436 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 4 | 0.103056 | 6.578 |
| w8 | 3 | 0.04892 | 2.875 |
| w9 | 9 | -0.006092 | -0.227 |
| w10 | 4 | 0.047853 | 0.772 |
| w11 | 5 | 0.049411 | 2.107 |
| w12 | 3 | 0.042843 | 2.692 |
| w13 | 4 | 0.102162 | 3.829 |
| w14 | 1 | -0.033288 | -1.949 |
| w15 | 1 | 0.002202 | -0.319 |
| w16 | 0 | None | 0.0 |
| w17 | 1 | -0.025894 | -1.591 |
| w18 | 2 | -0.042259 | -2.641 |
| w19 | 4 | -0.027087 | -1.954 |
| w20 | 6 | 0.148251 | 18.419 |
| w21 | 5 | -0.054903 | -3.896 |
| w22 | 1 | -0.009961 | -0.611 |
| w23 | 2 | 0.071958 | 5.143 |
| w24 | 2 | -0.052823 | -2.005 |
| w25 | 0 | None | 0.0 |
| w26 | 5 | 0.173854 | 14.207 |
| w27 | 2 | -0.061177 | -2.092 |
| w28 | 9 | 0.049015 | 2.437 |
| w29 | 0 | None | 0.0 |
| w30 | 6 | 0.137071 | 8.186 |
| w31 | 12 | -0.014896 | -4.963 |
| w32 | 5 | 0.118906 | 11.18 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 1 | -0.097892 | -3.678 |
| w3 | 7 | -0.065474 | -1.893 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | 0.024913 | 0.054 |
| w6 | 0 | None | 0.0 |
| w7 | 4 | 0.119436 | 9.357 |
| w8 | 3 | 0.037817 | 3.059 |
| w9 | 12 | 0.151322 | 26.078 |
| w10 | 2 | 0.11782 | 2.084 |
| w11 | 2 | -0.032113 | -2.38 |
| w12 | 6 | 0.036101 | 3.377 |
| w13 | 2 | 0.042953 | 0.317 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | -0.07806 | -0.391 |
| w16 | 0 | None | 0.0 |
| w17 | 1 | -0.011453 | -0.432 |
| w18 | 0 | None | 0.0 |
| w19 | 5 | -0.04149 | -2.395 |
| w20 | 8 | 0.015846 | 1.922 |
| w21 | 6 | 0.062117 | 4.286 |
| w22 | 0 | None | 0.0 |
| w23 | 3 | 0.023727 | 1.198 |
| w24 | 1 | -0.024262 | -1.987 |
| w25 | 0 | None | 0.0 |
| w26 | 3 | 0.103568 | 5.63 |
| w27 | 4 | 0.026468 | 0.078 |
| w28 | 7 | 0.336145 | 33.511 |
| w29 | 0 | None | 0.0 |
| w30 | 8 | -0.04437 | -2.356 |
| w31 | 8 | -0.015203 | 0.61 |
| w32 | 2 | 0.04441 | 2.323 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 0 | None | 0.0 |
| w11 | 5 | -0.092732 | -8.272 |
| w12 | 6 | 0.041371 | 2.777 |
| w13 | 5 | 0.196666 | 8.361 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | -0.107538 | -10.794 |
| w16 | 0 | None | 0.0 |
| w17 | 1 | -0.004611 | -0.89 |
| w18 | 8 | 0.041725 | 7.586 |
| w19 | 5 | 0.098197 | 6.54 |
| w20 | 9 | 0.07137 | 10.998 |
| w21 | 6 | 0.017165 | 1.397 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.047101 | 4.109 |
| w24 | 1 | -0.015263 | -3.011 |
| w25 | 1 | -0.109786 | -1.26 |
| w26 | 11 | 0.121223 | 12.462 |
| w27 | 2 | -0.006522 | -2.317 |
| w28 | 6 | 0.092598 | 9.19 |
| w29 | 5 | -0.030434 | -2.752 |
| w30 | 6 | -0.05589 | -2.903 |
| w31 | 10 | 0.004397 | 0.017 |
| w32 | 7 | -0.06383 | -7.354 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 2 | -0.113068 | -7.928 |
| w13 | 4 | 0.02802 | 1.969 |
| w14 | 1 | 0.017994 | -0.14 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | 0.100736 | 5.587 |
| w18 | 4 | -0.088448 | -4.263 |
| w19 | 4 | 0.096467 | 6.123 |
| w20 | 8 | 0.1818 | 23.093 |
| w21 | 3 | 0.08065 | 4.197 |
| w22 | 0 | None | 0.0 |
| w23 | 8 | -0.025961 | -3.435 |
| w24 | 4 | -0.02145 | -3.288 |
| w25 | 2 | 0.004989 | -0.125 |
| w26 | 4 | 0.015032 | 1.757 |
| w27 | 2 | -0.049192 | -2.272 |
| w28 | 7 | -0.003358 | -1.23 |
| w29 | 2 | -0.025612 | -1.292 |
| w30 | 10 | -0.115864 | -11.305 |
| w31 | 7 | -0.047664 | -4.554 |
| w32 | 5 | -0.130237 | -8.158 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 4 | -0.154299 | -8.353 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | -0.084088 | -5.313 |
| w18 | 0 | -0.10143 | 0.0 |
| w19 | 3 | -0.015913 | 0.764 |
| w20 | 10 | 0.041688 | -1.446 |
| w21 | 4 | 0.050732 | 2.36 |
| w22 | 0 | None | 0.0 |
| w23 | 8 | 0.078009 | 4.645 |
| w24 | 2 | -0.018932 | -3.137 |
| w25 | 2 | -0.074634 | -2.995 |
| w26 | 6 | 0.12453 | 9.593 |
| w27 | 2 | 0.025143 | -0.191 |
| w28 | 9 | 0.008825 | -0.208 |
| w29 | 2 | -0.07457 | -2.164 |
| w30 | 9 | -0.078583 | -6.358 |
| w31 | 11 | -0.054409 | -8.192 |
| w32 | 4 | 0.037622 | -0.014 |

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
| w15 | 2 | 0.045259 | 3.356 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | -0.082347 | -4.961 |
| w18 | 0 | None | 0.0 |
| w19 | 4 | 0.100564 | 5.509 |
| w20 | 1 | -0.028041 | -0.952 |
| w21 | 6 | 0.113099 | 6.923 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 1 | 0.042565 | 1.441 |
| w26 | 1 | -0.07441 | -0.909 |
| w27 | 0 | None | 0.0 |
| w28 | 1 | 0.064652 | 1.11 |
| w29 | 0 | None | 0.0 |
| w30 | 5 | -0.061891 | -4.515 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.06748 | 3.288 |
| w18 | 2 | -0.046162 | -0.552 |
| w19 | 6 | -0.147583 | -7.687 |
| w20 | 6 | 0.014306 | 4.277 |
| w21 | 5 | 0.017214 | -1.078 |
| w22 | 1 | -0.011903 | -0.293 |
| w23 | 3 | 0.041805 | 2.297 |
| w24 | 6 | -0.003535 | -7.685 |
| w25 | 3 | 0.014962 | -0.099 |
| w26 | 7 | -0.104488 | -7.854 |
| w27 | 3 | -0.007958 | -1.698 |
| w28 | 8 | 0.123734 | 10.328 |
| w29 | 2 | -0.039506 | -2.542 |
| w30 | 6 | -0.064726 | -4.801 |
| w31 | 6 | 0.044755 | 3.239 |
| w32 | 7 | 0.155176 | 9.289 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 9 | 0.214601 | 35.052 |
| w21 | 6 | 0.146341 | 11.3 |
| w22 | 1 | -0.028052 | -1.256 |
| w23 | 4 | 0.076415 | 1.6 |
| w24 | 3 | 0.025214 | -1.623 |
| w25 | 1 | 0.101331 | 4.003 |
| w26 | 8 | 0.088807 | 7.187 |
| w27 | 2 | 0.003423 | 0.37 |
| w28 | 8 | 0.004545 | 0.684 |
| w29 | 1 | -0.025586 | -0.699 |
| w30 | 6 | -0.030371 | -1.67 |
| w31 | 7 | -0.005722 | 0.143 |
| w32 | 3 | 0.011341 | 0.13 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 1 | 0.071867 | 3.098 |
| w23 | 8 | -0.010156 | -0.267 |
| w24 | 4 | -0.010508 | -3.635 |
| w25 | 2 | -0.037813 | -1.611 |
| w26 | 6 | -0.001487 | -0.452 |
| w27 | 2 | 0.059138 | 1.113 |
| w28 | 9 | 0.101494 | 10.324 |
| w29 | 1 | -0.058697 | -1.787 |
| w30 | 7 | -0.251616 | -22.321 |
| w31 | 6 | 0.056079 | 3.643 |
| w32 | 3 | -0.030806 | -4.12 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 2 | -0.088378 | -5.078 |
| w25 | 0 | None | 0.0 |
| w26 | 7 | -0.14393 | -15.963 |
| w27 | 0 | None | 0.0 |
| w28 | 8 | 0.097753 | 8.931 |
| w29 | 2 | -0.062629 | -3.009 |
| w30 | 9 | 0.011696 | 4.918 |
| w31 | 8 | 0.045162 | 4.047 |
| w32 | 2 | -0.086749 | -4.676 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 1 | -0.040325 | -0.732 |
| w6 | 2 | -0.087557 | -2.266 |
| w7 | 2 | 0.006009 | 0.383 |
| w8 | 5 | 0.056758 | 3.339 |
| w9 | 3 | 0.048351 | 3.885 |
| w10 | 3 | -0.006375 | -0.764 |
| w11 | 3 | 0.161449 | 10.023 |
| w12 | 11 | 0.091732 | 9.472 |
| w13 | 5 | 0.081096 | 1.268 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.059033 | -3.33 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | -0.054722 | -2.859 |
| w18 | 1 | 0.000426 | -0.081 |
| w19 | 6 | -0.075391 | -5.311 |
| w20 | 10 | 0.131311 | 11.799 |
| w21 | 6 | -0.059729 | -4.318 |
| w22 | 5 | -0.039396 | -2.877 |
| w23 | 5 | -0.092462 | -8.726 |
| w24 | 1 | -0.071445 | -2.093 |
| w25 | 4 | -0.134822 | -9.873 |
| w26 | 4 | -0.047606 | -5.316 |
| w27 | 0 | None | 0.0 |
| w28 | 4 | -0.032964 | -2.874 |
| w29 | 1 | -0.111698 | -2.726 |
| w30 | 0 | None | 0.0 |
| w31 | 7 | -0.056925 | -2.857 |
| w32 | 1 | 0.027942 | 0.136 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 0 | None | 0.0 |
| w6 | 3 | 0.047569 | 1.053 |
| w7 | 6 | 0.091719 | 6.127 |
| w8 | 8 | 0.006964 | -0.459 |
| w9 | 8 | 0.11967 | 12.657 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | -0.008184 | -0.816 |
| w12 | 10 | -0.171038 | -13.202 |
| w13 | 1 | 0.065475 | 2.065 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 1 | -0.007367 | -0.497 |
| w18 | 2 | 0.016552 | 0.603 |
| w19 | 2 | 0.009701 | 0.267 |
| w20 | 6 | 0.007651 | -0.982 |
| w21 | 2 | 0.109688 | 4.05 |
| w22 | 2 | -0.204679 | -11.309 |
| w23 | 2 | 0.057081 | 1.198 |
| w24 | 3 | -0.136649 | -5.221 |
| w25 | 6 | -0.001663 | -1.385 |
| w26 | 1 | 0.046618 | 1.343 |
| w27 | 2 | -0.01988 | -2.988 |
| w28 | 0 | None | 0.0 |
| w29 | 5 | -0.162525 | -16.895 |
| w30 | 0 | None | 0.0 |
| w31 | 4 | 0.003112 | 0.267 |
| w32 | 0 | None | 0.0 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 5 | 0.127168 | 5.449 |
| w18 | 0 | None | 0.0 |
| w19 | 1 | -0.07467 | -0.956 |
| w20 | 5 | -0.031206 | -3.516 |
| w21 | 10 | -0.055394 | -8.0 |
| w22 | 2 | 0.048032 | 1.501 |
| w23 | 8 | 0.009841 | 1.336 |
| w24 | 3 | 0.006341 | -1.437 |
| w25 | 3 | 0.104211 | 4.317 |
| w26 | 11 | 0.008401 | -1.494 |
| w27 | 3 | -0.040419 | -6.053 |
| w28 | 7 | 0.019186 | 0.05 |
| w29 | 2 | -0.028327 | -1.365 |
| w30 | 9 | -0.03215 | -0.76 |
| w31 | 9 | -0.041464 | -3.031 |
| w32 | 4 | -0.071688 | -6.782 |

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
| w17 | 4 | 0.114589 | 4.43 |
| w18 | 5 | 0.229122 | 20.798 |
| w19 | 3 | 0.030393 | 1.569 |
| w20 | 4 | 0.140019 | 7.03 |
| w21 | 4 | 0.043545 | 2.025 |
| w22 | 2 | 0.021186 | 0.171 |
| w23 | 3 | 0.014913 | 1.313 |
| w24 | 2 | -0.077753 | -6.271 |
| w25 | 1 | -0.013694 | -0.688 |
| w26 | 3 | -0.01723 | -3.38 |
| w27 | 0 | None | 0.0 |
| w28 | 6 | 0.223453 | 18.587 |
| w29 | 1 | -0.006165 | -0.082 |
| w30 | 10 | -0.023244 | -0.916 |
| w31 | 12 | 0.059657 | 6.772 |
| w32 | 3 | 0.087945 | 3.657 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 6 | 0.005414 | -0.182 |
| w20 | 5 | 0.24896 | 29.463 |
| w21 | 1 | 0.018818 | 0.594 |
| w22 | 0 | None | 0.0 |
| w23 | 1 | 0.021459 | 0.917 |
| w24 | 2 | -0.001003 | -2.487 |
| w25 | 3 | -0.006847 | -0.737 |
| w26 | 7 | -0.047099 | -4.448 |
| w27 | 2 | 0.021184 | 0.084 |
| w28 | 8 | 0.140919 | 11.04 |
| w29 | 1 | -0.013195 | -0.259 |
| w30 | 7 | 0.053388 | 7.853 |
| w31 | 10 | -0.027645 | -3.166 |
| w32 | 1 | 0.06469 | 2.4 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 1 | -0.149419 | -4.156 |
| w23 | 10 | 0.087263 | 5.374 |
| w24 | 4 | -0.02584 | -4.673 |
| w25 | 1 | 0.054718 | 2.217 |
| w26 | 3 | 0.087372 | 3.633 |
| w27 | 3 | 0.10446 | 2.165 |
| w28 | 6 | 0.190286 | 14.376 |
| w29 | 2 | -0.061469 | -2.732 |
| w30 | 6 | -0.036223 | -2.265 |
| w31 | 7 | 0.046829 | 4.342 |
| w32 | 3 | 0.011931 | -1.106 |

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
| w27 | 4 | 0.036636 | 0.062 |
| w28 | 5 | 0.079249 | 6.225 |
| w29 | 1 | -0.079237 | -2.483 |
| w30 | 7 | -0.04762 | -1.896 |
| w31 | 11 | -0.031235 | -2.126 |
| w32 | 0 | None | 0.0 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 3 | -0.107041 | -5.913 |
| w18 | 3 | 0.125538 | 8.18 |
| w19 | 2 | -0.022177 | -0.815 |
| w20 | 6 | 0.207226 | 22.427 |
| w21 | 4 | 0.074129 | 5.768 |
| w22 | 0 | None | 0.0 |
| w23 | 5 | 0.009092 | 0.646 |
| w24 | 4 | -0.03121 | -8.305 |
| w25 | 0 | None | 0.0 |
| w26 | 7 | 0.118609 | 10.636 |
| w27 | 2 | -0.003212 | -0.989 |
| w28 | 8 | 0.062952 | 4.721 |
| w29 | 2 | -0.074104 | -3.759 |
| w30 | 5 | -0.302741 | -22.549 |
| w31 | 5 | -0.035716 | -2.505 |
| w32 | 7 | -0.156608 | -18.625 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 4 | 0.037889 | 2.919 |
| w18 | 1 | 0.032976 | 0.211 |
| w19 | 5 | -0.018986 | -0.937 |
| w20 | 5 | 0.253544 | 24.97 |
| w21 | 5 | 0.053813 | 3.254 |
| w22 | 1 | 0.000973 | -0.325 |
| w23 | 5 | 0.023806 | 0.851 |
| w24 | 3 | -0.03608 | -10.098 |
| w25 | 0 | None | 0.0 |
| w26 | 7 | 0.032366 | 1.955 |
| w27 | 2 | 0.028142 | 0.253 |
| w28 | 9 | 0.120742 | 10.806 |
| w29 | 3 | -0.054255 | -2.455 |
| w30 | 9 | -0.008749 | -0.144 |
| w31 | 11 | -0.003509 | 0.615 |
| w32 | 8 | -0.03964 | -5.693 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 9 | 0.037109 | 2.596 |
| w29 | 1 | -0.148476 | -2.389 |
| w30 | 4 | -0.104175 | -4.813 |
| w31 | 5 | 0.060641 | 4.453 |
| w32 | 5 | -0.037088 | -6.312 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 0 | None | 0.0 |
| w15 | 5 | 0.091168 | 6.715 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | -0.150005 | -11.069 |
| w18 | 3 | 0.056948 | 3.51 |
| w19 | 6 | -0.069485 | -4.568 |
| w20 | 6 | -0.039235 | -1.065 |
| w21 | 2 | 0.013565 | 0.42 |
| w22 | 4 | -0.115239 | -7.411 |
| w23 | 5 | 0.250874 | 19.381 |
| w24 | 1 | 0.038399 | 1.614 |
| w25 | 0 | None | 0.0 |
| w26 | 9 | -0.00383 | 0.431 |
| w27 | 1 | 0.012317 | -0.147 |
| w28 | 7 | 0.116851 | 11.733 |
| w29 | 2 | -0.022881 | -1.098 |
| w30 | 7 | 0.002766 | 1.623 |
| w31 | 8 | 0.009076 | -0.433 |
| w32 | 5 | -0.167954 | -13.246 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 3 | 0.019292 | -1.148 |
| w26 | 3 | 0.080955 | 4.147 |
| w27 | 2 | -0.050108 | -1.479 |
| w28 | 9 | 0.046928 | 3.954 |
| w29 | 0 | None | 0.0 |
| w30 | 8 | -0.140996 | -13.119 |
| w31 | 4 | 0.041544 | 1.91 |
| w32 | 5 | -0.042738 | -4.635 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

