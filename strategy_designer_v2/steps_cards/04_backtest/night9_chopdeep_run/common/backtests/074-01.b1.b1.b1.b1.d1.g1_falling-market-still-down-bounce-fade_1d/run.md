# Backtest of 074-01.b1.b1.b1.b1.d1.g1_falling-market-still-down-bounce-fade_1d

- Plan: `../../../../../03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1.b1.d1.g1_falling-market-still-down-bounce-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.03738 | -0.725 |
| w2 | 3 | 0.051444 | 0.246 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 12 | 0.128886 | 7.213 |
| w8 | 8 | 0.14836 | 12.295 |
| w9 | 16 | 0.17981 | 41.036 |
| w10 | 5 | 0.069063 | 0.762 |
| w11 | 1 | None | -0.025 |
| w12 | 19 | 0.007703 | 1.738 |
| w13 | 9 | 0.123148 | 6.731 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 16 | 0.216989 | 23.548 |
| w18 | 5 | -0.049665 | -3.405 |
| w19 | 11 | -0.031352 | -2.974 |
| w20 | 14 | 0.127636 | 16.183 |
| w21 | 16 | 0.08031 | 5.474 |
| w22 | 0 | 0.006236 | 0.0 |
| w23 | 5 | -0.034346 | -3.713 |
| w24 | 4 | 0.011992 | -1.586 |
| w25 | 0 | None | 0.0 |
| w26 | 4 | -0.017167 | -1.522 |
| w27 | 0 | None | 0.0 |
| w28 | 6 | 0.048237 | 2.068 |
| w29 | 0 | None | 0.0 |
| w30 | 8 | 0.041144 | 3.385 |
| w31 | 13 | 0.033865 | 5.219 |
| w32 | 8 | 0.053546 | 2.271 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.107796 | -2.344 |
| w2 | 4 | 0.035187 | 0.72 |
| w3 | 0 | None | 0.0 |
| w4 | 1 | -0.039299 | -1.736 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | 0.030564 | 0.0 |
| w7 | 13 | 0.039367 | 2.554 |
| w8 | 15 | 0.245483 | 29.921 |
| w9 | 18 | 0.269535 | 48.507 |
| w10 | 2 | 0.130347 | 3.158 |
| w11 | 8 | 0.002448 | -0.92 |
| w12 | 21 | -0.008187 | -0.17 |
| w13 | 8 | 0.123142 | 5.507 |
| w14 | 2 | -0.002399 | -0.637 |
| w15 | 3 | 0.034029 | 0.483 |
| w16 | 0 | None | 0.0 |
| w17 | 10 | 0.08741 | 2.368 |
| w18 | 2 | 0.062253 | 0.942 |
| w19 | 15 | 0.039402 | 2.98 |
| w20 | 16 | 0.059253 | 9.356 |
| w21 | 5 | 0.048641 | 0.935 |
| w22 | 0 | None | 0.0 |
| w23 | 6 | -0.043796 | -3.091 |
| w24 | 11 | -0.04633 | -3.655 |
| w25 | 0 | None | 0.0 |
| w26 | 16 | 0.080848 | 8.67 |
| w27 | 2 | -0.011802 | -1.284 |
| w28 | 9 | 0.103255 | 7.836 |
| w29 | 1 | -0.08089 | -0.724 |
| w30 | 14 | -0.072398 | -5.468 |
| w31 | 16 | -0.021228 | 0.017 |
| w32 | 9 | 0.030897 | 2.302 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 1 | -0.005772 | -0.467 |
| w7 | 9 | -0.018792 | -0.635 |
| w8 | 18 | 0.02935 | 6.935 |
| w9 | 10 | 0.002644 | -2.7 |
| w10 | 7 | 0.03691 | 1.364 |
| w11 | 11 | -0.070282 | -6.905 |
| w12 | 14 | 0.113056 | 11.969 |
| w13 | 7 | 0.184607 | 9.702 |
| w14 | 3 | 0.031229 | 0.871 |
| w15 | 4 | 0.001568 | -0.285 |
| w16 | 2 | 0.040641 | 0.297 |
| w17 | 12 | 0.099461 | 3.556 |
| w18 | 7 | 0.014545 | 1.676 |
| w19 | 12 | 0.043619 | 5.63 |
| w20 | 5 | -2e-05 | 12.416 |
| w21 | 6 | 0.020541 | 0.352 |
| w22 | 1 | 0.038604 | 0.18 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | -0.036236 | -2.736 |
| w25 | 9 | 0.040274 | 2.76 |
| w26 | 9 | 0.128976 | 11.709 |
| w27 | 2 | 0.065934 | 3.797 |
| w28 | 9 | 0.064473 | 1.989 |
| w29 | 0 | None | 0.0 |
| w30 | 19 | -0.079971 | -5.882 |
| w31 | 15 | 0.057488 | 4.445 |
| w32 | 18 | 0.061608 | 4.913 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 11 | 0.093317 | 4.319 |
| w8 | 15 | 0.052611 | 2.123 |
| w9 | 18 | 0.015557 | 3.898 |
| w10 | 5 | 0.098914 | 1.298 |
| w11 | 7 | -0.018455 | -4.36 |
| w12 | 12 | 0.080284 | 5.322 |
| w13 | 6 | 0.099203 | 4.25 |
| w14 | 2 | -0.012719 | -1.429 |
| w15 | 5 | 0.020116 | 0.126 |
| w16 | 0 | None | 0.0 |
| w17 | 7 | 0.118447 | 3.58 |
| w18 | 8 | 0.008828 | 0.132 |
| w19 | 17 | 0.013032 | -1.09 |
| w20 | 22 | 0.177726 | 21.762 |
| w21 | 12 | -0.01208 | -1.608 |
| w22 | 4 | -0.021769 | -1.929 |
| w23 | 4 | 0.061303 | 3.758 |
| w24 | 5 | 0.059109 | 0.916 |
| w25 | 0 | None | 0.0 |
| w26 | 13 | 0.130165 | 11.141 |
| w27 | 2 | -0.131508 | -2.449 |
| w28 | 21 | -0.076628 | -9.089 |
| w29 | 0 | None | 0.0 |
| w30 | 8 | 0.027125 | -0.218 |
| w31 | 8 | -0.07538 | -7.56 |
| w32 | 12 | 0.168222 | 33.984 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 6 | -0.052939 | -2.386 |
| w3 | 15 | 0.041224 | 7.204 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | 0.01714 | -0.088 |
| w6 | 0 | None | 0.0 |
| w7 | 8 | 0.040868 | 2.139 |
| w8 | 18 | 0.109235 | 15.595 |
| w9 | 18 | 0.196052 | 42.847 |
| w10 | 3 | 0.203379 | 2.726 |
| w11 | 8 | -0.006106 | -0.999 |
| w12 | 15 | 0.038305 | 4.513 |
| w13 | 6 | 0.043904 | 1.089 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.045403 | -1.034 |
| w16 | 0 | None | 0.0 |
| w17 | 7 | 0.095264 | 2.385 |
| w18 | 1 | 0.020562 | 0.841 |
| w19 | 12 | -0.060391 | -5.31 |
| w20 | 17 | -0.013946 | -1.603 |
| w21 | 11 | 0.034936 | 2.35 |
| w22 | 0 | -0.02418 | 0.0 |
| w23 | 4 | -0.048463 | -2.087 |
| w24 | 11 | -0.001437 | -3.982 |
| w25 | 0 | None | 0.0 |
| w26 | 14 | 0.048757 | 5.01 |
| w27 | 5 | -0.051382 | -2.722 |
| w28 | 15 | 0.051378 | 8.098 |
| w29 | 0 | None | 0.0 |
| w30 | 16 | -0.032424 | -1.149 |
| w31 | 14 | -0.020229 | 0.767 |
| w32 | 6 | 0.019668 | 0.973 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 1 | 0.07901 | 0.995 |
| w11 | 13 | -0.075788 | -6.427 |
| w12 | 13 | 0.067644 | 5.574 |
| w13 | 5 | 0.147486 | 6.772 |
| w14 | 0 | None | 0.0 |
| w15 | 10 | -0.008149 | -4.698 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | 0.078961 | 1.313 |
| w18 | 16 | 0.106093 | 19.3 |
| w19 | 17 | -0.007886 | -0.809 |
| w20 | 19 | -0.075188 | -5.155 |
| w21 | 23 | -0.050076 | -5.245 |
| w22 | 1 | -0.029478 | -0.64 |
| w23 | 11 | 0.132251 | 16.0 |
| w24 | 8 | 0.034841 | -2.913 |
| w25 | 3 | 0.021816 | 0.881 |
| w26 | 17 | 0.182426 | 18.447 |
| w27 | 5 | -0.043517 | -4.135 |
| w28 | 16 | 0.001045 | -2.84 |
| w29 | 4 | -0.005795 | -0.544 |
| w30 | 18 | -0.066759 | -3.139 |
| w31 | 15 | -0.039405 | -3.336 |
| w32 | 9 | 0.008681 | -1.499 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 8 | 0.050511 | 0.188 |
| w13 | 6 | 0.069381 | 7.387 |
| w14 | 3 | -0.059383 | -5.111 |
| w15 | 9 | -0.028971 | -3.723 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | 0.139732 | 6.885 |
| w18 | 9 | 0.05437 | 2.207 |
| w19 | 12 | 0.053377 | 3.183 |
| w20 | 17 | 0.024943 | 2.738 |
| w21 | 9 | 0.102416 | 5.103 |
| w22 | 9 | 0.07179 | 1.688 |
| w23 | 20 | -0.093556 | -10.152 |
| w24 | 14 | -0.045585 | -15.254 |
| w25 | 5 | 0.023036 | -0.425 |
| w26 | 21 | -0.031857 | -2.155 |
| w27 | 4 | -0.05513 | -4.112 |
| w28 | 17 | -0.04783 | -4.493 |
| w29 | 1 | -0.11181 | -0.591 |
| w30 | 25 | -0.086967 | -6.939 |
| w31 | 12 | -0.059953 | -4.701 |
| w32 | 8 | 0.060641 | 1.639 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 6 | 0.063676 | 1.722 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | -0.031144 | -1.945 |
| w18 | 6 | 0.080785 | 5.963 |
| w19 | 24 | 0.028159 | 5.809 |
| w20 | 22 | -0.080004 | -7.408 |
| w21 | 10 | 0.072362 | 4.484 |
| w22 | 7 | -0.160407 | -11.142 |
| w23 | 21 | -0.031422 | 0.481 |
| w24 | 9 | -0.03459 | -11.435 |
| w25 | 3 | 0.012852 | -0.412 |
| w26 | 18 | 0.073911 | 5.818 |
| w27 | 4 | 0.011603 | -2.782 |
| w28 | 16 | -0.038852 | -3.518 |
| w29 | 5 | -0.161322 | -7.552 |
| w30 | 20 | 0.003022 | 2.433 |
| w31 | 18 | -0.095179 | -11.396 |
| w32 | 12 | -0.023676 | -3.177 |

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
| w15 | 3 | -0.039461 | -1.63 |
| w16 | 1 | -0.010493 | -0.99 |
| w17 | 12 | -0.107692 | -3.673 |
| w18 | 7 | 0.035211 | 1.645 |
| w19 | 13 | 0.047421 | 4.314 |
| w20 | 2 | -0.089218 | -1.914 |
| w21 | 11 | 0.046589 | 2.513 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 4 | 0.086268 | 3.544 |
| w26 | 1 | -0.07441 | -0.722 |
| w27 | 0 | None | 0.0 |
| w28 | 4 | -0.044366 | -1.849 |
| w29 | 0 | None | 0.0 |
| w30 | 13 | 0.037272 | 2.264 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 1 | -0.120467 | -7.638 |
| w17 | 11 | 0.202123 | 13.672 |
| w18 | 4 | 0.020848 | 0.316 |
| w19 | 12 | 0.041376 | 2.621 |
| w20 | 19 | -0.059421 | -6.192 |
| w21 | 17 | -0.01994 | -5.154 |
| w22 | 2 | 0.010764 | -0.209 |
| w23 | 10 | -0.064668 | -5.371 |
| w24 | 13 | -0.005738 | -14.062 |
| w25 | 3 | 0.018246 | 0.304 |
| w26 | 17 | -0.184418 | -17.512 |
| w27 | 6 | -0.022668 | -4.708 |
| w28 | 17 | -0.010847 | -1.049 |
| w29 | 5 | -0.078092 | -3.08 |
| w30 | 16 | -0.095006 | -7.877 |
| w31 | 20 | -0.062919 | -4.27 |
| w32 | 14 | 0.138698 | 11.732 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 18 | 0.072093 | 16.341 |
| w21 | 17 | 0.193676 | 16.755 |
| w22 | 3 | -0.016069 | -2.339 |
| w23 | 13 | 0.030973 | 4.404 |
| w24 | 8 | 0.038678 | -3.81 |
| w25 | 5 | 0.081501 | 3.436 |
| w26 | 19 | 0.029008 | 0.797 |
| w27 | 2 | -0.020409 | -0.187 |
| w28 | 22 | -0.002377 | 0.41 |
| w29 | 1 | -0.019588 | 0.228 |
| w30 | 18 | -0.175332 | -12.517 |
| w31 | 12 | -0.057424 | -3.091 |
| w32 | 8 | -0.045066 | -3.033 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 6 | 0.024715 | -0.098 |
| w23 | 13 | -0.029645 | -0.709 |
| w24 | 12 | 0.044875 | -5.215 |
| w25 | 2 | -0.174086 | -3.891 |
| w26 | 13 | -0.002567 | -0.512 |
| w27 | 4 | 0.07259 | 0.956 |
| w28 | 22 | -0.035522 | -2.65 |
| w29 | 3 | 0.010513 | 0.34 |
| w30 | 17 | -0.157566 | -14.931 |
| w31 | 9 | -0.005184 | 0.24 |
| w32 | 6 | 0.082624 | 1.903 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 11 | 0.009504 | -3.582 |
| w25 | 4 | 0.012318 | -0.283 |
| w26 | 17 | -0.024078 | -3.3 |
| w27 | 0 | None | 0.0 |
| w28 | 15 | 0.046856 | 2.917 |
| w29 | 1 | -0.12346 | -1.787 |
| w30 | 20 | -0.0354 | 0.246 |
| w31 | 11 | 0.003049 | 1.211 |
| w32 | 10 | -0.061903 | -3.224 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 2 | 0.061246 | 1.26 |
| w6 | 0 | -0.080217 | 0.0 |
| w7 | 10 | 0.02544 | 1.685 |
| w8 | 15 | -0.070651 | -5.522 |
| w9 | 19 | 0.208148 | 34.081 |
| w10 | 11 | 0.114225 | 1.349 |
| w11 | 8 | 0.010701 | -0.373 |
| w12 | 24 | -0.074027 | -7.219 |
| w13 | 4 | 0.106733 | 4.026 |
| w14 | 0 | None | 0.0 |
| w15 | 8 | 0.053208 | 2.416 |
| w16 | 0 | None | 0.0 |
| w17 | 13 | 0.068284 | 3.525 |
| w18 | 1 | -0.053647 | -0.88 |
| w19 | 12 | -0.144788 | -11.895 |
| w20 | 20 | 0.076287 | 6.382 |
| w21 | 15 | -0.055255 | -4.074 |
| w22 | 7 | -0.015925 | -1.438 |
| w23 | 12 | 0.133075 | 21.047 |
| w24 | 5 | -0.005199 | -1.167 |
| w25 | 8 | -0.096263 | -5.181 |
| w26 | 5 | 0.030724 | 1.348 |
| w27 | 2 | -0.045932 | -1.879 |
| w28 | 11 | -0.091258 | -6.281 |
| w29 | 5 | 0.01705 | 0.066 |
| w30 | 0 | None | 0.0 |
| w31 | 17 | -0.094523 | -6.909 |
| w32 | 2 | -0.006169 | -0.306 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 0 | None | 0.0 |
| w6 | 0 | 0.005413 | 0.0 |
| w7 | 15 | 0.171933 | 10.314 |
| w8 | 24 | 0.080953 | 8.75 |
| w9 | 20 | 0.243326 | 56.054 |
| w10 | 5 | 0.053721 | 0.673 |
| w11 | 5 | 0.030903 | 0.683 |
| w12 | 17 | 0.010595 | 1.725 |
| w13 | 6 | 0.160115 | 7.975 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 7 | 0.063089 | 2.571 |
| w18 | 7 | 0.035971 | 2.275 |
| w19 | 9 | 0.10709 | 7.488 |
| w20 | 13 | 0.012194 | -2.074 |
| w21 | 6 | 0.061142 | 2.363 |
| w22 | 3 | -0.216011 | -10.102 |
| w23 | 5 | -0.111176 | -9.605 |
| w24 | 6 | -0.048184 | -4.888 |
| w25 | 11 | 0.01397 | -2.121 |
| w26 | 2 | 0.073222 | 0.497 |
| w27 | 2 | 0.014908 | 0.226 |
| w28 | 0 | None | 0.0 |
| w29 | 6 | -0.05689 | -7.32 |
| w30 | 1 | -0.006203 | -0.216 |
| w31 | 10 | -0.01703 | -1.498 |
| w32 | 5 | -0.00465 | -0.854 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 12 | 0.163292 | 7.985 |
| w18 | 0 | None | 0.0 |
| w19 | 14 | 0.027219 | 2.948 |
| w20 | 13 | -0.084289 | -9.979 |
| w21 | 18 | 0.049496 | 3.315 |
| w22 | 3 | 0.011459 | -0.571 |
| w23 | 13 | 0.116088 | 13.57 |
| w24 | 7 | -0.021033 | -4.367 |
| w25 | 8 | 0.011495 | -0.827 |
| w26 | 15 | 0.074001 | 12.648 |
| w27 | 3 | -0.01674 | -3.565 |
| w28 | 12 | -0.002326 | -0.577 |
| w29 | 5 | -0.05727 | -3.096 |
| w30 | 21 | -0.124239 | -11.081 |
| w31 | 17 | -0.038883 | -2.138 |
| w32 | 5 | -0.07421 | -7.381 |

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
| w17 | 9 | 0.090813 | 3.312 |
| w18 | 15 | 0.040594 | 4.184 |
| w19 | 10 | 0.065208 | 5.174 |
| w20 | 10 | -0.021907 | -1.06 |
| w21 | 17 | 0.170615 | 14.301 |
| w22 | 7 | 0.01139 | 0.01 |
| w23 | 11 | 0.09297 | 10.521 |
| w24 | 4 | 0.008921 | -2.775 |
| w25 | 4 | -0.024584 | -0.516 |
| w26 | 6 | -0.043395 | -2.904 |
| w27 | 0 | None | 0.0 |
| w28 | 18 | 0.086149 | 8.436 |
| w29 | 0 | None | 0.0 |
| w30 | 17 | -0.11499 | -10.566 |
| w31 | 16 | -0.092072 | -8.063 |
| w32 | 9 | 0.102241 | 5.465 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 12 | 0.030861 | 4.723 |
| w20 | 15 | 0.152889 | 24.429 |
| w21 | 5 | 0.052433 | 1.564 |
| w22 | 0 | -0.012228 | 0.0 |
| w23 | 2 | 0.045097 | 0.807 |
| w24 | 6 | 0.022483 | -4.17 |
| w25 | 6 | 0.011543 | -0.464 |
| w26 | 12 | 0.096105 | 6.694 |
| w27 | 1 | 0.130381 | 0.799 |
| w28 | 19 | -0.027448 | -2.48 |
| w29 | 2 | -0.23324 | -4.636 |
| w30 | 17 | 0.03698 | 8.245 |
| w31 | 18 | -0.026624 | -2.861 |
| w32 | 2 | -0.231155 | -18.099 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 3 | 0.032727 | 0.279 |
| w23 | 14 | 0.115428 | 5.634 |
| w24 | 14 | -0.00814 | -8.19 |
| w25 | 3 | 0.049359 | 1.88 |
| w26 | 13 | 0.111921 | 9.913 |
| w27 | 6 | -0.015249 | -1.617 |
| w28 | 14 | 0.114186 | 7.808 |
| w29 | 4 | -0.244849 | -10.555 |
| w30 | 18 | -0.065298 | -5.035 |
| w31 | 17 | 0.039643 | 4.076 |
| w32 | 3 | -0.001899 | -0.766 |

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
| w27 | 6 | 0.047047 | -0.012 |
| w28 | 14 | 0.020343 | 1.608 |
| w29 | 3 | -0.036177 | -1.041 |
| w30 | 21 | 0.002597 | 5.434 |
| w31 | 18 | -0.032355 | -1.707 |
| w32 | 3 | -0.154845 | -2.591 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 10 | -0.153984 | -6.79 |
| w18 | 12 | 0.025057 | 4.577 |
| w19 | 16 | 0.016711 | 1.869 |
| w20 | 18 | 0.089769 | 13.048 |
| w21 | 14 | 0.020189 | 1.636 |
| w22 | 2 | 0.029776 | 0.454 |
| w23 | 14 | -0.042646 | -3.798 |
| w24 | 8 | -0.024717 | -9.84 |
| w25 | 1 | 0.037254 | 0.219 |
| w26 | 15 | 0.125544 | 10.667 |
| w27 | 4 | -0.030453 | -2.559 |
| w28 | 18 | -0.073524 | -5.492 |
| w29 | 3 | -0.08302 | -2.066 |
| w30 | 19 | -0.128179 | -22.411 |
| w31 | 17 | 0.041182 | 3.634 |
| w32 | 13 | -0.003291 | -2.353 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 14 | 0.192532 | 14.589 |
| w18 | 3 | -0.05439 | -1.884 |
| w19 | 16 | 0.083827 | 8.498 |
| w20 | 24 | 0.068512 | 8.073 |
| w21 | 14 | 0.039759 | 2.997 |
| w22 | 2 | 0.024802 | 0.502 |
| w23 | 13 | -0.002429 | -0.895 |
| w24 | 13 | -0.018297 | -14.401 |
| w25 | 0 | None | 0.0 |
| w26 | 16 | 0.099599 | 8.764 |
| w27 | 3 | -0.040376 | -1.955 |
| w28 | 17 | 0.063953 | 6.847 |
| w29 | 4 | -0.016764 | -0.449 |
| w30 | 27 | -0.056104 | -1.675 |
| w31 | 20 | 0.006806 | -0.021 |
| w32 | 13 | 0.058365 | 4.378 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 16 | 0.072522 | 5.695 |
| w29 | 2 | -0.171511 | -3.704 |
| w30 | 9 | 0.031551 | 3.286 |
| w31 | 10 | 0.062387 | 3.863 |
| w32 | 12 | 0.110015 | 6.627 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 0 | None | 0.0 |
| w15 | 13 | 0.053412 | 2.873 |
| w16 | 0 | None | 0.0 |
| w17 | 8 | -0.168603 | -6.586 |
| w18 | 7 | 0.07595 | 6.312 |
| w19 | 15 | 0.011687 | 0.758 |
| w20 | 16 | -0.053431 | -3.086 |
| w21 | 9 | -0.001605 | -1.611 |
| w22 | 4 | -0.147169 | -7.89 |
| w23 | 8 | 0.06124 | 4.308 |
| w24 | 8 | -0.01643 | -3.679 |
| w25 | 2 | -0.031445 | -0.797 |
| w26 | 17 | -0.035153 | -3.233 |
| w27 | 6 | -0.005741 | -1.369 |
| w28 | 19 | 0.047645 | 8.433 |
| w29 | 2 | -0.195522 | -4.384 |
| w30 | 15 | -0.049725 | -1.737 |
| w31 | 11 | -0.021627 | -1.566 |
| w32 | 14 | -0.09401 | -7.994 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 5 | 0.005894 | -2.635 |
| w26 | 8 | 0.079161 | 3.541 |
| w27 | 4 | -0.043205 | -2.301 |
| w28 | 23 | 0.020372 | 2.204 |
| w29 | 1 | -0.038296 | -1.296 |
| w30 | 24 | -0.054163 | -3.706 |
| w31 | 14 | 0.009217 | -0.684 |
| w32 | 6 | -0.023572 | -2.923 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

