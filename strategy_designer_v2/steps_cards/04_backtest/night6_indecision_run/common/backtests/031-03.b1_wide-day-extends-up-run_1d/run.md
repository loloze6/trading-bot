# Backtest of 031-03.b1_wide-day-extends-up-run_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-03.b1_wide-day-extends-up-run_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.034271 | -14.236 |
| w2 | 5 | 0.134849 | 59.768 |
| w3 | 18 | 0.118059 | 31.471 |
| w4 | 13 | -0.169672 | -17.307 |
| w5 | 20 | -0.010334 | 35.893 |
| w6 | 20 | 0.126184 | 81.552 |
| w7 | 3 | -0.103961 | -3.042 |
| w8 | 6 | 0.118077 | 6.336 |
| w9 | 4 | -0.11899 | -2.377 |
| w10 | 9 | -0.037364 | -2.047 |
| w11 | 15 | -0.005067 | 18.743 |
| w12 | 7 | 0.175673 | 5.064 |
| w13 | 18 | -0.036128 | -2.859 |
| w14 | 9 | -0.020432 | 2.705 |
| w15 | 17 | 0.059154 | 34.821 |
| w16 | 12 | 0.05334 | 20.337 |
| w17 | 5 | 0.066256 | 0.384 |
| w18 | 8 | -0.081797 | 1.015 |
| w19 | 6 | -0.002039 | -1.333 |
| w20 | 7 | 0.077886 | -4.618 |
| w21 | 13 | 0.0131 | 0.06 |
| w22 | 18 | 0.102623 | 54.495 |
| w23 | 10 | -0.005994 | -10.855 |
| w24 | 14 | 0.048574 | 41.617 |
| w25 | 16 | 0.019611 | 28.218 |
| w26 | 12 | -0.036414 | -5.484 |
| w27 | 12 | 0.146712 | 23.112 |
| w28 | 7 | -0.099871 | -5.968 |
| w29 | 19 | -0.044061 | -5.331 |
| w30 | 3 | 0.077357 | 8.252 |
| w31 | 11 | -0.081085 | -6.474 |
| w32 | 6 | 0.195303 | 34.108 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.077484 | 14.516 |
| w2 | 15 | -0.041039 | -26.626 |
| w3 | 14 | -0.071739 | -19.472 |
| w4 | 17 | -0.028218 | -11.295 |
| w5 | 13 | -0.024225 | 7.096 |
| w6 | 24 | 0.190892 | 82.287 |
| w7 | 4 | -0.036042 | -2.47 |
| w8 | 3 | -0.072637 | -13.647 |
| w9 | 10 | -0.060919 | -4.398 |
| w10 | 9 | 0.006464 | 11.591 |
| w11 | 11 | -0.029741 | -7.139 |
| w12 | 6 | 0.02071 | -3.727 |
| w13 | 13 | -0.034308 | 4.431 |
| w14 | 13 | -0.073319 | 5.404 |
| w15 | 22 | 0.205975 | 31.907 |
| w16 | 22 | -0.051454 | 4.691 |
| w17 | 10 | 0.07507 | -2.026 |
| w18 | 10 | 0.014909 | -9.041 |
| w19 | 2 | -0.143165 | -6.01 |
| w20 | 9 | -0.063323 | -11.521 |
| w21 | 11 | 0.046819 | -2.204 |
| w22 | 20 | -0.17644 | 0.78 |
| w23 | 7 | 0.033429 | -2.534 |
| w24 | 16 | -0.016061 | -12.885 |
| w25 | 16 | 0.004313 | 3.451 |
| w26 | 3 | -0.053934 | -5.526 |
| w27 | 16 | 0.033274 | 21.864 |
| w28 | 5 | -0.019731 | -3.867 |
| w29 | 14 | 0.13596 | 17.045 |
| w30 | 5 | -0.113914 | -16.647 |
| w31 | 3 | -0.084344 | -2.522 |
| w32 | 9 | 0.062906 | 7.458 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 17 | 0.087047 | 85.26 |
| w7 | 8 | 0.077327 | 14.066 |
| w8 | 4 | -0.065524 | -16.808 |
| w9 | 14 | 0.169904 | 36.974 |
| w10 | 8 | 0.034393 | -2.182 |
| w11 | 10 | -0.086966 | 13.307 |
| w12 | 6 | 0.017115 | 0.537 |
| w13 | 17 | -0.09939 | -11.5 |
| w14 | 11 | 0.1801 | 64.082 |
| w15 | 16 | 0.242993 | 95.091 |
| w16 | 12 | -0.054979 | 3.41 |
| w17 | 10 | 0.110028 | 31.477 |
| w18 | 6 | -0.017056 | -5.266 |
| w19 | 5 | 0.138543 | 1.371 |
| w20 | 4 | -0.019696 | -5.482 |
| w21 | 11 | 0.215203 | 28.763 |
| w22 | 13 | -0.162302 | -10.958 |
| w23 | 7 | -0.102803 | 1.313 |
| w24 | 17 | 0.029704 | 1.763 |
| w25 | 12 | -0.081317 | -20.771 |
| w26 | 10 | 0.091929 | 12.021 |
| w27 | 18 | 0.216921 | 169.046 |
| w28 | 7 | -0.105086 | -4.09 |
| w29 | 11 | 0.157959 | 29.098 |
| w30 | 4 | -0.088812 | -4.741 |
| w31 | 10 | -0.131647 | -12.334 |
| w32 | 10 | 0.282545 | 23.569 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 7 | 0.137033 | 22.03 |
| w8 | 7 | -0.004911 | -10.629 |
| w9 | 9 | 0.25852 | 29.944 |
| w10 | 12 | 0.092196 | 7.612 |
| w11 | 11 | 0.011866 | 1.42 |
| w12 | 8 | 0.024729 | -2.423 |
| w13 | 12 | -0.108185 | 2.159 |
| w14 | 8 | 0.092114 | 12.192 |
| w15 | 16 | -0.174025 | -45.994 |
| w16 | 13 | 0.046623 | 21.675 |
| w17 | 11 | 0.017592 | 8.521 |
| w18 | 6 | -0.170989 | -21.398 |
| w19 | 6 | -0.098421 | -13.069 |
| w20 | 5 | -0.035314 | -9.662 |
| w21 | 5 | 0.062622 | -7.421 |
| w22 | 15 | -0.052071 | 11.689 |
| w23 | 11 | 0.29597 | 47.865 |
| w24 | 18 | -0.121322 | -5.198 |
| w25 | 12 | -0.127112 | -3.166 |
| w26 | 7 | 0.031294 | -3.274 |
| w27 | 12 | 0.039053 | 13.73 |
| w28 | 8 | 0.098525 | 11.606 |
| w29 | 17 | -0.264346 | -23.805 |
| w30 | 17 | -0.074743 | -7.372 |
| w31 | 9 | -0.040419 | -6.013 |
| w32 | 10 | 0.248084 | 42.856 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | 0.084375 | 75.052 |
| w2 | 13 | -0.042635 | -14.14 |
| w3 | 13 | -0.055052 | -5.044 |
| w4 | 15 | 0.184949 | 121.454 |
| w5 | 20 | -0.088371 | 31.05 |
| w6 | 10 | 0.205027 | 45.257 |
| w7 | 12 | -0.123617 | 0.352 |
| w8 | 4 | -0.052042 | -9.169 |
| w9 | 7 | -0.032444 | 7.566 |
| w10 | 12 | -0.069505 | -0.608 |
| w11 | 7 | 0.051468 | 12.618 |
| w12 | 7 | -0.013233 | -1.653 |
| w13 | 21 | -0.039332 | 28.779 |
| w14 | 14 | 0.075698 | 54.122 |
| w15 | 20 | -0.032402 | -0.964 |
| w16 | 16 | 0.070863 | 17.875 |
| w17 | 12 | -0.034498 | 6.997 |
| w18 | 6 | -0.049096 | 2.403 |
| w19 | 5 | 0.032363 | -4.368 |
| w20 | 8 | -0.008764 | 12.93 |
| w21 | 8 | 0.054464 | 6.04 |
| w22 | 18 | 0.046915 | 27.808 |
| w23 | 12 | -0.224162 | -23.232 |
| w24 | 15 | -0.102438 | -0.096 |
| w25 | 13 | 0.017157 | 19.867 |
| w26 | 6 | 0.015332 | 2.191 |
| w27 | 10 | -0.023546 | 12.09 |
| w28 | 6 | -0.14921 | -14.66 |
| w29 | 24 | 0.172349 | 31.37 |
| w30 | 3 | -0.096136 | -7.895 |
| w31 | 11 | -0.096018 | -16.691 |
| w32 | 6 | 0.157161 | 8.304 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 17 | -0.014579 | 16.479 |
| w11 | 9 | -0.071506 | 0.829 |
| w12 | 10 | 0.100634 | 8.863 |
| w13 | 21 | -0.015275 | 13.082 |
| w14 | 12 | 0.070496 | 32.971 |
| w15 | 15 | 0.077539 | 3.575 |
| w16 | 23 | 0.060244 | 47.334 |
| w17 | 18 | 0.072336 | 33.77 |
| w18 | 4 | -0.218485 | -29.965 |
| w19 | 4 | 0.016555 | -3.869 |
| w20 | 9 | -0.080918 | -13.861 |
| w21 | 3 | 0.100775 | -0.483 |
| w22 | 23 | -0.002049 | 18.912 |
| w23 | 3 | -0.165523 | -14.456 |
| w24 | 15 | 0.186048 | 134.831 |
| w25 | 14 | 0.077177 | 11.48 |
| w26 | 3 | -0.029352 | -3.569 |
| w27 | 11 | 0.077943 | 58.823 |
| w28 | 4 | -0.075489 | -6.036 |
| w29 | 13 | 0.091547 | 5.177 |
| w30 | 2 | -0.084302 | -5.74 |
| w31 | 8 | -0.158726 | -12.37 |
| w32 | 22 | 0.154868 | 19.747 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 13 | -0.049589 | 6.407 |
| w13 | 17 | -0.052148 | -14.763 |
| w14 | 20 | 0.238332 | 93.937 |
| w15 | 5 | -0.098681 | 4.881 |
| w16 | 19 | 0.037381 | 21.149 |
| w17 | 11 | 0.058003 | -4.829 |
| w18 | 12 | -0.106966 | -19.063 |
| w19 | 9 | -0.0019 | 2.504 |
| w20 | 8 | -0.099798 | -15.146 |
| w21 | 8 | 0.012594 | -0.878 |
| w22 | 18 | 0.035232 | 14.069 |
| w23 | 3 | -0.037297 | -6.676 |
| w24 | 22 | -0.138204 | -23.055 |
| w25 | 13 | 0.149622 | 25.372 |
| w26 | 4 | 0.096354 | -9.261 |
| w27 | 11 | -0.028979 | -0.906 |
| w28 | 6 | -0.143878 | -12.278 |
| w29 | 16 | 0.185922 | 3.691 |
| w30 | 0 | None | 0.0 |
| w31 | 13 | -0.15366 | -13.147 |
| w32 | 16 | -0.014638 | -15.195 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 5 | -0.073132 | -12.891 |
| w16 | 17 | -0.029707 | 20.767 |
| w17 | 9 | -0.01424 | -11.29 |
| w18 | 11 | 0.044003 | 27.11 |
| w19 | 7 | -0.032895 | 3.445 |
| w20 | 9 | 0.108003 | 4.247 |
| w21 | 12 | 0.021413 | -0.797 |
| w22 | 13 | -0.008174 | -0.403 |
| w23 | 4 | -0.108047 | -10.015 |
| w24 | 21 | -0.027993 | 50.996 |
| w25 | 15 | 0.090003 | 7.404 |
| w26 | 1 | -0.011282 | -1.009 |
| w27 | 10 | 0.07708 | 99.718 |
| w28 | 5 | -0.167466 | -9.589 |
| w29 | 10 | -0.015957 | 15.757 |
| w30 | 1 | -0.029002 | 0.385 |
| w31 | 11 | 0.206511 | 14.584 |
| w32 | 12 | 0.091533 | 2.534 |

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
| w15 | 10 | -0.108202 | -12.285 |
| w16 | 25 | -0.013999 | 13.381 |
| w17 | 9 | 0.044388 | 7.489 |
| w18 | 6 | -0.073024 | -17.115 |
| w19 | 8 | 0.04597 | 6.056 |
| w20 | 8 | 0.017303 | 4.769 |
| w21 | 9 | -0.127775 | -4.989 |
| w22 | 8 | -0.06264 | -3.375 |
| w23 | 13 | 0.011056 | -12.345 |
| w24 | 20 | 0.047151 | 11.448 |
| w25 | 15 | -0.112098 | -8.712 |
| w26 | 8 | 0.243125 | 28.116 |
| w27 | 14 | 0.19344 | 105.12 |
| w28 | 7 | -0.189537 | -8.006 |
| w29 | 21 | -0.107218 | -16.253 |
| w30 | 0 | None | 0.0 |
| w31 | 23 | -0.258489 | -7.527 |
| w32 | 10 | 0.160839 | -1.011 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 21 | 0.153156 | 29.321 |
| w17 | 16 | -0.06405 | -0.978 |
| w18 | 8 | 0.028738 | 3.139 |
| w19 | 8 | 0.018731 | -3.191 |
| w20 | 6 | -0.044113 | -6.629 |
| w21 | 6 | -0.173749 | -19.33 |
| w22 | 17 | 0.003863 | 8.795 |
| w23 | 7 | -0.11559 | -21.522 |
| w24 | 21 | -0.052248 | 8.455 |
| w25 | 13 | 0.146522 | 20.246 |
| w26 | 7 | -0.020041 | -4.135 |
| w27 | 13 | 0.09818 | 29.012 |
| w28 | 1 | -0.291029 | -8.505 |
| w29 | 13 | 0.142783 | 14.64 |
| w30 | 7 | -0.045112 | -8.886 |
| w31 | 11 | -0.10774 | -11.373 |
| w32 | 7 | 0.130433 | 10.717 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 4 | -0.018271 | 4.389 |
| w21 | 9 | 0.003649 | 1.417 |
| w22 | 18 | 0.087921 | 20.207 |
| w23 | 6 | 0.006473 | -10.333 |
| w24 | 15 | 0.170246 | 113.862 |
| w25 | 10 | 0.12104 | 17.628 |
| w26 | 8 | -0.040556 | -14.686 |
| w27 | 16 | -0.027662 | 3.154 |
| w28 | 4 | -0.165078 | -8.927 |
| w29 | 15 | 0.025665 | 5.194 |
| w30 | 5 | 0.017556 | -3.638 |
| w31 | 8 | -0.066637 | -3.041 |
| w32 | 6 | 0.132352 | 9.872 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 12 | 0.064986 | 23.887 |
| w23 | 6 | 0.010507 | -11.938 |
| w24 | 17 | 0.179258 | 48.494 |
| w25 | 17 | -0.096313 | 47.502 |
| w26 | 6 | 0.107021 | -1.705 |
| w27 | 12 | 0.063052 | 25.374 |
| w28 | 3 | -0.012536 | -1.89 |
| w29 | 8 | -0.028678 | -1.019 |
| w30 | 6 | -0.024008 | -5.019 |
| w31 | 7 | -0.03829 | 5.181 |
| w32 | 12 | -0.090897 | -1.141 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 20 | -0.124383 | 9.468 |
| w25 | 10 | -0.012852 | -2.132 |
| w26 | 11 | -0.012985 | -2.578 |
| w27 | 23 | 0.06404 | 56.032 |
| w28 | 6 | 0.193471 | 15.931 |
| w29 | 8 | 0.002687 | 2.024 |
| w30 | 8 | 0.084903 | 3.397 |
| w31 | 6 | -0.061969 | 3.059 |
| w32 | 10 | 0.308652 | 62.207 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 14 | 0.161033 | 65.807 |
| w6 | 13 | 0.014552 | 7.36 |
| w7 | 11 | 0.033388 | 8.728 |
| w8 | 9 | 0.037158 | -8.385 |
| w9 | 6 | -0.093154 | -12.916 |
| w10 | 10 | 0.011249 | 5.223 |
| w11 | 10 | 0.013314 | 2.93 |
| w12 | 11 | -0.043575 | -16.388 |
| w13 | 16 | 0.030552 | 42.825 |
| w14 | 19 | -0.080377 | -13.009 |
| w15 | 11 | -0.055476 | -7.978 |
| w16 | 18 | 0.17544 | 51.784 |
| w17 | 10 | 0.033153 | 0.693 |
| w18 | 11 | -0.023841 | 7.192 |
| w19 | 10 | 0.041094 | 22.807 |
| w20 | 6 | 0.034524 | -2.501 |
| w21 | 4 | 0.099884 | 1.145 |
| w22 | 10 | -0.029955 | 1.21 |
| w23 | 10 | 0.004357 | -7.355 |
| w24 | 13 | -0.095998 | -3.758 |
| w25 | 9 | -0.008151 | 3.434 |
| w26 | 13 | 0.172065 | 29.671 |
| w27 | 16 | 0.002174 | 42.709 |
| w28 | 7 | -0.159912 | -12.517 |
| w29 | 11 | -0.032467 | 6.322 |
| w30 | 20 | 0.213488 | 121.924 |
| w31 | 10 | -0.004802 | -7.246 |
| w32 | 15 | 0.130895 | 35.421 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 19 | 0.075137 | 73.652 |
| w6 | 13 | -0.054479 | 16.889 |
| w7 | 5 | 0.034652 | 11.216 |
| w8 | 6 | 0.025335 | -2.643 |
| w9 | 6 | -0.025289 | -16.365 |
| w10 | 10 | 0.014984 | 15.212 |
| w11 | 14 | -0.084457 | -27.411 |
| w12 | 7 | -0.164481 | -8.12 |
| w13 | 17 | 0.034156 | 33.608 |
| w14 | 16 | -0.209589 | -22.254 |
| w15 | 7 | -0.195325 | -17.12 |
| w16 | 20 | -0.116926 | 10.791 |
| w17 | 8 | 0.038403 | -7.978 |
| w18 | 5 | -0.143126 | -18.158 |
| w19 | 14 | -0.113966 | -15.93 |
| w20 | 5 | -0.014542 | 1.931 |
| w21 | 7 | -0.016945 | -3.688 |
| w22 | 14 | -0.004971 | 15.739 |
| w23 | 7 | -0.047995 | -14.33 |
| w24 | 14 | -0.019506 | -1.032 |
| w25 | 4 | 0.05419 | 2.474 |
| w26 | 9 | 0.055975 | 2.456 |
| w27 | 6 | -0.050011 | 12.384 |
| w28 | 7 | -0.026732 | 1.787 |
| w29 | 8 | -0.199331 | -13.473 |
| w30 | 17 | -0.149613 | -18.05 |
| w31 | 10 | 0.046969 | 5.768 |
| w32 | 14 | -0.115031 | 2.845 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 9 | -0.042176 | -3.581 |
| w18 | 7 | 0.124706 | 29.871 |
| w19 | 9 | 0.037602 | 1.275 |
| w20 | 13 | -0.104686 | -9.85 |
| w21 | 9 | -0.120522 | -24.975 |
| w22 | 12 | 0.146771 | 35.934 |
| w23 | 8 | -0.062659 | -8.601 |
| w24 | 19 | 0.051246 | 21.875 |
| w25 | 8 | 0.168659 | 23.829 |
| w26 | 15 | 0.040002 | -3.605 |
| w27 | 12 | 0.173889 | 113.121 |
| w28 | 7 | -0.166199 | -8.888 |
| w29 | 8 | 0.270455 | 44.885 |
| w30 | 0 | -0.013055 | 0.0 |
| w31 | 8 | -0.105072 | -9.966 |
| w32 | 21 | 0.20022 | 64.128 |

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
| w17 | 13 | 0.028154 | -3.943 |
| w18 | 11 | 0.12544 | 1.79 |
| w19 | 3 | 0.107977 | 11.156 |
| w20 | 11 | -0.023324 | -7.023 |
| w21 | 9 | -0.109917 | -25.424 |
| w22 | 10 | 0.163325 | 45.524 |
| w23 | 8 | 0.007713 | -13.545 |
| w24 | 23 | 0.038521 | 35.066 |
| w25 | 13 | 0.066677 | 20.522 |
| w26 | 10 | -0.060639 | -8.675 |
| w27 | 20 | -0.007816 | 7.38 |
| w28 | 6 | -0.054194 | 0.124 |
| w29 | 16 | -0.02198 | -7.557 |
| w30 | 2 | 0.09535 | -0.328 |
| w31 | 8 | 0.050829 | -2.627 |
| w32 | 13 | 0.114201 | 32.673 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 6 | -0.212517 | -14.1 |
| w20 | 10 | -0.027693 | -7.498 |
| w21 | 13 | 0.028939 | 0.023 |
| w22 | 28 | -0.013255 | 51.095 |
| w23 | 9 | 0.04882 | -6.466 |
| w24 | 24 | 0.197953 | 148.877 |
| w25 | 6 | 0.003718 | -10.552 |
| w26 | 9 | -0.04509 | -16.913 |
| w27 | 10 | 0.010767 | 3.46 |
| w28 | 5 | -0.057924 | -7.895 |
| w29 | 12 | -0.093657 | -10.235 |
| w30 | 4 | 0.053527 | 0.082 |
| w31 | 11 | -0.171591 | -31.312 |
| w32 | 11 | 0.117743 | 53.376 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 12 | -0.043438 | 24.316 |
| w23 | 15 | -0.045447 | -8.336 |
| w24 | 19 | -0.06855 | -6.886 |
| w25 | 12 | -0.021456 | -10.682 |
| w26 | 10 | 0.13101 | 6.158 |
| w27 | 16 | -0.069111 | -9.976 |
| w28 | 8 | -0.04006 | -5.938 |
| w29 | 19 | 0.12706 | 12.66 |
| w30 | 5 | -0.001992 | -3.649 |
| w31 | 15 | -0.034364 | -10.034 |
| w32 | 8 | -0.008123 | 0.238 |

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
| w27 | 16 | 0.08307 | 28.359 |
| w28 | 11 | -0.176304 | -16.305 |
| w29 | 11 | 0.038034 | -2.155 |
| w30 | 3 | 0.067662 | -0.621 |
| w31 | 7 | -0.151982 | -14.059 |
| w32 | 16 | 0.223866 | 83.189 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 10 | -0.033987 | 2.257 |
| w18 | 9 | -0.074875 | -18.154 |
| w19 | 6 | 0.115637 | 7.611 |
| w20 | 4 | 0.019976 | 0.622 |
| w21 | 11 | -0.100295 | -17.839 |
| w22 | 13 | 0.012833 | 17.305 |
| w23 | 8 | -0.160075 | -24.583 |
| w24 | 15 | -0.150322 | 15.347 |
| w25 | 12 | 0.086166 | 13.538 |
| w26 | 7 | -0.037488 | -6.147 |
| w27 | 15 | -0.053505 | -17.438 |
| w28 | 1 | -0.267138 | -7.553 |
| w29 | 10 | 0.011751 | -9.427 |
| w30 | 7 | 0.183596 | 14.503 |
| w31 | 11 | -0.084303 | -17.049 |
| w32 | 3 | 0.06318 | 5.325 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 10 | 0.135052 | 9.66 |
| w18 | 8 | -0.197394 | -29.292 |
| w19 | 10 | 0.146928 | -15.285 |
| w20 | 9 | 0.017451 | -6.885 |
| w21 | 9 | -0.138169 | -15.836 |
| w22 | 15 | -0.036528 | 90.571 |
| w23 | 10 | 0.115618 | -4.335 |
| w24 | 13 | 0.096283 | 28.122 |
| w25 | 11 | 0.124084 | 32.128 |
| w26 | 8 | -0.030237 | -9.473 |
| w27 | 15 | -0.028404 | 8.837 |
| w28 | 2 | 0.064295 | -1.843 |
| w29 | 12 | 0.15074 | 3.761 |
| w30 | 3 | -0.048108 | 0.641 |
| w31 | 9 | -0.183135 | -8.439 |
| w32 | 17 | 0.126142 | 6.75 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 10 | -0.014974 | -6.048 |
| w29 | 14 | 0.069131 | 3.678 |
| w30 | 4 | 0.081985 | 3.39 |
| w31 | 10 | -0.070527 | -4.073 |
| w32 | 17 | 0.140213 | 20.944 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 5 | 0.212768 | 71.418 |
| w15 | 11 | -0.003677 | 14.138 |
| w16 | 12 | 0.055879 | 256.104 |
| w17 | 10 | -0.037952 | -7.191 |
| w18 | 9 | -0.063997 | -18.65 |
| w19 | 17 | -0.211335 | -28.429 |
| w20 | 8 | -0.167166 | -9.788 |
| w21 | 7 | 0.290831 | 97.24 |
| w22 | 13 | 0.189981 | 17.66 |
| w23 | 10 | -0.045955 | -2.491 |
| w24 | 15 | -0.088862 | -17.984 |
| w25 | 9 | 0.217663 | 53.747 |
| w26 | 10 | 0.038345 | -10.495 |
| w27 | 16 | 0.131019 | 43.354 |
| w28 | 6 | -0.194125 | -11.747 |
| w29 | 17 | 0.078139 | 37.137 |
| w30 | 4 | -0.004449 | -2.544 |
| w31 | 10 | -0.087801 | -11.098 |
| w32 | 6 | 0.34394 | 33.199 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 13 | 0.290593 | 141.237 |
| w26 | 8 | 0.081457 | 9.501 |
| w27 | 12 | 0.251047 | 50.375 |
| w28 | 5 | -0.118062 | -15.199 |
| w29 | 8 | 0.173179 | 22.046 |
| w30 | 4 | 0.024218 | -5.488 |
| w31 | 6 | 0.056703 | -4.574 |
| w32 | 12 | 0.230337 | 21.221 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

