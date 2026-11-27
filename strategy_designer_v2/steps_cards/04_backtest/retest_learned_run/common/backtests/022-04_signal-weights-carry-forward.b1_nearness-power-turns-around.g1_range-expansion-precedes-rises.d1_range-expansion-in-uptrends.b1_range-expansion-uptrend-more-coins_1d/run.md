# Backtest of 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends.b1_range-expansion-uptrend-more-coins_1d

- Plan: `../../../../../03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends.b1_range-expansion-uptrend-more-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 45 | -0.02277 | 4.228 |
| w2 | 37 | 0.101536 | 49.047 |
| w3 | 68 | 0.032092 | 86.073 |
| w4 | 51 | -0.089982 | -15.445 |
| w5 | 53 | 0.029239 | 87.49 |
| w6 | 59 | 0.022959 | 94.389 |
| w7 | 19 | -0.047139 | -11.57 |
| w8 | 29 | 0.079301 | 0.666 |
| w9 | 28 | -0.077935 | -20.867 |
| w10 | 47 | 0.08577 | 42.284 |
| w11 | 55 | 0.036416 | 48.893 |
| w12 | 26 | 0.062564 | -18.514 |
| w13 | 48 | -0.007532 | 17.584 |
| w14 | 54 | 0.034646 | 18.712 |
| w15 | 63 | 0.081101 | 99.319 |
| w16 | 51 | -0.09159 | 16.865 |
| w17 | 32 | 0.123138 | 7.214 |
| w18 | 40 | -0.029723 | -1.224 |
| w19 | 33 | -0.160219 | -25.51 |
| w20 | 28 | 0.086101 | -20.161 |
| w21 | 37 | -0.096582 | -38.215 |
| w22 | 59 | 0.011058 | 74.171 |
| w23 | 23 | 0.062223 | -18.036 |
| w24 | 67 | 0.075276 | 77.401 |
| w25 | 47 | -0.052128 | 18.65 |
| w26 | 39 | -0.045909 | -13.989 |
| w27 | 64 | 0.07621 | 73.909 |
| w28 | 31 | -0.003706 | -6.852 |
| w29 | 63 | -0.022202 | -4.528 |
| w30 | 22 | -0.031634 | -13.059 |
| w31 | 46 | -0.030961 | -8.144 |
| w32 | 38 | 0.181665 | 30.881 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | 0.035861 | 22.135 |
| w2 | 34 | -0.085593 | -14.828 |
| w3 | 48 | -0.111264 | -10.577 |
| w4 | 46 | -0.036863 | 40.547 |
| w5 | 66 | 0.031186 | 52.466 |
| w6 | 54 | 0.144711 | 92.406 |
| w7 | 19 | 0.044537 | 2.651 |
| w8 | 18 | -0.023985 | -21.602 |
| w9 | 14 | -0.128024 | -26.397 |
| w10 | 61 | -0.016293 | 38.912 |
| w11 | 35 | -0.017956 | 0.843 |
| w12 | 19 | 0.022703 | -13.235 |
| w13 | 53 | 0.012649 | 25.982 |
| w14 | 46 | -0.009971 | 27.608 |
| w15 | 51 | 0.052913 | 41.814 |
| w16 | 54 | -0.154387 | 11.543 |
| w17 | 36 | 0.074493 | 4.934 |
| w18 | 47 | 0.045892 | 6.352 |
| w19 | 30 | -0.122894 | -35.537 |
| w20 | 24 | 0.057718 | -6.3 |
| w21 | 37 | -0.040558 | -10.916 |
| w22 | 51 | -0.12168 | -7.528 |
| w23 | 24 | -0.050699 | -2.789 |
| w24 | 51 | -0.176758 | -18.028 |
| w25 | 46 | -0.020266 | 13.566 |
| w26 | 33 | -0.094152 | -19.692 |
| w27 | 62 | -0.035519 | 40.296 |
| w28 | 34 | -0.071139 | -13.509 |
| w29 | 44 | 0.221391 | 48.199 |
| w30 | 23 | -0.211228 | -38.186 |
| w31 | 35 | -0.128346 | -23.085 |
| w32 | 38 | 0.113646 | 15.754 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 52 | 0.079224 | 162.737 |
| w7 | 24 | 0.05615 | 7.425 |
| w8 | 11 | -0.069492 | -27.272 |
| w9 | 28 | 0.004086 | -7.571 |
| w10 | 32 | 0.036344 | -2.202 |
| w11 | 31 | -0.022101 | 7.55 |
| w12 | 19 | -0.137465 | -22.684 |
| w13 | 48 | -0.04113 | 6.293 |
| w14 | 40 | 0.11777 | 46.081 |
| w15 | 42 | 0.240485 | 136.014 |
| w16 | 48 | -0.045288 | 58.537 |
| w17 | 30 | 0.119742 | 28.193 |
| w18 | 31 | -0.128339 | -17.315 |
| w19 | 34 | 0.005691 | -9.229 |
| w20 | 19 | 0.013471 | -6.1 |
| w21 | 27 | 0.096994 | 0.041 |
| w22 | 45 | -0.030658 | 35.312 |
| w23 | 28 | -0.081905 | -8.685 |
| w24 | 42 | -0.044408 | 4.87 |
| w25 | 29 | 0.024956 | -9.491 |
| w26 | 26 | -0.103045 | -7.256 |
| w27 | 37 | 0.251419 | 180.878 |
| w28 | 30 | -0.093398 | -16.509 |
| w29 | 44 | 0.097367 | 39.739 |
| w30 | 18 | -0.15531 | -17.955 |
| w31 | 34 | -0.055977 | -20.813 |
| w32 | 23 | 0.19727 | 22.305 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 16 | 0.142146 | 22.414 |
| w8 | 24 | 0.025241 | -6.68 |
| w9 | 18 | 0.016661 | -24.132 |
| w10 | 43 | 0.069055 | 23.179 |
| w11 | 39 | -0.080854 | -12.59 |
| w12 | 26 | -0.041122 | -11.967 |
| w13 | 44 | -0.037157 | 20.275 |
| w14 | 49 | 0.013117 | 10.512 |
| w15 | 47 | -0.092147 | -22.704 |
| w16 | 51 | 0.009195 | 55.1 |
| w17 | 39 | 0.083717 | 17.552 |
| w18 | 29 | -0.064618 | -20.665 |
| w19 | 21 | -0.047207 | -23.434 |
| w20 | 21 | 0.085302 | -0.416 |
| w21 | 27 | 0.014603 | -24.667 |
| w22 | 45 | -0.072888 | 3.196 |
| w23 | 16 | 0.311621 | 69.508 |
| w24 | 48 | -0.171132 | 11.36 |
| w25 | 47 | 0.029827 | 63.35 |
| w26 | 26 | -0.060143 | -19.573 |
| w27 | 52 | -0.032944 | 12.091 |
| w28 | 27 | -0.132687 | -10.747 |
| w29 | 64 | -0.139855 | 2.762 |
| w30 | 36 | -0.098443 | -26.778 |
| w31 | 29 | -0.056055 | -18.712 |
| w32 | 29 | 0.186324 | 20.328 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 46 | 0.188462 | 146.176 |
| w2 | 37 | -0.140202 | -3.307 |
| w3 | 22 | 0.087239 | -2.386 |
| w4 | 58 | 0.202853 | 279.162 |
| w5 | 50 | 0.067072 | 88.592 |
| w6 | 49 | 0.114799 | 91.474 |
| w7 | 32 | 0.086716 | 25.512 |
| w8 | 17 | -0.00643 | -5.76 |
| w9 | 21 | -0.082081 | -31.389 |
| w10 | 46 | -0.037047 | 1.723 |
| w11 | 37 | 0.06478 | 22.664 |
| w12 | 25 | -0.114714 | -26.422 |
| w13 | 52 | 0.0043 | 51.44 |
| w14 | 60 | 0.160033 | 93.791 |
| w15 | 56 | 0.046901 | 20.756 |
| w16 | 63 | -0.014624 | 85.393 |
| w17 | 38 | 0.032521 | 19.967 |
| w18 | 43 | -0.069298 | 4.435 |
| w19 | 28 | -0.017958 | -9.802 |
| w20 | 25 | 0.091453 | 5.925 |
| w21 | 33 | -0.144975 | -14.062 |
| w22 | 51 | -0.024925 | 31.985 |
| w23 | 23 | -0.189058 | -21.119 |
| w24 | 48 | -0.078217 | 13.788 |
| w25 | 45 | 0.016317 | 17.867 |
| w26 | 25 | -0.068232 | -16.278 |
| w27 | 50 | -0.072259 | 21.736 |
| w28 | 8 | -0.136524 | -14.558 |
| w29 | 65 | 0.056183 | 68.881 |
| w30 | 20 | -0.101742 | -28.864 |
| w31 | 48 | -0.052668 | -15.581 |
| w32 | 40 | 0.168722 | 42.365 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 50 | 0.104083 | 42.3 |
| w11 | 26 | -0.110673 | 2.166 |
| w12 | 24 | -0.009429 | -27.745 |
| w13 | 56 | 0.107137 | 56.56 |
| w14 | 60 | 0.158093 | 67.048 |
| w15 | 39 | 0.068602 | 34.992 |
| w16 | 54 | 0.060298 | 102.906 |
| w17 | 44 | 0.150353 | 97.956 |
| w18 | 18 | -0.102025 | -14.787 |
| w19 | 22 | -0.072834 | -26.427 |
| w20 | 28 | -0.065491 | -20.66 |
| w21 | 19 | -0.184328 | -27.941 |
| w22 | 53 | 0.089634 | 47.298 |
| w23 | 18 | -0.134162 | -30.011 |
| w24 | 59 | 0.136071 | 156.457 |
| w25 | 30 | 0.108371 | -4.019 |
| w26 | 35 | -0.01905 | -12.022 |
| w27 | 47 | 0.217024 | 124.627 |
| w28 | 22 | -0.104713 | -16.352 |
| w29 | 42 | 0.090754 | 29.015 |
| w30 | 8 | -0.137861 | -19.677 |
| w31 | 25 | -0.103568 | -27.034 |
| w32 | 45 | 0.159876 | 7.309 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 48 | -0.162133 | -9.276 |
| w13 | 49 | -0.045176 | -17.147 |
| w14 | 56 | 0.109672 | 107.078 |
| w15 | 33 | -0.040526 | -2.674 |
| w16 | 59 | -0.109862 | 39.626 |
| w17 | 43 | 0.057234 | 13.352 |
| w18 | 35 | -0.035891 | -0.746 |
| w19 | 31 | -0.063752 | -12.055 |
| w20 | 36 | 0.123692 | 18.084 |
| w21 | 33 | -0.066877 | -21.697 |
| w22 | 45 | 0.034981 | 8.289 |
| w23 | 17 | 0.014099 | -10.83 |
| w24 | 49 | -0.011407 | 15.5 |
| w25 | 29 | 0.084074 | 7.562 |
| w26 | 16 | 0.031579 | -20.59 |
| w27 | 41 | 0.051097 | 22.13 |
| w28 | 19 | -0.107565 | -9.823 |
| w29 | 39 | 0.036798 | -2.724 |
| w30 | 7 | -0.05349 | -6.554 |
| w31 | 40 | -0.080127 | -15.444 |
| w32 | 27 | 0.055946 | -5.282 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 23 | 0.04924 | -6.295 |
| w16 | 59 | -0.007035 | 42.366 |
| w17 | 31 | 0.042219 | 1.144 |
| w18 | 36 | 0.090785 | 24.423 |
| w19 | 23 | -0.030941 | -19.338 |
| w20 | 27 | 0.025031 | -35.255 |
| w21 | 21 | -0.069314 | -23.803 |
| w22 | 41 | 0.132351 | 13.664 |
| w23 | 10 | -0.126933 | -19.098 |
| w24 | 56 | 0.024666 | 68.359 |
| w25 | 33 | 0.152227 | 20.37 |
| w26 | 27 | -0.078787 | -13.542 |
| w27 | 41 | 0.150471 | 85.334 |
| w28 | 21 | -0.10234 | -12.435 |
| w29 | 35 | 0.058338 | 16.61 |
| w30 | 6 | -0.156387 | -21.62 |
| w31 | 33 | 0.027407 | -6.102 |
| w32 | 28 | 0.086734 | -0.866 |

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
| w15 | 33 | -0.048453 | -3.673 |
| w16 | 59 | -0.100098 | 71.266 |
| w17 | 37 | 0.074079 | 11.474 |
| w18 | 42 | 0.023616 | 14.334 |
| w19 | 22 | -0.022773 | -11.286 |
| w20 | 44 | -0.009156 | -4.458 |
| w21 | 36 | 0.008955 | -26.824 |
| w22 | 49 | -0.029167 | 34.974 |
| w23 | 54 | -0.082709 | -7.84 |
| w24 | 77 | -0.010469 | 55.812 |
| w25 | 52 | 0.001548 | 2.499 |
| w26 | 54 | 0.123497 | 21.348 |
| w27 | 57 | 0.056622 | 128.782 |
| w28 | 36 | -0.09844 | -5.435 |
| w29 | 73 | -0.110548 | 24.372 |
| w30 | 19 | -0.088101 | -18.557 |
| w31 | 60 | -0.107376 | 7.299 |
| w32 | 56 | 0.084264 | 1.326 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 55 | 0.054832 | 36.146 |
| w17 | 35 | 0.131368 | 26.111 |
| w18 | 35 | 0.036991 | 11.234 |
| w19 | 30 | -0.055025 | -11.444 |
| w20 | 25 | 0.02644 | -11.944 |
| w21 | 18 | -0.205696 | -28.048 |
| w22 | 47 | -0.062052 | 9.117 |
| w23 | 27 | -0.020369 | -16.26 |
| w24 | 41 | 0.035636 | 36.231 |
| w25 | 43 | 0.122827 | 2.559 |
| w26 | 23 | 0.005129 | -13.621 |
| w27 | 34 | 0.115962 | 22.995 |
| w28 | 16 | -0.189448 | -18.743 |
| w29 | 29 | 0.067253 | -2.282 |
| w30 | 20 | -0.049588 | -31.115 |
| w31 | 30 | -0.073745 | -19.786 |
| w32 | 27 | 0.114183 | -0.807 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 31 | 0.114981 | 4.153 |
| w21 | 20 | -0.192935 | -34.598 |
| w22 | 41 | 0.075397 | 33.829 |
| w23 | 21 | 0.118242 | 2.145 |
| w24 | 47 | 0.13384 | 148.358 |
| w25 | 30 | 0.105769 | 25.778 |
| w26 | 33 | -0.047045 | -16.859 |
| w27 | 57 | 0.035054 | 30.194 |
| w28 | 16 | -0.012172 | -10.59 |
| w29 | 47 | 0.02697 | 17.554 |
| w30 | 20 | -0.002245 | -11.626 |
| w31 | 35 | -0.087772 | -16.792 |
| w32 | 33 | 0.056186 | -4.0 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 42 | 0.010555 | 23.252 |
| w23 | 18 | 0.066806 | -9.496 |
| w24 | 50 | 0.184412 | 132.483 |
| w25 | 41 | 0.084172 | 43.285 |
| w26 | 39 | -0.029509 | -10.799 |
| w27 | 43 | 0.019782 | 15.762 |
| w28 | 15 | -0.084974 | -17.589 |
| w29 | 34 | 0.043146 | -2.75 |
| w30 | 31 | 0.006678 | -9.98 |
| w31 | 33 | -0.041712 | -7.354 |
| w32 | 34 | 0.016663 | 42.819 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 42 | -0.002459 | 18.522 |
| w25 | 55 | 0.090626 | 10.028 |
| w26 | 24 | -0.080941 | -27.193 |
| w27 | 64 | 0.055777 | 86.508 |
| w28 | 22 | 0.018883 | -7.554 |
| w29 | 41 | 0.012516 | 3.505 |
| w30 | 13 | -0.0665 | -21.517 |
| w31 | 34 | -0.081335 | -13.637 |
| w32 | 33 | 0.163662 | 26.273 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 49 | 0.159413 | 122.301 |
| w6 | 45 | 0.002084 | 20.943 |
| w7 | 26 | 0.015988 | -0.214 |
| w8 | 28 | -0.02163 | -9.653 |
| w9 | 29 | -0.08224 | -26.814 |
| w10 | 44 | 0.075423 | 5.094 |
| w11 | 23 | 0.124936 | 31.156 |
| w12 | 27 | -0.073986 | -23.056 |
| w13 | 46 | 0.123093 | 82.824 |
| w14 | 56 | -0.049157 | 18.676 |
| w15 | 33 | 0.00829 | 9.429 |
| w16 | 52 | -0.00205 | 55.361 |
| w17 | 34 | 0.082095 | 7.09 |
| w18 | 32 | 0.08154 | 29.966 |
| w19 | 35 | -0.013144 | -13.473 |
| w20 | 24 | 0.023285 | -11.584 |
| w21 | 22 | 0.00972 | -37.463 |
| w22 | 35 | -0.076896 | -11.693 |
| w23 | 24 | -0.043702 | -27.817 |
| w24 | 52 | -0.073514 | -7.132 |
| w25 | 29 | 0.077502 | 8.925 |
| w26 | 52 | 0.014347 | 31.562 |
| w27 | 50 | -0.091321 | 7.622 |
| w28 | 28 | -0.086875 | -20.583 |
| w29 | 41 | 0.065785 | 8.898 |
| w30 | 46 | 0.233949 | 233.797 |
| w31 | 30 | -0.08775 | -13.575 |
| w32 | 41 | 0.145383 | 90.677 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 55 | 0.1235 | 128.521 |
| w6 | 41 | 0.069392 | 63.161 |
| w7 | 28 | -0.043553 | -6.63 |
| w8 | 21 | -0.069333 | -11.966 |
| w9 | 29 | 0.03417 | -20.243 |
| w10 | 45 | -0.026141 | 15.952 |
| w11 | 47 | -0.161273 | -1.916 |
| w12 | 21 | -0.043678 | -18.245 |
| w13 | 50 | 0.012394 | 18.855 |
| w14 | 62 | 0.014479 | 27.028 |
| w15 | 59 | -0.048996 | 13.064 |
| w16 | 46 | 0.011005 | 45.101 |
| w17 | 36 | 0.094386 | -4.019 |
| w18 | 28 | -0.077182 | -12.046 |
| w19 | 50 | -0.207218 | -22.397 |
| w20 | 38 | 0.095742 | 6.717 |
| w21 | 41 | -0.121065 | -20.079 |
| w22 | 44 | 0.065005 | 20.79 |
| w23 | 19 | 0.146209 | 3.901 |
| w24 | 64 | -0.06976 | 4.162 |
| w25 | 27 | -0.08455 | -15.583 |
| w26 | 49 | 0.136965 | 34.82 |
| w27 | 46 | -0.034175 | 3.248 |
| w28 | 42 | 0.010262 | 8.518 |
| w29 | 36 | -0.020415 | 7.408 |
| w30 | 65 | -0.135449 | 22.821 |
| w31 | 44 | 6e-05 | -2.084 |
| w32 | 49 | 0.038066 | 40.96 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 34 | -0.006845 | -8.593 |
| w18 | 48 | -0.163797 | 14.613 |
| w19 | 27 | -0.0488 | -21.554 |
| w20 | 30 | 0.047599 | -14.389 |
| w21 | 19 | -0.072916 | -28.491 |
| w22 | 51 | 0.034393 | 37.266 |
| w23 | 18 | 0.046721 | -17.714 |
| w24 | 48 | -0.003093 | 19.528 |
| w25 | 31 | 0.168512 | 21.816 |
| w26 | 26 | -0.073063 | -22.517 |
| w27 | 40 | 0.216754 | 85.942 |
| w28 | 25 | -0.005592 | 14.404 |
| w29 | 34 | 0.136302 | 30.521 |
| w30 | 8 | -0.105603 | -31.881 |
| w31 | 34 | 0.014039 | -14.563 |
| w32 | 50 | 0.023589 | 13.679 |

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
| w17 | 37 | -0.030409 | 2.375 |
| w18 | 25 | -0.054845 | -18.571 |
| w19 | 31 | 0.075032 | 6.422 |
| w20 | 33 | 0.063927 | 3.814 |
| w21 | 32 | -0.022422 | -20.641 |
| w22 | 39 | 0.062501 | 31.676 |
| w23 | 24 | -0.086088 | -20.907 |
| w24 | 57 | -0.100951 | 23.945 |
| w25 | 33 | 0.14886 | 16.787 |
| w26 | 49 | -0.091119 | 3.848 |
| w27 | 64 | -0.030957 | 27.556 |
| w28 | 13 | 0.038773 | -2.498 |
| w29 | 58 | -0.032647 | 10.989 |
| w30 | 14 | -0.087158 | -16.874 |
| w31 | 22 | -0.078312 | -24.501 |
| w32 | 34 | 0.092207 | 23.946 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 23 | -0.10316 | -17.587 |
| w20 | 29 | 0.044726 | 2.202 |
| w21 | 30 | 0.031583 | 3.958 |
| w22 | 62 | -0.007303 | 129.813 |
| w23 | 32 | 0.079 | -5.038 |
| w24 | 62 | 0.170625 | 216.557 |
| w25 | 30 | 0.019073 | -1.536 |
| w26 | 27 | -0.178556 | -32.663 |
| w27 | 43 | 0.032136 | -4.738 |
| w28 | 9 | -0.028327 | -13.27 |
| w29 | 50 | -0.055974 | 6.174 |
| w30 | 12 | -0.012741 | -9.594 |
| w31 | 34 | -0.095676 | -24.334 |
| w32 | 43 | -0.032098 | 15.872 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 43 | 0.099813 | 40.062 |
| w23 | 30 | -0.113068 | -23.957 |
| w24 | 43 | -0.036434 | 14.687 |
| w25 | 38 | -0.041008 | -28.879 |
| w26 | 23 | -0.109644 | -33.907 |
| w27 | 44 | -0.111484 | -3.326 |
| w28 | 16 | -0.109086 | -14.245 |
| w29 | 48 | 0.075993 | 17.675 |
| w30 | 8 | -0.048679 | -28.149 |
| w31 | 35 | 0.056751 | -3.885 |
| w32 | 30 | 0.0519 | 10.92 |

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
| w27 | 45 | 0.052442 | 41.166 |
| w28 | 25 | -0.013512 | -1.927 |
| w29 | 43 | 0.002459 | 0.563 |
| w30 | 13 | 0.043374 | -7.35 |
| w31 | 39 | -0.200822 | -31.146 |
| w32 | 39 | 0.062712 | 39.518 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 24 | 0.103075 | 4.63 |
| w18 | 20 | -0.018371 | -17.621 |
| w19 | 16 | 0.079903 | 5.375 |
| w20 | 19 | 0.049972 | 6.862 |
| w21 | 17 | -0.039114 | -21.5 |
| w22 | 41 | 0.048737 | 35.331 |
| w23 | 26 | -0.04401 | -12.959 |
| w24 | 58 | -0.039586 | 51.256 |
| w25 | 33 | 0.159032 | 5.594 |
| w26 | 23 | -0.099911 | -26.227 |
| w27 | 45 | 0.049642 | 14.499 |
| w28 | 21 | -0.07985 | -13.791 |
| w29 | 39 | -0.013854 | -18.726 |
| w30 | 19 | 0.133383 | 6.82 |
| w31 | 35 | -0.037005 | -24.494 |
| w32 | 27 | 0.091857 | -4.028 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 31 | 0.053285 | -5.374 |
| w18 | 27 | -0.043926 | -8.717 |
| w19 | 29 | -0.018027 | -18.095 |
| w20 | 24 | 0.032381 | -2.884 |
| w21 | 19 | -0.085722 | -25.026 |
| w22 | 40 | 0.042439 | 72.248 |
| w23 | 22 | 0.116134 | 4.096 |
| w24 | 43 | 0.05353 | 60.326 |
| w25 | 31 | 0.182945 | 45.367 |
| w26 | 26 | -0.062748 | -19.786 |
| w27 | 47 | 0.017204 | 9.659 |
| w28 | 10 | -0.022759 | -10.781 |
| w29 | 32 | 0.034709 | -3.247 |
| w30 | 13 | -0.025576 | -16.719 |
| w31 | 36 | -0.100974 | -23.541 |
| w32 | 20 | 0.115452 | 22.328 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 24 | -0.039309 | -31.641 |
| w29 | 39 | 0.024268 | -11.201 |
| w30 | 27 | -0.056302 | 0.186 |
| w31 | 42 | 0.002234 | 4.884 |
| w32 | 32 | 0.030611 | 15.39 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 39 | 0.08488 | 47.947 |
| w15 | 36 | 0.156949 | 89.404 |
| w16 | 41 | 0.004858 | 236.768 |
| w17 | 31 | 0.104604 | 12.851 |
| w18 | 30 | -0.065054 | -6.209 |
| w19 | 27 | -0.008497 | -2.73 |
| w20 | 23 | -0.001031 | -13.693 |
| w21 | 30 | 0.112977 | 60.645 |
| w22 | 49 | 0.026193 | 13.89 |
| w23 | 30 | 0.014129 | -5.814 |
| w24 | 45 | 0.023554 | 17.651 |
| w25 | 35 | 0.165279 | 83.171 |
| w26 | 27 | -0.051221 | -20.396 |
| w27 | 54 | 0.19084 | 140.478 |
| w28 | 19 | -0.026347 | -9.054 |
| w29 | 41 | 0.034913 | 25.284 |
| w30 | 14 | 0.020865 | -7.136 |
| w31 | 41 | -0.090542 | -17.694 |
| w32 | 25 | 0.174041 | 21.048 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 30 | 0.307851 | 162.192 |
| w26 | 40 | 0.009822 | -0.173 |
| w27 | 35 | 0.098877 | 56.218 |
| w28 | 23 | -0.108284 | -15.473 |
| w29 | 39 | 0.05951 | 8.07 |
| w30 | 10 | -0.079237 | -15.03 |
| w31 | 36 | -0.066427 | -18.081 |
| w32 | 33 | 0.156294 | 16.594 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

