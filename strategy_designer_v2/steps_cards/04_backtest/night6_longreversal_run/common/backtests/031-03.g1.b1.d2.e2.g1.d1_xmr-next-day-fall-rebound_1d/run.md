# Backtest of 031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound_1d

- Plan: `../../../../../03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 37 | 0.156837 | 8.399 |
| w2 | 36 | -0.033778 | 0.122 |
| w3 | 37 | -0.024968 | 6.163 |
| w4 | 20 | -0.152153 | -22.921 |
| w5 | 34 | 0.056669 | 16.481 |
| w6 | 33 | -0.051643 | 1.98 |
| w7 | 46 | 0.012579 | -0.693 |
| w8 | 38 | 0.082585 | 5.559 |
| w9 | 42 | 0.016191 | -22.684 |
| w10 | 30 | 0.081835 | 8.132 |
| w11 | 39 | 0.013531 | 7.957 |
| w12 | 47 | -0.004659 | -10.088 |
| w13 | 37 | 0.183656 | 17.456 |
| w14 | 36 | 0.082981 | 13.147 |
| w15 | 32 | -0.062691 | 3.511 |
| w16 | 36 | -0.00868 | 2.03 |
| w17 | 47 | 0.270025 | 27.229 |
| w18 | 37 | -0.072046 | -10.018 |
| w19 | 41 | -0.016109 | -6.573 |
| w20 | 46 | 0.040561 | -8.097 |
| w21 | 38 | -0.035133 | -15.245 |
| w22 | 35 | -0.045478 | 3.808 |
| w23 | 42 | 0.002495 | -11.104 |
| w24 | 35 | 0.138994 | 18.525 |
| w25 | 26 | 0.165692 | 20.491 |
| w26 | 48 | 0.00547 | -4.692 |
| w27 | 37 | -0.112544 | -0.935 |
| w28 | 37 | 0.026374 | -3.197 |
| w29 | 44 | 0.004339 | 1.217 |
| w30 | 45 | -0.040185 | -10.637 |
| w31 | 39 | 0.049381 | -7.854 |
| w32 | 44 | -0.20061 | -20.843 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 45 | 0.31968 | 40.114 |
| w2 | 39 | -0.077078 | -8.402 |
| w3 | 50 | 0.071533 | 10.922 |
| w4 | 33 | -0.05188 | 1.159 |
| w5 | 37 | 0.040374 | 12.542 |
| w6 | 36 | 0.129842 | 20.829 |
| w7 | 44 | 0.04609 | 3.182 |
| w8 | 49 | 0.124875 | -0.8 |
| w9 | 49 | 0.114875 | 0.242 |
| w10 | 39 | 0.03438 | 6.863 |
| w11 | 47 | 0.024111 | -0.735 |
| w12 | 43 | -0.064786 | -18.075 |
| w13 | 35 | 0.160146 | 14.336 |
| w14 | 46 | 0.212318 | 25.423 |
| w15 | 36 | 0.045398 | 9.802 |
| w16 | 39 | -0.054441 | 0.868 |
| w17 | 41 | 0.237659 | 27.509 |
| w18 | 42 | -0.05108 | -8.564 |
| w19 | 49 | 0.014575 | -5.78 |
| w20 | 46 | 0.099109 | 2.466 |
| w21 | 37 | 0.042017 | 5.385 |
| w22 | 44 | 0.019427 | 1.811 |
| w23 | 37 | -0.102006 | -13.578 |
| w24 | 43 | 0.065221 | 5.446 |
| w25 | 38 | 0.060942 | 6.905 |
| w26 | 43 | 0.032762 | -11.169 |
| w27 | 40 | -0.094574 | -8.376 |
| w28 | 37 | -0.100546 | -8.727 |
| w29 | 40 | 0.135397 | 11.437 |
| w30 | 48 | -0.037674 | -6.832 |
| w31 | 46 | 0.139598 | 3.686 |
| w32 | 48 | -0.081748 | -16.638 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 37 | -0.04589 | 9.612 |
| w7 | 44 | 0.028742 | 0.705 |
| w8 | 49 | 0.065789 | -9.824 |
| w9 | 38 | 0.050488 | 5.335 |
| w10 | 43 | 0.251206 | 15.324 |
| w11 | 42 | 0.048259 | 2.379 |
| w12 | 53 | -0.006375 | -11.28 |
| w13 | 38 | 0.080373 | 2.275 |
| w14 | 42 | 0.155591 | 19.925 |
| w15 | 38 | 0.082598 | 9.44 |
| w16 | 36 | 0.032587 | 12.814 |
| w17 | 39 | 0.18599 | 15.063 |
| w18 | 43 | 0.075631 | 1.766 |
| w19 | 45 | 0.038244 | -2.879 |
| w20 | 22 | 0.112499 | 2.547 |
| w21 | 41 | 0.157321 | 23.964 |
| w22 | 44 | 0.305144 | 40.516 |
| w23 | 41 | -0.013885 | 21.619 |
| w24 | 36 | 0.14704 | 15.829 |
| w25 | 38 | 0.064568 | 2.545 |
| w26 | 37 | -0.035259 | -8.379 |
| w27 | 35 | -0.095942 | 1.629 |
| w28 | 39 | 0.067591 | 4.206 |
| w29 | 44 | 0.126731 | 14.188 |
| w30 | 43 | -0.043495 | -12.357 |
| w31 | 49 | 0.062315 | -6.609 |
| w32 | 51 | -0.135094 | -19.515 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 46 | -0.024581 | -2.664 |
| w8 | 47 | 0.13878 | 0.561 |
| w9 | 52 | -0.114109 | -29.157 |
| w10 | 36 | 0.062683 | 6.045 |
| w11 | 36 | 0.090204 | 3.742 |
| w12 | 42 | -0.162131 | -30.762 |
| w13 | 32 | 0.100755 | 8.067 |
| w14 | 41 | 0.25856 | 22.673 |
| w15 | 38 | -0.035234 | -10.624 |
| w16 | 38 | 0.004883 | 7.729 |
| w17 | 45 | 0.222453 | 22.993 |
| w18 | 42 | 0.033319 | -6.833 |
| w19 | 49 | -0.027257 | -15.156 |
| w20 | 48 | 0.111375 | -0.787 |
| w21 | 44 | 0.158851 | 4.07 |
| w22 | 36 | 0.027951 | 0.348 |
| w23 | 44 | 0.035021 | 18.9 |
| w24 | 45 | 0.113114 | 11.038 |
| w25 | 36 | 0.032547 | 4.435 |
| w26 | 51 | 0.015875 | -9.162 |
| w27 | 40 | -0.023035 | 1.417 |
| w28 | 44 | -0.003788 | -6.324 |
| w29 | 45 | 0.069641 | 5.966 |
| w30 | 48 | 0.011489 | -2.121 |
| w31 | 41 | 0.242625 | 14.839 |
| w32 | 49 | -0.106067 | -35.077 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 32 | -0.064361 | 6.19 |
| w2 | 33 | 0.001636 | -2.709 |
| w3 | 44 | 0.174602 | 11.82 |
| w4 | 23 | 0.090314 | 17.637 |
| w5 | 40 | -0.04044 | 4.538 |
| w6 | 38 | 0.126624 | 19.772 |
| w7 | 43 | -0.053055 | -4.053 |
| w8 | 48 | 0.089446 | -2.316 |
| w9 | 42 | 0.044947 | -8.937 |
| w10 | 38 | 0.119636 | 7.793 |
| w11 | 42 | 0.020481 | 2.077 |
| w12 | 44 | -0.028536 | -11.582 |
| w13 | 36 | 0.151679 | 12.9 |
| w14 | 42 | 0.133678 | 16.694 |
| w15 | 38 | 0.047473 | 6.971 |
| w16 | 29 | 0.058821 | 15.852 |
| w17 | 36 | 0.18627 | 20.084 |
| w18 | 37 | 0.107337 | 8.553 |
| w19 | 46 | -0.090504 | -12.665 |
| w20 | 43 | 0.010577 | -9.426 |
| w21 | 38 | 0.107261 | 3.89 |
| w22 | 41 | 0.073025 | 12.705 |
| w23 | 47 | 0.056943 | -4.556 |
| w24 | 44 | 0.115082 | 15.591 |
| w25 | 33 | 0.079302 | 9.78 |
| w26 | 43 | -0.015454 | -10.045 |
| w27 | 44 | -0.10556 | -4.843 |
| w28 | 46 | 0.091186 | 1.388 |
| w29 | 38 | -0.055596 | 2.886 |
| w30 | 40 | -0.034539 | -9.629 |
| w31 | 44 | -0.02583 | -12.889 |
| w32 | 41 | -0.131558 | -15.511 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 42 | 0.147449 | 13.591 |
| w11 | 46 | 0.086283 | 2.897 |
| w12 | 43 | -0.103505 | -18.591 |
| w13 | 33 | 0.132075 | 9.651 |
| w14 | 34 | 0.213414 | 24.633 |
| w15 | 46 | 0.06757 | 7.792 |
| w16 | 31 | 0.015372 | 9.202 |
| w17 | 38 | 0.290351 | 37.813 |
| w18 | 47 | 0.068084 | -4.687 |
| w19 | 47 | -0.001477 | -6.864 |
| w20 | 46 | 0.08223 | 1.932 |
| w21 | 45 | 0.095583 | -3.871 |
| w22 | 38 | 0.14271 | 15.503 |
| w23 | 52 | 0.032064 | -5.252 |
| w24 | 33 | -0.005355 | 10.656 |
| w25 | 46 | 0.129109 | 5.46 |
| w26 | 51 | 0.041117 | -5.434 |
| w27 | 36 | -0.121038 | -3.352 |
| w28 | 37 | 0.026726 | -0.198 |
| w29 | 43 | -0.005425 | -0.32 |
| w30 | 51 | -0.013711 | -13.742 |
| w31 | 43 | 0.16862 | 6.645 |
| w32 | 41 | -0.31914 | -40.598 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 41 | -0.001767 | 2.814 |
| w13 | 38 | 0.00785 | -10.38 |
| w14 | 41 | 0.15765 | 28.463 |
| w15 | 41 | 0.220309 | 20.562 |
| w16 | 43 | 0.020474 | 8.111 |
| w17 | 39 | 0.21917 | 24.8 |
| w18 | 46 | 0.023751 | 1.436 |
| w19 | 48 | 0.17755 | 2.277 |
| w20 | 41 | 0.005905 | -3.906 |
| w21 | 34 | 0.069679 | 0.103 |
| w22 | 44 | 0.15195 | 11.838 |
| w23 | 47 | -0.000727 | -21.164 |
| w24 | 37 | 0.141945 | 11.942 |
| w25 | 41 | -0.029134 | -7.598 |
| w26 | 47 | 0.041695 | -16.142 |
| w27 | 43 | -0.114511 | -8.517 |
| w28 | 47 | -0.04324 | -10.403 |
| w29 | 44 | -0.112868 | -14.925 |
| w30 | 46 | 0.003004 | -16.274 |
| w31 | 45 | 0.046641 | -2.647 |
| w32 | 51 | 0.061291 | -4.594 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 42 | 0.189164 | 11.21 |
| w16 | 39 | -0.063584 | 0.273 |
| w17 | 42 | 0.31278 | 33.985 |
| w18 | 42 | 0.192595 | 31.141 |
| w19 | 42 | 0.004587 | -15.365 |
| w20 | 50 | 0.077349 | -0.407 |
| w21 | 34 | 0.054618 | -1.313 |
| w22 | 42 | -0.011806 | -4.703 |
| w23 | 50 | -0.086475 | -25.502 |
| w24 | 37 | 0.007505 | 5.959 |
| w25 | 47 | 0.045393 | -1.489 |
| w26 | 47 | -0.030232 | -12.388 |
| w27 | 46 | -0.095542 | -5.407 |
| w28 | 41 | 0.023094 | -4.402 |
| w29 | 44 | -0.018435 | -4.03 |
| w30 | 48 | -0.043475 | -16.516 |
| w31 | 41 | 0.014146 | -3.224 |
| w32 | 48 | -0.138663 | -17.038 |

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
| w15 | 37 | 0.08186 | 11.122 |
| w16 | 39 | -0.030787 | 6.58 |
| w17 | 41 | 0.268968 | 20.953 |
| w18 | 38 | 0.175753 | 16.227 |
| w19 | 45 | -0.004938 | -8.265 |
| w20 | 38 | 0.202112 | 26.737 |
| w21 | 39 | 0.099425 | -2.422 |
| w22 | 37 | 0.166315 | 16.797 |
| w23 | 41 | -0.034959 | -3.272 |
| w24 | 32 | 0.161047 | 20.32 |
| w25 | 39 | 0.018249 | -6.304 |
| w26 | 46 | -0.074061 | -5.996 |
| w27 | 34 | -0.055282 | -3.377 |
| w28 | 49 | 0.045915 | 4.882 |
| w29 | 34 | 0.044877 | 5.661 |
| w30 | 40 | 0.08768 | -2.386 |
| w31 | 46 | 0.094567 | 4.464 |
| w32 | 38 | -0.225621 | -19.634 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 36 | -0.079278 | -2.153 |
| w17 | 40 | 0.227024 | 31.046 |
| w18 | 46 | -0.010193 | -6.161 |
| w19 | 47 | -0.019812 | -11.227 |
| w20 | 45 | 0.085921 | -0.141 |
| w21 | 48 | 0.114147 | -3.389 |
| w22 | 38 | 0.085293 | 6.287 |
| w23 | 47 | 0.008596 | -16.152 |
| w24 | 39 | -0.024013 | -2.555 |
| w25 | 37 | 0.091621 | 2.436 |
| w26 | 42 | -0.1067 | -22.03 |
| w27 | 43 | -0.109018 | -9.352 |
| w28 | 47 | -0.045936 | -11.968 |
| w29 | 42 | -0.052192 | -10.294 |
| w30 | 46 | -0.091393 | -17.35 |
| w31 | 41 | 0.057163 | -1.261 |
| w32 | 59 | -0.064651 | -20.145 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 52 | -0.016134 | -12.021 |
| w21 | 43 | 0.09602 | -3.572 |
| w22 | 40 | -0.044052 | -0.191 |
| w23 | 49 | 0.030387 | -10.284 |
| w24 | 30 | -0.110437 | -0.801 |
| w25 | 47 | 0.131999 | 10.437 |
| w26 | 48 | -0.084751 | -13.55 |
| w27 | 47 | -0.056915 | -1.061 |
| w28 | 46 | -0.049196 | -10.524 |
| w29 | 41 | -0.087648 | -6.252 |
| w30 | 42 | -0.024344 | -9.274 |
| w31 | 45 | 0.113485 | 3.019 |
| w32 | 45 | -0.023326 | -10.606 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 38 | 0.031126 | 3.956 |
| w23 | 47 | -0.063008 | -18.009 |
| w24 | 32 | -0.017199 | 2.879 |
| w25 | 39 | 0.049751 | 9.13 |
| w26 | 45 | -0.08428 | -14.299 |
| w27 | 40 | -0.075422 | -4.872 |
| w28 | 41 | -0.02567 | -11.562 |
| w29 | 41 | -0.032902 | -4.179 |
| w30 | 46 | -0.102469 | -11.583 |
| w31 | 42 | 0.016806 | -2.569 |
| w32 | 45 | -0.042612 | 4.462 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 45 | 0.197656 | 25.533 |
| w25 | 39 | -0.011201 | -2.121 |
| w26 | 47 | -0.022456 | -9.091 |
| w27 | 36 | 0.08594 | 13.774 |
| w28 | 47 | 0.033152 | 3.6 |
| w29 | 45 | 0.071431 | 7.122 |
| w30 | 41 | 0.046414 | -5.998 |
| w31 | 41 | 0.017814 | -4.431 |
| w32 | 46 | 0.017738 | 3.606 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 39 | -0.043246 | 4.727 |
| w6 | 37 | 0.1556 | 23.178 |
| w7 | 50 | 0.093179 | 5.98 |
| w8 | 44 | 0.171527 | 6.252 |
| w9 | 53 | 0.021906 | -15.288 |
| w10 | 43 | 0.172731 | 10.061 |
| w11 | 45 | 0.092251 | 3.608 |
| w12 | 43 | -0.069283 | -18.412 |
| w13 | 35 | -0.021788 | 0.663 |
| w14 | 44 | 0.102415 | 12.809 |
| w15 | 42 | 0.134782 | 10.429 |
| w16 | 33 | -0.016254 | 6.19 |
| w17 | 39 | 0.313441 | 34.585 |
| w18 | 42 | 0.020082 | 3.317 |
| w19 | 40 | -0.10486 | -10.418 |
| w20 | 46 | 0.106534 | 1.822 |
| w21 | 38 | 0.105083 | 0.835 |
| w22 | 42 | 0.074909 | 4.364 |
| w23 | 41 | -0.055607 | -13.856 |
| w24 | 40 | 0.126731 | 10.791 |
| w25 | 48 | 0.057009 | 0.066 |
| w26 | 40 | -0.080723 | -3.077 |
| w27 | 43 | -0.088648 | -3.019 |
| w28 | 41 | -0.075992 | -11.264 |
| w29 | 45 | 0.04878 | 5.505 |
| w30 | 33 | -0.057726 | 10.43 |
| w31 | 46 | -0.037284 | -6.447 |
| w32 | 38 | -0.033611 | 5.464 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 39 | -0.01941 | 6.229 |
| w6 | 41 | 0.190371 | 20.559 |
| w7 | 47 | 0.133021 | 10.324 |
| w8 | 47 | 0.192497 | 10.604 |
| w9 | 44 | 0.096393 | -6.532 |
| w10 | 38 | 0.180357 | 13.778 |
| w11 | 38 | -0.034341 | -3.949 |
| w12 | 47 | 0.075213 | -3.841 |
| w13 | 43 | 0.13546 | 7.911 |
| w14 | 41 | 0.300603 | 34.753 |
| w15 | 40 | 0.178718 | 17.712 |
| w16 | 35 | 0.081422 | 15.582 |
| w17 | 40 | 0.350075 | 41.349 |
| w18 | 42 | 0.003782 | -5.475 |
| w19 | 46 | 0.036563 | -1.034 |
| w20 | 39 | 0.051661 | 0.406 |
| w21 | 34 | 0.105048 | 0.539 |
| w22 | 41 | 0.18723 | 15.578 |
| w23 | 45 | 0.049508 | -9.224 |
| w24 | 45 | 0.158804 | 11.078 |
| w25 | 41 | 0.272219 | 28.238 |
| w26 | 35 | 0.28641 | 28.223 |
| w27 | 34 | 0.024041 | -0.814 |
| w28 | 35 | 0.101322 | 11.432 |
| w29 | 47 | -0.0627 | -10.214 |
| w30 | 31 | -0.101912 | -3.949 |
| w31 | 39 | 0.127914 | 13.259 |
| w32 | 34 | 0.162933 | 26.244 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 45 | 0.120553 | 10.074 |
| w18 | 46 | -0.033953 | 1.082 |
| w19 | 51 | -0.013007 | -8.925 |
| w20 | 43 | -0.017011 | -5.811 |
| w21 | 42 | 0.135397 | -1.006 |
| w22 | 41 | 0.081917 | 8.555 |
| w23 | 50 | 0.151091 | 3.736 |
| w24 | 42 | 0.078094 | 7.592 |
| w25 | 39 | 0.137269 | 8.038 |
| w26 | 49 | 0.090346 | 0.422 |
| w27 | 43 | -0.029475 | 8.026 |
| w28 | 42 | 0.051784 | 2.056 |
| w29 | 48 | -0.060399 | -5.786 |
| w30 | 47 | -0.060197 | -14.492 |
| w31 | 47 | 0.128334 | -0.153 |
| w32 | 47 | -0.039277 | -3.275 |

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
| w17 | 40 | 0.16087 | 16.351 |
| w18 | 46 | -0.087325 | -19.114 |
| w19 | 46 | -0.021842 | -7.777 |
| w20 | 55 | 0.013131 | -2.379 |
| w21 | 42 | 0.103519 | 1.251 |
| w22 | 39 | 0.090976 | 7.642 |
| w23 | 45 | -0.072133 | -12.484 |
| w24 | 37 | -0.049391 | 1.892 |
| w25 | 40 | 0.134094 | 14.148 |
| w26 | 39 | -0.091559 | -6.668 |
| w27 | 42 | 0.013916 | 8.804 |
| w28 | 40 | 0.143126 | 8.637 |
| w29 | 44 | 0.039438 | 9.05 |
| w30 | 43 | -0.007221 | -10.052 |
| w31 | 43 | 0.089522 | 2.589 |
| w32 | 49 | -0.103736 | -5.85 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 49 | -0.059797 | -20.377 |
| w20 | 49 | 0.057422 | -0.157 |
| w21 | 43 | 0.10474 | 5.327 |
| w22 | 33 | 0.030362 | 21.56 |
| w23 | 50 | 0.000661 | -5.295 |
| w24 | 35 | 0.005018 | 8.951 |
| w25 | 43 | 0.019795 | -6.053 |
| w26 | 47 | 0.035005 | -2.535 |
| w27 | 47 | -0.04706 | -3.956 |
| w28 | 44 | -0.018541 | -10.952 |
| w29 | 41 | -0.112525 | -8.932 |
| w30 | 49 | -0.01793 | -13.525 |
| w31 | 47 | 0.121517 | 4.321 |
| w32 | 49 | -0.024134 | -0.873 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 44 | 0.15318 | 14.031 |
| w23 | 44 | 0.134696 | 6.994 |
| w24 | 43 | 0.203749 | 22.442 |
| w25 | 41 | -0.088718 | -14.09 |
| w26 | 51 | 0.015983 | -5.172 |
| w27 | 40 | -0.106342 | -6.451 |
| w28 | 47 | 0.041709 | -3.564 |
| w29 | 47 | -0.132791 | -10.115 |
| w30 | 46 | 0.066649 | -3.619 |
| w31 | 47 | 0.080343 | 1.547 |
| w32 | 37 | -0.081605 | -7.749 |

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
| w27 | 45 | 0.020753 | 6.569 |
| w28 | 51 | 0.143585 | 8.349 |
| w29 | 43 | -0.019361 | -2.09 |
| w30 | 48 | -0.026885 | -13.417 |
| w31 | 40 | 0.120327 | 6.022 |
| w32 | 45 | 0.014704 | 5.271 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 47 | 0.299674 | 24.782 |
| w18 | 46 | -0.013963 | -13.005 |
| w19 | 50 | -0.037869 | -14.272 |
| w20 | 49 | -0.003513 | -8.674 |
| w21 | 41 | 0.022596 | -11.555 |
| w22 | 38 | 0.083507 | 8.006 |
| w23 | 44 | -0.069239 | -22.022 |
| w24 | 33 | -0.000197 | -0.682 |
| w25 | 42 | -0.031272 | -6.581 |
| w26 | 44 | 0.126892 | -0.833 |
| w27 | 45 | -0.084608 | -5.938 |
| w28 | 42 | -0.0313 | -9.595 |
| w29 | 44 | -0.004786 | -7.414 |
| w30 | 41 | -0.079124 | -13.939 |
| w31 | 46 | 0.085433 | -2.352 |
| w32 | 50 | 0.137713 | 8.816 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 44 | 0.241133 | 21.409 |
| w18 | 46 | 0.076944 | 4.014 |
| w19 | 51 | 0.016296 | -4.524 |
| w20 | 46 | 0.002157 | -7.218 |
| w21 | 36 | 0.026131 | -9.544 |
| w22 | 32 | 0.018778 | 7.795 |
| w23 | 49 | -0.09245 | -18.13 |
| w24 | 37 | 0.035379 | 8.749 |
| w25 | 48 | 0.04655 | 4.392 |
| w26 | 51 | 0.004744 | -8.679 |
| w27 | 40 | -0.122128 | -7.342 |
| w28 | 45 | -0.010166 | -10.926 |
| w29 | 42 | -0.011901 | -4.799 |
| w30 | 49 | -0.008098 | -17.99 |
| w31 | 45 | 0.171015 | 4.443 |
| w32 | 58 | 0.011754 | -11.905 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 41 | -0.006476 | -3.111 |
| w29 | 45 | 0.118992 | 7.339 |
| w30 | 50 | -0.048774 | -7.123 |
| w31 | 43 | 0.02895 | 2.265 |
| w32 | 46 | 0.080685 | 7.885 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 40 | 0.034905 | 11.547 |
| w15 | 37 | -0.019666 | 5.967 |
| w16 | 26 | 0.077323 | 47.006 |
| w17 | 39 | 0.148486 | 8.682 |
| w18 | 42 | 0.154642 | 10.468 |
| w19 | 46 | 0.055313 | 3.415 |
| w20 | 48 | 0.022731 | -6.413 |
| w21 | 41 | 0.028557 | 7.385 |
| w22 | 48 | 0.061009 | 5.76 |
| w23 | 40 | 0.086657 | 4.559 |
| w24 | 38 | 0.028725 | 6.075 |
| w25 | 36 | -0.00707 | 3.04 |
| w26 | 48 | -0.036017 | -10.503 |
| w27 | 38 | -0.160539 | -3.243 |
| w28 | 45 | 0.006388 | -5.214 |
| w29 | 41 | -0.044814 | -2.301 |
| w30 | 42 | 0.007084 | -6.487 |
| w31 | 43 | 0.062113 | 3.59 |
| w32 | 45 | -0.086816 | -17.476 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 55 | -0.007257 | 3.853 |
| w26 | 50 | -0.038534 | -2.923 |
| w27 | 39 | -0.124101 | -3.937 |
| w28 | 46 | 0.017363 | -6.264 |
| w29 | 43 | -0.091383 | -7.431 |
| w30 | 43 | 0.054393 | -7.963 |
| w31 | 41 | 0.128231 | 7.648 |
| w32 | 47 | -0.140116 | -23.824 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

