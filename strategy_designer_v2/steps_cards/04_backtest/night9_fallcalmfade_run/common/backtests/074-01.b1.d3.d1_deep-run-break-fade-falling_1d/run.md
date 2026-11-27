# Backtest of 074-01.b1.d3.d1_deep-run-break-fade-falling_1d

- Plan: `../../../../../03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.d3.d1_deep-run-break-fade-falling_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | -0.006765 | 0.0 |
| w2 | 1 | 0.04302 | 0.159 |
| w3 | 1 | -0.194109 | -0.8 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 7 | 0.169838 | 13.584 |
| w8 | 5 | 0.142162 | 10.525 |
| w9 | 6 | 0.267803 | 35.315 |
| w10 | 1 | 0.035379 | 0.277 |
| w11 | 0 | None | 0.0 |
| w12 | 9 | 0.001441 | 0.466 |
| w13 | 1 | -0.015941 | -0.241 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | 0.211911 | 9.465 |
| w18 | 3 | -0.029642 | -1.922 |
| w19 | 6 | 0.057572 | 4.841 |
| w20 | 9 | 0.14792 | 14.617 |
| w21 | 9 | 0.046053 | 2.834 |
| w22 | 0 | 0.006236 | 0.0 |
| w23 | 0 | -0.001944 | 0.0 |
| w24 | 2 | -0.010449 | -1.959 |
| w25 | 0 | None | 0.0 |
| w26 | 1 | 0.058828 | 2.749 |
| w27 | 0 | None | 0.0 |
| w28 | 3 | -0.001035 | -0.318 |
| w29 | 0 | None | 0.0 |
| w30 | 4 | 0.002895 | 0.475 |
| w31 | 6 | 0.031481 | 5.072 |
| w32 | 4 | -0.01776 | -1.281 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | 0.01345 | 0.0 |
| w2 | 4 | -0.028311 | -1.38 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | -0.034925 | -5.348 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.028951 | -0.309 |
| w7 | 4 | 0.041515 | 2.113 |
| w8 | 12 | 0.20647 | 27.31 |
| w9 | 8 | 0.146309 | 16.916 |
| w10 | 1 | 0.122608 | 1.024 |
| w11 | 3 | -0.009853 | -1.192 |
| w12 | 8 | -0.033775 | -3.293 |
| w13 | 3 | 0.127385 | 4.115 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.007368 | -0.934 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | -0.059543 | -3.603 |
| w18 | 1 | 0.017634 | 0.751 |
| w19 | 7 | 0.090349 | 7.046 |
| w20 | 5 | 0.030952 | 5.007 |
| w21 | 1 | 0.077439 | 0.347 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.047865 | -1.808 |
| w24 | 6 | -0.011124 | -1.873 |
| w25 | 0 | None | 0.0 |
| w26 | 6 | 0.113112 | 10.143 |
| w27 | 1 | -0.023316 | -1.133 |
| w28 | 4 | 0.040876 | 2.862 |
| w29 | 1 | 0.063758 | 1.043 |
| w30 | 9 | -0.025835 | -1.663 |
| w31 | 10 | 0.032774 | 3.958 |
| w32 | 4 | 0.034402 | 2.468 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 0 | -0.01699 | 0.0 |
| w7 | 6 | -0.059599 | -5.587 |
| w8 | 8 | -0.003709 | 3.512 |
| w9 | 9 | 0.081392 | 6.761 |
| w10 | 5 | 0.077502 | 3.197 |
| w11 | 6 | -0.040302 | -3.633 |
| w12 | 6 | 0.105309 | 7.782 |
| w13 | 3 | 0.142325 | 5.234 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.004017 | -1.254 |
| w16 | 0 | -0.029333 | 0.0 |
| w17 | 3 | -0.034976 | -1.755 |
| w18 | 4 | 0.016204 | 1.287 |
| w19 | 5 | 0.070231 | 5.26 |
| w20 | 4 | -0.168782 | 12.29 |
| w21 | 3 | 0.046327 | 2.412 |
| w22 | 0 | 0.038604 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | -0.008343 | -1.148 |
| w25 | 5 | 0.051956 | 4.787 |
| w26 | 4 | 0.143497 | 12.613 |
| w27 | 1 | 0.112248 | 2.368 |
| w28 | 2 | 0.075303 | 2.638 |
| w29 | 1 | 0.010489 | 0.01 |
| w30 | 12 | -0.06695 | -4.964 |
| w31 | 7 | 0.064345 | 5.729 |
| w32 | 6 | -0.001096 | -1.131 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 7 | 0.044917 | 1.244 |
| w8 | 6 | 0.088043 | 8.229 |
| w9 | 6 | 0.001828 | 1.746 |
| w10 | 2 | 0.058274 | 1.032 |
| w11 | 5 | 0.119761 | 2.896 |
| w12 | 7 | -0.187957 | -18.095 |
| w13 | 4 | 0.060581 | 1.242 |
| w14 | 2 | -0.025428 | -1.855 |
| w15 | 2 | 0.000611 | -0.539 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | -0.021507 | -2.037 |
| w18 | 6 | -0.055823 | -3.923 |
| w19 | 7 | 0.153291 | 11.7 |
| w20 | 8 | 0.19001 | 18.969 |
| w21 | 6 | -0.010743 | -0.884 |
| w22 | 1 | 0.068995 | 2.523 |
| w23 | 1 | 0.063466 | 4.914 |
| w24 | 1 | 0.058457 | 1.384 |
| w25 | 0 | None | 0.0 |
| w26 | 9 | 0.133351 | 13.04 |
| w27 | 1 | -0.085641 | -3.459 |
| w28 | 5 | -0.110976 | -8.928 |
| w29 | 0 | None | 0.0 |
| w30 | 3 | 0.021778 | -0.175 |
| w31 | 7 | -0.0476 | -5.7 |
| w32 | 8 | 0.146029 | 16.576 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 2 | -0.113846 | -4.543 |
| w3 | 6 | 0.071046 | 8.062 |
| w4 | 0 | -0.003206 | 0.0 |
| w5 | 0 | 0.033407 | 0.0 |
| w6 | 0 | 0.044999 | 0.0 |
| w7 | 3 | 0.043892 | 2.956 |
| w8 | 7 | 0.204675 | 25.198 |
| w9 | 8 | 0.177566 | 27.101 |
| w10 | 2 | 0.112039 | 1.042 |
| w11 | 5 | 0.045821 | 2.261 |
| w12 | 7 | 0.078745 | 5.359 |
| w13 | 1 | -0.039899 | -0.469 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.065818 | -1.908 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | 0.002216 | -0.142 |
| w18 | 1 | 0.020562 | 0.86 |
| w19 | 5 | 0.041113 | 2.868 |
| w20 | 5 | 0.068206 | 5.117 |
| w21 | 5 | -0.022025 | -0.932 |
| w22 | 0 | -0.02418 | 0.0 |
| w23 | 2 | -0.097408 | -2.719 |
| w24 | 4 | 0.000426 | -2.804 |
| w25 | 0 | None | 0.0 |
| w26 | 5 | 0.041527 | 4.436 |
| w27 | 2 | -0.024492 | -1.52 |
| w28 | 7 | 0.259707 | 24.083 |
| w29 | 0 | 0.021792 | 0.0 |
| w30 | 7 | 0.01804 | 2.605 |
| w31 | 5 | 0.053335 | 5.181 |
| w32 | 2 | 0.001712 | 0.055 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 1 | 0.07905 | 1.255 |
| w11 | 5 | -0.064658 | -3.784 |
| w12 | 6 | -0.055084 | -4.197 |
| w13 | 2 | 0.1207 | 3.961 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | 0.12808 | 6.038 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.051187 | 1.904 |
| w18 | 7 | 0.137749 | 18.084 |
| w19 | 9 | 0.052833 | 3.337 |
| w20 | 7 | 0.029229 | 4.714 |
| w21 | 8 | -0.000134 | 0.623 |
| w22 | 0 | None | 0.0 |
| w23 | 3 | -0.002322 | -0.28 |
| w24 | 4 | 0.032805 | -2.632 |
| w25 | 2 | 0.035085 | 1.511 |
| w26 | 9 | 0.104602 | 10.273 |
| w27 | 1 | -0.038371 | -3.027 |
| w28 | 8 | 0.045124 | 2.696 |
| w29 | 4 | -0.01525 | -1.853 |
| w30 | 11 | -0.060112 | -3.303 |
| w31 | 9 | -0.03368 | -2.419 |
| w32 | 5 | -0.034504 | -3.586 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 3 | 0.025739 | -0.441 |
| w13 | 5 | 0.032505 | 3.054 |
| w14 | 1 | -0.069763 | -5.681 |
| w15 | 5 | -0.028747 | -1.629 |
| w16 | 0 | None | 0.0 |
| w17 | 6 | -0.104213 | -7.153 |
| w18 | 4 | 0.086277 | 6.008 |
| w19 | 3 | 0.056208 | 4.267 |
| w20 | 7 | 0.16665 | 16.42 |
| w21 | 4 | 0.01862 | 0.438 |
| w22 | 1 | 0.056142 | 1.987 |
| w23 | 6 | -0.103216 | -7.154 |
| w24 | 5 | -0.02632 | -8.706 |
| w25 | 4 | -0.034175 | -4.467 |
| w26 | 13 | -0.026776 | -2.388 |
| w27 | 3 | -0.100019 | -10.364 |
| w28 | 8 | -0.003128 | -1.665 |
| w29 | 1 | -0.003585 | -0.141 |
| w30 | 11 | -0.066973 | -5.133 |
| w31 | 6 | -0.088623 | -8.129 |
| w32 | 6 | 0.046318 | 1.779 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 7 | 0.031708 | 0.818 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | -0.054824 | -3.747 |
| w18 | 2 | -0.021049 | -1.384 |
| w19 | 9 | 0.175187 | 15.124 |
| w20 | 8 | 0.006046 | -0.743 |
| w21 | 5 | 0.11046 | 6.985 |
| w22 | 2 | -0.133746 | -12.155 |
| w23 | 9 | 0.119807 | 15.374 |
| w24 | 4 | -0.001452 | -6.475 |
| w25 | 1 | 0.035659 | 1.899 |
| w26 | 9 | 0.145846 | 15.326 |
| w27 | 3 | 0.072634 | 3.199 |
| w28 | 7 | -0.022973 | -2.941 |
| w29 | 5 | 0.009383 | -0.715 |
| w30 | 12 | 0.00021 | 0.526 |
| w31 | 13 | -0.026814 | -5.566 |
| w32 | 7 | -0.036145 | -4.416 |

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
| w15 | 2 | -0.064335 | -6.318 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | -0.181507 | -7.456 |
| w18 | 3 | 0.042007 | 1.316 |
| w19 | 6 | 0.161924 | 10.049 |
| w20 | 2 | -0.102503 | -5.805 |
| w21 | 4 | 0.112529 | 7.312 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 1 | 0.044321 | 1.164 |
| w26 | 1 | -0.07441 | -0.751 |
| w27 | 0 | None | 0.0 |
| w28 | 3 | -0.018521 | -2.091 |
| w29 | 0 | None | 0.0 |
| w30 | 5 | 0.003485 | -0.32 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | -0.017096 | 0.0 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 1 | -0.120467 | -9.606 |
| w17 | 5 | 0.015064 | -0.075 |
| w18 | 3 | -0.047019 | -1.745 |
| w19 | 7 | 0.143618 | 9.117 |
| w20 | 7 | -0.003391 | 1.825 |
| w21 | 9 | -0.155302 | -16.601 |
| w22 | 1 | 0.026313 | 0.601 |
| w23 | 5 | -0.012955 | -2.208 |
| w24 | 6 | 0.013339 | -7.179 |
| w25 | 3 | 0.015561 | -0.208 |
| w26 | 12 | -0.116252 | -12.843 |
| w27 | 2 | -0.026135 | -3.466 |
| w28 | 8 | 0.106149 | 8.596 |
| w29 | 4 | -0.06085 | -5.003 |
| w30 | 10 | -0.05639 | -5.334 |
| w31 | 9 | 0.01058 | 1.037 |
| w32 | 13 | 0.119996 | 10.773 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 7 | 0.012888 | 4.771 |
| w21 | 7 | 0.06646 | 2.995 |
| w22 | 1 | 0.049115 | 1.933 |
| w23 | 5 | 0.044137 | 3.67 |
| w24 | 5 | 0.021085 | -4.438 |
| w25 | 4 | 0.052644 | 2.336 |
| w26 | 14 | 0.039537 | 2.592 |
| w27 | 1 | -0.073127 | -0.737 |
| w28 | 8 | 0.055106 | 4.426 |
| w29 | 1 | -0.017091 | -0.866 |
| w30 | 8 | -0.094466 | -6.557 |
| w31 | 10 | -0.00894 | -0.413 |
| w32 | 5 | 0.052442 | 3.362 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 2 | 0.034699 | 0.817 |
| w23 | 7 | -0.164612 | -10.193 |
| w24 | 6 | 0.021747 | -6.135 |
| w25 | 1 | -0.034355 | -3.091 |
| w26 | 5 | 0.082848 | 6.388 |
| w27 | 3 | 0.089554 | 3.29 |
| w28 | 10 | -0.035801 | -3.034 |
| w29 | 2 | -0.06347 | -2.835 |
| w30 | 11 | -0.108922 | -12.334 |
| w31 | 9 | 0.002908 | 0.059 |
| w32 | 4 | 0.068606 | 3.246 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 4 | 0.020952 | -0.085 |
| w25 | 2 | 0.0223 | 0.688 |
| w26 | 9 | 0.010757 | 0.255 |
| w27 | 0 | None | 0.0 |
| w28 | 9 | 0.010044 | -0.212 |
| w29 | 3 | -0.005625 | -0.435 |
| w30 | 9 | -0.075223 | -4.897 |
| w31 | 8 | 0.020038 | 2.579 |
| w32 | 6 | -0.094307 | -9.152 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 0 | 0.024115 | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 4 | 0.032933 | 2.405 |
| w8 | 10 | 0.015406 | 1.772 |
| w9 | 10 | 0.082776 | 10.599 |
| w10 | 5 | -0.040527 | -3.005 |
| w11 | 5 | 0.103811 | 4.839 |
| w12 | 8 | 0.001877 | 0.518 |
| w13 | 2 | 0.122315 | 4.002 |
| w14 | 0 | None | 0.0 |
| w15 | 5 | -0.042963 | -2.717 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | 0.090009 | 0.747 |
| w18 | 1 | -0.028359 | -0.515 |
| w19 | 6 | 0.047359 | 4.289 |
| w20 | 6 | 0.251311 | 20.024 |
| w21 | 9 | 0.073394 | 9.069 |
| w22 | 2 | 0.01108 | -0.038 |
| w23 | 4 | 0.074774 | 10.037 |
| w24 | 4 | -0.01457 | -1.824 |
| w25 | 5 | -0.172419 | -10.663 |
| w26 | 6 | 0.07639 | 4.484 |
| w27 | 1 | -0.027519 | -2.497 |
| w28 | 6 | 0.063268 | 4.722 |
| w29 | 4 | -0.050955 | -4.948 |
| w30 | 0 | None | 0.0 |
| w31 | 8 | -0.166132 | -13.892 |
| w32 | 1 | 0.004956 | -0.169 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 0 | None | 0.0 |
| w6 | 3 | 0.027653 | 0.402 |
| w7 | 5 | 0.168001 | 11.106 |
| w8 | 9 | 0.225162 | 18.794 |
| w9 | 6 | 0.055569 | 4.85 |
| w10 | 2 | 0.048105 | 0.167 |
| w11 | 3 | 0.022326 | 0.627 |
| w12 | 8 | 0.006072 | 0.841 |
| w13 | 2 | 0.062846 | 2.149 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | -0.038056 | -1.723 |
| w18 | 2 | 0.045725 | 2.381 |
| w19 | 5 | 0.160447 | 12.013 |
| w20 | 4 | 0.020369 | -0.542 |
| w21 | 3 | 0.068865 | 2.229 |
| w22 | 1 | -0.246793 | -9.797 |
| w23 | 2 | -0.102224 | -4.567 |
| w24 | 1 | -0.023436 | -0.99 |
| w25 | 4 | -9.6e-05 | 2.29 |
| w26 | 1 | 0.076563 | 1.59 |
| w27 | 2 | 0.016087 | 0.313 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | -0.24977 | -20.752 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | 0.009052 | 0.044 |
| w32 | 1 | 0.016757 | -0.021 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 7 | -0.114991 | -10.666 |
| w18 | 0 | None | 0.0 |
| w19 | 6 | -0.011939 | -0.126 |
| w20 | 8 | -0.151506 | -13.807 |
| w21 | 10 | 0.077123 | 6.44 |
| w22 | 1 | -0.006159 | -0.992 |
| w23 | 4 | 0.211153 | 18.354 |
| w24 | 4 | -0.041223 | -7.093 |
| w25 | 3 | 0.030761 | 0.538 |
| w26 | 11 | 0.182429 | 25.159 |
| w27 | 2 | 0.003708 | -1.414 |
| w28 | 4 | -0.021103 | -2.891 |
| w29 | 2 | -0.001275 | -0.599 |
| w30 | 11 | -0.093214 | -8.281 |
| w31 | 10 | -0.038381 | -2.743 |
| w32 | 2 | -0.084587 | -4.15 |

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
| w17 | 4 | -0.067613 | -3.425 |
| w18 | 7 | -0.029904 | -4.573 |
| w19 | 6 | 0.123766 | 9.487 |
| w20 | 4 | -0.102962 | -6.2 |
| w21 | 8 | 0.075195 | 4.994 |
| w22 | 3 | 0.038758 | 1.328 |
| w23 | 5 | -0.013796 | -1.274 |
| w24 | 3 | 0.019991 | -1.395 |
| w25 | 1 | 0.002557 | 0.159 |
| w26 | 4 | 0.066155 | 1.922 |
| w27 | 0 | None | 0.0 |
| w28 | 4 | 0.086849 | 5.425 |
| w29 | 0 | -0.006165 | 0.0 |
| w30 | 8 | -0.062907 | -4.971 |
| w31 | 9 | -0.065458 | -5.538 |
| w32 | 5 | 0.092197 | 6.495 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 6 | 0.012898 | 1.505 |
| w20 | 8 | 0.126678 | 18.282 |
| w21 | 3 | 0.042439 | 1.486 |
| w22 | 0 | -0.012228 | 0.0 |
| w23 | 2 | 0.043115 | 1.895 |
| w24 | 4 | 0.07138 | 1.549 |
| w25 | 2 | 0.023597 | 0.425 |
| w26 | 8 | 0.120949 | 10.591 |
| w27 | 3 | 0.108796 | 3.753 |
| w28 | 10 | -0.050966 | -5.817 |
| w29 | 1 | 0.024991 | 0.302 |
| w30 | 10 | 0.044292 | 5.953 |
| w31 | 12 | -0.061751 | -6.221 |
| w32 | 3 | -0.151106 | -17.306 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 2 | 0.05006 | 1.821 |
| w23 | 5 | 0.073214 | 2.841 |
| w24 | 4 | -0.027081 | -7.413 |
| w25 | 1 | 0.056629 | 2.217 |
| w26 | 7 | 0.059614 | 4.133 |
| w27 | 3 | 0.06901 | 1.995 |
| w28 | 5 | 0.059657 | 4.635 |
| w29 | 3 | -0.208954 | -13.754 |
| w30 | 11 | -0.099534 | -5.677 |
| w31 | 10 | 0.046014 | 4.969 |
| w32 | 3 | 0.054093 | 2.316 |

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
| w27 | 2 | 0.062218 | 1.807 |
| w28 | 7 | 0.026669 | 2.194 |
| w29 | 3 | -0.086337 | -3.892 |
| w30 | 12 | 0.01687 | 5.456 |
| w31 | 11 | 0.021203 | 2.039 |
| w32 | 3 | -0.330981 | -18.569 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 4 | -0.101005 | -5.478 |
| w18 | 8 | -0.008323 | -1.498 |
| w19 | 6 | 0.056644 | 4.793 |
| w20 | 7 | 0.098919 | 10.073 |
| w21 | 6 | 0.024632 | 1.678 |
| w22 | 1 | 0.020585 | 0.407 |
| w23 | 5 | 0.007669 | 1.242 |
| w24 | 5 | 0.027878 | -2.615 |
| w25 | 1 | 0.020588 | 0.1 |
| w26 | 9 | 0.113058 | 10.325 |
| w27 | 2 | 0.034668 | 2.64 |
| w28 | 8 | -0.081556 | -5.721 |
| w29 | 2 | -0.045144 | -2.34 |
| w30 | 9 | -0.137956 | -22.512 |
| w31 | 8 | -0.020718 | -2.383 |
| w32 | 7 | -0.079831 | -7.943 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 9 | 0.099082 | 6.578 |
| w18 | 2 | -0.026573 | -0.194 |
| w19 | 6 | 0.088863 | 5.6 |
| w20 | 8 | -0.026961 | -2.421 |
| w21 | 6 | 0.036261 | 2.69 |
| w22 | 2 | 0.009946 | -0.317 |
| w23 | 5 | 0.03799 | 1.419 |
| w24 | 6 | -0.043911 | -12.828 |
| w25 | 0 | None | 0.0 |
| w26 | 13 | 0.13208 | 13.086 |
| w27 | 2 | -0.076317 | -1.38 |
| w28 | 8 | -0.019052 | -1.526 |
| w29 | 2 | -0.024496 | -1.254 |
| w30 | 12 | -0.011423 | -0.469 |
| w31 | 10 | 0.007308 | 0.149 |
| w32 | 9 | 0.048751 | 5.085 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 10 | 0.092137 | 8.59 |
| w29 | 1 | -0.011965 | -0.177 |
| w30 | 4 | 0.016292 | 3.054 |
| w31 | 5 | -0.043274 | -5.219 |
| w32 | 7 | 0.061225 | 3.885 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 0 | None | 0.0 |
| w15 | 3 | 0.065956 | 5.356 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | -0.141487 | -6.568 |
| w18 | 4 | 0.010449 | 0.79 |
| w19 | 10 | 0.057894 | 4.649 |
| w20 | 4 | -0.207355 | -12.757 |
| w21 | 4 | 0.060621 | 3.513 |
| w22 | 1 | -0.149017 | -7.986 |
| w23 | 4 | 0.144974 | 10.374 |
| w24 | 6 | 0.042829 | 1.365 |
| w25 | 1 | -0.024369 | -2.833 |
| w26 | 12 | -0.131069 | -11.299 |
| w27 | 1 | -0.026872 | -0.88 |
| w28 | 10 | 0.047652 | 5.132 |
| w29 | 2 | -0.016231 | -1.011 |
| w30 | 12 | -0.042348 | -1.341 |
| w31 | 7 | 0.033983 | 1.676 |
| w32 | 5 | -0.14307 | -12.146 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 4 | 0.023343 | -0.629 |
| w26 | 3 | 0.070539 | 3.178 |
| w27 | 2 | -0.042429 | -1.85 |
| w28 | 11 | 0.016227 | 0.678 |
| w29 | 1 | -0.038285 | -2.467 |
| w30 | 10 | -0.050594 | -3.879 |
| w31 | 5 | -0.031386 | -3.229 |
| w32 | 4 | -0.013212 | -2.482 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

