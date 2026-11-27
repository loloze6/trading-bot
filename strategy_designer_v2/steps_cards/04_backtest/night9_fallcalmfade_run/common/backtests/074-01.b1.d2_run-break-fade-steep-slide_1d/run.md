# Backtest of 074-01.b1.d2_run-break-fade-steep-slide_1d

- Plan: `../../../../../03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.d2_run-break-fade-steep-slide_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.006765 | -0.081 |
| w2 | 2 | 0.053656 | 1.018 |
| w3 | 1 | -0.194109 | -1.686 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 11 | 0.194219 | 12.692 |
| w8 | 7 | 0.122151 | 8.003 |
| w9 | 10 | 0.180777 | 33.542 |
| w10 | 2 | 0.088636 | 0.512 |
| w11 | 0 | None | 0.0 |
| w12 | 13 | 0.005946 | 1.261 |
| w13 | 5 | -0.042613 | -0.84 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 10 | 0.159937 | 10.197 |
| w18 | 4 | -0.034811 | -2.337 |
| w19 | 6 | 0.023224 | 1.419 |
| w20 | 10 | 0.102642 | 10.669 |
| w21 | 16 | -0.036756 | -2.587 |
| w22 | 1 | 0.006236 | -0.085 |
| w23 | 3 | 0.018524 | 0.726 |
| w24 | 3 | -0.024157 | -3.502 |
| w25 | 0 | None | 0.0 |
| w26 | 2 | 0.036298 | 1.569 |
| w27 | 0 | None | 0.0 |
| w28 | 4 | 0.000979 | -0.5 |
| w29 | 0 | None | 0.0 |
| w30 | 8 | -0.009435 | 0.13 |
| w31 | 12 | 0.035305 | 5.061 |
| w32 | 9 | -0.028153 | -2.792 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.012893 | 0.063 |
| w2 | 6 | -0.053608 | -2.878 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | -0.025893 | -2.785 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | -0.062518 | -2.474 |
| w7 | 8 | -0.054832 | -3.556 |
| w8 | 15 | 0.129077 | 15.325 |
| w9 | 14 | 0.236409 | 33.574 |
| w10 | 1 | 0.122608 | 1.334 |
| w11 | 7 | -0.028747 | -2.661 |
| w12 | 14 | -0.042082 | -3.559 |
| w13 | 6 | 0.134585 | 5.466 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | 0.007033 | -0.694 |
| w16 | 0 | None | 0.0 |
| w17 | 11 | -0.016607 | -0.973 |
| w18 | 2 | -0.022153 | -0.708 |
| w19 | 13 | 0.048729 | 3.017 |
| w20 | 9 | 0.033597 | 5.51 |
| w21 | 3 | 0.079387 | 1.49 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.063303 | -3.349 |
| w24 | 7 | -0.019285 | -2.436 |
| w25 | 0 | None | 0.0 |
| w26 | 8 | 0.11735 | 10.235 |
| w27 | 1 | -0.023316 | -0.909 |
| w28 | 6 | 0.02784 | 1.569 |
| w29 | 3 | 0.040774 | 0.177 |
| w30 | 14 | -0.032023 | -2.116 |
| w31 | 16 | -0.006428 | 0.431 |
| w32 | 8 | -0.024644 | -2.55 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 3 | -0.004327 | -2.118 |
| w7 | 7 | -0.04026 | -3.826 |
| w8 | 10 | 0.023006 | 5.519 |
| w9 | 11 | 0.028955 | -0.838 |
| w10 | 8 | 0.089987 | 3.401 |
| w11 | 8 | -0.034511 | -3.31 |
| w12 | 6 | 0.102835 | 6.83 |
| w13 | 6 | 0.145288 | 6.461 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.005493 | -1.026 |
| w16 | 1 | -0.029333 | -0.233 |
| w17 | 10 | 0.059488 | 2.517 |
| w18 | 5 | -0.008551 | -0.054 |
| w19 | 6 | 0.06883 | 5.121 |
| w20 | 4 | -0.134608 | 12.604 |
| w21 | 6 | 0.041798 | 1.645 |
| w22 | 1 | 0.038604 | 0.348 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | -0.023839 | -1.895 |
| w25 | 7 | 0.076529 | 6.889 |
| w26 | 6 | 0.15731 | 11.921 |
| w27 | 1 | 0.112248 | 3.016 |
| w28 | 4 | 0.076506 | 2.377 |
| w29 | 1 | 0.010489 | 0.018 |
| w30 | 15 | -0.143338 | -12.529 |
| w31 | 12 | 0.0073 | 1.381 |
| w32 | 7 | 0.010732 | -0.419 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 11 | 0.049562 | 1.789 |
| w8 | 8 | 0.111086 | 10.035 |
| w9 | 15 | 0.028573 | 5.455 |
| w10 | 6 | 0.088094 | 1.173 |
| w11 | 5 | 0.095313 | 3.281 |
| w12 | 10 | -0.041934 | -6.884 |
| w13 | 5 | 0.05329 | 0.564 |
| w14 | 2 | -0.017808 | -1.766 |
| w15 | 2 | 0.000237 | -0.451 |
| w16 | 0 | None | 0.0 |
| w17 | 10 | 0.041682 | 1.394 |
| w18 | 8 | -0.068676 | -5.958 |
| w19 | 12 | 0.130761 | 9.953 |
| w20 | 9 | 0.155956 | 16.247 |
| w21 | 9 | -0.024584 | -2.524 |
| w22 | 3 | 0.019881 | -0.27 |
| w23 | 2 | 0.078632 | 4.288 |
| w24 | 4 | 0.058726 | 0.568 |
| w25 | 0 | None | 0.0 |
| w26 | 12 | 0.144231 | 13.052 |
| w27 | 1 | -0.085641 | -2.395 |
| w28 | 7 | -0.099394 | -7.986 |
| w29 | 0 | None | 0.0 |
| w30 | 3 | 0.006384 | -1.122 |
| w31 | 8 | -0.046789 | -6.134 |
| w32 | 12 | 0.146536 | 19.11 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 3 | -0.115816 | -3.817 |
| w3 | 8 | 0.029372 | 6.894 |
| w4 | 1 | -0.003206 | -0.393 |
| w5 | 0 | 0.051909 | 0.0 |
| w6 | 2 | 0.049308 | 0.585 |
| w7 | 5 | -0.016568 | -2.136 |
| w8 | 9 | 0.188983 | 21.96 |
| w9 | 19 | 0.21109 | 42.04 |
| w10 | 2 | 0.14896 | 1.118 |
| w11 | 7 | 0.0224 | 0.47 |
| w12 | 10 | 0.052721 | 4.234 |
| w13 | 6 | -0.004632 | 0.357 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.072013 | -2.106 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | 0.018891 | 0.172 |
| w18 | 1 | 0.020562 | 0.538 |
| w19 | 7 | 0.033961 | 2.254 |
| w20 | 8 | 0.023916 | 2.608 |
| w21 | 11 | -0.074573 | -4.153 |
| w22 | 1 | -0.02418 | -0.179 |
| w23 | 2 | -0.07019 | -3.035 |
| w24 | 6 | 0.006706 | -3.056 |
| w25 | 0 | None | 0.0 |
| w26 | 6 | 0.059202 | 4.983 |
| w27 | 3 | 0.007076 | -0.366 |
| w28 | 12 | 0.186021 | 20.042 |
| w29 | 0 | 0.023067 | 0.0 |
| w30 | 11 | 0.031679 | 3.539 |
| w31 | 10 | 0.001667 | 1.37 |
| w32 | 6 | -0.016646 | -2.275 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 1 | 0.093859 | 0.845 |
| w11 | 8 | -0.02237 | -1.697 |
| w12 | 8 | -0.010862 | -0.712 |
| w13 | 6 | 0.116316 | 4.405 |
| w14 | 0 | None | 0.0 |
| w15 | 5 | 0.140561 | 6.394 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | 0.053026 | 1.463 |
| w18 | 10 | 0.147466 | 21.826 |
| w19 | 13 | 0.003248 | -0.169 |
| w20 | 9 | 0.034596 | 4.3 |
| w21 | 19 | -0.039068 | -2.754 |
| w22 | 0 | None | 0.0 |
| w23 | 7 | -0.025835 | -2.114 |
| w24 | 6 | 0.028367 | -3.273 |
| w25 | 3 | 0.012104 | 0.48 |
| w26 | 18 | 0.084443 | 8.377 |
| w27 | 1 | -0.038371 | -2.199 |
| w28 | 11 | -0.103085 | -17.322 |
| w29 | 5 | -0.035758 | -3.086 |
| w30 | 14 | -0.067552 | -4.048 |
| w31 | 13 | -0.075221 | -6.105 |
| w32 | 7 | -0.00532 | -1.584 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 6 | -0.008299 | -3.649 |
| w13 | 8 | 0.017597 | 1.913 |
| w14 | 2 | -0.075031 | -5.832 |
| w15 | 5 | -0.026735 | -2.135 |
| w16 | 0 | None | 0.0 |
| w17 | 8 | -0.050878 | -5.099 |
| w18 | 7 | -0.003322 | -4.239 |
| w19 | 3 | 0.052918 | 3.416 |
| w20 | 10 | 0.186509 | 20.311 |
| w21 | 6 | -0.040391 | -2.84 |
| w22 | 3 | 0.074984 | 1.454 |
| w23 | 12 | -0.086179 | -7.241 |
| w24 | 8 | -0.031008 | -10.848 |
| w25 | 5 | 0.008361 | -1.506 |
| w26 | 16 | -0.049931 | -4.786 |
| w27 | 5 | -0.069893 | -7.777 |
| w28 | 11 | -0.011715 | -1.962 |
| w29 | 2 | -0.020787 | -1.234 |
| w30 | 14 | -0.049747 | -3.898 |
| w31 | 8 | -0.116912 | -9.576 |
| w32 | 9 | -0.036361 | -4.541 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 7 | 0.037444 | 0.87 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | -0.074952 | -5.206 |
| w18 | 4 | -0.002058 | -1.936 |
| w19 | 11 | 0.121049 | 9.471 |
| w20 | 12 | 0.007704 | -0.289 |
| w21 | 10 | 0.070898 | 4.709 |
| w22 | 5 | -0.029907 | -3.815 |
| w23 | 14 | 0.026383 | 3.508 |
| w24 | 4 | -0.00109 | -5.405 |
| w25 | 1 | 0.035659 | 0.95 |
| w26 | 18 | 0.071207 | 3.858 |
| w27 | 3 | 0.055329 | 1.944 |
| w28 | 8 | -0.050486 | -4.825 |
| w29 | 5 | -0.006169 | -1.809 |
| w30 | 16 | -0.026734 | -1.795 |
| w31 | 16 | -0.025649 | -5.746 |
| w32 | 11 | -0.059387 | -6.666 |

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
| w15 | 2 | -0.065063 | -3.534 |
| w16 | 0 | None | 0.0 |
| w17 | 8 | -0.133825 | -5.957 |
| w18 | 4 | 0.031914 | 1.828 |
| w19 | 8 | 0.155325 | 9.243 |
| w20 | 3 | -0.091 | -3.274 |
| w21 | 11 | 0.044695 | 2.293 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 2 | 0.015117 | -0.075 |
| w26 | 1 | -0.07441 | -1.043 |
| w27 | 0 | None | 0.0 |
| w28 | 4 | -0.032416 | -1.796 |
| w29 | 0 | None | 0.0 |
| w30 | 10 | 0.031142 | 1.022 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | -0.017096 | 0.0 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 1 | -0.120467 | -8.945 |
| w17 | 10 | 0.011154 | -1.418 |
| w18 | 4 | -0.078432 | -4.703 |
| w19 | 8 | 0.132219 | 7.278 |
| w20 | 11 | -0.013804 | 0.697 |
| w21 | 14 | -0.132537 | -12.901 |
| w22 | 1 | 0.026313 | 0.4 |
| w23 | 7 | -0.02678 | -3.322 |
| w24 | 9 | -0.015592 | -13.539 |
| w25 | 4 | 0.040257 | 1.176 |
| w26 | 16 | -0.113671 | -11.562 |
| w27 | 5 | -0.02517 | -4.198 |
| w28 | 12 | 0.103454 | 7.629 |
| w29 | 6 | -0.049283 | -4.141 |
| w30 | 13 | -0.090583 | -8.53 |
| w31 | 15 | -0.035815 | -3.481 |
| w32 | 14 | 0.137619 | 11.816 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 10 | 0.025005 | 6.561 |
| w21 | 16 | -0.002194 | -0.061 |
| w22 | 3 | 0.032339 | 0.42 |
| w23 | 8 | -0.010852 | -0.314 |
| w24 | 5 | 0.015788 | -5.417 |
| w25 | 4 | 0.069047 | 3.37 |
| w26 | 19 | 0.032547 | 1.662 |
| w27 | 2 | -0.096636 | -1.695 |
| w28 | 13 | 0.100169 | 9.937 |
| w29 | 3 | -0.029694 | -1.678 |
| w30 | 14 | -0.063019 | -3.858 |
| w31 | 11 | -0.056721 | -4.14 |
| w32 | 9 | 0.051762 | 3.452 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 5 | 0.031938 | 0.477 |
| w23 | 11 | -0.157212 | -8.814 |
| w24 | 7 | 0.013512 | -8.734 |
| w25 | 1 | -0.034355 | -1.545 |
| w26 | 6 | 0.074979 | 5.248 |
| w27 | 3 | 0.048307 | 0.956 |
| w28 | 13 | -0.073763 | -6.702 |
| w29 | 3 | -0.071754 | -2.574 |
| w30 | 14 | -0.116981 | -13.019 |
| w31 | 12 | -0.011179 | -0.266 |
| w32 | 5 | 0.114149 | 5.499 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 7 | 0.022778 | -0.573 |
| w25 | 2 | 0.019592 | 0.577 |
| w26 | 17 | 0.064902 | 8.945 |
| w27 | 0 | None | 0.0 |
| w28 | 11 | -0.016543 | -2.981 |
| w29 | 3 | -0.050962 | -1.99 |
| w30 | 16 | -0.069198 | -4.105 |
| w31 | 11 | -0.013726 | 0.217 |
| w32 | 10 | -0.100226 | -8.6 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 6 | 0.048656 | 0.127 |
| w6 | 0 | None | 0.0 |
| w7 | 8 | 0.037048 | 2.323 |
| w8 | 11 | 0.062227 | 6.081 |
| w9 | 15 | 0.165269 | 21.404 |
| w10 | 10 | -0.044647 | -3.176 |
| w11 | 8 | 0.110297 | 6.135 |
| w12 | 16 | 0.064134 | 7.279 |
| w13 | 4 | 0.116602 | 4.882 |
| w14 | 0 | None | 0.0 |
| w15 | 6 | -0.005296 | -0.632 |
| w16 | 0 | None | 0.0 |
| w17 | 8 | 0.145768 | 4.475 |
| w18 | 1 | -0.028359 | -0.666 |
| w19 | 7 | 0.014477 | 0.773 |
| w20 | 10 | 0.264488 | 18.906 |
| w21 | 15 | -0.001022 | 2.41 |
| w22 | 5 | -0.024993 | -1.828 |
| w23 | 5 | 0.059346 | 5.869 |
| w24 | 5 | -0.033785 | -3.258 |
| w25 | 9 | -0.110528 | -9.848 |
| w26 | 8 | 0.062749 | 2.623 |
| w27 | 3 | -0.077609 | -4.603 |
| w28 | 8 | 0.02762 | 1.605 |
| w29 | 4 | -0.047178 | -3.79 |
| w30 | 0 | None | 0.0 |
| w31 | 12 | -0.137821 | -10.61 |
| w32 | 1 | 0.0138 | -0.154 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 0 | None | 0.0 |
| w6 | 4 | 0.035346 | 0.256 |
| w7 | 8 | 0.161976 | 8.762 |
| w8 | 13 | 0.242979 | 20.821 |
| w9 | 11 | 0.079185 | 9.393 |
| w10 | 3 | 0.082232 | 0.56 |
| w11 | 5 | 0.042121 | 1.593 |
| w12 | 15 | 0.029121 | 3.217 |
| w13 | 5 | 0.047648 | 1.412 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | -0.039477 | -1.611 |
| w18 | 4 | -0.005797 | -1.204 |
| w19 | 8 | 0.056018 | 2.455 |
| w20 | 8 | 0.031057 | 0.073 |
| w21 | 4 | 0.039744 | 0.866 |
| w22 | 2 | -0.259714 | -8.847 |
| w23 | 2 | -0.080235 | -4.966 |
| w24 | 3 | -0.049818 | -2.771 |
| w25 | 7 | 0.010478 | 0.589 |
| w26 | 2 | 0.052259 | 0.97 |
| w27 | 2 | -0.024776 | -2.304 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | -0.257257 | -22.399 |
| w30 | 0 | None | 0.0 |
| w31 | 9 | 0.019898 | 0.178 |
| w32 | 3 | 0.060231 | 0.069 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 14 | -0.078667 | -8.4 |
| w18 | 0 | None | 0.0 |
| w19 | 11 | -0.025486 | -1.171 |
| w20 | 9 | -0.171896 | -17.295 |
| w21 | 17 | 0.051999 | 6.348 |
| w22 | 2 | -0.06424 | -2.108 |
| w23 | 6 | 0.193181 | 16.612 |
| w24 | 6 | -0.038127 | -5.574 |
| w25 | 6 | -0.001397 | -2.137 |
| w26 | 15 | 0.147077 | 18.146 |
| w27 | 2 | -0.005051 | -2.296 |
| w28 | 7 | 0.016962 | -0.129 |
| w29 | 4 | -0.014485 | -2.285 |
| w30 | 15 | -0.101106 | -8.535 |
| w31 | 15 | -0.030193 | -2.316 |
| w32 | 5 | -0.062617 | -5.887 |

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
| w17 | 10 | -0.050859 | -3.609 |
| w18 | 10 | -0.092862 | -11.175 |
| w19 | 11 | 0.088614 | 7.248 |
| w20 | 8 | -0.059643 | -3.897 |
| w21 | 12 | 0.031582 | 2.772 |
| w22 | 6 | 0.039078 | 0.586 |
| w23 | 7 | -0.054045 | -5.162 |
| w24 | 4 | 0.034215 | -0.433 |
| w25 | 2 | -0.005026 | -0.397 |
| w26 | 6 | 0.034279 | 0.157 |
| w27 | 0 | None | 0.0 |
| w28 | 9 | 0.060979 | 5.021 |
| w29 | 1 | -0.006165 | -0.107 |
| w30 | 13 | -0.088728 | -7.649 |
| w31 | 16 | -0.06631 | -5.745 |
| w32 | 9 | 0.082555 | 4.658 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 11 | 0.07284 | 7.927 |
| w20 | 13 | 0.122567 | 17.924 |
| w21 | 5 | 0.062681 | 2.322 |
| w22 | 1 | -0.012228 | -0.82 |
| w23 | 3 | 0.029242 | 0.728 |
| w24 | 5 | 0.040912 | -2.295 |
| w25 | 3 | 0.071283 | 2.983 |
| w26 | 11 | 0.095393 | 6.441 |
| w27 | 3 | 0.047027 | 0.828 |
| w28 | 15 | -0.043322 | -4.352 |
| w29 | 2 | -0.027944 | -0.746 |
| w30 | 16 | 0.030861 | 6.035 |
| w31 | 16 | -0.074301 | -6.976 |
| w32 | 3 | -0.179152 | -14.722 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 2 | 0.043693 | 1.436 |
| w23 | 9 | 0.048732 | 1.901 |
| w24 | 5 | -0.029951 | -6.482 |
| w25 | 3 | 0.066439 | 3.23 |
| w26 | 12 | 0.053173 | 3.454 |
| w27 | 4 | 0.039203 | 0.987 |
| w28 | 8 | 0.109344 | 9.433 |
| w29 | 5 | -0.213977 | -11.097 |
| w30 | 14 | 0.000891 | 0.698 |
| w31 | 14 | 0.005096 | 0.053 |
| w32 | 4 | 0.087561 | 3.207 |

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
| w27 | 2 | 0.044853 | 0.633 |
| w28 | 12 | -0.003199 | -0.647 |
| w29 | 5 | -0.096793 | -4.238 |
| w30 | 14 | -0.042439 | -0.903 |
| w31 | 15 | -0.087434 | -7.102 |
| w32 | 3 | -0.302832 | -12.167 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 12 | -0.113045 | -6.323 |
| w18 | 13 | -0.041701 | -4.902 |
| w19 | 11 | 0.034243 | 3.069 |
| w20 | 9 | 0.131436 | 12.103 |
| w21 | 13 | -0.016773 | -1.402 |
| w22 | 2 | 0.024692 | 0.328 |
| w23 | 9 | -0.030447 | -2.888 |
| w24 | 6 | 0.020653 | -4.306 |
| w25 | 2 | 0.064579 | 1.366 |
| w26 | 14 | 0.127343 | 11.291 |
| w27 | 3 | 0.016722 | 0.588 |
| w28 | 11 | -0.084863 | -6.242 |
| w29 | 4 | -0.059281 | -3.302 |
| w30 | 14 | -0.110178 | -17.842 |
| w31 | 14 | 0.014934 | 0.191 |
| w32 | 11 | -0.004714 | -1.591 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 14 | 0.183779 | 17.981 |
| w18 | 4 | -0.113225 | -3.958 |
| w19 | 13 | 0.043955 | 3.055 |
| w20 | 9 | -0.112881 | -8.584 |
| w21 | 13 | -0.087078 | -8.09 |
| w22 | 3 | -0.030415 | -2.597 |
| w23 | 6 | -0.061679 | -4.493 |
| w24 | 8 | -0.036786 | -12.752 |
| w25 | 0 | None | 0.0 |
| w26 | 16 | 0.109686 | 9.965 |
| w27 | 4 | -0.081126 | -3.577 |
| w28 | 11 | -0.001281 | 0.138 |
| w29 | 3 | -0.046925 | -2.196 |
| w30 | 16 | -0.025013 | -1.45 |
| w31 | 17 | 0.003675 | -0.324 |
| w32 | 13 | 0.020912 | 1.385 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 18 | 0.076419 | 6.799 |
| w29 | 2 | 0.006069 | 0.029 |
| w30 | 6 | 0.000819 | 1.001 |
| w31 | 8 | -0.060905 | -6.452 |
| w32 | 11 | 0.069871 | 4.696 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 0 | None | 0.0 |
| w15 | 5 | 0.051446 | 1.741 |
| w16 | 0 | None | 0.0 |
| w17 | 6 | -0.079731 | -3.54 |
| w18 | 5 | 0.001969 | 0.467 |
| w19 | 11 | 0.013644 | 1.073 |
| w20 | 9 | -0.186128 | -11.747 |
| w21 | 8 | 0.007949 | -1.638 |
| w22 | 2 | -0.139856 | -7.752 |
| w23 | 4 | 0.155741 | 8.895 |
| w24 | 8 | 0.008782 | -2.102 |
| w25 | 2 | -0.020744 | -1.487 |
| w26 | 14 | -0.10939 | -10.164 |
| w27 | 2 | -0.051772 | -2.261 |
| w28 | 13 | 0.002901 | 1.915 |
| w29 | 4 | -0.023395 | -1.301 |
| w30 | 15 | 0.007057 | 3.573 |
| w31 | 12 | -0.025393 | -2.546 |
| w32 | 11 | -0.144082 | -12.034 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 5 | 0.032322 | -0.878 |
| w26 | 6 | 0.065355 | 2.808 |
| w27 | 3 | -0.012951 | -1.461 |
| w28 | 14 | 0.024995 | 2.11 |
| w29 | 1 | -0.037326 | -1.668 |
| w30 | 18 | -0.048185 | -3.905 |
| w31 | 9 | -0.026298 | -2.662 |
| w32 | 8 | -0.070193 | -8.343 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

