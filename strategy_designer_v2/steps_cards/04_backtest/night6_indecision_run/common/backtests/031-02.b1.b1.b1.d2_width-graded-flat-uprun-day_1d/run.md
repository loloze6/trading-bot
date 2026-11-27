# Backtest of 031-02.b1.b1.b1.d2_width-graded-flat-uprun-day_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.d2_width-graded-flat-uprun-day_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 2 | 0.022242 | 18.201 |
| w3 | 6 | 0.038913 | 15.134 |
| w4 | 3 | -0.122034 | -0.694 |
| w5 | 1 | 0.037582 | 6.983 |
| w6 | 3 | 0.036097 | 12.684 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 6 | 0.056521 | 39.364 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.00321 | -1.009 |
| w13 | 3 | -0.022226 | 4.172 |
| w14 | 1 | 0.062498 | -0.762 |
| w15 | 6 | -0.060049 | 16.574 |
| w16 | 2 | 0.041584 | -9.733 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 3 | 0.041045 | -0.462 |
| w20 | 4 | 0.064905 | -2.903 |
| w21 | 2 | -0.07464 | -7.192 |
| w22 | 7 | -0.004284 | 15.962 |
| w23 | 0 | 0.019975 | 0.0 |
| w24 | 1 | 0.0417 | 11.081 |
| w25 | 5 | -0.072394 | 0.572 |
| w26 | 0 | 0.015628 | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | -0.099529 | 0.0 |
| w30 | 3 | 0.038171 | 5.332 |
| w31 | 2 | -0.081535 | -6.768 |
| w32 | 0 | None | 0.0 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.064498 | 26.425 |
| w2 | 6 | -0.012246 | 9.248 |
| w3 | 2 | 0.027783 | -12.294 |
| w4 | 1 | -0.085953 | -1.388 |
| w5 | 4 | 0.110308 | 13.209 |
| w6 | 3 | -0.164005 | 1.915 |
| w7 | 1 | -0.019202 | -1.987 |
| w8 | 0 | None | 0.0 |
| w9 | 1 | -0.110723 | -11.009 |
| w10 | 3 | 0.028543 | 3.632 |
| w11 | 2 | -0.083854 | -3.039 |
| w12 | 2 | 0.136172 | 4.883 |
| w13 | 8 | 0.015541 | 3.199 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.131785 | -20.355 |
| w16 | 9 | 0.078122 | 29.445 |
| w17 | 3 | 0.009735 | 16.764 |
| w18 | 6 | 0.124746 | -15.648 |
| w19 | 1 | -0.118538 | -4.681 |
| w20 | 3 | 0.179682 | 5.355 |
| w21 | 0 | None | 0.0 |
| w22 | 4 | -0.009097 | -0.194 |
| w23 | 1 | -0.039709 | -1.998 |
| w24 | 7 | -0.094313 | -1.842 |
| w25 | 1 | 0.150209 | 42.471 |
| w26 | 1 | -0.012447 | -1.759 |
| w27 | 2 | -0.006307 | -0.651 |
| w28 | 4 | 0.032041 | 0.637 |
| w29 | 5 | 0.127263 | 26.068 |
| w30 | 2 | 0.005353 | -2.341 |
| w31 | 4 | -0.069321 | -3.714 |
| w32 | 2 | -0.045117 | -6.228 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 6 | -0.014884 | 8.132 |
| w7 | 6 | 0.014928 | -3.439 |
| w8 | 0 | None | 0.0 |
| w9 | 4 | 0.012846 | -3.047 |
| w10 | 2 | 0.070633 | -0.692 |
| w11 | 1 | -0.24341 | -3.761 |
| w12 | 0 | None | 0.0 |
| w13 | 4 | -0.008532 | 5.876 |
| w14 | 3 | 0.309775 | 62.242 |
| w15 | 3 | 0.073061 | 14.863 |
| w16 | 7 | -0.009582 | 14.127 |
| w17 | 2 | -0.072598 | -7.813 |
| w18 | 3 | 0.065247 | 7.418 |
| w19 | 0 | None | 0.0 |
| w20 | 1 | 0.130017 | 9.659 |
| w21 | 1 | -0.088983 | -7.533 |
| w22 | 2 | -0.049817 | 2.627 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | -0.046953 | 21.424 |
| w25 | 4 | -0.054659 | -3.833 |
| w26 | 4 | 0.039866 | 4.801 |
| w27 | 6 | 0.034477 | 9.508 |
| w28 | 0 | 0.088792 | 0.0 |
| w29 | 1 | 0.08488 | 9.288 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 3 | 0.024233 | -1.834 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 3 | -0.019589 | -0.932 |
| w8 | 2 | -0.084737 | -3.586 |
| w9 | 3 | 0.017899 | -3.737 |
| w10 | 0 | None | 0.0 |
| w11 | 6 | -0.090171 | -1.559 |
| w12 | 3 | -0.060566 | -7.102 |
| w13 | 4 | -0.032381 | 11.833 |
| w14 | 2 | 0.020501 | 2.138 |
| w15 | 6 | 0.022892 | 15.127 |
| w16 | 5 | -0.11391 | 14.645 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | -0.034274 | 0.0 |
| w19 | 4 | -0.055 | -19.674 |
| w20 | 4 | 0.129485 | 4.581 |
| w21 | 0 | None | 0.0 |
| w22 | 8 | 0.050326 | 14.856 |
| w23 | 0 | -0.004436 | 0.0 |
| w24 | 3 | 0.216951 | 3.659 |
| w25 | 2 | -0.092647 | 59.115 |
| w26 | 2 | -0.17708 | -20.569 |
| w27 | 5 | 0.020089 | 4.655 |
| w28 | 5 | 0.427829 | 10.997 |
| w29 | 4 | -0.044418 | 6.486 |
| w30 | 2 | -0.148159 | -4.907 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | -0.019777 | -2.017 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.052565 | 17.757 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 6 | 0.049206 | 41.372 |
| w5 | 5 | -0.120521 | -3.269 |
| w6 | 2 | -0.033698 | 2.334 |
| w7 | 4 | 0.062456 | 22.8 |
| w8 | 0 | 0.060934 | 0.0 |
| w9 | 2 | -0.196322 | 1.791 |
| w10 | 2 | 0.115786 | 5.544 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | 0.035225 | 5.622 |
| w13 | 7 | 0.028138 | 8.655 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.050001 | 0.648 |
| w16 | 4 | -0.134245 | -5.001 |
| w17 | 2 | 0.074844 | -4.802 |
| w18 | 2 | -0.056454 | 6.96 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | 0.008317 | 0.003 |
| w22 | 1 | 0.038976 | -4.03 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | 0.053439 | 1.552 |
| w25 | 3 | 0.156547 | 18.504 |
| w26 | 0 | 0.031017 | 0.0 |
| w27 | 0 | -0.031967 | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | 0.018242 | -0.366 |
| w30 | 1 | 0.064612 | 8.75 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 6 | 0.004501 | -1.944 |
| w11 | 1 | -0.200224 | -5.03 |
| w12 | 2 | 0.089299 | 5.558 |
| w13 | 8 | 0.007221 | -1.245 |
| w14 | 1 | -0.163329 | -3.113 |
| w15 | 0 | None | 0.0 |
| w16 | 7 | -0.123947 | -9.529 |
| w17 | 7 | -0.067278 | 15.394 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | 0.034973 | -8.334 |
| w21 | 0 | None | 0.0 |
| w22 | 5 | -0.092009 | 8.505 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | -0.007625 | -1.015 |
| w25 | 1 | 0.090046 | 18.806 |
| w26 | 1 | 0.06539 | 11.484 |
| w27 | 6 | 0.159753 | 14.542 |
| w28 | 0 | -0.014306 | 0.0 |
| w29 | 5 | 0.001328 | 43.831 |
| w30 | 2 | 0.103595 | 0.083 |
| w31 | 3 | -0.120518 | -10.916 |
| w32 | 3 | -0.05896 | -11.193 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 4 | 0.10021 | 24.633 |
| w13 | 0 | None | 0.0 |
| w14 | 8 | -0.011435 | 7.223 |
| w15 | 1 | -0.152775 | -7.091 |
| w16 | 6 | 0.031059 | 20.25 |
| w17 | 4 | 0.074619 | 4.553 |
| w18 | 1 | -0.055362 | 1.781 |
| w19 | 2 | 0.065337 | -1.27 |
| w20 | 0 | None | 0.0 |
| w21 | 1 | -0.178795 | -3.025 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | 0.051191 | 0.0 |
| w24 | 12 | 0.079653 | 25.124 |
| w25 | 2 | 0.061824 | 21.86 |
| w26 | 2 | -0.015359 | -5.286 |
| w27 | 2 | 0.058645 | 6.176 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | 0.030916 | -6.235 |
| w30 | 2 | 0.079377 | 0.062 |
| w31 | 0 | None | 0.0 |
| w32 | 8 | -0.009547 | -17.717 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 1 | -0.071865 | -4.256 |
| w16 | 6 | 0.187363 | 43.973 |
| w17 | 2 | -0.000313 | -7.743 |
| w18 | 5 | 0.165841 | 5.23 |
| w19 | 7 | 0.082629 | 6.119 |
| w20 | 2 | 0.032591 | -3.049 |
| w21 | 1 | 0.038846 | 2.879 |
| w22 | 4 | 0.04853 | 5.135 |
| w23 | 1 | 0.099234 | 2.924 |
| w24 | 5 | -0.052724 | 42.285 |
| w25 | 3 | 0.009548 | 21.592 |
| w26 | 3 | -0.069494 | -0.843 |
| w27 | 4 | 0.222463 | 36.989 |
| w28 | 0 | 0.084194 | 0.0 |
| w29 | 6 | 0.372313 | 23.355 |
| w30 | 0 | None | 0.0 |
| w31 | 1 | -0.048421 | -5.234 |
| w32 | 4 | 0.170976 | -5.782 |

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
| w15 | 3 | 0.146407 | -25.717 |
| w16 | 5 | 0.12088 | 17.246 |
| w17 | 3 | 0.026849 | 0.525 |
| w18 | 0 | -0.032922 | 0.0 |
| w19 | 1 | 0.122605 | 8.084 |
| w20 | 2 | 0.024469 | -0.248 |
| w21 | 2 | -0.035918 | 0.824 |
| w22 | 3 | -0.125742 | -3.907 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | 0.051462 | 2.486 |
| w25 | 0 | None | 0.0 |
| w26 | 3 | 0.206978 | -2.675 |
| w27 | 1 | 0.072673 | 25.511 |
| w28 | 0 | -0.088174 | 0.0 |
| w29 | 3 | 0.00779 | 8.584 |
| w30 | 3 | 0.053738 | 5.357 |
| w31 | 4 | -0.157339 | -3.913 |
| w32 | 3 | 0.008593 | -8.559 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 5 | -0.044362 | -5.041 |
| w17 | 2 | 0.068209 | 1.623 |
| w18 | 0 | None | 0.0 |
| w19 | 2 | -0.088728 | 0.644 |
| w20 | 2 | 0.085481 | -2.464 |
| w21 | 1 | -0.195549 | -8.816 |
| w22 | 4 | 0.045557 | 1.249 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | 0.084851 | 18.899 |
| w25 | 4 | 0.051081 | 18.134 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | 0.1147 | 0.0 |
| w29 | 5 | 0.104181 | -11.905 |
| w30 | 2 | 0.018489 | -4.466 |
| w31 | 2 | 0.078403 | -3.666 |
| w32 | 2 | -0.113422 | -9.846 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 2 | -0.01577 | 1.264 |
| w21 | 2 | 0.113899 | -3.792 |
| w22 | 7 | 0.037917 | -14.373 |
| w23 | 0 | None | 0.0 |
| w24 | 11 | 0.222671 | 117.409 |
| w25 | 2 | 0.085 | 3.688 |
| w26 | 2 | -0.106077 | -3.563 |
| w27 | 2 | 0.06134 | 5.531 |
| w28 | 0 | None | 0.0 |
| w29 | 5 | 0.106977 | 10.382 |
| w30 | 0 | None | 0.0 |
| w31 | 4 | -0.058638 | 1.103 |
| w32 | 2 | -0.094783 | -0.484 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 5 | 0.075982 | 16.947 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | -0.072572 | 40.628 |
| w25 | 5 | 0.227964 | 38.012 |
| w26 | 1 | -0.022097 | 2.038 |
| w27 | 3 | 0.026308 | 1.993 |
| w28 | 0 | None | 0.0 |
| w29 | 6 | -0.103971 | -6.82 |
| w30 | 2 | 0.055588 | 0.101 |
| w31 | 3 | -0.024391 | -4.312 |
| w32 | 2 | -0.016028 | 0.482 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 10 | 0.165392 | 33.959 |
| w25 | 0 | -0.084284 | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 8 | -0.076748 | 7.399 |
| w28 | 4 | 0.014092 | -0.205 |
| w29 | 0 | -0.146398 | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | -0.100766 | -10.03 |
| w32 | 0 | None | 0.0 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 8 | -0.055146 | -0.003 |
| w6 | 2 | 0.137671 | -8.879 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | -0.052003 | -6.694 |
| w9 | 0 | None | 0.0 |
| w10 | 6 | -0.108969 | 5.268 |
| w11 | 3 | -0.092025 | -5.087 |
| w12 | 2 | 0.095295 | -1.055 |
| w13 | 6 | 0.072379 | 7.956 |
| w14 | 5 | 0.014867 | 2.746 |
| w15 | 2 | -0.128158 | -19.884 |
| w16 | 6 | 0.135174 | 18.613 |
| w17 | 5 | 0.038452 | -0.638 |
| w18 | 3 | -0.032001 | -13.71 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | 0.02333 | -9.641 |
| w22 | 2 | 0.068825 | -7.47 |
| w23 | 3 | 0.044437 | 2.313 |
| w24 | 6 | -0.037217 | -5.525 |
| w25 | 0 | None | 0.0 |
| w26 | 3 | -0.043927 | 3.941 |
| w27 | 5 | -0.057428 | -13.743 |
| w28 | 2 | 0.051494 | -5.586 |
| w29 | 5 | -0.185755 | -6.789 |
| w30 | 7 | 0.215851 | 13.136 |
| w31 | 2 | 0.183142 | 8.083 |
| w32 | 3 | 0.304991 | 43.221 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 6 | -0.112635 | 19.138 |
| w6 | 8 | 0.207745 | -1.241 |
| w7 | 2 | -0.121027 | -0.419 |
| w8 | 2 | 0.234641 | 9.728 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | -0.097187 | 4.171 |
| w11 | 2 | 0.042507 | -7.948 |
| w12 | 4 | -0.078477 | -2.071 |
| w13 | 2 | -0.018833 | -1.566 |
| w14 | 4 | 0.104666 | 10.082 |
| w15 | 4 | 0.029834 | -10.261 |
| w16 | 10 | 0.049319 | 14.272 |
| w17 | 1 | -0.010667 | -2.866 |
| w18 | 0 | None | 0.0 |
| w19 | 2 | -0.070974 | -0.329 |
| w20 | 5 | 0.000899 | 1.183 |
| w21 | 2 | -0.324262 | -20.808 |
| w22 | 3 | 0.08033 | -1.452 |
| w23 | 1 | 0.195552 | 5.796 |
| w24 | 4 | -0.021234 | 0.094 |
| w25 | 4 | 0.085425 | 9.435 |
| w26 | 1 | 0.011467 | -0.225 |
| w27 | 4 | 0.097152 | 31.655 |
| w28 | 2 | -0.086332 | -0.457 |
| w29 | 1 | -0.059377 | -0.157 |
| w30 | 9 | 0.134166 | 3.626 |
| w31 | 0 | -0.234341 | 0.0 |
| w32 | 7 | -0.087466 | 4.512 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 4 | 0.12942 | 8.22 |
| w18 | 4 | -0.171103 | -11.398 |
| w19 | 1 | -0.083013 | 1.434 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | 0.088655 | 6.902 |
| w22 | 3 | -0.147569 | 7.023 |
| w23 | 3 | -0.044994 | -9.305 |
| w24 | 5 | 0.138343 | 25.273 |
| w25 | 9 | -0.046769 | 13.766 |
| w26 | 3 | -0.046205 | -4.944 |
| w27 | 4 | 0.03991 | 24.497 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | 0.026573 | -2.107 |
| w30 | 2 | 0.025575 | -8.594 |
| w31 | 0 | 0.003227 | 0.0 |
| w32 | 5 | -0.137047 | -20.625 |

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
| w17 | 4 | 0.123023 | 6.411 |
| w18 | 5 | 1.1e-05 | -1.104 |
| w19 | 6 | -0.038787 | 2.794 |
| w20 | 3 | 0.161421 | -1.353 |
| w21 | 5 | -0.153299 | -25.526 |
| w22 | 2 | 0.171573 | 2.257 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | -0.091062 | 4.839 |
| w25 | 1 | 0.024915 | 12.944 |
| w26 | 0 | None | 0.0 |
| w27 | 3 | 0.059668 | -1.025 |
| w28 | 2 | -0.00637 | -0.452 |
| w29 | 7 | -0.022284 | 12.88 |
| w30 | 0 | None | 0.0 |
| w31 | 3 | -0.10178 | -19.399 |
| w32 | 2 | 0.128616 | 0.887 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 1 | -0.073126 | -1.402 |
| w20 | 4 | -0.053763 | 21.664 |
| w21 | 3 | 0.004706 | -0.358 |
| w22 | 14 | 0.022866 | 65.463 |
| w23 | 2 | -0.100607 | -5.801 |
| w24 | 7 | 0.237867 | 44.557 |
| w25 | 1 | -0.113024 | -7.841 |
| w26 | 3 | -0.092659 | -5.769 |
| w27 | 4 | -0.056807 | 5.241 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | -0.047218 | -7.489 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 5 | -0.105117 | -16.432 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 5 | 0.091355 | 16.081 |
| w23 | 0 | 0.070406 | 0.0 |
| w24 | 6 | -0.105597 | -12.567 |
| w25 | 3 | -0.055415 | 1.32 |
| w26 | 0 | None | 0.0 |
| w27 | 4 | 0.090938 | -3.628 |
| w28 | 1 | -0.010904 | -0.473 |
| w29 | 2 | 0.072386 | 9.812 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | 0.048533 | 14.728 |
| w32 | 4 | 0.049323 | -6.66 |

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
| w27 | 1 | -0.091392 | 9.799 |
| w28 | 3 | 0.010296 | -1.708 |
| w29 | 4 | 0.058593 | 1.499 |
| w30 | 2 | 0.119861 | 0.517 |
| w31 | 5 | -0.166692 | -21.095 |
| w32 | 3 | 0.131257 | 32.412 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 2 | 0.017071 | 0.202 |
| w18 | 0 | None | 0.0 |
| w19 | 1 | -0.011855 | -11.919 |
| w20 | 0 | None | 0.0 |
| w21 | 6 | 0.003398 | -25.733 |
| w22 | 6 | -0.125319 | 1.897 |
| w23 | 2 | 0.088304 | 6.023 |
| w24 | 9 | -0.113324 | -5.424 |
| w25 | 2 | 0.018167 | 0.967 |
| w26 | 4 | -0.030898 | -7.326 |
| w27 | 4 | 0.216571 | 19.822 |
| w28 | 1 | -0.037989 | -13.38 |
| w29 | 8 | -0.067962 | -12.587 |
| w30 | 1 | -0.134818 | -13.083 |
| w31 | 2 | 0.004951 | 0.266 |
| w32 | 0 | None | 0.0 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 0 | None | 0.0 |
| w18 | 0 | 0.002526 | 0.0 |
| w19 | 1 | -0.14157 | -9.94 |
| w20 | 0 | None | 0.0 |
| w21 | 4 | -0.197458 | -25.148 |
| w22 | 6 | -0.046435 | 25.391 |
| w23 | 1 | 0.113843 | 6.738 |
| w24 | 1 | 0.204347 | 10.337 |
| w25 | 3 | -0.017601 | 1.209 |
| w26 | 2 | -0.087011 | 5.679 |
| w27 | 6 | 0.144417 | 6.498 |
| w28 | 0 | None | 0.0 |
| w29 | 10 | 0.190828 | 12.481 |
| w30 | 2 | -0.080454 | -6.564 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | 0.06704 | -6.045 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 4 | 0.067981 | 7.496 |
| w29 | 2 | 0.021726 | -3.027 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | 0.109517 | 9.629 |
| w32 | 2 | -0.035152 | -0.24 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 0 | None | 0.0 |
| w15 | 5 | 0.189432 | 3.704 |
| w16 | 3 | -0.018654 | -0.306 |
| w17 | 2 | 0.044594 | 0.987 |
| w18 | 3 | -0.019772 | -1.788 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | 0.211031 | 17.527 |
| w21 | 1 | -0.045555 | -3.949 |
| w22 | 1 | -0.06598 | -12.008 |
| w23 | 3 | 0.055214 | 3.535 |
| w24 | 1 | 0.025023 | 4.401 |
| w25 | 6 | 0.171159 | 37.943 |
| w26 | 2 | -0.050975 | 0.415 |
| w27 | 1 | 0.092701 | 19.389 |
| w28 | 1 | -0.018374 | -2.916 |
| w29 | 5 | -0.07193 | -6.699 |
| w30 | 2 | 0.050468 | 11.811 |
| w31 | 5 | -0.095222 | -2.957 |
| w32 | 4 | 0.01045 | -19.939 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 2 | 0.033065 | 9.232 |
| w26 | 1 | -0.060007 | -4.728 |
| w27 | 6 | -0.114897 | -26.241 |
| w28 | 2 | -0.005168 | 2.056 |
| w29 | 5 | -0.008773 | -3.529 |
| w30 | 2 | 0.04753 | 10.661 |
| w31 | 6 | -0.089818 | 3.772 |
| w32 | 4 | 0.029804 | -0.884 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

