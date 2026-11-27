# Backtest of 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound_1d

- Plan: `../../../../../03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | 0.003827 | 1.963 |
| w2 | 18 | -0.152865 | -15.086 |
| w3 | 15 | -0.026081 | 4.923 |
| w4 | 13 | -0.105683 | -19.905 |
| w5 | 23 | 0.152815 | 36.0 |
| w6 | 24 | -0.105725 | -5.735 |
| w7 | 26 | -0.055779 | -8.004 |
| w8 | 27 | 0.01044 | -3.041 |
| w9 | 23 | 0.047894 | -17.357 |
| w10 | 14 | 0.005979 | 2.728 |
| w11 | 19 | 0.073036 | 15.777 |
| w12 | 24 | -0.043878 | -14.088 |
| w13 | 17 | 0.148512 | 18.449 |
| w14 | 22 | 0.063956 | 12.329 |
| w15 | 24 | 0.004304 | 11.191 |
| w16 | 22 | -0.078204 | -3.245 |
| w17 | 17 | 0.192554 | 20.941 |
| w18 | 24 | 0.018141 | -0.365 |
| w19 | 26 | -0.005961 | -6.135 |
| w20 | 28 | -0.000324 | -15.512 |
| w21 | 20 | 0.030662 | -7.399 |
| w22 | 23 | 0.044962 | 14.455 |
| w23 | 22 | 0.010109 | -8.898 |
| w24 | 21 | 0.100122 | 20.933 |
| w25 | 18 | 0.0926 | 13.645 |
| w26 | 25 | 0.074249 | 6.506 |
| w27 | 23 | -0.023594 | 4.735 |
| w28 | 19 | 0.087708 | 6.373 |
| w29 | 24 | 0.078731 | 7.13 |
| w30 | 30 | -0.008261 | -12.904 |
| w31 | 24 | -0.10666 | -30.444 |
| w32 | 22 | -0.159921 | -22.95 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.223387 | 30.227 |
| w2 | 17 | -0.265593 | -25.654 |
| w3 | 13 | -0.076597 | -6.83 |
| w4 | 20 | -0.091344 | -16.603 |
| w5 | 19 | 0.15096 | 20.426 |
| w6 | 13 | 0.193172 | 37.737 |
| w7 | 17 | 0.041519 | 2.214 |
| w8 | 24 | 0.171216 | 7.7 |
| w9 | 26 | 0.173341 | 15.267 |
| w10 | 12 | -0.034415 | 0.116 |
| w11 | 19 | 0.017372 | -1.006 |
| w12 | 18 | 0.011334 | -9.298 |
| w13 | 21 | 0.211495 | 30.73 |
| w14 | 23 | 0.082349 | 14.561 |
| w15 | 26 | 0.038869 | 9.04 |
| w16 | 17 | -0.205328 | -16.174 |
| w17 | 16 | 0.252205 | 28.771 |
| w18 | 19 | -0.0154 | -6.466 |
| w19 | 24 | 0.03129 | -3.426 |
| w20 | 19 | 0.040525 | -1.85 |
| w21 | 18 | 0.137953 | 10.313 |
| w22 | 19 | 0.026923 | 2.824 |
| w23 | 22 | -0.0536 | -7.376 |
| w24 | 21 | 0.110442 | 11.637 |
| w25 | 20 | 0.063994 | 5.528 |
| w26 | 26 | 0.141165 | 6.123 |
| w27 | 17 | 0.005202 | 6.172 |
| w28 | 25 | -0.017887 | -3.222 |
| w29 | 19 | 0.227524 | 26.285 |
| w30 | 21 | 0.05569 | 1.873 |
| w31 | 20 | -0.000716 | -9.85 |
| w32 | 24 | -0.044962 | -12.55 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 20 | 0.023014 | 13.063 |
| w7 | 18 | 0.072793 | 1.297 |
| w8 | 24 | 0.120499 | 0.627 |
| w9 | 26 | 0.14366 | 21.077 |
| w10 | 18 | 0.152883 | 12.718 |
| w11 | 20 | 0.001582 | -0.564 |
| w12 | 25 | -0.086622 | -19.247 |
| w13 | 18 | 0.035164 | -2.583 |
| w14 | 19 | 0.114662 | 14.729 |
| w15 | 29 | -0.043446 | -0.623 |
| w16 | 12 | 0.047278 | 13.96 |
| w17 | 16 | 0.268005 | 25.752 |
| w18 | 26 | 0.121336 | 9.463 |
| w19 | 24 | 0.108685 | 1.583 |
| w20 | 11 | -0.051553 | -12.783 |
| w21 | 20 | 0.218259 | 40.794 |
| w22 | 23 | 0.268664 | 56.244 |
| w23 | 23 | -0.023571 | 0.737 |
| w24 | 21 | 0.09933 | 11.102 |
| w25 | 19 | -0.05396 | -7.612 |
| w26 | 18 | 0.003065 | -2.697 |
| w27 | 19 | -0.06329 | 8.717 |
| w28 | 20 | 0.078295 | 7.719 |
| w29 | 20 | 0.017521 | 4.03 |
| w30 | 23 | -0.027091 | -13.8 |
| w31 | 24 | -0.084157 | -23.686 |
| w32 | 26 | -0.136612 | -25.721 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 21 | 0.063269 | 3.039 |
| w8 | 22 | 0.178359 | 8.098 |
| w9 | 30 | -0.128412 | -32.448 |
| w10 | 17 | 0.059898 | 8.209 |
| w11 | 18 | 0.009643 | -0.359 |
| w12 | 17 | -0.046581 | -17.884 |
| w13 | 18 | 0.085585 | 9.557 |
| w14 | 17 | 0.133751 | 12.447 |
| w15 | 27 | 0.041573 | 0.847 |
| w16 | 19 | -0.122443 | -8.181 |
| w17 | 16 | 0.1563 | 15.014 |
| w18 | 19 | 0.076314 | 1.667 |
| w19 | 20 | 0.065504 | -3.152 |
| w20 | 23 | 0.050943 | -6.397 |
| w21 | 20 | 0.163545 | 8.088 |
| w22 | 18 | -0.062171 | -10.079 |
| w23 | 17 | 0.231412 | 54.046 |
| w24 | 22 | 0.196796 | 25.299 |
| w25 | 17 | 0.017062 | 2.304 |
| w26 | 25 | 0.014208 | -4.539 |
| w27 | 17 | 0.00222 | -1.185 |
| w28 | 20 | 0.080444 | 5.168 |
| w29 | 18 | 0.13433 | 13.662 |
| w30 | 22 | 0.107941 | 8.563 |
| w31 | 17 | 0.198362 | 14.106 |
| w32 | 26 | -0.099185 | -36.245 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.085388 | 3.423 |
| w2 | 19 | 0.030973 | 1.473 |
| w3 | 26 | 0.187157 | 19.928 |
| w4 | 12 | -0.057774 | -1.677 |
| w5 | 22 | 0.042651 | 14.817 |
| w6 | 22 | 0.086827 | 20.024 |
| w7 | 23 | 0.006976 | -1.226 |
| w8 | 26 | 0.219477 | 16.083 |
| w9 | 29 | 0.0844 | -2.319 |
| w10 | 17 | 0.153134 | 14.745 |
| w11 | 19 | -0.016285 | -1.497 |
| w12 | 23 | -0.020205 | -10.549 |
| w13 | 24 | 0.02743 | 1.088 |
| w14 | 24 | 0.127356 | 23.124 |
| w15 | 22 | -0.024693 | -3.026 |
| w16 | 20 | 0.018899 | 11.217 |
| w17 | 15 | 0.281887 | 38.965 |
| w18 | 25 | 0.096448 | 11.032 |
| w19 | 27 | -0.043994 | -10.581 |
| w20 | 23 | -0.043284 | -20.847 |
| w21 | 20 | 0.180792 | 12.978 |
| w22 | 19 | 0.081624 | 14.131 |
| w23 | 28 | 0.059734 | -1.393 |
| w24 | 22 | -0.005822 | 5.054 |
| w25 | 20 | 0.096776 | 15.2 |
| w26 | 24 | 0.026295 | -9.44 |
| w27 | 19 | -0.04271 | -3.344 |
| w28 | 24 | 0.095912 | 2.445 |
| w29 | 20 | 0.079532 | 19.166 |
| w30 | 26 | -0.085837 | -16.627 |
| w31 | 27 | -0.07136 | -20.926 |
| w32 | 27 | -0.135309 | -21.232 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 17 | 0.056462 | 8.515 |
| w11 | 18 | 0.028076 | -1.507 |
| w12 | 20 | -0.014769 | -9.045 |
| w13 | 15 | -0.014488 | -9.454 |
| w14 | 20 | 0.276329 | 39.798 |
| w15 | 25 | -0.012691 | -3.044 |
| w16 | 14 | -0.042011 | 3.292 |
| w17 | 13 | 0.297864 | 46.4 |
| w18 | 24 | 0.062725 | -4.582 |
| w19 | 21 | -0.007512 | -7.647 |
| w20 | 18 | 0.005826 | -10.274 |
| w21 | 24 | 0.071415 | -5.231 |
| w22 | 16 | 0.002362 | 3.34 |
| w23 | 21 | -0.0244 | -10.306 |
| w24 | 20 | -0.107675 | -4.291 |
| w25 | 16 | 0.079777 | 4.29 |
| w26 | 23 | 0.026362 | -4.342 |
| w27 | 19 | -0.000467 | 3.334 |
| w28 | 24 | 0.008547 | -1.553 |
| w29 | 27 | 0.098169 | 11.594 |
| w30 | 27 | 0.064557 | -6.148 |
| w31 | 18 | -0.025086 | -9.487 |
| w32 | 19 | -0.304738 | -45.487 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 22 | -0.051496 | -3.934 |
| w13 | 16 | 0.034033 | -5.247 |
| w14 | 20 | 0.143566 | 25.88 |
| w15 | 26 | 0.13944 | 12.953 |
| w16 | 21 | -0.021734 | 1.88 |
| w17 | 23 | 0.165732 | 19.766 |
| w18 | 18 | 0.087101 | 8.948 |
| w19 | 19 | 0.044707 | -4.93 |
| w20 | 22 | -0.072882 | -19.767 |
| w21 | 16 | 0.010687 | -6.649 |
| w22 | 18 | 0.193721 | 19.213 |
| w23 | 18 | 0.01259 | -12.798 |
| w24 | 25 | 0.084876 | 14.102 |
| w25 | 17 | 0.114132 | 8.69 |
| w26 | 24 | -0.036463 | -20.194 |
| w27 | 20 | 0.025206 | -1.832 |
| w28 | 18 | 0.045103 | -0.367 |
| w29 | 24 | -0.080828 | -13.577 |
| w30 | 20 | -0.001655 | -16.454 |
| w31 | 19 | -0.059321 | -11.5 |
| w32 | 22 | 0.043293 | -3.697 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 21 | 0.124398 | 10.244 |
| w16 | 22 | -0.138991 | -7.977 |
| w17 | 20 | 0.33256 | 48.635 |
| w18 | 18 | 0.278382 | 58.136 |
| w19 | 20 | -0.013502 | -15.412 |
| w20 | 25 | 0.017079 | -6.548 |
| w21 | 18 | 0.088594 | 2.169 |
| w22 | 19 | 0.163164 | 17.776 |
| w23 | 18 | -0.01518 | -14.638 |
| w24 | 17 | 0.083425 | 17.373 |
| w25 | 13 | 0.087976 | 5.47 |
| w26 | 17 | -0.114773 | -19.866 |
| w27 | 16 | -0.093324 | -8.111 |
| w28 | 15 | 0.234553 | 17.791 |
| w29 | 17 | 0.078773 | 5.44 |
| w30 | 24 | 0.055628 | -7.537 |
| w31 | 17 | -0.108472 | -16.793 |
| w32 | 22 | -0.095316 | -15.964 |

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
| w15 | 20 | 0.075172 | 7.942 |
| w16 | 22 | 0.028231 | 19.702 |
| w17 | 15 | 0.221755 | 14.76 |
| w18 | 20 | 0.081964 | 4.442 |
| w19 | 17 | -0.026978 | -6.748 |
| w20 | 18 | 0.288484 | 40.598 |
| w21 | 18 | 0.124375 | 0.586 |
| w22 | 18 | 0.199625 | 27.19 |
| w23 | 16 | -0.001782 | -3.0 |
| w24 | 20 | 0.040297 | 8.54 |
| w25 | 18 | 0.019944 | -1.509 |
| w26 | 22 | -0.014227 | 0.415 |
| w27 | 17 | -0.017463 | 4.204 |
| w28 | 26 | 0.070833 | 5.723 |
| w29 | 11 | -0.017425 | 0.591 |
| w30 | 26 | 0.117998 | 0.047 |
| w31 | 26 | 0.041054 | 5.523 |
| w32 | 19 | -0.142582 | -16.106 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 19 | 0.023978 | 6.87 |
| w17 | 22 | 0.177406 | 36.491 |
| w18 | 24 | 0.151761 | 15.189 |
| w19 | 22 | -0.061756 | -13.957 |
| w20 | 19 | 0.168621 | 11.947 |
| w21 | 27 | 0.093588 | -6.042 |
| w22 | 17 | 0.129523 | 13.122 |
| w23 | 25 | -0.03237 | -20.058 |
| w24 | 24 | -0.010865 | -0.55 |
| w25 | 18 | 0.081131 | 2.858 |
| w26 | 20 | -0.129585 | -23.33 |
| w27 | 20 | -0.020308 | -5.975 |
| w28 | 18 | 0.000965 | -5.887 |
| w29 | 19 | 0.010217 | -3.779 |
| w30 | 23 | 0.108988 | 1.75 |
| w31 | 17 | -0.09324 | -16.256 |
| w32 | 25 | -0.017306 | -13.905 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 17 | 0.109794 | 8.006 |
| w21 | 19 | -0.020677 | -15.236 |
| w22 | 19 | 0.071902 | 7.864 |
| w23 | 20 | -0.02997 | -14.426 |
| w24 | 19 | 0.110971 | 28.379 |
| w25 | 19 | 0.191707 | 20.249 |
| w26 | 22 | 0.024291 | -4.536 |
| w27 | 21 | -0.04429 | -1.34 |
| w28 | 21 | 0.055732 | 0.676 |
| w29 | 22 | -0.11251 | -12.408 |
| w30 | 22 | 0.023883 | -5.059 |
| w31 | 18 | 0.104301 | 2.869 |
| w32 | 24 | -0.032005 | -16.382 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 18 | 0.195523 | 23.136 |
| w23 | 14 | -0.011611 | -7.766 |
| w24 | 20 | 0.06446 | 17.477 |
| w25 | 20 | 0.133109 | 23.307 |
| w26 | 19 | -0.109234 | -14.862 |
| w27 | 13 | 0.106054 | 10.344 |
| w28 | 21 | -0.002778 | -8.401 |
| w29 | 21 | 0.054569 | 3.49 |
| w30 | 22 | -0.008863 | -6.121 |
| w31 | 22 | -0.060183 | -13.544 |
| w32 | 19 | 0.010374 | 15.952 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 22 | 0.173946 | 27.457 |
| w25 | 12 | -0.044465 | -5.582 |
| w26 | 23 | 0.06319 | 7.433 |
| w27 | 13 | 0.078691 | 10.916 |
| w28 | 24 | 0.152631 | 18.837 |
| w29 | 22 | 0.073153 | 8.229 |
| w30 | 27 | 0.174052 | 12.859 |
| w31 | 19 | -0.157221 | -20.942 |
| w32 | 19 | -0.052347 | -3.892 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 17 | 0.045877 | 10.235 |
| w6 | 21 | 0.142317 | 24.819 |
| w7 | 20 | 0.107889 | 5.98 |
| w8 | 20 | 0.117261 | 7.191 |
| w9 | 28 | 0.146344 | 1.198 |
| w10 | 15 | 0.054394 | 5.333 |
| w11 | 24 | 0.179735 | 22.445 |
| w12 | 19 | 0.140247 | 10.232 |
| w13 | 20 | -0.000387 | 3.558 |
| w14 | 21 | 0.032146 | 6.799 |
| w15 | 19 | 0.047117 | 1.405 |
| w16 | 17 | -0.081017 | -3.663 |
| w17 | 20 | 0.278257 | 36.652 |
| w18 | 18 | 0.005548 | 0.933 |
| w19 | 16 | -0.027963 | -5.643 |
| w20 | 15 | -0.02516 | -6.452 |
| w21 | 13 | -0.037564 | -12.368 |
| w22 | 17 | 0.239252 | 27.404 |
| w23 | 14 | -0.042025 | -8.664 |
| w24 | 22 | 0.110552 | 13.111 |
| w25 | 21 | 0.040102 | -1.983 |
| w26 | 17 | -0.098926 | -10.405 |
| w27 | 19 | -0.117941 | -13.363 |
| w28 | 17 | 0.094257 | 5.768 |
| w29 | 30 | 0.018388 | 1.022 |
| w30 | 15 | 0.052594 | 18.261 |
| w31 | 17 | -0.004391 | -3.148 |
| w32 | 17 | 0.018477 | 6.589 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 17 | -0.087225 | -1.822 |
| w6 | 19 | 0.288043 | 44.375 |
| w7 | 23 | 0.169151 | 15.307 |
| w8 | 27 | 0.175842 | 13.425 |
| w9 | 21 | 0.160386 | 10.605 |
| w10 | 18 | -0.020546 | -2.389 |
| w11 | 21 | -0.00434 | -1.689 |
| w12 | 19 | 0.090535 | 0.145 |
| w13 | 22 | 0.080298 | 8.569 |
| w14 | 19 | 0.240449 | 35.337 |
| w15 | 27 | 0.103853 | 14.969 |
| w16 | 21 | 0.046131 | 18.087 |
| w17 | 18 | 0.288519 | 41.293 |
| w18 | 22 | -0.011194 | -8.549 |
| w19 | 23 | 0.009052 | -2.085 |
| w20 | 20 | -0.009647 | -5.327 |
| w21 | 20 | 0.118902 | 4.282 |
| w22 | 19 | 0.104475 | 8.606 |
| w23 | 20 | 0.058874 | -5.063 |
| w24 | 22 | -0.051006 | -8.301 |
| w25 | 26 | 0.215374 | 22.072 |
| w26 | 20 | 0.286457 | 32.747 |
| w27 | 22 | 0.010347 | -3.259 |
| w28 | 15 | 0.154281 | 12.708 |
| w29 | 25 | 0.004378 | -3.734 |
| w30 | 24 | 0.010706 | 6.126 |
| w31 | 15 | 0.071858 | 7.696 |
| w32 | 19 | 0.04338 | 9.431 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 21 | 0.097085 | 9.867 |
| w18 | 21 | 0.059499 | 15.685 |
| w19 | 17 | 0.145694 | 9.041 |
| w20 | 16 | -0.062938 | -12.707 |
| w21 | 17 | 0.169085 | 3.937 |
| w22 | 15 | 0.099549 | 11.008 |
| w23 | 22 | 0.135558 | 3.177 |
| w24 | 18 | 0.27165 | 36.54 |
| w25 | 20 | 0.261662 | 30.171 |
| w26 | 24 | 0.097271 | 6.253 |
| w27 | 18 | 0.195022 | 41.665 |
| w28 | 19 | 0.161188 | 15.509 |
| w29 | 18 | -0.101066 | -12.824 |
| w30 | 28 | 0.004318 | -10.684 |
| w31 | 22 | 0.007182 | -9.77 |
| w32 | 20 | -0.052194 | -8.082 |

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
| w17 | 21 | 0.138305 | 18.17 |
| w18 | 24 | 0.017248 | -2.68 |
| w19 | 19 | 0.153226 | 12.668 |
| w20 | 21 | 0.054513 | 2.409 |
| w21 | 17 | 0.099697 | 4.321 |
| w22 | 17 | -0.006086 | -0.536 |
| w23 | 16 | 0.113606 | 11.758 |
| w24 | 20 | -0.067783 | -3.308 |
| w25 | 13 | 0.012214 | 2.492 |
| w26 | 18 | -0.200299 | -18.682 |
| w27 | 19 | 0.056722 | 16.185 |
| w28 | 20 | 0.166302 | 13.262 |
| w29 | 16 | 0.031994 | 6.21 |
| w30 | 25 | 0.098702 | 0.372 |
| w31 | 20 | -0.024551 | -11.801 |
| w32 | 18 | -0.139203 | -13.849 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 23 | -0.112174 | -21.749 |
| w20 | 17 | 0.077735 | 8.316 |
| w21 | 20 | -0.008759 | -4.626 |
| w22 | 17 | -0.13469 | -7.54 |
| w23 | 20 | 0.029316 | -2.83 |
| w24 | 18 | 0.091791 | 25.201 |
| w25 | 16 | 0.026428 | -3.953 |
| w26 | 21 | 0.021825 | -3.173 |
| w27 | 18 | -0.021785 | -2.774 |
| w28 | 20 | -0.029575 | -11.656 |
| w29 | 20 | -0.023641 | -4.03 |
| w30 | 26 | -0.005629 | -15.003 |
| w31 | 22 | -0.096194 | -14.614 |
| w32 | 22 | -0.010242 | 1.54 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 22 | 0.181326 | 23.204 |
| w23 | 22 | 0.110741 | 6.424 |
| w24 | 17 | 0.170793 | 24.253 |
| w25 | 22 | -0.030387 | -9.341 |
| w26 | 23 | 0.102181 | 4.506 |
| w27 | 18 | -0.084967 | -8.58 |
| w28 | 17 | 0.087219 | 4.741 |
| w29 | 15 | -0.014639 | -0.866 |
| w30 | 22 | 0.12409 | 7.109 |
| w31 | 27 | -0.048591 | -18.052 |
| w32 | 15 | -0.08479 | -7.758 |

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
| w27 | 25 | 0.095586 | 17.639 |
| w28 | 23 | 0.165007 | 15.446 |
| w29 | 23 | -0.021518 | -5.75 |
| w30 | 25 | -0.00681 | -12.546 |
| w31 | 21 | -0.04713 | -12.295 |
| w32 | 16 | 0.048005 | 8.404 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 22 | 0.245386 | 21.159 |
| w18 | 17 | -0.047664 | -17.725 |
| w19 | 22 | 0.042215 | -6.245 |
| w20 | 18 | -0.01228 | -7.633 |
| w21 | 16 | -0.028057 | -14.079 |
| w22 | 17 | 0.147601 | 20.918 |
| w23 | 21 | 0.058559 | -6.148 |
| w24 | 21 | 0.065488 | 11.38 |
| w25 | 12 | 0.062108 | 3.173 |
| w26 | 19 | 0.019055 | -5.063 |
| w27 | 18 | -0.021799 | -1.661 |
| w28 | 19 | -0.013495 | -7.77 |
| w29 | 23 | 0.148207 | 11.275 |
| w30 | 19 | -0.125871 | -26.297 |
| w31 | 15 | 0.059988 | -1.224 |
| w32 | 24 | 0.098677 | 9.084 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 19 | 0.275909 | 30.801 |
| w18 | 15 | 0.073978 | 5.55 |
| w19 | 23 | 0.047098 | -4.664 |
| w20 | 17 | 0.097512 | 6.004 |
| w21 | 15 | 0.013482 | -10.862 |
| w22 | 18 | 0.129181 | 24.568 |
| w23 | 13 | -0.099837 | -16.124 |
| w24 | 20 | 0.1275 | 20.645 |
| w25 | 17 | 0.006866 | 1.564 |
| w26 | 21 | -0.014006 | -10.135 |
| w27 | 23 | -0.078874 | -9.915 |
| w28 | 22 | 0.062369 | -2.323 |
| w29 | 19 | 0.039898 | -0.06 |
| w30 | 19 | 0.048452 | -9.076 |
| w31 | 21 | -0.00048 | -10.72 |
| w32 | 25 | 0.141662 | 6.803 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 23 | 0.081355 | 7.153 |
| w29 | 26 | 0.01231 | -2.115 |
| w30 | 20 | 0.048622 | 7.934 |
| w31 | 24 | -0.107178 | -14.131 |
| w32 | 23 | 0.018856 | 5.906 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 13 | -0.024322 | 0.362 |
| w15 | 12 | 0.015546 | 1.875 |
| w16 | 14 | 0.016591 | 19.24 |
| w17 | 10 | 0.068212 | 6.497 |
| w18 | 15 | 0.061741 | 3.698 |
| w19 | 24 | 0.109442 | 11.68 |
| w20 | 24 | 0.139726 | 8.693 |
| w21 | 14 | 0.070138 | 8.457 |
| w22 | 21 | 0.03767 | 7.681 |
| w23 | 16 | 0.121967 | 9.512 |
| w24 | 19 | 0.096055 | 18.65 |
| w25 | 17 | -0.068506 | -5.525 |
| w26 | 21 | 0.01792 | -3.597 |
| w27 | 18 | -0.04592 | 3.062 |
| w28 | 21 | 0.055794 | 1.007 |
| w29 | 23 | -0.03597 | -3.84 |
| w30 | 21 | 0.006824 | -6.075 |
| w31 | 19 | -0.075685 | -12.169 |
| w32 | 21 | -0.04616 | -14.71 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 28 | 0.095032 | 19.433 |
| w26 | 24 | 0.076706 | 6.164 |
| w27 | 17 | -0.079874 | -5.97 |
| w28 | 19 | 0.031565 | -3.381 |
| w29 | 23 | -0.034762 | -3.412 |
| w30 | 20 | 0.03934 | -4.569 |
| w31 | 19 | 0.106157 | 7.835 |
| w32 | 27 | -0.084785 | -19.993 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

