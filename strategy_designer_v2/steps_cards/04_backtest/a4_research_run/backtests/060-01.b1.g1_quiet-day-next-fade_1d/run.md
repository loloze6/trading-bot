# Backtest of 060-01.b1.g1_quiet-day-next-fade_1d

- Plan: `../../../../03_test_plan/a4_research_run/plans/060-01.b1.g1_quiet-day-next-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, AVAX, ZEC, CRV, FIL, TAO, DOGE, ONDO as BCHUSD, AVAXUSD, ZECUSD, CRVUSD, FILUSD, TAOUSD, DOGEUSD, ONDOUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 26 | -0.168497 | -20.358 |
| w8 | 22 | -0.137054 | -17.138 |
| w9 | 26 | 0.220711 | 67.439 |
| w10 | 22 | -0.020209 | -25.027 |
| w11 | 27 | -0.001431 | -8.306 |
| w12 | 19 | -0.065639 | -11.914 |
| w13 | 30 | -0.039191 | -26.462 |
| w14 | 28 | 0.086815 | -0.781 |
| w15 | 24 | 0.030089 | -9.267 |
| w16 | 21 | 0.164127 | 4.871 |
| w17 | 27 | 0.166145 | 14.919 |
| w18 | 26 | 0.066958 | 5.496 |
| w19 | 18 | -0.016019 | -4.663 |
| w20 | 23 | -0.033572 | -2.502 |
| w21 | 22 | 0.08386 | 7.192 |
| w22 | 20 | -0.087646 | -23.319 |
| w23 | 28 | 0.010317 | -24.131 |
| w24 | 21 | 0.026957 | -7.754 |
| w25 | 24 | 0.132189 | 1.798 |
| w26 | 23 | -0.052384 | -12.828 |
| w27 | 20 | -0.055284 | -19.435 |
| w28 | 23 | -0.17626 | -29.311 |
| w29 | 24 | -0.06556 | -25.858 |
| w30 | 26 | -0.046928 | -20.466 |
| w31 | 23 | 0.075123 | 11.333 |
| w32 | 23 | 0.076284 | 10.47 |

- AVAXUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18, w19 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 19 | 0.056355 | 13.861 |
| w21 | 31 | -0.042791 | -1.962 |
| w22 | 19 | -0.086617 | -19.335 |
| w23 | 21 | -0.005337 | 2.821 |
| w24 | 22 | -0.060378 | -37.908 |
| w25 | 16 | -0.047491 | -6.67 |
| w26 | 22 | 0.106417 | 16.811 |
| w27 | 16 | 0.00804 | -7.955 |
| w28 | 24 | -0.111525 | -12.431 |
| w29 | 16 | 0.006391 | -5.139 |
| w30 | 24 | -0.062733 | -6.551 |
| w31 | 20 | 0.001537 | 3.099 |
| w32 | 23 | 0.002583 | -1.794 |

- ZECUSD: 28 of 32 windows run. 4 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 27 | 0.033214 | -17.963 |
| w6 | 20 | -0.114965 | -26.47 |
| w7 | 20 | 0.017046 | 0.391 |
| w8 | 20 | 0.017008 | 3.452 |
| w9 | 22 | 0.155531 | 31.284 |
| w10 | 16 | 0.126849 | 5.211 |
| w11 | 22 | -0.138698 | -21.936 |
| w12 | 21 | -0.05739 | -4.911 |
| w13 | 23 | 0.070737 | -2.91 |
| w14 | 18 | 0.045122 | -7.121 |
| w15 | 22 | 0.14352 | 18.585 |
| w16 | 19 | -0.025346 | -19.252 |
| w17 | 19 | 0.001946 | -2.482 |
| w18 | 25 | 0.189622 | 30.632 |
| w19 | 21 | -0.145051 | -19.483 |
| w20 | 26 | 0.148739 | 24.61 |
| w21 | 26 | 0.046517 | 7.985 |
| w22 | 15 | -0.091865 | -12.745 |
| w23 | 27 | 0.022789 | 9.865 |
| w24 | 20 | 0.290028 | 27.646 |
| w25 | 17 | 0.124377 | 17.391 |
| w26 | 27 | -0.039661 | -17.792 |
| w27 | 28 | -0.040885 | -23.397 |
| w28 | 25 | -0.035138 | -5.03 |
| w29 | 18 | 0.20852 | 25.03 |
| w30 | 24 | -0.030781 | -28.512 |
| w31 | 28 | 0.043532 | 3.959 |
| w32 | 23 | 0.045593 | -16.163 |

- CRVUSD: 16 of 32 windows run. 15 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 23 | -0.040804 | -13.328 |
| w18 | 22 | 0.069085 | -4.114 |
| w19 | 18 | 0.085402 | 13.544 |
| w20 | 22 | 0.089942 | 10.351 |
| w21 | 23 | -0.035121 | -4.613 |
| w22 | 18 | 0.06396 | -1.139 |
| w23 | 19 | 0.062282 | 19.779 |
| w24 | 24 | 0.043358 | -7.013 |
| w25 | 24 | 0.010617 | -4.182 |
| w26 | 25 | -0.031221 | -7.37 |
| w27 | 17 | 0.07566 | -12.1 |
| w28 | 22 | -0.066917 | -13.218 |
| w29 | 24 | 0.005886 | -7.91 |
| w30 | 23 | -0.131566 | -15.916 |
| w31 | 22 | 0.074989 | 11.11 |
| w32 | 24 | 0.082771 | -1.457 |

- w16 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_CRVUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- FILUSD: 16 of 32 windows run. 16 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 25 | 0.021942 | 3.535 |
| w18 | 20 | -0.050844 | -10.325 |
| w19 | 20 | -0.096271 | -10.921 |
| w20 | 22 | -0.096323 | -19.488 |
| w21 | 19 | -0.168691 | -12.189 |
| w22 | 17 | -0.001387 | -14.96 |
| w23 | 25 | -0.156446 | -23.673 |
| w24 | 22 | 0.124385 | -1.209 |
| w25 | 17 | -0.017122 | -7.805 |
| w26 | 25 | -0.004103 | -2.602 |
| w27 | 16 | -0.059604 | -18.927 |
| w28 | 20 | 0.073865 | 10.54 |
| w29 | 19 | -0.044175 | -10.063 |
| w30 | 24 | 0.100159 | 17.7 |
| w31 | 24 | -0.060324 | -7.205 |
| w32 | 19 | 0.074564 | 8.588 |

- TAOUSD: 5 of 32 windows run. 27 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18, w19, w20, w21, w22, w23, w24, w25, w26, w27 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 21 | 0.123295 | 18.292 |
| w29 | 24 | 0.019895 | 1.849 |
| w30 | 18 | -0.053676 | -14.491 |
| w31 | 21 | 0.031378 | -1.855 |
| w32 | 22 | 0.035118 | -0.052 |

- DOGEUSD: 19 of 32 windows run. 13 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 20 | -0.035771 | -12.397 |
| w15 | 31 | 0.096464 | 2.409 |
| w16 | 25 | 0.117907 | -6.589 |
| w17 | 26 | 0.093921 | 7.822 |
| w18 | 29 | 0.042853 | 9.859 |
| w19 | 27 | -0.047618 | -9.204 |
| w20 | 25 | -0.034796 | 1.436 |
| w21 | 23 | 0.102627 | 10.241 |
| w22 | 21 | -0.074217 | -14.527 |
| w23 | 25 | 0.006675 | 0.625 |
| w24 | 22 | -0.010241 | -10.798 |
| w25 | 24 | -0.079074 | -29.887 |
| w26 | 19 | -0.067151 | -9.538 |
| w27 | 23 | 0.033145 | -16.413 |
| w28 | 22 | -0.038197 | -1.366 |
| w29 | 21 | -0.040306 | -13.62 |
| w30 | 18 | -0.087709 | -6.794 |
| w31 | 26 | -0.0196 | -5.935 |
| w32 | 23 | -0.047861 | -10.133 |

- ONDOUSD: 6 of 32 windows run. 26 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18, w19, w20, w21, w22, w23, w24, w25, w26 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w27 | 15 | 0.086152 | -0.24 |
| w28 | 23 | -0.050839 | -7.029 |
| w29 | 16 | 0.002792 | -2.67 |
| w30 | 22 | 0.07998 | 18.231 |
| w31 | 23 | 0.029307 | 7.318 |
| w32 | 21 | 0.070665 | -0.736 |

