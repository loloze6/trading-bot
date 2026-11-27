# Backtest of 074-01.b1.b1.b1.b1.d1.d2_swing-scaled-still-down-fade_1d

- Plan: `../../../../../03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1.b1.d1.d2_swing-scaled-still-down-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.037228 | -0.988 |
| w2 | 5 | 0.04335 | 0.735 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 11 | 0.127024 | 8.328 |
| w8 | 8 | 0.147967 | 13.096 |
| w9 | 16 | 0.234456 | 44.536 |
| w10 | 5 | 0.057603 | 0.776 |
| w11 | 1 | None | -0.034 |
| w12 | 21 | 0.012824 | 2.278 |
| w13 | 7 | 0.138721 | 7.683 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 15 | 0.194631 | 19.0 |
| w18 | 5 | -0.047776 | -3.3 |
| w19 | 11 | -0.045878 | -4.665 |
| w20 | 13 | 0.126228 | 16.192 |
| w21 | 17 | 0.071191 | 4.594 |
| w22 | 1 | 0.006236 | -0.057 |
| w23 | 5 | -0.032956 | -3.3 |
| w24 | 4 | 0.006788 | -1.588 |
| w25 | 0 | None | 0.0 |
| w26 | 4 | -0.017049 | -1.402 |
| w27 | 0 | None | 0.0 |
| w28 | 6 | 0.043138 | 1.432 |
| w29 | 0 | None | 0.0 |
| w30 | 8 | 0.045079 | 3.451 |
| w31 | 11 | 0.018849 | 3.916 |
| w32 | 7 | 0.059481 | 1.755 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.054934 | -1.177 |
| w2 | 5 | 0.046034 | 1.792 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | -0.039404 | -4.925 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.030794 | 0.217 |
| w7 | 13 | 0.043925 | 3.694 |
| w8 | 14 | 0.244393 | 31.954 |
| w9 | 17 | 0.238674 | 43.269 |
| w10 | 2 | 0.13086 | 2.597 |
| w11 | 8 | -0.006552 | -1.843 |
| w12 | 21 | -0.008408 | -0.182 |
| w13 | 8 | 0.100545 | 2.628 |
| w14 | 2 | 0.002858 | -0.514 |
| w15 | 4 | 0.031428 | 0.528 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | 0.13304 | 5.479 |
| w18 | 2 | 0.04894 | 1.06 |
| w19 | 15 | 0.047451 | 4.066 |
| w20 | 15 | 0.054229 | 8.489 |
| w21 | 5 | 0.056256 | 2.16 |
| w22 | 0 | None | 0.0 |
| w23 | 5 | -0.039153 | -2.709 |
| w24 | 13 | -0.042696 | -5.493 |
| w25 | 0 | None | 0.0 |
| w26 | 16 | 0.059515 | 6.884 |
| w27 | 3 | -0.011621 | -1.691 |
| w28 | 9 | 0.114705 | 10.899 |
| w29 | 1 | -0.08089 | -0.969 |
| w30 | 14 | -0.07209 | -4.986 |
| w31 | 17 | -0.013956 | 0.557 |
| w32 | 8 | 0.036405 | 1.739 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 2 | -0.006848 | -0.797 |
| w7 | 9 | -0.010469 | -0.553 |
| w8 | 18 | 0.039717 | 9.242 |
| w9 | 10 | -0.013523 | -4.599 |
| w10 | 7 | 0.037498 | 1.463 |
| w11 | 12 | -0.067805 | -7.798 |
| w12 | 12 | 0.121373 | 12.707 |
| w13 | 7 | 0.149575 | 5.049 |
| w14 | 3 | 0.036903 | 1.604 |
| w15 | 4 | 0.001891 | -0.324 |
| w16 | 3 | 0.021054 | -0.349 |
| w17 | 12 | 0.15605 | 9.263 |
| w18 | 7 | -0.001944 | 0.779 |
| w19 | 11 | 0.040127 | 6.278 |
| w20 | 5 | -0.041152 | 10.634 |
| w21 | 7 | 0.029288 | 1.184 |
| w22 | 1 | 0.038604 | 0.267 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | -0.051211 | -5.431 |
| w25 | 9 | 0.034192 | 2.747 |
| w26 | 9 | 0.114023 | 10.621 |
| w27 | 2 | 0.08858 | 6.608 |
| w28 | 8 | 0.075187 | 2.886 |
| w29 | 0 | None | 0.0 |
| w30 | 20 | -0.081452 | -5.816 |
| w31 | 14 | 0.040704 | 3.775 |
| w32 | 18 | 0.060867 | 4.323 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 11 | 0.093911 | 5.742 |
| w8 | 17 | 0.043791 | 3.397 |
| w9 | 19 | 0.003358 | 2.061 |
| w10 | 5 | 0.098781 | 1.454 |
| w11 | 7 | -0.040207 | -6.597 |
| w12 | 11 | 0.077566 | 5.066 |
| w13 | 5 | 0.0743 | 1.983 |
| w14 | 3 | -0.003076 | -1.634 |
| w15 | 5 | 0.022092 | 0.272 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | 0.141915 | 9.494 |
| w18 | 8 | -0.002687 | -0.63 |
| w19 | 17 | 0.014694 | -0.984 |
| w20 | 20 | 0.172649 | 19.173 |
| w21 | 13 | -0.012057 | -2.223 |
| w22 | 4 | -0.012118 | -1.891 |
| w23 | 4 | 0.059041 | 2.957 |
| w24 | 5 | 0.057791 | 0.655 |
| w25 | 0 | None | 0.0 |
| w26 | 14 | 0.111696 | 10.133 |
| w27 | 3 | -0.130636 | -4.007 |
| w28 | 22 | -0.071771 | -9.74 |
| w29 | 0 | None | 0.0 |
| w30 | 8 | 0.028019 | -0.137 |
| w31 | 11 | -0.097168 | -9.462 |
| w32 | 13 | 0.147558 | 27.774 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 6 | -0.044851 | -1.799 |
| w3 | 13 | 0.059679 | 7.403 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | 0.016262 | -0.113 |
| w6 | 0 | None | 0.0 |
| w7 | 9 | 0.055785 | 3.753 |
| w8 | 17 | 0.103993 | 16.624 |
| w9 | 18 | 0.192914 | 40.392 |
| w10 | 1 | 0.203484 | 1.349 |
| w11 | 8 | -0.016984 | -1.977 |
| w12 | 14 | 0.0502 | 5.899 |
| w13 | 5 | 0.08297 | 2.18 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | -0.050284 | -2.488 |
| w16 | 0 | None | 0.0 |
| w17 | 7 | 0.09695 | 3.426 |
| w18 | 1 | 0.020562 | 0.86 |
| w19 | 12 | -0.071482 | -6.348 |
| w20 | 15 | 0.000887 | 0.785 |
| w21 | 12 | 0.046225 | 2.923 |
| w22 | 1 | -0.02418 | -0.165 |
| w23 | 4 | -0.044065 | -1.82 |
| w24 | 11 | 0.002575 | -3.392 |
| w25 | 0 | None | 0.0 |
| w26 | 14 | 0.034513 | 3.783 |
| w27 | 5 | -0.054249 | -2.841 |
| w28 | 15 | 0.041921 | 6.764 |
| w29 | 0 | None | 0.0 |
| w30 | 15 | -0.024978 | 0.287 |
| w31 | 12 | -0.004782 | 1.551 |
| w32 | 4 | 0.011784 | -0.02 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 1 | 0.07901 | 0.874 |
| w11 | 13 | -0.051013 | -4.91 |
| w12 | 13 | 0.051141 | 4.365 |
| w13 | 4 | 0.154141 | 5.22 |
| w14 | 0 | None | 0.0 |
| w15 | 12 | -0.013131 | -4.982 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | 0.085217 | 3.137 |
| w18 | 16 | 0.088093 | 17.404 |
| w19 | 17 | -0.019287 | -1.806 |
| w20 | 17 | -0.081207 | -6.358 |
| w21 | 21 | -0.038113 | -3.744 |
| w22 | 1 | -0.029478 | -0.707 |
| w23 | 10 | 0.120137 | 16.07 |
| w24 | 8 | 0.034361 | -4.06 |
| w25 | 3 | 0.00788 | 0.193 |
| w26 | 17 | 0.16966 | 16.827 |
| w27 | 5 | -0.043357 | -5.141 |
| w28 | 19 | 0.018122 | -1.493 |
| w29 | 5 | 0.016495 | -0.026 |
| w30 | 17 | -0.062113 | -2.246 |
| w31 | 15 | -0.049468 | -4.389 |
| w32 | 10 | -0.019459 | -3.526 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 8 | 0.04148 | -0.59 |
| w13 | 6 | 0.063847 | 6.094 |
| w14 | 3 | -0.05474 | -5.914 |
| w15 | 9 | -0.009616 | -3.64 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | 0.118524 | 5.401 |
| w18 | 8 | 0.069759 | 4.37 |
| w19 | 12 | 0.054937 | 4.297 |
| w20 | 16 | 0.057386 | 6.093 |
| w21 | 10 | 0.084392 | 4.952 |
| w22 | 10 | 0.060205 | 1.055 |
| w23 | 20 | -0.095771 | -11.279 |
| w24 | 14 | -0.048753 | -14.902 |
| w25 | 5 | 0.004589 | -1.971 |
| w26 | 21 | -0.030338 | -2.111 |
| w27 | 4 | -0.050732 | -3.791 |
| w28 | 17 | -0.049201 | -4.938 |
| w29 | 1 | -0.11181 | -0.61 |
| w30 | 24 | -0.094421 | -6.856 |
| w31 | 12 | -0.085032 | -6.99 |
| w32 | 7 | 0.09979 | 6.226 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 7 | 0.065046 | 2.85 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | 0.01786 | 0.213 |
| w18 | 6 | 0.082017 | 5.475 |
| w19 | 24 | -0.003712 | 2.316 |
| w20 | 22 | -0.106668 | -9.069 |
| w21 | 10 | 0.075646 | 4.755 |
| w22 | 7 | -0.147728 | -9.601 |
| w23 | 20 | -0.027199 | 0.734 |
| w24 | 9 | -0.037121 | -12.266 |
| w25 | 3 | 0.002728 | -1.014 |
| w26 | 18 | 0.077628 | 6.71 |
| w27 | 5 | 0.012281 | -2.146 |
| w28 | 19 | -0.051777 | -5.141 |
| w29 | 4 | -0.167708 | -10.742 |
| w30 | 23 | 0.018121 | 4.321 |
| w31 | 17 | -0.10726 | -13.519 |
| w32 | 14 | -0.04249 | -5.247 |

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
| w15 | 3 | -0.040392 | -3.405 |
| w16 | 1 | -0.010493 | -0.89 |
| w17 | 14 | -0.055262 | -3.174 |
| w18 | 7 | 0.037852 | 2.059 |
| w19 | 13 | 0.028742 | 2.803 |
| w20 | 2 | -0.08506 | -3.009 |
| w21 | 12 | 0.046634 | 2.557 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 4 | 0.084684 | 2.551 |
| w26 | 1 | -0.07441 | -1.006 |
| w27 | 0 | None | 0.0 |
| w28 | 4 | -0.025726 | -1.858 |
| w29 | 0 | None | 0.0 |
| w30 | 13 | 0.054044 | 3.982 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 1 | -0.120467 | -8.636 |
| w17 | 11 | 0.194544 | 14.747 |
| w18 | 4 | 0.021612 | 0.325 |
| w19 | 12 | 0.033558 | 2.188 |
| w20 | 18 | -0.064932 | -6.493 |
| w21 | 18 | -0.030616 | -5.538 |
| w22 | 2 | 0.008966 | -0.328 |
| w23 | 12 | -0.069425 | -6.713 |
| w24 | 12 | 0.001082 | -13.286 |
| w25 | 5 | -0.011792 | -1.839 |
| w26 | 19 | -0.138031 | -14.448 |
| w27 | 6 | -0.023155 | -5.293 |
| w28 | 17 | -0.008762 | -0.966 |
| w29 | 5 | -0.074322 | -2.97 |
| w30 | 16 | -0.116942 | -9.007 |
| w31 | 20 | -0.074003 | -6.004 |
| w32 | 15 | 0.141721 | 11.644 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 17 | 0.060471 | 12.123 |
| w21 | 18 | 0.177006 | 17.814 |
| w22 | 3 | -0.014681 | -2.169 |
| w23 | 14 | 0.038715 | 5.277 |
| w24 | 8 | 0.044776 | -3.509 |
| w25 | 5 | 0.059308 | 2.049 |
| w26 | 20 | 0.030466 | 1.201 |
| w27 | 2 | -0.021415 | -0.199 |
| w28 | 21 | 0.019365 | 1.499 |
| w29 | 1 | -0.005871 | 0.341 |
| w30 | 18 | -0.166127 | -12.918 |
| w31 | 13 | -0.045897 | -2.599 |
| w32 | 7 | -0.055324 | -2.871 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 7 | 0.022536 | -0.254 |
| w23 | 14 | -0.026469 | 0.684 |
| w24 | 12 | 0.043847 | -6.511 |
| w25 | 2 | -0.17371 | -6.052 |
| w26 | 13 | -0.017841 | -1.64 |
| w27 | 5 | 0.078099 | 1.467 |
| w28 | 21 | -0.023392 | -1.725 |
| w29 | 3 | 0.019342 | 0.683 |
| w30 | 17 | -0.150569 | -12.838 |
| w31 | 10 | -0.000401 | 0.502 |
| w32 | 6 | 0.100767 | 4.008 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 13 | -0.002309 | -4.72 |
| w25 | 4 | 0.014676 | -0.052 |
| w26 | 18 | -0.007461 | -1.719 |
| w27 | 0 | None | 0.0 |
| w28 | 16 | 0.051571 | 3.312 |
| w29 | 1 | -0.12372 | -1.678 |
| w30 | 21 | -0.031745 | 0.585 |
| w31 | 10 | 0.00769 | 1.549 |
| w32 | 10 | -0.052415 | -3.151 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 2 | 0.058539 | 1.158 |
| w6 | 1 | -0.080217 | -0.564 |
| w7 | 10 | 0.024788 | 2.031 |
| w8 | 15 | -0.069523 | -6.224 |
| w9 | 21 | 0.15623 | 24.543 |
| w10 | 12 | 0.011976 | -1.745 |
| w11 | 9 | 0.041441 | 1.818 |
| w12 | 23 | -0.099476 | -9.625 |
| w13 | 4 | 0.104254 | 3.498 |
| w14 | 0 | None | 0.0 |
| w15 | 8 | 0.048959 | 2.578 |
| w16 | 0 | None | 0.0 |
| w17 | 14 | 0.089404 | 6.812 |
| w18 | 2 | -0.054023 | -1.461 |
| w19 | 13 | -0.115869 | -9.991 |
| w20 | 20 | 0.115381 | 10.434 |
| w21 | 15 | -0.045168 | -4.039 |
| w22 | 7 | -0.001994 | -0.853 |
| w23 | 12 | 0.109268 | 17.324 |
| w24 | 6 | -0.011871 | -1.913 |
| w25 | 8 | -0.053238 | -2.714 |
| w26 | 5 | 0.02816 | 0.931 |
| w27 | 2 | -0.046336 | -2.369 |
| w28 | 11 | -0.101747 | -7.738 |
| w29 | 6 | 0.013923 | -0.037 |
| w30 | 0 | None | 0.0 |
| w31 | 16 | -0.121944 | -9.704 |
| w32 | 2 | -0.006885 | -0.446 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.006146 | -0.176 |
| w7 | 15 | 0.17298 | 11.95 |
| w8 | 24 | 0.084011 | 9.365 |
| w9 | 20 | 0.261559 | 50.914 |
| w10 | 5 | 0.052006 | 0.828 |
| w11 | 5 | 0.03154 | 0.824 |
| w12 | 18 | 0.011347 | 2.145 |
| w13 | 5 | 0.148211 | 5.175 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 7 | 0.056802 | 3.015 |
| w18 | 7 | 0.03569 | 2.195 |
| w19 | 9 | 0.106306 | 6.874 |
| w20 | 12 | 0.034581 | -0.342 |
| w21 | 6 | 0.049264 | 1.661 |
| w22 | 3 | -0.219182 | -9.766 |
| w23 | 6 | -0.116422 | -8.889 |
| w24 | 6 | -0.05763 | -4.872 |
| w25 | 9 | -0.014945 | -2.746 |
| w26 | 2 | 0.075242 | 0.467 |
| w27 | 2 | 0.021775 | 0.724 |
| w28 | 0 | None | 0.0 |
| w29 | 6 | -0.005779 | -2.577 |
| w30 | 1 | -0.006213 | -0.272 |
| w31 | 12 | 0.003453 | -0.386 |
| w32 | 5 | -0.011096 | -1.14 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 12 | 0.152168 | 8.843 |
| w18 | 0 | None | 0.0 |
| w19 | 15 | 0.017444 | 2.261 |
| w20 | 13 | -0.07875 | -9.263 |
| w21 | 19 | 0.043238 | 3.416 |
| w22 | 3 | 0.00902 | -0.721 |
| w23 | 13 | 0.11303 | 13.485 |
| w24 | 7 | -0.040465 | -6.142 |
| w25 | 8 | 0.011568 | -0.676 |
| w26 | 16 | 0.082896 | 13.45 |
| w27 | 4 | -0.019071 | -6.104 |
| w28 | 14 | -0.009352 | -2.103 |
| w29 | 5 | -0.061493 | -3.596 |
| w30 | 20 | -0.137357 | -12.364 |
| w31 | 17 | -0.042361 | -2.481 |
| w32 | 4 | -0.079492 | -7.838 |

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
| w17 | 9 | 0.14992 | 7.866 |
| w18 | 15 | 0.054484 | 6.689 |
| w19 | 10 | 0.072974 | 5.629 |
| w20 | 11 | -0.036885 | -3.136 |
| w21 | 16 | 0.153241 | 17.69 |
| w22 | 8 | -0.004792 | -1.477 |
| w23 | 10 | 0.092854 | 11.517 |
| w24 | 5 | -0.002631 | -4.442 |
| w25 | 3 | -0.017048 | 0.008 |
| w26 | 7 | -0.008588 | -2.493 |
| w27 | 0 | None | 0.0 |
| w28 | 18 | 0.09589 | 9.802 |
| w29 | 0 | None | 0.0 |
| w30 | 19 | -0.125505 | -10.939 |
| w31 | 17 | -0.110889 | -9.561 |
| w32 | 10 | 0.107978 | 6.951 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 12 | 0.023595 | 4.248 |
| w20 | 15 | 0.114 | 16.618 |
| w21 | 5 | 0.053833 | 2.369 |
| w22 | 0 | -0.012228 | 0.0 |
| w23 | 2 | 0.045104 | 0.832 |
| w24 | 6 | 0.0176 | -5.163 |
| w25 | 6 | 0.006026 | -0.898 |
| w26 | 11 | 0.095116 | 6.489 |
| w27 | 1 | 0.130384 | 0.906 |
| w28 | 18 | -0.021644 | -1.14 |
| w29 | 3 | -0.23125 | -6.73 |
| w30 | 16 | 0.050885 | 9.638 |
| w31 | 19 | -0.036576 | -3.805 |
| w32 | 3 | -0.223865 | -18.878 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 3 | 0.027729 | -0.02 |
| w23 | 15 | 0.129424 | 8.7 |
| w24 | 14 | -0.013307 | -9.864 |
| w25 | 3 | 0.049293 | 1.512 |
| w26 | 13 | 0.110944 | 10.015 |
| w27 | 7 | -0.016272 | -1.753 |
| w28 | 15 | 0.114014 | 9.194 |
| w29 | 4 | -0.304648 | -18.304 |
| w30 | 18 | -0.068485 | -4.949 |
| w31 | 17 | 0.029453 | 2.795 |
| w32 | 4 | 0.014758 | -1.121 |

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
| w27 | 6 | 0.053576 | 0.303 |
| w28 | 13 | 0.020243 | 1.499 |
| w29 | 3 | -0.025495 | -1.259 |
| w30 | 21 | 0.020788 | 6.939 |
| w31 | 18 | -0.032318 | -1.833 |
| w32 | 3 | -0.116391 | -4.106 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 10 | -0.124936 | -5.975 |
| w18 | 12 | 0.024007 | 6.265 |
| w19 | 16 | 0.001104 | 0.15 |
| w20 | 19 | 0.080542 | 11.631 |
| w21 | 14 | 0.033086 | 3.125 |
| w22 | 2 | 0.032287 | 0.725 |
| w23 | 14 | -0.043365 | -4.099 |
| w24 | 8 | -0.026389 | -10.257 |
| w25 | 1 | 0.038457 | 0.221 |
| w26 | 15 | 0.115798 | 9.459 |
| w27 | 4 | -0.037832 | -3.603 |
| w28 | 18 | -0.078447 | -6.398 |
| w29 | 4 | -0.081007 | -1.921 |
| w30 | 19 | -0.110452 | -20.618 |
| w31 | 18 | 0.032295 | 2.478 |
| w32 | 14 | 0.000985 | -2.645 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 14 | 0.227521 | 15.592 |
| w18 | 3 | -0.076768 | -2.635 |
| w19 | 17 | 0.072303 | 7.827 |
| w20 | 22 | 0.027086 | 2.852 |
| w21 | 12 | 0.076692 | 8.03 |
| w22 | 2 | 0.017856 | -0.014 |
| w23 | 15 | -0.00356 | -0.975 |
| w24 | 13 | -0.020989 | -14.863 |
| w25 | 0 | None | 0.0 |
| w26 | 16 | 0.10001 | 9.544 |
| w27 | 3 | -0.041998 | -2.351 |
| w28 | 17 | 0.065379 | 7.764 |
| w29 | 4 | -0.005078 | -0.333 |
| w30 | 28 | -0.053153 | -1.932 |
| w31 | 19 | 0.007756 | 0.339 |
| w32 | 13 | 0.069717 | 6.016 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 15 | 0.079577 | 6.517 |
| w29 | 2 | -0.173643 | -3.833 |
| w30 | 9 | 0.024812 | 3.346 |
| w31 | 9 | 0.067252 | 4.25 |
| w32 | 14 | 0.092361 | 7.066 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 0 | None | 0.0 |
| w15 | 13 | 0.059196 | 5.188 |
| w16 | 0 | None | 0.0 |
| w17 | 8 | -0.141279 | -7.504 |
| w18 | 8 | 0.078874 | 6.798 |
| w19 | 15 | 0.012206 | 0.875 |
| w20 | 17 | -0.070225 | -5.001 |
| w21 | 9 | 0.01122 | -1.231 |
| w22 | 4 | -0.15488 | -8.93 |
| w23 | 9 | 0.075089 | 5.556 |
| w24 | 9 | -0.008802 | -5.568 |
| w25 | 2 | -0.031656 | -0.907 |
| w26 | 17 | -0.057539 | -5.547 |
| w27 | 6 | -0.005119 | -1.701 |
| w28 | 20 | 0.053523 | 7.934 |
| w29 | 2 | -0.198989 | -7.028 |
| w30 | 14 | -0.029354 | -0.245 |
| w31 | 12 | -0.028529 | -2.265 |
| w32 | 13 | -0.113074 | -9.887 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 4 | 0.012026 | -2.911 |
| w26 | 8 | 0.076253 | 3.671 |
| w27 | 5 | -0.046969 | -3.465 |
| w28 | 23 | 0.020486 | 2.248 |
| w29 | 1 | -0.038296 | -1.597 |
| w30 | 25 | -0.039853 | -1.472 |
| w31 | 13 | 0.00346 | -1.123 |
| w32 | 6 | -0.04459 | -4.379 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

