# Backtest of 031-01.g1_weekly-gains-carry-into-saturday_1d

- Plan: `../../../../../03_test_plan/night6_yearlow_run/plans/031-01.g1_weekly-gains-carry-into-saturday_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.022211 | -0.853 |
| w2 | 8 | 0.198988 | 25.789 |
| w3 | 12 | -0.063177 | -0.557 |
| w4 | 9 | -0.020381 | -0.317 |
| w5 | 11 | 0.052169 | 9.709 |
| w6 | 11 | -0.01783 | 3.806 |
| w7 | 7 | 0.116119 | 6.013 |
| w8 | 8 | 0.059874 | 2.164 |
| w9 | 4 | 0.109365 | 3.268 |
| w10 | 8 | 0.083468 | 6.764 |
| w11 | 10 | 0.117364 | 22.865 |
| w12 | 6 | 0.055352 | 1.805 |
| w13 | 10 | -0.038219 | -5.601 |
| w14 | 10 | 0.124932 | 12.772 |
| w15 | 11 | -0.004259 | 2.914 |
| w16 | 11 | 0.068236 | 9.981 |
| w17 | 9 | -0.024958 | -2.009 |
| w18 | 8 | -0.014714 | -1.636 |
| w19 | 7 | 0.036191 | 1.011 |
| w20 | 5 | 0.013813 | -0.74 |
| w21 | 9 | 0.028726 | 0.627 |
| w22 | 9 | 0.009056 | 7.529 |
| w23 | 3 | -0.017493 | -0.743 |
| w24 | 9 | -0.045855 | -0.419 |
| w25 | 7 | -0.037597 | -1.593 |
| w26 | 7 | 0.037287 | 3.286 |
| w27 | 9 | -0.083136 | -4.358 |
| w28 | 10 | 0.03725 | 2.176 |
| w29 | 5 | 0.029298 | 1.392 |
| w30 | 5 | 0.015408 | -0.685 |
| w31 | 8 | -0.022315 | -3.591 |
| w32 | 5 | -0.028089 | -2.08 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.09692 | -8.955 |
| w2 | 6 | -0.011971 | -1.675 |
| w3 | 9 | -0.090026 | -4.536 |
| w4 | 9 | 0.009578 | -0.575 |
| w5 | 10 | 0.050145 | 3.479 |
| w6 | 9 | 0.111137 | 23.476 |
| w7 | 5 | -0.048353 | -4.975 |
| w8 | 7 | 0.091506 | 1.023 |
| w9 | 5 | 0.104999 | 3.782 |
| w10 | 9 | 0.117691 | 10.089 |
| w11 | 8 | 0.070929 | 3.786 |
| w12 | 6 | -0.050002 | -4.417 |
| w13 | 11 | -0.017112 | -1.983 |
| w14 | 7 | 0.27701 | 22.703 |
| w15 | 8 | 0.086004 | 6.922 |
| w16 | 10 | 0.083553 | 7.645 |
| w17 | 8 | -0.02783 | -1.914 |
| w18 | 9 | 0.022627 | 0.88 |
| w19 | 5 | 0.106666 | 3.993 |
| w20 | 4 | 0.03609 | -0.013 |
| w21 | 10 | 0.038105 | 3.109 |
| w22 | 10 | -0.084055 | -6.252 |
| w23 | 4 | -0.024704 | -2.618 |
| w24 | 11 | -0.043431 | -3.474 |
| w25 | 7 | 0.022172 | 5.626 |
| w26 | 5 | 0.047062 | 1.479 |
| w27 | 9 | 0.159555 | 27.196 |
| w28 | 8 | -0.038131 | -2.898 |
| w29 | 7 | 0.134811 | 13.611 |
| w30 | 5 | 0.037458 | 0.76 |
| w31 | 6 | -0.028662 | -4.614 |
| w32 | 5 | 0.0025 | -1.795 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 10 | -0.076356 | -3.715 |
| w7 | 5 | -0.01057 | -3.367 |
| w8 | 4 | -0.156351 | -7.642 |
| w9 | 5 | 0.025591 | 1.846 |
| w10 | 5 | 0.001719 | -1.195 |
| w11 | 6 | -0.04892 | -3.014 |
| w12 | 6 | -0.029762 | -3.183 |
| w13 | 11 | -0.064741 | -8.986 |
| w14 | 7 | 0.320469 | 25.252 |
| w15 | 8 | 0.260103 | 59.167 |
| w16 | 10 | 0.169914 | 19.912 |
| w17 | 6 | 0.124829 | 10.544 |
| w18 | 4 | -0.002682 | -0.587 |
| w19 | 7 | 0.114182 | 4.91 |
| w20 | 4 | 0.087189 | 2.073 |
| w21 | 8 | -0.079721 | -7.898 |
| w22 | 11 | -0.056423 | -4.733 |
| w23 | 6 | -0.031638 | -3.351 |
| w24 | 8 | -0.043655 | -1.838 |
| w25 | 5 | 0.045561 | 3.628 |
| w26 | 8 | 0.206514 | 22.942 |
| w27 | 9 | 0.246198 | 38.501 |
| w28 | 8 | 0.017171 | 1.062 |
| w29 | 5 | 0.043549 | 4.13 |
| w30 | 4 | 0.033238 | 0.184 |
| w31 | 5 | -0.037215 | -5.385 |
| w32 | 3 | 0.050149 | 3.281 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 7 | 0.006921 | -0.101 |
| w8 | 5 | 0.042561 | -0.478 |
| w9 | 4 | 0.026775 | -0.401 |
| w10 | 7 | 0.131185 | 11.337 |
| w11 | 5 | 0.028142 | 1.099 |
| w12 | 7 | -0.020294 | -3.205 |
| w13 | 11 | -0.102671 | -12.083 |
| w14 | 8 | 0.166181 | 12.542 |
| w15 | 6 | 0.093977 | 9.285 |
| w16 | 9 | 0.039995 | 2.202 |
| w17 | 7 | 0.041592 | 5.5 |
| w18 | 7 | 0.031256 | -0.394 |
| w19 | 7 | 0.160257 | 6.25 |
| w20 | 3 | -0.037245 | -2.905 |
| w21 | 9 | -0.0236 | -3.447 |
| w22 | 9 | -0.034964 | -3.805 |
| w23 | 5 | 0.086534 | 4.968 |
| w24 | 6 | 0.031337 | 1.545 |
| w25 | 6 | 0.345851 | 58.192 |
| w26 | 7 | 0.059207 | 1.627 |
| w27 | 7 | 0.065927 | 6.048 |
| w28 | 6 | 0.042422 | -0.15 |
| w29 | 12 | -0.205753 | -18.616 |
| w30 | 7 | -0.075772 | -8.905 |
| w31 | 10 | -0.033988 | -5.886 |
| w32 | 3 | 0.000112 | -1.788 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.065205 | 14.395 |
| w2 | 8 | -0.04949 | -2.679 |
| w3 | 7 | -0.070036 | -5.513 |
| w4 | 10 | -0.243861 | -17.034 |
| w5 | 10 | 0.064683 | 9.558 |
| w6 | 7 | -0.034755 | -0.062 |
| w7 | 6 | 0.057974 | 4.204 |
| w8 | 4 | 0.11464 | 1.988 |
| w9 | 5 | 0.106681 | 5.652 |
| w10 | 9 | 0.056758 | 2.716 |
| w11 | 6 | 0.065597 | 6.34 |
| w12 | 5 | -0.05274 | -4.66 |
| w13 | 13 | -0.039949 | -5.101 |
| w14 | 9 | 0.324669 | 36.322 |
| w15 | 8 | 0.030213 | 4.23 |
| w16 | 11 | -0.090764 | -4.288 |
| w17 | 9 | 0.112589 | 14.049 |
| w18 | 8 | -0.008503 | -0.78 |
| w19 | 6 | 0.040743 | 1.561 |
| w20 | 7 | 0.068878 | 2.868 |
| w21 | 9 | 0.031553 | 1.821 |
| w22 | 10 | 0.00293 | 3.802 |
| w23 | 6 | -0.131547 | -6.753 |
| w24 | 11 | -0.045756 | -1.477 |
| w25 | 8 | 0.011398 | 2.334 |
| w26 | 6 | 0.046036 | 2.555 |
| w27 | 9 | 0.119758 | 12.119 |
| w28 | 7 | -0.000392 | -2.625 |
| w29 | 9 | 0.119004 | 16.3 |
| w30 | 3 | -0.032125 | -2.263 |
| w31 | 8 | -0.006196 | -1.843 |
| w32 | 4 | -0.054479 | -2.89 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 8 | 0.124625 | 13.6 |
| w11 | 5 | -0.054941 | -3.387 |
| w12 | 5 | -0.043708 | -4.41 |
| w13 | 13 | -0.06952 | -10.001 |
| w14 | 11 | 0.213936 | 22.209 |
| w15 | 6 | 0.062436 | 5.022 |
| w16 | 9 | 0.08499 | 11.462 |
| w17 | 11 | -0.021231 | 1.358 |
| w18 | 3 | 0.086798 | 2.405 |
| w19 | 4 | 0.116685 | 6.208 |
| w20 | 6 | 0.096366 | 3.857 |
| w21 | 6 | 0.158601 | 7.045 |
| w22 | 11 | -0.030529 | -1.008 |
| w23 | 2 | -0.040383 | -4.21 |
| w24 | 8 | 0.035075 | 7.41 |
| w25 | 6 | 0.068648 | 4.588 |
| w26 | 6 | 0.117873 | 6.818 |
| w27 | 9 | 0.114301 | 16.033 |
| w28 | 5 | -0.025868 | -3.599 |
| w29 | 6 | 0.084833 | 6.29 |
| w30 | 4 | -0.004933 | -1.689 |
| w31 | 7 | -0.060008 | -5.63 |
| w32 | 6 | 0.071393 | 3.09 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 7 | 0.006972 | 0.073 |
| w13 | 10 | -0.120848 | -18.839 |
| w14 | 9 | -0.029993 | -0.259 |
| w15 | 6 | 0.066137 | 2.056 |
| w16 | 11 | -0.078468 | -4.776 |
| w17 | 10 | 0.110642 | 13.51 |
| w18 | 6 | -0.075447 | -8.105 |
| w19 | 7 | -0.011277 | -1.925 |
| w20 | 8 | -0.032447 | -4.291 |
| w21 | 9 | 0.001222 | -1.89 |
| w22 | 9 | -0.063786 | -4.9 |
| w23 | 4 | 0.039433 | -0.179 |
| w24 | 9 | 0.097789 | 9.527 |
| w25 | 6 | 0.058028 | 2.868 |
| w26 | 6 | 0.14263 | 4.838 |
| w27 | 6 | 0.074591 | 7.337 |
| w28 | 8 | 0.00778 | -1.618 |
| w29 | 6 | 0.166661 | 9.692 |
| w30 | 3 | 0.042703 | 0.008 |
| w31 | 10 | 0.020605 | -1.745 |
| w32 | 7 | -0.048364 | -7.91 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 7 | 0.078167 | 3.918 |
| w16 | 10 | -0.043752 | -0.386 |
| w17 | 7 | -0.07368 | -6.345 |
| w18 | 8 | -0.049425 | -5.336 |
| w19 | 3 | 0.084088 | 2.684 |
| w20 | 5 | 0.122809 | 5.55 |
| w21 | 7 | -4e-06 | -2.943 |
| w22 | 9 | -0.008723 | -1.573 |
| w23 | 5 | 0.011117 | -1.557 |
| w24 | 9 | 0.0896 | 11.338 |
| w25 | 8 | -0.043069 | -6.023 |
| w26 | 7 | 0.119077 | 4.866 |
| w27 | 8 | 0.094574 | 13.307 |
| w28 | 8 | -0.027382 | -2.513 |
| w29 | 5 | 0.101668 | 6.926 |
| w30 | 5 | 0.017568 | -1.148 |
| w31 | 5 | -0.064933 | -5.618 |
| w32 | 8 | -0.144768 | -11.528 |

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
| w15 | 7 | -0.096121 | 3.172 |
| w16 | 9 | -0.001963 | 3.272 |
| w17 | 7 | 0.04552 | 5.072 |
| w18 | 7 | 0.059765 | 2.802 |
| w19 | 7 | 0.036617 | 0.72 |
| w20 | 7 | -0.067086 | -3.485 |
| w21 | 9 | -0.045894 | -5.552 |
| w22 | 8 | 0.000461 | 1.008 |
| w23 | 12 | 0.005499 | -0.227 |
| w24 | 10 | 0.032887 | 4.908 |
| w25 | 8 | 0.111553 | 9.377 |
| w26 | 10 | 0.054918 | 7.714 |
| w27 | 9 | 0.012094 | 12.333 |
| w28 | 9 | 0.021347 | 2.35 |
| w29 | 13 | -0.068757 | -5.156 |
| w30 | 6 | -0.016717 | -2.065 |
| w31 | 10 | 0.245394 | 15.012 |
| w32 | 11 | 0.037161 | 0.305 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 8 | 0.226208 | 22.635 |
| w17 | 9 | -0.070539 | -6.765 |
| w18 | 8 | -0.033435 | -3.524 |
| w19 | 7 | 0.124552 | 4.086 |
| w20 | 6 | 5e-05 | -1.448 |
| w21 | 7 | 0.021762 | -1.253 |
| w22 | 9 | 0.041739 | 6.857 |
| w23 | 3 | -0.081432 | -6.527 |
| w24 | 7 | 0.15737 | 18.492 |
| w25 | 7 | 0.052273 | 1.004 |
| w26 | 7 | 0.029592 | -1.055 |
| w27 | 7 | 0.286533 | 31.924 |
| w28 | 8 | -0.069117 | -4.286 |
| w29 | 7 | 0.212356 | 15.6 |
| w30 | 5 | 0.0259 | -0.598 |
| w31 | 6 | -0.008941 | -2.511 |
| w32 | 4 | -0.05931 | -6.243 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 6 | 0.079863 | 2.646 |
| w21 | 7 | 0.002585 | -1.582 |
| w22 | 10 | -0.034859 | -1.166 |
| w23 | 3 | -0.018784 | -2.249 |
| w24 | 10 | 0.136675 | 22.326 |
| w25 | 5 | -0.023942 | -2.542 |
| w26 | 7 | 0.094018 | 4.482 |
| w27 | 9 | -0.020078 | 0.854 |
| w28 | 8 | 0.073897 | 2.814 |
| w29 | 5 | 0.187532 | 13.868 |
| w30 | 6 | -0.001806 | -1.711 |
| w31 | 6 | -0.019166 | -3.902 |
| w32 | 5 | -0.0934 | -8.23 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 9 | 0.112303 | 11.595 |
| w23 | 5 | 0.038787 | 0.826 |
| w24 | 9 | 0.099159 | 11.101 |
| w25 | 7 | 0.018555 | 4.022 |
| w26 | 5 | 0.024945 | 0.132 |
| w27 | 8 | 0.109637 | 10.169 |
| w28 | 6 | -0.053589 | -5.474 |
| w29 | 5 | 0.220426 | 17.866 |
| w30 | 5 | 0.073867 | 3.677 |
| w31 | 9 | 0.071767 | 2.352 |
| w32 | 5 | 0.068414 | 6.425 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 8 | 0.033935 | 4.937 |
| w25 | 9 | -0.028622 | -1.907 |
| w26 | 7 | 0.095918 | 6.615 |
| w27 | 11 | 0.098182 | 12.755 |
| w28 | 7 | 0.010865 | -0.069 |
| w29 | 5 | 0.092649 | 5.775 |
| w30 | 5 | 0.046263 | 1.545 |
| w31 | 7 | -0.009947 | -3.653 |
| w32 | 3 | 0.014004 | 0.724 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 9 | -0.017503 | 1.709 |
| w6 | 8 | -0.092574 | -4.898 |
| w7 | 7 | 0.056599 | 1.37 |
| w8 | 5 | -0.022828 | -1.88 |
| w9 | 6 | 0.036208 | -0.899 |
| w10 | 6 | 0.035071 | 1.634 |
| w11 | 6 | -0.032031 | -5.022 |
| w12 | 8 | -0.039793 | -4.526 |
| w13 | 12 | -0.112038 | -9.456 |
| w14 | 12 | 0.169658 | 21.214 |
| w15 | 6 | -0.04454 | -3.834 |
| w16 | 12 | 0.22153 | 23.263 |
| w17 | 8 | -0.04516 | -2.745 |
| w18 | 8 | 0.050451 | 4.012 |
| w19 | 6 | 0.076102 | 6.27 |
| w20 | 5 | 0.023597 | 0.039 |
| w21 | 6 | -0.014024 | -1.858 |
| w22 | 8 | 0.005892 | 0.148 |
| w23 | 7 | 0.04217 | 1.428 |
| w24 | 10 | 0.037653 | 2.529 |
| w25 | 7 | 0.201965 | 12.33 |
| w26 | 8 | 0.061904 | 4.56 |
| w27 | 8 | -0.041848 | -3.195 |
| w28 | 7 | -0.066948 | -4.636 |
| w29 | 7 | 0.12554 | 10.159 |
| w30 | 10 | 0.138926 | 19.995 |
| w31 | 7 | 0.100192 | 5.896 |
| w32 | 8 | 0.04486 | 6.03 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 12 | 0.056494 | 12.994 |
| w6 | 10 | 0.08558 | 14.441 |
| w7 | 7 | 0.023147 | -0.14 |
| w8 | 6 | 0.038061 | 0.254 |
| w9 | 5 | 0.035363 | 0.387 |
| w10 | 11 | 0.020388 | 1.137 |
| w11 | 8 | 0.138165 | 11.598 |
| w12 | 7 | -0.032997 | -3.426 |
| w13 | 12 | -0.046389 | -6.072 |
| w14 | 10 | 0.163645 | 19.173 |
| w15 | 10 | 0.153628 | 10.595 |
| w16 | 11 | 0.096729 | 10.966 |
| w17 | 9 | -0.022259 | -0.675 |
| w18 | 7 | 0.049788 | 2.003 |
| w19 | 8 | 0.007278 | -1.066 |
| w20 | 8 | -0.044191 | -2.774 |
| w21 | 10 | -0.019326 | -3.364 |
| w22 | 6 | 0.049272 | 3.301 |
| w23 | 3 | 0.033017 | 0.347 |
| w24 | 11 | 0.039426 | 0.96 |
| w25 | 8 | 0.024207 | -0.211 |
| w26 | 10 | -0.082999 | -6.292 |
| w27 | 6 | -0.005351 | -1.677 |
| w28 | 11 | -0.135197 | -5.627 |
| w29 | 5 | 0.077811 | 5.318 |
| w30 | 8 | 0.104077 | 8.621 |
| w31 | 10 | 0.004095 | -0.055 |
| w32 | 10 | -0.067804 | -4.146 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 10 | -0.061524 | -6.762 |
| w18 | 9 | 0.096991 | 11.384 |
| w19 | 6 | 0.126196 | 5.219 |
| w20 | 8 | -0.025026 | -3.178 |
| w21 | 8 | 0.008939 | -3.111 |
| w22 | 9 | -0.028249 | -1.85 |
| w23 | 7 | -0.0487 | -5.852 |
| w24 | 9 | -0.040799 | -2.614 |
| w25 | 7 | 0.049657 | 1.722 |
| w26 | 8 | -0.07654 | -7.137 |
| w27 | 11 | 0.015387 | 6.629 |
| w28 | 7 | -0.022409 | -0.801 |
| w29 | 8 | -0.02022 | -2.699 |
| w30 | 5 | 0.039603 | 0.781 |
| w31 | 6 | -0.044552 | -5.047 |
| w32 | 6 | -0.032047 | -3.801 |

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
| w17 | 9 | -0.08465 | -7.937 |
| w18 | 8 | -0.006566 | -1.517 |
| w19 | 6 | -0.017678 | -2.136 |
| w20 | 7 | 0.071296 | 3.615 |
| w21 | 9 | 0.013246 | -0.578 |
| w22 | 11 | 0.004488 | 1.589 |
| w23 | 7 | -0.089099 | -7.083 |
| w24 | 11 | -0.066073 | -1.309 |
| w25 | 7 | 0.047408 | 3.2 |
| w26 | 7 | -0.007982 | -0.324 |
| w27 | 10 | 0.005534 | 3.926 |
| w28 | 8 | 0.002109 | -1.079 |
| w29 | 11 | 0.082616 | 9.136 |
| w30 | 6 | -0.030096 | -2.775 |
| w31 | 6 | -0.153138 | -11.607 |
| w32 | 6 | 0.045693 | 3.492 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 6 | -0.014861 | -1.823 |
| w20 | 7 | -0.019991 | -4.228 |
| w21 | 7 | -0.004271 | -0.954 |
| w22 | 10 | -0.019674 | 5.174 |
| w23 | 7 | 0.085214 | 3.75 |
| w24 | 11 | -0.026789 | 3.824 |
| w25 | 6 | -0.076127 | -6.329 |
| w26 | 9 | -0.018243 | -3.571 |
| w27 | 8 | 0.04066 | 3.051 |
| w28 | 7 | 0.041815 | 0.542 |
| w29 | 7 | 0.163614 | 12.081 |
| w30 | 4 | -0.045398 | -5.254 |
| w31 | 7 | 0.031216 | -0.81 |
| w32 | 8 | -0.028453 | -3.986 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 10 | -0.05127 | -3.092 |
| w23 | 7 | -0.062677 | -5.732 |
| w24 | 8 | -0.085972 | -3.387 |
| w25 | 6 | -0.17651 | -13.547 |
| w26 | 6 | 0.009636 | -0.997 |
| w27 | 10 | -0.007594 | -0.274 |
| w28 | 8 | -0.093489 | -9.076 |
| w29 | 7 | 0.250297 | 25.304 |
| w30 | 6 | -0.000178 | -0.99 |
| w31 | 7 | -0.089651 | -8.529 |
| w32 | 8 | -0.042341 | -5.142 |

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
| w27 | 10 | -0.042313 | -0.924 |
| w28 | 9 | -0.047652 | -4.928 |
| w29 | 5 | 0.148392 | 10.575 |
| w30 | 5 | -0.019938 | -2.808 |
| w31 | 6 | -0.029565 | -4.847 |
| w32 | 6 | -0.146888 | -15.945 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 4 | 0.059275 | 3.473 |
| w18 | 7 | 0.05105 | 3.389 |
| w19 | 5 | 0.021028 | -0.473 |
| w20 | 3 | 0.265118 | 12.181 |
| w21 | 7 | 0.043312 | 0.208 |
| w22 | 8 | 0.098063 | 14.41 |
| w23 | 7 | -0.055916 | -6.234 |
| w24 | 9 | 0.016016 | 3.641 |
| w25 | 6 | 0.029538 | 0.396 |
| w26 | 9 | 0.085997 | 3.347 |
| w27 | 8 | 0.123129 | 13.265 |
| w28 | 7 | -0.036536 | -2.688 |
| w29 | 6 | 0.125633 | 7.833 |
| w30 | 5 | -0.092661 | -6.346 |
| w31 | 8 | -0.038797 | -4.218 |
| w32 | 4 | -0.174643 | -14.041 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 6 | 0.003958 | -1.635 |
| w18 | 6 | -0.004215 | -1.222 |
| w19 | 4 | 0.083686 | 2.845 |
| w20 | 6 | 0.070467 | 2.63 |
| w21 | 9 | 0.104281 | 4.311 |
| w22 | 9 | -0.012979 | 3.532 |
| w23 | 5 | -0.052581 | -4.35 |
| w24 | 9 | -0.056046 | -0.896 |
| w25 | 6 | 0.20399 | 17.3 |
| w26 | 6 | 0.062322 | 2.25 |
| w27 | 9 | 0.035761 | 4.36 |
| w28 | 7 | 0.011688 | -1.422 |
| w29 | 6 | 0.199166 | 12.778 |
| w30 | 5 | -0.030645 | -3.49 |
| w31 | 6 | -0.107814 | -9.256 |
| w32 | 4 | -0.102013 | -10.283 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 10 | -0.0136 | -2.947 |
| w29 | 7 | 0.084709 | 4.143 |
| w30 | 4 | 0.038082 | 1.052 |
| w31 | 6 | 0.109738 | 7.59 |
| w32 | 4 | -0.025545 | -4.182 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 7 | 0.104018 | 4.591 |
| w15 | 6 | 0.117922 | 20.532 |
| w16 | 7 | 0.00917 | 37.821 |
| w17 | 5 | -0.04061 | -0.642 |
| w18 | 7 | 0.020907 | 0.216 |
| w19 | 5 | 0.067496 | 4.896 |
| w20 | 6 | 0.056512 | 1.101 |
| w21 | 6 | 0.37174 | 45.308 |
| w22 | 9 | 0.044944 | 2.717 |
| w23 | 7 | 0.041 | 0.856 |
| w24 | 10 | -0.08105 | -4.004 |
| w25 | 6 | -0.039015 | -2.988 |
| w26 | 5 | 0.137032 | 7.761 |
| w27 | 8 | 0.049446 | 14.157 |
| w28 | 8 | 0.005557 | -2.187 |
| w29 | 6 | 0.232821 | 22.97 |
| w30 | 4 | 0.067352 | 2.027 |
| w31 | 6 | -0.051152 | -6.232 |
| w32 | 6 | 0.005877 | -1.289 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 6 | -0.009303 | 2.329 |
| w26 | 8 | 0.021382 | 0.806 |
| w27 | 6 | -0.02383 | 1.196 |
| w28 | 9 | -0.031393 | -5.408 |
| w29 | 6 | 0.12268 | 7.929 |
| w30 | 4 | 0.026296 | -0.186 |
| w31 | 6 | -0.03174 | -4.558 |
| w32 | 4 | -0.056155 | -5.781 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

