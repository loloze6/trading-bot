# Backtest of 035-02_break-swings-above-continues_1d

- Plan: `../../../../../03_test_plan/night7_rangefail_run/plans/035-02_break-swings-above-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.051695 | 5.865 |
| w2 | 4 | 0.219367 | 57.879 |
| w3 | 22 | 0.036121 | 54.477 |
| w4 | 17 | 0.036044 | 1.864 |
| w5 | 13 | -0.032674 | 54.288 |
| w6 | 20 | 0.110758 | 49.015 |
| w7 | 1 | -0.131377 | -2.227 |
| w8 | 3 | 0.095957 | 6.62 |
| w9 | 2 | -0.085944 | -16.755 |
| w10 | 7 | 0.11244 | 16.698 |
| w11 | 10 | 0.091944 | 36.019 |
| w12 | 0 | None | 0.0 |
| w13 | 17 | -0.065797 | -1.165 |
| w14 | 8 | -0.082887 | 1.781 |
| w15 | 16 | 0.145109 | 114.344 |
| w16 | 10 | 0.014024 | 4.527 |
| w17 | 11 | 0.024557 | 8.944 |
| w18 | 11 | -0.112019 | -11.248 |
| w19 | 2 | 0.043596 | 5.559 |
| w20 | 0 | None | 0.0 |
| w21 | 8 | -0.173898 | -49.784 |
| w22 | 11 | 0.100355 | 72.445 |
| w23 | 2 | -0.012151 | 1.527 |
| w24 | 6 | 0.190005 | 18.149 |
| w25 | 10 | 0.033702 | 10.916 |
| w26 | 10 | -0.041894 | 0.984 |
| w27 | 16 | 0.125626 | 2.464 |
| w28 | 4 | 0.005663 | -1.335 |
| w29 | 13 | -0.070867 | 4.12 |
| w30 | 3 | 0.089142 | 7.374 |
| w31 | 12 | -0.066105 | -18.7 |
| w32 | 4 | 0.237023 | 25.308 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.248578 | 8.473 |
| w2 | 4 | -0.041124 | -8.918 |
| w3 | 6 | -0.07388 | -3.474 |
| w4 | 7 | -0.103316 | -13.87 |
| w5 | 9 | -0.019434 | 22.741 |
| w6 | 13 | 0.079166 | 114.32 |
| w7 | 2 | 0.070019 | 1.956 |
| w8 | 2 | 0.043742 | -5.356 |
| w9 | 0 | None | 0.0 |
| w10 | 11 | -0.057855 | -0.561 |
| w11 | 6 | -0.030978 | 8.434 |
| w12 | 2 | -0.090648 | -3.65 |
| w13 | 10 | -0.073106 | 23.327 |
| w14 | 10 | -0.213514 | 3.906 |
| w15 | 16 | -0.060681 | 13.764 |
| w16 | 9 | 0.030064 | 37.379 |
| w17 | 5 | -0.072584 | -1.992 |
| w18 | 6 | 0.008013 | -5.259 |
| w19 | 4 | -0.039951 | 1.35 |
| w20 | 1 | -0.069534 | -6.634 |
| w21 | 7 | 0.016615 | -32.955 |
| w22 | 9 | -0.072467 | -15.836 |
| w23 | 5 | -0.127913 | -21.14 |
| w24 | 2 | -0.119227 | -12.132 |
| w25 | 5 | -0.076288 | -18.81 |
| w26 | 2 | -0.009028 | -3.967 |
| w27 | 12 | -0.057642 | -13.231 |
| w28 | 2 | 0.024287 | -2.971 |
| w29 | 14 | -0.051594 | 18.767 |
| w30 | 3 | -0.440067 | -35.291 |
| w31 | 2 | 0.027792 | -3.115 |
| w32 | 5 | 0.16168 | 15.889 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 8 | 0.137078 | 58.032 |
| w7 | 3 | 0.047945 | 7.675 |
| w8 | 0 | None | 0.0 |
| w9 | 5 | 0.018545 | -12.293 |
| w10 | 0 | None | 0.0 |
| w11 | 3 | 0.025439 | -8.906 |
| w12 | 4 | -0.138095 | -21.139 |
| w13 | 8 | 0.043376 | -4.069 |
| w14 | 1 | 0.218497 | 62.135 |
| w15 | 2 | 0.184157 | 191.925 |
| w16 | 4 | -0.018954 | 25.301 |
| w17 | 2 | 0.061604 | 35.826 |
| w18 | 6 | -0.289185 | -30.135 |
| w19 | 2 | 0.075467 | -0.87 |
| w20 | 4 | -0.074633 | -8.332 |
| w21 | 4 | -0.106446 | -9.011 |
| w22 | 9 | -0.145882 | -8.925 |
| w23 | 4 | -0.063031 | 12.697 |
| w24 | 3 | 0.049657 | 7.75 |
| w25 | 4 | -0.132794 | -9.576 |
| w26 | 2 | -0.022597 | 4.203 |
| w27 | 8 | 0.225645 | 147.987 |
| w28 | 4 | -0.000239 | -4.64 |
| w29 | 6 | 0.220095 | 40.424 |
| w30 | 0 | None | 0.0 |
| w31 | 4 | -0.037408 | -14.662 |
| w32 | 3 | 0.26976 | 11.371 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 3 | 0.172262 | 25.113 |
| w8 | 2 | -0.004329 | -7.373 |
| w9 | 5 | -0.011962 | -21.076 |
| w10 | 7 | -0.025825 | 4.136 |
| w11 | 4 | -0.015013 | -4.868 |
| w12 | 2 | -0.028159 | 9.599 |
| w13 | 9 | -0.122555 | 13.416 |
| w14 | 2 | -0.01427 | 14.454 |
| w15 | 8 | -0.158581 | -21.638 |
| w16 | 9 | 0.079073 | 35.059 |
| w17 | 6 | -0.036023 | 1.541 |
| w18 | 2 | -0.168413 | -18.663 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | -0.159688 | 3.287 |
| w21 | 2 | -0.011937 | -32.159 |
| w22 | 7 | 0.176321 | 2.693 |
| w23 | 5 | 0.171795 | 26.359 |
| w24 | 9 | -0.194988 | -14.011 |
| w25 | 7 | -0.020008 | 13.484 |
| w26 | 3 | -0.033017 | -21.178 |
| w27 | 7 | -0.009724 | -9.594 |
| w28 | 5 | -0.048439 | -24.636 |
| w29 | 15 | -0.287893 | -26.924 |
| w30 | 3 | -0.14659 | -10.926 |
| w31 | 2 | -0.057365 | -3.696 |
| w32 | 3 | 0.31781 | 33.323 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.1477 | 161.59 |
| w2 | 6 | -0.029389 | -3.559 |
| w3 | 4 | 0.109327 | -0.836 |
| w4 | 11 | 0.214271 | 169.978 |
| w5 | 15 | -0.029333 | 74.504 |
| w6 | 8 | 0.141421 | 36.872 |
| w7 | 8 | 0.040808 | 34.608 |
| w8 | 2 | -0.00986 | -4.649 |
| w9 | 1 | -0.103313 | -2.605 |
| w10 | 7 | -0.149739 | -3.888 |
| w11 | 6 | 0.007735 | 36.122 |
| w12 | 2 | 0.004484 | -25.175 |
| w13 | 14 | -0.031875 | 29.299 |
| w14 | 8 | 0.04191 | 77.823 |
| w15 | 16 | 0.016337 | -10.67 |
| w16 | 18 | 0.15107 | 46.203 |
| w17 | 10 | 0.01645 | 39.239 |
| w18 | 7 | -0.066448 | -4.904 |
| w19 | 2 | 0.061216 | 4.663 |
| w20 | 5 | -0.006643 | -5.909 |
| w21 | 3 | 0.014187 | -16.569 |
| w22 | 12 | 0.079152 | 32.508 |
| w23 | 4 | -0.123161 | -9.811 |
| w24 | 5 | -0.013524 | 12.633 |
| w25 | 12 | 0.023597 | 4.058 |
| w26 | 2 | 0.041332 | 2.353 |
| w27 | 10 | 0.020539 | 1.822 |
| w28 | 0 | None | 0.0 |
| w29 | 10 | 0.092478 | 36.045 |
| w30 | 2 | -0.13343 | -21.706 |
| w31 | 7 | -0.082542 | -3.984 |
| w32 | 4 | -0.062771 | 13.513 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 10 | 0.031795 | 53.873 |
| w11 | 2 | 0.056597 | 1.459 |
| w12 | 0 | -0.081242 | 0.0 |
| w13 | 12 | 0.021806 | 28.192 |
| w14 | 11 | 0.011745 | 34.588 |
| w15 | 5 | 0.137165 | 26.527 |
| w16 | 13 | 0.153598 | 65.617 |
| w17 | 10 | 0.033512 | 82.232 |
| w18 | 0 | None | 0.0 |
| w19 | 3 | -0.154307 | -20.4 |
| w20 | 2 | -0.049875 | -21.366 |
| w21 | 1 | 0.001131 | -5.043 |
| w22 | 14 | 0.012709 | 11.112 |
| w23 | 3 | -0.16526 | -14.802 |
| w24 | 8 | 0.115485 | 157.003 |
| w25 | 7 | -0.009657 | 9.885 |
| w26 | 6 | -0.065721 | -22.544 |
| w27 | 9 | 0.18815 | 44.087 |
| w28 | 2 | 0.018254 | 0.346 |
| w29 | 7 | 0.162577 | 47.213 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 8 | -0.005813 | -21.887 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 8 | -0.071333 | -8.636 |
| w13 | 6 | -0.062312 | -19.033 |
| w14 | 10 | 0.061913 | 51.146 |
| w15 | 4 | -0.101372 | -13.093 |
| w16 | 10 | 0.037316 | 20.318 |
| w17 | 9 | -0.003257 | 6.229 |
| w18 | 4 | -0.187764 | 2.807 |
| w19 | 3 | -0.095146 | -10.947 |
| w20 | 5 | -0.10839 | -16.49 |
| w21 | 7 | 0.087038 | -19.88 |
| w22 | 12 | 0.068318 | -3.134 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | -0.016312 | 21.316 |
| w25 | 11 | -0.043792 | 20.969 |
| w26 | 2 | -0.028712 | -7.399 |
| w27 | 8 | 0.016481 | 3.814 |
| w28 | 0 | None | 0.0 |
| w29 | 5 | 0.055353 | -14.28 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | -0.005104 | -12.902 |
| w32 | 2 | -0.044428 | -8.79 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 2 | 0.024937 | -5.56 |
| w16 | 9 | 0.02887 | 42.706 |
| w17 | 2 | 0.090076 | -0.376 |
| w18 | 2 | 0.020973 | 48.917 |
| w19 | 1 | -0.121624 | -16.042 |
| w20 | 1 | -0.113243 | -7.432 |
| w21 | 8 | 0.056512 | -35.27 |
| w22 | 7 | 0.114583 | 6.221 |
| w23 | 0 | None | 0.0 |
| w24 | 12 | 0.06825 | 52.221 |
| w25 | 11 | 0.034319 | 27.242 |
| w26 | 4 | -0.009211 | -13.095 |
| w27 | 11 | 0.031581 | 24.768 |
| w28 | 4 | 0.10349 | 3.478 |
| w29 | 3 | -0.052809 | 22.185 |
| w30 | 0 | None | 0.0 |
| w31 | 4 | 0.076451 | 15.437 |
| w32 | 4 | -0.065824 | -13.803 |

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
| w15 | 4 | -0.058525 | -5.203 |
| w16 | 7 | -0.035146 | 2.914 |
| w17 | 4 | 0.047655 | 12.501 |
| w18 | 7 | -0.224908 | -34.966 |
| w19 | 6 | 0.021563 | 14.453 |
| w20 | 2 | -0.261614 | -14.743 |
| w21 | 0 | None | 0.0 |
| w22 | 6 | -0.074619 | -10.695 |
| w23 | 14 | 0.012808 | -11.29 |
| w24 | 12 | 0.013622 | 15.736 |
| w25 | 4 | 0.101569 | 16.169 |
| w26 | 6 | 0.145306 | 34.8 |
| w27 | 18 | -0.132078 | -11.353 |
| w28 | 2 | -0.032227 | -9.284 |
| w29 | 10 | -0.036962 | 3.87 |
| w30 | 0 | None | 0.0 |
| w31 | 19 | -0.202092 | 0.312 |
| w32 | 10 | 0.034871 | -3.797 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 10 | -0.029009 | 29.227 |
| w17 | 10 | -0.080989 | -16.058 |
| w18 | 11 | -0.071968 | 6.087 |
| w19 | 2 | -0.03735 | 4.478 |
| w20 | 3 | -0.048613 | -5.9 |
| w21 | 0 | None | 0.0 |
| w22 | 14 | -0.005905 | -3.42 |
| w23 | 0 | None | 0.0 |
| w24 | 10 | 0.027637 | 65.988 |
| w25 | 13 | -0.021732 | 10.41 |
| w26 | 2 | -0.046563 | -1.016 |
| w27 | 7 | 0.287528 | 3.568 |
| w28 | 0 | None | 0.0 |
| w29 | 3 | 0.163022 | 26.198 |
| w30 | 4 | -0.045374 | -5.165 |
| w31 | 5 | -0.076925 | -15.505 |
| w32 | 0 | None | 0.0 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 4 | 0.013429 | 1.674 |
| w21 | 2 | -0.061967 | 1.292 |
| w22 | 7 | -0.064259 | -11.608 |
| w23 | 0 | None | 0.0 |
| w24 | 14 | 0.093162 | 123.245 |
| w25 | 5 | 0.122804 | 11.478 |
| w26 | 3 | -0.008705 | -16.984 |
| w27 | 8 | 0.036973 | -2.812 |
| w28 | 2 | 0.023876 | -1.127 |
| w29 | 7 | 0.112922 | 21.381 |
| w30 | 4 | 0.075836 | 6.829 |
| w31 | 4 | 0.04178 | -5.054 |
| w32 | 4 | -0.072007 | -11.871 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 1 | -0.023543 | -6.036 |
| w23 | 0 | None | 0.0 |
| w24 | 7 | 0.208718 | 89.532 |
| w25 | 10 | -0.105832 | 40.827 |
| w26 | 4 | 0.000611 | -6.266 |
| w27 | 11 | -0.150475 | 14.125 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | 0.167008 | 23.106 |
| w30 | 2 | 0.113421 | -4.919 |
| w31 | 8 | -0.059739 | -7.08 |
| w32 | 4 | 0.063337 | 27.55 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 7 | -0.123932 | 4.213 |
| w25 | 10 | 0.010628 | 0.487 |
| w26 | 1 | -0.083025 | -10.079 |
| w27 | 19 | 0.083903 | 38.561 |
| w28 | 5 | 0.159114 | 5.726 |
| w29 | 4 | -0.025347 | -3.558 |
| w30 | 0 | None | 0.0 |
| w31 | 4 | 0.159607 | -0.56 |
| w32 | 3 | 0.238344 | 0.727 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 7 | 0.324065 | 45.949 |
| w6 | 13 | -0.034852 | 1.767 |
| w7 | 3 | -0.000305 | 8.139 |
| w8 | 2 | 0.060108 | -0.759 |
| w9 | 2 | -0.019877 | -8.646 |
| w10 | 3 | 0.082561 | 6.618 |
| w11 | 6 | 0.054684 | 10.142 |
| w12 | 2 | -0.057472 | -20.368 |
| w13 | 15 | -0.021364 | 43.591 |
| w14 | 6 | -0.124676 | 17.378 |
| w15 | 4 | -0.066757 | -0.516 |
| w16 | 10 | 0.087343 | 90.305 |
| w17 | 9 | -0.036426 | 6.348 |
| w18 | 9 | -0.043117 | -6.052 |
| w19 | 6 | 0.035453 | -2.699 |
| w20 | 2 | 0.120706 | 7.137 |
| w21 | 2 | -0.030691 | -4.628 |
| w22 | 10 | -0.044616 | -17.002 |
| w23 | 0 | None | 0.0 |
| w24 | 10 | -0.177959 | -26.703 |
| w25 | 1 | -0.088681 | 2.571 |
| w26 | 10 | 0.139563 | 49.986 |
| w27 | 10 | 0.003144 | 33.414 |
| w28 | 2 | -0.118393 | -7.675 |
| w29 | 9 | -0.021288 | -2.796 |
| w30 | 20 | 0.000356 | 140.009 |
| w31 | 2 | 0.032284 | 5.561 |
| w32 | 10 | 0.134278 | 63.551 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 8 | 0.007804 | 40.999 |
| w6 | 11 | -0.123887 | 6.5 |
| w7 | 3 | 0.001306 | 4.786 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | -0.125125 | -10.419 |
| w10 | 4 | -0.023179 | 9.184 |
| w11 | 9 | -0.031918 | 17.644 |
| w12 | 2 | -0.15505 | -16.255 |
| w13 | 10 | -0.125048 | -13.985 |
| w14 | 13 | -0.204624 | -2.67 |
| w15 | 9 | -0.023744 | 13.746 |
| w16 | 9 | -0.072057 | 10.731 |
| w17 | 7 | 0.032358 | -17.294 |
| w18 | 1 | -0.064011 | -3.1 |
| w19 | 6 | -0.112937 | -27.238 |
| w20 | 4 | 7.8e-05 | -2.655 |
| w21 | 6 | -0.247884 | -39.246 |
| w22 | 3 | 0.031991 | 9.734 |
| w23 | 1 | 0.080936 | 15.019 |
| w24 | 7 | -0.056466 | -3.197 |
| w25 | 6 | -0.032181 | -0.05 |
| w26 | 7 | 0.025755 | -1.733 |
| w27 | 5 | -0.157562 | 6.863 |
| w28 | 4 | 0.139836 | 29.228 |
| w29 | 5 | -0.052152 | -22.652 |
| w30 | 9 | -0.308975 | -27.659 |
| w31 | 4 | 0.140437 | 4.625 |
| w32 | 11 | 0.026684 | 20.743 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 3 | -0.059299 | -11.325 |
| w18 | 9 | 0.079242 | 21.755 |
| w19 | 4 | -0.055331 | -9.333 |
| w20 | 3 | -0.081864 | -8.359 |
| w21 | 0 | None | 0.0 |
| w22 | 10 | -0.039206 | 31.325 |
| w23 | 4 | -0.030006 | -8.639 |
| w24 | 9 | -0.006267 | 9.722 |
| w25 | 9 | -0.106159 | 11.426 |
| w26 | 2 | -0.053818 | -0.202 |
| w27 | 9 | -0.048705 | 125.394 |
| w28 | 3 | -0.175922 | -7.365 |
| w29 | 7 | 0.200792 | 41.36 |
| w30 | 0 | None | 0.0 |
| w31 | 2 | -0.091388 | -5.803 |
| w32 | 10 | -0.049599 | -12.872 |

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
| w17 | 2 | -0.149708 | -5.521 |
| w18 | 2 | -0.031182 | -8.921 |
| w19 | 5 | -0.051281 | 13.477 |
| w20 | 4 | -0.050801 | -6.232 |
| w21 | 4 | -0.028897 | -41.731 |
| w22 | 3 | 0.160709 | 36.096 |
| w23 | 2 | -0.069939 | -6.182 |
| w24 | 6 | -0.09374 | -13.955 |
| w25 | 10 | -0.071341 | 22.44 |
| w26 | 11 | 0.06671 | -21.555 |
| w27 | 12 | 0.04655 | 37.972 |
| w28 | 2 | -0.106141 | -11.601 |
| w29 | 16 | -0.013043 | -3.489 |
| w30 | 0 | None | 0.0 |
| w31 | 2 | 0.015934 | -5.031 |
| w32 | 5 | 0.175288 | 7.825 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.061424 | -2.992 |
| w21 | 1 | -0.051475 | -2.762 |
| w22 | 15 | -0.000959 | 67.894 |
| w23 | 5 | 0.105951 | -2.118 |
| w24 | 14 | 0.130872 | 302.791 |
| w25 | 3 | -0.130133 | -16.706 |
| w26 | 7 | 0.016979 | -35.298 |
| w27 | 11 | -0.008836 | 12.731 |
| w28 | 2 | 0.068881 | 2.96 |
| w29 | 9 | 0.106795 | 13.71 |
| w30 | 0 | None | 0.0 |
| w31 | 3 | -0.052786 | -11.049 |
| w32 | 4 | 0.044779 | 19.424 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 5 | -0.086346 | 23.09 |
| w23 | 4 | -0.011651 | -14.566 |
| w24 | 9 | -0.010704 | 2.405 |
| w25 | 6 | -0.134476 | -9.384 |
| w26 | 0 | None | 0.0 |
| w27 | 8 | -0.082139 | -3.184 |
| w28 | 1 | -0.157763 | -14.607 |
| w29 | 10 | 0.206464 | 41.077 |
| w30 | 1 | -0.098934 | -11.971 |
| w31 | 2 | 0.064634 | 0.498 |
| w32 | 7 | -0.104074 | -0.207 |

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
| w27 | 9 | 0.070724 | 23.317 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | -0.056567 | 15.532 |
| w30 | 2 | 0.036534 | -5.364 |
| w31 | 0 | None | 0.0 |
| w32 | 4 | 0.101141 | 24.511 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 4 | -0.107627 | -1.31 |
| w18 | 2 | 0.150205 | -4.954 |
| w19 | 2 | 0.087048 | -4.18 |
| w20 | 1 | -0.135553 | -9.012 |
| w21 | 2 | -0.09446 | -6.367 |
| w22 | 9 | 0.053075 | 6.274 |
| w23 | 4 | -0.124322 | -27.169 |
| w24 | 9 | -0.052355 | -2.539 |
| w25 | 6 | 0.05458 | 12.559 |
| w26 | 0 | None | 0.0 |
| w27 | 12 | 0.003282 | -6.969 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | 0.108582 | 3.965 |
| w30 | 4 | 0.358391 | 10.621 |
| w31 | 4 | -0.033517 | -9.728 |
| w32 | 2 | -0.127122 | -6.15 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 4 | 0.028468 | -1.339 |
| w18 | 1 | -0.005641 | 4.982 |
| w19 | 3 | -0.128852 | -2.62 |
| w20 | 3 | 0.002578 | -7.423 |
| w21 | 2 | -0.310606 | -26.594 |
| w22 | 10 | -0.018349 | 23.246 |
| w23 | 4 | 0.089706 | -7.958 |
| w24 | 12 | -0.042542 | 40.993 |
| w25 | 9 | 0.051869 | 45.148 |
| w26 | 3 | 0.00642 | -17.82 |
| w27 | 10 | -0.003624 | 38.462 |
| w28 | 2 | 0.129915 | 1.417 |
| w29 | 6 | 0.051545 | -0.316 |
| w30 | 3 | -0.065031 | -10.623 |
| w31 | 5 | -0.086015 | -8.783 |
| w32 | 4 | -0.039859 | -3.949 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 5 | 0.031587 | 12.396 |
| w29 | 5 | 0.039852 | 4.987 |
| w30 | 4 | -0.123538 | -13.492 |
| w31 | 4 | 0.101029 | 13.298 |
| w32 | 5 | -0.038774 | 5.305 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 3 | 0.331883 | 56.357 |
| w15 | 4 | -0.070277 | -5.78 |
| w16 | 6 | 0.1433 | 225.542 |
| w17 | 3 | 0.024107 | -0.612 |
| w18 | 1 | -0.063933 | -5.914 |
| w19 | 3 | -0.25628 | -16.37 |
| w20 | 1 | -0.125027 | -17.357 |
| w21 | 2 | 0.047606 | 77.482 |
| w22 | 7 | -0.057161 | -9.928 |
| w23 | 0 | None | 0.0 |
| w24 | 9 | -0.216388 | -15.279 |
| w25 | 6 | 0.084106 | 54.738 |
| w26 | 4 | 0.021333 | -8.034 |
| w27 | 9 | 0.22924 | 63.502 |
| w28 | 0 | None | 0.0 |
| w29 | 6 | 0.164908 | 21.679 |
| w30 | 2 | 0.029232 | 1.995 |
| w31 | 3 | 0.065846 | -3.0 |
| w32 | 3 | 0.242284 | 6.402 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 6 | 0.246237 | 139.31 |
| w26 | 5 | -0.032659 | 4.749 |
| w27 | 8 | 0.289098 | 73.251 |
| w28 | 3 | 0.001995 | -9.654 |
| w29 | 8 | 0.166437 | 24.099 |
| w30 | 1 | -0.043335 | -3.751 |
| w31 | 2 | -0.007187 | 0.946 |
| w32 | 3 | -0.053071 | -14.603 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

