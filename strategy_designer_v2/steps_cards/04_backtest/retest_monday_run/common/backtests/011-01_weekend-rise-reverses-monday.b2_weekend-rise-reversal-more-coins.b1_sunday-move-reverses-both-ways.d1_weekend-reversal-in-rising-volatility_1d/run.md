# Backtest of 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility_1d

- Plan: `../../../../../03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.091175 | 1.243 |
| w2 | 13 | 0.078569 | 7.127 |
| w3 | 8 | 0.018117 | 15.564 |
| w4 | 15 | -0.066118 | -24.374 |
| w5 | 13 | 0.058205 | 15.919 |
| w6 | 14 | -0.044212 | -1.399 |
| w7 | 9 | 0.014623 | -5.278 |
| w8 | 4 | 0.065303 | -0.287 |
| w9 | 7 | 0.241946 | 35.299 |
| w10 | 8 | 0.033734 | 1.963 |
| w11 | 12 | 0.113129 | 11.804 |
| w12 | 6 | 0.208989 | 9.055 |
| w13 | 11 | 0.148921 | 6.553 |
| w14 | 9 | 0.059674 | 1.457 |
| w15 | 17 | -0.087479 | 6.25 |
| w16 | 7 | -0.008227 | -1.189 |
| w17 | 9 | 0.131409 | 0.779 |
| w18 | 6 | -0.011088 | -6.955 |
| w19 | 9 | -0.067198 | -0.234 |
| w20 | 8 | -0.098942 | -11.614 |
| w21 | 8 | -0.008638 | 1.513 |
| w22 | 12 | 0.156348 | 9.666 |
| w23 | 7 | 0.05167 | 0.427 |
| w24 | 10 | -0.054565 | -2.739 |
| w25 | 11 | -0.119959 | 7.746 |
| w26 | 13 | -0.153957 | -8.638 |
| w27 | 4 | -0.339164 | -16.713 |
| w28 | 9 | 0.108101 | 19.939 |
| w29 | 4 | -0.008989 | 2.446 |
| w30 | 17 | -0.145359 | 4.04 |
| w31 | 6 | 0.08228 | 1.654 |
| w32 | 8 | 0.007334 | 3.502 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.084403 | -21.45 |
| w2 | 8 | 0.175635 | 10.934 |
| w3 | 9 | 0.053139 | 5.303 |
| w4 | 14 | -0.013149 | -17.993 |
| w5 | 10 | 0.064793 | -6.037 |
| w6 | 20 | 0.128483 | 19.771 |
| w7 | 9 | 0.091088 | 4.113 |
| w8 | 12 | 0.005626 | -6.592 |
| w9 | 11 | -0.037802 | -3.409 |
| w10 | 10 | 0.166506 | 3.957 |
| w11 | 10 | 0.015826 | -6.919 |
| w12 | 9 | 0.178817 | 7.307 |
| w13 | 13 | 0.062188 | -2.141 |
| w14 | 8 | 0.089833 | 6.963 |
| w15 | 15 | -0.006468 | 11.968 |
| w16 | 5 | 0.018249 | -0.468 |
| w17 | 12 | 0.292611 | 23.578 |
| w18 | 11 | 0.018014 | 17.336 |
| w19 | 7 | -0.185542 | -2.68 |
| w20 | 8 | 0.061864 | -2.284 |
| w21 | 10 | -0.034332 | 0.07 |
| w22 | 10 | -0.003071 | -5.835 |
| w23 | 6 | 0.098779 | 6.261 |
| w24 | 8 | 0.062816 | 7.647 |
| w25 | 14 | 0.197597 | -2.154 |
| w26 | 6 | 0.188261 | 9.284 |
| w27 | 15 | -0.093809 | -13.039 |
| w28 | 6 | -0.0665 | -8.415 |
| w29 | 10 | -0.045241 | -11.128 |
| w30 | 9 | -0.036851 | 7.378 |
| w31 | 6 | -0.031144 | -4.167 |
| w32 | 10 | -0.016064 | -4.998 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 10 | 0.036051 | 26.296 |
| w7 | 3 | 0.08676 | 6.084 |
| w8 | 5 | 0.065447 | -1.03 |
| w9 | 7 | -0.04892 | 0.266 |
| w10 | 6 | 0.035042 | 2.949 |
| w11 | 6 | 0.068889 | 30.209 |
| w12 | 12 | -0.051955 | -18.593 |
| w13 | 15 | 0.122051 | 13.42 |
| w14 | 6 | 0.066706 | 0.562 |
| w15 | 11 | 0.221416 | 23.857 |
| w16 | 12 | 0.117343 | 8.86 |
| w17 | 4 | 0.025631 | -0.737 |
| w18 | 6 | 0.059752 | 0.201 |
| w19 | 9 | -0.202944 | -11.846 |
| w20 | 2 | 0.077816 | 0.345 |
| w21 | 8 | 0.236043 | 41.623 |
| w22 | 6 | 0.0113 | 0.099 |
| w23 | 8 | 0.014736 | -1.411 |
| w24 | 6 | -0.265436 | -13.258 |
| w25 | 8 | 0.157465 | 2.261 |
| w26 | 18 | -0.020729 | 5.816 |
| w27 | 11 | -0.137843 | -4.025 |
| w28 | 6 | 0.174192 | 9.043 |
| w29 | 8 | -0.081578 | -0.228 |
| w30 | 10 | -0.306206 | -7.132 |
| w31 | 5 | -0.028478 | -4.873 |
| w32 | 11 | -0.020171 | 1.156 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 6 | -0.039232 | -3.31 |
| w8 | 3 | 0.184627 | 4.167 |
| w9 | 8 | -0.08971 | -8.567 |
| w10 | 10 | 0.036234 | 2.156 |
| w11 | 4 | 0.016721 | -8.453 |
| w12 | 9 | 0.10046 | 0.053 |
| w13 | 10 | 0.087891 | -16.716 |
| w14 | 5 | 0.086177 | -0.261 |
| w15 | 14 | 0.022119 | 24.524 |
| w16 | 8 | 0.180751 | 8.568 |
| w17 | 6 | 0.358134 | 8.331 |
| w18 | 12 | -0.048258 | 4.489 |
| w19 | 11 | -0.020484 | -0.922 |
| w20 | 9 | 0.005299 | -4.155 |
| w21 | 3 | 0.087067 | 1.762 |
| w22 | 10 | 0.132314 | 6.855 |
| w23 | 11 | 0.178986 | 14.674 |
| w24 | 12 | 0.005795 | -0.728 |
| w25 | 10 | 0.055065 | -1.322 |
| w26 | 9 | 0.135614 | 10.812 |
| w27 | 12 | -0.030564 | 0.222 |
| w28 | 11 | -0.082386 | -11.534 |
| w29 | 12 | -0.044218 | -2.231 |
| w30 | 15 | 0.009119 | -5.327 |
| w31 | 3 | 0.266224 | 3.431 |
| w32 | 9 | 0.147749 | 9.526 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.190278 | -20.078 |
| w2 | 9 | 0.05899 | -4.675 |
| w3 | 14 | -0.102109 | -4.249 |
| w4 | 13 | -0.154267 | -28.451 |
| w5 | 12 | -0.139355 | -27.23 |
| w6 | 17 | 0.150111 | 39.225 |
| w7 | 10 | 0.059481 | 2.971 |
| w8 | 7 | 0.053105 | 1.566 |
| w9 | 10 | -0.054569 | 2.319 |
| w10 | 10 | 0.19394 | 5.301 |
| w11 | 9 | 0.019807 | -5.064 |
| w12 | 10 | 0.201563 | 16.343 |
| w13 | 16 | 0.09521 | 11.923 |
| w14 | 7 | 0.060603 | 1.806 |
| w15 | 14 | -0.074501 | -0.191 |
| w16 | 8 | 0.021778 | -4.859 |
| w17 | 6 | 0.217053 | 11.599 |
| w18 | 11 | 0.003755 | -8.693 |
| w19 | 7 | 0.009364 | 4.018 |
| w20 | 11 | -0.177687 | -19.117 |
| w21 | 9 | 0.002686 | -7.53 |
| w22 | 9 | 0.145715 | 11.162 |
| w23 | 7 | 0.059328 | -2.246 |
| w24 | 13 | -0.049819 | 1.332 |
| w25 | 11 | 0.02883 | 29.801 |
| w26 | 11 | -0.173834 | -11.655 |
| w27 | 8 | -0.01287 | -0.38 |
| w28 | 15 | 0.125965 | 4.584 |
| w29 | 6 | 0.007531 | 3.872 |
| w30 | 10 | -0.038108 | 10.887 |
| w31 | 6 | 0.134351 | 9.854 |
| w32 | 10 | -0.034604 | -1.371 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 9 | 0.238437 | 12.868 |
| w11 | 9 | 0.072565 | 13.626 |
| w12 | 9 | 0.149782 | 4.236 |
| w13 | 16 | 0.106073 | 11.646 |
| w14 | 8 | 0.162123 | 6.777 |
| w15 | 16 | -0.076403 | -12.665 |
| w16 | 9 | -0.083566 | -14.997 |
| w17 | 8 | 0.09604 | 6.824 |
| w18 | 9 | -0.037173 | -2.2 |
| w19 | 7 | -0.230315 | -2.711 |
| w20 | 9 | -0.056608 | -6.308 |
| w21 | 12 | 0.024985 | -6.115 |
| w22 | 9 | 0.037678 | 4.429 |
| w23 | 10 | 0.091204 | 5.324 |
| w24 | 14 | 0.022631 | 1.015 |
| w25 | 10 | 0.130831 | 11.331 |
| w26 | 10 | 0.195856 | 12.275 |
| w27 | 12 | -0.113769 | -0.481 |
| w28 | 4 | 0.1336 | 6.388 |
| w29 | 13 | 0.014778 | 7.018 |
| w30 | 10 | -0.089521 | 0.674 |
| w31 | 10 | -0.024775 | -8.505 |
| w32 | 9 | 0.010934 | 2.396 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 11 | 0.034695 | 0.11 |
| w13 | 11 | 0.08903 | -0.657 |
| w14 | 7 | 0.062601 | 8.257 |
| w15 | 4 | -0.002028 | -1.677 |
| w16 | 15 | -0.06105 | -8.065 |
| w17 | 6 | 0.041115 | -0.868 |
| w18 | 7 | 0.129278 | 33.108 |
| w19 | 14 | 0.030915 | 2.336 |
| w20 | 9 | -0.05414 | -5.578 |
| w21 | 10 | 0.093413 | 1.688 |
| w22 | 9 | 0.155898 | 7.006 |
| w23 | 7 | -0.008728 | -1.007 |
| w24 | 14 | 0.218852 | 28.13 |
| w25 | 6 | 0.040265 | 5.754 |
| w26 | 7 | 0.035394 | -4.455 |
| w27 | 12 | 0.061063 | -0.778 |
| w28 | 5 | -0.058576 | -2.431 |
| w29 | 5 | -0.017399 | -0.932 |
| w30 | 10 | -0.112538 | 0.906 |
| w31 | 10 | 0.013544 | -12.49 |
| w32 | 12 | 0.034294 | -6.082 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 9 | 0.099144 | 13.526 |
| w16 | 11 | -0.169849 | -15.826 |
| w17 | 8 | 0.235995 | 12.397 |
| w18 | 13 | -0.040644 | 7.521 |
| w19 | 5 | 0.056065 | 0.044 |
| w20 | 7 | -0.118817 | -15.949 |
| w21 | 5 | 0.093048 | -5.259 |
| w22 | 12 | 0.06607 | 14.146 |
| w23 | 13 | 0.160366 | 12.856 |
| w24 | 15 | 0.048511 | 23.151 |
| w25 | 12 | 0.245823 | 16.653 |
| w26 | 10 | 0.050185 | 7.421 |
| w27 | 13 | -0.016351 | 4.817 |
| w28 | 7 | 0.003094 | -5.968 |
| w29 | 4 | -0.00465 | 3.915 |
| w30 | 8 | -0.116966 | -2.346 |
| w31 | 13 | 0.078558 | -2.418 |
| w32 | 10 | 0.019596 | -1.239 |

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
| w15 | 12 | 0.047478 | 20.237 |
| w16 | 13 | -0.147163 | 0.478 |
| w17 | 5 | 0.280078 | 7.792 |
| w18 | 12 | 0.032277 | 9.884 |
| w19 | 10 | -0.093122 | -3.072 |
| w20 | 4 | 0.255922 | 11.425 |
| w21 | 8 | 0.053119 | -1.66 |
| w22 | 17 | -0.026544 | -2.356 |
| w23 | 6 | -0.066572 | -1.828 |
| w24 | 9 | 0.078801 | 0.99 |
| w25 | 9 | -0.095004 | -6.005 |
| w26 | 11 | 0.116565 | 13.908 |
| w27 | 14 | -0.07383 | -67.483 |
| w28 | 3 | 0.001589 | -0.533 |
| w29 | 12 | 0.11479 | 7.747 |
| w30 | 7 | -0.007609 | -3.978 |
| w31 | 4 | 0.067677 | -1.025 |
| w32 | 8 | 0.052928 | 11.723 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 7 | -0.071596 | -5.537 |
| w17 | 8 | 0.261243 | 10.734 |
| w18 | 7 | 0.05023 | 13.073 |
| w19 | 3 | -0.096289 | -7.233 |
| w20 | 5 | -0.118381 | -5.696 |
| w21 | 6 | 0.044439 | -6.751 |
| w22 | 9 | 0.07915 | 10.814 |
| w23 | 6 | 0.121429 | 3.853 |
| w24 | 13 | 0.050206 | 10.109 |
| w25 | 13 | 0.094444 | 13.979 |
| w26 | 11 | 0.051386 | 4.421 |
| w27 | 13 | -0.006473 | 0.785 |
| w28 | 8 | 0.15221 | 6.114 |
| w29 | 7 | -0.09499 | 0.065 |
| w30 | 10 | -0.077389 | -1.805 |
| w31 | 12 | -0.059701 | -11.288 |
| w32 | 14 | 0.053552 | 0.681 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 6 | -0.050365 | -5.342 |
| w21 | 6 | -0.027559 | -12.449 |
| w22 | 9 | 0.009446 | 5.46 |
| w23 | 5 | 0.050494 | 4.31 |
| w24 | 15 | 0.094724 | 6.909 |
| w25 | 12 | 0.043606 | 14.134 |
| w26 | 9 | -0.044071 | 10.429 |
| w27 | 11 | 0.056504 | 4.567 |
| w28 | 8 | 0.078919 | 10.811 |
| w29 | 10 | 0.010807 | 5.159 |
| w30 | 9 | -0.0777 | 0.69 |
| w31 | 8 | -0.060089 | -11.253 |
| w32 | 11 | 0.061978 | 7.145 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 9 | 0.054864 | 8.463 |
| w23 | 7 | 0.116533 | 4.564 |
| w24 | 15 | 0.103825 | 28.88 |
| w25 | 9 | 0.211452 | 22.275 |
| w26 | 10 | 0.05956 | 2.102 |
| w27 | 7 | 0.057223 | 1.555 |
| w28 | 11 | 0.100628 | 4.643 |
| w29 | 7 | -0.01994 | -0.55 |
| w30 | 12 | -0.017626 | 8.541 |
| w31 | 10 | 0.037166 | -2.847 |
| w32 | 14 | -0.032171 | 0.266 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 9 | -0.060846 | 7.701 |
| w25 | 19 | 0.124253 | 5.331 |
| w26 | 11 | 0.097959 | 9.614 |
| w27 | 10 | 0.024836 | 6.912 |
| w28 | 9 | 0.138863 | 10.372 |
| w29 | 7 | -0.136967 | -5.246 |
| w30 | 7 | -0.097496 | 3.207 |
| w31 | 7 | 0.024899 | -2.013 |
| w32 | 7 | 0.152527 | 22.011 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 8 | -0.521665 | -61.005 |
| w6 | 14 | -0.066741 | 4.847 |
| w7 | 6 | 0.038972 | 6.471 |
| w8 | 8 | 0.0444 | 4.412 |
| w9 | 11 | 0.022385 | 3.571 |
| w10 | 10 | -0.07146 | -8.656 |
| w11 | 15 | 0.042939 | -7.305 |
| w12 | 11 | 0.24216 | 18.294 |
| w13 | 7 | 0.096651 | 5.732 |
| w14 | 9 | 0.049127 | 4.489 |
| w15 | 11 | 0.105857 | 15.902 |
| w16 | 15 | 0.106773 | -3.726 |
| w17 | 8 | 0.224591 | 8.611 |
| w18 | 8 | 0.060181 | 6.619 |
| w19 | 11 | 0.087549 | 27.273 |
| w20 | 5 | 0.094425 | 1.325 |
| w21 | 7 | 0.02937 | 2.076 |
| w22 | 12 | 0.031273 | 10.412 |
| w23 | 11 | 0.034643 | -0.586 |
| w24 | 13 | 0.085409 | 12.432 |
| w25 | 15 | 0.061901 | -12.462 |
| w26 | 9 | 0.225524 | 33.426 |
| w27 | 13 | 0.091223 | -4.962 |
| w28 | 5 | -0.171588 | -2.993 |
| w29 | 9 | -0.037797 | 5.381 |
| w30 | 12 | -0.101212 | -15.234 |
| w31 | 9 | 0.025444 | 1.53 |
| w32 | 11 | -0.034287 | 0.657 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 10 | 0.037332 | 10.827 |
| w6 | 17 | 0.076668 | 16.329 |
| w7 | 12 | -0.127941 | -4.897 |
| w8 | 11 | -0.14224 | -4.97 |
| w9 | 11 | 0.112436 | 14.743 |
| w10 | 8 | 0.095469 | 3.449 |
| w11 | 11 | 0.109904 | 6.607 |
| w12 | 9 | 0.196253 | 10.245 |
| w13 | 16 | 0.121901 | 6.746 |
| w14 | 10 | 0.14255 | -1.54 |
| w15 | 10 | 0.081899 | 7.604 |
| w16 | 10 | 0.206165 | 37.085 |
| w17 | 12 | 0.020751 | -2.002 |
| w18 | 11 | -0.09659 | -2.373 |
| w19 | 10 | 0.091126 | 2.472 |
| w20 | 9 | 0.16657 | 11.86 |
| w21 | 11 | -0.015824 | 9.921 |
| w22 | 11 | 0.002058 | 8.686 |
| w23 | 12 | -0.071394 | -8.099 |
| w24 | 9 | 0.108643 | 7.07 |
| w25 | 15 | -0.009963 | 1.005 |
| w26 | 13 | 0.103967 | 3.04 |
| w27 | 12 | 0.326317 | 27.809 |
| w28 | 4 | 0.037887 | 1.295 |
| w29 | 17 | -0.024248 | 16.444 |
| w30 | 11 | 0.222019 | 31.47 |
| w31 | 11 | -0.064859 | -17.421 |
| w32 | 13 | -0.128793 | -13.447 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 8 | 0.19527 | 16.866 |
| w18 | 15 | 0.1125 | 17.078 |
| w19 | 4 | -0.065226 | 0.496 |
| w20 | 10 | 0.090163 | 3.168 |
| w21 | 7 | 0.05249 | -1.927 |
| w22 | 9 | 0.152123 | 14.543 |
| w23 | 10 | 0.058202 | 0.778 |
| w24 | 8 | 0.304454 | 34.303 |
| w25 | 7 | -0.054907 | 1.039 |
| w26 | 8 | 0.121871 | 0.337 |
| w27 | 12 | 0.122201 | 21.087 |
| w28 | 11 | 0.070515 | 5.776 |
| w29 | 5 | -0.051142 | -1.981 |
| w30 | 7 | -0.07663 | 2.572 |
| w31 | 10 | -0.006949 | -8.709 |
| w32 | 14 | 0.156435 | 2.24 |

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
| w17 | 10 | 0.174884 | 3.281 |
| w18 | 10 | -0.106733 | -9.864 |
| w19 | 6 | -0.067722 | 2.701 |
| w20 | 7 | 0.050611 | -4.023 |
| w21 | 5 | 0.048087 | -13.899 |
| w22 | 12 | 0.148612 | 4.351 |
| w23 | 7 | 0.088187 | 0.738 |
| w24 | 14 | 0.071581 | 17.804 |
| w25 | 18 | 0.112901 | 22.43 |
| w26 | 8 | 0.039031 | 17.956 |
| w27 | 16 | -0.014731 | -9.409 |
| w28 | 7 | 0.231458 | 3.892 |
| w29 | 11 | 0.008454 | 4.262 |
| w30 | 13 | -0.062936 | 13.077 |
| w31 | 11 | 0.018986 | 0.026 |
| w32 | 10 | 0.056403 | -0.487 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 9 | -0.139776 | -6.925 |
| w20 | 8 | -0.006579 | -6.736 |
| w21 | 7 | 0.157545 | 15.015 |
| w22 | 11 | -0.011795 | 5.892 |
| w23 | 0 | -0.112857 | 0.0 |
| w24 | 14 | -0.204121 | -49.434 |
| w25 | 13 | 0.287354 | 16.197 |
| w26 | 13 | 0.177284 | 12.725 |
| w27 | 9 | 0.03381 | 5.776 |
| w28 | 12 | 0.008683 | -2.569 |
| w29 | 10 | 0.116318 | 8.873 |
| w30 | 10 | -0.050579 | 4.462 |
| w31 | 8 | -0.006466 | -11.727 |
| w32 | 16 | 0.028519 | -2.993 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 8 | 0.148835 | 11.792 |
| w23 | 11 | -0.097078 | -6.085 |
| w24 | 11 | 0.010691 | 5.408 |
| w25 | 14 | -0.017383 | 23.403 |
| w26 | 10 | 0.049362 | 1.778 |
| w27 | 9 | -0.02283 | -4.626 |
| w28 | 5 | 0.139398 | 6.063 |
| w29 | 11 | -0.07831 | -1.62 |
| w30 | 7 | -0.147855 | -1.805 |
| w31 | 11 | 0.204497 | 24.532 |
| w32 | 14 | 0.196237 | 17.653 |

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
| w27 | 12 | 0.026151 | 4.793 |
| w28 | 10 | 0.134605 | 10.769 |
| w29 | 7 | -0.082369 | 2.022 |
| w30 | 12 | -0.090376 | 2.893 |
| w31 | 10 | 0.013919 | -7.133 |
| w32 | 10 | -0.021024 | 2.633 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 5 | 0.163614 | 1.531 |
| w18 | 10 | 0.117431 | 13.228 |
| w19 | 10 | -0.111183 | -8.623 |
| w20 | 7 | 0.147303 | 8.917 |
| w21 | 8 | -0.079785 | -19.275 |
| w22 | 10 | 0.013219 | 11.8 |
| w23 | 5 | 0.11589 | 4.357 |
| w24 | 14 | 0.037332 | 12.883 |
| w25 | 12 | 0.105327 | 13.286 |
| w26 | 9 | 0.203947 | 12.462 |
| w27 | 14 | 0.130051 | 13.613 |
| w28 | 4 | -0.039537 | -5.514 |
| w29 | 4 | -0.087757 | -0.71 |
| w30 | 10 | -0.051522 | -2.408 |
| w31 | 15 | -0.062896 | -13.793 |
| w32 | 16 | 0.058766 | 2.968 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 7 | 0.147812 | 16.131 |
| w18 | 14 | 0.017555 | 4.488 |
| w19 | 7 | 0.011016 | 3.109 |
| w20 | 8 | -0.045634 | -5.829 |
| w21 | 3 | -0.034587 | -4.195 |
| w22 | 8 | 0.07803 | -42.063 |
| w23 | 7 | -0.296559 | -9.893 |
| w24 | 11 | -0.220691 | -3.942 |
| w25 | 8 | 0.075677 | 6.53 |
| w26 | 12 | 0.094564 | 8.561 |
| w27 | 6 | 0.144725 | 17.801 |
| w28 | 9 | 0.036223 | 1.943 |
| w29 | 8 | 0.020399 | 5.567 |
| w30 | 8 | -0.140889 | -0.228 |
| w31 | 8 | -0.052398 | -12.607 |
| w32 | 13 | 0.106147 | 2.565 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 14 | 0.012401 | -3.377 |
| w29 | 4 | -0.051485 | -0.562 |
| w30 | 7 | -0.188269 | -9.46 |
| w31 | 15 | 0.086376 | -6.601 |
| w32 | 10 | -0.000452 | 9.346 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 3 | -0.207625 | -3.272 |
| w15 | 8 | 0.151834 | 36.576 |
| w16 | 12 | -0.015262 | -0.202 |
| w17 | 3 | 0.105316 | 2.051 |
| w18 | 4 | -0.007521 | 0.261 |
| w19 | 7 | 0.143485 | 2.696 |
| w20 | 10 | -0.009831 | -2.869 |
| w21 | 8 | 0.008814 | -7.076 |
| w22 | 11 | 0.241794 | 9.983 |
| w23 | 5 | 0.000727 | -5.512 |
| w24 | 9 | -0.314107 | -19.076 |
| w25 | 12 | -0.007169 | 8.283 |
| w26 | 9 | 0.089514 | 8.934 |
| w27 | 4 | -0.276983 | -16.142 |
| w28 | 10 | 0.13726 | 10.31 |
| w29 | 10 | 0.001841 | 8.187 |
| w30 | 5 | -0.051909 | 4.017 |
| w31 | 9 | -0.074392 | -9.504 |
| w32 | 11 | 0.051193 | 8.446 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 7 | -0.066493 | -0.438 |
| w26 | 10 | 0.062288 | 2.242 |
| w27 | 8 | 0.091692 | -0.799 |
| w28 | 10 | 0.149152 | 6.488 |
| w29 | 5 | 4.9e-05 | -0.16 |
| w30 | 7 | -0.094194 | -1.026 |
| w31 | 10 | 0.017005 | 3.145 |
| w32 | 13 | 0.038835 | -0.822 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

